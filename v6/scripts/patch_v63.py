#!/usr/bin/env python3
"""Construye un libro V6.3 a partir de uno de la familia V6.1.

Uso:  python3 patch_v63.py entrada_V6.1.xlsx salida_V6.3_sin_deslizadores.xlsx
      (después, SIEMPRE: python3 add_sliders.py salida_V6.3_sin_deslizadores.xlsx Entregable_V6.3.xlsx)

Dependencias: openpyxl >= 3.1. Sin rutas personales.

Capas:
  1. patch_v62_base.aplicar_capa_v62  (ausencias ≠ cero, moneda común, conciliación de f,
     transición al terminal, estados y textos de la V6.2; SIN el bloque de evidencias
     de la V6.2, que pisaba las filas 121–124 de Control maestro)
  2. esta capa V6.3:
     - control de evidencias con inventario explícito por motor (Control maestro 176+)
     - la conciliación de f llega al estado global (V39 ampliada)
     - dominios económicos: deuda bruta, arrendamientos, caja, pensiones, minoritarios,
       D&A, capex, intereses, SBC, I+D y acciones no admiten negativos (V37 ampliada
       + validaciones de datos en Historia)
     - LISTO solo con evidencias documentadas; PROVISIONAL con estimaciones declaradas
     - estilos de los bloques nuevos de Diagnóstico V6 (la V6.2 los dejó sin tema)
"""
import os
import sys
from copy import copy

from openpyxl import load_workbook
from openpyxl.formatting.rule import Rule
from openpyxl.styles import Font, PatternFill
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.worksheet.datavalidation import DataValidation

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import patch_v62_base as base  # noqa: E402

HI, AN, PA, DI, MO, PN, CM = base.HI, base.AN, base.PA, base.DI, base.MO, base.PN, base.CM
Q = chr(34)

# ============================================================ 1 · EVIDENCIAS
# El inventario se construye desde la relación independiente de entradas materiales
# (relacion_entradas_materiales.py, derivada de la traza de fórmulas y de la activación empírica),
# no al revés.
import relacion_entradas_materiales as REL  # noqa: E402

R0 = 179                                   # primera fila del inventario
R1 = R0 + len(REL.ENTRADAS) - 1            # última
RES = R1 + 2                               # cabecera del resumen
FILA = {k: RES + 1 + n for n, k in enumerate(
    ("calculo", "M", "Dtot", "doc", "Htot", "hconf", "estim", "noverif", "hip", "sinclas", "indebido", "estado"))}
FILA_NOTA = FILA["estado"] + 1
MOTOR_ACTIVO = REL.M

# Filas de trazabilidad nuevas (metadatos que faltaban en la tabla): unidad y norma contable.
TRAZABILIDAD_NUEVA = [
    ("A174", "Control maestro"), ("B174", "'Control maestro'!J4"), ("C174", "Unidad financiera de todos los importes (mm, miles…)"),
    ("D174", "Dato objetivo / metadata"), ("E174", "Pendiente de carga"),
    ("A175", "Control maestro"), ("B175", "'Control maestro'!L4"), ("C175", "Norma contable (IFRS, US GAAP, Otro)"),
    ("D175", "Dato objetivo / metadata"), ("E175", "Pendiente de carga"),
]


def _fila_inventario(r, e):
    t = e["fila"]
    I, J, K, D, F = f"I{r}", f"J{r}", f"K{r}", f"D{r}", f"F{r}"
    estado = (
        f'=IF(NOT({F}),"—",'
        f'IF({I}="Pendiente de inversor","hipótesis pendiente",'
        f'IF({I}="Dato no verificable","no verificable",'
        f'IF({I}="No aplicable","no aplicable indebido",'
        f'IF({I}="Estimación declarada",IF({K},"estimación","estimación sin justificar"),'
        f'IF({D}="dato",'
        f'IF({I}="Rellenado y verificado",IF({J}="","sin fuente","documentada"),'
        f'IF({I}="Hipótesis confirmada","incoherente: dato marcado como hipótesis","sin clasificar")),'
        f'IF({I}="Hipótesis confirmada",IF({K},"hipótesis confirmada","hipótesis sin justificar"),'
        f'IF({I}="Rellenado y verificado","incoherente: hipótesis marcada como hecho","sin clasificar"))))))))'
    )
    if t == 175:
        prefix = f'=IF(NOT({F}),"—",'
        estado = (prefix + 'IF(LEN(TRIM(CLEAN(SUBSTITUTE($L$4," "," "))))=0,'
                  '"falta norma contable",' + estado[len(prefix):] + ')')
    return [
        (f"A{r}", t),
        (f"B{r}", f"=$B${t}"),
        (f"C{r}", f"=$C${t}"),
        (f"D{r}", e["tipo"]),
        (f"E{r}", " · ".join(e["motores"])),
        (f"F{r}", "=" + e["excel"]),
        (f"G{r}", e["cond"]),
        (f"H{r}", e["periodo"]),
        (I, f'=IF($F${t}="","",$F${t})'),
        (J, f'=IF($J${t}="","",$J${t})'),
        (K, f'=OR($J${t}<>"",$M${t}<>"",$N${t}<>"")'),
        (f"L{r}", estado),
    ]


def bloque_evidencias():
    Lr = f"$L${R0}:$L${R1}"
    Fr = f"$F${R0}:$F${R1}"
    Dr = f"$D${R0}:$D${R1}"
    f = FILA
    celdas = [
        ("A176", "  CONTROL DE EVIDENCIAS (V6.3) · inventario de las entradas materiales de cada motor, por tipo y condición de uso"),
        ("A177", "Un DATO se documenta («Rellenado y verificado» + documento en J). Una HIPÓTESIS o decisión se razona y se "
                 "confirma («Hipótesis confirmada» + justificación en J, M o N): no es un hecho verificado. «Estimación "
                 "declarada» + justificación deja el libro PROVISIONAL. Excel no comprueba la verdad de nada de esto."),
        ("A178", "Fila"), ("B178", "Celda"), ("C178", "Concepto"), ("D178", "Tipo"), ("E178", "Motores"),
        ("F178", "Aplica ahora"), ("G178", "Condición de uso"), ("H178", "Período / uso"),
        ("I178", "Clasificación (col. F)"), ("J178", "Documento (col. J)"), ("K178", "Justificación (J, M o N)"),
        ("L178", "Estado de evidencia"),
    ]
    for n, e in enumerate(REL.ENTRADAS):
        celdas += _fila_inventario(R0 + n, e)
    celdas += [
        (f"A{RES}", f'="  RESUMEN DE EVIDENCIAS · motor activo: "&IF({MOTOR_ACTIVO}="","(sin elegir)",{MOTOR_ACTIVO})'),
        (f"A{f['calculo']}", "Cálculo"),
        (f"D{f['calculo']}", '=IF(Motor!$B$252,"bloqueado · "&Motor!$B$257,"disponible")'),
        (f"A{f['M']}", "Entradas materiales activas (M)"),
        (f"D{f['M']}", f"=COUNTIF({Fr},TRUE)"),
        (f"A{f['Dtot']}", "· de ellas, datos"),
        (f"D{f['Dtot']}", f'=COUNTIFS({Fr},TRUE,{Dr},"dato")'),
        (f"A{f['doc']}", "Datos documentados (fuente declarada)"),
        (f"D{f['doc']}", f'=COUNTIF({Lr},"documentada")'),
        (f"A{f['Htot']}", "· de ellas, hipótesis y decisiones"),
        (f"D{f['Htot']}", f'=COUNTIFS({Fr},TRUE,{Dr},"hipótesis")'),
        (f"A{f['hconf']}", "Hipótesis razonadas y confirmadas"),
        (f"D{f['hconf']}", f'=COUNTIF({Lr},"hipótesis confirmada")'),
        (f"A{f['estim']}", "Estimaciones justificadas (resultado provisional)"),
        (f"D{f['estim']}", f'=COUNTIF({Lr},"estimación")'),
        (f"A{f['noverif']}", "Datos no verificables"),
        (f"D{f['noverif']}", f'=COUNTIF({Lr},"no verificable")'),
        (f"A{f['hip']}", "Hipótesis pendientes («Pendiente de inversor»)"),
        (f"D{f['hip']}", f'=COUNTIF({Lr},"hipótesis pendiente")'),
        (f"A{f['sinclas']}", "Sin dato, sin clasificar, sin fuente, sin justificar o incoherentes"),
        (f"D{f['sinclas']}", (f'=COUNTIF({Lr},"sin clasificar")+COUNTIF({Lr},"sin fuente")'
                             f'+COUNTIF({Lr},"estimación sin justificar")+COUNTIF({Lr},"hipótesis sin justificar")'
                             f'+COUNTIF({Lr},"incoherente: dato marcado como hipótesis")'
                             f'+COUNTIF({Lr},"incoherente: hipótesis marcada como hecho")'
                             f'+COUNTIF({Lr},"falta norma contable")')),
        (f"A{f['indebido']}", "«No aplicable» en una entrada que el motor usa"),
        (f"D{f['indebido']}", f'=COUNTIF({Lr},"no aplicable indebido")'),
        (f"A{f['estado']}", "ESTADO DE LAS EVIDENCIAS"),
        (f"D{f['estado']}", (
            f'=IF(D{f["M"]}=0,"sin entradas aplicables: elige el motor en Análisis C62",'
            f'IF(D{f["noverif"]}+D{f["hip"]}+D{f["sinclas"]}+D{f["indebido"]}=0,'
            f'IF(D{f["estim"]}=0,'
            f'"documentadas "&D{f["doc"]}&" de "&D{f["Dtot"]}&" · hipótesis confirmadas "&D{f["hconf"]}&" de "&D{f["Htot"]}'
            f'&" (declarado por el analista; Excel no comprueba el dato)",'
            f'"PROVISIONAL · "&D{f["estim"]}&" estimación(es) justificada(s) · documentadas "&D{f["doc"]}&" de "&D{f["Dtot"]}'
            f'&" · hipótesis confirmadas "&D{f["hconf"]}&" de "&D{f["Htot"]}),'
            f'"INCOMPLETAS · datos "&D{f["doc"]}&" de "&D{f["Dtot"]}&" · hipótesis confirmadas "&D{f["hconf"]}&" de "&D{f["Htot"]}'
            f'&" · "&D{f["estim"]}&" estimaciones · "&D{f["noverif"]}&" no verificables · "&D{f["hip"]}&" hipótesis pendientes · "'
            f'&D{f["sinclas"]}&" sin dato, sin clasificar, sin fuente o incoherentes · "&D{f["indebido"]}&" «No aplicable» indebido"))')),
        (f"A{FILA_NOTA}", "Este bloque mide la documentación declarada de los datos y la confirmación razonada de las hipótesis "
                          "que usa el motor activo; no la corrección del cálculo (eso lo hace Motor, filas 201–268). Las "
                          "entradas que el motor no usa no bloquean nada. Relación de origen: relacion_entradas_materiales.py."),
    ]
    return celdas


PENDIENTES = "+".join(f"'Control maestro'!$D${FILA[k]}" for k in ("noverif", "hip", "sinclas", "indebido"))
ESTIM = f"'Control maestro'!$D${FILA['estim']}"


def estado_libro_v63(orig):
    """Envuelve ESTADO DEL LIBRO: LISTO solo con datos documentados e hipótesis confirmadas."""
    o = orig[1:]
    return (f'=IF(({o})="LISTO",IF({PENDIENTES}=0,IF({ESTIM}=0,"LISTO",'
            f'"LISTO · PROVISIONAL ("&{ESTIM}&" estimaciones justificadas)"),'
            f'"NO LISTO · evidencias incompletas ("&({PENDIENTES})&" pendientes) · cálculo completo"),{o})')


# ============================================================ 2 · CONCILIACIÓN → ESTADO
CONCILIACION_INV = (
    'IF(Historia!$C$81="⛔ TÉCNICO · la conciliación no cuadra",'
    '"INV|La conciliación de f no cuadra (Historia C81): la fórmula de Historia C58 o el bloque de '
    'conciliación (Historia 73–81) han sido alterados; restaura la plantilla o verifica el archivo '
    'con verificar_v63.py","")'
)

# ============================================================ 3 · DOMINIOS ECONÓMICOS
NO_NEGATIVOS = [
    (8,  "<0",  "Amortizaciones (D&A) negativas en Historia fila 8: escribe el importe en positivo"),
    (12, "<0",  "Capex negativo en Historia fila 12: la plantilla pide el capex en positivo"),
    (15, "<0",  "Intereses pagados negativos en Historia fila 15: importe pagado, en positivo"),
    (16, "<0",  "Intereses en financiación negativos en Historia fila 16: importe pagado, en positivo"),
    (17, "<0",  "Principal de arrendamientos negativo en Historia fila 17: importe pagado, en positivo"),
    (18, "<0",  "SBC negativa en Historia fila 18"),
    (19, "<0",  "I+D negativa en Historia fila 19"),
    (20, "<=0", "Acciones diluidas ≤ 0 en Historia fila 20"),
    (22, "<0",  "Deuda financiera negativa en Historia fila 22: la plantilla pide deuda BRUTA (corto + largo "
                "plazo, sin arrendamientos), no deuda neta; no admite negativos"),
    (23, "<0",  "Pasivo por arrendamientos negativo en Historia fila 23: es una obligación bruta, no admite negativos"),
    (24, "<0",  "Caja negativa en Historia fila 24: la caja es un saldo ≥ 0; un descubierto bancario va en la deuda (fila 22)"),
    (26, "<0",  "Minoritarios negativos en Historia fila 26: intereses no dominantes del balance, ≥ 0"),
]


def dominios_inv():
    cola = '""'
    for fila, op, msg in reversed(NO_NEGATIVOS):
        cola = f'IF(COUNTIF(Historia!$C${fila}:$L${fila},"{op}")>0,"INV|{msg}",{cola})'
    return cola


def _envolver(orig, cola):
    o = orig[1:]
    return f'=IF(({o})<>"",{o},{cola})'


# ============================================================ 4 · TEXTOS
# Pensiones: la fila 25 es una posición NETA con signo (déficit > 0, superávit < 0). El motor B
# resta solo el déficit; un superávit se trata como 0 y se avisa (no se suma al valor: no es caja
# disponible para el accionista sin más análisis).
HI_C65_V63 = '=IF(AND(ISNUMBER(L25),ISNUMBER(L26)),MAX(0,L25)+L26,"")'
AVISO_PENSIONES = ('IF(AND(ISNUMBER(Historia!$L$25),Historia!$L$25<0),'
                   '"AVI|Superávit de pensiones en Historia L25 ("&TEXT(Historia!$L$25,"#,##0")&"): se trata '
                   'como déficit 0 y no se suma al valor; si crees que es recuperable, documéntalo en Control maestro","")')

TEXTOS_V63 = [
    (HI, "B25", "Posición neta (obligación − activos del plan): déficit > 0 se resta; superávit < 0 se trata "
                "como 0 · escribe 0 si no hay; vacío = desconocido"),
    (DI, "A15", "r operativa · motor B · tasa personalizada: tu r exigida (Análisis C56), el coste histórico de "
                "la deuda (intereses ÷ deuda media, Historia C63) y los pesos de financiación observados "
                "(capitalización C41 y deuda + arrendamientos C64). No es una estimación íntegra del coste de "
                "capital de mercado; exige moneda común y deuda bruta ≥ 0."),
    (CM, "F16", "Clasificación final (declarada por el analista; Excel no comprueba el dato)"),
    (CM, "F106", "Clasificación final (declarada por el analista; Excel no comprueba el dato)"),
    (CM, "J16", "Documento / emisor (fuente declarada)"),
    (CM, "J106", "Documento / emisor (fuente declarada)"),
    (MO, "A269", "ESTADO DE LAS EVIDENCIAS (Control maestro, resumen del bloque 176+)"),
    (PN, "C19", "Hip. base"),
    (PN, "K19", "Hip. base"),
    (PN, "B3", '="Evidencias: "&Motor!$B$269'),
]

GUIA_V63 = [
    ("A66", "V6.3 · Convenciones que antes no estaban escritas"),
    ("A67", "Historia: una celda vacía es un dato DESCONOCIDO, nunca cero. Para un cero comprobado escribe 0. "
            "El motor exige las partidas que usa en los períodos que usa (Motor V05, V23) y las medias "
            "históricas no se calculan con años incompletos."),
    ("A68", "Importes brutos y saldos (deuda, arrendamientos, caja, minoritarios, D&A, capex, intereses, SBC, "
            "I+D, acciones) no admiten negativos: la hoja los marca como DATOS INVÁLIDOS. FCF, resultados, "
            "circulante y adquisiciones netas sí pueden ser negativos. Pensiones (fila 25) es una posición neta: "
            "el déficit se resta y un superávit se trata como 0 con aviso."),
    ("A69", "Crecimiento: años 1–5 al ritmo de la palanca; años 6–10 baja en línea recta hasta el g para "
            "siempre, que se alcanza en el año 10. Margen (ROE en el motor C): sube en línea recta desde el "
            "último año hasta el objetivo en 5 años y se mantiene. En el terminal la reinversión es g ÷ ROIC."),
    ("A70", "Motor B: r operativa = r·E/(E+D) + i·(1−t)·D/(E+D), con E = capitalización (Análisis C41), "
            "D = deuda + arrendamientos del último año (Historia C64) e i = intereses ÷ deuda media "
            "(Historia C63). Es una tasa personalizada, no un coste de capital de mercado; exige moneda común."),
    ("A71", "Caja, deuda y ajustes se suman o restan al valor presente sin descontar (son saldos de hoy). La "
            "recuperación si quiebra se trata como valor presente. Los escenarios suponen supervivencia y el "
            "ajuste por quiebra se aplica una sola vez encima."),
    ("A72", "Evidencias (Control maestro, bloque 176+): cada entrada material del motor activo es un DATO (se "
            "documenta con fuente) o una HIPÓTESIS o decisión (r, crecimiento, márgenes, reinversión, rentabilidad y "
            "crecimiento terminales, probabilidades, quiebra, exceso de caja, FCF normalizado, motor, base del margen…: "
            "se razona y se confirma, nunca se presenta como hecho). LISTO solo con todo documentado y confirmado; "
            "LISTO · PROVISIONAL con estimaciones justificadas; NO LISTO con pendientes, no verificables, sin "
            "clasificar o un «No aplicable» indebido. Excel no comprueba la verdad de nada de esto."),
    ("A73", "Lo que los controles internos detectan: salidas sobrescritas por un valor (V39), una f que no "
            "cuadra con sus propios insumos (Historia C81) y datos fuera de dominio. Lo que NO detectan: una "
            "fórmula alterada que conserve el resultado o la manipulación de las propias reglas. Para eso está "
            "verificar_v63.py contra la referencia aprobada (referencia_V6.3.json)."),
]

VERSION = [
    (AN, "A1", lambda v: v.replace("V6.1", "V6.3")),
    (PN, "A1", lambda v: v.replace("DCF V6.1", "DCF V6.3")),
    ("Guía V6", "A1", lambda v: v.replace("V6.1", "V6.3")),
    (CM, "A3", lambda v: "Versión V6.3 (30-oct-2026, cobertura completa de evidencias) · ausencias ≠ cero · control de evidencias de datos e hipótesis por motor · "
                         "dominios económicos · conciliación de f con efecto en el estado · verificador externo "
                         "contra referencia aprobada. Detalle: Informe_V6_3.md"),
]

OPCIONES_F = '"Rellenado y verificado,Hipótesis confirmada,Estimación declarada,Pendiente de inversor,Dato no verificable,No aplicable"'


# ============================================================ aplicación
def _copiar_estilo(ws, origen, destino):
    ws[destino]._style = copy(ws[origen]._style)


def estilos_bloques_nuevos(wb):
    """La V6.2 escribió en filas sin tema (Diagnóstico 213+). Se copia el estilo del tema."""
    di = wb[DI]
    for r in range(213, 225):
        for col in "ABCD":
            _copiar_estilo(di, "B175" if col != "A" else "A175", f"{col}{r}")
    for col in "ABCD":
        _copiar_estilo(di, "A174", f"{col}213")          # cabecera de sección
    for r in (176, 177, 178):
        for col in "BCD":
            di[f"{col}{r}"].number_format = "0.0%"
    hi = wb[HI]
    for r in range(74, 81):
        hi[f"C{r}"].number_format = "#,##0.00"
    hi["C80"].number_format = "0.000%"
    cm = wb[CM]
    for r in range(174, FILA_NOTA + 1):                   # filas sin tema a partir de la 214
        for col in "ABCDEFGHIJKLMN":
            _copiar_estilo(cm, "A173", f"{col}{r}")
    for col in "ABCDEFGHIJKL":
        _copiar_estilo(cm, "A106", f"{col}178")           # cabecera de tabla
        _copiar_estilo(cm, "A105", f"{col}176")           # cabecera de sección
    _copiar_estilo(cm, "A105", f"A{RES}")
    cm[f"D{FILA['estado']}"].font = Font(name="Arial", size=11, bold=True, color="FFE6EDF3")
    for r in range(R0, R1 + 1):
        cm[f"A{r}"].number_format = "0"


def formatos_condicionales(wb):
    pn = wb[PN]
    for cf in pn.conditional_formatting:
        if str(cf.sqref) == "J2:N2":
            for rule in cf.rules:
                if rule.formula == ['LEFT($J$2,5)="LISTO"']:
                    rule.formula = ['$J$2="LISTO"']        # verde solo con LISTO a secas
    ambar = DifferentialStyle(font=Font(color="FFD29922"))
    azul = DifferentialStyle(font=Font(color="FF58A6FF"))
    verde = DifferentialStyle(font=Font(color="FF3FB950"))
    pn.conditional_formatting.add("J2:N2", Rule(type="expression", dxf=ambar,
                                                formula=['LEFT($J$2,19)="LISTO · PROVISIONAL"']))
    pn.conditional_formatting.add("B3:H3", Rule(type="expression", dxf=ambar,
                                                formula=['ISNUMBER(SEARCH("INCOMPLETAS",$B$3))']))
    pn.conditional_formatting.add("B3:H3", Rule(type="expression", dxf=azul,
                                                formula=['ISNUMBER(SEARCH("PROVISIONAL",$B$3))']))
    pn.conditional_formatting.add("B3:H3", Rule(type="expression", dxf=verde,
                                                formula=['LEFT($B$3,24)="Evidencias: documentadas"']))


def validaciones(wb):
    cm = wb[CM]
    for dv in cm.data_validations.dataValidation:
        if str(dv.sqref) in ("F17:F82", "F107:F173"):
            dv.formula1 = OPCIONES_F
        if str(dv.sqref) in ("F107:F173", "E107:E173"):
            dv.sqref = __import__("openpyxl").worksheet.cell_range.MultiCellRange(str(dv.sqref).replace("173", "175"))
    hi = wb[HI]
    dv_pos = DataValidation(type="decimal", operator="greaterThanOrEqual", formula1="0", allow_blank=True,
                            showErrorMessage=True, errorTitle="Importe no negativo",
                            error="Esta partida es un importe bruto o un saldo: no admite negativos. "
                                  "Si es cero comprobado escribe 0; si no lo conoces, deja la celda vacía.")
    for rng in ("C8:L8", "C12:L12", "C15:L19", "C22:L24", "C26:L26"):
        dv_pos.add(rng)
    hi.add_data_validation(dv_pos)
    dv_acc = DataValidation(type="decimal", operator="greaterThan", formula1="0", allow_blank=True,
                            showErrorMessage=True, errorTitle="Acciones",
                            error="Las acciones diluidas deben ser un número positivo.")
    dv_acc.add("C20:L20")
    hi.add_data_validation(dv_acc)


def main(src, dst, canonico=None):
    wb = load_workbook(src)
    registro = []
    base.aplicar_capa_v62(wb, registro)

    cm = wb[CM]
    for coord, val in TRAZABILIDAD_NUEVA:
        cm[coord] = val
    registro.append(("Control maestro!A174:E175", None, "filas de trazabilidad", "unidad financiera (J4) y norma contable (L4)"))
    for coord, val in bloque_evidencias():
        cm[coord] = val
    registro.append((f"Control maestro!A176:L{FILA_NOTA}", None, "bloque nuevo",
                     f"control de evidencias: {len(REL.ENTRADAS)} entradas materiales (datos e hipótesis) por motor y condición"))
    wb[MO]["B269"] = f"='Control maestro'!$D${FILA['estado']}"
    wb[MO]["B266"] = estado_libro_v63(wb[MO]["B266"].value)
    registro.append(("Motor!B266 · B269", None, "estado del libro y de las evidencias",
                     "LISTO solo con evidencias documentadas; PROVISIONAL con estimaciones"))
    wb[MO]["E236"] = _envolver(wb[MO]["E236"].value, CONCILIACION_INV)
    registro.append(("Motor!E236", None, "V39 + conciliación", "la conciliación de f bloquea el valor"))
    wb[MO]["E234"] = _envolver(wb[MO]["E234"].value, dominios_inv())
    wb[HI]["C65"] = HI_C65_V63
    wb[MO]["E223"] = _envolver(wb[MO]["E223"].value, AVISO_PENSIONES)
    registro.append(("Historia!C65 · Motor!E223", None, "pensiones", "superávit de pensiones = déficit 0, con aviso"))
    registro.append(("Motor!E234", None, "V37 + dominios", "importes brutos y saldos no admiten negativos"))
    for hoja, coord, txt in TEXTOS_V63:
        wb[hoja][coord] = txt
        registro.append((f"{hoja}!{coord}", None, str(txt)[:40], "texto V6.3"))
    g = wb['Guía V6']
    for coord, txt in GUIA_V63:
        g[coord] = txt
    for r in range(66, 74):
        g[f'A{r}']._style = copy(g['A26']._style)
    g['A66']._style = copy(g['A25']._style)
    registro.append(('Guía V6!A66:A73', None, 'bloque nuevo', 'convenciones V6.3 escritas'))
    for hoja, coord, fn in VERSION:
        wb[hoja][coord] = fn(str(wb[hoja][coord].value))
    registro.append(('etiquetas de versión', None, 'V6.3', 'Análisis A1, Panel A1, Guía A1, Control maestro A3'))
    validaciones(wb)
    formatos_condicionales(wb)
    estilos_bloques_nuevos(wb)

    wb.save(dst)
    restauradas = base.restaurar_partes(src, dst)
    if canonico:
        # Los gráficos de los ejemplos V6.1 habían perdido el fondo del área de trazado respecto a la
        # plantilla. Se toman los tres gráficos de la plantilla canónica: las series apuntan a las
        # mismas celdas de Motor en todos los libros y no llevan valores en caché.
        base.restaurar_partes(canonico, dst, prefijos=("xl/charts/",))
        registro.append(("xl/charts/chart1-3.xml", None, "canónicos", f"gráficos tomados de {os.path.basename(canonico)}"))
    for ref, _, _, motivo in registro:
        print(f"  {ref:<40} {motivo}")
    print(f"{len(registro)} cambios -> {dst}")
    print(f"  partes restauradas del original (gráficos y dibujos): {len(restauradas)}")


if __name__ == "__main__":
    _canon = sys.argv[sys.argv.index("--graficos-de") + 1] if "--graficos-de" in sys.argv else None
    main(sys.argv[1], sys.argv[2], _canon)
