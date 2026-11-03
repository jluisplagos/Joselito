#!/usr/bin/env python3
"""Migra una V5.3 evaluada por el personaje v1 a la plantilla V6.3 (pipeline paso 1; encargo §4.7 y §11 pieza 2).

Uso: migrar_v53_a_v63.py etapa1/<E>_evaluada.xlsx Plantilla_V6.3.xlsx <E>_v63_base.xlsx [--config config_v2.json]

Copia SOLO la lista blanca de migrate_values.py (V6.1) intersecada con el inventario de entradas de la V6.3, escribiendo con
el método de la pieza 1 (XML directo: el libro sigue íntegro). Además:
  - normaliza Control maestro!D5 (ratio ADR) a número o vacío (un texto como «ADR» deja Motor!B253 en falso);
  - antepone «HEREDADO · V5.3 (fórmula en V6.3): » a la columna N de las filas 60, 65 y 70 de Control maestro (B67:D67);
  - no copia B67:D67 (fórmula en V6.3) ni ninguna celda que en la V6.3 sea fórmula;
  - deja <E>_v63_base.xlsx.conciliacion.json con cada valor del origen clasificado (conservado / excluido / transformado / conflicto).
Código 0 ok · 1 verificación fallida · 2 uso.
"""
import argparse
import json
import os
import subprocess
import sys

import openpyxl
from openpyxl.utils import get_column_letter, range_boundaries

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import config_v2  # noqa: E402
from v63_xml import LibroV63  # noqa: E402

WHITELIST = {
    "Análisis": ["B3", "D3", "B4", "D4", "C11:C14", "C17:C20", "C24:C28", "C31:C34", "C37", "C38", "C40", "C41", "C42",
                 "C46:C51", "C53:C57", "C60", "C61", "C62", "B65:D66", "B68:D69", "C76", "C88", "C93", "C96:C98", "B101", "B102", "C103", "C104"],
    "Control maestro": ["H4", "J4", "L4", "N4", "B5", "D5", "F5", "J5", "L5", "N5", "E17:N82", "C86:E102"],
}
TRANSFORMADAS = {"Análisis": ["B67:D67"]}
FILAS_HEREDADO = (60, 65, 70)
PREFIJO = "HEREDADO · V5.3 (fórmula en V6.3): "


def celdas(rng):
    c1, r1, c2, r2 = range_boundaries(rng)
    return {f"{get_column_letter(c)}{r}" for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("origen_v53")
    ap.add_argument("plantilla_v63")
    ap.add_argument("salida")
    ap.add_argument("--config", default=os.path.join(AQUI, "..", "config_v2.json"))
    a = ap.parse_args()
    cfg = config_v2.cargar(a.config)
    sys.path.insert(0, cfg["plantilla"]["scripts_v63"])
    import inventario_entradas  # noqa
    entradas = inventario_entradas.conjunto_entradas()
    wl = {h: set().union(*(celdas(x) for x in v)) & entradas.get(h, set()) for h, v in WHITELIST.items()}
    tr = {h: set().union(*(celdas(x) for x in v)) for h, v in TRANSFORMADAS.items()}
    src = openpyxl.load_workbook(a.origen_v53, data_only=True)
    libro = LibroV63(a.plantilla_v63)
    rec = {"origen": a.origen_v53, "plantilla": a.plantilla_v63, "conservados": [], "excluidos": [], "transformados": [], "conflictos": [], "normalizados": []}
    escritura = {}
    for hoja in WHITELIST:
        if hoja not in src.sheetnames:
            rec["conflictos"].append({"hoja": hoja, "motivo": "no existe en el origen"})
            continue
        ws = src[hoja]
        for fila in ws.iter_rows():
            for c in fila:
                v = c.value
                if v is None or (isinstance(v, str) and v.startswith("=")):
                    continue
                ref = c.coordinate
                e = {"hoja": hoja, "celda": ref, "valor": v if isinstance(v, (int, float)) else str(v)[:80]}
                if ref in tr.get(hoja, set()):
                    e["motivo"] = "en V6.3 es fórmula (calculado)"
                    rec["transformados"].append(e)
                    continue
                if ref not in wl[hoja]:
                    e["motivo"] = "etiqueta, texto fijo o celda fuera del inventario de entradas de la V6.3"
                    rec["excluidos"].append(e)
                    continue
                if libro.tiene_formula(hoja, ref):
                    e["motivo"] = "la celda destino es fórmula en V6.3"
                    rec["conflictos"].append(e)
                    continue
                if hasattr(v, "isoformat"):
                    escritura[f"{hoja}!{ref}"] = {"valor": v.date().isoformat() if hasattr(v, "date") else v.isoformat(), "tipo": "fecha"}
                else:
                    escritura[f"{hoja}!{ref}"] = v
                rec["conservados"].append(e)
    # D5 a número o vacío
    d5 = escritura.get("Control maestro!D5")
    if d5 is not None and not isinstance(d5, (int, float)):
        try:
            escritura["Control maestro!D5"] = float(str(d5).replace(",", "."))
        except ValueError:
            rec["normalizados"].append({"celda": "Control maestro!D5", "antes": d5, "despues": None, "motivo": "ratio ADR no numérico: se vacía (la fase 1 lo rellenará si procede)"})
            escritura["Control maestro!D5"] = None
    # prefijo HEREDADO en N de las filas de B67:D67
    for r in FILAS_HEREDADO:
        k = f"Control maestro!N{r}"
        if escritura.get(k) not in (None, ""):
            if not str(escritura[k]).startswith(PREFIJO):
                escritura[k] = PREFIJO + str(escritura[k])
                rec["normalizados"].append({"celda": k, "motivo": "prefijo HEREDADO añadido (S-16)"})
    libro.escribir_celdas(escritura, entradas)
    libro.borrar_caches()
    libro.guardar(a.salida)
    rec["resumen"] = {k: len(rec[k]) for k in ("conservados", "excluidos", "transformados", "conflictos", "normalizados")}
    json.dump(rec, open(a.salida + ".conciliacion.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print("OK:", a.salida, rec["resumen"])
    r = subprocess.run([sys.executable, cfg["plantilla"]["verificador"], a.salida, cfg["plantilla"]["referencia"]], capture_output=True, text=True)
    print((r.stdout.strip().splitlines() or [r.stderr])[-1])
    return 0 if r.returncode == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
