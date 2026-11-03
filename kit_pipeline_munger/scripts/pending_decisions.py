#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lista lo que falta en la PARTE AUTOMÁTICA de un Excel antes de pasarlo al personaje.

Detecta:
  1. Celdas de datos obligatorias vacías (C46, C47, C50; además C37, C53, C55).
  2. Filas de Control maestro de celdas de DATOS marcadas «Pendiente de inversor»
     (columna E o F), con lo que dice la fila: periodo propuesto (G), criterio (M) y notas (N).
Las celdas de juicio (las 37) no se listan: las rellena el personaje.

Uso:
  python3 pending_decisions.py --excel empresas/Nike/Nike.xlsx [--json pendientes.json]
Sale con 1 si hay alguna decisión BLOQUEANTE (celda obligatoria vacía); 0 si no.
"""
import argparse, json, sys
import openpyxl
from cells import SHEET_ANALISIS, SHEET_CONTROL, JUDGMENT_CELLS

REQUIRED = ["C46", "C47", "C50", "C37", "C53", "C55"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--excel", required=True)
    ap.add_argument("--json")
    a = ap.parse_args()
    wb = openpyxl.load_workbook(a.excel)
    an, cm = wb[SHEET_ANALISIS], wb[SHEET_CONTROL]
    items = []
    seen = set()
    for row in range(1, cm.max_row + 1):
        ref = cm.cell(row, 2).value
        if not (isinstance(ref, str) and ref.startswith("Análisis!")):
            continue
        cell = ref.split("!")[-1].strip()
        if cell in JUDGMENT_CELLS:
            continue
        estado = " ".join(str(cm.cell(row, c).value or "") for c in (5, 6))
        if "pendiente de inversor" in estado.lower():
            items.append({"celda": cell, "concepto": cm.cell(row, 3).value, "valor_actual": an[cell].value,
                          "periodo_propuesto": cm.cell(row, 7).value, "criterio": cm.cell(row, 13).value,
                          "notas": cm.cell(row, 14).value, "motivo": "Pendiente de inversor en Control maestro"})
            seen.add(cell)
    for c in REQUIRED:
        v = an[c].value
        if (v is None or (isinstance(v, str) and not v.strip())) and c not in seen:
            items.append({"celda": c, "concepto": None, "valor_actual": None, "periodo_propuesto": None,
                          "criterio": None, "notas": None, "motivo": "Celda obligatoria vacía"})
    for it in items:
        v = an[it["celda"]].value
        vacia = v is None or (isinstance(v, str) and not v.strip())
        it["bloqueante"] = bool(vacia and it["celda"] in REQUIRED)
    items.sort(key=lambda x: not x["bloqueante"])
    empresa = an["B3"].value
    print(f"== {empresa}: {len(items)} decisión(es) pendiente(s) en la parte automática")
    for it in items:
        tag = "BLOQUEANTE" if it["bloqueante"] else "no bloqueante (tiene valor o es opcional)"
        print(f"- {it['celda']} · {it['concepto'] or ''} · {it['motivo']} · {tag}")
        if it["periodo_propuesto"]: print(f"    periodo: {str(it['periodo_propuesto'])[:200]}")
        if it["criterio"]: print(f"    criterio: {str(it['criterio'])[:400]}")
        if it["notas"]: print(f"    notas: {str(it['notas'])[:400]}")
    if a.json:
        json.dump({"empresa": empresa, "pendientes": items}, open(a.json, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1, default=str)
    sys.exit(1 if any(i["bloqueante"] for i in items) else 0)


if __name__ == "__main__":
    main()
