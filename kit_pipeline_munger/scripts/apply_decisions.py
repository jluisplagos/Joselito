#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Escribe en una COPIA del Excel las decisiones del inversor sobre la PARTE AUTOMÁTICA.

Solo celdas de datos (nunca las 37 de juicio ni fórmulas). Para cada celda escrita, su fila de
Control maestro pasa a «Rellenado y verificado» y se registra la decisión literal en la columna M.

Uso:
  python3 apply_decisions.py --source Nike.xlsx --out Nike_listo.xlsx \
      --set C46=4665 --set C47=642 --set C50=743 \
      --nota "Decisión del inversor (11-oct-2026): FCF base con media 3 años FY24–26" [--periodo "FY2024–FY2026"]
"""
import argparse, os, shutil, sys
import openpyxl
from cells import SHEET_ANALISIS, SHEET_CONTROL, JUDGMENT_CELLS, to_number


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--set", action="append", default=[], help="CELDA=VALOR (número o texto)")
    ap.add_argument("--nota", required=True, help="decisión del inversor, literal")
    ap.add_argument("--periodo")
    a = ap.parse_args()
    if os.path.abspath(a.source) == os.path.abspath(a.out):
        print("ERROR: --out no puede ser el origen"); sys.exit(1)
    shutil.copyfile(a.source, a.out)
    wb = openpyxl.load_workbook(a.out)
    an, cm = wb[SHEET_ANALISIS], wb[SHEET_CONTROL]
    rows = {}
    for row in range(1, cm.max_row + 1):
        ref = cm.cell(row, 2).value
        if isinstance(ref, str) and ref.startswith("Análisis!"):
            rows.setdefault(ref.split("!")[-1].strip(), row)
    for item in a.set:
        cell, _, raw = item.partition("=")
        cell = cell.strip().upper()
        if cell in JUDGMENT_CELLS:
            print(f"ERROR: {cell} es celda de juicio; la rellena el personaje"); sys.exit(1)
        cur = an[cell].value
        if isinstance(cur, str) and cur.startswith("="):
            print(f"ERROR: {cell} tiene fórmula; no se toca"); sys.exit(1)
        try:
            val = to_number(raw)
        except Exception:
            val = raw.strip()
        an[cell].value = val
        r = rows.get(cell)
        if r:
            cm.cell(r, 5).value = "Listo para auditoría"
            cm.cell(r, 6).value = "Rellenado y verificado"
            if a.periodo: cm.cell(r, 7).value = a.periodo
            prev = cm.cell(r, 13).value
            cm.cell(r, 13).value = f"{a.nota} → {cell} = {raw.strip()}." + (f" Antes: {prev}" if prev else "")
        print(f"OK {cell} = {val!r}")
    wb.save(a.out)
    print("Guardado:", a.out)


if __name__ == "__main__":
    main()
