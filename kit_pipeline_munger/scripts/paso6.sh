#!/usr/bin/env bash
# Paso 6 completo de una empresa: fill_excel → recalc → verify_excel → verify_quotes (respuesta + Observaciones)
# → add_cached_values. Ejecutar desde la carpeta que contiene kit/ y empresas/.
# Uso: bash kit/scripts/paso6.sh <Empresa>      (usa <Empresa>_listo.xlsx si existe; si no, <Empresa>.xlsx)
set -u
e=$1; E=empresas/$e; S=kit/scripts
SRC=$E/${e}_listo.xlsx; [ -f "$SRC" ] || SRC=$E/${e}.xlsx
python3 $S/fill_excel.py --source "$SRC" --json $E/juicio.json --out $E/${e}_evaluada.xlsx || { echo "PASO6: FAIL (fill_excel)"; exit 2; }
bash $S/recalc.sh $E/${e}_evaluada.xlsx $E/recalc >/dev/null || { echo "PASO6: FAIL (recalc)"; exit 2; }
python3 $S/verify_excel.py --source "$SRC" --filled $E/${e}_evaluada.xlsx --recalc $E/recalc/${e}_evaluada.xlsx --json $E/juicio.json > $E/verificacion_excel.txt; x=$?
python3 -c "import json,sys;d=json.load(open(sys.argv[1]));open(sys.argv[2],'w').write('\n\n'.join(f'{k}: {v}' for k,v in d['observaciones'].items()))" $E/juicio.json $E/obs_tmp.md
{ python3 $S/verify_quotes.py --text $E/respuesta.md --corpus kit/munger.md; qa=$?
  echo "--- Observaciones del JSON"; python3 $S/verify_quotes.py --text $E/obs_tmp.md --corpus kit/munger.md; qb=$?
  echo "CITAS GLOBAL: $([ $qa -eq 0 ] && [ $qb -eq 0 ] && echo PASS || echo FAIL)"; } > $E/verificacion_citas.txt
python3 $S/add_cached_values.py $E/${e}_evaluada.xlsx $E/recalc/${e}_evaluada.xlsx $E/${e}_evaluada_v.xlsx && mv $E/${e}_evaluada_v.xlsx $E/${e}_evaluada.xlsx
cat $E/verificacion_excel.txt; grep "CITAS GLOBAL" $E/verificacion_citas.txt
if [ $x -eq 0 ] && grep -q "CITAS GLOBAL: PASS" $E/verificacion_citas.txt; then echo "PASO6: PASS"; else echo "PASO6: FAIL"; exit 1; fi
