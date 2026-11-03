#!/usr/bin/env python3
"""Escribe celdas en un libro V6.3 conservando su integridad (pieza 1, encargo §11).

Uso:
  escribir_v63.py ENTRADA.xlsx SALIDA.xlsx --celdas celdas.json [--lista-blanca juicio|entradas|cualquiera]
                  [--conservar-caches] [--verificar referencia_V6.3.json] [--copia-de-prueba]

celdas.json: {"Análisis!C11": "Sí", "Palancas!B14": 0.04, "Palancas!B38": {"valor": "2027-03-31", "tipo": "fecha"},
              "Palancas!C10": null, "Control maestro!N21": "[Clase: …] …"}
  - Las fechas de Palancas!B38:B40 se convierten a serial de Excel aunque no lleven "tipo": "fecha".
  - null vacía la celda (conserva su estilo).
  - Nunca se escribe una celda con fórmula (error, código 3).
  - Por defecto (`--lista-blanca juicio`) solo admite las 68 celdas de juicio y E/F/N de sus 66 filas de
    Control maestro (celdas_v2.py); `entradas` admite todo el inventario de entradas de la V6.3
    (inventario_entradas.py del paquete V6.3, ruta en config_v2.json); `cualquiera` no comprueba.
  - Salvo `--conservar-caches`, borra el <v> de todas las fórmulas para que el recálculo sea real (§1.4).
  - `--copia-de-prueba` solo documenta que SALIDA es una copia de prueba (D10): no verifica integridad
    salvo que se pida; nunca escribe sobre ENTRADA.
  - `--verificar REF` ejecuta verificar_v63.py sobre SALIDA y devuelve su código (0 = íntegro).
Códigos: 0 ok · 1 verificación fallida · 2 uso · 3 celda con fórmula o fuera de la lista blanca.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from v63_xml import CeldaNoPermitida, FormulaProtegida, LibroV63  # noqa: E402
import celdas_v2  # noqa: E402

FECHAS = {"Palancas!B38", "Palancas!B39", "Palancas!B40"}


def cargar_config():
    import config_v2
    for cand in (os.path.join(AQUI, "..", "config_v2.json"), os.path.join(AQUI, "config_v2.json")):
        if os.path.exists(cand):
            return config_v2.cargar(cand)
    return {}


def lista_blanca(nombre, config):
    if nombre == "juicio":
        return celdas_v2.lista_blanca_juicio()
    if nombre == "entradas":
        ruta = config.get("plantilla", {}).get("scripts_v63")
        if not ruta or not os.path.isdir(ruta):
            raise SystemExit("config_v2.json → plantilla.scripts_v63 no apunta a la carpeta scripts/ del paquete V6.3")
        sys.path.insert(0, ruta)
        import inventario_entradas  # noqa
        return inventario_entradas.conjunto_entradas()
    if nombre == "cualquiera":
        return None
    raise SystemExit(f"lista blanca desconocida: {nombre}")


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada")
    ap.add_argument("salida")
    ap.add_argument("--celdas", required=True, help="JSON {'Hoja!REF': valor}")
    ap.add_argument("--lista-blanca", default="juicio", choices=["juicio", "entradas", "cualquiera"])
    ap.add_argument("--conservar-caches", action="store_true")
    ap.add_argument("--verificar", metavar="REFERENCIA_JSON")
    ap.add_argument("--copia-de-prueba", action="store_true")
    ap.add_argument("--registro", metavar="JSON", help="escribe un registro de lo escrito")
    a = ap.parse_args()
    if os.path.abspath(a.entrada) == os.path.abspath(a.salida):
        print("ERROR: la salida no puede ser la entrada (se escribe siempre en una copia)")
        return 2
    config = cargar_config()
    celdas = json.load(open(a.celdas, encoding="utf-8"))
    for k, v in list(celdas.items()):
        if k in FECHAS and isinstance(v, str):
            celdas[k] = {"valor": v, "tipo": "fecha"}
    permitidas = lista_blanca(a.lista_blanca, config)
    libro = LibroV63(a.entrada)
    try:
        escritas = libro.escribir_celdas(celdas, permitidas)
    except (FormulaProtegida, CeldaNoPermitida) as e:
        print(f"ERROR: {e}")
        return 3
    n_cache = 0 if a.conservar_caches else libro.borrar_caches()
    libro.guardar(a.salida)
    registro = {"entrada": a.entrada, "salida": a.salida, "sha256_entrada": sha256(a.entrada), "sha256_salida": sha256(a.salida),
                "celdas_escritas": escritas, "caches_borradas": n_cache, "copia_de_prueba": a.copia_de_prueba,
                "lista_blanca": a.lista_blanca}
    print(f"OK: {len(escritas)} celdas escritas en {a.salida} ({n_cache} cachés de fórmula borradas)")
    if a.verificar:
        verificador = config.get("plantilla", {}).get("verificador") or os.path.join(os.path.dirname(a.verificar), "..", "scripts", "verificar_v63.py")
        r = subprocess.run([sys.executable, verificador, a.salida, a.verificar], capture_output=True, text=True)
        registro["verificacion"] = {"codigo": r.returncode, "salida": (r.stdout + r.stderr)[-2000:]}
        print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[-300:])
        if a.registro:
            json.dump(registro, open(a.registro, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        return 0 if r.returncode == 0 else 1
    if a.registro:
        json.dump(registro, open(a.registro, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
