#!/usr/bin/env python3
"""Comprobación de entrada de un libro V6.3 con los datos de fase 1 (encargo §3.4; pipeline pasos 3 y 7).

Uso: comprobar_entrada_v63.py <E>_v63_datos.xlsx CARPETA [--motor A|B|C] [--config config_v2.json]

Hace: verificar_v63 · recálculo forzado (recalc.sh) · estado técnico · simulación de los TRES motores con palancas de
prueba (informa cuáles son calculables con los datos que hay y por qué no los otros) · comparabilidad Motor!B253 ·
niveles de §3.4 (bloqueante / necesario para LISTO·PROVISIONAL / no bloqueante). Escribe:
  CARPETA/entrada_v63.md, CARPETA/entrada_v63.json, CARPETA/datos_ausentes.json (lo no bloqueante que falta), CARPETA/recalc/<libro>
Código: 0 sin bloqueantes · 1 bloqueante (el pipeline se detiene: pendiente_de_datos) · 2 uso.
Con --motor, el motor elegido por la fase A tiene que ser calculable; si no, código 1.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import config_v2  # noqa: E402
import leer_v63 as L  # noqa: E402
from v63_xml import LibroV63  # noqa: E402

MOTOR_C62 = {"A": "Sí", "B": "No · financiación cambia mucho", "C": "No · banco o aseguradora"}


def recalc(libro, outdir, perfil):
    r = subprocess.run(["bash", os.path.join(AQUI, "recalc.sh"), libro, outdir, perfil], capture_output=True, text=True)
    out = os.path.join(outdir, os.path.basename(libro))
    return (r.returncode == 0 and os.path.exists(out)), out, r.stdout + r.stderr


def verificar(libro, cfg):
    r = subprocess.run([sys.executable, cfg["plantilla"]["verificador"], libro, cfg["plantilla"]["referencia"]], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1:] 


def simular_motor(libro, motor, t, tmpdir, perfil):
    """Escribe palancas de prueba y el motor en una copia, recalcula y devuelve (calculable, reglas_nivel1_fallidas, C83)."""
    h = t["historia"]["anclas"]
    a = t["analisis"]
    m0 = L.num(h.get("margen_ultimo")) or L.num(h.get("margen_medio")) or 0.10
    roe0 = L.num(h.get("roe_ultimo")) or L.num(h.get("roe_medio_5")) or 0.10
    celdas = {"Análisis!C62": MOTOR_C62[motor],
              "Palancas!B14": 0.03, "Palancas!C14": 0.04, "Palancas!D14": 0.05,
              "Análisis!B68": 0.015, "Análisis!C68": 0.02, "Análisis!D68": 0.025,
              "Palancas!B18": 0.10, "Palancas!C18": 0.10, "Palancas!D18": 0.10,
              "Análisis!B69": 0.2, "Análisis!C69": 0.6, "Análisis!D69": 0.2,
              "Análisis!B65": "Otra (explícala en tus palabras)", "Análisis!C65": "Otra (explícala en tus palabras)", "Análisis!D65": "Otra (explícala en tus palabras)",
              "Análisis!B66": "simulación", "Análisis!C66": "simulación", "Análisis!D66": "simulación"}
    if motor == "C":
        celdas.update({"Palancas!B15": max(roe0 * 0.8, 0.01), "Palancas!C15": max(roe0, 0.01), "Palancas!D15": max(roe0 * 1.2, 0.01),
                       "Palancas!B16": None, "Palancas!C16": None, "Palancas!D16": None})
    else:
        celdas.update({"Palancas!B15": max(m0 * 0.8, 0.005), "Palancas!C15": max(m0, 0.005), "Palancas!D15": max(m0 * 1.2, 0.005),
                       "Palancas!B16": 1.0, "Palancas!C16": 1.0, "Palancas!D16": 1.0})
    if not t["palancas"].get("C5"):
        celdas["Palancas!C5"] = "Madura"
    if not t["palancas"].get("C6"):
        celdas["Palancas!C6"] = "Ninguno"
    c52 = L.num(a.get("C52"))
    if motor == "A":
        celdas["Palancas!C43"] = "No aplica" if (c52 is not None and c52 > 0) else None
    if motor == "A" and L.num(a.get("C76")) is None:
        celdas["Análisis!C76"] = 0
    if not a.get("C51"):
        celdas["Análisis!C51"] = "Sí"
    if L.num(a.get("C56")) is None:
        celdas["Análisis!C56"] = 0.09
    cj = os.path.join(tmpdir, f"sim_{motor}.json")
    json.dump(celdas, open(cj, "w", encoding="utf-8"), ensure_ascii=False)
    sim = os.path.join(tmpdir, f"sim_{motor}.xlsx")
    r = subprocess.run([sys.executable, os.path.join(AQUI, "escribir_v63.py"), libro, sim, "--celdas", cj, "--lista-blanca", "juicio"], capture_output=True, text=True)
    if r.returncode != 0:
        return False, [f"no se pudo escribir la simulación: {r.stdout + r.stderr}"], None, None
    ok, rec, _ = recalc(sim, os.path.join(tmpdir, "recalc"), perfil)
    if not ok:
        return False, ["LibreOffice no recalculó la simulación"], None, None
    ts = L.todo(L.abrir(rec))
    reglas = ts["motor"]["reglas"]
    fallidas = [r_ for r_ in reglas if r_["aplica"] and r_["resultado"] in ("INCOMPLETO", "DATOS INVÁLIDOS", "MODELO NO APLICABLE") and r_["nivel"] == 1]
    c83 = L.num(ts["analisis"].get("C83"))
    calculable = (not ts["motor"]["bloqueo_valor_B252"]) and c83 is not None
    return calculable, [f"{x['id']} {x['resultado']}: {x['causa']}" for x in fallidas], c83, ts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("libro")
    ap.add_argument("carpeta")
    ap.add_argument("--motor", choices=["A", "B", "C"])
    ap.add_argument("--config", default=os.path.join(AQUI, "..", "config_v2.json"))
    a = ap.parse_args()
    cfg = config_v2.cargar(a.config)
    perfil = cfg.get("recalc", {}).get("perfil", os.path.join(a.carpeta, ".lo_perfil"))
    os.makedirs(a.carpeta, exist_ok=True)
    bloq, necesarios, no_bloq, notas = [], [], [], []
    # 1. integridad
    code, tail = verificar(a.libro, cfg)
    integro = code == 0
    if not integro:
        bloq.append({"dato": "libro íntegro (verificar_v63.py)", "detalle": " ".join(tail)})
    # 2. recálculo forzado
    ok, rec, out = recalc(a.libro, os.path.join(a.carpeta, "recalc"), perfil)
    if not ok:
        bloq.append({"dato": "recálculo con LibreOffice", "detalle": out[-300:]})
        escribir_salidas(a, {"bloqueantes": bloq, "necesarios": necesarios, "no_bloqueantes": no_bloq, "motores": {}, "notas": notas, "integro": integro})
        return 1
    t = L.todo(L.abrir(rec))
    an, pal, cm, m, d, h = t["analisis"], t["palancas"], t["control_maestro"], t["motor"], t["diagnostico"], t["historia"]
    # 3. datos bloqueantes explícitos (§3.4)
    def falta(ref, nombre, lista, origen, nota=""):
        lista.append({"dato": ref, "que": nombre, "origen_esperado": origen, "nota": nota})
    if not an.get("B3"):
        falta("Análisis!B3", "nombre de la empresa", bloq, "fase 1 / etapa 1")
    if not an.get("D3"):
        falta("Análisis!D3", "ticker", bloq, "fase 1 / etapa 1")
    if L.num(an.get("C37")) is None:
        falta("Análisis!C37", "precio actual (en la moneda del modelo)", bloq, "fase1_v63.json (precio con fecha y, si hace falta, tipo de cambio)")
    if L.num(an.get("C41")) is None:
        falta("Análisis!C41", "capitalización (mm, moneda del modelo)", bloq, "fase1_v63.json")
    if L.num(an.get("C55")) is None:
        falta("Análisis!C55", "acciones diluidas (mm)", bloq, "fase1_v63.json / etapa 1")
    for ref in ("C46", "C47", "C48", "C49", "C50"):
        v = an.get(ref)
        if v is not None and L.num(v) is None:
            falta(f"Análisis!{ref}", "dato del FCF base no numérico", bloq, "etapa 1 / fase 1", f"valor {v!r}")
    if L.num(an.get("C46")) is None or L.num(an.get("C47")) is None:
        falta("Análisis!C46:C47", "CFO y capex medios (FCF base)", bloq, "etapa 1 / fase 1")
    if not pal.get("C7"):
        falta("Palancas!C7", "sector de Damodaran (la hoja lo exige; sin él no hay cuartiles)", bloq, "fase1_v63.json (lista Sector!A5:A98)")
    d5 = cm["cabecera"]["D5_ratio_adr"]
    if d5 not in (None, "") and L.num(d5) is None:
        falta("Control maestro!D5", "ratio ADR no numérico", bloq, "fase1_v63.json", f"valor {d5!r}")
    if not m["comparable_B253"]:
        falta("Motor!B253", "precio no comparable con el valor", bloq, "fase1_v63.json",
              f"Palancas!C48 = {pal.get('C48')!r} · Control maestro!H4 = {cm['cabecera']['H4_moneda']!r} · D5 = {d5!r} · C47 = {pal.get('C47')!r}")
    for r_ in m["reglas"]:
        if r_["aplica"] and r_["resultado"] == "DATOS INVÁLIDOS":
            falta(f"regla {r_['id']}", r_["regla"], bloq, "fase 1", r_["causa"])
    # 4. necesarios para LISTO·PROVISIONAL (no para el valor)
    for ref, nombre in (("C24", "ROIC/ROCE"), ("C26", "CFO ÷ beneficio neto"), ("C28", "dilución"), ("C31", "cobros/inventario vs ingresos"),
                        ("C32", "goodwill ÷ activo"), ("C33", "deuda neta ÷ EBITDA"), ("C34", "la caja cubre la deuda a corto")):
        if an.get(ref) in (None, ""):
            falta(f"Análisis!{ref}", nombre + " (comprobación C08 de la hoja)", necesarios, "fase1_v63.json o derivado de Historia (rellenar_fase1_v63.py)")
    for ref, nombre in (("H4_moneda", "moneda del modelo"), ("J4_unidad", "unidad"), ("L4_norma", "norma contable")):
        if not cm["cabecera"].get(ref):
            falta(f"Control maestro!{ref[:2]}", nombre, necesarios if ref != "H4_moneda" else bloq, "fase1_v63.json")
    # 4b. evidencias de datos pendientes en el inventario (control de evidencias): necesarias para LISTO·PROVISIONAL, no para el valor
    for x in cm["inventario"]:
        if x.get("aplica") and x.get("tipo") == "dato" and x.get("estado_evidencia") not in ("documentada", "—", None, ""):
            falta(f"evidencia {x['celda']}", f"{x.get('concepto')}: {x.get('estado_evidencia')}", necesarios, "fase1_v63.json (fuente y página del dato) o etapa 1",
                  "el dato está pero su clasificación/documento no permite LISTO·PROVISIONAL; la fase C juzga si es material")
    # 5. no bloqueantes
    if not any(g[0] for g in pal["geografia"]):
        falta("Palancas!A28:B33", "reparto geográfico", no_bloq, "fase1_v63.json", "sin él la r mínima no lleva prima de los países donde vende")
    if L.num(pal.get("C24")) is None:
        falta("Palancas!C24", "tamaño del mercado año 10", no_bloq, "extractos (solo con cifra de fuente primaria)")
    if L.num(an.get("C88")) is None:
        falta("Análisis!C88", "P/FCF histórico", no_bloq, "fase1_v63.json")
    if L.num(an.get("C38")) is None:
        falta("Análisis!C38", "valor intrínseco de fuente externa (contraste)", no_bloq, "fase1_v63.json (opcional)")
    for r_ in m["reglas"]:
        if r_["aplica"] and r_["resultado"] == "AVISO":
            notas.append(f"{r_['id']} AVISO: {r_['causa']}")
    # 6. simulación de los tres motores
    motores = {}
    with tempfile.TemporaryDirectory() as tmp:
        for letra in ("A", "B", "C"):
            calc, fallidas, c83, _ = simular_motor(a.libro, letra, t, tmp, perfil)
            motores[letra] = {"calculable": calc, "reglas_nivel_1_fallidas": fallidas, "C83_simulado": c83}
    if not any(v["calculable"] for v in motores.values()):
        falta("Historia / datos", "ningún motor calcula con los datos presentes", bloq, "fase1_v63.json (Contrato_de_relleno_V6.3.csv)",
              " · ".join(f"{k}: {'; '.join(v['reglas_nivel_1_fallidas'])}" for k, v in motores.items()))
    if a.motor and not motores[a.motor]["calculable"]:
        falta("motor elegido", f"el motor {a.motor} elegido por la fase A no es calculable", bloq, "fase1_v63.json",
              "; ".join(motores[a.motor]["reglas_nivel_1_fallidas"]))
    res = {"libro": a.libro, "recalc": rec, "integro": integro, "estado_tecnico": m["estado_tecnico_B255"], "causa_tecnica": m["causa_tecnica_B256"],
           "estado_libro": m["estado_libro_B266"], "comparable": m["comparable_B253"], "motores": motores, "motor_elegido": a.motor,
           "bloqueantes": bloq, "necesarios_para_listo_provisional": necesarios, "no_bloqueantes": no_bloq, "avisos": notas,
           "anios_con_ventas": h["anclas"].get("anios_con_ventas")}
    escribir_salidas(a, res)
    print(f"{'BLOQUEANTE' if bloq else 'OK'}: {len(bloq)} bloqueantes · {len(necesarios)} necesarios para LISTO·PROVISIONAL · {len(no_bloq)} no bloqueantes · motores calculables: {[k for k, v in motores.items() if v['calculable']]}")
    return 1 if bloq else 0


def escribir_salidas(a, res):
    json.dump(res, open(os.path.join(a.carpeta, "entrada_v63.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    # datos_ausentes.json: lo no bloqueante (necesarios + no bloqueantes) para la revisión de la fase C (S-19)
    da = []
    for x in res.get("necesarios_para_listo_provisional", []):
        da.append({"dato": x["dato"], "que": x.get("que"), "nivel": "necesario para LISTO·PROVISIONAL", "origen_esperado": x.get("origen_esperado"), "nota": x.get("nota", "")})
    for x in res.get("no_bloqueantes", []):
        da.append({"dato": x["dato"], "que": x.get("que"), "nivel": "no bloqueante", "origen_esperado": x.get("origen_esperado"), "nota": x.get("nota", "")})
    json.dump(da, open(os.path.join(a.carpeta, "datos_ausentes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = [f"# Comprobación de entrada · {os.path.basename(a.libro)}\n",
          f"- Íntegro (verificar_v63.py): {res.get('integro')} · estado técnico: {res.get('estado_tecnico')} ({res.get('causa_tecnica') or '—'}) · estado del libro: {res.get('estado_libro')} · comparable precio↔valor: {res.get('comparable')} · años con ventas: {res.get('anios_con_ventas')}",
          "\n## Motores calculables (simulación con palancas de prueba)\n"]
    for k, v in res.get("motores", {}).items():
        md.append(f"- Motor {k}: {'CALCULABLE' if v['calculable'] else 'NO calculable'}" + (f" · reglas de nivel 1 que fallan: {'; '.join(v['reglas_nivel_1_fallidas'])}" if v["reglas_nivel_1_fallidas"] else ""))
    if res.get("motor_elegido"):
        md.append(f"- Motor elegido por la fase A: {res['motor_elegido']} → {'calculable' if res['motores'].get(res['motor_elegido'], {}).get('calculable') else 'NO calculable: pendiente_de_datos'}")
    for titulo, clave in (("## BLOQUEANTE (el pipeline se detiene: pendiente_de_datos)", "bloqueantes"), ("## Necesario para LISTO · PROVISIONAL (no para el valor)", "necesarios_para_listo_provisional"), ("## No bloqueante", "no_bloqueantes")):
        md.append("\n" + titulo + "\n")
        items = res.get(clave, [])
        md.extend([f"- {x['dato']}: {x.get('que', '')} · de dónde: {x.get('origen_esperado', '')}" + (f" · {x['nota']}" if x.get('nota') else "") for x in items] or ["- ninguno"])
    md.append("\n## Avisos de la hoja\n")
    md.extend([f"- {x}" for x in res.get("avisos", [])] or ["- ninguno"])
    open(os.path.join(a.carpeta, "entrada_v63.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")


if __name__ == "__main__":
    sys.exit(main())
