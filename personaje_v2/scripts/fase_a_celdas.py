#!/usr/bin/env python3
"""Convierte la salida de una fase (fase_a.json / fase_b.json / fase_c.json) en el JSON de celdas que escribe escribir_v63.py:
las celdas de la fase + E/F/N de sus filas de Control maestro (D9: siempre «Estimación declarada»).

Uso: fase_a_celdas.py fase_X.json A|B|C celdas_salida.json
Código 0 ok · 1 faltan celdas u observaciones de la fase · 2 uso.
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import celdas_v2 as C  # noqa: E402


def normalizar(clave):
    return clave if "!" in clave else f"Análisis!{clave}"


def convertir(fase_json, fase):
    celdas_fase = C.celdas_de_fase(fase)
    celdas = {normalizar(k): v for k, v in (fase_json.get("celdas") or {}).items()}
    obs = {normalizar(k): v for k, v in (fase_json.get("observaciones") or {}).items()}
    salida, faltan = {}, []
    for clave in sorted(celdas_fase):
        hoja, ref = clave.split("!")
        meta = C.CELDAS[hoja][ref]
        if clave not in celdas:
            # condicionales pueden faltar: se escriben vacías; las demás son error
            if meta.get("condicional"):
                salida[clave] = None
            else:
                faltan.append(clave)
                continue
        else:
            salida[clave] = celdas[clave]
        r = meta.get("cm")
        if r:
            salida[f"Control maestro!E{r}"] = C.E_LISTO
            salida[f"Control maestro!F{r}"] = C.F_ESTIMACION
            o = obs.get(clave)
            if not o:
                faltan.append(f"observación de {clave}")
            else:
                salida[f"Control maestro!N{r}"] = str(o)[:900]
    extra = [k for k in celdas if k not in celdas_fase]
    return salida, faltan, extra


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    fj = json.load(open(sys.argv[1], encoding="utf-8"))
    salida, faltan, extra = convertir(fj, sys.argv[2])
    json.dump(salida, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if extra:
        print(f"AVISO: la fase {sys.argv[2]} trae celdas que no son suyas y se ignoran: {extra}")
    if faltan:
        print(f"FALTAN ({len(faltan)}): {faltan}")
        return 1
    print(f"OK: {len(salida)} celdas (incluidas E/F/N de Control maestro) → {sys.argv[3]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
