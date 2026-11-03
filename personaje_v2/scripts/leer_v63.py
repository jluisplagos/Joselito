#!/usr/bin/env python3
"""Lectura de un libro V6.3 RECALCULADO (copia de recalc/, con valores) para los scripts del v2.

Todo se lee con openpyxl data_only=True. Las funciones devuelven diccionarios JSON-serializables.
Las direcciones de celda están tomadas de la plantilla V6.3 (volcado del 30-oct-2026); si la plantilla
cambia, cambian aquí (y se anota en DECISIONES.md).
"""
import datetime as _dt

import openpyxl
from openpyxl.utils import get_column_letter

ANIOS_COLS = [get_column_letter(c) for c in range(3, 13)]  # C..L (Historia)


def _v(x):
    if isinstance(x, (_dt.datetime, _dt.date)):
        return x.isoformat()[:10]
    return x


def abrir(path):
    return openpyxl.load_workbook(path, data_only=True)


def celda(wb, hoja, ref):
    return _v(wb[hoja][ref].value)


def rango(wb, hoja, ref):
    ws = wb[hoja]
    return [[_v(c.value) for c in fila] for fila in ws[ref]]


def num(x):
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None


# ---------------- Historia ----------------
FILAS_HISTORIA = {
    5: "anio", 6: "ventas", 7: "ebit", 8: "da", 9: "beneficio_neto", 10: "tipo_impositivo", 11: "cfo", 12: "capex",
    13: "adquisiciones", 14: "circulante", 15: "intereses", 16: "intereses_financiacion", 17: "arrendamientos_principal",
    18: "sbc", 19: "id", 20: "acciones_diluidas", 21: "patrimonio", 22: "deuda", 23: "arrendamientos", 24: "caja",
    25: "pensiones", 26: "minoritarios",
}
SERIES_HISTORIA = {28: "crecimiento_ventas", 29: "margen_ebit", 30: "reinversion_neta_organica", 31: "reinversion_neta_total",
                   32: "capital_invertido", 33: "roic", 34: "roe", 35: "fcf_accionista", 38: "roic_con_id"}
ANCLAS = {
    "C43": "anios_con_ventas", "C44": "ventas_ultimo", "C45": "cagr_3", "C46": "cagr_5", "C47": "cagr_serie", "C48": "margen_ultimo",
    "C49": "margen_medio", "C50": "margen_min", "C51": "margen_max", "C52": "tipo_impositivo_5", "C53": "s2c_marginal",
    "C54": "s2c_medio", "C55": "roic_medio_5", "C56": "roe_medio_5", "C57": "anios_fcf_base", "C58": "f", "C59": "patrimonio_ultimo",
    "C60": "roe_ultimo", "C61": "beneficio_ultimo", "C62": "ebitda_ultimo", "C63": "coste_deuda", "C64": "deuda_mas_arr",
    "C65": "pensiones_mas_minor", "C66": "caja_ultimo",
}


def historia(wb):
    ws = wb["Historia"]
    out = {"partidas": {}, "series": {}, "anclas": {}, "notas": {}}
    for fila, nombre in FILAS_HISTORIA.items():
        out["partidas"][nombre] = [_v(ws[f"{c}{fila}"].value) for c in ANIOS_COLS]
        out["notas"][nombre] = _v(ws[f"M{fila}"].value)
    for fila, nombre in SERIES_HISTORIA.items():
        out["series"][nombre] = [_v(ws[f"{c}{fila}"].value) for c in ANIOS_COLS]
    for ref, nombre in ANCLAS.items():
        out["anclas"][nombre] = _v(ws[ref].value)
        out["anclas"][ref] = out["anclas"][nombre]
    return out


# ---------------- Palancas (anclas y cuartiles) ----------------
def palancas(wb):
    ws = wb["Palancas"]
    g = lambda r: _v(ws[r].value)  # noqa: E731
    return {
        "C5": g("C5"), "C6": g("C6"), "C7": g("C7"), "C8": g("C8"), "C9": g("C9"), "C10": g("C10"),
        "B14": g("B14"), "C14": g("C14"), "D14": g("D14"), "B15": g("B15"), "C15": g("C15"), "D15": g("D15"),
        "B16": g("B16"), "C16": g("C16"), "D16": g("D16"), "B17": g("B17"), "C17": g("C17"), "D17": g("D17"),
        "B18": g("B18"), "C18": g("C18"), "D18": g("D18"), "C22": g("C22"), "C23": g("C23"), "C24": g("C24"),
        "etiquetas": {"fila14": g("A14"), "fila15": g("A15"), "fila16": g("A16"), "fila18": g("A18")},
        "media_propia": {"crecimiento": g("F14"), "margen": g("F15"), "s2c_marginal": g("F16"), "roic": g("F18"), "s2c_medio": g("F19")},
        "sector": {"crecimiento_q1": g("G14"), "crecimiento_mediana": g("H14"), "crecimiento_q3": g("I14"),
                   "margen_q1": g("G15"), "margen_mediana": g("H15"), "margen_q3": g("I15"),
                   "roic_media": g("H18"), "s2c_medio_q1": g("G19"), "s2c_medio_mediana": g("H19"), "s2c_medio_q3": g("I19"),
                   "g_pista_min": g("G17"), "g_pista_max": g("I17")},
        "geografia": [[g(f"A{r}"), g(f"B{r}"), g(f"C{r}"), g(f"D{r}")] for r in range(28, 34)],
        "predicciones": [[g(f"A{r}"), g(f"B{r}"), g(f"C{r}"), g(f"D{r}")] for r in range(38, 41)],
        "C43": g("C43"), "C44": g("C44"), "C45": g("C45"), "C46": g("C46"), "C47": g("C47"), "C48": g("C48"),
    }


# ---------------- Análisis ----------------
CELDAS_ANALISIS = ["B3", "D3", "B4", "D4", "C7", "D7", "A6", "C11", "C12", "C13", "C14", "C17", "C18", "C19", "C20", "C24", "C25", "C26",
                   "C27", "C28", "C31", "C32", "C33", "C34", "C37", "C38", "C39", "C40", "C41", "C42", "C46", "C47", "C48", "C49", "C50",
                   "C51", "C52", "C53", "C54", "C55", "C56", "C57", "C59", "C60", "C61", "C62", "B65", "C65", "D65", "B66", "C66", "D66",
                   "B67", "C67", "D67", "B68", "C68", "D68", "B69", "C69", "D69", "C76", "B78", "C78", "D78", "C83", "C84", "C85", "C86",
                   "C87", "C88", "C93", "C96", "C97", "C98", "B101", "B102", "C103", "C104"]


def analisis(wb):
    ws = wb["Análisis"]
    out = {ref: _v(ws[ref].value) for ref in CELDAS_ANALISIS}
    out["veredictos"] = {f"D{r}": _v(ws[f"D{r}"].value) for r in list(range(11, 15)) + list(range(17, 21)) + list(range(24, 29)) + list(range(31, 35)) + [84, 85, 86, 93]}
    out["tabla_dcf_inverso"] = [[num(ws[f"A{r}"].value), num(ws[f"B{r}"].value)] for r in range(108, 189)]
    return out


# ---------------- Diagnóstico V6 ----------------
def diagnostico(wb):
    ws = wb["Diagnóstico V6"]
    g = lambda r: _v(ws[r].value)  # noqa: E731
    return {
        "motor": g("C5"), "coherencia_tipo_motor": g("C6"), "V0": g("C9"), "m0": g("C10"), "t": g("C11"), "f": g("C12"),
        "B0": g("C13"), "roe0": g("C14"), "r_operativa": g("C15"), "pasivos_netos_B": g("C16"), "r_minima": g("C17"), "r_vs_minima": g("C18"),
        "por_escenario": {"ventas_anio_10": [g("B22"), g("C22"), g("D22")], "fcf_anio_1": [g("B23"), g("C23"), g("D23")], "fcf_anio_10": [g("B24"), g("C24"), g("D24")],
                          "crecimiento_fcf_implicito": [g("B25"), g("C25"), g("D25")], "valor_anios_1_10": [g("B26"), g("C26"), g("D26")],
                          "valor_para_siempre": [g("B27"), g("C27"), g("D27")], "peso_terminal": [g("B28"), g("C28"), g("D28")],
                          "ajuste": [g("B29"), g("C29"), g("D29")], "valor_antes_quiebra": [g("B30"), g("C30"), g("D30")],
                          "valor_final": [g("B31"), g("C31"), g("D31")], "valor_por_accion": [g("B32"), g("C32"), g("D32")],
                          "valor_sin_crecimiento": [g("B33"), g("C33"), g("D33")], "valor_del_crecimiento": [g("B34"), g("C34"), g("D34")],
                          "roic_marginal_implicito": [g("B35"), g("C35"), g("D35")], "cuota_implicita": [g("B36"), g("C36"), g("D36")]},
        "semaforos": {f"fila{r}": [g(f"A{r}"), g(f"B{r}"), g(f"C{r}"), g(f"D{r}")] for r in range(40, 51)},
        "cuanto_pagas_por_crecer": [[g(f"A{r}"), g(f"B{r}"), g(f"C{r}"), g(f"D{r}")] for r in range(53, 58)],
        "multiplos": [[g(f"A{r}"), g(f"B{r}"), g(f"C{r}"), g(f"D{r}"), g(f"E{r}")] for r in range(61, 66)],
        "autocomprobaciones": [[g(f"A{r}"), g(f"B{r}")] for r in range(69, 85)],
        "parametros": {"C91": g("C91"), "C92": g("C92"), "C93": g("C93"), "C94": g("C94"), "C156": g("C156"), "C158": g("C158"), "C179": g("C179")},
        "causas_activas": [g(f"A{r}") for r in range(161, 173) if g(f"A{r}")],
        "salto_anio_11": {"filas": [[g(f"A{r}"), g(f"B{r}"), g(f"C{r}"), g(f"D{r}")] for r in range(174, 181)]},
        "tornado": {"rotulos": [g(f"A{r}") for r in range(215, 221)], "efectos": [[g(f"B{r}"), g(f"C{r}")] for r in range(215, 221)],
                    "mas_influyente": g("C221"), "B222": g("B222"), "B223": g("B223")},
        "precio_referencia_hoja": g("C156"),
    }


# ---------------- Motor ----------------
def motor(wb):
    ws = wb["Motor"]
    g = lambda r: _v(ws[r].value)  # noqa: E731
    reglas = []
    for r in range(201, 250):
        rid = g(f"A{r}")
        if not rid:
            continue
        reglas.append({"id": rid, "regla": g(f"B{r}"), "aplica": g(f"C{r}"), "resultado": g(f"D{r}"), "codigo": g(f"E{r}"),
                       "causa": g(f"F{r}"), "nivel": g(f"G{r}"), "prioridad": g(f"H{r}"), "n_causa_activa": g(f"I{r}")})
    return {"bloqueo_valor_B252": g("B252"), "comparable_B253": g("B253"), "bloqueo_lectura_B254": g("B254"),
            "estado_tecnico_B255": g("B255"), "causa_tecnica_B256": g("B256"), "estado_inversion_B258": g("B258"),
            "n_avisos_B260": g("B260"), "n_causas_B261": g("B261"), "estado_libro_B266": g("B266"), "lectura_precio_B267": g("B267"),
            "veredicto_B268": g("B268"), "evidencias_B269": g("B269"), "dcf_inverso_monotono_B193": g("B193"), "reglas": reglas}


# ---------------- Control maestro ----------------
def control_maestro(wb):
    ws = wb["Control maestro"]
    g = lambda r: _v(ws[r].value)  # noqa: E731
    filas = {}
    for r in range(17, 176):
        cel = g(f"B{r}")
        if not cel:
            continue
        filas[r] = {"celda": cel, "concepto": g(f"C{r}"), "naturaleza": g(f"D{r}"), "E": g(f"E{r}"), "F": g(f"F{r}"), "periodo": g(f"G{r}"),
                    "unidad": g(f"H{r}"), "tipo_fuente": g(f"I{r}"), "J": g(f"J{r}"), "K": g(f"K{r}"), "L": g(f"L{r}"), "M": g(f"M{r}"), "N": g(f"N{r}")}
    inventario = []
    for r in range(179, 237):
        cel = g(f"B{r}")
        if not cel:
            continue
        inventario.append({"fila_cm": g(f"A{r}"), "celda": cel, "concepto": g(f"C{r}"), "tipo": g(f"D{r}"), "motores": g(f"E{r}"),
                           "aplica": g(f"F{r}"), "condicion": g(f"G{r}"), "clasificacion": g(f"I{r}"), "documento": g(f"J{r}"),
                           "justificada": g(f"K{r}"), "estado_evidencia": g(f"L{r}")})
    cabecera = {"H4_moneda": g("H4"), "J4_unidad": g("J4"), "L4_norma": g("L4"), "N4_cierre": g("N4"), "B5_mercado": g("B5"),
                "D5_ratio_adr": g("D5"), "F5_periodo": g("F5"), "J5_fx": g("J5"), "L5_revision": g("L5"), "N5_responsable": g("N5")}
    resumen = {f"D{r}": g(f"D{r}") for r in range(240, 251)}
    return {"cabecera": cabecera, "filas": filas, "inventario": inventario, "resumen": resumen}


def todo(wb):
    return {"analisis": analisis(wb), "palancas": palancas(wb), "diagnostico": diagnostico(wb), "historia": historia(wb),
            "motor": motor(wb), "control_maestro": control_maestro(wb)}


if __name__ == "__main__":
    import json
    import sys
    wb = abrir(sys.argv[1])
    print(json.dumps(todo(wb), ensure_ascii=False, indent=1, default=str)[:3000])
