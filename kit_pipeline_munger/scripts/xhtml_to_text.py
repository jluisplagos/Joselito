#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convierte los informes xhtml (ESEF/SEC) de una carpeta de empresa a texto con marcas [PDF PAGE n].

Quita la cabecera XBRL oculta y toma cada bloque de página del xhtml como una página (en los ESEF
probados, las marcas coinciden con la paginación del informe). Añade las filas a textos_index.md
(ejecutar DESPUÉS de extract_pdf_text.py, que crea el índice).

Uso:
  python3 xhtml_to_text.py --folder empresas/Jumbo --outdir empresas/Jumbo/texto
"""
import argparse, glob, os, warnings
warnings.filterwarnings("ignore")
from bs4 import BeautifulSoup


def pages_of(path):
    soup = BeautifulSoup(open(path, "rb").read(), "lxml")
    for t in soup(["script", "style"]): t.decompose()
    for t in soup.find_all(style=lambda v: v and "display:none" in v.replace(" ", "")): t.decompose()
    body = [k for k in soup.body.children if getattr(k, "name", None)]
    cont = body[0] if len(body) == 1 else soup.body
    pages = [k for k in cont.children if getattr(k, "name", None)]
    return [p.get_text(" ", strip=True) for p in pages]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder", required=True)
    ap.add_argument("--outdir")
    a = ap.parse_args()
    outdir = a.outdir or a.folder
    os.makedirs(outdir, exist_ok=True)
    files = sorted(glob.glob(os.path.join(a.folder, "*.xhtml")) + glob.glob(os.path.join(a.folder, "*.html")))
    if not files:
        print("No hay xhtml en", a.folder); return
    idx = os.path.join(outdir, "textos_index.md")
    if not os.path.exists(idx):
        open(idx, "w", encoding="utf-8").write("| Archivo | Páginas | Palabras |\n|---|---|---|\n")
    for f in files:
        base = os.path.splitext(os.path.basename(f))[0]
        texts = pages_of(f)
        with open(os.path.join(outdir, base + ".txt"), "w", encoding="utf-8") as out:
            for i, t in enumerate(texts, 1):
                out.write(f"\n[PDF PAGE {i}]\n{t}\n")
        words = sum(len(t.split()) for t in texts)
        open(idx, "a", encoding="utf-8").write(f"| {base}.txt | {len(texts)} | {words:,} |\n")
        print(f"OK {base}: {len(texts)} páginas, {words:,} palabras")


if __name__ == "__main__":
    main()
