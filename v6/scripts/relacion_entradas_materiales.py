"""Relación de las entradas MATERIALES de la valoración y de la lectura del precio, por motor.

Origen (independiente del inventario de evidencias de Control maestro):
  - `trazar_entradas_materiales.py` → `relacion_independiente.json`: traza estática del grafo de
    fórmulas desde las salidas y activación empírica por motor y configuración (492 recálculos).
  - Tres entradas añadidas por razonamiento sobre la traza estática, porque la perturbación tiene
    un punto ciego con ellas: Palancas C43 (sus opciones «Transitorio» y «Extraordinario» producen
    la misma rama), Palancas C8 (el fixture tiene márgenes constantes, así que «Media del ciclo»
    = «Último año») y Palancas C6 (la opción perturbada solo avisa; «Financiera» bloquea A y B).
  - Dos metadatos añadidos por el encargo («unidades necesarias para interpretar»): Control maestro
    J4 (unidad) y L4 (norma contable). No mueven ninguna salida; sin ellos no se puede interpretar
    ninguna cifra.

Cada entrada: celda, fila de la tabla de trazabilidad de Control maestro, tipo (dato → se
documenta; hipótesis → se razona y se confirma), motores, condición de uso (texto, fórmula Excel y
predicado Python equivalente), período que usa el cálculo. La fórmula Excel usa M como referencia al
motor activo ('Diagnóstico V6'!$C$5).
"""

M = "'Diagnóstico V6'!$C$5"
TODOS = f'OR({M}="A",{M}="B",{M}="C")'
AB = f'OR({M}="A",{M}="B")'


def _solo(m):
    return f'{M}="{m}"'


# predicados Python: reciben (motor, ins) donde ins es un dict con los valores de entrada relevantes
def _motor_en(*ms):
    return lambda motor, ins: motor in ms


def _c52(ins):
    v = [ins.get(k) for k in ("A_C46", "A_C47", "A_C48", "A_C49", "A_C50")]
    if any(not isinstance(x, (int, float)) or isinstance(x, bool) for x in v):
        return None
    sbc = 0 if ins.get("A_C51") == "No" else v[4]
    return v[0] - v[1] - v[2] - v[3] - sbc


def _desviacion(ins):
    p, c, a = ins.get("A_C37"), ins.get("A_C41"), ins.get("A_C55")
    if not all(isinstance(x, (int, float)) for x in (p, c, a)) or p <= 0 or a <= 0:
        return None
    return abs(c / (p * a) - 1)


ENTRADAS = [
    # ---------------- DATOS (se documentan: «Rellenado y verificado» + documento en J)
    dict(id="precio", celda="Análisis!C37", fila=38, tipo="dato", motores="ABC",
         cond="siempre (lectura del precio)", excel=TODOS, py=_motor_en("A", "B", "C"),
         periodo="fecha de valoración (Palancas C45)"),
    dict(id="capitalizacion", celda="Análisis!C41", fila=41, tipo="dato", motores="ABC",
         cond="siempre (bloquea el valor si falta; peso de financiación en B)", excel=TODOS,
         py=_motor_en("A", "B", "C"), periodo="fecha de valoración, en la moneda de cotización"),
    dict(id="acciones", celda="Análisis!C55", fila=52, tipo="dato", motores="ABC",
         cond="siempre", excel=TODOS, py=_motor_en("A", "B", "C"),
         periodo="acciones vigentes en la fecha de valoración (no la media del ejercicio)"),
    dict(id="cfo_media", celda="Análisis!C46", fila=43, tipo="dato", motores="A",
         cond="siempre en A (FCF base)", excel=_solo("A"), py=_motor_en("A"),
         periodo="media de 3–5 ejercicios (declara cuál en la columna G)"),
    dict(id="capex_media", celda="Análisis!C47", fila=44, tipo="dato", motores="A",
         cond="siempre en A", excel=_solo("A"), py=_motor_en("A"), periodo="media de 3–5 ejercicios"),
    dict(id="int_fin_media", celda="Análisis!C48", fila=45, tipo="dato", motores="A",
         cond="siempre en A (0 explícito si no hay)", excel=_solo("A"), py=_motor_en("A"),
         periodo="media de 3–5 ejercicios"),
    dict(id="leases_media", celda="Análisis!C49", fila=46, tipo="dato", motores="A",
         cond="siempre en A (0 explícito si no hay)", excel=_solo("A"), py=_motor_en("A"),
         periodo="media de 3–5 ejercicios"),
    dict(id="sbc_media", celda="Análisis!C50", fila=48, tipo="dato", motores="A",
         cond="siempre en A (0 explícito si no hay)", excel=_solo("A"), py=_motor_en("A"),
         periodo="media de 3–5 ejercicios"),
    dict(id="h_anios", celda="Historia!C5:L5", fila=107, tipo="dato", motores="ABC",
         cond="siempre (años consecutivos, el último en L)", excel=TODOS, py=_motor_en("A", "B", "C"),
         periodo="todos los ejercicios cargados"),
    dict(id="h_ventas", celda="Historia!C6:L6", fila=108, tipo="dato", motores="AB",
         cond="A y B", excel=AB, py=_motor_en("A", "B"),
         periodo="ventana de f (Historia C57) y último ejercicio; toda la serie si Palancas C8 = «Media del ciclo»"),
    dict(id="h_ebit", celda="Historia!C7:L7", fila=109, tipo="dato", motores="AB",
         cond="A y B", excel=AB, py=_motor_en("A", "B"),
         periodo="ventana de f y último ejercicio; toda la serie con «Media del ciclo»"),
    dict(id="h_da", celda="Historia!C8:L8", fila=110, tipo="dato", motores="A",
         cond="A", excel=_solo("A"), py=_motor_en("A"), periodo="ventana de f"),
    dict(id="h_beneficio", celda="Historia!C9:L9", fila=111, tipo="dato", motores="C",
         cond="C", excel=_solo("C"), py=_motor_en("C"), periodo="último ejercicio (L9)"),
    dict(id="h_tipo", celda="Historia!C10:L10", fila=112, tipo="dato", motores="AB",
         cond="A y B", excel=AB, py=_motor_en("A", "B"), periodo="ventana de f (A) · media de 5 ejercicios (A y B)"),
    dict(id="h_capex", celda="Historia!C12:L12", fila=114, tipo="dato", motores="A",
         cond="A", excel=_solo("A"), py=_motor_en("A"), periodo="ventana de f"),
    dict(id="h_circulante", celda="Historia!C14:L14", fila=116, tipo="dato", motores="A",
         cond="A", excel=_solo("A"), py=_motor_en("A"), periodo="ventana de f"),
    dict(id="h_intereses", celda="Historia!C15:L15", fila=117, tipo="dato", motores="B",
         cond="B", excel=_solo("B"), py=_motor_en("B"), periodo="último ejercicio (L15)"),
    dict(id="h_patrimonio", celda="Historia!C21:L21", fila=123, tipo="dato", motores="C",
         cond="C", excel=_solo("C"), py=_motor_en("C"), periodo="último ejercicio (L21)"),
    dict(id="h_deuda", celda="Historia!C22:L22", fila=124, tipo="dato", motores="B",
         cond="B", excel=_solo("B"), py=_motor_en("B"), periodo="dos últimos ejercicios (K22, L22)"),
    dict(id="h_arrend", celda="Historia!C23:L23", fila=125, tipo="dato", motores="B",
         cond="B", excel=_solo("B"), py=_motor_en("B"), periodo="dos últimos ejercicios (K23, L23)"),
    dict(id="h_caja", celda="Historia!C24:L24", fila=126, tipo="dato", motores="B",
         cond="B", excel=_solo("B"), py=_motor_en("B"), periodo="último ejercicio (L24)"),
    dict(id="h_pensiones", celda="Historia!C25:L25", fila=127, tipo="dato", motores="B",
         cond="B", excel=_solo("B"), py=_motor_en("B"), periodo="último ejercicio (L25); superávit = 0 con aviso"),
    dict(id="h_minoritarios", celda="Historia!C26:L26", fila=128, tipo="dato", motores="B",
         cond="B", excel=_solo("B"), py=_motor_en("B"), periodo="último ejercicio (L26)"),
    dict(id="moneda_cotizacion", celda="Palancas!C48", fila=171, tipo="dato", motores="ABC",
         cond="siempre (comparabilidad; en B también el valor)", excel=TODOS, py=_motor_en("A", "B", "C"),
         periodo="fecha de valoración"),
    dict(id="moneda_modelo", celda="'Control maestro'!H4", fila=172, tipo="dato", motores="ABC",
         cond="siempre", excel=TODOS, py=_motor_en("A", "B", "C"), periodo="moneda de los estados financieros"),
    dict(id="ratio_adr", celda="'Control maestro'!D5", fila=173, tipo="dato", motores="ABC",
         cond="si Palancas C47 = «ADR o ADS» o D5 informado",
         excel=f'AND({TODOS},OR(Palancas!$C$47="ADR o ADS",\'Control maestro\'!$D$5<>""))',
         py=lambda motor, ins: ins.get("P_C47") == "ADR o ADS" or ins.get("CM_D5") not in (None, ""),
         periodo="fecha de valoración"),
    dict(id="unidad", celda="'Control maestro'!J4", fila=174, tipo="dato", motores="ABC",
         cond="siempre (metadato: sin él ninguna cifra se interpreta)", excel=TODOS,
         py=_motor_en("A", "B", "C"), periodo="unidad de todos los importes (mm, miles…)"),
    dict(id="norma", celda="'Control maestro'!L4", fila=175, tipo="dato", motores="ABC",
         cond="siempre (metadato: IFRS / US GAAP cambia intereses y arrendamientos)", excel=TODOS,
         py=_motor_en("A", "B", "C"), periodo="marco contable de los estados"),
    # ---------------- HIPÓTESIS Y DECISIONES (se razonan y se confirman: «Hipótesis confirmada» + justificación)
    dict(id="motor", celda="Análisis!C62", fila=57, tipo="hipótesis", motores="ABC",
         cond="siempre (elección del motor)", excel=TODOS, py=_motor_en("A", "B", "C"), periodo="—"),
    dict(id="r", celda="Análisis!C56", fila=53, tipo="hipótesis", motores="ABC",
         cond="siempre (r exigida; en B entra en la r operativa)", excel=TODOS, py=_motor_en("A", "B", "C"), periodo="—"),
    dict(id="caso_especial", celda="Palancas!C6", fila=138, tipo="hipótesis", motores="ABC",
         cond="siempre (aplicabilidad del motor: «Financiera» bloquea A y B)", excel=TODOS,
         py=_motor_en("A", "B", "C"), periodo="—"),
    dict(id="base_margen", celda="Palancas!C8", fila=139, tipo="hipótesis", motores="AB",
         cond="A y B (margen de partida: último año o media del ciclo)", excel=AB, py=_motor_en("A", "B"), periodo="—"),
    dict(id="anios_f", celda="Historia!C57", fila=129, tipo="hipótesis", motores="A",
         cond="A (ventana que calibra f)", excel=_solo("A"), py=_motor_en("A"), periodo="—"),
    dict(id="restar_sbc", celda="Análisis!C51", fila=49, tipo="hipótesis", motores="A",
         cond="A, si la SBC (C50) no es 0", excel=f'AND({_solo("A")},ISNUMBER(Análisis!$C$50),Análisis!$C$50<>0)',
         py=lambda motor, ins: motor == "A" and isinstance(ins.get("A_C50"), (int, float)) and ins.get("A_C50") != 0,
         periodo="—"),
]
for col, esc in (("B", "MALO"), ("C", "NORMAL"), ("D", "BUENO")):
    filas = {"B": (142, 143, 144, 145, 61, 62), "C": (146, 147, 148, 149, 66, 67), "D": (150, 151, 152, 153, 71, 72)}[col]
    ENTRADAS += [
        dict(id=f"crec_{esc}", celda=f"Palancas!{col}14", fila=filas[0], tipo="hipótesis", motores="ABC",
             cond="siempre", excel=TODOS, py=_motor_en("A", "B", "C"), periodo="años 1–5"),
        dict(id=f"margen_{esc}", celda=f"Palancas!{col}15", fila=filas[1], tipo="hipótesis", motores="ABC",
             cond="siempre (margen objetivo; ROE objetivo en C)", excel=TODOS, py=_motor_en("A", "B", "C"), periodo="año 5 en adelante"),
        dict(id=f"s2c_{esc}", celda=f"Palancas!{col}16", fila=filas[2], tipo="hipótesis", motores="AB",
             cond="A y B (reinversión)", excel=AB, py=_motor_en("A", "B"), periodo="años 1–10"),
        dict(id=f"roic_{esc}", celda=f"Palancas!{col}18", fila=filas[3], tipo="hipótesis", motores="ABC",
             cond="siempre (rentabilidad terminal)", excel=TODOS, py=_motor_en("A", "B", "C"), periodo="año 11 en adelante"),
        dict(id=f"g_{esc}", celda=f"Análisis!{col}68", fila=filas[4], tipo="hipótesis", motores="ABC",
             cond="siempre (crecimiento terminal)", excel=TODOS, py=_motor_en("A", "B", "C"), periodo="año 11 en adelante"),
        dict(id=f"prob_{esc}", celda=f"Análisis!{col}69", fila=filas[5], tipo="hipótesis", motores="ABC",
             cond="siempre (ponderación)", excel=TODOS, py=_motor_en("A", "B", "C"), periodo="—"),
    ]
ENTRADAS += [
    dict(id="p_quiebra", celda="Palancas!C22", fila=154, tipo="hipótesis", motores="ABC",
         cond="si está informada y es > 0 (vacía = 0 por convención, con aviso)",
         excel=f'AND({TODOS},ISNUMBER(Palancas!$C$22),Palancas!$C$22>0)',
         py=lambda motor, ins: isinstance(ins.get("P_C22"), (int, float)) and ins.get("P_C22") > 0, periodo="10 años"),
    dict(id="recuperacion", celda="Palancas!C23", fila=155, tipo="hipótesis", motores="ABC",
         cond="si la probabilidad de quiebra es > 0",
         excel=f'AND({TODOS},ISNUMBER(Palancas!$C$22),Palancas!$C$22>0)',
         py=lambda motor, ins: isinstance(ins.get("P_C22"), (int, float)) and ins.get("P_C22") > 0,
         periodo="valor presente"),
    dict(id="exceso_caja", celda="Análisis!C76", fila=82, tipo="hipótesis", motores="A",
         cond="A, si está informado y no es 0",
         excel=f'AND({_solo("A")},ISNUMBER(Análisis!$C$76),Análisis!$C$76<>0)',
         py=lambda motor, ins: motor == "A" and isinstance(ins.get("A_C76"), (int, float)) and ins.get("A_C76") != 0,
         periodo="saldo de hoy, sin descontar"),
    dict(id="naturaleza_fcf", celda="Palancas!C43", fila=166, tipo="hipótesis", motores="A",
         cond="A, si el FCF base (Análisis C52) ≤ 0",
         excel=f'AND({_solo("A")},ISNUMBER(Análisis!$C$52),Análisis!$C$52<=0)',
         py=lambda motor, ins: motor == "A" and _c52(ins) is not None and _c52(ins) <= 0, periodo="—"),
    dict(id="fcf_normalizado", celda="Palancas!C44", fila=167, tipo="hipótesis", motores="A",
         cond="A, si C52 ≤ 0 y la naturaleza es Transitorio o Extraordinario (calibra f)",
         excel=(f'AND({_solo("A")},ISNUMBER(Análisis!$C$52),Análisis!$C$52<=0,'
                'OR(Palancas!$C$43="Transitorio",Palancas!$C$43="Extraordinario"))'),
         py=lambda motor, ins: motor == "A" and _c52(ins) is not None and _c52(ins) <= 0
         and ins.get("P_C43") in ("Transitorio", "Extraordinario"), periodo="—"),
    dict(id="causa_desviacion", celda="Palancas!C47", fila=170, tipo="hipótesis", motores="ABC",
         cond="si la desviación capitalización ÷ (precio × acciones) supera el umbral (Diagnóstico C91) o hay causa declarada",
         excel=(f'AND({TODOS},OR(AND(Palancas!$C$47<>"",Palancas!$C$47<>"Ninguna"),'
                'IF(AND(ISNUMBER(Análisis!$C$37),ISNUMBER(Análisis!$C$41),ISNUMBER(Análisis!$C$55),'
                'N(Análisis!$C$37)>0,N(Análisis!$C$55)>0),'
                'ABS(Análisis!$C$41/(N(Análisis!$C$37)*N(Análisis!$C$55))-1)>\'Diagnóstico V6\'!$C$91,FALSE)))'),
         py=lambda motor, ins: (ins.get("P_C47") not in (None, "", "Ninguna"))
         or (_desviacion(ins) is not None and _desviacion(ins) > ins.get("D_C91", 0.05)),
         periodo="fecha de valoración"),
]

# Entradas editables que NO están en la relación, y por qué (comprobado en la activación empírica).
EXCLUSIONES = [
    ("Análisis C11:C13 (filtro Pabrai)", "gate de dominio (solo «Sí»/«No» exactos); lo controla el estado de inversión, no la evidencia"),
    ("Análisis B65:D66, B101, B102, C14, C17:C20, C24:C28, C31:C34, C93, C96:C98, C103, C104",
     "juicios cualitativos y completitud (nivel 3): no mueven el valor ni la lectura del precio"),
    ("Análisis C38, C40, C42, C53, C54, C57, C60, C88",
     "indicadores auxiliares (fuente externa, FCF yield, múltiplos, tasa sin riesgo): no mueven las salidas vigiladas"),
    ("Historia filas 11, 13, 16, 17, 18, 19, 20", "anclas informativas (S2C marginal, FCF histórico, ROIC con I+D): sin efecto en las salidas"),
    ("Palancas C5, C7, C9, C10, C24, C45, C46, A28:B33, A38:C40",
     "pistas, sector, I+D en anclas, cuota implícita, fechas (solo aviso), países (r mínima), predicciones: sin efecto en las salidas"),
    ("Panel C6, F6, E20:E25", "visualización y modo estudio: no tocan la hipótesis base (R05)"),
    ("Diagnóstico V6 C91:C94, C158, C179, B222:C223", "parámetros de diseño visibles (el verificador informa sus cambios) y líneas de juicio libre"),
    ("Control maestro E:N de la trazabilidad", "es la documentación misma"),
    ("Palancas C22 vacía", "convención deliberada: probabilidad de quiebra 0 con aviso visible; se exige confirmación solo cuando se informa > 0"),
    ("Análisis C76 vacío o 0", "convención deliberada: sin exceso de caja; se exige confirmación solo cuando se informa ≠ 0"),
]


def activas(motor, ins):
    """Entradas activas para un motor y un estado de entradas (predicados Python)."""
    return [e for e in ENTRADAS if e["py"](motor, ins)]


def leer_ins(wb):
    """Valores de entrada que necesitan los predicados, leídos de un libro abierto con openpyxl."""
    an, pa, cm, di = wb["Análisis"], wb["Palancas"], wb["Control maestro"], wb["Diagnóstico V6"]
    ins = {f"A_{c}": an[c].value for c in ("C37", "C41", "C55", "C46", "C47", "C48", "C49", "C50", "C51", "C76")}
    ins.update({f"P_{c}": pa[c].value for c in ("C22", "C43", "C47")})
    ins["CM_D5"] = cm["D5"].value
    ins["D_C91"] = di["C91"].value if isinstance(di["C91"].value, (int, float)) else 0.05
    return ins
