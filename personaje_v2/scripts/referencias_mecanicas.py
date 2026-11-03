#!/usr/bin/env python3
"""Referencias mecánicas por palanca (Anexo B §B.2; decisión D5). Versión de las reglas: config → version_referencias_mecanicas.

Son CONVENCIÓN DEL EJERCICIO: cifras reproducibles desde las anclas de Historia y los cuartiles de Sector,
para medir la desviación de Munger. No son una estimación de Damodaran ni una predicción. Cuando los datos
no permiten una referencia defendible, la referencia es `null` con su motivo, y no se sustituye por otra medida.

Uso como módulo: calcular(datos, config) → dict. Uso como script: referencias_mecanicas.py datos_v63.json config_v2.json salida.json
"""
import json
import math
import statistics
import sys

LISTA_G = [0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03]
LISTA_P = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6]


def num(x):
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) and not (isinstance(x, float) and math.isnan(x)) else None


def redondear(x, paso):
    if x is None:
        return None
    return round(round(x / paso) * paso, 10)


def ajustar_lista(x, lista=LISTA_G):
    """valor de la lista más cercano; en empate, el de abajo."""
    if x is None:
        return None
    mejor = min(lista, key=lambda v: (abs(v - x), v))
    return mejor


def sigma(serie, minimo=4, defecto=0.03):
    vals = [num(v) for v in serie if num(v) is not None]
    if len(vals) < minimo:
        return defecto, f"σ = {defecto} por convención (solo {len(vals)} tasas anuales)"
    return statistics.stdev(vals), f"σ muestral de {len(vals)} tasas anuales = {statistics.stdev(vals):.4f}"


def cagr(serie, n=5):
    vals = [num(v) for v in serie]
    if len(vals) < n + 1 or vals[-1] is None or vals[-1 - n] is None or vals[-1 - n] <= 0 or vals[-1] <= 0:
        return None
    return (vals[-1] / vals[-1 - n]) ** (1 / n) - 1


def crecimientos(serie):
    vals = [num(v) for v in serie]
    out = []
    for a, b in zip(vals, vals[1:]):
        out.append(b / a - 1 if a not in (None, 0) and b is not None and a > 0 else None)
    return out


def orden(m, n, b, nota):
    """Fuerza MALO ≤ NORMAL ≤ BUENO igualando al NORMAL lo que se salga (y lo anota)."""
    if n is None:
        return m, n, b
    if m is not None and m > n:
        nota.append(f"MALO_ref {m} > NORMAL_ref {n}: se iguala al NORMAL")
        m = n
    if b is not None and b < n:
        nota.append(f"BUENO_ref {b} < NORMAL_ref {n}: se iguala al NORMAL")
        b = n
    return m, n, b


def calcular(d, config):
    """d: datos_v63.json (volcar_datos_v63.py): anclas, series, palancas (sector), analisis, diagnostico."""
    conv = config.get("convenciones", {})
    rm = conv.get("referencias_mecanicas", {})
    red = conv.get("redondeo", {"crecimiento": 0.005, "margen": 0.005, "s2c": 0.1, "roic": 0.01})
    sigma_def = rm.get("sigma_minima_crecimiento_si_pocas_tasas", 0.03)
    suelo_malo = rm.get("suelo_crecimiento_malo", -0.10)
    g_sin_rf = rm.get("g_perpetuo_sin_rf", 0.025)
    tope_rm = rm.get("tope_rentabilidad_marginal_sobre_roic_hist", 2.0)
    tope_roic = rm.get("roic_lp_bueno_tope_sobre_c56", 0.10)
    p_ref = conv.get("probabilidades_referencia", {"MALO": 0.2, "NORMAL": 0.6, "BUENO": 0.2})
    quiebra_ref = conv.get("quiebra_con_disparador", 0.05)
    disp = conv.get("quiebra_disparadores", {})

    anc = d["historia"]["anclas"]
    ser = d["historia"]["series"]
    part = d["historia"]["partidas"]
    pal = d["palancas"]
    sec = pal["sector"]
    an = d["analisis"]
    motor = d["diagnostico"]["motor"]
    etapa = pal.get("C5")
    base_margen = pal.get("C8")
    if base_margen not in ("Último año", "Media del ciclo"):
        raise ValueError(f"Palancas!C8 = {base_margen!r}: la base del margen tiene que ser «Último año» o «Media del ciclo» (fase A)")
    tasa = num(an.get("C56")) if motor in ("A", "C") else num(d["diagnostico"].get("r_operativa"))
    if tasa is None:
        raise ValueError(f"tasa del motor {motor} no numérica (Análisis!C56 o Diagnóstico V6!C15): sin tasa no hay referencias defendibles")
    rf = num(an.get("C57"))
    t = num(anc.get("tipo_impositivo_5"))
    out = {"version_referencias_mecanicas": config.get("version_referencias_mecanicas"), "motor": motor,
           "nota": "convención del ejercicio (Anexo B §B.2): no son estimaciones de Damodaran; «criterio_relacionado» no respalda la cifra",
           "tasa_del_motor": tasa, "rf": rf, "palancas": {}}

    # ---------- crecimiento 1–5 ----------
    nota = []
    if motor == "C":
        c46 = cagr(part["patrimonio"], 5)
        serie_tasas = crecimientos(part["patrimonio"])
        fuente_c46 = "CAGR 5 años del patrimonio (Historia fila 21)"
    else:
        c46 = num(anc.get("cagr_5"))
        serie_tasas = ser.get("crecimiento_ventas", [])
        fuente_c46 = "Historia!C46 (CAGR 5 años de ventas)"
    q1, q3 = num(sec.get("crecimiento_q1")), num(sec.get("crecimiento_q3"))
    if c46 is None or q1 is None or q3 is None:
        motivo = "no disponible: " + ("falta el CAGR a 5 años (" + fuente_c46 + ")" if c46 is None else "faltan los cuartiles del sector (Palancas G14:I14)")
        out["palancas"]["crecimiento_1_5"] = {"NORMAL": None, "MALO": None, "BUENO": None, "referencia_no_disponible_motivo": motivo,
                                              "anclas_usadas": {"cagr_5": c46, "sector_q1": q1, "sector_q3": q3}}
    else:
        s, snota = sigma(serie_tasas, 4, sigma_def)
        n_ref = min(max(c46, q1), q3)
        if etapa == "En declive":
            n_ref = min(n_ref, 0.0)
            nota.append("«En declive»: NORMAL_ref ≤ 0")
        m_ref = min(n_ref, max(min(q1, n_ref - s), suelo_malo))
        candidatos_b = [n_ref + s, q3] + ([1.5 * c46] if c46 > 0 else [])
        b_ref = max(n_ref, min(candidatos_b))
        m_ref, n_ref, b_ref = redondear(m_ref, red["crecimiento"]), redondear(n_ref, red["crecimiento"]), redondear(b_ref, red["crecimiento"])
        m_ref, n_ref, b_ref = orden(m_ref, n_ref, b_ref, nota)
        out["palancas"]["crecimiento_1_5"] = {"NORMAL": n_ref, "MALO": m_ref, "BUENO": b_ref, "referencia_no_disponible_motivo": None,
                                              "regla": "NORMAL = CAGR 5a acotado a [Q1, Q3]; MALO = mín(NORMAL, máx(mín(Q1, NORMAL − σ), −0,10)); BUENO = máx(NORMAL, mín(NORMAL + σ, Q3, 1,5 × CAGR))",
                                              "anclas_usadas": {"cagr_5": c46, "fuente": fuente_c46, "sector_q1": q1, "sector_mediana": num(sec.get("crecimiento_mediana")), "sector_q3": q3, "sigma": s, "sigma_nota": snota},
                                              "criterio_relacionado": "E4 (el pasado predice mal); I1 (el crecimiento se paga con reinversión)", "notas": nota}

    # ---------- margen objetivo año 5 (ROE en C) ----------
    nota = []
    if motor == "C":
        roe = [num(x) for x in ser.get("roe", []) if num(x) is not None]
        m0 = num(anc.get("roe_ultimo")) if base_margen != "Media del ciclo" else num(anc.get("roe_medio_5"))
        media, mn, mx = (statistics.mean(roe) if roe else None), (min(roe) if roe else None), (max(roe) if roe else None)
        q3m = None
        fuente = "Historia!C60 / C56 y la fila 34 (ROE)"
    else:
        m0 = num(anc.get("margen_ultimo")) if base_margen != "Media del ciclo" else num(anc.get("margen_medio"))
        media, mn, mx = num(anc.get("margen_medio")), num(anc.get("margen_min")), num(anc.get("margen_max"))
        q3m = num(sec.get("margen_q3"))
        fuente = "Historia!C48 / C49 (según Palancas!C8), C50, C51 y Sector Q3"
    if m0 is None:
        out["palancas"]["margen_objetivo"] = {"NORMAL": None, "MALO": None, "BUENO": None, "referencia_no_disponible_motivo": "no disponible: la base del margen (m0) no es un número (menos de un ejercicio con margen)",
                                             "anclas_usadas": {"m0": m0, "fuente": fuente}}
    else:
        n_ref = m0
        m_ref = max(min(m0, media if media is not None else m0), mn if mn is not None else m0)
        if mx is not None and abs(m0 - mx) < 1e-12:
            b_ref = m0
        else:
            cands = [x for x in (mx, q3m) if x is not None]
            b_ref = max(m0, min(cands)) if cands else m0
        m_ref, n_ref, b_ref = (redondear(m_ref, red["margen"]), redondear(n_ref, red["margen"]), redondear(b_ref, red["margen"]))
        m_ref, n_ref, b_ref = orden(m_ref, n_ref, b_ref, nota)
        out["palancas"]["margen_objetivo"] = {"NORMAL": n_ref, "MALO": m_ref, "BUENO": b_ref, "referencia_no_disponible_motivo": None,
                                             "regla": "NORMAL = m0 (último año o media del ciclo según C8); MALO = máx(mín(m0, media), mínimo); BUENO = máx(m0, mín(máximo histórico, Q3 sector)); si m0 ya es el máximo, BUENO = m0",
                                             "anclas_usadas": {"m0": m0, "base": base_margen, "media": media, "min": mn, "max": mx, "sector_q3": q3m, "fuente": fuente},
                                             "criterio_relacionado": "E2 (la competencia muerde los márgenes); E5 (cíclicas); E7 (comprobar contra la historia)", "notas": nota}

    # ---------- S2C marginal (A, B) ----------
    nota = []
    c55 = num(anc.get("roic_medio_5"))
    if motor == "C":
        out["palancas"]["s2c"] = {"NORMAL": None, "MALO": None, "BUENO": None, "referencia_no_disponible_motivo": "no aplica en el motor C (B16:D16 se dejan vacías)", "anclas_usadas": {}}
    else:
        c53 = num(anc.get("s2c_marginal"))
        if c53 is None or c53 <= 0:
            out["palancas"]["s2c"] = {"NORMAL": None, "MALO": None, "BUENO": None,
                                      "referencia_no_disponible_motivo": "no disponible: Historia!C53 (S2C marginal 5 años) no es un número > 0 (reinversión neta acumulada ≤ 0 o datos insuficientes). No se sustituye por el S2C medio del sector, que es otra medida",
                                      "anclas_usadas": {"s2c_marginal_C53": c53, "s2c_medio_sector_mediana_solo_contexto": num(sec.get("s2c_medio_mediana"))}}
        else:
            mref = out["palancas"]["margen_objetivo"]
            def con_tope(s2c, margen):
                if c55 is None or t is None or margen is None:
                    nota.append("tope de rentabilidad marginal no aplicado (faltan C55, C52 o el margen de referencia)")
                    return s2c
                rm_ = s2c * margen * (1 - t)
                if rm_ > tope_rm * c55:
                    nota.append(f"S2C reducido para que la rentabilidad marginal no supere {tope_rm}× el ROIC histórico ({tope_rm * c55:.4f})")
                    return (tope_rm * c55) / (margen * (1 - t)) if margen * (1 - t) > 0 else s2c
                return s2c
            n_ref = con_tope(c53, mref.get("NORMAL"))
            m_ref = 0.75 * n_ref
            b_ref = con_tope(1.25 * n_ref, mref.get("BUENO"))
            m_ref, n_ref, b_ref = redondear(m_ref, red["s2c"]), redondear(n_ref, red["s2c"]), redondear(b_ref, red["s2c"])
            m_ref, n_ref, b_ref = orden(m_ref, n_ref, b_ref, nota)
            out["palancas"]["s2c"] = {"NORMAL": n_ref, "MALO": m_ref, "BUENO": b_ref, "referencia_no_disponible_motivo": None,
                                      "regla": "NORMAL = Historia!C53 con tope (rentabilidad marginal ≤ 2× ROIC histórico); MALO = 0,75 × NORMAL; BUENO = 1,25 × NORMAL con el mismo tope",
                                      "anclas_usadas": {"s2c_marginal_C53": c53, "roic_medio_5_C55": c55, "tipo_impositivo_C52": t},
                                      "criterio_relacionado": "I1 (reinversión = Δventas ÷ S2C); la banda ±25 % es convención del ejercicio", "notas": nota}

    # ---------- g para siempre ----------
    nota = []
    base = min(g_sin_rf, rf) if rf is not None else g_sin_rf
    if rf is None:
        nota.append(f"sin tasa sin riesgo (Análisis!C57): {g_sin_rf} por convención")
    n_ref = ajustar_lista(base)
    if etapa == "En declive":
        n_ref = min(n_ref, 0.01)
        nota.append("«En declive»: NORMAL_ref ≤ 0,01")
    m_ref = ajustar_lista(max(n_ref - 0.01, 0))
    b_cands = [n_ref + 0.005, 0.03] + ([rf] if rf is not None else [])
    b_ref = ajustar_lista(min(b_cands))
    if tasa is not None:
        for nombre in ("m_ref", "n_ref", "b_ref"):
            v = locals()[nombre]
            if v >= tasa:
                nota.append(f"{nombre} = {v} ≥ tasa del motor {tasa}: se baja al mayor valor de la lista por debajo (N1)")
        abajo = [x for x in LISTA_G if x < tasa]
        tope = max(abajo) if abajo else 0
        m_ref, n_ref, b_ref = min(m_ref, tope), min(n_ref, tope), min(b_ref, tope)
    m_ref, n_ref, b_ref = orden(m_ref, n_ref, b_ref, nota)
    out["palancas"]["g_perpetuo"] = {"NORMAL": n_ref, "MALO": m_ref, "BUENO": b_ref, "referencia_no_disponible_motivo": None,
                                     "regla": "NORMAL = mín(0,025; rf) ajustado a la lista; MALO = NORMAL − 0,01 (suelo 0); BUENO = mín(NORMAL + 0,005; rf; 0,03); siempre < tasa del motor",
                                     "anclas_usadas": {"rf_C57": rf, "tasa_del_motor": tasa, "etapa_C5": etapa},
                                     "criterio_relacionado": "E1 (g estable ≤ rf, orientación); N1 (g < tasa del motor)", "notas": nota}

    # ---------- ROIC largo plazo (ROE en C) ----------
    nota = []
    if tasa is None:
        out["palancas"]["roic_lp"] = {"NORMAL": None, "MALO": None, "BUENO": None, "referencia_no_disponible_motivo": "no disponible: falta la tasa del motor (Análisis!C56 o Diagnóstico V6!C15)", "anclas_usadas": {}}
    else:
        hist = num(anc.get("roe_medio_5")) if motor == "C" else c55
        c56a = num(an.get("C56"))
        n_ref = m_ref = tasa
        if hist is None:
            b_ref, motivo_b = None, "BUENO no disponible: faltan cinco ejercicios con ROIC (Historia!C55)" if motor != "C" else "BUENO no disponible: faltan cinco ejercicios con ROE (Historia!C56)"
        else:
            cands = [hist] + ([c56a + tope_roic] if c56a is not None else [])
            b_ref = min(cands)
            if hist < tasa:
                b_ref = tasa
                nota.append("ROIC histórico < tasa del motor: BUENO_ref = tasa")
            motivo_b = None
        m_ref, n_ref, b_ref = redondear(m_ref, red["roic"]), redondear(n_ref, red["roic"]), redondear(b_ref, red["roic"])
        m_ref, n_ref, b_ref = orden(m_ref, n_ref, b_ref, nota)
        g_max = max(x for x in (out["palancas"]["g_perpetuo"]["MALO"], out["palancas"]["g_perpetuo"]["NORMAL"], out["palancas"]["g_perpetuo"]["BUENO"]) if x is not None)
        if n_ref is not None and n_ref <= g_max:
            nota.append(f"tasa del motor {tasa} ≤ g_ref {g_max}: ROIC_ref ≤ g (N2); la fase B tiene que resolverlo")
        out["palancas"]["roic_lp"] = {"NORMAL": n_ref, "MALO": m_ref, "BUENO": b_ref, "referencia_no_disponible_motivo": motivo_b,
                                      "regla": "NORMAL = MALO = tasa del motor (convención: sin retornos en exceso a perpetuidad como caso neutro; no una ley); BUENO = mín(ROIC medio 5a, Análisis!C56 + 0,10), y la tasa si el histórico es menor",
                                      "anclas_usadas": {"tasa_del_motor": tasa, "roic_hist": hist, "C56": c56a, "sector_roic_media_H18_solo_contexto": num(sec.get("roic_media"))},
                                      "criterio_relacionado": "E2, E3; I2 (reinversión terminal g ÷ ROIC); el tope sobre la tasa es config referencias_mecanicas.roic_lp_bueno_tope_sobre_c56 (0,03 desde v2.1, MR pp. 62–63)", "notas": nota}

    # ---------- probabilidades, quiebra, exceso de caja, mercado ----------
    out["palancas"]["probabilidades"] = {"NORMAL": p_ref["NORMAL"], "MALO": p_ref["MALO"], "BUENO": p_ref["BUENO"], "referencia_no_disponible_motivo": None,
                                         "regla": "0,2 / 0,6 / 0,2 (convención del ejercicio, S-6)", "criterio_relacionado": "E6 (suman 1 si cubren el rango)"}
    disparadores = []
    c33, c34 = num(an.get("C33")), an.get("C34")
    if c33 is not None and c33 > disp.get("deuda_neta_ebitda_mayor_que", 4):
        disparadores.append(f"Análisis!C33 = {c33} > {disp.get('deuda_neta_ebitda_mayor_que', 4)}")
    if disp.get("caja_no_cubre_deuda_corto", True) and c34 == "No":
        disparadores.append("Análisis!C34 = No (la caja no cubre la deuda a corto)")
    if disp.get("etapa_joven", True) and etapa == "Joven (sin beneficios estables)":
        disparadores.append("Palancas!C5 = Joven")
    c64, c52 = num(anc.get("deuda_mas_arr")), num(an.get("C52"))
    if c64 is not None and c52 is not None and c64 > 0 and (c52 <= 0 or c64 > disp.get("deuda_mas_arrendamientos_sobre_fcf_base_mayor_que", 3) * c52):
        # con FCF base ≤ 0 cualquier deuda positiva supera 3 × FCF base: el disparador también salta
        disparadores.append(f"deuda + arrendamientos (Historia!C64 = {c64}) > {disp.get('deuda_mas_arrendamientos_sobre_fcf_base_mayor_que', 3)} × FCF base ({c52})" + (" (FCF base ≤ 0)" if c52 <= 0 else ""))
    out["palancas"]["quiebra"] = {"C22": quiebra_ref if disparadores else None, "C23": 0 if disparadores else None, "disparadores": disparadores,
                                  "regla": "vacío (= 0) salvo disparador; con disparador 0,05 como convención y obligación de argumentar; C23 = 0",
                                  "criterio_relacionado": "E6 (no contar el riesgo dos veces)"}
    out["palancas"]["exceso_caja"] = {"C76": 0 if motor == "A" else None, "regla": "0 salvo evidencia (regla del inversor v1.2); vacío en B y C"}
    out["palancas"]["mercado"] = {"C24": None, "referencia_no_disponible_motivo": "solo con cifra de fuente primaria en los extractos"}

    # ---------- rentabilidad marginal implícita y salto del año 11 con las referencias ----------
    impl = {}
    for esc in ("MALO", "NORMAL", "BUENO"):
        s2c = out["palancas"]["s2c"].get(esc)
        m = out["palancas"]["margen_objetivo"].get(esc)
        r_lp = out["palancas"]["roic_lp"].get(esc)
        if s2c is not None and m is not None and t is not None:
            rmarg = s2c * m * (1 - t)
            impl[esc] = {"rentabilidad_marginal": rmarg, "roic_lp_ref": r_lp, "salto_anio_11": (rmarg - r_lp) if r_lp is not None else None}
        else:
            impl[esc] = {"rentabilidad_marginal": None, "roic_lp_ref": r_lp, "salto_anio_11": None}
    out["implicaciones_con_referencias"] = impl
    return out


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        return 2
    d = json.load(open(sys.argv[1], encoding="utf-8"))
    cfg = json.load(open(sys.argv[2], encoding="utf-8"))
    out = calcular(d, cfg)
    json.dump(out, open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("OK:", {k: (v.get("MALO"), v.get("NORMAL"), v.get("BUENO")) for k, v in out["palancas"].items() if "NORMAL" in v})
    return 0


if __name__ == "__main__":
    sys.exit(main())
