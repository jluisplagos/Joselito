#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vuelca la parte automática del Excel a un Markdown para el agente de juicio.

Lee la copia RECALCULADA (LibreOffice) para que las fórmulas tengan valor. Incluye:
  1. Las celdas de datos de Análisis con su etiqueta y nota de la plantilla.
  2. (v1.3) La EVIDENCIA DE FASE 1 de Control maestro para cada celda de datos: periodo (G),
     unidad (H), tipo de fuente (I), documento (J), página (L), criterio (M) y observaciones (N).
  3. (v1.3) La evidencia de fase 1 que haya en las filas de las celdas de JUICIO (columnas M y N),
     por ejemplo las operaciones de insiders en la fila de C97 o la evidencia preparada para C25.
  4. La hoja Base financiera completa, si existe.
El agente de juicio nunca abre el Excel: trabaja con este volcado.

Uso:
  python3 dump_data_cells.py --recalc recalc/Empresa.xlsx --out datos_automaticos.md
"""
import argparse
import openpyxl
from cells import SHEET_ANALISIS, SHEET_CONTROL, CONTROL_COL_REF, DATA_CELLS, JUDGMENT_CELLS

# Columnas de Control maestro (1 = A)
CM_COLS = [(7, "Periodo"), (8, "Unidad / moneda"), (9, "Tipo de fuente"), (10, "Documento"),
           (12, "Página / nota"), (13, "Criterio / decisión"), (14, "Observaciones")]


def fmt(v):
    if v is None: return ""
    if hasattr(v, "strftime"): return v.strftime("%Y-%m-%d")
    if isinstance(v, float): return f"{v:,.4f}".rstrip("0").rstrip(".")
    return str(v)


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def cm_rows(cm):
    """Celda de Análisis → fila de Control maestro (por la referencia de la columna B)."""
    rows = {}
    for r in range(1, cm.max_row + 1):
        ref = cm.cell(r, CONTROL_COL_REF).value
        if isinstance(ref, str) and ref.startswith("Análisis!"):
            rows.setdefault(ref.split("!")[-1].strip(), r)
    return rows


def evidence_block(cm, row, cols):
    out = []
    for c, name in cols:
        v = cm.cell(row, c).value
        if v is not None and str(v).strip():
            out.append(f"- {name}: {fmt(v)}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--recalc", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    wb = openpyxl.load_workbook(a.recalc, data_only=True)
    an = wb[SHEET_ANALISIS]
    cm = wb[SHEET_CONTROL] if SHEET_CONTROL in wb.sheetnames else None
    rows = cm_rows(cm) if cm is not None else {}

    lines = ["# Datos automáticos de la plantilla (solo lectura)", ""]
    lines.append("Estas celdas vienen de la parte automática (fase 1). Se usan tal cual; no se recalculan ni se cambia la base del FCF. "
                 "Si algo no cuadra con el informe, se dice en Observaciones.")
    lines.append("")
    lines.append("## 1. Valores")
    lines.append("")
    lines.append("| Celda | Etiqueta | Valor | Nota de la plantilla |")
    lines.append("|---|---|---|---|")
    for c in DATA_CELLS:
        r = an[c].row
        col = an[c].column
        if col == 3:   # celdas C: etiqueta en A, nota en B, semáforo en D
            label = an.cell(r, 1).value or ""
            note = " ".join(fmt(x) for x in (an.cell(r, 2).value, an.cell(r, 4).value) if x)
        else:          # celdas B o D: etiqueta en la columna anterior
            label = an.cell(r, col - 1).value or ""
            note = ""
        lines.append(f"| {c} | {fmt(label)[:90]} | {fmt(an[c].value)} | {note[:140]} |")
    lines.append("")

    # C52 depende de C51 (celda de juicio). Si faltan C46/C47/C50 no se puede derivar: se dice, no se pone 0.
    vals = {x: an[x].value for x in ("C46", "C47", "C48", "C49", "C50")}
    missing = [x for x in ("C46", "C47", "C50") if not is_num(vals[x])]
    if missing:
        lines.append(f"FCF base derivado: NO SE PUEDE CALCULAR, faltan {', '.join(missing)} (decisión pendiente del paso 0). "
                     "No supongas 0.")
    else:
        c46, c47, c50 = (float(vals[x]) for x in ("C46", "C47", "C50"))
        c48 = float(vals["C48"]) if is_num(vals["C48"]) else 0.0
        c49 = float(vals["C49"]) if is_num(vals["C49"]) else 0.0
        lines.append(f"FCF base derivado (misma fórmula de la plantilla): con SBC restada (C51 = Sí) = C46 − C47 − C48 − C49 − C50 = "
                     f"{c46 - c47 - c48 - c49 - c50:,.0f} mm; sin restar SBC (C51 = No) = {c46 - c47 - c48 - c49:,.0f} mm.")
    lines.append(f"Precio actual C37 = {fmt(an['C37'].value)}; acciones diluidas C55 = {fmt(an['C55'].value)} mm.")
    lines.append("")
    lines.append("Celdas de juicio que debes rellenar (actualmente vacías o a sustituir): " + ", ".join(JUDGMENT_CELLS))
    lines.append("")

    if cm is not None:
        lines.append("## 2. Evidencia de fase 1 por celda de datos (Control maestro)")
        lines.append("")
        lines.append("Es lo que ya se investigó con fuente primaria: periodo, unidad, documento, página, definición usada y "
                     "sensibilidades. Antes de decir que un dato «no cuadra», «no consta» o «no se puede conciliar», mira aquí: "
                     "suele ser otra fecha, otra ventana (LTM, media) u otra definición. Si aun así discrepas, dilo con la fuente.")
        lines.append("")
        for c in DATA_CELLS:
            r = rows.get(c)
            if not r:
                continue
            ev = evidence_block(cm, r, CM_COLS)
            if ev:
                lines.append(f"### {c} = {fmt(an[c].value)}")
                lines.extend(ev)
                lines.append("")
        # filas de Control maestro de datos que no están en DATA_CELLS (p. ej. C38, C57 ya están; CONTROL, otras)
        extra = [k for k in rows if k not in DATA_CELLS and k not in JUDGMENT_CELLS]
        for c in extra:
            ev = evidence_block(cm, rows[c], CM_COLS)
            if ev:
                lines.append(f"### {c}")
                lines.extend(ev)
                lines.append("")

        lines.append("## 3. Evidencia de fase 1 en filas de celdas de juicio")
        lines.append("")
        lines.append("La fase 1 dejó aquí hechos para algunas celdas de juicio. Son hechos verificados, no órdenes: la celda la "
                     "decides tú, salvo las reglas del inversor indicadas en el prompt de juicio (por ejemplo C97).")
        lines.append("")
        for c in JUDGMENT_CELLS:
            r = rows.get(c)
            if not r:
                continue
            ev = evidence_block(cm, r, [(7, "Periodo"), (10, "Documento"), (13, "Evidencia / criterio de fase 1"),
                                        (14, "Notas de fase 1")])
            if ev:
                lines.append(f"### {c}")
                lines.extend(ev)
                lines.append("")

    if "Base financiera" in wb.sheetnames:
        bf = wb["Base financiera"]
        lines.append("## 4. Base financiera (series históricas)")
        lines.append("")
        for row in bf.iter_rows(min_row=1, max_row=bf.max_row):
            vals = [fmt(c.value) for c in row]
            if any(v for v in vals):
                lines.append("| " + " | ".join(vals) + " |")
    open(a.out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"OK: {a.out}")


if __name__ == "__main__":
    main()
