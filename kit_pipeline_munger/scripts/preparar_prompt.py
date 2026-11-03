#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepara el prompt de un agente para una empresa: sustituye {EMPRESA}, {CARPETA} y
{LISTA_DE_DOCUMENTOS} y convierte las rutas `kit/...` en absolutas, para que el agente
funcione sea cual sea su directorio de trabajo.

Uso:
  python3 kit/scripts/preparar_prompt.py --tipo extraccion|juicio|verificacion \
      --empresa "Hermès International" --carpeta empresas/Hermes --out prompts_listos/juicio_Hermes.md
La lista de documentos se toma de <carpeta>/texto/*.txt.
"""
import argparse, glob, os, re

ap = argparse.ArgumentParser()
ap.add_argument("--tipo", required=True, choices=["extraccion", "juicio", "verificacion"])
ap.add_argument("--empresa", required=True)
ap.add_argument("--carpeta", required=True)
ap.add_argument("--out", required=True)
a = ap.parse_args()
kit = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
carpeta = os.path.abspath(a.carpeta)
docs = "; ".join(sorted(os.path.basename(p) for p in glob.glob(os.path.join(carpeta, "texto", "*.txt"))))
t = open(os.path.join(kit, "prompts", a.tipo + ".md"), encoding="utf-8").read()
t = t.replace("{EMPRESA}", a.empresa).replace("{CARPETA}", carpeta).replace("{LISTA_DE_DOCUMENTOS}", docs or "(ver texto/)")
t = re.sub(r"(?<![\w/])kit/", kit + "/", t)
os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
open(a.out, "w", encoding="utf-8").write(t)
print("OK:", a.out)
