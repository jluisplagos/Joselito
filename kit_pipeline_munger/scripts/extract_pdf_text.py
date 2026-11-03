#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convierte los PDF de una carpeta de empresa a texto con marcas de página [PDF PAGE n].

Usa pdftotext (poppler) y, si falla, pypdf. Escribe <nombre>.txt junto a cada PDF
(o en --outdir) y un índice textos_index.md con número de páginas y palabras.

Uso:
  python3 extract_pdf_text.py --folder empresas/Hermes [--outdir empresas/Hermes/texto]
"""
import argparse, os, subprocess, glob, sys


def pdftotext(pdf, txt):
    try:
        subprocess.run(["pdftotext", "-layout", pdf, txt], check=True, capture_output=True)
        raw = open(txt, encoding="utf-8", errors="replace").read()
        pages = raw.split("\f")
        if pages and not pages[-1].strip(): pages = pages[:-1]
        return pages
    except Exception:
        return None


def pypdf_pages(pdf):
    from pypdf import PdfReader
    rd = PdfReader(pdf)
    return [(p.extract_text() or "") for p in rd.pages]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder", required=True)
    ap.add_argument("--outdir")
    a = ap.parse_args()
    outdir = a.outdir or a.folder
    os.makedirs(outdir, exist_ok=True)
    index = ["| Archivo | Páginas | Palabras |", "|---|---|---|"]
    pdfs = sorted(glob.glob(os.path.join(a.folder, "*.pdf")) + glob.glob(os.path.join(a.folder, "*.PDF")))
    if not pdfs:
        print("No hay PDF en", a.folder); sys.exit(1)
    for pdf in pdfs:
        base = os.path.splitext(os.path.basename(pdf))[0]
        txt = os.path.join(outdir, base + ".txt")
        pages = pdftotext(pdf, txt)
        if pages is None:
            pages = pypdf_pages(pdf)
        with open(txt, "w", encoding="utf-8") as f:
            for i, p in enumerate(pages, 1):
                f.write(f"\n[PDF PAGE {i}]\n{p.strip()}\n")
        words = sum(len(p.split()) for p in pages)
        index.append(f"| {base}.txt | {len(pages)} | {words:,} |")
        print(f"OK {base}: {len(pages)} páginas, {words:,} palabras")
    open(os.path.join(outdir, "textos_index.md"), "w", encoding="utf-8").write("\n".join(index) + "\n")


if __name__ == "__main__":
    main()
