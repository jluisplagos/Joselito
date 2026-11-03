#!/usr/bin/env python3
"""Comprobación conjunta de las hipótesis sin fundamento (D10; Anexo B §B.6; Anexo D §D.6b).

Uso: comprobacion_conjunta.py CARPETA <E>_v63_evaluada.xlsx [--config config_v2.json]
Lee fase_c.json → fundamento_material.comprobacion_conjunta.combinacion ({"Hoja!REF": valor}) y rangos_y_evidencia (si los hay).
Escribe la combinación en una COPIA DE PRUEBA (comprobacion_conjunta/<E>_conj.xlsx; nunca toca el libro), recalcula con
recálculo forzado, lee valores (leer_resultados.py), calcula la escalera (precio_de_si.py --copia), pasa la gramática sobre la
copia y escribe comprobacion_conjunta.json con `sobrevive`. El script NO decide: la fase C lee el resultado en su segundo turno.
Código 0 ok · 1 no se pudo ejecutar (fallo mecánico) · 2 uso · 3 combinación mal formada por el agente (celda ajena a las 52 de A/B, de la
fase C, de Control maestro, o valor no numérico): el pipeline pide corrección a la fase C.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import config_v2  # noqa: E402
import celdas_v2 as C  # noqa: E402


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("libro")
    ap.add_argument("--config", default=os.path.join(AQUI, "..", "config_v2.json"))
    a = ap.parse_args()
    cfg = config_v2.cargar(a.config)
    fc = json.load(open(os.path.join(a.carpeta, "fase_c.json"), encoding="utf-8"))
    fm = fc.get("fundamento_material") or {}
    cc = fm.get("comprobacion_conjunta") or {}
    comb = cc.get("combinacion")
    if not cc.get("procede") or not comb:
        print("no procede: fase_c.json no trae una combinación (procede = false o combinacion vacía)")
        return 3
    if not isinstance(comb, dict):
        print(f"ERROR: combinacion tiene que ser un objeto celda → valor (es {type(comb).__name__})")
        return 3
    # claves sin hoja → Análisis (mismo criterio que fase_a_celdas.py y el ejemplo de §D.6b)
    comb = {(k if "!" in k else f"Análisis!{k}"): v for k, v in comb.items()}
    permitidas = C.lista_blanca_juicio()
    malas = [k for k in comb if k.split("!")[0] not in permitidas or k.split("!")[1] not in permitidas[k.split("!")[0]] or k.startswith("Control maestro")]
    if malas:
        print(f"ERROR: la combinación toca celdas que no son de juicio: {malas}")
        return 3
    fase_c_solo = [k for k in comb if C.CELDAS[k.split("!")[0]][k.split("!")[1]].get("fase") == "C"]
    if fase_c_solo:
        print(f"ERROR: la combinación toca celdas de la fase C (todavía no escritas): {fase_c_solo}")
        return 3
    no_num = [k for k, v in comb.items() if not isinstance(v, (int, float)) or isinstance(v, bool)]
    if no_num:
        print(f"ERROR: la combinación trae valores no numéricos: {no_num}")
        return 3
    carp = os.path.join(a.carpeta, "comprobacion_conjunta")
    os.makedirs(carp, exist_ok=True)
    base = os.path.basename(a.libro).replace("_v63_evaluada", "").replace(".xlsx", "")
    copia = os.path.join(carp, f"{base}_conj.xlsx")
    cj = os.path.join(carp, "combinacion.json")
    json.dump(comb, open(cj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    rc, out = run([sys.executable, os.path.join(AQUI, "escribir_v63.py"), a.libro, copia, "--celdas", cj, "--copia-de-prueba"])
    if rc != 0:
        print("ERROR al escribir la copia de prueba:", out[-400:])
        return 1
    perfil = os.path.join(a.carpeta, ".lo_perfil") if cfg.get("recalc", {}).get("perfil_por_empresa", True) else cfg.get("recalc", {}).get("perfil", os.path.join(carp, ".lo_perfil"))
    rc, out = run(["bash", os.path.join(AQUI, "recalc.sh"), copia, os.path.join(carp, "recalc"), perfil])
    if rc != 0:
        print("ERROR al recalcular la copia:", out[-400:])
        return 1
    rec = os.path.join(carp, "recalc", os.path.basename(copia))
    res_path = os.path.join(carp, "resultados.json")
    rc, out = run([sys.executable, os.path.join(AQUI, "leer_resultados.py"), rec, res_path, "--exigir-recalculo-forzado"])
    if rc != 0:
        print("ERROR al leer la copia recalculada:", out[-400:])
        return 1
    res = json.load(open(res_path, encoding="utf-8"))
    res["copia_de_prueba"] = True
    json.dump(res, open(res_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    precio_path = os.path.join(carp, "precio.json")
    if os.path.exists(precio_path):
        os.remove(precio_path)
    rc, out = run([sys.executable, os.path.join(AQUI, "precio_de_si.py"), res_path, precio_path, "--copia", "--k", str(cfg.get("convenciones", {}).get("k_asimetria", 3))])
    if rc not in (0, 5) or not os.path.exists(precio_path):
        print(f"ERROR: precio_de_si.py sobre la copia terminó con código {rc}:", out[-400:])
        return 1
    precio = json.load(open(precio_path, encoding="utf-8"))
    # gramática sobre la copia (carpeta temporal con fase_b, referencias, datos y los resultados de la copia)
    tmp = os.path.join(carp, "gramatica_copia")
    os.makedirs(tmp, exist_ok=True)
    for f in ("fase_b.json", "referencias_mecanicas.json", "datos_v63.json"):
        shutil.copy(os.path.join(a.carpeta, f), os.path.join(tmp, f))
    shutil.copy(res_path, os.path.join(tmp, "resultados.json"))
    rc_g, out_g = run([sys.executable, os.path.join(AQUI, "comprobar_gramatica.py"), tmp, "--tras-recalculo", "--copia-de-prueba"])
    if rc_g == 4 or not os.path.exists(os.path.join(tmp, "gramatica.json")):
        print("ERROR: la gramática no pudo ejecutarse sobre la copia:", out_g[-400:])
        return 1
    gram = json.load(open(os.path.join(tmp, "gramatica.json"), encoding="utf-8"))
    errores = [f"{x['id']} {x.get('escenario') or ''}: {x['detalle']}" for x in gram["hallazgos"] if x["categoria"] in ("error", "límite del modelo")]
    original = json.load(open(os.path.join(a.carpeta, "precio.json"), encoding="utf-8")) if os.path.exists(os.path.join(a.carpeta, "precio.json")) else {}
    zona = precio.get("zona")
    sobrevive = (zona in ("cumple_regla_k", "bajo_malo")) and not errores and "sin_lectura" not in precio and "sin_escalera" not in precio
    out = {
        "libro_origen": a.libro, "copia_de_prueba": copia, "hash_copia": hashlib.sha256(open(copia, "rb").read()).hexdigest(),
        "combinacion": comb, "rangos_y_evidencia": cc.get("rangos_y_evidencia") or {h.get("celda"): h.get("alternativas_defendibles") for h in (fm.get("hipotesis_sin_fundamento") or [])},
        "coherencia_economica": cc.get("coherencia_economica"),
        "recalculo_forzado_comprobado": res.get("recalculo_forzado_comprobado"),
        "precio_actual": precio.get("precio"),
        "resultados_bajo_combinacion": {"B78": res["valores"].get("B78"), "C78": res["valores"].get("C78"), "D78": res["valores"].get("D78"), "C83": res["valores"].get("C83"),
                                        "Motor!B255": res["estados"].get("estado_tecnico_B255"), "semaforos": {k: v[1:] for k, v in (res.get("semaforos") or {}).items() if k in ("fila40", "fila41", "fila42", "fila43", "fila44")},
                                        "errores_gramatica": errores},
        "escalera_bajo_combinacion": {k: precio.get(k) for k in ("P_estrella", "precio_si", "precio_escenario_malo", "ponderado", "zona")} | {"zona_precio_actual": zona, "sin_lectura": precio.get("sin_lectura"), "sin_escalera": precio.get("sin_escalera")},
        "escalera_original": {k: original.get(k) for k in ("V", "p", "P_estrella", "precio_si", "precio_escenario_malo", "ponderado", "zona")} | {"zona_precio_actual": original.get("zona")},
        "sobrevive": sobrevive,
        "nota": "superar esta comprobación no es una garantía de seguridad; su fuerza depende de los rangos declarados (S-17)",
    }
    json.dump(out, open(os.path.join(a.carpeta, "comprobacion_conjunta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print(f"OK: comprobación conjunta → sobrevive = {sobrevive} · zona bajo la combinación: {zona} (original: {original.get('zona')}) · errores de gramática: {len(errores)} → comprobacion_conjunta.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
