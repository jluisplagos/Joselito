#!/usr/bin/env python3
"""Relación INDEPENDIENTE de las entradas editables que alimentan la valoración y la lectura del
precio de cada motor. No lee el inventario de evidencias de Control maestro: lo que hace es

  1. una traza estática del grafo de fórmulas desde las salidas hasta las celdas editables, y
  2. una activación empírica: para cada celda candidata, por motor y por configuración (quiebra
     activa, FCF base ≤ 0 con FCF normalizado, exceso de caja, ADR, desviación de capitalización),
     se cambia su valor, se recalcula con LibreOffice y se mira si alguna salida cambia.

Salidas vigiladas: Análisis B78:D78, C83, C84, C85, C86 · Motor B252, B253, B254, B267 ·
Diagnóstico V6 C156.

Uso: python3 trazar_entradas_materiales.py Ejemplo_V6.3_EmpresaX.xlsx carpeta_trabajo salida.json
Dependencias: openpyxl, soffice. Tarda unos minutos (≈ 350 recálculos).
"""
import collections
import json
import os
import re
import shutil
import subprocess
import sys

from openpyxl import load_workbook
from openpyxl.utils import get_column_letter as L
from openpyxl.utils import range_boundaries

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from inventario_entradas import ENTRADAS  # noqa: E402

AN, HI, PA, DI, MO, PN, CM = ("Análisis", "Historia", "Palancas", "Diagnóstico V6", "Motor", "Panel", "Control maestro")
SALIDAS = [(AN, "B78"), (AN, "C78"), (AN, "D78"), (AN, "C83"), (AN, "C84"), (AN, "C85"), (AN, "C86"),
           (MO, "B252"), (MO, "B253"), (MO, "B254"), (MO, "B267"), (DI, "C156")]
MOT = {"A": "Sí", "B": "No · financiación cambia mucho", "C": "No · banco o aseguradora"}

# Celdas editables que por diseño NO se consideran entradas de la valoración (se comprueban igual;
# si alguna resultara activa, la relación lo diría y habría que revisar la exclusión).
EXCLUIDAS_POR_DISENO = {
    PN: "interruptores de visualización y modo estudio (no tocan la hipótesis base: R05)",
    DI: "parámetros de diseño (umbrales, k del precio de referencia) y líneas de juicio libres",
}
NO_PERTURBAR = {(CM, c) for c in ("H4",)}  # H4 se trata en la configuración de monedas, no suelta


def celdas(rango):
    c0, r0, c1, r1 = range_boundaries(rango)
    return [f"{L(c)}{r}" for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)]


# ------------------------------------------------------------------ 1 · traza estática
def traza_estatica(path):
    wb = load_workbook(path)
    F = {}
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("="):
                    F[(ws.title, c.coordinate)] = c.value
    hojas = {h.lower(): h for h in wb.sheetnames}
    pat = re.compile(r"(?:((?:'[^']+')|(?:[A-Za-zÁÉÍÓÚÑáéíóúñ][\wÁÉÍÓÚÑáéíóúñ .]*))!)?(\$?[A-Z]{1,3}\$?\d+(?::\$?[A-Z]{1,3}\$?\d+)?)")

    def refs(formula, hoja):
        out = set()
        f = re.sub(r'"[^"]*"', '""', formula)
        for m in pat.finditer(f):
            sh, rng = m.group(1), m.group(2).replace("$", "")
            if sh:
                sh = sh.strip("'")
                if sh.lower() not in hojas:
                    continue
                sh = hojas[sh.lower()]
            else:
                sh = hoja
            try:
                c0, r0, c1, r1 = range_boundaries(rng)
            except Exception:
                continue
            if None in (c0, r0, c1, r1) or (c1 - c0 + 1) * (r1 - r0 + 1) > 4000:
                continue
            for rr in range(r0, r1 + 1):
                for cc in range(c0, c1 + 1):
                    out.add((sh, f"{L(cc)}{rr}"))
        return out

    visto, pila = set(), list(SALIDAS)
    while pila:
        k = pila.pop()
        if k in visto:
            continue
        visto.add(k)
        f = F.get(k)
        if f:
            for r in refs(f, k[0]):
                if r not in visto:
                    pila.append(r)
    editables = {h: set(sum((celdas(r) for r in rangos), [])) for h, rangos in ENTRADAS.items()}
    alcanzadas = sorted(f"{h}!{c}" for h, c in visto if c in editables.get(h, set()))
    return alcanzadas


# ------------------------------------------------------------------ 2 · activación empírica
def leer_salidas(path):
    wb = load_workbook(path, data_only=True)
    out = {}
    for h, c in SALIDAS:
        v = wb[h][c].value
        out[f"{h}!{c}"] = round(v, 9) if isinstance(v, float) else v
    return out


def perturbar(v, hoja, coord, listas):
    """Devuelve un valor distinto y válido para la celda; None si no se puede perturbar."""
    key = f"{hoja}!{coord}"
    if key in listas:
        ops = listas[key]
        return next((o for o in ops if o != v), None)
    if isinstance(v, bool):
        return not v
    if isinstance(v, (int, float)):
        return v * 1.07 + (0.013 if abs(v) < 1 else 1.0) if v != 0 else 1.0
    if v is None:
        return None
    if isinstance(v, str):
        return v + " (perturbado)"
    return None


LISTAS = {
    f"{AN}!C51": ["Sí", "No"],
    f"{AN}!C62": list(MOT.values()),
    f"{PA}!C5": ["Madura en crecimiento", "Madura", "En crecimiento"],
    f"{PA}!C6": ["Ninguno", "Regulada (red, concesión)", "Financiera (banco o aseguradora)"],
    f"{PA}!C7": ["Machinery", "Software (System & Application)", "Retail (General)"],
    f"{PA}!C8": ["Último año", "Media del ciclo"],
    f"{PA}!C9": ["No", "Sí"],
    f"{PA}!C43": ["Transitorio", "Extraordinario", "Estructural", "No aplica"],
    f"{PA}!C47": ["Ninguna", "ADR o ADS", "Básicas frente a diluidas"],
    f"{PA}!C48": ["EUR", "USD"],
    f"{CM}!L4": ["IFRS", "US GAAP"],
    f"{CM}!J4": ["mm", "miles"],
}
# valores con los que se «rellena» una celda vacía para ver si una entrada opcional es material
RELLENO = {
    f"{AN}!C76": 50, f"{AN}!C38": 30, f"{AN}!C40": 90, f"{AN}!C42": 12, f"{AN}!C53": 100, f"{AN}!C54": 250,
    f"{AN}!C57": 0.03, f"{AN}!C60": 0.01, f"{AN}!C88": 15,
    f"{PA}!C22": 0.10, f"{PA}!C23": 50, f"{PA}!C24": 5000, f"{PA}!C10": 5, f"{PA}!C43": "Transitorio",
    f"{PA}!C44": 200, f"{PA}!C47": "Básicas frente a diluidas",
    f"{CM}!D5": 1, f"{CM}!L4": "IFRS", f"{CM}!J4": "mm",
    f"{HI}!C57": 3,
}

# configuraciones que activan entradas condicionales (sobre la base de cada motor)
CONFIGS = {
    "base": {},
    "quiebra": {f"{PA}!C22": 0.10, f"{PA}!C23": 50},
    "fcf_negativo_normalizado": {f"{AN}!C46": 0, f"{PA}!C43": "Transitorio", f"{PA}!C44": 200},
    "exceso_caja": {f"{AN}!C76": 50},
    "adr": {f"{PA}!C47": "ADR o ADS", f"{CM}!D5": 1},
    "desviacion_capitalizacion": {f"{AN}!C41": 2200 * 1.30, f"{PA}!C47": "Básicas frente a diluidas"},
    "id_capitalizada": {f"{PA}!C9": "Sí", f"{PA}!C10": 5},
}


def candidatos(wb):
    """Celdas editables a perturbar: una por celda, salvo Historia, que va por filas (C:L)."""
    out = []
    for hoja, rangos in ENTRADAS.items():
        if hoja in EXCLUIDAS_POR_DISENO or hoja == CM and False:
            pass
        for r in rangos:
            if hoja == HI and r == "C5:L26":
                for fila in range(5, 27):
                    out.append((HI, f"fila{fila}"))
                continue
            if hoja == HI and r == "M5:S26":
                continue
            if hoja == CM and r in ("E17:N82", "C86:E102", "E107:N173"):
                continue   # trazabilidad: documentación, no entradas del cálculo
            for c in celdas(r):
                out.append((hoja, c))
    return out


def aplicar(wb, hoja, coord, valor):
    if coord.startswith("fila"):
        fila = int(coord[4:])
        for col in range(3, 13):
            v = wb[HI].cell(fila, col).value
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                wb[HI].cell(fila, col).value = (v * 1.07 + 1.0) if fila != 10 else min(0.95, v * 1.07 + 0.013)
        return True
    wb[hoja][coord] = valor
    return True


# En las configuraciones condicionales solo se perturban las entradas que esa configuración activa
# (más las que interactúan con ellas); el barrido completo se hace en «base».
SUBCONJUNTO = {
    "quiebra": [f"{PA}!C22", f"{PA}!C23", f"{AN}!C56", f"{AN}!B69", f"{AN}!C69", f"{AN}!D69"],
    "fcf_negativo_normalizado": [f"{PA}!C43", f"{PA}!C44", f"{AN}!C46", f"{AN}!C47", f"{AN}!C48", f"{AN}!C49",
                                 f"{AN}!C50", f"{AN}!C51", f"{HI}!C57", f"{HI}!fila7", f"{HI}!fila8",
                                 f"{HI}!fila10", f"{HI}!fila12", f"{HI}!fila14", f"{HI}!fila6"],
    "exceso_caja": [f"{AN}!C76"],
    "adr": [f"{PA}!C47", f"{CM}!D5", f"{PA}!C48", f"{AN}!C37", f"{AN}!C41"],
    "desviacion_capitalizacion": [f"{PA}!C47", f"{AN}!C41", f"{AN}!C55", f"{AN}!C37"],
    "id_capitalizada": [f"{PA}!C9", f"{PA}!C10", f"{HI}!fila19", f"{PA}!B18", f"{PA}!C18", f"{PA}!D18"],
}


def construir_casos(src, work, motor, config):
    base_p = os.path.join(work, f"{motor}__{config}__BASE.xlsx")
    if not os.path.exists(base_p):
        shutil.copy(src, base_p)
        wb = load_workbook(base_p)
        wb[AN]["C62"] = MOT[motor]
        for k, v in CONFIGS[config].items():
            h, c = k.split("!"); wb[h][c] = v
        wb.save(base_p)
    base_wb = load_workbook(base_p)
    casos = []
    sub = set(SUBCONJUNTO.get(config, []))
    for hoja, coord in candidatos(base_wb):
        if (hoja, coord) in NO_PERTURBAR:
            continue
        key = f"{hoja}!{coord}"
        if config != "base" and key not in sub:
            continue
        if coord.startswith("fila"):
            nuevo = "×1,07"
        else:
            actual = base_wb[hoja][coord].value
            if actual is None or actual == "":
                nuevo = RELLENO.get(key)
                if nuevo is None:
                    continue
            else:
                nuevo = perturbar(actual, hoja, coord, LISTAS)
                if nuevo is None:
                    continue
        p = os.path.join(work, f"{motor}__{config}__{hoja[:3]}_{coord}.xlsx")
        if not os.path.exists(p):
            shutil.copy(base_p, p)
            wb = load_workbook(p)
            aplicar(wb, hoja, coord, nuevo)
            wb.save(p)
        casos.append((key, p, nuevo))
    return base_p, casos


def recalcular(ficheros, destino, maximo=None):
    os.makedirs(destino, exist_ok=True)
    ficheros = [f for f in ficheros if not os.path.exists(os.path.join(destino, os.path.basename(f)))]
    if maximo is not None:
        ficheros = ficheros[:maximo]
    for i in range(0, len(ficheros), 20):
        subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx", "--outdir", destino]
                       + ficheros[i:i + 20], capture_output=True, timeout=1200)


def main():
    src, work, out = sys.argv[1], sys.argv[2], sys.argv[3]
    fase = sys.argv[sys.argv.index("--fase") + 1] if "--fase" in sys.argv else "todo"
    maximo = int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else None
    if fase == "todo" and os.path.isdir(work):
        shutil.rmtree(work)
    os.makedirs(work, exist_ok=True)
    estatica = traza_estatica(src)
    plan = []   # (motor, config, key, path, nuevo)
    bases = {}
    for motor in "ABC":
        for config in CONFIGS:
            if config == "fcf_negativo_normalizado" and motor != "A":
                continue
            if config == "exceso_caja" and motor != "A":
                continue
            base_p, casos = construir_casos(src, work, motor, config)
            bases[(motor, config)] = base_p
            for key, p, nuevo in casos:
                plan.append((motor, config, key, p, nuevo))
    todos = list(bases.values()) + [p for _, _, _, p, _ in plan]
    rct = os.path.join(work, "rct")
    if fase == "construir":
        print(f"construidos {len(todos)} libros"); return
    pendientes = [f for f in todos if not os.path.exists(os.path.join(rct, os.path.basename(f)))]
    print(f"recálculo: {len(pendientes)} pendientes de {len(todos)}")
    recalcular(todos, rct, maximo)
    if fase == "recalcular":
        return
    sal_base = {k: leer_salidas(os.path.join(rct, os.path.basename(p))) for k, p in bases.items()}
    activ = collections.defaultdict(dict)   # key -> motor -> {config: [salidas que cambian]}
    for motor, config, key, p, nuevo in plan:
        rp = os.path.join(rct, os.path.basename(p))
        if not os.path.exists(rp):
            activ[key].setdefault(motor, {})[config] = "NO RECALCULADO"
            continue
        s = leer_salidas(rp)
        b = sal_base[(motor, config)]
        cambian = [k for k in s if s[k] != b[k]]
        if cambian:
            activ[key].setdefault(motor, {})[config] = cambian
    rel = {
        "fuente": os.path.basename(src),
        "salidas_vigiladas": [f"{h}!{c}" for h, c in SALIDAS],
        "configuraciones": CONFIGS,
        "traza_estatica_editables_alcanzadas": estatica,
        "activacion_empirica": {k: activ[k] for k in sorted(activ)},
        "perturbadas_sin_efecto": sorted({key for _, _, key, _, _ in plan} - set(activ)),
        "recalculos": len(todos),
    }
    json.dump(rel, open(out, "w"), ensure_ascii=False, indent=1, default=str)
    print(f"traza estática: {len(estatica)} celdas editables alcanzadas")
    print(f"activación empírica: {len(activ)} entradas mueven alguna salida · {len(rel['perturbadas_sin_efecto'])} sin efecto · {len(todos)} recálculos")
    for k in sorted(activ):
        print(f"  {k:<26} " + " · ".join(f"{m}:{','.join(cfgs)}" for m, cfgs in activ[k].items()))


if __name__ == "__main__":
    main()
