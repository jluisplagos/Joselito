#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Comprueba que las citas a Munger de un texto existen en munger.md con libro y página correctos.

Reconoce citas entre «…», “…” o "…" seguidas de un paréntesis con la referencia, p. ej.
  «…» (PCA p.85–86; HIM)   ·   “…” (Poor Charlie's Almanack, p. 110)   ·   (DR pp.303–304; TCI p.91)
y también referencias sueltas sin cita textual, que solo comprueba por página.

Un fragmento que no aparece literal pero sí con ≥ 85 % de sus palabras en una misma entrada cuenta
como «aproximado» (aviso, no fallo): cubre erratas del .txt, comillas y puntuación.

Uso:
  python3 verify_quotes.py --text respuesta.md --corpus munger.md [--strict]
Sale con 0 si no hay fragmentos ausentes ni páginas erróneas (con --strict también falla si hay
referencias sueltas cuya página no existe en el corpus, o fragmentos solo aproximados).
"""
import argparse, re, sys

BOOKS = {
    "DR": "Damn Right!", "PCA": "Poor Charlie's Almanack", "TCI": "The Complete Investor", "AIWTK": "All I Want to Know",
    "DAMN RIGHT": "Damn Right!", "DAMN RIGHT!": "Damn Right!", "POOR CHARLIE'S ALMANACK": "Poor Charlie's Almanack",
    "THE COMPLETE INVESTOR": "The Complete Investor", "ALL I WANT TO KNOW": "All I Want to Know",
}
BOOK_RE = r"(DR|PCA|TCI|AIWTK|Damn Right!?|Poor Charlie['’]s Almanack|The Complete Investor|All I Want to Know)"
PAGES_RE = r"pp?\.\s*(\d+(?:\s*[–-]\s*\d+)?(?:,\s*\d+(?:\s*[–-]\s*\d+)?)*)"
cit_corpus_re = re.compile(r"(Damn Right!|Poor Charlie['’]s Almanack|The Complete Investor|All I Want to Know)[^()]*?" + PAGES_RE)
cit_text_re = re.compile(BOOK_RE + r",?\s+" + PAGES_RE, re.I)
quote_re = re.compile(r"(?:«([^»]+)»|“([^”]+)”|\"([^\"]{20,}?)\")\s*(\(([^()]*(?:\([^()]*\)[^()]*)*)\))?")
STOP = {"the", "and", "you", "that", "this", "with", "for", "are", "was", "but", "not", "have", "from", "they", "will", "your"}


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[—–-]", " ", s).replace("…", " ")
    s = re.sub(r"\s*%", "%", s)
    s = re.sub(r"percent(age)?", lambda m: "%" + (m.group(1) or ""), s, flags=re.I)
    s = re.sub(r"[\[\]]", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def pages_list(txt):
    out = []
    for part in re.split(r",\s*", txt.strip()):
        r = re.split(r"\s*[–-]\s*", part.strip())
        try:
            a = int(r[0]); b = int(r[1]) if len(r) > 1 and r[1] else a
            out.append((a, b))
        except ValueError:
            pass
    return out


def book_name(tok):
    return BOOKS.get(tok.strip().replace("’", "'").upper())


def parse_text_cites(cit):
    out = []
    for m in cit_text_re.finditer(cit):
        book = book_name(m.group(1))
        if not book: continue
        out += [(book, a, b) for (a, b) in pages_list(m.group(2))]
    return out


def corpus_cites(line):
    out = []
    for m in cit_corpus_re.finditer(line):
        book = m.group(1).replace("’", "'")
        out += [(book, a, b) for (a, b) in pages_list(m.group(2))]
    return out


def words(f):
    return [w for w in re.findall(r"[a-z0-9%']+", f) if len(w) >= 3 and w not in STOP]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()

    corpus_lines = open(a.corpus, encoding="utf-8").read().split("\n")
    corpus_norm = [norm(l) for l in corpus_lines]
    corpus_words = [set(words(l)) for l in corpus_norm]
    pages_in_corpus = set()
    for l in corpus_lines:
        for (b, x, y) in corpus_cites(l):
            for p in range(x, y + 1): pages_in_corpus.add((b, p))

    text = open(a.text, encoding="utf-8").read().replace("*", "").replace("_", "")
    missing, approx, page_bad, loose_bad = [], [], [], []
    n_quotes = n_loose = 0
    quoted_spans = []
    for m in quote_re.finditer(text):
        q = m.group(1) or m.group(2) or m.group(3) or ""
        cit = m.group(5) or ""
        frags = [norm(f) for f in re.split(r"…|\[[^\]]*\]", q)]
        frags = [f for f in frags if len(f.split()) >= 4]
        markers = set(re.findall(r"\b(the|and|you|of|to|is|it|that|we|i|a)\b", " ".join(frags)))
        if not frags or len(markers) < 2:
            continue  # cita en español u otra cosa (opciones de los desplegables, etc.)
        n_quotes += 1
        quoted_spans.append(m.span())
        hits = set()
        for f in frags:
            h = [i for i, cl in enumerate(corpus_norm) if f in cl]
            if not h:
                fw = set(words(f))
                if fw:
                    h = [i for i, cw in enumerate(corpus_words) if len(fw & cw) / len(fw) >= 0.85]
                if h: approx.append((f, q[:70]))
                else: missing.append((f, q[:70]))
            hits.update(h)
        want = parse_text_cites(cit)
        if want and hits:
            have = []
            for i in hits: have += corpus_cites(corpus_lines[i])
            for (book, x, y) in want:
                if not any(hb == book and not (y < hx or x > hy) for (hb, hx, hy) in have):
                    page_bad.append((book, x, y, q[:60]))
    for m in cit_text_re.finditer(text):
        if any(s <= m.start() < e for s, e in quoted_spans):
            continue
        for (book, x, y) in parse_text_cites(m.group(0)):
            n_loose += 1
            if not any((book, p) in pages_in_corpus for p in range(x, y + 1)):
                loose_bad.append((book, x, y))

    print(f"Citas textuales comprobadas: {n_quotes} | referencias sueltas: {n_loose}")
    print(f"\nFRAGMENTOS NO ENCONTRADOS ({len(missing)}):")
    for f, q in missing: print(f"  [{f}]  <- «{q}…»")
    print(f"\nFRAGMENTOS SOLO APROXIMADOS, ≥85 % de palabras en una entrada ({len(approx)}):")
    for f, q in approx: print(f"  [{f}]")
    print(f"\nPÁGINA NO COINCIDE ({len(page_bad)}):")
    for b, x, y, q in page_bad: print(f"  {b} {x}-{y}  <- «{q}…»")
    print(f"\nREFERENCIAS SUELTAS CON PÁGINA INEXISTENTE ({len(loose_bad)}):")
    for b, x, y in loose_bad: print(f"  {b} {x}-{y}")
    bad = len(missing) + len(page_bad) + ((len(loose_bad) + len(approx)) if a.strict else 0)
    print("\nRESULTADO:", "PASS" if bad == 0 else f"FAIL ({bad})")
    sys.exit(0 if bad == 0 else 1)


if __name__ == "__main__":
    main()
