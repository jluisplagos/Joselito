#!/usr/bin/env python3
"""Lee la copia recalculada de un libro V6.3 y escribe resultados.json (Anexo D §D.5).

Uso: leer_resultados.py recalc/<E>.xlsx resultados.json [--exigir-recalculo-forzado]
Comprueba que el recálculo fue real (encargo §4.7): valores que la hoja calcula por fórmula se recomputan
aquí desde los datos de Historia y tienen que coincidir; y los veredictos dependientes de celdas escritas
no pueden seguir en «—». Si falla, código 4 (y con --exigir-recalculo-forzado no escribe nada).
"""
import json
import sys

import leer_v63 as L


def comprobar_recalculo(t):
    fallos = []
    h = t["historia"]
    ventas = h["partidas"]["ventas"]
    n_ventas = sum(1 for x in ventas if L.num(x) is not None)
    c43 = L.num(h["anclas"]["anios_con_ventas"])
    if c43 is not None and c43 != n_ventas:
        fallos.append(f"Historia!C43 = {c43} pero hay {n_ventas} ventas: cachés viejas")
    ebit, v = h["partidas"]["ebit"][-1], ventas[-1]
    if L.num(ebit) is not None and L.num(v) not in (None, 0):
        c48 = L.num(h["anclas"]["margen_ultimo"])
        if c48 is None or abs(c48 - ebit / v) > 1e-9:
            fallos.append(f"Historia!C48 = {c48} ≠ EBIT/ventas del último año {ebit / v:.6f}: cachés viejas")
    a = t["analisis"]
    for cin, dep in (("C11", "D11"), ("C12", "D12"), ("C13", "D13"), ("C17", "D17"), ("C18", "D18"), ("C25", "D25")):
        if a.get(cin) not in (None, "") and a["veredictos"].get(dep) in (None, "—"):
            fallos.append(f"Análisis!{cin} escrita pero {dep} sigue en «—»: cachés viejas")
    motor_letra = t["diagnostico"]["motor"]
    c62 = a.get("C62")
    esperado = {"Sí": "A", "No · financiación cambia mucho": "B", "No · banco o aseguradora": "C"}.get(c62)
    if esperado and motor_letra != esperado:
        fallos.append(f"Análisis!C62 = {c62!r} pero Diagnóstico V6!C5 = {motor_letra!r}: cachés viejas")
    return fallos


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    src, dst = sys.argv[1], sys.argv[2]
    wb = L.abrir(src)
    t = L.todo(wb)
    fallos = comprobar_recalculo(t)
    a, d, m, cm = t["analisis"], t["diagnostico"], t["motor"], t["control_maestro"]
    res = {
        "origen": src,
        "recalculo_forzado_comprobado": not fallos,
        "fallos_recalculo": fallos,
        "valores": {k: a.get(k) for k in ("B78", "C78", "D78", "C83", "C84", "C85", "C86", "C39", "C87", "C37", "C41", "C55", "C56", "C57")},
        "probabilidades": [a.get("B69"), a.get("C69"), a.get("D69")],
        "g_perpetuo": [a.get("B68"), a.get("C68"), a.get("D68")],
        "estados": {k: m[k] for k in ("estado_tecnico_B255", "causa_tecnica_B256", "estado_inversion_B258", "estado_libro_B266",
                                     "lectura_precio_B267", "veredicto_B268", "evidencias_B269", "bloqueo_valor_B252", "comparable_B253",
                                     "bloqueo_lectura_B254", "n_avisos_B260", "n_causas_B261", "dcf_inverso_monotono_B193")},
        "reglas_motor": m["reglas"],
        "causas_activas": d["causas_activas"],
        "semaforos": d["semaforos"],
        "por_escenario": d["por_escenario"],
        "cuanto_pagas_por_crecer": d["cuanto_pagas_por_crecer"],
        "multiplos": d["multiplos"],
        "autocomprobaciones": d["autocomprobaciones"],
        "salto_anio_11": d["salto_anio_11"],
        "tornado": d["tornado"],
        "precio_referencia_hoja_C156": d["precio_referencia_hoja"],
        "parametros_hoja": d["parametros"],
        "evidencias": cm["resumen"],
        "banderas_C7": a.get("C7"), "revisar_D7": a.get("D7"), "veredicto_A6": a.get("A6"),
        "tabla_dcf_inverso": a["tabla_dcf_inverso"],
        "motor": d["motor"], "coherencia_tipo_motor": d["coherencia_tipo_motor"],
        "r_operativa_C15": d["r_operativa"], "r_minima_C17": d["r_minima"], "r_vs_minima_C18": d["r_vs_minima"],
        "pasivos_netos_B_C16": d["pasivos_netos_B"], "V0": d["V0"], "m0": d["m0"], "t": d["t"], "f": d["f"],
        "anclas_historia": {k: v for k, v in t["historia"]["anclas"].items() if not k.startswith("C")},
        "palancas": {k: t["palancas"][k] for k in ("C5", "C6", "C7", "C8", "C9", "C10", "B14", "C14", "D14", "B15", "C15", "D15", "B16", "C16", "D16",
                                                   "B18", "C18", "D18", "C22", "C23", "C24", "C43", "C44", "C47", "C48")},
        "veredictos_analisis": a["veredictos"],
        "celdas_juicio_analisis": {k: a.get(k) for k in ("C11", "C12", "C13", "C14", "C17", "C18", "C19", "C20", "C25", "C27", "C51", "C56", "C61", "C62",
                                                        "B65", "C65", "D65", "B66", "C66", "D66", "C76", "C93", "C97", "C98", "B101", "B102", "C103", "C104")},
    }
    exigir = "--exigir-recalculo-forzado" in sys.argv
    if fallos:
        print("RECÁLCULO NO FORZADO: " + " | ".join(fallos))
        if exigir:
            return 4
    json.dump(res, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print(f"OK: resultados.json → {dst} · motor {res['motor']} · estado {res['estados']['estado_tecnico_B255']} · libro {res['estados']['estado_libro_B266']}")
    return 0 if not fallos else 4


if __name__ == "__main__":
    sys.exit(main())
