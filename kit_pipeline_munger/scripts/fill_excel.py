#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Escribe el juicio (juicio.json) en una COPIA del Excel de la empresa.

Solo toca: las 37 celdas de juicio de la hoja Análisis y la columna N (Observaciones)
de las 37 filas de tipo S en Control maestro. Nada más. Nunca sobrescribe el origen.

Uso:
  python3 fill_excel.py --source Empresa.xlsx --json juicio.json --out Empresa_evaluada.xlsx
"""
import argparse, json, sys, shutil, os
import openpyxl
from cells import (SHEET_ANALISIS, SHEET_CONTROL, CONTROL_COL_OBS, JUDGMENT_CELLS, ENFORCED, NUMERIC,
                   to_number, judgment_rows)


def fail(msg):
    print("ERROR:", msg)
    sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--json", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    if os.path.abspath(a.source) == os.path.abspath(a.out):
        fail("--out no puede ser el mismo archivo que --source")

    data = json.load(open(a.json, encoding="utf-8"))
    celdas = data.get("celdas", {})
    obs = data.get("observaciones", {})

    missing = [c for c in JUDGMENT_CELLS if c not in celdas or celdas[c] in (None, "")]
    if missing:
        fail(f"faltan valores en celdas: {missing}")
    missing_obs = [c for c in JUDGMENT_CELLS if not str(obs.get(c, "")).strip()]
    if missing_obs:
        fail(f"faltan Observaciones: {missing_obs}")

    # normalizar y validar
    values = {}
    for c in JUDGMENT_CELLS:
        v = celdas[c]
        if c in NUMERIC:
            try:
                v = to_number(v)
            except Exception:
                fail(f"{c} debe ser numérico, recibido {v!r}")
        else:
            v = str(v).strip()
            if c in ENFORCED and v not in ENFORCED[c]:
                fail(f"{c}={v!r} no está en el desplegable {ENFORCED[c]}")
        values[c] = v

    probs = values["B69"] + values["C69"] + values["D69"]
    if abs(probs - 1.0) > 0.001:
        fail(f"las probabilidades suman {probs:.3f}, no 1")
    r = values["C56"]
    for g in ("B68", "C68", "D68"):
        if values[g] >= r:
            fail(f"{g}={values[g]} no es menor que r={r}")
    if values["C76"] < 0:
        fail("C76 no puede ser negativo")

    shutil.copyfile(a.source, a.out)
    wb = openpyxl.load_workbook(a.out)
    if SHEET_ANALISIS not in wb.sheetnames or SHEET_CONTROL not in wb.sheetnames:
        fail("el libro no tiene las hojas Análisis / Control maestro")
    an = wb[SHEET_ANALISIS]
    cm = wb[SHEET_CONTROL]

    # C53 (caja) para comprobar C76 ≤ C53 cuando C53 es un valor
    c53 = an["C53"].value
    if isinstance(c53, (int, float)) and values["C76"] > c53:
        fail(f"C76={values['C76']} > C53={c53}")

    for c in JUDGMENT_CELLS:
        cell = an[c]
        if isinstance(cell.value, str) and cell.value.startswith("="):
            fail(f"{c} contiene una fórmula en el origen; no es una celda de juicio en este libro")
        cell.value = values[c]

    # Observaciones en Control maestro
    written = 0
    rows_S = judgment_rows(cm)
    missing_rows = [c for c in JUDGMENT_CELLS if c not in rows_S]
    if missing_rows:
        fail(f"Control maestro no tiene fila (columna B = Análisis!celda) para: {missing_rows}")
    for c in JUDGMENT_CELLS:
        cm.cell(rows_S[c], CONTROL_COL_OBS).value = str(obs[c]).strip()
        written += 1

    wb.save(a.out)
    print(f"OK: 37 celdas y {written} Observaciones escritas en {a.out}")
    print("Cubo declarado:", data.get("cubo"), "| precio de Sí declarado:", data.get("precio_de_si"))


if __name__ == "__main__":
    main()
