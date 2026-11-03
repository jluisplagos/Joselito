#!/usr/bin/env python3
"""Salida diagnóstica (D18; Anexo D §D.11): diagnostico.md y diagnostico.json cuando el estado no es «concluido».

Uso: diagnostico.py CARPETA --estado ESTADO --tipo falta_de_datos|incertidumbre_no_acotada|limite_del_modelo|fallo_de_implementacion
                    --detalle "…" --paso N [--comprobacion ID] [--categoria error|límite del modelo|desviación|aviso]
                    [--que-hace-falta "…"] [--desde-paso N] [--quien "Claude Code | José Luis (datos)"]
Lo que sigue válido lo deduce de los archivos presentes en CARPETA (fase_a.json, fase_b.json, fase_c.json, comprobaciones…).
"""
import argparse
import datetime as dt
import glob
import json
import os
import sys


def cargar(carpeta, nombre):
    p = os.path.join(carpeta, nombre)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("--estado", required=True, choices=["pendiente_de_datos", "pendiente_de_investigacion", "modelo_no_aplicable", "no_entregable"])
    ap.add_argument("--tipo", required=True, choices=["falta_de_datos", "incertidumbre_no_acotada", "limite_del_modelo", "fallo_de_implementacion"])
    ap.add_argument("--detalle", required=True)
    ap.add_argument("--paso", type=int, required=True)
    ap.add_argument("--comprobacion")
    ap.add_argument("--categoria")
    ap.add_argument("--que-hace-falta", default="")
    ap.add_argument("--desde-paso", type=int)
    ap.add_argument("--quien", default="Claude Code")
    a = ap.parse_args()
    c = a.carpeta
    fa, fb, fc = cargar(c, "fase_a.json"), cargar(c, "fase_b.json"), cargar(c, "fase_c.json")
    entrada, pipe = cargar(c, "entrada_v63.json"), cargar(c, "estado_pipeline.json")
    valido = {}
    if entrada:
        valido["libro"] = f"íntegro: {entrada.get('integro')} · estado técnico {entrada.get('estado_tecnico')} · motores calculables {[k for k, v in (entrada.get('motores') or {}).items() if v.get('calculable')]}"
    if fa:
        valido["cubo_cualitativo"] = fa.get("cubo_provisional")
        valido["descalificadores"] = [d.get("nombre") for d in (fa.get("descalificadores") or []) if d.get("aplica")] or "ninguno aplica"
        valido["gestion"] = {k: (fa.get("celdas") or {}).get(k) for k in ("C97", "C98")}
        valido["seis_preguntas"] = bool(fa.get("seis_preguntas"))
        valido["celdas_fase_a"] = sorted((fa.get("celdas") or {}).keys())
    if fb:
        valido["palancas_fase_b"] = "escritas" if (pipe or {}).get("fase_b_escrita") else "en fase_b.json, no verificadas"
    if fc:
        valido["fase_c"] = {k: fc.get(k) for k in ("cubo_final", "estado_analisis") if k in fc}
        if fc.get("revision_datos_ausentes"):
            valido["revision_datos_ausentes"] = fc["revision_datos_ausentes"]
        if fc.get("fundamento_material"):
            valido["hipotesis_sin_fundamento"] = [h.get("celda") for h in (fc["fundamento_material"].get("hipotesis_sin_fundamento") or [])]
    no_valido = []
    if a.estado == "no_entregable":
        no_valido = [f"todo lo posterior al paso {a.paso}"]
    elif a.estado in ("pendiente_de_datos", "modelo_no_aplicable") and not fb:
        no_valido = ["palancas (fase B no ejecutada)", "escalera de precios"]
    elif a.estado == "pendiente_de_investigacion":
        no_valido = ["conclusión de compra (sin fundamento suficiente)"]
    intentos = (pipe or {}).get("intentos", {})
    out = {"empresa": (fa or {}).get("empresa") or os.path.basename(os.path.abspath(c)), "fecha": dt.date.today().isoformat(), "estado_analisis": a.estado,
           "causa": {"tipo": a.tipo, "detalle": a.detalle, "comprobacion": a.comprobacion, "categoria": a.categoria},
           "paso_en_que_se_detuvo": a.paso, "intentos": intentos, "lo_que_sigue_valido": valido, "lo_que_no_es_valido": no_valido,
           "para_continuar": {"que_hace_falta": a.que_hace_falta, "desde_que_paso": a.desde_paso if a.desde_paso is not None else a.paso, "quien": a.quien},
           "archivos": sorted(os.path.basename(p) for p in glob.glob(os.path.join(c, "*")) if os.path.isfile(p))}
    json.dump(out, open(os.path.join(c, "diagnostico.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = [f"# Diagnóstico · {out['empresa']} · {out['fecha']}\n", f"- **Estado:** `{a.estado}`", f"- **Causa ({a.tipo}):** {a.detalle}" + (f" · comprobación {a.comprobacion} ({a.categoria})" if a.comprobacion else ""),
          f"- **Paso en que se detuvo:** {a.paso} · intentos: {json.dumps(intentos, ensure_ascii=False)}",
          "- **Lo que sigue válido:** " + "; ".join(f"{k}: {json.dumps(v, ensure_ascii=False)[:160]}" for k, v in valido.items()),
          "- **Lo que no es válido:** " + ("; ".join(no_valido) if no_valido else "nada en particular"),
          f"- **Para continuar:** {a.que_hace_falta or '(ver causa)'} · desde el paso {out['para_continuar']['desde_que_paso']} · quién: {a.quien}",
          f"- Archivos: {', '.join(out['archivos'])}"]
    open(os.path.join(c, "diagnostico.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"diagnóstico escrito: {a.estado} · {a.tipo} · paso {a.paso}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
