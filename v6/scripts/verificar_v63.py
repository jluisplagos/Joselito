#!/usr/bin/env python3
"""Verifica un libro V6.3 contra la REFERENCIA APROBADA (generar_referencia.py).

Uso: python3 verificar_v63.py archivo.xlsx referencia_V6.3.json [--json salida.json]
Código de salida: 0 = íntegro · 1 = diferencias no autorizadas (se nombran) · 2 = error de uso.

Qué detecta (FALLO):
  - una fórmula distinta de la aprobada, sustituida por un valor, o eliminada
  - una fórmula nueva fuera del inventario de entradas
  - una etiqueta, tabla o lista fija alterada
  - validaciones de datos, formato condicional o nombres definidos distintos (por contenido)
  - controles de formulario, dibujos o gráficos distintos (por contenido, no por recuento)
  - hojas añadidas, quitadas, renombradas o reordenadas
Qué NO es fallo (se informa como AVISO):
  - un valor en una celda de entrada (eso es usar la hoja)
  - una fórmula escrita en una celda de entrada
  - un parámetro de diseño editable con otro valor (Diagnóstico C91:C94, C158, C179; Historia C57)
  - texto nuevo en una celda libre que no es fórmula

Qué NO puede detectar: una manipulación de este verificador o de la referencia. Por eso la
referencia se entrega con el SHA-256 del archivo del que salió y se guarda aparte del libro.
"""
import hashlib
import json
import sys
import zipfile

from openpyxl import load_workbook

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from inventario_entradas import PARAMETROS, conjunto_entradas  # noqa: E402
from generar_referencia import capturar  # noqa: E402


def comparar(path, ref):
    obs = capturar(path)
    fallos, avisos = [], []
    if obs["hojas"] != ref["hojas"]:
        fallos.append(f"hojas: {obs['hojas']} ≠ {ref['hojas']}")
    entradas = conjunto_entradas()

    # fórmulas aprobadas
    for k, f in ref["formulas"].items():
        g = obs["formulas"].get(k)
        if g == f:
            continue
        hoja, coord = k.split("!")
        if g is None:
            fijo = obs["fijos"].get(k)
            if fijo is not None:
                fallos.append(f"{k}: fórmula sustituida por el valor {fijo!r}")
            else:
                # puede ser una entrada ocupada por el usuario (p. ej. Control maestro) o celda vacía
                if coord in entradas.get(hoja, set()):
                    avisos.append(f"{k}: celda de entrada que en la referencia tenía fórmula")
                else:
                    fallos.append(f"{k}: fórmula eliminada")
        else:
            fallos.append(f"{k}: fórmula alterada → {g[:80]}")
    # fórmulas no previstas
    for k, g in obs["formulas"].items():
        if k in ref["formulas"]:
            continue
        hoja, coord = k.split("!")
        if coord in entradas.get(hoja, set()):
            avisos.append(f"{k}: fórmula en una celda de entrada ({g[:60]})")
        else:
            fallos.append(f"{k}: fórmula no prevista ({g[:60]})")
    # celdas fijas
    for k, v in ref["fijos"].items():
        g = obs["fijos"].get(k, obs["formulas"].get(k))
        if g == v:
            continue
        if k in PARAMETROS:
            avisos.append(f"{k}: parámetro editable {v!r} → {g!r}")
        elif isinstance(g, str) and g.startswith("="):
            fallos.append(f"{k}: celda fija sustituida por fórmula")
        else:
            fallos.append(f"{k}: celda fija alterada {str(v)[:40]!r} → {str(g)[:40]!r}")
    for k, g in obs["fijos"].items():
        if k not in ref["fijos"]:
            avisos.append(f"{k}: contenido nuevo fuera de las entradas ({str(g)[:40]!r})")

    for hoja in ref["validaciones"]:
        if obs["validaciones"].get(hoja) != ref["validaciones"][hoja]:
            a, b = ref["validaciones"][hoja], obs["validaciones"].get(hoja, [])
            dif = [x for x in a if x not in b] + [x for x in b if x not in a]
            fallos.append(f"validaciones de datos distintas en {hoja}: {dif[:3]}")
    for hoja in ref["formato_condicional"]:
        if obs["formato_condicional"].get(hoja) != ref["formato_condicional"][hoja]:
            fallos.append(f"formato condicional distinto en {hoja}")
    for k, val in ref.get("parametros", {}).items():
        if obs.get("parametros", {}).get(k) != val:
            avisos.append(f"{k}: parámetro editable {val!r} → {obs.get('parametros', {}).get(k)!r}")
    if obs["nombres_definidos"] != ref["nombres_definidos"]:
        fallos.append("nombres definidos distintos")
    for parte, h in ref["partes_paquete"].items():
        if obs["partes_paquete"].get(parte) != h:
            fallos.append(f"parte del paquete alterada o ausente: {parte}")
    for parte in obs["partes_paquete"]:
        if parte not in ref["partes_paquete"]:
            fallos.append(f"parte del paquete no prevista: {parte}")
    return fallos, avisos


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    path, refp = sys.argv[1], sys.argv[2]
    ref = json.load(open(refp))
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    fallos, avisos = comparar(path, ref)
    res = {"archivo": path.split("/")[-1], "sha256": sha, "referencia": ref.get("version"),
           "sha256_origen_referencia": ref.get("sha256_origen"),
           "veredicto": "ÍNTEGRO" if not fallos else "ALTERADO", "fallos": fallos, "avisos": avisos}
    if "--json" in sys.argv:
        json.dump(res, open(sys.argv[sys.argv.index("--json") + 1], "w"), ensure_ascii=False, indent=1)
    print(f"{res['archivo']} · SHA-256 {sha[:16]}… · referencia {res['referencia']} "
          f"(origen {str(res['sha256_origen_referencia'])[:16]}…)")
    print(f"VEREDICTO: {res['veredicto']} · {len(fallos)} fallos · {len(avisos)} avisos")
    for f in fallos[:40]:
        print("  FALLO ", f)
    if len(fallos) > 40:
        print(f"  … y {len(fallos) - 40} más")
    for a in avisos[:12]:
        print("  aviso ", a)
    if len(avisos) > 12:
        print(f"  … y {len(avisos) - 12} avisos más")
    return 0 if not fallos else 1


if __name__ == "__main__":
    sys.exit(main())
