#!/usr/bin/env python3
"""Comprueba las celdas escritas por el personaje v2 en el libro evaluado (Anexo A §A.5; criterio 3 de §10.2).

Uso: comprobar_celdas_v2.py <E>_v63_evaluada.xlsx <E>_v63_datos.xlsx [--fases A,B,C] [--motor A|B|C] [--salida comprobacion_celdas.json]
Lee los dos libros en el XML (sin recalcular). --fases dice qué fases se han escrito ya (por defecto A,B,C).
Código 0 ok · 1 errores (cualquier incumplimiento es un error D17: se corrige o no_entregable) · 2 uso.
"""
import argparse
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import celdas_v2 as C  # noqa: E402
from v63_xml import LibroV63  # noqa: E402

LISTA_G = [0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03]
LISTA_P = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6]


def num(x):
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("evaluado")
    ap.add_argument("entrada")
    ap.add_argument("--fases", default="A,B,C")
    ap.add_argument("--motor")
    ap.add_argument("--salida")
    a = ap.parse_args()
    fases = set(a.fases.split(","))
    ev, en = LibroV63(a.evaluado), LibroV63(a.entrada)
    err, ok = [], []
    g = lambda h, r: ev.leer(h, r)  # noqa: E731
    motor = a.motor or {"Sí": "A", "No · financiación cambia mucho": "B", "No · banco o aseguradora": "C"}.get(g("Análisis", "C62"))
    tasa = num(g("Análisis", "C56"))
    # 1. vocabulario y tipos de las celdas de las fases escritas
    for hoja, d in C.CELDAS.items():
        for ref, meta in d.items():
            if meta["fase"] not in fases:
                continue
            v = g(hoja, ref)
            clave = f"{hoja}!{ref}"
            cond = meta.get("condicional")
            if cond:
                # condicionales: vacías solo cuando su regla lo manda
                if ref == "C10" and g("Palancas", "C9") == "No":
                    (ok if v in (None, "") else err).append(f"{clave}: debe quedar vacía con C9 = No (tiene {v!r})")
                    continue
                if ref in ("B16", "C16", "D16") and motor == "C":
                    (ok if v in (None, "") else err).append(f"{clave}: vacía en motor C (tiene {v!r})")
                    continue
                if ref == "C76" and motor in ("B", "C"):
                    (ok if v in (None, "") else err).append(f"{clave}: vacía en motores B y C (tiene {v!r})")
                    continue
                if ref == "C23" and num(g("Palancas", "C22")) in (None, 0):
                    continue
                if ref in ("C22", "C24", "C44") and v in (None, ""):
                    if ref == "C44" and g("Palancas", "C43") in ("Transitorio", "Extraordinario"):
                        err.append(f"{clave}: obligatoria con C43 = {g('Palancas', 'C43')}")
                    continue
            if v in (None, ""):
                err.append(f"{clave}: vacía")
                continue
            if "lista" in meta and v not in meta["lista"]:
                err.append(f"{clave}: {v!r} no está en el vocabulario {meta['lista']}")
            elif "lista_num" in meta and (num(v) is None or not any(abs(v - x) < 1e-9 for x in meta["lista_num"])):
                err.append(f"{clave}: {v!r} no está en la lista {meta['lista_num']}")
            elif meta.get("tipo") == "decimal" and num(v) is None:
                err.append(f"{clave}: {v!r} no es numérico")
            elif meta.get("tipo") == "entero" and (num(v) is None or int(v) != v or v < 1):
                err.append(f"{clave}: {v!r} no es un entero ≥ 1")
            elif meta.get("tipo") == "fecha" and (num(v) is None or v < 40000):
                err.append(f"{clave}: {v!r} no es una fecha (serial de Excel)")
            elif meta.get("tipo") == "texto" and not isinstance(v, str):
                err.append(f"{clave}: {v!r} no es texto")
            else:
                ok.append(clave)
    # 2. reglas numéricas (si está la fase B)
    if "B" in fases:
        ps = [num(g("Análisis", r)) for r in ("B69", "C69", "D69")]
        if None in ps or abs(sum(ps) - 1) > 1e-6:
            err.append(f"probabilidades {ps} no suman 1")
        for r in ("B68", "C68", "D68"):
            gg = num(g("Análisis", r))
            if gg is not None and tasa is not None and gg >= tasa:
                err.append(f"Análisis!{r} = {gg} ≥ tasa de descuento {tasa}")
        for col in "BCD":
            r_lp, gg = num(g("Palancas", f"{col}18")), num(g("Análisis", f"{col}68"))
            if r_lp is not None and gg is not None and r_lp <= gg:
                err.append(f"Palancas!{col}18 = {r_lp} ≤ g {gg}")
            s2c = num(g("Palancas", f"{col}16"))
            if motor in ("A", "B") and s2c is not None and s2c <= 0:
                err.append(f"Palancas!{col}16 = {s2c} ≤ 0")
        c76, c53 = num(g("Análisis", "C76")), num(g("Análisis", "C53"))
        if motor == "A" and c76 is not None and c53 is not None and c76 > c53:
            err.append(f"C76 = {c76} > caja C53 = {c53}")
        c22, c23 = num(g("Palancas", "C22")), num(g("Palancas", "C23"))
        if c22 is not None and not 0 <= c22 <= 1:
            err.append(f"Palancas!C22 = {c22} fuera de [0, 1]")
        if c22 and (c23 is None or c23 < 0):
            err.append(f"Palancas!C23 = {c23!r} con C22 > 0")
    if "C" in fases:
        for i in (38, 39, 40):
            if not g("Palancas", f"A{i}") or num(g("Palancas", f"B{i}")) is None or num(g("Palancas", f"C{i}")) is None:
                err.append(f"predicción {i - 37} incompleta (A{i}, B{i}, C{i})")
            elif not 0 <= g("Palancas", f"C{i}") <= 1:
                err.append(f"Palancas!C{i} fuera de [0, 1]")
        c104 = g("Análisis", "C104")
        if isinstance(c104, str):
            if not c104.startswith(C.C104_PREFIJO):
                err.append(f"C104 no empieza por «{C.C104_PREFIJO}»: {c104[:60]!r}")
            if "%" in c104 or re.search(r"\d+\s*(por ciento|pct)", c104, re.I):
                err.append(f"C104 contiene un porcentaje (D16): {c104[:80]!r}")
    if "A" in fases:
        for r in ("B66", "C66", "D66"):
            if not g("Análisis", r):
                err.append(f"Análisis!{r} vacía")
    # 3. filas de Control maestro de las celdas escritas
    for hoja, d in C.CELDAS.items():
        for ref, meta in d.items():
            if meta["fase"] not in fases or not meta.get("cm"):
                continue
            r = meta["cm"]
            E, F, N = g("Control maestro", f"E{r}"), g("Control maestro", f"F{r}"), g("Control maestro", f"N{r}")
            if E != C.E_LISTO:
                err.append(f"Control maestro!E{r} ({hoja}!{ref}) = {E!r} ≠ «{C.E_LISTO}»")
            if F != C.F_ESTIMACION:
                err.append(f"Control maestro!F{r} ({hoja}!{ref}) = {F!r} ≠ «{C.F_ESTIMACION}»")
            if not isinstance(N, str) or not N.strip():
                err.append(f"Control maestro!N{r} ({hoja}!{ref}) sin Observación")
            else:
                if not re.search(r"\[Clase: (fundamentada|convención|técnico|sin juicio propio)\]", N):
                    err.append(f"Control maestro!N{r}: falta [Clase: …] válida")
                if not re.search(r"\[Confianza: (alta|media|baja)\]", N):
                    err.append(f"Control maestro!N{r}: falta [Confianza: …]")
                if "Hereda:" not in N:
                    err.append(f"Control maestro!N{r}: falta la línea «Hereda:»")
                if len(N) > 900:
                    err.append(f"Control maestro!N{r}: {len(N)} caracteres (> 900)")
    # 4. ninguna celda fuera de las permitidas cambiada respecto al libro de entrada
    permitidas = C.lista_blanca_juicio()
    cambios = []
    for hoja in ev.hojas():
        A, B = ev.todas_las_celdas(hoja), en.todas_las_celdas(hoja)
        for ref in set(A) | set(B):
            if A.get(ref) != B.get(ref) and ref not in permitidas.get(hoja, set()):
                va, vb = A.get(ref), B.get(ref)
                if isinstance(va, tuple) or isinstance(vb, tuple):
                    cambios.append(f"{hoja}!{ref}: fórmula cambiada")
                else:
                    cambios.append(f"{hoja}!{ref}: {vb!r} → {va!r}")
    if cambios:
        err.extend(["celda fuera de las 68/66 cambiada: " + x for x in cambios[:30]])
    res = {"evaluado": a.evaluado, "entrada": a.entrada, "fases": sorted(fases), "motor": motor, "errores": err, "n_ok": len(ok)}
    if a.salida:
        json.dump(res, open(a.salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(("PASS" if not err else "FALLA") + f": {len(err)} errores · {len(ok)} celdas correctas · fases {sorted(fases)} · motor {motor}")
    for e in err[:40]:
        print("  -", e)
    return 0 if not err else 1


if __name__ == "__main__":
    sys.exit(main())
