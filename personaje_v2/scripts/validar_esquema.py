#!/usr/bin/env python3
"""Valida un JSON del pipeline contra su esquema (Anexo D; esquema/*.esquema.json).

Uso: validar_esquema.py ARCHIVO.json [fase_a|fase_b|fase_c|ficha] [--turno 1|2] [--salida errores.txt]
Sin nombre de esquema, lo deduce del nombre del archivo (fase_a.json → fase_a, …). Con fase_c y --turno, fija `turno` antes de
validar (el turno 2 exige estado, cubo, decisión, celdas y observaciones; el turno 1 los admite a null).
Código 0 válido · 1 inválido (lista de errores, una línea cada uno) · 2 uso o esquema ausente · 3 falta la librería jsonschema.
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ESQUEMAS = os.path.join(AQUI, "..", "esquema")


def validar(datos, nombre):
    try:
        import jsonschema
    except ImportError:
        return None, ["falta la librería jsonschema (pip install jsonschema)"]
    ruta = os.path.join(ESQUEMAS, f"{nombre}.esquema.json")
    if not os.path.exists(ruta):
        return None, [f"esquema ausente: {ruta}"]
    esquema = json.load(open(ruta, encoding="utf-8"))
    v = jsonschema.Draft7Validator(esquema)
    errores = []
    for e in sorted(v.iter_errors(datos), key=lambda x: list(x.absolute_path)):
        camino = "/".join(str(p) for p in e.absolute_path) or "(raíz)"
        errores.append(f"{camino}: {e.message[:300]}")
    return esquema, errores


def main():
    args, turno, salida = [], None, None
    it = iter(sys.argv[1:])
    for a in it:
        if a == "--turno":
            turno = int(next(it))
        elif a == "--salida":
            salida = next(it)
        elif a.startswith("--"):
            print(f"opción desconocida: {a}")
            return 2
        else:
            args.append(a)
    if not args:
        print(__doc__)
        return 2
    archivo = args[0]
    nombre = args[1] if len(args) > 1 else os.path.basename(archivo).split(".")[0]
    if not os.path.exists(archivo):
        print(f"no existe: {archivo}")
        return 2
    try:
        datos = json.load(open(archivo, encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"INVÁLIDO · {archivo} no es JSON: {e}")
        return 1
    if nombre == "fase_c" and turno is not None and isinstance(datos, dict):
        datos = dict(datos, turno=turno)
    esquema, errores = validar(datos, nombre)
    if esquema is None:
        print("ERROR: " + errores[0])
        return 3 if "jsonschema" in errores[0] else 2
    texto = f"{'VÁLIDO' if not errores else 'INVÁLIDO'} · {os.path.basename(archivo)} contra {nombre}.esquema.json" + (f" (turno {turno})" if turno else "") + "\n" + "\n".join(errores)
    print(texto.strip())
    if salida:
        open(salida, "w", encoding="utf-8").write(texto.strip() + "\n")
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
