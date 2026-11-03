#!/usr/bin/env python3
"""Genera la REFERENCIA APROBADA de una versión terminada.

Uso: python3 generar_referencia.py Plantilla_V6.3.xlsx referencia_V6.3.json [--version V6.3]

Se ejecuta UNA vez, sobre la plantilla final, DESPUÉS de que haya pasado las pruebas. La referencia
se entrega aparte con su identificación (SHA-256 del archivo del que salió). Nunca se regenera a
partir de un archivo sospechoso: eso convertiría la verificación en una tautología.

Qué captura:
  - el orden y los nombres de las hojas
  - la fórmula exacta de cada celda con fórmula
  - el valor exacto de cada celda fija (etiquetas, tablas, listas) que no está en el inventario
    de entradas editables (inventario_entradas.py)
  - el inventario de entradas editables
  - el contenido de las validaciones de datos, los formatos condicionales y los nombres definidos
  - el hash de cada parte de controles de formulario, dibujos y gráficos del paquete
"""
import hashlib
import json
import sys
import zipfile
from datetime import date

from openpyxl import load_workbook

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from inventario_entradas import ENTRADAS, PARAMETROS, conjunto_entradas  # noqa: E402

PARTES_PAQUETE = ("xl/ctrlProps/", "xl/drawings/", "xl/charts/", "xl/worksheets/_rels/")


def _ser(v):
    if isinstance(v, (int, float, str, bool)) or v is None:
        return v
    return str(v)


def capturar(path):
    wb = load_workbook(path)
    entradas = conjunto_entradas()
    formulas, fijos, validaciones, cf = {}, {}, {}, {}
    for ws in wb.worksheets:
        ent = entradas.get(ws.title, set())
        for row in ws.iter_rows():
            for c in row:
                if c.value is None:
                    continue
                k = f"{ws.title}!{c.coordinate}"
                if isinstance(c.value, str) and c.value.startswith("="):
                    formulas[k] = c.value
                elif c.coordinate not in ent:
                    fijos[k] = _ser(c.value)
        validaciones[ws.title] = sorted(
            [str(dv.sqref), dv.type or "", dv.operator or "", str(dv.formula1 or ""),
             str(dv.formula2 or ""), bool(dv.allow_blank)]
            for dv in ws.data_validations.dataValidation)
        reglas = []
        for rango in ws.conditional_formatting:
            for r in rango.rules:
                reglas.append([str(rango.sqref), r.type or "", r.operator or "", list(r.formula or [])])
        cf[ws.title] = sorted(reglas)
    nombres = {k: str(v.value) for k, v in wb.defined_names.items()}
    parametros = {}
    for k in sorted(PARAMETROS):
        h, c = k.split("!")
        parametros[k] = _ser(wb[h][c].value)
    z = zipfile.ZipFile(path)
    partes = {n: hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist()
              if any(n.startswith(p) for p in PARTES_PAQUETE)}
    return {
        "hojas": wb.sheetnames,
        "formulas": formulas,
        "fijos": fijos,
        "entradas": ENTRADAS,
        "validaciones": validaciones,
        "formato_condicional": cf,
        "nombres_definidos": nombres,
        "parametros": parametros,
        "partes_paquete": partes,
    }


def main():
    src, dst = sys.argv[1], sys.argv[2]
    version = sys.argv[sys.argv.index("--version") + 1] if "--version" in sys.argv else "V6.3"
    ref = capturar(src)
    ref.update({
        "version": version,
        "generada_desde": src.split("/")[-1],
        "sha256_origen": hashlib.sha256(open(src, "rb").read()).hexdigest(),
        "fecha": date.today().isoformat(),
    })
    json.dump(ref, open(dst, "w"), ensure_ascii=False, indent=0, sort_keys=True)
    print(f"referencia {version}: {len(ref['formulas'])} fórmulas · {len(ref['fijos'])} celdas fijas · "
          f"{sum(len(v) for v in ref['validaciones'].values())} validaciones · "
          f"{len(ref['partes_paquete'])} partes del paquete")
    print(f"origen: {ref['generada_desde']} · SHA-256 {ref['sha256_origen']}")
    print(f"-> {dst}")


if __name__ == "__main__":
    main()
