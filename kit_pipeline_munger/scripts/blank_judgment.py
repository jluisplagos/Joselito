#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Crea una copia del Excel con las 37 celdas de juicio y sus Observaciones en blanco.

Para los Excel que ya llevan la parte automática Y los juicios del inversor: la copia en blanco
es la entrada del personaje; el original se conserva para comparar.

Uso:
  python3 blank_judgment.py --source Empresa_mia.xlsx --out Empresa.xlsx
"""
import argparse, os, shutil, sys
import openpyxl
from cells import SHEET_ANALISIS, SHEET_CONTROL, CONTROL_COL_OBS, JUDGMENT_CELLS, judgment_rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if os.path.abspath(a.source) == os.path.abspath(a.out):
        print("ERROR: --out no puede ser el origen"); sys.exit(1)
    shutil.copyfile(a.source, a.out)
    wb = openpyxl.load_workbook(a.out)
    an = wb[SHEET_ANALISIS]; cm = wb[SHEET_CONTROL]
    n = 0
    for c in JUDGMENT_CELLS:
        v = an[c].value
        if isinstance(v, str) and v.startswith("="):
            print(f"AVISO: {c} tiene fórmula; no se toca"); continue
        if v is not None:
            n += 1
        an[c].value = None
    m = 0
    for key, row in judgment_rows(cm).items():
        if cm.cell(row, CONTROL_COL_OBS).value is not None:
            cm.cell(row, CONTROL_COL_OBS).value = None; m += 1
    wb.save(a.out)
    print(f"OK: {n} celdas de juicio y {m} Observaciones puestas en blanco → {a.out}")


if __name__ == "__main__":
    main()
