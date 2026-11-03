#!/usr/bin/env python3
"""Convierte los PDF de una empresa a texto con marcas [PDF PAGE n] (formato que leen todos los agentes y verificadores).

Uso: pdf_a_texto.py empresas_v2/<E>   (lee <E>/pdf/*.pdf y escribe <E>/texto/<nombre>.txt)
Pon en el nombre de cada PDF el ejercicio que cubre (p. ej. AR_2024.pdf, CF_2024.pdf): fase1_historia.py elige un informe por
año por el número del nombre y por la presencia de estados financieros. pdftotext -layout; si no da texto, pypdf.
Código 0 ok · 1 algún PDF sin texto (escaneado: hace falta OCR) · 2 uso.
"""
import glob
import os
import subprocess
import sys


def paginas(pdf):
    try:
        r = subprocess.run(["pdftotext", "-layout", pdf, "-"], check=True, capture_output=True)
        p = r.stdout.decode("utf-8", errors="replace").split("\f")
        if p and not p[-1].strip():
            p = p[:-1]
        if any(x.strip() for x in p):
            return p
    except Exception:
        pass
    from pypdf import PdfReader
    return [(x.extract_text() or "") for x in PdfReader(pdf).pages]


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    c = sys.argv[1]
    pdfs = sorted(glob.glob(os.path.join(c, "pdf", "*.pdf")) + glob.glob(os.path.join(c, "pdf", "*.PDF")))
    if not pdfs:
        print(f"no hay PDF en {c}/pdf")
        return 2
    os.makedirs(os.path.join(c, "texto"), exist_ok=True)
    malos = 0
    for pdf in pdfs:
        p = paginas(pdf)
        n = sum(len(x.split()) for x in p)
        dest = os.path.join(c, "texto", os.path.splitext(os.path.basename(pdf))[0] + ".txt")
        with open(dest, "w", encoding="utf-8") as f:
            for i, x in enumerate(p, 1):
                f.write(f"[PDF PAGE {i}]\n{x}\n")
        aviso = "  ← SIN TEXTO (¿escaneado?)" if n < 50 * max(1, len(p)) // 10 else ""
        malos += bool(aviso)
        print(f"{os.path.basename(pdf)}: {len(p)} páginas, {n} palabras → {dest}{aviso}")
    return 1 if malos else 0


if __name__ == "__main__":
    sys.exit(main())
