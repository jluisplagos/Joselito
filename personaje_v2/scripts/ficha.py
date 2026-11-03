#!/usr/bin/env python3
"""ficha.json por empresa (Anexo D §D.7): lo necesario para la capa entre empresas y el futuro Damodaran independiente.

Uso: ficha.py CARPETA [--estado ESTADO] [--config config_v2.json]
Lee lo que haya en CARPETA (fase_a/b/c.json, resultados.json, precio.json, referencias_mecanicas.json, gramatica.json,
comprobacion_conjunta.json, entrada_v63.json, datos_v63.json, estado_pipeline.json, datos_ausentes.json, diagnostico.json).
Los campos que no existen en el estado van a null: nunca se inventan.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import config_v2  # noqa: E402
import celdas_v2 as C  # noqa: E402

PAL_CLAVES = {"g15": "crecimiento_1_5", "m_obj": "margen_objetivo", "s2c": "s2c", "g_inf": "g_perpetuo", "roic_lp": "roic_lp"}
CELDA_PAL = {"crecimiento_1_5": "Palancas!{c}14", "margen_objetivo": "Palancas!{c}15", "s2c": "Palancas!{c}16", "g_perpetuo": "Análisis!{c}68", "roic_lp": "Palancas!{c}18"}


def cargar(c, n):
    p = os.path.join(c, n)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if p and os.path.isfile(p) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("--estado")
    ap.add_argument("--config", default=os.path.join(AQUI, "..", "config_v2.json"))
    a = ap.parse_args()
    c = a.carpeta
    cfg = config_v2.cargar(a.config)
    fa, fb, fc = cargar(c, "fase_a.json"), cargar(c, "fase_b.json"), cargar(c, "fase_c.json")
    res, precio, refs, gram = cargar(c, "resultados.json"), cargar(c, "precio.json"), cargar(c, "referencias_mecanicas.json"), cargar(c, "gramatica.json")
    cc, entrada, datos, pipe, da, diag = cargar(c, "comprobacion_conjunta.json"), cargar(c, "entrada_v63.json"), cargar(c, "datos_v63.json"), cargar(c, "estado_pipeline.json"), cargar(c, "datos_ausentes.json"), cargar(c, "diagnostico.json")
    f1 = cargar(c, "fase1_v63.json") or {}  # en los estados tempranos (pendiente_de_datos en los pasos 1-3) es la única fuente del nombre
    estado = a.estado or (pipe or {}).get("estado_analisis") or (fc or {}).get("estado_analisis") or "no_entregable"
    an = (datos or {}).get("analisis") or {}
    her = (datos or {}).get("herencia") or {}
    libros = {n: (os.path.join(c, f) if f else None) for n, f in (("entrada", next((f for f in os.listdir(c) if f.endswith("_v63_datos.xlsx")), "")), ("evaluado", next((f for f in os.listdir(c) if f.endswith("_v63_evaluada.xlsx")), "")))}
    # escenarios
    esc = {}
    for i, e in enumerate(("MALO", "NORMAL", "BUENO")):
        col = "BCD"[i]
        pal = {}
        for k, pk in PAL_CLAVES.items():
            ent = (((fb or {}).get("palancas") or {}).get(pk) or {}).get(e) or {}
            pal[k] = {kk: ent.get(kk) for kk in ("referencia_mecanica", "referencia_no_disponible_motivo", "valor", "desviacion", "clase", "confianza")} if ent else None
        esc[e] = {"historia": ((fa or {}).get("escenarios") or {}).get(e), "frase": ((fa or {}).get("celdas") or {}).get(f"{col}66"),
                  "probabilidad": ((res or {}).get("probabilidades") or [None] * 3)[i], "valor_accion": ((res or {}).get("valores") or {}).get(f"{col}78"), "palancas": pal}
    # cambios vs etapa 1 (34 heredadas)
    cambios = []
    for src in (fa, fb, fc):
        for k, v in ((src or {}).get("herencia") or {}).items():
            cambios.append({"celda": k, "antes": v.get("etapa1"), "despues": ((src or {}).get("celdas") or {}).get(k), "decision": v.get("decision"), "motivo": v.get("motivo"),
                            "evidencia_y_razonamiento": v.get("evidencia_y_razonamiento")})
    # C62 corregida por la fase C al declarar el límite del modelo (única corrección que llega al libro)
    for k, v in ((fc or {}).get("celdas_corregidas") or {}).items():
        if k in ("C62", "Análisis!C62") and v.get("despues") != v.get("antes"):
            for cmb in cambios:
                if cmb["celda"] in ("C62", "Análisis!C62"):
                    cmb.update({"despues": v.get("despues"), "decision": "cambia", "motivo": "razonamiento_corregido", "evidencia_y_razonamiento": f"corregida en la fase C (límite del modelo): {v.get('motivo')}"})
    # recuento de clases
    rec = {"fundamentada": 0, "convencion": 0, "tecnico": 0, "sin_juicio": 0}
    mapa = {"fundamentada": "fundamentada", "convención": "convencion", "técnico": "tecnico", "sin juicio propio": "sin_juicio"}
    for src in (fa, fb, fc):
        for o in ((src or {}).get("observaciones") or {}).values():
            for cl, k in mapa.items():
                if isinstance(o, str) and f"[Clase: {cl}]" in o:
                    rec[k] += 1
    fm = (fc or {}).get("fundamento_material") or {}
    decision = (fc or {}).get("decision")
    cubo_final = (fc or {}).get("cubo_final")
    if estado == "modelo_no_aplicable" and not decision:
        cubo_p = (fc or fa or {}).get("cubo_provisional")
        decision = {"accion": {"No": "descartar", "Demasiado difícil": "demasiado_dificil"}.get(cubo_p), "precio_objetivo": None, "condicion": None}
    if estado == "no_entregable":
        # lo que la fase C hubiera concluido no se entrega: la ficha no lleva cubo ni acción (D17)
        decision, cubo_final = None, None
    elif estado == "modelo_no_aplicable":
        # nunca comprar ni esperar, nunca cubo Sí (§8); el cubo es el cualitativo
        if decision and decision.get("accion") in ("comprar", "esperar"):
            decision = dict(decision, accion=None, precio_objetivo=None, condicion=None)
        if cubo_final == "Sí":
            cubo_final = None
    elif estado in ("pendiente_de_datos", "pendiente_de_investigacion"):
        decision = {"accion": None, "precio_objetivo": None, "condicion": None, "condiciones_revision": (decision or {}).get("condiciones_revision")} if decision else None
        cubo_final = cubo_final if cubo_final in ("Vigilar", "No", "Demasiado difícil") else None
    causa = None
    if estado != "concluido":
        causa = (diag or {}).get("causa") or {"tipo": {"pendiente_de_datos": "falta_de_datos", "pendiente_de_investigacion": "incertidumbre_no_acotada", "modelo_no_aplicable": "limite_del_modelo"}.get(estado, "fallo_de_implementacion"), "detalle": None}
    ficha = {
        "empresa": an.get("B3") or (fa or {}).get("empresa") or f1.get("empresa") or os.path.basename(os.path.abspath(c)), "ticker": an.get("D3") or f1.get("ticker"),
        "fecha": (fa or {}).get("fecha_analisis") or an.get("D4") or f1.get("fecha_analisis") or dt.date.today().isoformat(),
        "moneda": (((datos or {}).get("control_maestro") or {}).get("cabecera") or {}).get("H4_moneda") or f1.get("moneda_modelo"),
        "versiones": {"personaje": cfg.get("version_personaje"), "plantilla": "V6.3", "gramatica": cfg.get("version_gramatica"), "referencias_mecanicas": cfg.get("version_referencias_mecanicas"), "config": cfg.get("version_config")},
        "hashes": {"libro_entrada": sha(libros["entrada"]), "libro_evaluado": sha(libros["evaluado"])},
        "estado_analisis": estado, "causa_si_no_concluido": causa,
        "etapa1": {"cubo": (her.get("celdas") or {}).get("C104"), "cubo_juicio": None, "precio_de_si": None, "fecha": None, "r": (her.get("celdas") or {}).get("C56")},
        "cubo": cubo_final, "cubo_cualitativo_fase_a": (fa or {}).get("cubo_provisional"),
        "decision": decision, "insumos_decision_cartera": (fc or {}).get("insumos_decision_cartera"),
        "motor": (res or {}).get("motor") or (fb or {}).get("motor"),
        "escenarios": esc, "valor_ponderado": ((res or {}).get("valores") or {}).get("C83"), "precio": ((res or {}).get("valores") or {}).get("C37"),
        "escalera": precio, "fundamento_material": fm or None, "comprobacion_conjunta": cc,
        "revision_datos_ausentes": (fc or {}).get("revision_datos_ausentes"),
        "estado_libro": ((res or {}).get("estados") or {}).get("estado_libro_B266"), "estado_evidencias": ((res or {}).get("estados") or {}).get("evidencias_B269"),
        "palanca_mas_influyente": {"nombre": ((res or {}).get("tornado") or {}).get("mas_influyente"), "nota": "información, no criterio (D10)"},
        "semaforos": (res or {}).get("semaforos"), "salto_anio_11": (((res or {}).get("salto_anio_11") or {}).get("filas") or [None] * 5)[4] if res else None,
        "peso_terminal": ((res or {}).get("por_escenario") or {}).get("peso_terminal"),
        "cambios_vs_etapa1": cambios, "n_cambios_vs_etapa1": len(cambios),
        "predicciones": [{"texto": ((fc or {}).get("celdas") or {}).get(f"Palancas!A{i}"), "fecha": ((fc or {}).get("celdas") or {}).get(f"Palancas!B{i}"), "prob": ((fc or {}).get("celdas") or {}).get(f"Palancas!C{i}"), "resultado": None} for i in (38, 39, 40)] if fc else None,
        "incertidumbre_pendiente": ((fc or {}).get("celdas") or {}).get("Diagnóstico V6!B222"), "que_lo_resolveria": ((fc or {}).get("celdas") or {}).get("Diagnóstico V6!B223") or fm.get("que_lo_resolveria"),
        "cambiaria_de_cubo": (fc or {}).get("cambiaria_de_cubo"), "autocomprobacion": (fc or {}).get("autocomprobacion"),
        "recuento_clases": rec, "desviaciones_justificadas": {"n": len(((fb or {}).get("desviaciones_justificadas") or []) + ((fc or {}).get("desviaciones_justificadas") or [])),
                                                             "lista": ((fb or {}).get("desviaciones_justificadas") or []) + ((fc or {}).get("desviaciones_justificadas") or [])},
        "avisos": [x for x in ((gram or {}).get("hallazgos") or []) if x.get("categoria") == "aviso"],
        "confianza_global": (fc or {}).get("confianza_global"),
        "que_falta": {"bloqueantes": (entrada or {}).get("bloqueantes"), "necesarios_para_listo_provisional": (entrada or {}).get("necesarios_para_listo_provisional"), "no_bloqueantes": (entrada or {}).get("no_bloqueantes"), "datos_ausentes": da},
        "citas": {"munger": None, "damodaran": None},
        "dos_errores": (fb or {}).get("dos_errores"), "seis_preguntas": (fa or {}).get("seis_preguntas"), "descalificadores": (fa or {}).get("descalificadores"), "foso": (fa or {}).get("foso"),
        "comparacion_etapa_1": (fc or {}).get("comparacion_etapa_1"),
    }
    # citas: contar referencias (Libro p. n) en los textos
    import re
    textos = json.dumps([fa, fb, fc], ensure_ascii=False)
    ficha["citas"] = {"munger": len(re.findall(r"\((?:PCA|TCI|DR|AIWTK|Poor Charlie's Almanack|Tao of Charlie Munger|Damn Right|All I Want To Know)[^)]*p\.?\s*\d+", textos)),
                      "damodaran": len(re.findall(r"\((?:NN|GV|MR|CV|PA|UD|FS|Numbers and Narrative|Growth and Value|Measuring Returns|Closure in Valuation|Probabilistic Approaches|Ups and Downs|Financial Service Firms)[^)]*p\.?\s*\d+", textos))}
    json.dump(ficha, open(os.path.join(c, "ficha.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print(f"OK: ficha.json · estado {estado} · cubo {ficha['cubo']} · acción {(decision or {}).get('accion')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
