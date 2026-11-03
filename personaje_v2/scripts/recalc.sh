#!/usr/bin/env bash
# Recalcula un libro V6.3 con LibreOffice en modo headless, con RECÁLCULO FORZADO (encargo §1.4):
# perfil propio con OOXMLRecalcMode = 0 (recalcular siempre al cargar), porque `soffice --convert-to`
# conserva los valores cacheados si no se le obliga. La copia recalculada sirve SOLO para leer valores:
# pierde los controles y el verificador la rechaza; nunca es el entregable.
#
# Uso: bash recalc.sh LIBRO.xlsx DIR_SALIDA [DIR_PERFIL]
# Salida: DIR_SALIDA/<nombre del libro>. Código 0 si existe; 1 si LibreOffice no produjo nada.
set -euo pipefail
in="$1"; outdir="${2:-recalc}"; perfil="${3:-${TMPDIR:-/tmp}/lo_perfil_v2}"
mkdir -p "$outdir" "$perfil/user"
xcu="$perfil/user/registrymodifications.xcu"
if [ ! -f "$xcu" ] || ! grep -q 'OOXMLRecalcMode' "$xcu"; then
cat > "$xcu" << 'XCU'
<?xml version="1.0" encoding="UTF-8"?>
<oor:items xmlns:oor="http://openoffice.org/2001/registry" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<item oor:path="/org.openoffice.Office.Calc/Formula/Load"><prop oor:name="OOXMLRecalcMode" oor:op="fuse"><value>0</value></prop></item>
<item oor:path="/org.openoffice.Office.Calc/Formula/Load"><prop oor:name="ODFRecalcMode" oor:op="fuse"><value>0</value></prop></item>
<item oor:path="/org.openoffice.Office.Common/Misc"><prop oor:name="FirstRun" oor:op="fuse"><value>false</value></prop></item>
</oor:items>
XCU
fi
# ruta absoluta del perfil (file:// exige absoluta)
perfil_abs="$(cd "$perfil" && pwd)"
out="$outdir/$(basename "$in")"
rm -f "$out"
soffice -env:UserInstallation="file://$perfil_abs" --headless --calc --convert-to xlsx --outdir "$outdir" "$in" >/dev/null 2>&1 || true
if [ ! -f "$out" ]; then echo "ERROR: LibreOffice no produjo $out"; exit 1; fi
echo "OK: $out (recálculo forzado, perfil $perfil_abs)"
