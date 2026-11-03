#!/usr/bin/env python3
"""Pruebas del pipeline con datos sintéticos y agentes simulados (§10.2: 10, 12(a), 13, 14, 15 y una pasada completa).

Uso: python3 pruebas/test_pipeline_sintetico.py [nombre_de_prueba …]
Empresa sintética: Empresa X (inventada) → etapa1 = V5.3 sintética; fase1_v63.json = esquema/fase1_v63.ejemplo.json.
"""
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import agentes_sinteticos as AG  # noqa: E402

PY = sys.executable
PIPE = os.path.join(RAIZ, "scripts", "pipeline.py")
BASE = os.path.join(AQUI, "sintetico")
resultados = []


def paso(nombre, ok, detalle=""):
    resultados.append({"prueba": nombre, "ok": bool(ok), "detalle": detalle})
    print(("PASA " if ok else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))


def preparar(nombre, quitar_fase1=(), quitar_precio=False, precio=None, quitar_etapa1=()):
    c = os.path.join(BASE, nombre)
    shutil.rmtree(c, ignore_errors=True)
    os.makedirs(os.path.join(c, "etapa1"))
    v53 = os.path.join(AQUI, "sintetico", "_origen", "EmpresaX_v53_evaluada_sintetica.xlsx")
    dest = os.path.join(c, "etapa1", f"{nombre}_evaluada.xlsx")
    shutil.copy(v53, dest)
    if quitar_etapa1:  # la V5.3 de origen se edita con openpyxl (solo se lee después; no es un libro V6.3)
        import openpyxl
        wb = openpyxl.load_workbook(dest)
        for ref in quitar_etapa1:
            wb["Análisis"][ref] = None
        wb.save(dest)
    open(os.path.join(c, "etapa1", "respuesta.md"), "w", encoding="utf-8").write("# respuesta v1 (sintética)\n\nCubo: VIGILAR. Precio de Sí v1: 15.\n")
    json.dump({"empresa": "Empresa X (inventada)", "cubo": "VIGILAR", "precio_de_si": 15}, open(os.path.join(c, "etapa1", "juicio.json"), "w", encoding="utf-8"))
    f1 = json.load(open(os.path.join(RAIZ, "esquema", "fase1_v63.ejemplo.json"), encoding="utf-8"))
    for k in quitar_fase1:
        f1["analisis"].pop(k, None)
    if quitar_precio:
        f1["precio"]["valor"] = None
    if precio is not None:
        f1["precio"]["valor"] = precio
        f1["capitalizacion"]["valor"] = precio * 100
    json.dump(f1, open(os.path.join(c, "fase1_v63.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return c


def correr(c, reaccion, max_vueltas=30):
    """Lanza el pipeline y, cuando espera a un agente, llama a reaccion(c, nombre_agente)."""
    rc = None
    for _ in range(max_vueltas):
        r = subprocess.run([PY, PIPE, c], capture_output=True, text=True)
        rc = r.returncode
        if rc != 10:
            return rc, r.stdout + r.stderr
        esp = open(os.path.join(c, "ESPERANDO.md"), encoding="utf-8").read()
        nombre = esp.split("**")[1]
        reaccion(c, nombre)
    return rc, "demasiadas vueltas"


def estado(c):
    return json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))


def reaccion_normal(variante=None):
    def r(c, nombre):
        if nombre == "extraccion_v63":
            AG.extracto(c)
        elif nombre == "fase_a":
            AG.fase_a(c, limite=(variante == "limite"))
        elif nombre == "fase_b":
            if variante == "bloqueo":
                AG.fase_b(c, g_bueno=0.09, justificar=True)   # g ≥ tasa: error que «no corrige» nunca
            else:
                AG.fase_b(c, justificar=True)
        elif nombre == "fase_c_turno1":
            AG.fase_c(c, 1, material_ausente=("Análisis!C34" if variante == "datos_ausentes" else None), sin_base=(variante == "sin_base"))
        elif nombre == "fase_c_turno2":
            AG.fase_c(c, 2, material_ausente=("Análisis!C34" if variante == "datos_ausentes" else None), sin_base=(variante == "sin_base"))
        elif nombre == "verificacion":
            AG.auditoria(c, "REPETIR" if variante == "auditoria_repetir" else "APROBADO")
        else:
            raise RuntimeError(nombre)
    return r


def t_pasada_completa():
    c = preparar("EmpresaX")
    rc, out = correr(c, reaccion_normal())
    st = estado(c)
    paso("pasada completa: termina (código 0)", rc == 0, out.strip().splitlines()[-1] if out.strip() else "")
    paso("pasada completa: estado final concluido o pendiente_de_investigacion (según la comprobación conjunta)", st.get("estado_analisis") in ("concluido", "pendiente_de_investigacion"), f"estado {st.get('estado_analisis')} · intentos {st['intentos']} · auditoría {st.get('auditoria')}")
    for f in ("ficha.json", "informe.md", "precio.json", "resultados.json", "gramatica.json", "verificacion_integridad.txt"):
        paso(f"pasada completa: existe {f}", os.path.exists(os.path.join(c, f)))
    cc = os.path.exists(os.path.join(c, "comprobacion_conjunta.json"))
    fcj = json.load(open(os.path.join(c, "fase_c.json"), encoding="utf-8"))
    paso("B.6 punto 5: con conclusión provisional no favorable (zona caro → esperar) la comprobación conjunta no se ejecuta", fcj.get("conclusion_provisional") != "comprar" and not cc,
         f"conclusión provisional {fcj.get('conclusion_provisional')} · comprobación conjunta: {cc}")
    ev = os.path.join(c, "EmpresaX_v63_evaluada.xlsx")
    sys.path.insert(0, os.path.join(RAIZ, "scripts")); import config_v2  # noqa: E402
    cfgp = config_v2.cargar(os.path.join(RAIZ, "config_v2.json"))
    r = subprocess.run([PY, cfgp["plantilla"]["verificador"], ev, cfgp["plantilla"]["referencia"]], capture_output=True, text=True)
    paso("criterio 1: libro evaluado íntegro (verificar_v63.py = 0)", r.returncode == 0, (r.stdout.strip().splitlines() or [""])[-1])
    ficha = json.load(open(os.path.join(c, "ficha.json"), encoding="utf-8"))
    c104 = (ficha.get("escalera") or {}).get("zona"), json.load(open(os.path.join(c, "fase_c.json")))["celdas"]["C104"]
    paso("criterio 7: C104 empieza por «Pendiente de decisión de cartera» y sin porcentaje", c104[1].startswith("Pendiente de decisión de cartera") and "%" not in c104[1], c104[1][:120])
    paso("criterio 3/§7.3: estado del libro esperado (LISTO · PROVISIONAL o NO LISTO · incompleto por C08)", (ficha.get("estado_libro") or "").startswith(("LISTO · PROVISIONAL", "NO LISTO · incompleto", "NO LISTO · evidencias")), ficha.get("estado_libro"))
    print(open(os.path.join(c, "informe.md"), encoding="utf-8").read()[:1200])
    return c


def t_favorable():
    c = preparar("EmpresaX_favorable", precio=16)
    rc, out = correr(c, reaccion_normal())
    st = estado(c)
    cc = os.path.exists(os.path.join(c, "comprobacion_conjunta.json"))
    j = json.load(open(os.path.join(c, "comprobacion_conjunta.json"))) if cc else {}
    paso("12(a) favorable: comprobación conjunta ejecutada sobre la copia de prueba y documentada (combinación, rangos, escalera bajo la combinación)",
         rc == 0 and cc and os.path.exists(os.path.join(c, "comprobacion_conjunta", "EmpresaX_favorable_conj.xlsx")) and j.get("combinacion") and "escalera_bajo_combinacion" in j,
         f"sobrevive {j.get('sobrevive')} · zona original {(j.get('escalera_original') or {}).get('zona_precio_actual')} → bajo combinación {(j.get('escalera_bajo_combinacion') or {}).get('zona_precio_actual')}")
    fc = json.load(open(os.path.join(c, "fase_c.json")))
    esperado = "concluido" if j.get("sobrevive") else "pendiente_de_investigacion"
    paso("12(b) el estado final sigue al resultado de la comprobación conjunta", st.get("estado_analisis") == esperado and (fc["decision"]["accion"] == ("comprar" if j.get("sobrevive") else None)),
         f"estado {st.get('estado_analisis')} · acción {fc['decision']['accion']} · cubo {fc['cubo_final']}")
    paso("12(d) la combinación no usa la suma del tornado ni la palanca más influyente (solo celdas de hipótesis sin fundamento)", all(k.split('!')[1] in ('B14','C14','D14','B15','C15','D15','B16','C16','D16','B18','C18','D18','B68','C68','D68','B69','C69','D69') for k in j.get('combinacion', {})), str(list(j.get('combinacion', {}).keys())))
    ev = os.path.join(c, "EmpresaX_favorable_v63_evaluada.xlsx")
    import hashlib
    paso("12(a) la copia de prueba no sustituye al libro (hash distinto, libro íntegro)", hashlib.sha256(open(ev,'rb').read()).hexdigest() != j.get("hash_copia"))
    errs = ((j.get("resultados_bajo_combinacion") or {}).get("errores_gramatica") or [])
    paso("B.6: la gramática sobre la copia no marca como error las hipótesis «sin juicio propio» movidas por la combinación (solo reglas [I]/[N]/formato)", not errs, str(errs)[:300])


def t_favorable_sobrevive():
    """Precio muy por debajo del escenario MALO: la combinación adversa tiene que sobrevivir y el cierre ser concluido · comprar · Sí
    con fundamento_material.resultado = comprobacion_conjunta_superada (D10, camino principal de una conclusión favorable)."""
    c = preparar("EmpresaX_sobrevive", precio=8)
    rc, out = correr(c, reaccion_normal())
    st = estado(c)
    j = json.load(open(os.path.join(c, "comprobacion_conjunta.json"))) if os.path.exists(os.path.join(c, "comprobacion_conjunta.json")) else {}
    fc = json.load(open(os.path.join(c, "fase_c.json"))) if os.path.exists(os.path.join(c, "fase_c.json")) else {}
    fm = fc.get("fundamento_material") or {}
    paso("12(a) sobrevive: la comprobación conjunta se ejecutó y la conclusión favorable sobrevive (zona bajo la combinación cumple la regla, sin errores)",
         rc == 0 and j.get("sobrevive") is True and not ((j.get("resultados_bajo_combinacion") or {}).get("errores_gramatica")),
         f"sobrevive {j.get('sobrevive')} · zona original {(j.get('escalera_original') or {}).get('zona_precio_actual')} → bajo combinación {(j.get('escalera_bajo_combinacion') or {}).get('zona_precio_actual')} · errores {(j.get('resultados_bajo_combinacion') or {}).get('errores_gramatica')}")
    paso("12(b) sobrevive: cierre concluido · comprar · Sí · comprobacion_conjunta_superada · auditoría APROBADO",
         st.get("estado_analisis") == "concluido" and (fc.get("decision") or {}).get("accion") == "comprar" and fc.get("cubo_final") == "Sí" and fm.get("resultado") == "comprobacion_conjunta_superada" and st.get("auditoria") == "APROBADO",
         f"estado {st.get('estado_analisis')} · acción {(fc.get('decision') or {}).get('accion')} · cubo {fc.get('cubo_final')} · resultado {fm.get('resultado')} · auditoría {st.get('auditoria')}")
    ficha = json.load(open(os.path.join(c, "ficha.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "ficha.json")) else {}
    paso("criterio 7 †: ficha válida contra su esquema y sin diagnóstico vigente en concluido", st.get("ficha_valida") is True and not os.path.exists(os.path.join(c, "diagnostico.md")) and ficha.get("estado_analisis") == "concluido",
         f"ficha_valida {st.get('ficha_valida')} · diagnostico.md {os.path.exists(os.path.join(c, 'diagnostico.md'))}")
    paso("D16: ningún porcentaje en C104 ni tamaño de posición en la ficha", "%" not in (fc.get("celdas") or {}).get("C104", "%") and "posición" not in json.dumps(ficha.get("insumos_decision_cartera"), ensure_ascii=False).lower())


def t_abstencion():
    c = preparar("EmpresaX_sin_precio", quitar_precio=True)
    rc, out = correr(c, reaccion_normal())
    st = estado(c)
    paso("10 abstención: sin precio el pipeline se detiene en la entrada, pendiente_de_datos, sin agentes", rc == 0 and st.get("estado_analisis") == "pendiente_de_datos" and not os.path.exists(os.path.join(c, "fase_a.json")) and os.path.exists(os.path.join(c, "diagnostico.md")),
         open(os.path.join(c, "diagnostico.md"), encoding="utf-8").read()[:300] if os.path.exists(os.path.join(c, "diagnostico.md")) else out[-300:])


def t_bloqueo():
    c = preparar("EmpresaX_bloqueo")
    rc, out = correr(c, reaccion_normal("bloqueo"))
    st = estado(c)
    d = json.load(open(os.path.join(c, "diagnostico.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "diagnostico.json")) else {}
    paso("13 bloqueo: error de gramática persistente → no_entregable tras max_correcciones (nunca APROBADO)", rc == 0 and st.get("estado_analisis") == "no_entregable" and st["intentos"]["fase_b"] == 3 and d.get("causa", {}).get("tipo") == "fallo_de_implementacion",
         f"estado {st.get('estado_analisis')} · intentos B {st['intentos']['fase_b']} · causa {d.get('causa', {}).get('detalle', '')[:120]}")


def t_limite():
    c = preparar("EmpresaX_limite")
    rc, out = correr(c, reaccion_normal("limite"))
    st = estado(c)
    paso("14 límite del modelo: C62 «otro método» → modelo_no_aplicable, sin fase B, con ficha e informe", rc == 0 and st.get("estado_analisis") == "modelo_no_aplicable" and not os.path.exists(os.path.join(c, "fase_b.json")) and os.path.exists(os.path.join(c, "ficha.json")),
         f"estado {st.get('estado_analisis')} · ficha.cubo_cualitativo {json.load(open(os.path.join(c, 'ficha.json'))).get('cubo_cualitativo_fase_a') if os.path.exists(os.path.join(c, 'ficha.json')) else None}")


def t_datos_ausentes():
    c = preparar("EmpresaX_sin_C34", quitar_fase1=("C34",), quitar_etapa1=("C34",), precio=16)
    rc, out = correr(c, reaccion_normal("datos_ausentes"))
    st = estado(c)
    da = json.load(open(os.path.join(c, "datos_ausentes.json"), encoding="utf-8"))
    d = json.load(open(os.path.join(c, "diagnostico.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "diagnostico.json")) else {}
    fc = json.load(open(os.path.join(c, "fase_c.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "fase_c.json")) else {}
    paso("15 datos ausentes: C34 ausente está en datos_ausentes.json", any(x["dato"] == "Análisis!C34" for x in da), str([x["dato"] for x in da]))
    paso("15 datos ausentes: la fase C lo declara material → pendiente_de_datos, acción null, diagnóstico con el dato", rc == 0 and st.get("estado_analisis") == "pendiente_de_datos" and (fc.get("decision") or {}).get("accion") is None and "C34" in json.dumps(d.get("causa", {}), ensure_ascii=False),
         f"estado {st.get('estado_analisis')} · causa {d.get('causa', {}).get('detalle', '')[:140]}")


def t_auditoria_repetir():
    """§10.2.13: una auditoría forzada a REPETIR agota max_correcciones_auditoria (2) y termina en no_entregable, nunca APROBADO;
    cada corrección pide una fase C NUEVA (archivo más nuevo) y una auditoría NUEVA."""
    c = preparar("EmpresaX_repetir", precio=8)
    rc, out = correr(c, reaccion_normal("auditoria_repetir"), max_vueltas=40)
    st = estado(c)
    d = json.load(open(os.path.join(c, "diagnostico.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "diagnostico.json")) else {}
    paso("13 auditoría REPETIR persistente → no_entregable tras 2 correcciones de la fase C (nunca APROBADO por agotamiento)",
         rc == 0 and st.get("estado_analisis") == "no_entregable" and st["auditoria"] == "REPETIR" and st["intentos"]["auditoria"] == 3 and d.get("causa", {}).get("tipo") == "fallo_de_implementacion",
         f"estado {st.get('estado_analisis')} · auditoría {st.get('auditoria')} · intentos auditoría {st['intentos']['auditoria']} · causa {d.get('causa', {}).get('detalle', '')[:100]}")
    hist = "\n".join(st.get("historial", []))
    paso("13 cada corrección pidió una auditoría y una fase C nuevas (3 auditorías leídas, 3 pasadas de la fase C)", hist.count("13:auditoria.md") >= 0 and hist.count("auditoría REPETIR: corrección") == 2 and hist.count("agente simulado") == 0,
         f"correcciones registradas: {hist.count('auditoría REPETIR: corrección')}")
    ficha = json.load(open(os.path.join(c, "ficha.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "ficha.json")) else {}
    paso("13 en no_entregable la ficha no lleva cubo ni acción y valida contra su esquema", ficha.get("cubo") is None and ficha.get("decision") is None and st.get("ficha_valida") is True, f"cubo {ficha.get('cubo')} · decision {ficha.get('decision')} · válida {st.get('ficha_valida')}")


def t_sin_base():
    c = preparar("EmpresaX_sin_base", precio=16)
    rc, out = correr(c, reaccion_normal("sin_base"))
    st = estado(c)
    paso("12(c) hipótesis sin base para acotar → pendiente_de_investigacion sin comprobación conjunta", rc == 0 and st.get("estado_analisis") == "pendiente_de_investigacion" and not os.path.exists(os.path.join(c, "comprobacion_conjunta.json")),
         f"estado {st.get('estado_analisis')}")


if __name__ == "__main__":
    os.makedirs(os.path.join(BASE, "_origen"), exist_ok=True)
    if not os.path.exists(os.path.join(BASE, "_origen", "EmpresaX_v53_evaluada_sintetica.xlsx")):
        # el libro de partida viene en el paquete (pruebas/sintetico/_origen/); sin él la prueba no puede correr
        print("FALTA pruebas/sintetico/_origen/EmpresaX_v53_evaluada_sintetica.xlsx (va en el paquete del repositorio)")
        sys.exit(2)
    pruebas = {"completa": t_pasada_completa, "favorable": t_favorable, "sobrevive": t_favorable_sobrevive, "abstencion": t_abstencion, "bloqueo": t_bloqueo, "limite": t_limite, "datos_ausentes": t_datos_ausentes, "sin_base": t_sin_base, "auditoria_repetir": t_auditoria_repetir}
    sel = sys.argv[1:] or list(pruebas)
    for n in sel:
        print(f"\n=== {n} ===")
        try:
            pruebas[n]()
        except Exception as e:  # noqa
            import traceback; traceback.print_exc()
            paso(n, False, f"excepción: {e}")
    json.dump(resultados, open(os.path.join(BASE, "resultado_pruebas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    n_ok = sum(r["ok"] for r in resultados)
    print(f"\n{n_ok}/{len(resultados)} pruebas PASAN")
    sys.exit(0 if n_ok == len(resultados) else 1)
