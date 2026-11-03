#!/usr/bin/env python3
"""Biblioteca de escritura íntegra en libros V6.3 (pieza 1 del encargo, §11).

Escribe valores en celdas de entrada directamente en el XML del paquete .xlsx, sin pasar por
openpyxl (que pierde los deslizadores y reescribe los gráficos, §1.4 del encargo). Todo lo que no
es una hoja modificada se copia byte a byte, así que `verificar_v63.py` sigue dando 0.

Reglas:
  - nunca escribe en una celda con fórmula (error FormulaProtegida);
  - respeta el estilo (atributo s) de la celda, que es lo que da el formato dd/mm/yyyy a las fechas
    de Palancas!B38:B40 y el formato % a las palancas;
  - texto → cadena inline (<is><t>); número → <v>; fecha ISO → serial de Excel; None → celda vacía;
  - `borrar_caches()` elimina el <v> de toda celda con <f> para que LibreOffice recalcule de verdad
    (trampa de §1.4: con cachés, `soffice --convert-to` conserva los valores viejos).
"""
import datetime as _dt
import re
import zipfile
from copy import copy

from lxml import etree

NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
RNS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
_RE_REF = re.compile(r"^([A-Z]{1,3})(\d+)$")


class FormulaProtegida(Exception):
    pass


class CeldaNoPermitida(Exception):
    pass


def col_a_num(col):
    n = 0
    for ch in col:
        n = n * 26 + (ord(ch) - 64)
    return n


def partir_ref(ref):
    m = _RE_REF.match(ref)
    if not m:
        raise ValueError(f"referencia de celda inválida: {ref!r}")
    return m.group(1), int(m.group(2))


def serial_excel(fecha):
    """ISO 'AAAA-MM-DD' (o date/datetime) → serial de Excel (base 1899-12-30)."""
    if isinstance(fecha, str):
        fecha = _dt.date.fromisoformat(fecha)
    if isinstance(fecha, _dt.datetime):
        fecha = fecha.date()
    return (fecha - _dt.date(1899, 12, 30)).days


def _texto_numero(valor):
    if isinstance(valor, bool):
        raise TypeError("los booleanos no son un tipo de celda de la V6.3")
    if isinstance(valor, int):
        return str(valor)
    r = repr(float(valor))
    if r.endswith(".0"):
        r = r[:-2]
    return r


class LibroV63:
    """Un .xlsx abierto como paquete. Solo modifica las hojas en las que se escribe."""

    def __init__(self, path):
        self.path = path
        z = zipfile.ZipFile(path)
        self._infos = z.infolist()
        self._datos = {i.filename: z.read(i.filename) for i in self._infos}
        z.close()
        wb = etree.fromstring(self._datos["xl/workbook.xml"])
        rels = etree.fromstring(self._datos["xl/_rels/workbook.xml.rels"])
        rid2t = {r.get("Id"): r.get("Target") for r in rels}
        self.partes = {}  # nombre de hoja → ruta de la parte
        for s in wb.find(f"{{{NS}}}sheets"):
            t = rid2t[s.get(f"{{{RNS}}}id")]
            t = t.lstrip("/")
            if not t.startswith("xl/"):
                t = "xl/" + t
            self.partes[s.get("name")] = t
        self._arboles = {}
        self._modificadas = set()

    # ---- acceso ----
    def hojas(self):
        return list(self.partes)

    def _arbol(self, hoja):
        if hoja not in self.partes:
            raise KeyError(f"hoja desconocida: {hoja!r}")
        if hoja not in self._arboles:
            self._arboles[hoja] = etree.fromstring(self._datos[self.partes[hoja]])
        return self._arboles[hoja]

    def _celda(self, hoja, ref, crear=False):
        root = self._arbol(hoja)
        col, fila = partir_ref(ref)
        sd = root.find(f"{{{NS}}}sheetData")
        row = None
        for r in sd.findall(f"{{{NS}}}row"):
            rn = int(r.get("r"))
            if rn == fila:
                row = r
                break
            if rn > fila:
                if not crear:
                    return None
                row = etree.Element(f"{{{NS}}}row", r=str(fila))
                r.addprevious(row)
                break
        if row is None:
            if not crear:
                return None
            row = etree.SubElement(sd, f"{{{NS}}}row", r=str(fila))
        n = col_a_num(col)
        for c in row.findall(f"{{{NS}}}c"):
            ccol, _ = partir_ref(c.get("r"))
            cn = col_a_num(ccol)
            if cn == n:
                return c
            if cn > n:
                if not crear:
                    return None
                nueva = etree.Element(f"{{{NS}}}c", r=ref)
                c.addprevious(nueva)
                return nueva
        if not crear:
            return None
        return etree.SubElement(row, f"{{{NS}}}c", r=ref)

    def tiene_formula(self, hoja, ref):
        c = self._celda(hoja, ref)
        return c is not None and c.find(f"{{{NS}}}f") is not None

    def leer(self, hoja, ref):
        """Valor tal como está en el XML (texto, número o None). Para fórmulas devuelve ('=', f)."""
        c = self._celda(hoja, ref)
        if c is None:
            return None
        f = c.find(f"{{{NS}}}f")
        if f is not None:
            return ("=", f.text)
        t = c.get("t")
        if t == "inlineStr":
            is_ = c.find(f"{{{NS}}}is")
            return "".join(is_.itertext()) if is_ is not None else ""
        v = c.find(f"{{{NS}}}v")
        if v is None or v.text is None:
            return None
        if t in ("str", "s", "e"):
            return v.text
        if t == "b":
            return v.text == "1"
        x = float(v.text)
        return int(x) if x.is_integer() and "." not in v.text and "E" not in v.text.upper() else x

    def todas_las_celdas(self, hoja):
        """{ref: valor} de todas las celdas con contenido de la hoja (fórmulas como ('=', f))."""
        root = self._arbol(hoja)
        out = {}
        for c in root.iter(f"{{{NS}}}c"):
            ref = c.get("r")
            v = self.leer(hoja, ref) if False else None
            f = c.find(f"{{{NS}}}f")
            if f is not None:
                out[ref] = ("=", f.text)
                continue
            t = c.get("t")
            if t == "inlineStr":
                is_ = c.find(f"{{{NS}}}is")
                out[ref] = "".join(is_.itertext()) if is_ is not None else ""
                continue
            vv = c.find(f"{{{NS}}}v")
            if vv is None or vv.text is None:
                continue
            if t in ("str", "s", "e"):
                out[ref] = vv.text
            elif t == "b":
                out[ref] = vv.text == "1"
            else:
                x = float(vv.text)
                out[ref] = int(x) if x.is_integer() and "." not in vv.text and "E" not in vv.text.upper() else x
        return out

    # ---- escritura ----
    def escribir(self, hoja, ref, valor, tipo=None):
        """valor: str | int | float | None | 'AAAA-MM-DD' con tipo='fecha'."""
        c = self._celda(hoja, ref, crear=True)
        if c.find(f"{{{NS}}}f") is not None:
            raise FormulaProtegida(f"{hoja}!{ref} tiene fórmula: no se escribe")
        for hijo in list(c):
            c.remove(hijo)
        estilo = c.get("s")
        for k in list(c.attrib):
            if k not in ("r", "s"):
                del c.attrib[k]
        if estilo is not None:
            c.set("s", estilo)
        if valor is None or (isinstance(valor, str) and valor == "" and tipo != "texto"):
            c.set("t", "n")
            return
        if tipo == "fecha":
            c.set("t", "n")
            etree.SubElement(c, f"{{{NS}}}v").text = str(serial_excel(valor))
            return
        if isinstance(valor, (_dt.date, _dt.datetime)):
            c.set("t", "n")
            etree.SubElement(c, f"{{{NS}}}v").text = str(serial_excel(valor))
            return
        if isinstance(valor, (int, float)) and not isinstance(valor, bool):
            c.set("t", "n")
            etree.SubElement(c, f"{{{NS}}}v").text = _texto_numero(valor)
            return
        if isinstance(valor, str):
            c.set("t", "inlineStr")
            is_ = etree.SubElement(c, f"{{{NS}}}is")
            t = etree.SubElement(is_, f"{{{NS}}}t")
            t.text = valor
            if valor != valor.strip() or "\n" in valor:
                t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
            return
        raise TypeError(f"tipo no admitido para {hoja}!{ref}: {type(valor).__name__}")

    def vaciar(self, hoja, ref):
        self.escribir(hoja, ref, None)

    def borrar_caches(self, hojas=None):
        """Quita el <v> de toda celda con <f> (en todas las hojas o en las indicadas)."""
        n = 0
        for hoja in (hojas or self.partes):
            root = self._arbol(hoja)
            for c in root.iter(f"{{{NS}}}c"):
                if c.find(f"{{{NS}}}f") is None:
                    continue
                for v in c.findall(f"{{{NS}}}v"):
                    c.remove(v)
                    n += 1
            self._modificadas.add(hoja)
        return n

    def marcar_modificada(self, hoja):
        self._modificadas.add(hoja)

    # ---- guardado ----
    def guardar(self, destino):
        """Escribe el paquete: partes no tocadas byte a byte, hojas tocadas reserializadas."""
        nuevos = {}
        for hoja in self._modificadas | set(self._arboles):
            # una hoja parseada pero no escrita se deja en bytes originales
            if hoja not in self._modificadas:
                continue
            root = self._arboles[hoja]
            nuevos[self.partes[hoja]] = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
        with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as zout:
            for info in self._infos:
                i2 = copy(info)
                zout.writestr(i2, nuevos.get(info.filename, self._datos[info.filename]))
        return destino

    def escribir_celdas(self, celdas, permitidas=None):
        """celdas: {"Hoja!REF": valor | {"valor": v, "tipo": "fecha"|"texto"|"numero"} }.
        permitidas: {hoja: set(refs)} o None (sin lista blanca)."""
        escritas = []
        for clave, v in celdas.items():
            if "!" not in clave:
                raise ValueError(f"clave sin hoja: {clave!r} (usa 'Hoja!REF')")
            hoja, ref = clave.split("!", 1)
            if permitidas is not None and ref not in permitidas.get(hoja, set()):
                raise CeldaNoPermitida(f"{clave} no está en la lista blanca")
            tipo = None
            if isinstance(v, dict) and "valor" in v:
                tipo = v.get("tipo")
                v = v["valor"]
            if tipo == "numero" and isinstance(v, str):
                v = float(v.replace(",", "."))
            self.escribir(hoja, ref, v, tipo=tipo)
            self._modificadas.add(hoja)
            escritas.append(clave)
        return escritas
