#!/usr/bin/env python3
"""Añade (o sustituye) la fila de una empresa en resumen_v2.csv (Anexo D §D.10).

Uso: resumen.py CARPETA resumen_v2.csv
"""
import csv
import json
import os
import sys

COLS = ["empresa", "fecha", "estado_analisis", "causa_si_no_concluido", "cubo_v1", "cubo_v2", "motor", "precio", "moneda", "precio_escenario_malo", "precio_si",
        "ponderado", "zona", "accion", "fundamento_material", "estado_libro", "palanca_mas_influyente", "n_desviaciones", "n_sin_juicio", "n_tecnico",
        "n_hipotesis_sin_fundamento", "comprobacion_conjunta", "n_datos_ausentes", "n_datos_ausentes_materiales", "intentos_B", "intentos_C", "verificacion",
        "coste_estimado", "tiempo_min"]


def main():
    c, csv_path = sys.argv[1], sys.argv[2]
    F = json.load(open(os.path.join(c, "ficha.json"), encoding="utf-8"))
    pipe = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "estado_pipeline.json")) else {}
    esc = F.get("escalera") or {}
    fm = F.get("fundamento_material") or {}
    rda = F.get("revision_datos_ausentes") or {}
    fila = {"empresa": F.get("empresa"), "fecha": F.get("fecha"), "estado_analisis": F.get("estado_analisis"),
            "causa_si_no_concluido": (F.get("causa_si_no_concluido") or {}).get("tipo"), "cubo_v1": (F.get("comparacion_etapa_1") or {}).get("cubo_v1"),
            "cubo_v2": F.get("cubo"), "motor": F.get("motor"), "precio": F.get("precio"), "moneda": F.get("moneda"),
            "precio_escenario_malo": esc.get("precio_escenario_malo"), "precio_si": esc.get("precio_si"), "ponderado": esc.get("ponderado"), "zona": esc.get("zona"),
            "accion": (F.get("decision") or {}).get("accion"), "fundamento_material": fm.get("resultado"), "estado_libro": F.get("estado_libro"),
            "palanca_mas_influyente": (F.get("palanca_mas_influyente") or {}).get("nombre"), "n_desviaciones": (F.get("desviaciones_justificadas") or {}).get("n"),
            "n_sin_juicio": (F.get("recuento_clases") or {}).get("sin_juicio"), "n_tecnico": (F.get("recuento_clases") or {}).get("tecnico"),
            "n_hipotesis_sin_fundamento": len(fm.get("hipotesis_sin_fundamento") or []) if fm else None,
            "comprobacion_conjunta": (F.get("comprobacion_conjunta") or {}).get("sobrevive") if F.get("comprobacion_conjunta") else None,
            "n_datos_ausentes": len(rda.get("revisados") or []) if rda else len(((F.get("que_falta") or {}).get("datos_ausentes") or [])),
            "n_datos_ausentes_materiales": sum(1 for x in (rda.get("revisados") or []) if x.get("material_para_conclusion_favorable")) if rda else None,
            "intentos_B": (pipe.get("intentos") or {}).get("fase_b"), "intentos_C": (pipe.get("intentos") or {}).get("fase_c"), "verificacion": pipe.get("auditoria"),
            "coste_estimado": pipe.get("coste_estimado"), "tiempo_min": pipe.get("tiempo_min")}
    filas = []
    if os.path.exists(csv_path):
        with open(csv_path, encoding="utf-8", newline="") as fh:
            filas = [r for r in csv.DictReader(fh) if r.get("empresa") != fila["empresa"]]
    filas.append({k: ("" if v is None else v) for k, v in fila.items()})
    with open(csv_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS)
        w.writeheader()
        for r in filas:
            w.writerow({k: r.get(k, "") for k in COLS})
    print(f"OK: fila de {fila['empresa']} en {csv_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
