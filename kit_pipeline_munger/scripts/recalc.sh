#!/usr/bin/env bash
# Recalcula un Excel con LibreOffice (sin abrir ventana) y deja la copia en <outdir>.
# La copia recalculada sirve SOLO para leer valores (A6, B78, C83…). El archivo que se entrega
# es el escrito por fill_excel.py, no esta copia.
#
# Uso: bash recalc.sh Empresa_evaluada.xlsx recalc/
set -euo pipefail
in="$1"; outdir="${2:-recalc}"
mkdir -p "$outdir"
soffice --headless --calc --convert-to xlsx --outdir "$outdir" "$in" >/dev/null 2>&1
out="$outdir/$(basename "$in")"
if [ ! -f "$out" ]; then echo "ERROR: LibreOffice no produjo $out"; exit 1; fi
echo "OK: $out"
