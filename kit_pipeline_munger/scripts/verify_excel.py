#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica un Excel evaluado contra su origen (el Excel de la empresa antes del juicio).

Comprueba:
  1. Integridad: toda fórmula del origen sigue idéntica; ninguna celda fuera de las permitidas cambió;
     las validaciones de datos (desplegables) siguen presentes.
  2. Las 37 celdas de juicio tienen valor, con el vocabulario de los desplegables; números bien formados;
     probabilidades suman 1; cada g terminal < r; C76 entre 0 y C53.
  3. Las 37 filas de celdas de juicio en Control maestro (columna B = Análisis!celda) tienen Observaciones (columna N).
  4. Si se pasa --recalc (copia recalculada por LibreOffice): A6 calcula, B78/C83 numéricos,
     precio de Sí = mín(B78, 0,75·C83); si hay --json, lo compara con el declarado.

Uso:
  python3 verify_excel.py --source Empresa.xlsx --filled Empresa_evaluada.xlsx [--recalc recalc/Empresa_evaluada.xlsx] [--json juicio.json]
Sale con código 0 si todo pasa; 1 si algo falla.
"""
import argparse, json, sys
import openpyxl
from cells import (SHEET_ANALISIS, SHEET_CONTROL, CONTROL_COL_OBS, JUDGMENT_CELLS, ENFORCED, SUGGESTED, NUMERIC,
                   judgment_rows)

errors, warnings, info = [], [], []


def err(m): errors.append(m)
def warn(m): warnings.append(m)


def s_rows(cm):
    return judgment_rows(cm)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--filled", required=True)
    ap.add_argument("--recalc")
    ap.add_argument("--json")
    a = ap.parse_args()

    src = openpyxl.load_workbook(a.source)
    fil = openpyxl.load_workbook(a.filled)

    # ---- 1. integridad
    if src.sheetnames != fil.sheetnames:
        err(f"hojas distintas: {src.sheetnames} vs {fil.sheetnames}")
    allowed = {(SHEET_ANALISIS, c) for c in JUDGMENT_CELLS}
    cm_src = src[SHEET_CONTROL]
    for key, row in s_rows(cm_src).items():
        allowed.add((SHEET_CONTROL, cm_src.cell(row, CONTROL_COL_OBS).coordinate))
    changed_outside = []
    for name in src.sheetnames:
        if name not in fil.sheetnames:
            continue
        ws, wf = src[name], fil[name]
        max_r = max(ws.max_row, wf.max_row); max_c = max(ws.max_column, wf.max_column)
        for r in range(1, max_r + 1):
            for c in range(1, max_c + 1):
                v1 = ws.cell(r, c).value; v2 = wf.cell(r, c).value
                if v1 == v2:
                    continue
                coord = ws.cell(r, c).coordinate
                if isinstance(v1, str) and v1.startswith("="):
                    err(f"fórmula alterada en {name}!{coord}: {v1!r} → {v2!r}")
                elif (name, coord) not in allowed:
                    changed_outside.append(f"{name}!{coord}: {v1!r} → {v2!r}")
    if changed_outside:
        err("celdas cambiadas fuera de las permitidas: " + "; ".join(changed_outside[:20]) +
            (" …" if len(changed_outside) > 20 else ""))
    nv_src = len(src[SHEET_ANALISIS].data_validations.dataValidation)
    nv_fil = len(fil[SHEET_ANALISIS].data_validations.dataValidation)
    if nv_fil < nv_src:
        err(f"se perdieron validaciones de datos en Análisis: {nv_src} → {nv_fil}")
    if len(fil.defined_names) < len(src.defined_names):
        err("se perdieron nombres definidos (listas de Opciones)")

    # ---- 2. celdas de juicio
    an = fil[SHEET_ANALISIS]
    vals = {}
    for c in JUDGMENT_CELLS:
        v = an[c].value
        if v is None or (isinstance(v, str) and not v.strip()):
            err(f"{c} vacía")
            continue
        if c in NUMERIC:
            if not isinstance(v, (int, float)):
                err(f"{c} no es numérica: {v!r}")
                continue
            if c in SUGGESTED and v not in SUGGESTED[c]:
                warn(f"{c}={v} no está en la lista sugerida {SUGGESTED[c]}")
        else:
            v = str(v).strip()
            if c in ENFORCED and v not in ENFORCED[c]:
                err(f"{c}={v!r} fuera del desplegable {ENFORCED[c]}")
            if c in SUGGESTED and v not in SUGGESTED[c]:
                warn(f"{c}={v!r} no es opción de la lista; debe ir explicada en B66/C66/D66")
        vals[c] = v
    if all(k in vals for k in ("B69", "C69", "D69")):
        s = vals["B69"] + vals["C69"] + vals["D69"]
        if abs(s - 1) > 0.001:
            err(f"probabilidades suman {s:.3f}")
    c57 = an["C57"].value
    if "C56" in vals and isinstance(c57, (int, float)) and vals["C56"] <= c57:
        warn(f"r = C56 ({vals['C56']}) ≤ tasa sin riesgo C57 ({c57}): revisa la convención de r para esta moneda")
    if "C56" in vals:
        for g in ("B68", "C68", "D68"):
            if g in vals and vals[g] >= vals["C56"]:
                err(f"{g}={vals[g]} ≥ r={vals['C56']}")
    if "C76" in vals:
        c53 = an["C53"].value
        if vals["C76"] < 0:
            err("C76 negativo")
        if isinstance(c53, (int, float)) and vals["C76"] > c53:
            err(f"C76={vals['C76']} > C53={c53}")
    if vals.get("C51") not in (None, "Sí"):
        warn("C51 ≠ Sí: el procedimiento dice restar siempre la SBC")

    # ---- 3. Observaciones
    cm = fil[SHEET_CONTROL]
    rows = s_rows(cm)
    if len(rows) != 37:
        err(f"Control maestro tiene {len(rows)} filas de celdas de juicio, no 37")
    empty_obs = [c for c in JUDGMENT_CELLS if c in rows and not str(cm.cell(rows[c], CONTROL_COL_OBS).value or "").strip()]
    if empty_obs:
        err(f"Observaciones vacías: {empty_obs}")

    # ---- 4. recalculado
    if a.recalc:
        rc = openpyxl.load_workbook(a.recalc, data_only=True)[SHEET_ANALISIS]
        a6, b78, c83, c85, c52, c53 = (rc[x].value for x in ("A6", "B78", "C83", "C85", "C52", "C53"))
        info.append(f"A6 = {a6!r}")
        if not a6:
            err("A6 no calcula (vacío) en el recalculado")
        if isinstance(b78, (int, float)) and isinstance(c83, (int, float)):
            precio_si = min(b78, 0.75 * c83)
            info.append(f"B78 (malo) = {b78:.1f} | C83 (ponderado) = {c83:.1f} | precio de Sí = {precio_si:.1f} | C85 = {c85}")
            if a.json:
                d = json.load(open(a.json, encoding="utf-8"))
                dec = d.get("precio_de_si")
                try:
                    dec = float(str(dec).replace(",", "."))
                    if abs(dec - precio_si) / precio_si > 0.02:
                        warn(f"precio de Sí declarado {dec} ≠ calculado {precio_si:.1f} (regla: mín(B78, 0,75·C83))")
                except Exception:
                    warn(f"precio_de_si no numérico en el JSON: {dec!r}")
        else:
            err(f"B78/C83 no numéricos en el recalculado: {b78!r} / {c83!r}")
        info.append(f"C52 (FCF base) = {c52!r} | C53 (caja) = {c53!r}")

    print("== VERIFICACIÓN", a.filled)
    for m in info: print("  i ", m)
    for m in warnings: print("  ⚠ ", m)
    for m in errors: print("  ✗ ", m)
    print("RESULTADO:", "PASS" if not errors else f"FAIL ({len(errors)} errores)")
    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
