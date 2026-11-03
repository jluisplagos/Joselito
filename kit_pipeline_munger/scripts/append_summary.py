#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Añade una fila a resumen.csv con el resultado de una empresa.

Uso:
  python3 append_summary.py --csv resumen.csv --json juicio.json --recalc recalc/Empresa_evaluada.xlsx \
      --verificacion PASS|FAIL [--mi-excel Empresa_mia.xlsx]

Si se pasa --mi-excel (el Excel con los juicios del inversor), añade cuántas de las 37 celdas
difieren y cuáles.
"""
import argparse, csv, json, os
import openpyxl
from cells import SHEET_ANALISIS, JUDGMENT_CELLS, NUMERIC

COLS = ["empresa", "fecha", "cubo", "precio_de_si_declarado", "precio_de_si_calculado", "A6",
        "B78_malo", "C83_ponderado", "C85_asimetria", "r", "B67", "C67", "D67", "B68", "C68", "D68",
        "B69", "C69", "D69", "C76", "C13", "C14", "C98", "C103", "verificacion", "celdas_distintas_al_inversor",
        "cuales"]


def same(a, b, c):
    if a is None and b is None: return True
    if c in NUMERIC:
        try: return abs(float(a) - float(b)) < 1e-9
        except Exception: return str(a) == str(b)
    return str(a).strip() == str(b).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--json", required=True)
    ap.add_argument("--recalc", required=True)
    ap.add_argument("--verificacion", required=True)
    ap.add_argument("--mi-excel")
    a = ap.parse_args()
    d = json.load(open(a.json, encoding="utf-8"))
    rc = openpyxl.load_workbook(a.recalc, data_only=True)[SHEET_ANALISIS]
    g = lambda c: rc[c].value
    b78, c83 = g("B78"), g("C83")
    calc = min(b78, 0.75 * c83) if isinstance(b78, (int, float)) and isinstance(c83, (int, float)) else ""
    row = {
        "empresa": d.get("empresa") or g("B3"), "fecha": d.get("fecha_analisis") or g("D4"), "cubo": d.get("cubo"),
        "precio_de_si_declarado": d.get("precio_de_si"), "precio_de_si_calculado": round(calc, 1) if calc != "" else "",
        "A6": g("A6"), "B78_malo": b78, "C83_ponderado": c83, "C85_asimetria": g("C85"), "r": g("C56"),
        "B67": g("B67"), "C67": g("C67"), "D67": g("D67"), "B68": g("B68"), "C68": g("C68"), "D68": g("D68"),
        "B69": g("B69"), "C69": g("C69"), "D69": g("D69"), "C76": g("C76"), "C13": g("C13"), "C14": g("C14"),
        "C98": g("C98"), "C103": g("C103"), "verificacion": a.verificacion,
        "celdas_distintas_al_inversor": "", "cuales": "",
    }
    if a.mi_excel:
        mine = openpyxl.load_workbook(a.mi_excel, data_only=True)[SHEET_ANALISIS]
        diff = [c for c in JUDGMENT_CELLS if not same(mine[c].value, rc[c].value, c)]
        row["celdas_distintas_al_inversor"] = len(diff); row["cuales"] = " ".join(diff)
    new = not os.path.exists(a.csv)
    with open(a.csv, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        if new: w.writeheader()
        w.writerow(row)
    print("OK fila añadida:", row["empresa"], row["cubo"], "precio de Sí calc.", row["precio_de_si_calculado"], "| A6:", row["A6"])


if __name__ == "__main__":
    main()
