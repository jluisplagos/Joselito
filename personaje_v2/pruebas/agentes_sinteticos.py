#!/usr/bin/env python3
"""Agentes SIMULADOS para las pruebas con datos sintéticos (§10.2: 10, 12(a), 13, 14, 15). Generan fase_a.json, fase_b.json,
fase_c.json (dos turnos), extracto_v63.md y auditoria.md con el esquema del Anexo D, a partir de los archivos que el pipeline
deja en la carpeta (datos_v63.json, referencias_mecanicas.json, gramatica.json, datos_ausentes.json, precio.json…).
No son el personaje: son un sustituto mecánico para probar el pipeline, la gramática y los estados.
"""
import datetime as dt
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(AQUI), "scripts"))
import celdas_v2 as C  # noqa: E402

OBS = "[Clase: {clase}] [Confianza: media] Hereda: {hereda}. {extra}Apoyo: Historia C46 y extracto p. 3 (sintético). Lo sustituiría: un dato contrario en el próximo informe."


def cargar(c, n):
    p = os.path.join(c, n)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def extracto(c):
    open(os.path.join(c, "extracto_v63.md"), "w", encoding="utf-8").write(
        "# extracto_v63 (sintético)\n\n## 1. Mercado y cuota\nNo encontrado en los documentos.\n\n## 9. Lo que no encontré\n- Tamaño del mercado (no publicado)\n- Cuota de mercado\n")


def fase_a(c, motor="A", c62=None, limite=False, c13="Sí"):
    d = cargar(c, "datos_v63.json")
    her = (d.get("herencia") or {}).get("celdas") or {}
    c62 = c62 or {"A": "Sí", "B": "No · financiación cambia mucho", "C": "No · banco o aseguradora"}[motor]
    celdas = {"C11": "Sí", "C12": "Sí", "C13": c13, "C14": "Calidad a precio razonable", "C17": "Sí", "C18": "Sí", "C19": "Sí", "C20": "Incert. alta + riesgo bajo",
              "C25": "Sí", "C27": "Estable", "C51": "Sí", "C56": 0.09, "C61": "No está claro", "C62": c62, "C97": "Neutral", "C98": "Buena",
              "Palancas!C5": "Madura en crecimiento", "Palancas!C6": "Ninguno", "Palancas!C8": "Último año", "Palancas!C9": "No", "Palancas!C10": None,
              "Palancas!C43": "No aplica", "Palancas!C47": "Ninguna",
              "B65": "El viento de cola se frena", "C65": "Crece al ritmo de su mercado", "D65": "Gana cuota: el moat se ensancha",
              "B66": "El mercado se enfría y la empresa crece al 3 % con el margen de siempre.", "C66": "Crece como su mercado, al 8 %, y mantiene el margen del 20 %.", "D66": "Gana cuota y el margen sube dos puntos por escala; la mejora se la queda la empresa."}
    herencia = {}
    for k in ("C11", "C12", "C13", "C14", "C17", "C18", "C19", "C20", "C25", "C27", "C51", "C56", "C61", "C62", "C97", "C98", "B65", "C65", "D65", "B66", "C66", "D66"):
        antes = her.get(k)
        herencia[k] = {"etapa1": antes, "decision": "mantiene" if antes == celdas[k] else "cambia", "motivo": "misma_evidencia" if antes == celdas[k] else "evidencia_nueva",
                       "evidencia_y_razonamiento": "revisada la Historia de 10 años (filas 6, 7, 29) y el extracto p. 3: sostiene la respuesta (sintético)"}
    obs = {}
    for h, dd in C.CELDAS.items():
        for ref, meta in dd.items():
            if meta["fase"] == "A":
                k = ref if h == "Análisis" else f"{h}!{ref}"
                obs[k] = OBS.format(clase="fundamentada", hereda=(f"{her.get(ref)} → mantiene (misma_evidencia): la Historia la sostiene" if h == "Análisis" else "nueva en V6.3"), extra="")
    fa = {"empresa": d["analisis"].get("B3"), "ticker": d["analisis"].get("D3"), "fecha_analisis": str(d["analisis"].get("D4"))[:10], "version_personaje": "v2.0",
          "cinco_frases": "Vende X a Y; cobra por Z; la caja sale de W (sintético).",
          "seis_preguntas": {"confio_en_la_gestion": "sí (sintético)", "puede_danar_reputacion": "no", "que_puede_salir_mal": "que el mercado se enfríe", "lo_entiendo": "sí", "necesita_capital": "poco", "que_caja_espero": "la de los últimos 3 años"},
          "descalificadores": [{"nombre": "deuda que mata", "aplica": False, "evidencia": "deuda neta/EBITDA 0,8 (Análisis C33)"}],
          "foso": {"tipo": "coste de cambio", "pruebas": {"sobrino_idiota": "sí", "duracion": "10 años", "quien_me_mata": "nadie visible", "empresa_o_nicho": "empresa"}},
          "cubo_provisional": "Vigilar", "limite_del_modelo": {"aplica": limite, "cual": "L3" if limite else None, "porque": "otro método (sintético)" if limite else None},
          "celdas": celdas, "herencia": herencia,
          "escenarios": {e: {"historia": celdas[f"{col}66"], "mecanismo": "volumen (sintético)", "quien_se_queda_la_mejora": "la empresa", "que_lo_pararia": "un competidor con precio", "hechos_en_que_se_apoya": ["Historia fila 28", "extracto p. 3"]} for e, col in (("MALO", "B"), ("NORMAL", "C"), ("BUENO", "D"))},
          "observaciones": obs, "lo_que_no_se": ["la cuota de mercado"], "que_no_sabria_munger": ["nada en particular"]}
    json.dump(fa, open(os.path.join(c, "fase_a.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(os.path.join(c, "fase_a.md"), "w", encoding="utf-8").write("# fase A (sintética)\n")
    return fa


def fase_b(c, clase_normal="sin juicio propio", roic_bueno=None, g_bueno=None, prob=None, justificar=True, variante=None):
    refs = cargar(c, "referencias_mecanicas.json")
    d = cargar(c, "datos_v63.json")
    motor = refs["motor"]
    def ent(pal, esc, valor=None, clase=None, porque="copio la referencia mecánica"):
        r = refs["palancas"][pal].get(esc)
        motivo = refs["palancas"][pal].get("referencia_no_disponible_motivo")
        v = r if valor is None else valor
        cl = clase or (clase_normal if valor is None else "fundamentada")
        if r is None and cl == "sin juicio propio":
            cl = "técnico"
        return {"referencia_mecanica": r, "referencia_no_disponible_motivo": motivo, "valor": v, "desviacion": (None if r is None else round(v - r, 6)), "clase": cl, "confianza": "media",
                "porque": porque, "apoyo": "Historia C46, C49, C53, C55 (sintético)", "lo_sustituiria": "un cambio en la serie de márgenes"}
    pal = {p: {e: ent(p, e) for e in ("MALO", "NORMAL", "BUENO")} for p in ("crecimiento_1_5", "margen_objetivo", "s2c", "g_perpetuo", "roic_lp")}
    if motor == "C":
        pal["s2c"] = {e: ent("s2c", e, valor=None, clase="convención") | {"valor": None, "desviacion": None} for e in ("MALO", "NORMAL", "BUENO")}
    if roic_bueno is not None:
        pal["roic_lp"]["BUENO"] = ent("roic_lp", "BUENO", roic_bueno, "fundamentada", "el foso dura (sintético)")
    if g_bueno is not None:
        pal["g_perpetuo"]["BUENO"] = ent("g_perpetuo", "BUENO", g_bueno, "fundamentada", "prueba de error (sintético)")
    probs = prob or {"MALO": 0.2, "NORMAL": 0.6, "BUENO": 0.2}
    pal["probabilidades"] = {e: ent("probabilidades", e, probs[e], "sin juicio propio" if prob is None else "fundamentada") for e in ("MALO", "NORMAL", "BUENO")}
    pal["probabilidades"]["argumento"] = "referencia 0,2/0,6/0,2 (convención)"
    cel = {}
    for p, (hoja, b, cc, dd) in {"crecimiento_1_5": ("Palancas", "B14", "C14", "D14"), "margen_objetivo": ("Palancas", "B15", "C15", "D15"), "s2c": ("Palancas", "B16", "C16", "D16"),
                                  "g_perpetuo": ("Análisis", "B68", "C68", "D68"), "roic_lp": ("Palancas", "B18", "C18", "D18"), "probabilidades": ("Análisis", "B69", "C69", "D69")}.items():
        for e, ref in zip(("MALO", "NORMAL", "BUENO"), (b, cc, dd)):
            cel[f"{hoja}!{ref}"] = pal[p][e]["valor"]
    q = refs["palancas"]["quiebra"]
    cel.update({"Análisis!C76": 0 if motor == "A" else None, "Palancas!C22": q.get("C22"), "Palancas!C23": q.get("C23"), "Palancas!C24": None, "Palancas!C44": None})
    her = (d.get("herencia") or {}).get("celdas") or {}
    herencia = {k: {"etapa1": her.get(k), "decision": "mantiene" if her.get(k) == cel.get(f"Análisis!{k}") else "cambia", "motivo": "misma_evidencia" if her.get(k) == cel.get(f"Análisis!{k}") else "definicion_o_medicion_distinta",
                    "evidencia_y_razonamiento": "la V6.3 mide g y probabilidades con el mismo sentido; revisada la Historia (sintético)"} for k in ("B68", "C68", "D68", "B69", "C69", "D69", "C76")}
    obs = {}
    for h, dd in C.CELDAS.items():
        for ref, meta in dd.items():
            if meta["fase"] == "B":
                k = f"{h}!{ref}"
                cl = "fundamentada"
                for p, (hoja, *rr) in {"crecimiento_1_5": ("Palancas", "B14", "C14", "D14"), "margen_objetivo": ("Palancas", "B15", "C15", "D15"), "s2c": ("Palancas", "B16", "C16", "D16"), "g_perpetuo": ("Análisis", "B68", "C68", "D68"), "roic_lp": ("Palancas", "B18", "C18", "D18"), "probabilidades": ("Análisis", "B69", "C69", "D69")}.items():
                    if h == hoja and ref in rr:
                        cl = pal[p][("MALO", "NORMAL", "BUENO")[rr.index(ref)]]["clase"]
                hereda = "nueva en V6.3" if h == "Palancas" else f"{her.get(ref)} → mantiene (misma_evidencia): misma definición"
                extra = f"Referencia mecánica: ver referencias_mecanicas.json. Decisión: {cel.get(k)}. Desviación: {'ninguna' if cl == 'sin juicio propio' else 'declarada'} porque sintético. "
                obs[k] = OBS.format(clase=cl, hereda=hereda, extra=extra)
    fb = {"motor": motor, "palancas": pal, "quiebra": {"C22": q.get("C22"), "C23": q.get("C23"), "disparadores": q.get("disparadores") or [], "clase": "convención", "porque": "sin disparador (sintético)"},
          "mercado": {"C24": None, "fuente": None}, "exceso_caja": {"C76": 0 if motor == "A" else None, "clase": "fundamentada", "porque": "sin caja ociosa documentada"},
          "fcf_normalizado": {"C44": None, "clase": None, "porque": "FCF base > 0"}, "desviaciones_justificadas": [], "limite_del_modelo": {"aplica": False, "cual": None, "porque": None},
          "herencia": herencia, "dos_errores": {"mas_cerca_de": "regatear", "porque": "sintético"}, "celdas": cel, "observaciones": obs}
    if justificar:
        g = cargar(c, "gramatica.json")
        PAL_DE = {"G4": "roic_lp", "G5": "margen_objetivo", "G6": "crecimiento_1_5", "G7": "s2c", "G3": "g_perpetuo", "G10b": "probabilidades"}
        if g:
            for h_ in g["hallazgos"]:
                if h_["categoria"] == "desviación":
                    fb["desviaciones_justificadas"].append({"comprobacion": h_["id"], "escenario": h_["escenario"] or "todos",
                                                            "justificacion": f"Justificación sintética para {h_['id']}: la Historia (fila 29: margen del 20 % en los diez ejercicios; fila 28) y el extracto p. 3 sostienen el valor, y el mecanismo es la escala.",
                                                            "hechos": ["Historia fila 29", "extracto p. 3"], "clase": "fundamentada"})
                    # una palanca «sin juicio propio» no puede sostener una desviación (§B.3): el agente sintético la declara fundamentada
                    # con el mismo valor (desviación 0 respecto a la referencia) y hechos de la Historia, como haría el personaje
                    palanca = PAL_DE.get(h_["id"])
                    escs = [h_["escenario"]] if h_["escenario"] else ["MALO", "NORMAL", "BUENO"]
                    for e in escs:
                        if palanca and palanca in pal and e in pal[palanca] and pal[palanca][e].get("clase") in ("sin juicio propio", "técnico"):
                            pal[palanca][e]["clase"] = "fundamentada"
                            pal[palanca][e]["porque"] = "la referencia coincide con la propia historia de la empresa (sintético)"
                            pal[palanca][e]["apoyo"] = "Historia fila 29 (margen) y fila 28 (crecimiento), extracto p. 3 (sintético)"
                            # la Observación de la celda cambia de clase
                            for k_, v_ in obs.items():
                                hoja_, ref_ = k_.split("!")
                                mapa_ = {"crecimiento_1_5": ("Palancas", "B14", "C14", "D14"), "margen_objetivo": ("Palancas", "B15", "C15", "D15"), "s2c": ("Palancas", "B16", "C16", "D16"), "g_perpetuo": ("Análisis", "B68", "C68", "D68"), "roic_lp": ("Palancas", "B18", "C18", "D18"), "probabilidades": ("Análisis", "B69", "C69", "D69")}[palanca]
                                if hoja_ == mapa_[0] and ref_ == mapa_[1 + ("MALO", "NORMAL", "BUENO").index(e)]:
                                    obs[k_] = v_.replace("[Clase: sin juicio propio]", "[Clase: fundamentada]").replace("[Clase: técnico]", "[Clase: fundamentada]").replace("Desviación: ninguna", "Desviación: ninguna (fundamentada en la propia historia)")
    json.dump(fb, open(os.path.join(c, "fase_b.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(os.path.join(c, "fase_b.md"), "w", encoding="utf-8").write("# fase B (sintética)\n")
    return fb


def fase_c(c, turno, material_ausente=None, sin_base=False, favorable=True):
    fb, precio, da, cc = cargar(c, "fase_b.json"), cargar(c, "precio.json") or {}, cargar(c, "datos_ausentes.json") or [], cargar(c, "comprobacion_conjunta.json")
    res, d = cargar(c, "resultados.json") or {}, cargar(c, "datos_v63.json")
    fecha = str(d["analisis"].get("D4"))[:10]
    f0 = dt.date.fromisoformat(fecha)
    f1 = (f0 + dt.timedelta(days=540)).isoformat()
    revisados = [{"dato": x["dato"], "que_falta": x.get("que"), "conclusion_afectada": "ninguna celda de juicio" if x["dato"] != material_ausente else "descalificador «deuda que mata»",
                  "material_para_conclusion_favorable": x["dato"] == material_ausente, "porque": "no entra en la escalera ni en los descalificadores (sintético)" if x["dato"] != material_ausente else "sin la liquidez no puedo descartar que la deuda apriete (sintético)"} for x in da]
    alguno = any(r["material_para_conclusion_favorable"] for r in revisados)
    hip = []
    for p in ("crecimiento_1_5", "margen_objetivo", "s2c", "g_perpetuo", "roic_lp", "probabilidades"):
        for e in ("MALO", "NORMAL", "BUENO"):
            ent = (fb["palancas"].get(p) or {}).get(e) or {}
            if ent.get("clase") in ("sin juicio propio", "técnico"):
                v = ent.get("valor")
                if sin_base and p == "roic_lp":
                    ad = {"hay_base": False, "rango": None, "evidencia": "no hay base para acotarlo: la media del sector es un dato de otras empresas y el umbral de la plantilla no es un techo económico (sintético)"}
                else:
                    ad = {"hay_base": True, "rango": [round(v * 0.8, 4), v] if isinstance(v, (int, float)) and v is not None else None,
                          "evidencia": "suelo = el peor valor de la propia serie (Historia, sintético); techo = el valor decidido"}
                hip.append({"celda": p + "·" + e, "hipotesis": f"{p} {e} = {v}", "clase": ent.get("clase"), "porque_sin_fundamento": "copiada de la referencia (sintético)", "alternativas_defendibles": ad})
    conclusion_prov = "comprar" if favorable and precio.get("zona") in ("cumple_regla_k", "bajo_malo") else "esperar"
    procede = favorable and conclusion_prov == "comprar" and bool(hip) and all(h["alternativas_defendibles"]["hay_base"] for h in hip) and not alguno
    comb = {}
    if procede:
        # combinación: extremos desfavorables de los rangos (probabilidades MALO ↑, BUENO ↓; palancas al suelo)
        mapa = {"crecimiento_1_5": ("Palancas", "B14", "C14", "D14"), "margen_objetivo": ("Palancas", "B15", "C15", "D15"), "s2c": ("Palancas", "B16", "C16", "D16"), "g_perpetuo": ("Análisis", "B68", "C68", "D68"), "roic_lp": ("Palancas", "B18", "C18", "D18")}
        for h in hip:
            p, e = h["celda"].split("·")
            if p == "probabilidades":
                continue
            hoja, *refs = mapa[p]
            ref = refs[("MALO", "NORMAL", "BUENO").index(e)]
            lo = h["alternativas_defendibles"]["rango"][0]
            if p == "g_perpetuo":
                lo = max(x for x in (0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03) if x <= lo)
            elif p == "s2c":
                lo = round(lo, 1)
            elif p == "roic_lp":
                lo = round(lo, 2)
            else:
                lo = round(round(lo / 0.005) * 0.005, 4)
            comb[f"{hoja}!{ref}"] = lo
        if any(h["celda"].startswith("probabilidades") for h in hip):
            comb.update({"Análisis!B69": 0.3, "Análisis!C69": 0.5, "Análisis!D69": 0.2})
    fm = {"hipotesis_sin_fundamento": hip,
          "comprobacion_conjunta": {"procede": procede, "combinacion": comb or None, "coherencia_economica": "si el foso dura menos, bajan a la vez margen y ROIC terminal, y el MALO gana probabilidad (sintético)" if procede else None, "sobrevive": None},
          "resultado": None, "hipotesis_que_mas_condiciona": hip[0]["celda"] if hip else None, "que_lo_resolveria": "el ROIC por segmento de los informes (sintético)"}
    estado, cubo, accion, prec_obj = None, None, None, None
    if turno == 2:
        if cc is not None:
            fm["comprobacion_conjunta"]["sobrevive"] = cc.get("sobrevive")
        if alguno and conclusion_prov in ("comprar", "esperar"):
            estado, cubo, accion = "pendiente_de_datos", "Vigilar", None
            fm["resultado"] = "no_procede"
        elif conclusion_prov == "comprar":
            if not hip:
                estado, cubo, accion, fm["resultado"] = "concluido", "Sí", "comprar", "sin_limitacion"
            elif not all(h["alternativas_defendibles"]["hay_base"] for h in hip):
                estado, cubo, accion, fm["resultado"] = "pendiente_de_investigacion", "Vigilar", None, "pendiente_de_investigacion"
            elif cc and cc.get("sobrevive"):
                estado, cubo, accion, fm["resultado"] = "concluido", "Sí", "comprar", "comprobacion_conjunta_superada"
            else:
                estado, cubo, accion, fm["resultado"] = "pendiente_de_investigacion", "Vigilar", None, "pendiente_de_investigacion"
        else:
            estado, cubo, accion, prec_obj, fm["resultado"] = "concluido", "Vigilar", "esperar", precio.get("precio_si"), "no_procede"
    fund_txt = {"sin_limitacion": "lista vacía", "comprobacion_conjunta_superada": "comprobación conjunta superada", "pendiente_de_investigacion": "pendiente de investigación", "no_procede": "pendiente de datos" if estado == "pendiente_de_datos" else "lista no vacía (conclusión no favorable)"}.get(fm["resultado"], "pendiente")
    concl_txt = {"comprar": "comprar al precio actual", "esperar": f"esperar: precio de Sí ≤ {precio.get('precio_si'):.2f}" if precio.get("precio_si") else "esperar", None: ("sin conclusión (pendiente de datos: " + ", ".join(r["dato"] for r in revisados if r["material_para_conclusion_favorable"]) + ")") if estado == "pendiente_de_datos" else "sin conclusión (pendiente de investigación)"}[accion]
    c104 = f"{C.C104_PREFIJO} · conclusión del personaje: {concl_txt} · zona {precio.get('zona')} · precio de Sí ≤ {precio.get('precio_si') or 0:.2f} · precio esc. MALO {precio.get('precio_escenario_malo') or 0:.2f} · ponderado {precio.get('ponderado') or 0:.2f} · fundamento {fund_txt}"
    cel = {"C93": "Sí", "C103": "Sí", "C104": c104, "B101": "Tesis sintética en cinco frases.", "B102": "Tesis inversa sintética con hechos (Historia fila 29).",
           "Palancas!A38": "Ventas FY siguiente ≥ 1.000 mm (sintético)", "Palancas!B38": f1, "Palancas!C38": 0.7, "Palancas!A39": "Margen EBIT ≥ 18 % (sintético)", "Palancas!B39": f1, "Palancas!C39": 0.6,
           "Palancas!A40": "Acciones diluidas ≤ 100 mm (sintético)", "Palancas!B40": f1, "Palancas!C40": 0.6,
           "Diagnóstico V6!B222": (hip[0]["hipotesis"] if hip else "ninguna hipótesis sin fundamento; la que más condiciona es el margen objetivo"), "Diagnóstico V6!B223": "el ROIC por segmento de los informes (sintético)"}
    her = (d.get("herencia") or {}).get("celdas") or {}
    herencia = {k: {"etapa1": her.get(k), "decision": "cambia", "motivo": "evidencia_nueva", "evidencia_y_razonamiento": "reescrita en la etapa 2 con la Historia de 10 años (S-8, sintético)"} for k in ("C93", "B101", "B102", "C103", "C104")}
    obs = {}
    for h, dd in C.CELDAS.items():
        for ref, meta in dd.items():
            if meta["fase"] == "C" and meta.get("cm"):
                k = ref if h == "Análisis" else f"{h}!{ref}"
                obs[k] = OBS.format(clase="fundamentada", hereda=(f"{her.get(ref)} → cambia (evidencia_nueva): reescrita" if h == "Análisis" else "nueva en V6.3"), extra="")
    g = cargar(c, "gramatica.json") or {"hallazgos": []}
    dj = [{"comprobacion": x["id"], "escenario": x["escenario"] or "todos", "justificacion": f"Justificación sintética de {x['id']} tras el recálculo: la pérdida de ventaja en el año 11 está en la tesis; Historia fila 33 y extracto p. 3.", "hechos": ["Historia fila 33", "extracto p. 3"], "clase": "fundamentada"}
          for x in g["hallazgos"] if x["categoria"] == "desviación" and x["id"] in ("G8", "G16", "G17")]
    fc = {"turno": turno, "una_sola_historia": {"coherente": True, "incoherencias": []},
          "lo_que_dice_la_hoja": {"semaforos_relevantes": [], "peso_terminal_NORMAL": ((res.get("por_escenario") or {}).get("peso_terminal") or [None, None, None])[1], "salto_anio_11": {}, "dcf_inverso": str(precio.get("g_impl_actual")), "palanca_mas_influyente": (res.get("tornado") or {}).get("mas_influyente"), "nota": "el tornado es información, no criterio"},
          "desviaciones_justificadas": dj, "autocomprobacion": [{"sesgo": s, "hallazgo": "nada relevante (sintético)", "cambio": "ninguno porque sintético"} for s in ("anclaje en la etapa 1", "anclaje en el precio o en la fuente externa", "consistencia y compromiso", "historia bonita / viento de cola atribuido a la empresa", "optimismo del BUENO frente a la tasa base", "doble castigo del mismo riesgo", "disponibilidad (lo vívido del extracto)", "autoridad (guía de la dirección como hecho)", "¿el MALO es de verdad malo?", "lo no numerable que pesa y no está en las palancas")],
          "revisar_palancas": False, "instrucciones_revision": None, "limite_del_modelo": {"aplica": False}, "cubo_provisional": "Sí" if conclusion_prov == "comprar" else "Vigilar", "conclusion_provisional": conclusion_prov,
          "revision_datos_ausentes": {"revisados": revisados, "alguno_material": alguno}, "fundamento_material": fm,
          "estado_analisis": estado, "cubo_final": cubo, "escalera": {"de": "precio.json"},
          "decision": {"accion": accion, "precio_objetivo": prec_obj, "condicion": None, "condiciones_revision": {"al_alza": "…", "a_la_baja": "…"}},
          "insumos_decision_cartera": {"precio_actual": precio.get("precio"), "zona": precio.get("zona"), "precio_de_si": precio.get("precio_si"), "precio_escenario_malo": precio.get("precio_escenario_malo"), "ponderado": precio.get("ponderado"),
                                       "distancia_a_precio_si": (precio.get("distancias") or {}).get("a_precio_si"), "distancia_a_malo": (precio.get("distancias") or {}).get("a_malo"), "fundamento": fund_txt,
                                       "datos_ausentes_materiales": [r["dato"] for r in revisados if r["material_para_conclusion_favorable"]], "descalificadores_considerados": ["deuda que mata"], "r": 0.09, "r_minima": res.get("r_minima_C17"), "palanca_mas_influyente": (res.get("tornado") or {}).get("mas_influyente")},
          "herencia": herencia, "comparacion_etapa_1": {"cubo_v1": her.get("C104"), "precio_de_si_v1": None, "cubo_v2": cubo, "precio_de_si_v2": precio.get("precio_si"), "por_que_difieren": "sintético"},
          "celdas": cel, "celdas_corregidas": {}, "cambiaria_de_cubo": {"a_si": "…", "a_no": "…", "a_demasiado_dificil": "…"}, "observaciones": obs, "confianza_global": "media"}
    json.dump(fc, open(os.path.join(c, "fase_c.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    open(os.path.join(c, "fase_c.md"), "w", encoding="utf-8").write("# fase C (sintética)\n")
    return fc


def auditoria(c, veredicto="APROBADO"):
    open(os.path.join(c, "auditoria.md"), "w", encoding="utf-8").write("# auditoría (sintética)\n\n1. PASA · mecánica\n…\n\nVEREDICTO: " + veredicto + "\n")


if __name__ == "__main__":
    print(__doc__)
