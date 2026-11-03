#!/usr/bin/env bash
# Paso 12: verificaciones mecánicas (encargo §4.7). Uso: verificar_todo.sh CARPETA LIBRO_EVALUADO LIBRO_ENTRADA
# Cualquier FAIL → código 1 (no_entregable). Deja verificacion_*.txt en CARPETA.
set -u
C="$1"; EV="$2"; EN="$3"; AQUI="$(cd "$(dirname "$0")" && pwd)"; CFG="$AQUI/../config_v2.json"
REF=$(python3 "$AQUI/config_v2.py" plantilla.referencia "$CFG")
VER=$(python3 "$AQUI/config_v2.py" plantilla.verificador "$CFG")
MUNGER=$(python3 "$AQUI/config_v2.py" kit_v1.corpus_munger "$CFG")
DAMO=$(python3 "$AQUI/config_v2.py" corpus.damodaran "$CFG")
fail=0
paso() { if [ "$2" -eq 0 ]; then echo "PASS · $1"; else echo "FAIL · $1 (código $2)"; fail=1; fi; }
python3 "$VER" "$EV" "$REF" > "$C/verificacion_integridad.txt" 2>&1; paso "verificar_v63.py (libro evaluado íntegro)" $?
fases="A,B,C"; [ -f "$C/fase_c.json" ] || { [ -f "$C/fase_b.json" ] && fases="A,B" || fases="A"; }
python3 "$AQUI/comprobar_celdas_v2.py" "$EV" "$EN" --fases "$fases" --salida "$C/verificacion_celdas.json" > "$C/verificacion_celdas.txt" 2>&1; paso "comprobar_celdas_v2.py (fases $fases)" $?
if [ -f "$C/resultados.json" ] && [ -f "$C/fase_b.json" ]; then
  if [ -f "$C/fase_c.json" ]; then python3 "$AQUI/comprobar_gramatica.py" "$C" --tras-recalculo --con-fase-c > "$C/verificacion_gramatica.txt" 2>&1; else python3 "$AQUI/comprobar_gramatica.py" "$C" --tras-recalculo > "$C/verificacion_gramatica.txt" 2>&1; fi
  paso "comprobar_gramatica.py (código 0 exigido)" $?
fi
# esquemas del Anexo D (criterio 7 †: la ficha valida contra su esquema; las fases también)
(
  for f in fase_a fase_b; do [ -f "$C/$f.json" ] && { python3 "$AQUI/validar_esquema.py" "$C/$f.json" "$f" || exit 1; }; done
  [ -f "$C/fase_c.json" ] && { python3 "$AQUI/validar_esquema.py" "$C/fase_c.json" fase_c --turno 2 || exit 1; }
  [ -f "$C/ficha.json" ] && { python3 "$AQUI/validar_esquema.py" "$C/ficha.json" ficha || exit 1; }
  exit 0
) > "$C/verificacion_esquemas.txt" 2>&1; paso "validar_esquema.py (fase_a/b/c y ficha contra esquema/)" $?
# citas: Munger y Damodaran sobre informe.md, fase_*.md y Observaciones (si existe verify_quotes_v2.py)
if [ -f "$AQUI/verify_quotes_v2.py" ]; then
  # las Observaciones (columna N) y los textos de los JSON de las fases se vuelcan a un .md temporal y se comprueban igual (§10.2.5)
  python3 - "$C" > "$C/observaciones_para_citas.md" << 'PY'
import json, os, sys
c = sys.argv[1]
for n in ("fase_a.json", "fase_b.json", "fase_c.json"):
    p = os.path.join(c, n)
    if not os.path.exists(p):
        continue
    d = json.load(open(p, encoding="utf-8"))
    print(f"# {n}")
    for k, v in (d.get("observaciones") or {}).items():
        print(f"## {k}\n{v}\n")
    # cada texto se vuelca como línea propia, sin la sintaxis JSON: las comillas rectas de JSON no son citas y
    # verify_quotes_v2 las leería como tales (fallo de implementación visto con Rational, 3-nov-2026)
    def hojas(x, ruta):
        if isinstance(x, dict):
            for kk, vv in x.items():
                hojas(vv, f"{ruta}.{kk}")
        elif isinstance(x, list):
            for i, vv in enumerate(x):
                hojas(vv, f"{ruta}[{i}]")
        elif isinstance(x, str) and x.strip():
            print(f"- {ruta}: {x}")
    for k in ("escenarios", "herencia", "desviaciones_justificadas", "fundamento_material", "autocomprobacion", "celdas", "cinco_frases", "seis_preguntas"):
        if d.get(k) is not None:
            print(f"## {k}")
            hojas(d[k], k)
            print()
PY
  args=(); for f in "$C"/informe.md "$C"/fase_a.md "$C"/fase_b.md "$C"/fase_c.md "$C"/observaciones_para_citas.md; do [ -f "$f" ] && args+=("$f"); done
  if [ ${#args[@]} -gt 0 ]; then
    python3 "$AQUI/verify_quotes_v2.py" --corpus "$MUNGER" --corpus "$DAMO" --paginas-estrictas "${args[@]}" > "$C/verificacion_citas.txt" 2>&1; paso "verify_quotes_v2.py (Munger y Damodaran; textos y Observaciones; páginas estrictas; corpus ausente = fallo)" $?
  fi
else
  echo "SKIP · verify_quotes_v2.py no existe todavía (pieza 3)"
fi
# estado del libro esperado (§7.3): LISTO · PROVISIONAL, o NO LISTO solo por causas previstas y ya listadas en la entrada
python3 - "$C" > "$C/verificacion_estado_libro.txt" 2>&1 << 'PY'
import json, sys, os, re
c = sys.argv[1]
res = json.load(open(os.path.join(c, "resultados.json"))) if os.path.exists(os.path.join(c, "resultados.json")) else None
pipe = json.load(open(os.path.join(c, "estado_pipeline.json"))) if os.path.exists(os.path.join(c, "estado_pipeline.json")) else {}
ent = json.load(open(os.path.join(c, "entrada_v63.json"))) if os.path.exists(os.path.join(c, "entrada_v63.json")) else {}
if not res: print("sin resultados.json"); sys.exit(0)
est = res["estados"]["estado_libro_B266"] or ""
tec = res["estados"]["estado_tecnico_B255"]
faltan_c08 = [x["dato"] for x in ent.get("necesarios_para_listo_provisional", [])]
fase_c = pipe.get("fase_c_escrita")
fase_b = pipe.get("fase_b_escrita")
estado_final = pipe.get("estado_analisis")
reglas = [r for r in res.get("reglas_motor", []) if r.get("aplica") and r.get("resultado") not in ("OK", "N/A", "AVISO")]
print(f"estado del libro: {est!r} · técnico: {tec!r} · fase B escrita: {fase_b} · fase C escrita: {fase_c} · estado del análisis: {estado_final} · faltan (C08/metadatos): {faltan_c08}")
print("reglas no OK:", [(r.get("id"), r.get("resultado"), r.get("causa")) for r in reglas])
fallos = []
if estado_final == "modelo_no_aplicable":
    # el libro queda con el motor sin aplicar: se admite NO LISTO · modelo no aplicable o incompleto (sin fase B)
    if not est.startswith("NO LISTO"):
        fallos.append(f"modelo_no_aplicable con estado del libro {est!r}")
elif fase_c:
    if est.startswith("LISTO · PROVISIONAL") or est == "LISTO":
        pass
    elif est.startswith("NO LISTO · incompleto") or est.startswith("NO LISTO · evidencias incompletas"):
        # solo C08 (respuestas de la etapa 1 ausentes ya listadas) o evidencias pendientes de filas de datos ya listadas (§7.1)
        celdas_c08 = [x for x in faltan_c08 if not str(x).startswith("evidencia ")]
        c08_ok = bool(celdas_c08) and all(x.split("!")[-1] in ("C24", "C26", "C28", "C31", "C32", "C33", "C34") for x in celdas_c08)
        malas = [r.get("id") for r in reglas if r.get("resultado") in ("INCOMPLETO", "DATOS INVÁLIDOS", "MODELO NO APLICABLE") and not (r.get("id") == "C08" and c08_ok)]
        if malas:
            fallos.append(f"estado técnico {tec!r} por reglas no previstas: {malas}")
        if est.startswith("NO LISTO · evidencias incompletas"):
            pend = (res.get("evidencias") or {})
            # D246 = datos no verificables (dato sin documento: problema de la fase 1, §7.1, siempre listado en la entrada) ·
            # D247 = hipótesis pendientes · D248 = sin dato / sin clasificar / sin fuente / incoherentes · D249 = «No aplicable» indebido
            no_verif = pend.get("D246") or 0
            otros = {k: (pend.get(k) or 0) for k in ("D247", "D248", "D249") if (pend.get(k) or 0)}
            if otros:
                fallos.append(f"evidencias pendientes que no son «datos no verificables» {otros}: hipótesis pendientes, sin fuente o «No aplicable» indebido son fallo del pipeline")
            listados = [x.get("dato", "") for x in (ent.get("necesarios_para_listo_provisional") or []) + (ent.get("no_bloqueantes") or [])]
            n_list = sum(1 for x in listados if str(x).startswith("evidencia "))
            if no_verif > n_list:
                fallos.append(f"{no_verif} datos no verificables en la hoja pero la entrada solo listó {n_list} evidencias pendientes")
    else:
        fallos.append(f"estado del libro no previsto con la fase C escrita: {est!r}")
else:
    # sin fase C: solo puede faltar completitud (C05/C07/C10 de la fase C, o palancas si tampoco hay fase B)
    if not est.startswith("NO LISTO · incompleto"):
        fallos.append(f"sin fase C el estado tiene que ser NO LISTO · incompleto, no {est!r}")
    malas = [r.get("id") for r in reglas if r.get("resultado") in ("DATOS INVÁLIDOS", "MODELO NO APLICABLE")]
    if malas:
        fallos.append(f"reglas con DATOS INVÁLIDOS / MODELO NO APLICABLE: {malas}")
for f in fallos:
    print("FAIL:", f)
sys.exit(1 if fallos else 0)
PY
paso "estado del libro esperado (§7.3)" $?
# crecimiento implícito frente a Análisis!C86 (§10.2.6; solo cuando la tabla del DCF inverso es utilizable)
python3 - "$C" > "$C/verificacion_c86.txt" 2>&1 << 'PY'
import json, sys, os
c = sys.argv[1]
p = os.path.join(c, "precio.json")
if not os.path.exists(p): print("sin precio.json"); sys.exit(0)
pr = json.load(open(p, encoding="utf-8"))
print(f"tabla utilizable: {pr.get('tabla_dcf_inverso_ok')} · g implícito al precio actual: {pr.get('g_impl_actual')} · coincide con C86: {pr.get('coincide_C86')}")
sys.exit(1 if pr.get("coincide_C86") is False else 0)
PY
paso "precio_de_si.py: crecimiento implícito coincide con Análisis!C86 (±0,5 pt)" $?
# cachés y verificación final
ADD="$(python3 "$AQUI/config_v2.py" kit_v1.scripts "$CFG")/add_cached_values.py"
REC="$C/recalc/$(basename "$EV")"
if [ -f "$REC" ]; then
  python3 "$ADD" "$EV" "$REC" "$C/con_cache.tmp.xlsx" > "$C/verificacion_cache.txt" 2>&1 && python3 "$VER" "$C/con_cache.tmp.xlsx" "$REF" >> "$C/verificacion_cache.txt" 2>&1; rc=$?
  paso "add_cached_values + verificar_v63 otra vez" $rc
  [ $rc -eq 0 ] && mv "$C/con_cache.tmp.xlsx" "$EV" || rm -f "$C/con_cache.tmp.xlsx"
fi
# todas las verificaciones tienen que haber dejado su archivo: si falta alguno, el script no corrió entero (fallo del propio script)
for f in verificacion_integridad.txt verificacion_celdas.txt verificacion_esquemas.txt verificacion_estado_libro.txt verificacion_c86.txt; do
  [ -f "$C/$f" ] || { echo "FAIL · falta $f: verificar_todo.sh no completó todas las comprobaciones"; fail=1; }
done
echo "RESULTADO verificar_todo.sh: $([ $fail -eq 0 ] && echo PASS || echo FAIL)"
exit $fail
