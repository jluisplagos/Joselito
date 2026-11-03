#!/usr/bin/env python3
"""Pieza 3: convierte los PDF de Damodaran a texto con marcas [PDF PAGE n] (mismo formato que extract_pdf_text.py del kit v1)
y deja un índice con páginas y palabras para la lectura por bloques.

Uso: construir_corpus_damodaran.py --pdf corpus/pdf --out corpus/texto
"""
import argparse
import glob
import os
import subprocess
import sys

CODIGOS = {"narrative&numbers": "NN", "narrative_numbers": "NN", "growthorigins": "GV", "returnmeasures": "MR", "termvalue": "CV", "probabilistic": "PA", "commodity": "UD", "finfirm09": "FS"}
TITULOS = {"NN": "Numbers and Narrative", "GV": "Growth and Value", "MR": "Measuring Returns", "CV": "Closure in Valuation", "PA": "Probabilistic Approaches", "UD": "Ups and Downs", "FS": "Financial Service Firms"}


def paginas(pdf):
    try:
        r = subprocess.run(["pdftotext", "-layout", pdf, "-"], check=True, capture_output=True)
        pages = r.stdout.decode("utf-8", errors="replace").split("\f")
        if pages and not pages[-1].strip():
            pages = pages[:-1]
        if any(p.strip() for p in pages):
            return pages, "pdftotext"
    except Exception:
        pass
    from pypdf import PdfReader
    return [(p.extract_text() or "") for p in PdfReader(pdf).pages], "pypdf"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    pdfs = sorted(glob.glob(os.path.join(a.pdf, "*.pdf")) + glob.glob(os.path.join(a.pdf, "*.PDF")))
    if not pdfs:
        print(f"no hay PDF en {a.pdf}: José Luis tiene que adjuntar los siete documentos (corpus/README.md)")
        return 1
    idx = ["| Código | Título corto | Archivo | Páginas | Palabras | Extractor |", "|---|---|---|---|---|---|"]
    for pdf in pdfs:
        base = os.path.splitext(os.path.basename(pdf))[0]
        cod = next((c for k, c in CODIGOS.items() if k in base.lower()), None)
        pages, how = paginas(pdf)
        txt = os.path.join(a.out, f"{cod or base}.txt")
        with open(txt, "w", encoding="utf-8") as f:
            for i, p in enumerate(pages, 1):
                f.write(f"\n[PDF PAGE {i}]\n{p}\n")
        n_pal = sum(len(p.split()) for p in pages)
        idx.append(f"| {cod or '?'} | {TITULOS.get(cod, '?')} | {os.path.basename(pdf)} | {len(pages)} | {n_pal} | {how} |")
        print(f"{cod or base}: {len(pages)} páginas, {n_pal} palabras ({how}) → {txt}")
    open(os.path.join(a.out, "indice.md"), "w", encoding="utf-8").write("\n".join(idx) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
