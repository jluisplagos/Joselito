#!/usr/bin/env bash
# Paso 0 del pipeline: comprueba el entorno (encargo §0.2c). Código 0 si todo está; 1 si falta algo.
set -u
ok=0
py() { python3 -c "import $1" 2>/dev/null && echo "OK  python: $1" || { echo "FALTA python: $1"; ok=1; }; }
py openpyxl; py lxml; py pypdf
for b in soffice pdftotext; do command -v "$b" >/dev/null && echo "OK  binario: $b ($("$b" --version 2>/dev/null | head -1))" || { echo "FALTA binario: $b"; ok=1; }; done
py jsonschema
cfg="$(dirname "$0")/../config_v2.json"
if [ -f "$cfg" ]; then
  for k in plantilla.archivo plantilla.referencia plantilla.verificador plantilla.scripts_v63 kit_v1.corpus_munger kit_v1.scripts; do
    p=$(python3 "$(dirname "$0")/config_v2.py" "$k" "$cfg")
    [ -e "$p" ] && echo "OK  $k → $p" || { echo "FALTA $k → $p (ajusta la ruta en config_v2.json; las relativas se resuelven desde personaje_v2/)"; ok=1; }
  done
  d=$(python3 "$(dirname "$0")/config_v2.py" corpus.damodaran "$cfg")
  [ -e "$d" ] && echo "OK  corpus.damodaran → $d" || echo "AVISO corpus.damodaran → $d no existe todavía (pieza 3: faltan los PDF); las citas a Damodaran con página fallarán"
else
  echo "FALTA config_v2.json"; ok=1
fi
python3 "$(dirname "$0")/precio_de_si.py" --autotest || ok=1
exit $ok
