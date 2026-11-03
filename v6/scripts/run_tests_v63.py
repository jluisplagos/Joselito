#!/usr/bin/env python3
"""Batería de pruebas de la V6.3 con recálculo real (LibreOffice headless).

Uso: python3 run_tests_v63.py carpeta_entregables carpeta_salida [--referencia referencia_V6.3.json]
     carpeta_entregables debe contener Plantilla_V6.3.xlsx, Ejemplo_V6.3_EmpresaX.xlsx,
     Ejemplo_ABB_V6.3.xlsx y Ejemplo_migracion_Hermes_V6.3.xlsx.
Dependencias: openpyxl >= 3.1 y `soffice` en el PATH. Sin rutas personales.

Cada caso declara su resultado ESPERADO antes de ejecutarse. La carpeta de salida se vacía al
empezar: no se reutilizan recálculos antiguos. Una prueba cuyo archivo recalculado no aparece se
registra como NO EJECUTADA, nunca como superada. Código de salida 1 si alguna falla.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

AN, HI, PA, DI, MO, PN, CM, GU = ("Análisis", "Historia", "Palancas", "Diagnóstico V6",
                                  "Motor", "Panel", "Control maestro", "Guía V6")
MOT = {"A": "Sí", "B": "No · financiación cambia mucho", "C": "No · banco o aseguradora",
       "C_orig": "No · banco, aseguradora o regulada"}
REF = {"A": 25.8903521530386, "B": 30.7047681225928,
       "C_palancas_A": 17.8908417408599, "C_orig": 11.89975227122322}
REF78 = {"A": (15.1023915686987, 25.0689493251303, 39.1425212211033),
         "B": (17.3539528333579, 29.7144295704154, 47.0265990683598),
         "C_palancas_A": (10.9505167042730, 17.2492128342923, 26.7560534971496),
         "C_orig": (8.336252583141702, 11.977714961759025, 15.229363887697314)}

# --------------------------------------------------------------- comprobadores
def vacio():            return ("sin valor", lambda v: v in (None, ""))
def igual(x, tol=1e-9): return (f"{x:.10f}", lambda v: isinstance(v, (int, float)) and abs(v - x) <= tol)
def num():              return ("un número", lambda v: isinstance(v, (int, float)))
def es(t):              return (repr(t), lambda v: v == t)
def contiene(t):        return (f"contiene «{t}»", lambda v: isinstance(v, str) and t in v)
def no_contiene(t):     return (f"no contiene «{t}»", lambda v: not (isinstance(v, str) and t in v))
def empieza(t):         return (f"empieza por «{t}»", lambda v: isinstance(v, str) and v.startswith(t))
def texto_legible():    return ("texto, no un error", lambda v: isinstance(v, str) and v != "" and not v.startswith("#"))

CASOS = []
def caso(nombre, familia, base, mut, checks, motor=None):
    CASOS.append(dict(nombre=nombre, familia=familia, base=base, motor=motor, mut=mut, checks=checks))

def fila(h, f, cols="CDEFGHIJKL"):
    return {f"{h}!{c}{f}": None for c in cols}

def sin_errores_inesperados(wb):
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and c.value.startswith("#") and c.value != "#N/A":
                    return False
    return True
SIN_ERR = ("sin #VALUE!/#REF!/#DIV/0!/#NAME? (los #N/A de Motor!B141:E169 son los huecos de gráfico)", sin_errores_inesperados)

def receta_evidencias(wb, f43="Dato no verificable"):
    cm = wb[CM]
    for r in range(17, 120):
        d = cm.cell(r, 4).value
        if isinstance(d, str) and "dato" in d.lower():
            cm.cell(r, 10).value = "Documento de prueba"
            cm.cell(r, 6).value = f43 if r == 43 else "Rellenado y verificado"
    for r in (124, 126):
        cm.cell(r, 10).value = None; cm.cell(r, 6).value = None

import relacion_entradas_materiales as REL  # relación independiente (traza + activación empírica)

def completar(wb, motor, excepto=()):
    """Documenta todos los DATOS activos y confirma todas las HIPÓTESIS activas del motor, según la
    relación independiente. No lee el inventario de Control maestro."""
    cm = wb[CM]
    # Synthetic fixture only: the accounting standard must be present too.
    if cm["L4"].value in (None, ""): cm["L4"] = "IFRS"
    ins = REL.leer_ins(wb)
    for e in REL.activas(motor, ins):
        if e["id"] in excepto:
            continue
        t = e["fila"]
        if e["tipo"] == "dato":
            cm.cell(t, 6).value = "Rellenado y verificado"; cm.cell(t, 10).value = "Documento ficticio de prueba"
        else:
            cm.cell(t, 6).value = "Hipótesis confirmada"; cm.cell(t, 13).value = "Razonamiento ficticio de prueba"

def solo_datos(wb, motor):
    cm = wb[CM]; ins = REL.leer_ins(wb)
    for e in REL.activas(motor, ins):
        if e["tipo"] == "dato":
            cm.cell(e["fila"], 6).value = "Rellenado y verificado"; cm.cell(e["fila"], 10).value = "Documento ficticio de prueba"

def documentar_B(wb): completar(wb, "B")
def documentar_A(wb): completar(wb, "A")

def palancas_C_orig(wb):
    pa = wb[PA]
    for col, (g, m, ro) in zip("BCD", ((0.03, 0.10, 0.10), (0.06, 0.14, 0.13), (0.08, 0.16, 0.15))):
        pa[f"{col}14"] = g; pa[f"{col}15"] = m; pa[f"{col}16"] = "n/a"; pa[f"{col}18"] = ro

EX, TPL, ABB, HER = "EmpresaX", "Plantilla", "ABB", "Hermes"

# ===================== 1 · tres fallos nuevos (revisión externa sobre la V6.2)
caso("N1_evidencias_receta_motorB", "1 · fallos nuevos", EX, receta_evidencias,
     {f"{MO}!B269": empieza("INCOMPLETAS"), f"{MO}!B266": empieza("NO LISTO · evidencias incompletas"),
      f"{AN}!C83": igual(REF["B"])}, motor="B")
caso("N1_evidencias_receta_motorA", "1 · fallos nuevos", EX, receta_evidencias,
     {f"{MO}!B269": contiene("1 no verificables"), f"{MO}!B266": empieza("NO LISTO · evidencias incompletas")}, motor="A")
caso("N1_solo_datos_documentados_B_no_basta", "1 · fallos nuevos", EX, lambda wb: solo_datos(wb, "B"),
     {f"{MO}!B269": contiene("hipótesis confirmadas 0 de 22"), f"{MO}!B266": empieza("NO LISTO")}, motor="B")
caso("N1_datos_e_hipotesis_B_LISTO", "1 · fallos nuevos", EX, documentar_B,
     {f"{MO}!B269": empieza("documentadas 17 de 17 · hipótesis confirmadas 22 de 22"), f"{MO}!B266": es("LISTO")}, motor="B")
caso("N1_datos_e_hipotesis_A_LISTO", "1 · fallos nuevos", EX, documentar_A,
     {f"{MO}!B269": empieza("documentadas 19 de 19 · hipótesis confirmadas 24 de 24"), f"{MO}!B266": es("LISTO")}, motor="A")
caso("N1_datos_e_hipotesis_C_LISTO", "1 · fallos nuevos", EX, lambda wb: completar(wb, "C"),
     {f"{MO}!B269": empieza("documentadas 10 de 10 · hipótesis confirmadas 18 de 18"), f"{MO}!B266": es("LISTO"),
      f"{AN}!C83": igual(REF["C_palancas_A"])}, motor="C")
# --- N4 · revisión externa de la cobertura (30-oct): las dos recetas exactas
def receta_B_cobertura(wb):
    cm = wb[CM]
    for t in (38, 41, 52, 107, 108, 109, 112, 117, 124, 125, 126, 127, 128):
        cm.cell(t, 6).value = "Rellenado y verificado"; cm.cell(t, 10).value = "Documento ficticio de prueba"
    cm["F53"] = "Pendiente de inversor"; cm["F146"] = "Pendiente de inversor"
caso("N4_receta_B_r_y_crecimiento_pendientes", "1 · fallos nuevos", EX, receta_B_cobertura,
     {f"{MO}!B266": empieza("NO LISTO · evidencias incompletas"), f"{MO}!B269": empieza("INCOMPLETAS"),
      f"{AN}!C83": igual(REF["B"])}, motor="B")
def receta_A_cobertura(wb):
    cm = wb[CM]
    for t in (38, 41, 52, 43, 44, 45, 46, 48, 107, 108, 109, 110, 112, 114, 116):
        cm.cell(t, 6).value = "Rellenado y verificado"; cm.cell(t, 10).value = "Documento ficticio de prueba"
    wb[AN]["C46"] = 0; wb[PA]["C43"] = "Transitorio"; wb[PA]["C44"] = 200
    cm["F167"] = "Dato no verificable"; cm["J167"] = None
caso("N4_receta_A_FCF_normalizado_no_verificable", "1 · fallos nuevos", EX, receta_A_cobertura,
     {f"{MO}!B266": empieza("NO LISTO · evidencias incompletas"), f"{MO}!B269": contiene("1 no verificables"),
      f"{AN}!C83": igual(53.9956252725454), f"{HI}!C71": contiene("Palancas C44")}, motor="A")
def receta_A_estimacion_justificada(wb):
    wb[AN]["C46"] = 0; wb[PA]["C43"] = "Transitorio"; wb[PA]["C44"] = 200
    completar(wb, "A"); cm = wb[CM]
    cm["F167"] = "Estimación declarada"; cm["M167"] = "Media de los 3 ejercicios anteriores al cierre extraordinario"
caso("N4_receta_A_FCF_normalizado_estimacion_justificada", "1 · fallos nuevos", EX, receta_A_estimacion_justificada,
     {f"{MO}!B266": empieza("LISTO · PROVISIONAL (1 estimaciones"), f"{AN}!C83": igual(53.9956252725454)}, motor="A")
caso("N4_exceso_de_caja_sin_confirmar", "1 · fallos nuevos", EX,
     lambda wb: (wb[AN].__setitem__("C76", 50), completar(wb, "A", excepto=("exceso_caja",))),
     {f"{MO}!B266": empieza("NO LISTO · evidencias incompletas (1 pendientes)"), f"{AN}!C83": igual(REF["A"] + 0.5)}, motor="A")
caso("N4_hipotesis_marcada_como_hecho_es_incoherente", "1 · fallos nuevos", EX,
     lambda wb: (completar(wb, "B"), wb[CM].__setitem__("F53", "Rellenado y verificado"), wb[CM].__setitem__("J53", "doc")),
     {f"{MO}!B266": empieza("NO LISTO · evidencias incompletas (1 pendientes)"),
      f"{CM}!L{179 + [e['id'] for e in REL.ENTRADAS].index('r')}": contiene("incoherente")}, motor="B")
caso("N4_hipotesis_sin_justificar", "1 · fallos nuevos", EX,
     lambda wb: (completar(wb, "B"), wb[CM].__setitem__("M53", None), wb[CM].__setitem__("J53", None), wb[CM].__setitem__("N53", None)),
     {f"{MO}!B266": empieza("NO LISTO · evidencias incompletas (1 pendientes)")}, motor="B")
caso("N1_filas_121_124_restauradas", "1 · fallos nuevos", EX, None,
     {f"{CM}!B122": es("Historia!C20:L20"), f"{CM}!B123": es("Historia!C21:L21"), f"{CM}!B124": es("Historia!C22:L22"),
      f"{CM}!A121": es("Historia"), f"{CM}!C122": es("Acciones diluidas (mm)")})
caso("N2_C58_cero_bloquea", "1 · fallos nuevos", EX, lambda wb: wb[HI].__setitem__("C58", "=0"),
     {f"{AN}!C83": vacio(), f"{MO}!B255": es("DATOS INVÁLIDOS"), f"{MO}!B256": contiene("conciliación de f no cuadra"),
      f"{HI}!C81": contiene("no cuadra")}, motor="A")
caso("N2_C58_formula_falsa_bloquea", "1 · fallos nuevos", EX, lambda wb: wb[HI].__setitem__("C58", "=0.014*1.5"),
     {f"{AN}!C83": vacio(), f"{MO}!B255": es("DATOS INVÁLIDOS")}, motor="A")
caso("N2_conciliacion_no_evaluable_no_bloquea", "1 · fallos nuevos", EX, fila(HI, 8),
     {f"{HI}!C81": es("—"), f"{MO}!B255": es("INCOMPLETO"), f"{MO}!B256": no_contiene("conciliación")}, motor="A")
caso("N3_L22_deuda_negativa", "1 · fallos nuevos", EX, {f"{HI}!L22": -200},
     {f"{AN}!C83": vacio(), f"{MO}!B255": es("DATOS INVÁLIDOS"), f"{MO}!B256": contiene("deuda BRUTA")}, motor="B")
caso("N3_L23_arrendamientos_negativos", "1 · fallos nuevos", EX, {f"{HI}!L23": -10},
     {f"{AN}!C83": vacio(), f"{MO}!B255": es("DATOS INVÁLIDOS")}, motor="B")
caso("N3_L24_caja_negativa", "1 · fallos nuevos", EX, {f"{HI}!L24": -5},
     {f"{AN}!C83": vacio(), f"{MO}!B256": contiene("Caja negativa")}, motor="B")
caso("N3_E12_capex_negativo", "1 · fallos nuevos", EX, {f"{HI}!E12": -3},
     {f"{AN}!C83": vacio(), f"{MO}!B256": contiene("Capex negativo")}, motor="A")
caso("N3_E8_DA_negativa_fuera_de_ventana", "1 · fallos nuevos", EX, {f"{HI}!C8": -1},
     {f"{AN}!C83": vacio(), f"{MO}!B255": es("DATOS INVÁLIDOS")}, motor="A")
caso("N3_circulante_negativo_permitido", "1 · fallos nuevos", EX, {f"{HI}!E14": -3},
     {f"{AN}!C83": num(), f"{MO}!B255": es("COMPLETO Y VÁLIDO")}, motor="A")
caso("N3_adquisiciones_negativas_permitidas", "1 · fallos nuevos", EX, {f"{HI}!E13": -30},
     {f"{AN}!C83": num(), f"{MO}!B255": es("COMPLETO Y VÁLIDO")}, motor="A")
caso("N3_CFO_negativo_permitido", "1 · fallos nuevos", EX, {f"{HI}!C11": -50},
     {f"{MO}!B255": es("COMPLETO Y VÁLIDO")}, motor="A")
caso("N3_superavit_pensiones_es_cero_con_aviso", "1 · fallos nuevos", EX, {f"{HI}!L25": -40},
     {f"{AN}!C83": igual(REF["B"]), f"{HI}!C65": igual(0.0), f"{MO}!B255": es("COMPLETO Y VÁLIDO"),
      "__libro__": ("aviso de superávit de pensiones en las causas activas",
                    lambda wb: any("Superávit de pensiones" in str(wb[MO].cell(r, 2).value) for r in range(271, 283)))}, motor="B")
caso("N3_deficit_pensiones_se_resta", "1 · fallos nuevos", EX, {f"{HI}!L25": 40},
     {f"{AN}!C83": igual(REF["B"] - 0.4), f"{HI}!C65": igual(40.0)}, motor="B")

# ===================== 2 · fallos anteriores
caso("A1_amortizaciones_ausentes", "2 · fallos anteriores", EX, fila(HI, 8),
     {f"{AN}!C83": vacio(), f"{MO}!B255": es("INCOMPLETO"), f"{MO}!B256": contiene("amortizaciones")}, motor="A")
caso("A2_amortizacion_parcial", "2 · fallos anteriores", EX, {f"{HI}!L8": None},
     {f"{AN}!C83": vacio(), f"{MO}!B256": contiene("amortizaciones")}, motor="A")
caso("B1_caja_ausente", "2 · fallos anteriores", EX, {f"{HI}!L24": None},
     {f"{AN}!C83": vacio(), f"{MO}!B256": contiene("caja del último año")}, motor="B")
caso("C1_monedas_distintas_B", "2 · fallos anteriores", EX, {f"{PA}!C48": "USD", f"{CM}!H4": "EUR"},
     {f"{AN}!C83": vacio(), f"{MO}!B255": es("DATOS INVÁLIDOS"), f"{MO}!B256": contiene("pesos de financiación")}, motor="B")
caso("C2_monedas_distintas_A_solo_lectura", "2 · fallos anteriores", EX, {f"{PA}!C48": "USD", f"{CM}!H4": "EUR"},
     {f"{AN}!C83": igual(REF["A"]), f"{AN}!C84": vacio(), f"{MO}!B253": es(False)}, motor="A")
for f_, txt in ((12, "capex"), (14, "circulante")):
    caso(f"A3_fila{f_}_ausente", "2 · fallos anteriores", EX, fila(HI, f_),
         {f"{AN}!C83": vacio(), f"{MO}!B255": es("INCOMPLETO")}, motor="A")
for f_ in (22, 23, 25, 26):
    caso(f"B2_L{f_}_ausente", "2 · fallos anteriores", EX, {f"{HI}!L{f_}": None},
         {f"{AN}!C83": vacio(), f"{MO}!B255": es("INCOMPLETO")}, motor="B")
caso("B3_ceros_explicitos_valen", "2 · fallos anteriores", EX, {f"{HI}!L23": 0, f"{HI}!L25": 0, f"{HI}!L26": 0},
     {f"{AN}!C83": num(), f"{MO}!B255": es("COMPLETO Y VÁLIDO")}, motor="B")
caso("A4_C48_vacio", "2 · fallos anteriores", EX, {f"{AN}!C48": None},
     {f"{AN}!C83": vacio(), f"{MO}!B256": contiene("intereses en financiación")}, motor="A")
caso("A5_C49_vacio", "2 · fallos anteriores", EX, {f"{AN}!C49": None},
     {f"{AN}!C83": vacio(), f"{MO}!B256": contiene("arrendamientos")}, motor="A")

# ===================== 3 · ausencia, cero, estimación, no verificable, filas > 119, No aplicable
def estimacion_justificada(wb):
    documentar_B(wb); cm = wb[CM]
    cm.cell(127, 6).value = "Estimación declarada"; cm.cell(127, 13).value = "Sin déficit material según la nota 14"
caso("E1_estimacion_justificada_provisional", "3 · evidencias", EX, estimacion_justificada,
     {f"{MO}!B266": empieza("LISTO · PROVISIONAL (1 estimaciones"), f"{MO}!B269": empieza("PROVISIONAL"),
      f"{AN}!C83": igual(REF["B"])}, motor="B")
def estimacion_sin_justificar(wb):
    documentar_B(wb); cm = wb[CM]
    cm.cell(127, 6).value = "Estimación declarada"; cm.cell(127, 10).value = None; cm.cell(127, 13).value = None
caso("E2_estimacion_sin_justificar_pendiente", "3 · evidencias", EX, estimacion_sin_justificar,
     {f"{MO}!B266": empieza("NO LISTO · evidencias incompletas (1 pendientes)")}, motor="B")
def no_verificable(wb):
    documentar_B(wb); wb[CM].cell(126, 6).value = "Dato no verificable"
caso("E3_no_verificable_no_es_completa", "3 · evidencias", EX, no_verificable,
     {f"{MO}!B269": contiene("1 no verificables"), f"{MO}!B266": empieza("NO LISTO")}, motor="B")
def no_aplicable_indebido(wb):
    documentar_B(wb); wb[CM].cell(126, 6).value = "No aplicable"
caso("E4_no_aplicable_en_caja_indebido", "3 · evidencias", EX, no_aplicable_indebido,
     {f"{MO}!B269": contiene("1 «No aplicable» indebido"), f"{MO}!B266": empieza("NO LISTO")}, motor="B")
def no_aplicable_legitimo(wb):
    documentar_B(wb); wb[CM].cell(110, 6).value = "No aplicable"   # D&A: el motor B no la usa
caso("E5_no_aplicable_en_entrada_no_usada_ok", "3 · evidencias", EX, no_aplicable_legitimo,
     {f"{MO}!B266": es("LISTO")}, motor="B")
def fuente_pendiente_fila_124(wb):
    documentar_B(wb); wb[CM].cell(124, 10).value = None
caso("E6_fuente_pendiente_fila_124_cuenta", "3 · evidencias", EX, fuente_pendiente_fila_124,
     {f"{MO}!B269": contiene("1 sin clasificar"), f"{MO}!B266": empieza("NO LISTO")}, motor="B")
def hipotesis_pendiente(wb):
    documentar_B(wb); wb[CM].cell(117, 6).value = "Pendiente de inversor"
caso("E7_hipotesis_pendiente_cuenta", "3 · evidencias", EX, hipotesis_pendiente,
     {f"{MO}!B269": contiene("1 hipótesis pendientes")}, motor="B")
def rellenar_otras_no_convierte(wb):
    documentar_B(wb); wb[CM].cell(126, 6).value = "Pendiente de inversor"
    wb[AN]["C97"] = "Sí"; wb[AN]["C98"] = "Buena"; wb[AN]["B101"] = "Tesis de prueba"
caso("E8_rellenar_otras_celdas_no_confirma", "3 · evidencias", EX, rellenar_otras_no_convierte,
     {f"{MO}!B269": contiene("1 hipótesis pendientes")}, motor="B")
caso("E9_sin_motor_sin_entradas_aplicables", "3 · evidencias", TPL, None,
     {f"{MO}!B269": empieza("sin entradas aplicables")})
caso("E10_ABB_conserva_pendientes", "3 · evidencias", ABB, None,
     {f"{AN}!C83": vacio(), f"{MO}!B255": es("INCOMPLETO"), f"{MO}!B256": contiene("Análisis C48, C49"),
      f"{AN}!C49": vacio(), f"{MO}!B269": empieza("INCOMPLETAS")})
caso("E11_ABB_variante_prueba_C49_cero", "3 · evidencias", ABB, {f"{AN}!C49": 0},
     {f"{AN}!C83": igual(37.3528564268176), f"{MO}!B255": es("INCOMPLETO"),
      f"{MO}!B256": contiene("Filtro Pabrai"), f"{HI}!C65": igual(559.0)})
caso("E12_EmpresaX_sigue_ficticia", "3 · evidencias", EX, None,
     {f"{AN}!B3": contiene("inventada"), f"{AN}!C83": igual(REF["A"]), f"{MO}!B266": empieza("NO LISTO · evidencias incompletas"),
      f"{PN}!B3": empieza("Evidencias: INCOMPLETAS")}, motor="A")

# ===================== 4 · plantilla vacía, ausencias parciales y combinaciones
caso("V1_plantilla_vacia", "4 · vacía y combinaciones", TPL, None,
     {f"{AN}!C83": vacio(), f"{MO}!B255": es("INCOMPLETO"), f"{MO}!B256": texto_legible(), "__libro__": SIN_ERR})
caso("V2_A_combinacion_D&A_y_capex", "4 · vacía y combinaciones", EX, {**fila(HI, 8), **fila(HI, 12)},
     {f"{AN}!C83": vacio(), f"{MO}!B256": texto_legible(), "__libro__": SIN_ERR}, motor="A")
caso("V3_A_combinacion_C50_y_B15", "4 · vacía y combinaciones", EX, {f"{AN}!C50": None, f"{PA}!B15": None},
     {f"{AN}!C83": vacio(), f"{MO}!B256": texto_legible(), "__libro__": SIN_ERR}, motor="A")
caso("V4_B_combinacion_caja_deuda_intereses", "4 · vacía y combinaciones", EX, {f"{HI}!L24": None, f"{HI}!L22": None, f"{HI}!L15": None},
     {f"{AN}!C83": vacio(), f"{MO}!B256": texto_legible(), "__libro__": SIN_ERR}, motor="B")
caso("V5_B_combinacion_moneda_y_caja", "4 · vacía y combinaciones", EX, {f"{PA}!C48": None, f"{HI}!L24": None},
     {f"{AN}!C83": vacio(), f"{MO}!B256": texto_legible(), "__libro__": SIN_ERR}, motor="B")
caso("V6_C_combinacion_patrimonio_beneficio", "4 · vacía y combinaciones", EX, {f"{HI}!L21": None, f"{HI}!L9": None},
     {f"{AN}!C83": vacio(), f"{MO}!B256": texto_legible(), "__libro__": SIN_ERR}, motor="C")
caso("V7_C_combinacion_ROE_y_g", "4 · vacía y combinaciones", EX, {f"{PA}!C15": None, f"{AN}!C68": None},
     {f"{AN}!C83": vacio(), f"{MO}!B256": texto_legible(), "__libro__": SIN_ERR}, motor="C")
caso("V8_parcial_tipo_impositivo_un_año", "4 · vacía y combinaciones", EX, {f"{HI}!K10": None},
     {f"{AN}!C83": vacio(), f"{MO}!B255": es("INCOMPLETO"), f"{HI}!C52": vacio()}, motor="A")
caso("V9_texto_en_historia", "4 · vacía y combinaciones", EX, {f"{HI}!L8": "n/d"},
     {f"{AN}!C83": vacio(), f"{MO}!B255": es("DATOS INVÁLIDOS"), "__libro__": SIN_ERR}, motor="A")
caso("V10_C51_fuera_dominio", "4 · vacía y combinaciones", EX, {f"{AN}!C51": "Tal vez"},
     {f"{AN}!C83": vacio(), f"{MO}!B255": es("DATOS INVÁLIDOS")}, motor="A")
for _c in ("B15", "C16", "D18"):
    caso(f"V11_causa_legible_{_c}", "4 · vacía y combinaciones", EX, {f"{PA}!{_c}": None},
         {f"{AN}!C83": vacio(), f"{MO}!B256": texto_legible(), "__libro__": SIN_ERR}, motor="A")

# ===================== 5 · referencias numéricas
caso("R1_motor_A", "5 · referencias", EX, None,
     {f"{AN}!C83": igual(REF["A"]), f"{AN}!B78": igual(REF78["A"][0]), f"{AN}!C78": igual(REF78["A"][1]),
      f"{AN}!D78": igual(REF78["A"][2]), f"{MO}!B255": es("COMPLETO Y VÁLIDO")}, motor="A")
caso("R2_motor_B", "5 · referencias", EX, None,
     {f"{AN}!C83": igual(REF["B"]), f"{AN}!B78": igual(REF78["B"][0]), f"{AN}!C78": igual(REF78["B"][1]),
      f"{AN}!D78": igual(REF78["B"][2])}, motor="B")
caso("R3_motor_C_con_palancas_del_ejemplo_A", "5 · referencias", EX, None,
     {f"{AN}!C83": igual(REF["C_palancas_A"]), f"{AN}!B78": igual(REF78["C_palancas_A"][0]),
      f"{AN}!C78": igual(REF78["C_palancas_A"][1]), f"{AN}!D78": igual(REF78["C_palancas_A"][2])}, motor="C")
caso("R4_motor_C_fixture_original_test_fill", "5 · referencias", EX, palancas_C_orig,
     {f"{AN}!B78": igual(REF78["C_orig"][0], 1e-6), f"{AN}!C78": igual(REF78["C_orig"][1], 1e-6),
      f"{AN}!D78": igual(REF78["C_orig"][2], 1e-6), f"{AN}!C83": igual(REF["C_orig"], 1e-6)}, motor="C_orig")
caso("R5_f_conciliada", "5 · referencias", EX, None,
     {f"{HI}!C58": igual(0.014, 1e-12), f"{HI}!C80": igual(0.014, 1e-12), f"{HI}!C81": contiene("cuadra")}, motor="A")

# ===================== 6 · modo estudio, tasa, probabilidades, lectura de precio
def estudio(on, nivel):
    def f(wb):
        wb[PN]["F6"] = on
        for r in range(20, 26): wb[PN].cell(r, 5).value = nivel
    return f
for m in "ABC":
    for on, niv in (("ON", 0), ("ON", 40), ("OFF", 40)):
        ref = REF["C_palancas_A"] if m == "C" else REF[m]
        caso(f"S1_estudio_{m}_{on}_{niv}", "6 · invariantes", EX, estudio(on, niv),
             {f"{AN}!C83": igual(ref), f"{AN}!C56": igual(0.09)}, motor=m)
caso("S2_tasa_usuario_se_conserva_B", "6 · invariantes", EX, None,
     {f"{AN}!C56": igual(0.09), f"{DI}!C15": igual(0.0839952904238619)}, motor="B")
caso("S3_C15_vacia_fuera_de_B", "6 · invariantes", EX, None, {f"{DI}!C15": es("—"), f"{DI}!C16": es("—")}, motor="A")
caso("S4_probabilidades_fuera", "6 · invariantes", EX, {f"{AN}!B69": -0.1, f"{AN}!C69": 1.1, f"{AN}!D69": 0.0},
     {f"{AN}!C83": vacio(), f"{MO}!B255": es("DATOS INVÁLIDOS")}, motor="A")
caso("S5_ponderado_equiprobable", "6 · invariantes", EX, {f"{AN}!B69": 1/3, f"{AN}!C69": 1/3, f"{AN}!D69": 1/3},
     {"__libro__": ("C83 = media de B78:D78", lambda wb: abs(wb[AN]["C83"].value - sum(wb[AN][c+"78"].value for c in "BCD")/3) < 1e-9)}, motor="A")
caso("S6_quiebra_150", "6 · invariantes", EX, {f"{PA}!C22": 1.5}, {f"{AN}!C83": vacio(), f"{MO}!B255": es("DATOS INVÁLIDOS")}, motor="A")
caso("S7_quiebra_30_recuperacion_sin_descontar", "6 · invariantes", EX, {f"{PA}!C22": 0.30, f"{PA}!C23": 350},
     {f"{AN}!B78": igual(0.7 * REF78["A"][0] + 0.3 * 3.5, 1e-9)}, motor="A")
caso("S8_g_mayor_que_r", "6 · invariantes", EX, {f"{AN}!C68": 0.12, f"{AN}!C56": 0.10}, {f"{AN}!C83": vacio(), f"{MO}!B255": es("DATOS INVÁLIDOS")}, motor="A")
caso("S9_precio_vacio_bloquea_lectura", "6 · invariantes", EX, {f"{AN}!C37": None},
     {f"{AN}!C84": vacio(), f"{DI}!C156": vacio(), f"{PN}!M25": vacio()}, motor="A")
caso("S10_precio_referencia_k", "6 · invariantes", EX, {f"{DI}!C158": 0.5},
     {f"{DI}!C156": igual(min(REF78["A"][0], 0.5 * REF["A"]))}, motor="A")
caso("S11_salidas_dependientes_con_valor_bloqueado", "6 · invariantes", EX, {f"{HI}!L24": None},
     {f"{AN}!C84": vacio(), f"{AN}!C86": vacio(), f"{DI}!C156": vacio(), f"{PN}!K20": vacio(),
      f"{AN}!B90": vacio(), f"{AN}!D92": vacio(), f"{AN}!A90": texto_legible()}, motor="B")
caso("S12_ADR_ratio_1_comparable", "6 · invariantes", EX, {f"{PA}!C47": "ADR o ADS", f"{CM}!D5": 1}, {f"{MO}!B253": es(True)}, motor="A")
caso("S13_ADR_sin_ratio_no_comparable", "6 · invariantes", EX, {f"{PA}!C47": "ADR o ADS"}, {f"{MO}!B253": es(False), f"{AN}!C84": vacio()}, motor="A")

# ===================== 9 · cobertura: una prueba por entrada material activa y motor (relación independiente)
CONFIGS_COB = {
    "base": (lambda wb: None, "ABC"),
    "quiebra": (lambda wb: (wb[PA].__setitem__("C22", 0.10), wb[PA].__setitem__("C23", 50)), "ABC"),
    "fcf_neg": (lambda wb: (wb[AN].__setitem__("C46", 0), wb[PA].__setitem__("C43", "Transitorio"), wb[PA].__setitem__("C44", 200)), "A"),
    "exceso_caja": (lambda wb: wb[AN].__setitem__("C76", 50), "A"),
    "adr": (lambda wb: (wb[PA].__setitem__("C47", "ADR o ADS"), wb[CM].__setitem__("D5", 1)), "ABC"),
    "desviacion": (lambda wb: (wb[AN].__setitem__("C41", 2200 * 1.30), wb[PA].__setitem__("C47", "Básicas frente a diluidas")), "ABC"),
}
SOLO_EN_CONFIG = {"quiebra": {"p_quiebra", "recuperacion"}, "fcf_neg": {"naturaleza_fcf", "fcf_normalizado"},
                  "exceso_caja": {"exceso_caja"}, "adr": {"ratio_adr", "causa_desviacion"}, "desviacion": {"causa_desviacion"}}

def _pendiente(e, wb):
    cm = wb[CM]; t = e["fila"]
    if e["tipo"] == "dato":
        cm.cell(t, 6).value = None; cm.cell(t, 10).value = None
    else:
        cm.cell(t, 6).value = "Pendiente de inversor"

def _caso_cobertura(cfg, motor, e):
    def f(wb):
        CONFIGS_COB[cfg][0](wb)
        completar(wb, motor)
        _pendiente(e, wb)
    return f

_motores_base = {"A": "A", "B": "B", "C": "C"}
_BASE_WB = None
def _activas_en(cfg, motor):
    global _BASE_WB
    if _BASE_WB is None:
        _BASE_WB = load_workbook(os.path.join(sys.argv[1], "Ejemplo_V6.3_EmpresaX.xlsx"))
    import copy as _copy
    wb = _BASE_WB
    # estado de entradas tras aplicar la configuración (sobre una copia ligera de los valores)
    ins = REL.leer_ins(wb)
    if cfg == "quiebra": ins.update(P_C22=0.10)
    if cfg == "fcf_neg": ins.update(A_C46=0, P_C43="Transitorio")
    if cfg == "exceso_caja": ins.update(A_C76=50)
    if cfg == "adr": ins.update(P_C47="ADR o ADS", CM_D5=1)
    if cfg == "desviacion": ins.update(A_C41=2200 * 1.30, P_C47="Básicas frente a diluidas")
    return REL.activas(motor, ins)

def generar_cobertura():
    for cfg, (_, motores) in CONFIGS_COB.items():
        for motor in motores:
            act = _activas_en(cfg, motor)
            if cfg != "base":
                act = [e for e in act if e["id"] in SOLO_EN_CONFIG[cfg]]
            for e in act:
                caso(f"COB_{cfg}_{motor}_{e['id']}", "9 · cobertura", EX, _caso_cobertura(cfg, motor, e),
                     {f"{MO}!B266": empieza("NO LISTO · evidencias incompletas (1 pendientes)"),
                      f"{MO}!B255": es("COMPLETO Y VÁLIDO")}, motor=motor)
            # positivo: todo documentado y confirmado en esta configuración → LISTO
            def _pos(wb, cfg=cfg, motor=motor):
                CONFIGS_COB[cfg][0](wb); completar(wb, motor)
            caso(f"COB_{cfg}_{motor}_todo_confirmado_LISTO", "9 · cobertura", EX, _pos,
                 {f"{MO}!B266": es("LISTO"), f"{MO}!B255": es("COMPLETO Y VÁLIDO")}, motor=motor)
        # «No aplicable» legítimo en una entrada que el motor no usa
    caso("COB_no_aplicable_legitimo_DA_en_B", "9 · cobertura", EX,
         lambda wb: (completar(wb, "B"), wb[CM].__setitem__("F110", "No aplicable")), {f"{MO}!B266": es("LISTO")}, motor="B")
    caso("COB_no_aplicable_legitimo_S2C_en_C", "9 · cobertura", EX,
         lambda wb: (completar(wb, "C"), wb[CM].__setitem__("F144", "No aplicable")), {f"{MO}!B266": es("LISTO")}, motor="C")
    caso("COB_no_aplicable_indebido_r_en_C", "9 · cobertura", EX,
         lambda wb: (completar(wb, "C"), wb[CM].__setitem__("F53", "No aplicable")),
         {f"{MO}!B266": empieza("NO LISTO · evidencias incompletas (1 pendientes)"), f"{MO}!B269": contiene("1 «No aplicable» indebido")}, motor="C")
    caso("COB_no_verificable_crecimiento_en_A", "9 · cobertura", EX,
         lambda wb: (completar(wb, "A"), wb[CM].__setitem__("F146", "Dato no verificable")),
         {f"{MO}!B266": empieza("NO LISTO · evidencias incompletas (1 pendientes)"), f"{MO}!B269": contiene("1 no verificables")}, motor="A")
    caso("COB_estimacion_sin_justificar_margen_en_B", "9 · cobertura", EX,
         lambda wb: (completar(wb, "B"), wb[CM].__setitem__("F147", "Estimación declarada"), wb[CM].__setitem__("M147", None)),
         {f"{MO}!B266": empieza("NO LISTO · evidencias incompletas (1 pendientes)")}, motor="B")
    caso("COB_estimacion_justificada_ROIC_en_C_provisional", "9 · cobertura", EX,
         lambda wb: (completar(wb, "C"), wb[CM].__setitem__("F149", "Estimación declarada"), wb[CM].__setitem__("M149", "Rango del sector")),
         {f"{MO}!B266": empieza("LISTO · PROVISIONAL (1 estimaciones")}, motor="C")
    caso("COB_quiebra_vacia_no_exige_confirmacion", "9 · cobertura", EX, lambda wb: completar(wb, "A"),
         {f"{MO}!B266": es("LISTO"), f"{PA}!C22": vacio()}, motor="A")

# ===================== 8 · visualización de los bloques nuevos (sobre el entregable, sin recalcular)
_R1 = 179 + len(REL.ENTRADAS) - 1
BLOQUES = [(HI, 73, 82, "ABC"), (DI, 174, 180, "ABCD"), (DI, 213, 224, "ABC"), (CM, 174, _R1 + 15, "ABCDEFGHIJKL"),
           (GU, 66, 73, "A"), (PN, 3, 3, "B")]


def comprobar_visualizacion(path):
    wb = load_workbook(path)
    fallos = []
    for hoja, r0, r1, cols in BLOQUES:
        ws = wb[hoja]
        for r in range(r0, r1 + 1):
            if ws.row_dimensions[r].hidden:
                fallos.append(f"{hoja} fila {r} oculta")
            for col in cols:
                c = ws[f"{col}{r}"]
                if c.value is None:
                    continue
                if ws.column_dimensions[col].hidden or (ws.column_dimensions[col].width is not None and ws.column_dimensions[col].width == 0):
                    fallos.append(f"{hoja} columna {col} oculta")
                if c.font is None or c.font.color is None or c.font.color.rgb in (None, "FF000000"):
                    fallos.append(f"{hoja}!{col}{r} sin color de tema")
                if c.fill is None or c.fill.fill_type is None:
                    fallos.append(f"{hoja}!{col}{r} sin fondo de tema")
    pn = wb[PN]
    reglas = [list(r.formula or []) for cf in pn.conditional_formatting for r in cf.rules]
    for esperado in (['$J$2="LISTO"'], ['LEFT($J$2,19)="LISTO · PROVISIONAL"'], ['ISNUMBER(SEARCH("INCOMPLETAS",$B$3))']):
        if esperado not in reglas:
            fallos.append(f"Panel: falta la regla de formato {esperado}")
    return fallos


# =============================================================== motor
def construir(entregables, destino):
    os.makedirs(destino, exist_ok=True)
    fuentes = {EX: "Ejemplo_V6.3_EmpresaX.xlsx", TPL: "Plantilla_V6.3.xlsx",
               ABB: "Ejemplo_ABB_V6.3.xlsx", HER: "Ejemplo_migracion_Hermes_V6.3.xlsx"}
    ficheros = []
    for c in CASOS:
        p = os.path.join(destino, c["nombre"] + ".xlsx")
        shutil.copy(os.path.join(entregables, fuentes[c["base"]]), p)
        wb = load_workbook(p)
        if c["motor"]:
            wb[AN]["C62"] = MOT[c["motor"]]
        m = c["mut"]
        if callable(m):
            m(wb)
        elif m:
            for ref, val in m.items():
                h, coord = ref.split("!")
                wb[h][coord] = val
        wb.save(p)
        ficheros.append(p)
    return ficheros


def recalcular(ficheros, destino):
    os.makedirs(destino, exist_ok=True)
    for i in range(0, len(ficheros), 20):
        subprocess.run(["soffice", "--headless", "--calc", "--convert-to", "xlsx", "--outdir", destino]
                       + ficheros[i:i + 20], capture_output=True, timeout=1200)


def evaluar(destino, sha_base):
    res = []
    for c in CASOS:
        p = os.path.join(destino, c["nombre"] + ".xlsx")
        base = {"nombre": c["nombre"], "familia": c["familia"], "archivo_base": c["base"], "motor": c["motor"] or "—",
                "entradas": ("función: " + c["mut"].__name__) if callable(c["mut"]) else (c["mut"] or "—"),
                "sha256_entregable_base": sha_base}
        if not os.path.exists(p):
            res.append({**base, "resultado": "NO EJECUTADA", "motivo": "LibreOffice no produjo el archivo recalculado"})
            continue
        wb = load_workbook(p, data_only=True)
        detalle, ok = [], True
        for ref, (esperado, pred) in c["checks"].items():
            if ref == "__libro__":
                try:
                    paso, v = bool(pred(wb)), "—"
                except Exception as e:
                    paso, v = False, f"error: {e}"
            else:
                h, coord = ref.split("!")
                v = wb[h][coord].value
                paso = bool(pred(v))
            ok &= paso
            detalle.append({"celda": ref, "esperado": esperado,
                            "obtenido": v if not isinstance(v, float) else round(v, 10), "resultado": "OK" if paso else "FALLA"})
        res.append({**base, "comprobaciones": detalle, "resultado": "SUPERADA" if ok else "FALLIDA"})
    return res


def main():
    if len(sys.argv) < 3:
        print(__doc__); return 2
    entregables, out = sys.argv[1], sys.argv[2]
    refp = sys.argv[sys.argv.index("--referencia") + 1] if "--referencia" in sys.argv else None
    generar_cobertura()
    if "--solo-familia" in sys.argv:
        pref = sys.argv[sys.argv.index("--solo-familia") + 1]
        CASOS[:] = [c for c in CASOS if c["familia"].startswith(pref)]
    if "--excluir-familia" in sys.argv:
        pref = sys.argv[sys.argv.index("--excluir-familia") + 1]
        CASOS[:] = [c for c in CASOS if not c["familia"].startswith(pref)]
    saltar_integridad_y_vis = "--solo-familia" in sys.argv
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    shas = {f: hashlib.sha256(open(os.path.join(entregables, f), "rb").read()).hexdigest()
            for f in sorted(os.listdir(entregables)) if f.endswith(".xlsx")}
    fich = construir(entregables, os.path.join(out, "casos"))
    recalcular(fich, os.path.join(out, "rct"))
    res = evaluar(os.path.join(out, "rct"), shas.get("Ejemplo_V6.3_EmpresaX.xlsx"))

    # 8 · visualización (sobre el entregable, sin recalcular)
    for f in ([] if saltar_integridad_y_vis else ("Plantilla_V6.3.xlsx", "Ejemplo_V6.3_EmpresaX.xlsx")):
        fal = comprobar_visualizacion(os.path.join(entregables, f))
        res.append({"nombre": f"VIS_{f}", "familia": "8 · visualización", "archivo_base": f, "motor": "—",
                    "entradas": "—", "sha256_entregable_base": shas[f],
                    "comprobaciones": [{"celda": "bloques nuevos", "esperado": "visibles, con tema y reglas de color",
                                        "obtenido": fal or "OK", "resultado": "OK" if not fal else "FALLA"}],
                    "resultado": "SUPERADA" if not fal else "FALLIDA"})

    # 7 · verificador contra la referencia aprobada (si se pasa)
    if refp and not saltar_integridad_y_vis:
        import verificar_v63
        ref = json.load(open(refp))
        for f in shas:
            fallos, avisos = verificar_v63.comparar(os.path.join(entregables, f), ref)
            res.append({"nombre": f"INT_{f}", "familia": "7 · integridad", "archivo_base": f, "motor": "—", "entradas": "—",
                        "sha256_entregable_base": shas[f],
                        "comprobaciones": [{"celda": "libro completo", "esperado": "ÍNTEGRO frente a " + str(ref.get("version")),
                                            "obtenido": fallos or "ÍNTEGRO", "resultado": "OK" if not fallos else "FALLA"}],
                        "resultado": "SUPERADA" if not fallos else "FALLIDA"})
        # manipulaciones obligatorias: deben ser rechazadas nombrando la celda
        from patch_v62_base import restaurar_partes
        man_dir = os.path.join(out, "manipulaciones"); os.makedirs(man_dir)
        for nombre, hoja, coord, val in (("C58_cero", HI, "C58", "=0"), ("C83_cero", AN, "C83", "=0"),
                                         ("C83_valor", AN, "C83", 25.0), ("V23_anulada", MO, "E223", '=""')):
            src = os.path.join(entregables, "Plantilla_V6.3.xlsx")
            tmp = os.path.join(man_dir, f"tmp_{nombre}.xlsx"); dst = os.path.join(man_dir, f"{nombre}.xlsx")
            shutil.copy(src, tmp); wb = load_workbook(tmp); wb[hoja][coord] = val; wb.save(tmp)
            subprocess.run([sys.executable, "-I", os.path.join(HERE, "add_sliders.py"), tmp, dst], check=True, capture_output=True)
            restaurar_partes(src, dst)
            fallos, _ = verificar_v63.comparar(dst, ref)
            nombrada = any(f"{hoja}!{coord}" in x for x in fallos)
            res.append({"nombre": f"MAN_{nombre}", "familia": "7 · integridad", "archivo_base": "Plantilla_V6.3.xlsx",
                        "motor": "—", "entradas": {f"{hoja}!{coord}": val}, "sha256_entregable_base": shas["Plantilla_V6.3.xlsx"],
                        "comprobaciones": [{"celda": f"{hoja}!{coord}", "esperado": "ALTERADO y la celda nombrada",
                                            "obtenido": fallos, "resultado": "OK" if (fallos and nombrada) else "FALLA"}],
                        "resultado": "SUPERADA" if (fallos and nombrada) else "FALLIDA"})
        # entradas legítimas: sin falsos positivos
        src = os.path.join(entregables, "Plantilla_V6.3.xlsx")
        tmp = os.path.join(man_dir, "tmp_legit.xlsx"); dst = os.path.join(man_dir, "legitimas.xlsx")
        shutil.copy(src, tmp); wb = load_workbook(tmp)
        for h, c, v in ((AN, "B3", "Prueba SA"), (AN, "C37", 10), (HI, "L6", 500), (HI, "M6", "nota"),
                        (CM, "J124", "Informe anual"), (CM, "F124", "Rellenado y verificado"), (PA, "C48", "EUR"),
                        (PN, "E20", 30), (DI, "B222", "¿Es sostenible el margen?"), (CM, "H4", "EUR")):
            wb[h][c] = v
        wb.save(tmp)
        subprocess.run([sys.executable, "-I", os.path.join(HERE, "add_sliders.py"), tmp, dst], check=True, capture_output=True)
        restaurar_partes(src, dst)
        fallos, _ = verificar_v63.comparar(dst, ref)
        res.append({"nombre": "INT_entradas_legitimas_sin_falsos_positivos", "familia": "7 · integridad",
                    "archivo_base": "Plantilla_V6.3.xlsx", "motor": "—", "entradas": "10 entradas rellenadas",
                    "sha256_entregable_base": shas["Plantilla_V6.3.xlsx"],
                    "comprobaciones": [{"celda": "libro completo", "esperado": "ÍNTEGRO", "obtenido": fallos or "ÍNTEGRO",
                                        "resultado": "OK" if not fallos else "FALLA"}],
                    "resultado": "SUPERADA" if not fallos else "FALLIDA"})

    sup = sum(r["resultado"] == "SUPERADA" for r in res)
    fal = sum(r["resultado"] == "FALLIDA" for r in res)
    noe = sum(r["resultado"] == "NO EJECUTADA" for r in res)
    salida = {"version": "V6.3", "entregables_probados": shas, "referencia": refp,
              "total": len(res), "superadas": sup, "fallidas": fal, "no_ejecutadas": noe,
              "no_ejecutadas_declaradas": [
                  "Excel real: deslizadores, colores, avisos de reparación y guardado/reapertura (solo LibreOffice 24.2 headless)",
                  "V37 frente a booleanos en Historia (LibreOffice los lee como números)",
                  "R03 migración desde Hermes_evaluada.xlsx y R08 ABB desde abb_fase1.json: insumos no entregados"],
              "casos": res}
    json.dump(salida, open(os.path.join(out, "resultados_v63.json"), "w"), ensure_ascii=False, indent=1, default=str)
    print(f"{sup} superadas · {fal} fallidas · {noe} no ejecutadas · total {len(res)}")
    for r in res:
        if r["resultado"] != "SUPERADA":
            print(f"  {r['resultado']}: {r['nombre']}")
            for d in r.get("comprobaciones", []):
                if d["resultado"] != "OK":
                    print(f"     {d['celda']}: esperado {d['esperado']} · obtenido {str(d['obtenido'])[:160]!r}")
    return 0 if fal == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
