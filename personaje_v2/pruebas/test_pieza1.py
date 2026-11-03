#!/usr/bin/env python3
"""Pruebas de la pieza 1 (encargo §11): escritura íntegra + recálculo forzado.

Se ejecutan sobre la plantilla y sobre Ejemplo_V6.3_EmpresaX.xlsx (empresa INVENTADA: datos sintéticos).
Uso: python3 pruebas/test_pieza1.py  → deja los archivos en pruebas/salida_pieza1/ y escribe resultado.json
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "scripts"))
from v63_xml import LibroV63, FormulaProtegida  # noqa: E402
import openpyxl  # noqa: E402

sys.path.insert(0, os.path.join(RAIZ, "scripts"))
import config_v2  # noqa: E402
cfg = config_v2.cargar(os.path.join(RAIZ, "config_v2.json"))
PLANTILLA = cfg["plantilla"]["archivo"]
REF = cfg["plantilla"]["referencia"]
VERIF = cfg["plantilla"]["verificador"]
EMPRESA_X = cfg["plantilla"]["ejemplo_empresa_x"]
ADD_CACHED = os.path.join(cfg["kit_v1"]["scripts"], "add_cached_values.py")
OUT = os.path.join(AQUI, "salida_pieza1")
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)
ESCRIBIR = os.path.join(RAIZ, "scripts", "escribir_v63.py")
RECALC = os.path.join(RAIZ, "scripts", "recalc.sh")
PERFIL = cfg.get("recalc", {}).get("perfil", os.path.join(OUT, "lo_perfil"))
resultados = []


def paso(nombre, ok, detalle=""):
    resultados.append({"prueba": nombre, "ok": bool(ok), "detalle": detalle})
    print(("PASA " if ok else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))


def verificar(path):
    r = subprocess.run([sys.executable, VERIF, path, REF], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1:] if (r.stdout + r.stderr).strip() else []


def escribir(entrada, salida, celdas, extra=()):
    cj = salida + ".celdas.json"
    json.dump(celdas, open(cj, "w", encoding="utf-8"), ensure_ascii=False)
    r = subprocess.run([sys.executable, ESCRIBIR, entrada, salida, "--celdas", cj, *extra], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def recalc(path):
    r = subprocess.run(["bash", RECALC, path, os.path.join(OUT, "recalc"), PERFIL], capture_output=True, text=True)
    return r.returncode, os.path.join(OUT, "recalc", os.path.basename(path)), r.stdout + r.stderr


def leer(path, hoja, ref):
    wb = openpyxl.load_workbook(path, data_only=True)
    return wb[hoja][ref].value


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


# ---------- 1. plantilla: una celda de cada tipo ----------
p1 = os.path.join(OUT, "plantilla_1.xlsx")
celdas = {
    "Análisis!C11": "Sí",                       # texto de lista
    "Palancas!B14": 0.04,                        # número
    "Palancas!B38": "2027-03-31",                # fecha (serial, estilo dd/mm/yyyy)
    "Palancas!C10": 5,                           # entero (se vaciará después)
    "Análisis!B101": "Tesis de prueba en una celda combinada B101:D101.",  # combinada
    "Control maestro!E21": "Listo para auditoría",
    "Control maestro!F21": "Estimación declarada",
    "Control maestro!N21": "[Clase: fundamentada] [Confianza: alta] Hereda: nueva en V6.3. Apoyo: prueba. Lo sustituiría: nada.",
}
rc, out = escribir(PLANTILLA, p1, celdas)
paso("1a escribir una celda de cada tipo en la plantilla", rc == 0, out.strip().splitlines()[-1] if out.strip() else "")
code, tail = verificar(p1)
paso("1b verificar_v63.py = 0 tras escribir", code == 0, " ".join(tail))
# vaciar C10 en una segunda escritura (idempotente, misma lista)
p2 = os.path.join(OUT, "plantilla_2.xlsx")
rc, out = escribir(p1, p2, {"Palancas!C10": None})
code, tail = verificar(p2)
paso("1c vaciar Palancas!C10 en una segunda escritura y seguir íntegro", rc == 0 and code == 0, " ".join(tail))
lib = LibroV63(p2)
paso("1d lectura XML: C11, B14, C10 vacía, B38 serial", lib.leer("Análisis", "C11") == "Sí" and lib.leer("Palancas", "B14") == 0.04
     and lib.leer("Palancas", "C10") is None and lib.leer("Palancas", "B38") == 46477,
     f"C11={lib.leer('Análisis','C11')!r} B14={lib.leer('Palancas','B14')!r} C10={lib.leer('Palancas','C10')!r} B38={lib.leer('Palancas','B38')!r}")
# openpyxl ve la fecha como fecha (estilo conservado)
v = leer(p2, "Palancas", "B38")
paso("1e openpyxl lee Palancas!B38 como fecha 2027-03-31", str(v)[:10] == "2027-03-31", str(v))
# recálculo forzado: D11 debe decir ✓ PASA (en la plantilla sin tocar dice «—»)
rc, rec, out = recalc(p2)
d11 = leer(rec, "Análisis", "D11") if rc == 0 else None
paso("1f recálculo forzado: Análisis!D11 = «✓ PASA» con C11 escrita", rc == 0 and d11 == "✓ PASA", f"D11={d11!r}")
# add_cached_values y verificar otra vez
p3 = os.path.join(OUT, "plantilla_3_cache.xlsx")
r = subprocess.run([sys.executable, ADD_CACHED, p2, rec, p3], capture_output=True, text=True)
code, tail = verificar(p3)
paso("1g add_cached_values.py + verificar_v63.py = 0", r.returncode == 0 and code == 0, " ".join(tail))

# ---------- 2. Empresa X (sintética): cambiar Palancas!C14 cambia Análisis!C78 ----------
rc0, rec0, _ = recalc(EMPRESA_X)
c78_0 = leer(rec0, "Análisis", "C78")
c14_0 = leer(rec0, "Palancas", "C14")
px = os.path.join(OUT, "empresaX_c14.xlsx")
rc, out = escribir(EMPRESA_X, px, {"Palancas!C14": round((c14_0 or 0.05) + 0.02, 4)})
code, tail = verificar(px)
rc2, recx, _ = recalc(px)
c78_1 = leer(recx, "Análisis", "C78")
paso("2a Empresa X: escribir Palancas!C14 (+2 pts) deja el libro íntegro", rc == 0 and code == 0, " ".join(tail))
paso("2b Empresa X: Análisis!C78 cambia tras el recálculo forzado", isinstance(c78_0, (int, float)) and isinstance(c78_1, (int, float)) and c78_1 > c78_0,
     f"C14 {c14_0} → {round((c14_0 or 0.05) + 0.02, 4)}; C78 {c78_0} → {c78_1}")
# comprobación extra: sin recálculo forzado (perfil sin OOXMLRecalcMode) la copia mantendría cachés; aquí comprobamos que
# el libro escrito NO lleva cachés en las fórmulas (borradas), que es el primer remedio de §1.4
import zipfile, re
xml_an = zipfile.ZipFile(px).read("xl/worksheets/sheet2.xml").decode("utf-8")
m = re.search(r'<c r="C78"[^>]*>.*?</c>', xml_an, re.S)
paso("2c el libro escrito no conserva <v> en celdas con fórmula (cachés borradas)", m is not None and "<f>" in m.group(0) and "<v>" not in m.group(0), (m.group(0)[:90] if m else "C78 no encontrada"))

# ---------- 3. idempotencia A → B → C sobre el mismo libro ----------
pa = os.path.join(OUT, "sec_A.xlsx"); pb = os.path.join(OUT, "sec_B.xlsx"); pc = os.path.join(OUT, "sec_C.xlsx")
ra, _ = escribir(PLANTILLA, pa, {"Análisis!C62": "Sí", "Palancas!C5": "Madura", "Control maestro!N57": "fase A"})
rb, _ = escribir(pa, pb, {"Palancas!B14": 0.01, "Palancas!C14": 0.03, "Palancas!D14": 0.05, "Análisis!B68": 0.02, "Control maestro!N142": "fase B"})
rcc, _ = escribir(pb, pc, {"Análisis!C104": "Pendiente de decisión de cartera · conclusión del personaje: sin conclusión (prueba)", "Palancas!B39": "2027-06-30", "Diagnóstico V6!B222": "prueba", "Control maestro!N81": "fase C"})
codes = [verificar(p)[0] for p in (pa, pb, pc)]
lib = LibroV63(pc)
paso("3 escrituras sucesivas A→B→C: íntegro en cada paso y los valores anteriores se conservan", ra == rb == rcc == 0 and codes == [0, 0, 0]
     and lib.leer("Análisis", "C62") == "Sí" and lib.leer("Palancas", "C14") == 0.03 and lib.leer("Diagnóstico V6", "B222") == "prueba",
     f"codes={codes}")

# ---------- 4. protecciones ----------
pf = os.path.join(OUT, "formula.xlsx")
rc, out = escribir(PLANTILLA, pf, {"Análisis!A6": "x"})
paso("4a negarse a escribir una celda con fórmula (Análisis!A6)", rc == 3 and not os.path.exists(pf), out.strip().splitlines()[-1] if out.strip() else "")
pf2 = os.path.join(OUT, "formula2.xlsx")
rc, out = escribir(PLANTILLA, pf2, {"Análisis!A6": "x"}, extra=("--lista-blanca", "cualquiera"))
paso("4a' negarse a escribir una celda con fórmula incluso con lista blanca «cualquiera»", rc == 3 and not os.path.exists(pf2), out.strip().splitlines()[-1] if out.strip() else "")
pn = os.path.join(OUT, "nopermitida.xlsx")
rc, out = escribir(PLANTILLA, pn, {"Análisis!C37": 100})
paso("4b negarse a escribir una celda de datos con la lista blanca «juicio» (Análisis!C37)", rc == 3 and not os.path.exists(pn), out.strip().splitlines()[-1] if out.strip() else "")
pe = os.path.join(OUT, "entradas.xlsx")
rc, out = escribir(PLANTILLA, pe, {"Análisis!C37": 100}, extra=("--lista-blanca", "entradas"))
code, _ = verificar(pe)
paso("4c con la lista blanca «entradas» sí escribe Análisis!C37 y sigue íntegro", rc == 0 and code == 0)
pz = os.path.join(OUT, "fija.xlsx")
rc, out = escribir(PLANTILLA, pz, {"Análisis!A1": "x"}, extra=("--lista-blanca", "cualquiera"))
code, tail = verificar(pz)
paso("4d escribir una celda fija (Análisis!A1) con «cualquiera» lo detecta el verificador (≠ 0)", rc == 0 and code != 0, " ".join(tail))

# ---------- 5. copia de prueba: la entrada no cambia ----------
h0 = sha(pb)
pcp = os.path.join(OUT, "copia_prueba.xlsx")
rc, out = escribir(pb, pcp, {"Palancas!D18": 0.14}, extra=("--copia-de-prueba",))
paso("5 --copia-de-prueba no toca el libro de origen", rc == 0 and sha(pb) == h0 and os.path.exists(pcp))

json.dump(resultados, open(os.path.join(OUT, "resultado.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n_ok = sum(r["ok"] for r in resultados)
print(f"\n{n_ok}/{len(resultados)} pruebas PASAN")
sys.exit(0 if n_ok == len(resultados) else 1)
