#!/usr/bin/env python3
"""Carga config_v2.json y convierte en absolutas las rutas relativas: una ruta relativa se resuelve respecto a la carpeta
donde está el config (personaje_v2/), así el mismo archivo vale en el repositorio (`../kit_pipeline_munger/munger.md`) y en
cualquier copia. Las rutas absolutas se respetan.

Uso como módulo: `from config_v2 import cargar; cfg = cargar()` (o `cargar(ruta)`).
Uso desde bash: `python3 config_v2.py plantilla.referencia` imprime la ruta resuelta (código 1 si la clave no existe).
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
POR_DEFECTO = os.path.join(AQUI, "..", "config_v2.json")
CLAVES_RUTA = {
    "plantilla": ("archivo", "referencia", "verificador", "scripts_v63", "add_sliders", "patch_base", "ejemplo_empresa_x", "docs"),
    "kit_v1": ("carpeta", "corpus_munger", "scripts"),
    "corpus": ("damodaran",),
    "recalc": ("perfil",),
}


def resolver(valor, base):
    if isinstance(valor, str) and valor and not valor.startswith("<") and not os.path.isabs(valor):
        return os.path.normpath(os.path.join(base, valor))
    return valor


def cargar(ruta=None):
    ruta = os.path.abspath(ruta or POR_DEFECTO)
    cfg = json.load(open(ruta, encoding="utf-8"))
    base = os.path.dirname(ruta)
    for seccion, claves in CLAVES_RUTA.items():
        if isinstance(cfg.get(seccion), dict):
            for k in claves:
                if k in cfg[seccion]:
                    cfg[seccion][k] = resolver(cfg[seccion][k], base)
    if isinstance(cfg.get("resumen_csv"), str):
        cfg["resumen_csv"] = resolver(cfg["resumen_csv"], base)
    cfg["_ruta_config"] = ruta
    return cfg


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    ruta = sys.argv[2] if len(sys.argv) > 2 else None
    cfg = cargar(ruta)
    x = cfg
    for parte in sys.argv[1].split("."):
        if not isinstance(x, dict) or parte not in x:
            print(f"clave no encontrada: {sys.argv[1]}", file=sys.stderr)
            return 1
        x = x[parte]
    print(x if not isinstance(x, (dict, list)) else json.dumps(x, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
