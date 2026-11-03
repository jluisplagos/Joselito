#!/usr/bin/env python3
"""Construye los cuatro entregables V6.3 desde los originales V6.1.

Uso: python3 construir_v63.py carpeta_con_V6.1 carpeta_salida
Necesita en la misma carpeta: patch_v63.py, patch_v62_base.py, add_sliders.py.
"""
import os, re, subprocess, sys, tempfile, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
FECHA_FIJA = (2026, 10, 29, 0, 0, 0)


def normalizar_paquete(path):
    """Construcción determinista: fija las fechas de las entradas del zip y la fecha de
    modificación de docProps/core.xml, que openpyxl pone a la hora actual. Así la reconstrucción
    desde los originales produce exactamente el mismo SHA-256 que el entregable."""
    z = zipfile.ZipFile(path)
    items = [(i, z.read(i.filename)) for i in z.infolist()]
    z.close()
    tmp = path + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        for info, datos in items:
            if info.filename == "docProps/core.xml":
                datos = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                               rb"\g<1>2026-10-29T00:00:00Z\g<2>", datos)
            ni = zipfile.ZipInfo(info.filename, date_time=FECHA_FIJA)
            ni.compress_type = zipfile.ZIP_DEFLATED
            ni.external_attr = info.external_attr
            out.writestr(ni, datos)
    os.replace(tmp, path)
PARES = [("Plantilla_V6.1.xlsx", "Plantilla_V6.3.xlsx"),
         ("Ejemplo_V6.1_EmpresaX.xlsx", "Ejemplo_V6.3_EmpresaX.xlsx"),
         ("Ejemplo_ABB_V6.1.xlsx", "Ejemplo_ABB_V6.3.xlsx"),
         ("Ejemplo_migracion_Hermes_V6.1.xlsx", "Ejemplo_migracion_Hermes_V6.3.xlsx")]
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    for a, b in PARES:
        mid = os.path.join(tmp, b)
        subprocess.run([sys.executable, "-I", os.path.join(HERE, "patch_v63.py"), os.path.join(src, a), mid,
                        "--graficos-de", os.path.join(src, "Plantilla_V6.1.xlsx")],
                       check=True, capture_output=True)
        subprocess.run([sys.executable, "-I", os.path.join(HERE, "add_sliders.py"), mid, os.path.join(out, b)],
                       check=True, capture_output=True)
        normalizar_paquete(os.path.join(out, b))
        print(f"{a} -> {b}")
