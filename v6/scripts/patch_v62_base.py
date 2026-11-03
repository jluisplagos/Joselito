#!/usr/bin/env python3
"""Capa V6.2 (sin el bloque de evidencias, que la V6.3 rehace). La usa patch_v63.py.

No se ejecuta sola: importar desde patch_v63.py.
Dependencias: openpyxl >= 3.1
No usa rutas personales: todo entra por argumento.

CONVENCIÓN CENTRAL (V6.2): en la hoja Historia una celda vacía significa
DATO DESCONOCIDO, nunca cero. Para declarar un cero comprobado hay que
escribir 0. Las partidas que el motor seleccionado utiliza se exigen en los
períodos que el cálculo usa realmente.
"""
import os
import shutil
import sys
import zipfile
from openpyxl import load_workbook


def restaurar_partes(origen, destino, prefijos=("xl/charts/", "xl/drawings/")):
    """Devuelve a `destino` las partes XML que openpyxl reescribe sin necesidad.

    openpyxl serializa los títulos de eje vacíos como el texto «None», que se vería
    en los tres gráficos. Como esta corrección no toca los gráficos, se copian tal
    cual del archivo de origen.
    """
    zo = zipfile.ZipFile(origen)
    originales = {n: zo.read(n) for n in zo.namelist()
                  if any(n.startswith(p) for p in prefijos)}
    zo.close()
    # Los ejemplos de la V6.1 ya venían con «None» como título de eje (openpyxl
    # serializa así un título vacío). Se limpia aquí, no se propaga.
    for n, datos in list(originales.items()):
        if "charts/chart" in n and b"<a:t>None</a:t>" in datos:
            originales[n] = datos.replace(b"<a:t>None</a:t>", b"<a:t></a:t>")
    tmp = destino + ".tmp"
    zd = zipfile.ZipFile(destino)
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as salida:
        for item in zd.infolist():
            datos = originales.get(item.filename, zd.read(item.filename))
            salida.writestr(item, datos)
    zd.close()
    os.replace(tmp, destino)
    return sorted(originales)

HI, AN, PA, DI, MO, PN, CM = ("Historia", "Análisis", "Palancas",
                              "Diagnóstico V6", "Motor", "Panel", "Control maestro")

# --- helpers de fórmula -----------------------------------------------------
def falta_en_ventana(fila):
    """Nº de celdas vacías de `fila` dentro de la ventana de C57 años."""
    return (f'SUMPRODUCT(--(COLUMN($C$6:$L$6)>12-$C$57),--($C${fila}:$L${fila}=""))')

# Filas que la calibración de f usa de verdad (ver Historia C58):
#   6 ventas · 7 EBIT · 8 D&A · 10 tipo impositivo · 12 capex · 14 circulante
FILAS_F = (6, 7, 8, 10, 12, 14)

C58_NUEVA = (
    '=IF(OR(NOT(ISNUMBER($C$70)),NOT(ISNUMBER($C$57)),$C$57<1,$C$43<$C$57,'
    'SUMPRODUCT(--($C$6:$L$14<>""),--NOT(ISNUMBER($C$6:$L$14)))>0,'
    + ",".join(f'{falta_en_ventana(f)}>0' for f in FILAS_F) + '),"",'
    'IF(SUMPRODUCT(--(COLUMN($C$6:$L$6)>12-$C$57),$C$6:$L$6)<=0,"",'
    '((SUMPRODUCT(--(COLUMN($C$6:$L$6)>12-$C$57),$C$7:$L$7,1-$C$10:$L$10)'
    '-SUMPRODUCT(--(COLUMN($C$6:$L$6)>12-$C$57),$C$12:$L$12-$C$8:$L$8+$C$14:$L$14))'
    '/$C$57-$C$70)/(SUMPRODUCT(--(COLUMN($C$6:$L$6)>12-$C$57),$C$6:$L$6)/$C$57)))'
)

# Anclas de balance: una partida ausente no es cero.
C63_NUEVA = ('=IF(AND(ISNUMBER(L15),ISNUMBER(K22),ISNUMBER(L22),'
             'ISNUMBER(K23)=ISNUMBER(L23),(N(K22)+N(K23)+N(L22)+N(L23))>0),'
             'L15/((N(K22)+N(K23)+N(L22)+N(L23))/2),"")')
C64_NUEVA = '=IF(AND(ISNUMBER(L22),ISNUMBER(L23)),L22+L23,"")'
C65_NUEVA = '=IF(AND(ISNUMBER(L25),ISNUMBER(L26)),L25+L26,"")'

# Medias históricas: sin ausencias parciales dentro de la ventana usada.
C49_NUEVA = '=IF(AND(COUNT(C29:L29)>0,COUNT(C29:L29)=$C$43),AVERAGE(C29:L29),"")'
C52_NUEVA = '=IF(AND($C$43>0,COUNT(H10:L10)=MIN(5,$C$43)),AVERAGE(H10:L10),"")'
C55_NUEVA = ('=IF($C$68="Sí",IF(AND($C$43>0,COUNT(H38:L38)=MIN(5,$C$43)),AVERAGE(H38:L38),""),'
             'IF(AND($C$43>0,COUNT(H33:L33)=MIN(5,$C$43)),AVERAGE(H33:L33),""))')
C56_NUEVA = '=IF(AND($C$43>0,COUNT(H34:L34)=MIN(5,$C$43)),AVERAGE(H34:L34),"")'

# Puente a patrimonio del motor B: la caja desconocida no vale cero.
DI_C16_NUEVA = ('=IF($C5<>"B","—",IF(AND(ISNUMBER(Historia!$C$64),ISNUMBER(Historia!$C$65),'
                'ISNUMBER(Historia!$C$66)),Historia!$C$64+Historia!$C$65-Historia!$C$66,""))')

# --- reglas del Motor: la ausencia se declara con su causa concreta ---------
def _falta(fila):
    return ('SUMPRODUCT(--(COLUMN(Historia!$C$6:$L$6)>12-Historia!$C$57),'
            f'--(Historia!$C${fila}:$L${fila}=""))')

_CONCEPTOS_A = [
    (6,  "ventas (fila 6)"),
    (7,  "resultado operativo EBIT (fila 7)"),
    (8,  "amortizaciones D&A (fila 8)"),
    (10, "tipo impositivo efectivo (fila 10)"),
    (12, "capex (fila 12)"),
    (14, "aumento del circulante (fila 14)"),
]

_V05_COLA = "".join(
    f'IF({_falta(f)}>0,"INC|Motor A: faltan {txt} en algún año de la ventana que calibra f '
    '(Historia, últimos "&Historia!$C$57&" ejercicios); un hueco no vale cero",'
    for f, txt in _CONCEPTOS_A) + '""' + ")" * len(_CONCEPTOS_A)

V05_NUEVA = (
    '=IF(C205,IF(Historia!$C$57="","INC|Falta Historia C57 (años de la media del FCF base)",'
    'IF(NOT(ISNUMBER(Historia!$C$57)),"INV|Historia C57 no es un número",'
    'IF(Historia!$C$57<>INT(Historia!$C$57),"INV|Historia C57 ("&Historia!$C$57&") debe ser un número entero de ejercicios",'
    'IF(COUNT(Historia!$C$6:$L$6)=0,"",'
    'IF(OR(Historia!$C$57<1,Historia!$C$57>COUNT(Historia!$C$6:$L$6)),'
    '"INV|Historia C57 ("&Historia!$C$57&") fuera de rango: entre 1 y los ejercicios con ventas ("&COUNT(Historia!$C$6:$L$6)&")",'
    + _V05_COLA + '))))),"")'
)

C15_NUEVA = (
    '=IF($C5<>"B","—",IF(NOT(ISNUMBER(Historia!$C$64)),"",'
    'IF(AND(ISNUMBER(Análisis!$C$56),Historia!$C$64=0),Análisis!$C$56,'
    'IF(AND(ISNUMBER(Análisis!$C$56),ISNUMBER(Análisis!$C$41),N(Análisis!$C$41)>0,'
    "ISNUMBER(Historia!$C$63),EXACT(Palancas!$C48,'Control maestro'!$H$4)),"
    '(Análisis!$C$56*Análisis!$C$41+Historia!$C$63*(1-N($C11))*Historia!$C$64)'
    '/(Análisis!$C$41+Historia!$C$64),""))))'
)

V23_NUEVA = (
    '=IF(C223,'
    'IF(OR(AND(Historia!$L$15<>"",NOT(ISNUMBER(Historia!$L$15))),'
    'AND(Historia!$L$22<>"",NOT(ISNUMBER(Historia!$L$22))),'
    'AND(Historia!$L$23<>"",NOT(ISNUMBER(Historia!$L$23)))),'
    '"INV|Motor B: intereses o deuda del último año no numéricos (Historia L15, L22, L23)",'
    'IF(NOT(ISNUMBER(Historia!$C$64)),'
    '"INC|Motor B: falta la deuda o los arrendamientos del último año (Historia L22, L23); escribe 0 si no hay",'
    'IF(NOT(ISNUMBER(Historia!$L$24)),'
    '"INC|Motor B: falta la caja del último año (Historia L24); una caja desconocida no vale cero",'
    'IF(NOT(ISNUMBER(Historia!$C$65)),'
    '"INC|Motor B: faltan pensiones o minoritarios del último año (Historia L25, L26); escribe 0 si no hay",'
    "IF(OR(Palancas!$C48=\"\",'Control maestro'!$H$4=\"\"),"
    '"INC|Motor B: falta declarar la moneda de cotización (Palancas C48) o la del modelo '
    '(Control maestro H4): sin ambas no se puede comprobar que capitalización y deuda sean comparables",'
    "IF(NOT(EXACT(Palancas!$C48,'Control maestro'!$H$4)),"
    '"INV|Motor B: la capitalización está en "&Palancas!$C48&" y la deuda en "&'
    "'Control maestro'!$H$4&"
    '": los pesos de financiación no son comparables. Normaliza la capitalización a "&'
    "'Control maestro'!$H$4&"
    '" y concilia el importe en Control maestro (la hoja no convierte divisas)",'
    "IF(NOT(ISNUMBER('Diagnóstico V6'!$C15)),"
    '"INC|Motor B: no se puede calcular la r operativa (Historia L15, L22, L23 y Análisis C41)",'
    '""' + ")" * 7 + ',"")'
)

ETIQUETAS = [
    (HI, "B23", "Balance (IFRS 16) · escribe 0 si no hay; vacío = desconocido"),
    (HI, "B24", "Balance · escribe 0 si no hay; vacío = desconocido"),
    (HI, "B25", "Balance · escribe 0 si no hay; vacío = desconocido"),
    (HI, "B26", "Intereses no dominantes · escribe 0 si no hay; vacío = desconocido"),
]

# ---------------------------------------------------------------- Prioridad 2
# Conciliación legible de f (motor A), en filas libres de Historia (73-82).
_V = 'SUMPRODUCT(--(COLUMN($C$6:$L$6)>12-$C$57),'
_G = 'IF(NOT(ISNUMBER($C$58)),"",'

BLOQUE_F = [
    ("A73", "  CONCILIACIÓN DE f · motor A · sobre los últimos C57 ejercicios"),
    ("A74", "Ventas medias de la ventana"),
    ("C74", f'={_G}{_V}$C$6:$L$6)/$C$57)'),
    ("A75", "Resultado operativo después de impuestos (NOPAT) medio"),
    ("C75", f'={_G}{_V}$C$7:$L$7,1-$C$10:$L$10)/$C$57)'),
    ("A76", "Reinversión neta media (capex − D&A + circulante)"),
    ("C76", f'={_G}{_V}$C$12:$L$12-$C$8:$L$8+$C$14:$L$14)/$C$57)'),
    ("A77", "Flujo operativo implícito (NOPAT − reinversión)"),
    ("C77", '=IF(OR(NOT(ISNUMBER($C$75)),NOT(ISNUMBER($C$76))),"",$C$75-$C$76)'),
    ("A78", "FCF base que calibra f (Historia C70)"),
    ("C78", '=IF(NOT(ISNUMBER($C$58)),"",$C$70)'),
    ("A79", "Diferencia = fugas al accionista (mm por año)"),
    ("C79", '=IF(OR(NOT(ISNUMBER($C$77)),NOT(ISNUMBER($C$78))),"",$C$77-$C$78)'),
    ("A80", "f implícita = diferencia ÷ ventas medias"),
    ("C80", '=IF(OR(NOT(ISNUMBER($C$79)),NOT(ISNUMBER($C$74)),$C$74=0),"",$C$79/$C$74)'),
    ("A81", "Comprobación: coincide con C58"),
    ("C81", '=IF(OR(NOT(ISNUMBER($C$80)),NOT(ISNUMBER($C$58))),"—",'
            'IF(ABS($C$80-$C$58)<0.000000001,"✓ cuadra","⛔ TÉCNICO · la conciliación no cuadra"))'),
    ("A82", "Qué recoge f: la diferencia entre el flujo operativo que implica la historia y el FCF "
            "base declarado. Absorbe intereses, financiación neta, arrendamientos, SBC y adquisiciones "
            "en la medida en que el FCF base los recoja. Proyectarla como % constante de ventas supone "
            "que esa diferencia escala con el negocio; si la financiación cambia mucho, usa el motor B. "
            "Una f negativa no es un error: significa que el FCF base supera al flujo operativo implícito."),
]

# V19: un vacío en la probabilidad de quiebra es una convención, no un riesgo medido.
V19_NUEVA = (
    '=IF(C219,IF(Palancas!$C22="",'
    '"AVI|Probabilidad de quiebra vacía (Palancas C22): se asume 0 por convención, '
    'no es un riesgo medido",'
    'IF(OR(NOT(ISNUMBER(Palancas!$C22)),Palancas!$C22<0,Palancas!$C22>1),'
    '"INV|Probabilidad de quiebra fuera de [0, 1] (Palancas C22)","")),"")'
)

TEXTOS = [
    (HI, "A58", "Fugas al accionista (f, % de ventas) · conciliación en la fila 73"),
    (HI, "A63", "Coste de la deuda (intereses ÷ deuda media) · aproximación histórica, "
                "no el coste actual de financiación"),
    (DI, "A15", "r operativa · motor B · usa el coste histórico de la deuda y tu r exigida, "
                "no un coste de capital de mercado"),
    (DI, "A16", "Pasivos netos que se restan · motor B · deuda + arrendamientos + pensiones "
                "+ minoritarios − caja, todo del último año"),
    (PA, "A22", "Probabilidad de quiebra en 10 años (vacío = 0 por convención, no riesgo medido)"),
    (PA, "E22", "Las tablas por rating de Damodaran dan acumulados a 5 años (BBB ≈ 1,6 %; BB ≈ 6,5 %; "
                "B ≈ 16,9 %). Esta celda pide 10 años: no es el mismo horizonte y pasar de uno a otro "
                "exige una hipótesis explícita que anotes en Control maestro."),
    (PA, "A23", "Valor presente de lo que recuperaría el accionista si quiebra (mm)"),
    (PA, "E23", "Casi siempre 0. Se usa como valor presente, sin descontar: si piensas en un cobro "
                "futuro, descuéntalo tú y anota el momento y la tasa en Control maestro."),
]

# Bloque 10 · coherencia de la transición al terminal (años 10 -> 11).
def _marginal(col):
    return (f'=IF($C$5="C","—",IF(AND(ISNUMBER(Palancas!${col}$16),ISNUMBER(Palancas!${col}$15),'
            f'ISNUMBER(Historia!$C$52)),Palancas!${col}$16*Palancas!${col}$15*(1-Historia!$C$52),""))')

BLOQUE_TRANSICION = [
    ("A174", "  10 · COHERENCIA DE LA TRANSICIÓN AL TERMINAL (años 10 → 11)"),
    ("A175", "Concepto"), ("B175", "MALO"), ("C175", "NORMAL"), ("D175", "BUENO"),
    ("A176", "Rentabilidad marginal implícita en los años 1–10 (S2C × margen objetivo × (1 − t))"),
    ("B176", _marginal("B")), ("C176", _marginal("C")), ("D176", _marginal("D")),
    ("A177", "ROIC o ROE a largo plazo que usa el terminal (Palancas B18:D18)"),
    ("B177", '=IF(ISNUMBER(Palancas!$B$18),Palancas!$B$18,"")'),
    ("C177", '=IF(ISNUMBER(Palancas!$C$18),Palancas!$C$18,"")'),
    ("D177", '=IF(ISNUMBER(Palancas!$D$18),Palancas!$D$18,"")'),
    ("A178", "Salto en el año 11 (puntos; positivo = la rentabilidad marginal cae al pasar al terminal)"),
    ("B178", '=IF(OR(NOT(ISNUMBER(B176)),NOT(ISNUMBER(B177))),"",B176-B177)'),
    ("C178", '=IF(OR(NOT(ISNUMBER(C176)),NOT(ISNUMBER(C177))),"",C176-C177)'),
    ("D178", '=IF(OR(NOT(ISNUMBER(D176)),NOT(ISNUMBER(D177))),"",D176-D177)'),
    ("A179", "Umbral del aviso (puntos; ajustable)"), ("C179", 0.05),
    ("A180", "Durante los años 1–10 cada euro reinvertido rinde S2C × margen × (1 − t). El terminal usa "
             "el ROIC a largo plazo y reinvierte g ÷ ROIC. Si los dos no coinciden, en el año 11 cambia "
             "la rentabilidad del capital sin que nada lo diga: es una hipótesis tuya sobre la pérdida "
             "(o ganancia) de ventaja competitiva, y conviene escribirla en la tesis."),
]

AVISO_TRANSICION = (
    "IF(COUNT('Diagnóstico V6'!$B$178:$D$178)<>3,\"\","
    "IF(NOT(ISNUMBER('Diagnóstico V6'!$C$179)),\"\","
    'IF($C$5="C","",'
    "IF(MAX(ABS('Diagnóstico V6'!$B$178),ABS('Diagnóstico V6'!$C$178),"
    "ABS('Diagnóstico V6'!$D$178))<='Diagnóstico V6'!$C$179,\"\","
    '"AVI|La rentabilidad marginal de los años 1–10 y el ROIC del terminal se separan más de "&'
    'TEXT(\'Diagnóstico V6\'!$C$179*100,"0.#")&" puntos: el salto del año 11 es una hipótesis. '
    'Hazla explícita (Diagnóstico V6, bloque 10)"))))'
)

# Delimitación de los motores, unidad de las acciones y combinación quiebra/escenarios.
APENDICES = [
    (AN, "E55", " Usa las acciones vigentes en la fecha de valoración. La media diluida del ejercicio "
                "(Historia fila 20) es otra cosa: su diferencia con esta no es por sí sola un error, "
                "pero si la conciliación avisa, declara la causa en Palancas C47."),
    (AN, "E62", " El motor C es un modelo simplificado de patrimonio y ROE: sirve para ver si el "
                "reparto y el crecimiento del patrimonio son coherentes, y NO valida la solvencia ni "
                "el capital regulatorio de ningún banco o aseguradora."),
    (AN, "E75", " Ojo: la celda muestra valor terminal ÷ FCF del año 10, que incluye el factor de "
                "reinversión (1 − g ÷ ROIC) del terminal. No es (1 + g) ÷ (r − g): esa fórmula solo "
                "valdría si la reinversión no cambiara al pasar al año 11."),
]

NOTAS = [
    (PA, "A25", "Cómo se combinan la quiebra y los escenarios"),
    (PA, "E25", "Los tres escenarios se valoran suponiendo que la empresa sobrevive. El ajuste por "
                "quiebra se aplica después y una sola vez sobre cada escenario: valor = (1 − p) × valor "
                "del escenario + p × recuperación. Si tu r exigida ya lleva una prima por riesgo de "
                "quiebra, estarías contando el mismo riesgo dos veces."),
]

# ---------------------------------------------------------------- Prioridad 3
AN_E6 = ('=IF(Motor!$B$261=0,"Sin causas activas","Causas activas: "&Motor!$B$261&'
         '" · estado técnico: "&Motor!$B$255&" · inversión: "&Motor!$B$258)'
         '&" · "&Motor!$B$269')

# Nombres: ni el autor del resultado ni el umbral deben acreditar nada.
RENOMBRES = [
    (PN, "C19", "Hipótesis base"),
    (PN, "K19", "Hipótesis base"),
    (PN, "B26", "Pista:  ▒ rango del sector   ◆ media de la empresa   ● hipótesis base   ▲ tú.   "
                "El número gris (0–40, 20 = sin cambio) es el que mueve el deslizador; con el Modo "
                "estudio apagado, «Tú» es igual a la hipótesis base."),
    (DI, "A84", "ESTADO DEL LIBRO · LISTO = el cálculo está completo y pasa sus comprobaciones. "
                "No es una aprobación de inversión ni dice que los datos sean ciertos: mira el "
                "estado de las evidencias y las advertencias."),
    (DI, "A156", "Precio de referencia (convención configurable, no una orden de compra)"),
    (DI, "A157", "Convención: mín(valor del escenario MALO; k × valor ponderado). No garantiza "
                 "ningún margen de seguridad: es una regla, no una medida del riesgo."),
    (DI, "A158", "k · factor del precio de referencia (ajustable)"),
]

DI_C156 = ('=IF(OR(Motor!$B$254,NOT(ISNUMBER(Análisis!$B$78)),NOT(ISNUMBER(Análisis!$C$83)),'
           'NOT(ISNUMBER($C$158))),"",MIN(Análisis!$B$78,$C$158*Análisis!$C$83))')

PN_M25 = ('=IF(OR(Motor!$B$254,NOT(ISNUMBER(Análisis!$B$78)),NOT(ISNUMBER(Análisis!$C$83)),'
          "NOT(ISNUMBER('Diagnóstico V6'!$C$156))),"
          '""'
          ",\"precio de referencia \"&FIXED('Diagnóstico V6'!$C$156,2))")

# Bloque 11 · qué sostiene el valor (a partir del tornado que ya existe) y qué falta por resolver.
def _efecto(fila):
    return ('=IF(OR(NOT(ISNUMBER(Motor!$D$%d)),NOT(ISNUMBER(Motor!$E$%d))),"",'
            'MAX(ABS(Motor!$D$%d),ABS(Motor!$E$%d)))' % (fila, fila, fila, fila))

def _pct(destino, fila):
    return ('=IF(OR(NOT(ISNUMBER($B$%d)),NOT(ISNUMBER(Motor!$F$%d)),Motor!$F$%d=0),"",'
            '$B$%d/ABS(Motor!$F$%d))' % (destino, fila, fila, destino, fila))

BLOQUE_SOSTIENE = [("A213", "  11 · QUÉ SOSTIENE ESTE VALOR Y QUÉ LO PUEDE INVALIDAR"),
                   ("A214", "Palanca (sensibilidad del escenario NORMAL)"),
                   ("B214", "Mayor efecto por acción"), ("C214", "% sobre el valor NORMAL")]
for _i, _f in enumerate(range(174, 180)):
    _d = 215 + _i
    BLOQUE_SOSTIENE += [(f"A{_d}", f"=Motor!$A${_f}"), (f"B{_d}", _efecto(_f)), (f"C{_d}", _pct(_d, _f))]
BLOQUE_SOSTIENE += [
    ("A221", "La hipótesis que más condiciona el valor"),
    ("C221", '=IF(COUNT($B$215:$B$220)=0,"",INDEX($A$215:$A$220,'
             'MATCH(MAX($B$215:$B$220),$B$215:$B$220,0)))'),
    ("A222", "Incertidumbre material pendiente (escríbela tú, en una línea)"),
    ("A223", "Qué dato o documento la resolvería"),
    ("A224", "Las cifras de arriba salen del tornado que ya calcula la hoja: miden cuánto mueve el "
             "valor cada palanca dentro de su rango, no cuál es más probable. Las dos líneas de abajo "
             "son tuyas: la hoja no sabe qué desconoces del negocio y no va a inventarlo."),
]

_Q = chr(34)

AN_E83 = (
    "=" + _Q + "Solo calcula si los 3 escenarios tienen valor y las probabilidades suman 1." + _Q
    + "&IF('Diagnóstico V6'!$C$221=" + _Q + _Q + "," + _Q + _Q + ","
    + _Q + " · La palanca que más mueve este valor: " + _Q
    + "&'Diagnóstico V6'!$C$221&IF(ISNUMBER('Diagnóstico V6'!$B$215),"
    + _Q + " (hasta " + _Q + "&FIXED(MAX('Diagnóstico V6'!$B$215:$B$220),2)&"
    + _Q + " por acción)" + _Q + "," + _Q + _Q + "))"
)

# Análisis C48 y C49 (intereses en financiación y principal de arrendamientos) entraban
# en el FCF base como cero cuando estaban vacíos. Se exige el dato o un 0 explícito.
AN_C52 = ('=IF(OR(NOT(ISNUMBER(C46)),NOT(ISNUMBER(C47)),NOT(ISNUMBER(C48)),'
          'NOT(ISNUMBER(C49)),NOT(ISNUMBER(C50)),'
          'NOT(OR(EXACT(C51,"Sí"),EXACT(C51,"No"))),N(C47)<0),"",'
          'C46-C47-C48-C49-IF(EXACT(C51,"No"),0,C50))')

AN_C59 = ('=IF(OR(NOT(ISNUMBER(C46)),NOT(ISNUMBER(C47)),NOT(ISNUMBER(C48)),'
          'NOT(ISNUMBER(C49)),NOT(ISNUMBER(C50))),"",'
          'IF((C46-C47-C48-C49)<=0,"",C50/(C46-C47-C48-C49)))')

V09_COLA = ('IF(AND(\'Diagnóstico V6\'!$C5="A",OR(Análisis!$C$48="",Análisis!$C$49="")),'
            '"INC|Faltan intereses en financiación o principal de arrendamientos '
            '(Análisis C48, C49): escribe 0 si la empresa no tiene; un vacío no es un cero",'
            '"")')

CAMBIOS = [
    (HI, "C49", C49_NUEVA, "media de márgenes: exige la serie completa, no una media parcial"),
    (HI, "C52", C52_NUEVA, "tipo impositivo medio: exige los años de la ventana, no una media parcial"),
    (HI, "C55", C55_NUEVA, "ROIC medio: exige los años de la ventana"),
    (HI, "C56", C56_NUEVA, "ROE medio: exige los años de la ventana"),
    (HI, "C58", C58_NUEVA, "f: exige ventas, EBIT, D&A, tipo, capex y circulante en CADA año de la ventana"),
    (HI, "C63", C63_NUEVA, "coste de la deuda: perímetro consistente; deuda ausente no es cero"),
    (HI, "C64", C64_NUEVA, "deuda + arrendamientos: arrendamientos ausentes no son cero"),
    (HI, "C65", C65_NUEVA, "pensiones + minoritarios: ausentes no son cero"),
    (DI, "C16", DI_C16_NUEVA, "pasivos netos: caja ausente no es cero (caso B)"),
    (MO, "E205", V05_NUEVA, "V05: nombra el concepto que falta en la ventana de f (motor A)"),
    (AN, "E83", AN_E83, "junto al valor ponderado: la palanca que más lo condiciona"),
    (AN, "C52", AN_C52, "FCF base: C48 y C49 vacíos ya no valen cero"),
    (AN, "C59", AN_C59, "peso de la SBC: mismo criterio que C52"),
    (AN, "E6", AN_E6, "junto al veredicto: estado técnico + estado de las evidencias"),
    (DI, "C156", DI_C156, "precio de referencia con factor k configurable"),
    (PN, "M25", PN_M25, "Panel: «precio de referencia», no «precio de Sí»"),
    (DI, "C15", C15_NUEVA, "r operativa: deuda desconocida no es «sin deuda»; exige moneda común"),
    (MO, "E219", V19_NUEVA, "V19: el vacío de la probabilidad de quiebra se declara como convención"),
    (MO, "E223", V23_NUEVA, "V23: exige caja, pensiones y minoritarios del motor B con causa concreta"),
]

def aplicar_capa_v62(wb, registro):
    """Aplica la capa V6.2 sobre un libro abierto (sin guardar)."""
    for hoja, coord, nueva, motivo in CAMBIOS:
        ws = wb[hoja]
        antes = ws[coord].value
        ws[coord] = nueva
        registro.append((f"{hoja}!{coord}", antes, nueva, motivo))
    _v09 = wb[MO]['E209'].value[1:]
    wb[MO]['E209'] = '=IF(' + _v09 + '<>"",' + _v09 + ',' + V09_COLA + ')'
    registro.append(('Motor!E209', None, 'V09 + ausencia', 'C48/C49 ausentes bloquean con causa'))
    _v16 = wb[MO]['E216'].value[1:]
    wb[MO]['E216'] = '=IF(' + _v16 + '<>"",' + _v16 + ',' + AVISO_TRANSICION.replace("$C$5", "'Diagnóstico V6'!$C5") + ')'
    registro.append(('Motor!E216', None, 'V16 + aviso', 'avisa del salto de rentabilidad en el año 11'))
    for coord, val in BLOQUE_SOSTIENE:
        wb[DI][coord] = val
    registro.append(('Diagnóstico V6!A213:C224', None, 'bloque nuevo',
                     'qué sostiene el valor, incertidumbre pendiente y qué la resolvería'))
    wb[DI]['C158'] = 0.75
    for hoja, coord, txt in RENOMBRES:
        wb[hoja][coord] = txt
    registro.append(('Panel C19/K19/B26 · Diagnóstico A84/A156:A158', None, 'renombrados',
                     '«Hipótesis base» en vez de «Munger»; «precio de referencia» con k ajustable'))
    for hoja, coord, cola in APENDICES:
        wb[hoja][coord] = (str(wb[hoja][coord].value or '').rstrip() + cola)
        registro.append((f'{hoja}!{coord}', None, cola.strip()[:40], 'delimitación del alcance'))
    for hoja, coord, txt in NOTAS:
        wb[hoja][coord] = txt
        registro.append((f'{hoja}!{coord}', None, txt[:40], 'convención: escenarios condicionales a la supervivencia'))
    for coord, val in BLOQUE_TRANSICION:
        wb[DI][coord] = val
    registro.append(('Diagnóstico V6!A174:D180', None, 'bloque nuevo', 'coherencia de la transición al terminal'))
    for coord, val in BLOQUE_F:
        wb[HI][coord] = val
    registro.append(('Historia!A73:C82', None, 'bloque nuevo', 'conciliación legible de f (motor A)'))
    for hoja, coord, txt in TEXTOS:
        wb[hoja][coord] = txt
        registro.append((f'{hoja}!{coord}', None, txt, 'texto: convención explícita'))
    for hoja, coord, txt in ETIQUETAS:
        wb[hoja][coord] = txt
        registro.append((f'{hoja}!{coord}', None, txt, 'etiqueta: vacío = desconocido'))
