# -*- coding: utf-8 -*-
"""Construye la plantilla V6 a partir de la V5.3 sin mover ninguna celda de Análisis.

Hojas nuevas: Panel (primera), Palancas (lo que se rellena), Diagnóstico V6 (lo que se calcula),
Historia, Sector, Riesgo país, Guía V6 y Motor (oculta).
Uso: python3 build_v6.py plantilla_v53.xlsx Plantilla_V6.xlsx
"""
import json, sys, os, datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter as CL
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.workbook.properties import CalcProperties
from openpyxl.chart import LineChart, BarChart, Reference
from openpyxl.chart.data_source import AxDataSource, StrRef

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = sys.argv[1], sys.argv[2]
wb = openpyxl.load_workbook(SRC)
AN, CM, OP = wb['Análisis'], wb['Control maestro'], wb['Opciones']

# ---------------------------------------------------------------- paleta sobria
INK, MUTED, WHITE = 'FF000000', 'FF595959', 'FFFFFFFF'
TITLE_BG, BAND_BG, SUB_BG, HDR_BG = '1F3A4D', '2E6E78', 'DCE6EC', 'F2F2F2'
IN_BG, IN_FG, ACCENT = 'FFF6CC', 'FF0000FF', 'FF1F4E79'
GOOD_BG, WARN_BG, BAD_BG = 'C6EFCE', 'FFE699', 'F8CBAD'
GOOD_FG, WARN_FG, BAD_FG = 'FF006100', 'FF7F6000', 'FF9C0006'
BLUE_D, BLUE_M, BLUE_L, GRAY = '1F4E79', '2E75B6', '9DC3E6', '808080'
F = 'Arial'
THIN = Side(style='thin', color='FFD0D0D0')
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
PCT, PCT2 = '0.0%;[Red]\\(0.0%\\);\\-', '0.00%;[Red]\\(0.00%\\);\\-'
NUM, NUM2 = '#,##0;[Red]\\(#,##0\\);\\-', '#,##0.00;[Red]\\(#,##0.00\\);\\-'
NUM1, MULT, DEC2 = '#,##0.0;[Red]\\(#,##0.0\\);\\-', '0.0"x";[Red]\\(0.0"x"\\);\\-', '0.00'


def fill(h):
    return PatternFill('solid', fgColor='FF' + h)


def title(ws, row, text, c2=10):
    for c in range(1, c2 + 1):
        ws.cell(row, c).fill = fill(TITLE_BG)
    x = ws.cell(row, 1, text)
    x.font = Font(name=F, size=14, bold=True, color=WHITE)
    x.alignment = Alignment(vertical='center', indent=1)
    ws.row_dimensions[row].height = 26


def band(ws, row, text, c2=10):
    for c in range(1, c2 + 1):
        ws.cell(row, c).fill = fill(BAND_BG)
    x = ws.cell(row, 1, text)
    x.font = Font(name=F, size=11, bold=True, color=WHITE)
    x.alignment = Alignment(vertical='center', indent=1)
    ws.row_dimensions[row].height = 20


def subband(ws, row, text, c2=10):
    for c in range(1, c2 + 1):
        ws.cell(row, c).fill = fill(SUB_BG)
    x = ws.cell(row, 1, text)
    x.font = Font(name=F, size=10, bold=True)
    x.alignment = Alignment(vertical='center', indent=1)


def header(ws, row, values, c1=1):
    for i, v in enumerate(values):
        c = ws.cell(row, c1 + i, v)
        c.font = Font(name=F, size=10, bold=True)
        c.fill = fill(HDR_BG)
        c.border = BOX
        c.alignment = Alignment(wrap_text=True, vertical='center')
    ws.row_dimensions[row].height = 30


def label(ws, ref, text, bold=False, size=10):
    c = ws[ref]
    c.value = text
    c.font = Font(name=F, size=size, bold=bold)
    c.alignment = Alignment(vertical='center', indent=1)
    return c


def inp(ws, ref, value=None, fmt=None):
    c = ws[ref]
    if value is not None:
        c.value = value
    c.font = Font(name=F, size=10, color=IN_FG)
    c.fill = fill(IN_BG)
    c.border = BOX
    c.alignment = Alignment(vertical='center', horizontal='right' if fmt else 'left', indent=1)
    if fmt:
        c.number_format = fmt
    return c


def out(ws, ref, formula, fmt=None, bold=False, size=10, wrap=False, color=None):
    c = ws[ref]
    c.value = formula
    c.font = Font(name=F, size=size, bold=bold, color=color)
    c.alignment = Alignment(vertical='center', wrap_text=wrap,
                            horizontal='right' if fmt else 'left', indent=1)
    if fmt:
        c.number_format = fmt
    return c


def note(ws, ref, text, size=10):
    c = ws[ref]
    c.value = text
    c.font = Font(name=F, size=size, color=MUTED)
    c.alignment = Alignment(wrap_text=True, vertical='center', indent=1)
    return c


def dv_list(ws, sqref, formula, strict=True, prompt=None):
    dv = DataValidation(type='list', formula1=formula, allow_blank=True, showErrorMessage=strict)
    if prompt:
        dv.promptTitle, dv.prompt, dv.showInputMessage = 'V6', prompt, True
    ws.add_data_validation(dv)
    dv.add(sqref)
    return dv


def verdict_cf(ws, rng):
    first = rng.split(':')[0].replace('$', '')
    for word, bg, fg in (('BANDERA', BAD_BG, BAD_FG), ('TÉCNICO', BAD_BG, BAD_FG), ('REVISAR', WARN_BG, WARN_FG), ('PASA', GOOD_BG, GOOD_FG)):
        ws.conditional_formatting.add(rng, FormulaRule(formula=[f'ISNUMBER(SEARCH("{word}",{first}))'],
                                                       fill=fill(bg), font=Font(color=fg, bold=(word == 'BANDERA'))))


def widths(ws, spec):
    for k, w in spec.items():
        ws.column_dimensions[k].width = w


# ---------------------------------------------------------------- nombres de hoja
PAL, DG, HI, MO, SE = 'Palancas', "'Diagnóstico V6'", 'Historia', 'Motor', 'Sector'
AGG0_PLACEHOLDER = 252   # fila de «BLOQUEO DEL VALOR» en Motor (se verifica con un assert al construir Motor)
GATEP_PLACEHOLDER = f"Motor!$B${AGG0_PLACEHOLDER + 2}"   # BLOQUEO DE LA LECTURA DE PRECIO
RP, PA = "'Riesgo país'", 'Panel'
# direcciones clave (una sola fuente de verdad)
C_ETAPA, C_CASO, C_SECTOR, C_BASE, C_IDA, C_IDV = 'C5', 'C6', 'C7', 'C8', 'C9', 'C10'
R_CREC, R_MARG, R_S2C, R_G, R_ROIC = 14, 15, 16, 17, 18
C_PQ, C_REC, C_MKT = 'C22', 'C23', 'C24'
C_FCFNAT, C_FCFNORM, C_FPRECIO, C_FACC, C_CAUSA, C_MONEDA = 'C43', 'C44', 'C45', 'C46', 'C47', 'C48'
MONEDA_MODELO = "'Control maestro'!$H$4"
RATIO_ADR = "'Control maestro'!$D$5"
PAIS0, PRED0 = 28, 38
D_MOTOR, D_COHER = 'C5', 'C6'
D_V0, D_M0, D_TAU, D_F, D_B0, D_ROE0, D_ROP, D_PAS, D_RMIN, D_RVS = \
    'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18'
RES0 = 22          # primera fila de resultados en Diagnóstico
R_GFCF = RES0 + 3  # crecimiento del FCF implícito → Análisis B67:D67
DIAG0 = 40         # primer semáforo
DIAGN = 11         # número de semáforos
PG0 = 53           # «cuánto pagas por crecer»
MU0 = 61           # múltiplos
AC0 = 69           # autocomprobaciones
ACN = 15

# ================================================================== Opciones
etapas = ['Joven (sin beneficios estables)', 'En crecimiento', 'Madura en crecimiento', 'Madura', 'En declive']
casos = ['Ninguno', 'Financiera (banco o aseguradora)', 'Regulada (red, concesión)', 'Cíclica o materias primas',
         'Intangibles (I+D, marca)', 'Emergente (riesgo país)', 'Multinegocio o conglomerado']
c62 = ['Sí', 'No · financiación cambia mucho', 'No · banco o aseguradora',
       'No · este tipo de empresa requiere otro método']
LISTAS = [('K', 'Etapa del ciclo de vida', etapas, 'Lista_Etapa'), ('L', 'Caso especial', casos, 'Lista_Caso'),
          ('M', 'Base de partida', ['Último año', 'Media del ciclo'], 'Lista_Base'),
          ('N', 'Sí / No', ['Sí', 'No'], 'Lista_SiNo'),
          ('O', 'Escenario (Panel)', ['MALO', 'NORMAL', 'BUENO'], 'Lista_Escenario'),
          ('P', 'Modo estudio', ['ON', 'OFF'], 'Lista_OnOff'),
          ('Q', 'Aplicabilidad / motor (C62)', c62, 'Lista_C62'),
          ('R', 'Naturaleza del FCF base ≤ 0', ['No aplica', 'Transitorio', 'Extraordinario', 'Estructural'], 'Lista_FCFNat'),
          ('S', 'Causa de la diferencia de capitalización',
           ['Ninguna', 'ADR o ADS', 'Split o contrasplit', 'Básicas frente a diluidas', 'Fechas distintas',
            'Otra (explicada en Control maestro)'], 'Lista_CausaCap')]
for col, hdr, vals, name in LISTAS:
    c = OP[f'{col}2']
    c.value = hdr
    c.font = Font(name=F, size=10, bold=True)
    for i, v in enumerate(vals):
        OP[f'{col}{3 + i}'] = v
    OP.column_dimensions[col].width = 40
    wb.defined_names[name] = DefinedName(name, attr_text=f'Opciones!${col}$3:${col}${2 + len(vals)}')

# ================================================================== Sector
sect = [s for s in json.load(open(os.path.join(HERE, 'sectores.json'))) if not s['name'].startswith('Total Market')]
S = wb.create_sheet(SE)
title(S, 1, '  SECTOR · cuartiles y medias de Damodaran', 20)
note(S, 'A2', 'Archivos Ginzu de Damodaran (fcffsimpleginzu), datos de enero de 2026. Crecimiento de ventas a 3 años; '
               'margen operativo antes de impuestos; S2C = ventas ÷ capital invertido (medida MEDIA, no marginal). '
               'Se actualiza cada enero pegando la tabla nueva sobre estas mismas columnas.')
S.merge_cells('A2:T2')
S.row_dimensions[2].height = 32
label(S, 'A3', 'Fecha de las tablas de sector (actualízala al pegar tablas nuevas)', bold=True)
inp(S, 'B3', datetime.date(2026, 1, 1), 'yyyy-mm-dd')
note(S, 'C3', 'La usa la comprobación de vigencia (Diagnóstico V6, parámetro C94).')
S.merge_cells('C3:H3')
header(S, 4, ['Sector (Damodaran)', 'Nº empresas', 'Crec. Q1', 'Crec. mediana', 'Crec. Q3', 'Margen Q1',
              'Margen mediana', 'Margen Q3', 'S2C medio Q1', 'S2C medio mediana', 'S2C medio Q3', 'ROIC (media)',
              'Coste de capital', 'EV/Ventas', 'EV/EBITDA', 'Precio/Valor contable', 'ROE', 'Tasa de reinversión',
              'Margen medio', 'Crec. 5 años'])
for i, s in enumerate(sect):
    r = 5 + i
    vals = [s['name'], s['n']] + s['gq'] + s['mq'] + s['sq'] + [s['roic'], s['coc'], s['evs'], s['eve'], s['pb'],
                                                               s['roe'], s['rr'], s['m'], s['g5']]
    for j, v in enumerate(vals):
        c = S.cell(r, 1 + j, v)
        c.font = Font(name=F, size=10)
        n = 1 + j
        if 3 <= n <= 8 or n in (12, 13, 17, 18, 19, 20):
            c.number_format = PCT
        elif 9 <= n <= 11:
            c.number_format = DEC2
        elif 14 <= n <= 16:
            c.number_format = MULT
SEC_LAST = 4 + len(sect)
widths(S, {'A': 34, **{CL(c): 12 for c in range(2, 21)}})
S.freeze_panes = 'B5'
wb.defined_names['Lista_Sectores'] = DefinedName('Lista_Sectores', attr_text=f'Sector!$A$5:$A${SEC_LAST}')
SEC_COL = {'gq1': 'C', 'gmed': 'D', 'gq3': 'E', 'mq1': 'F', 'mmed': 'G', 'mq3': 'H',
           'sq1': 'I', 'smed': 'J', 'sq3': 'K', 'roic': 'L', 'evs': 'N', 'eve': 'O', 'pb': 'P', 'roe': 'Q'}


def sect_of(key):
    c = SEC_COL[key]
    return f'IFERROR(INDEX(Sector!${c}$5:${c}${SEC_LAST},MATCH({PAL}!${C_SECTOR},Sector!$A$5:$A${SEC_LAST},0)),"")'


# ================================================================== Riesgo país
paises = json.load(open(os.path.join(HERE, 'paises.json')))
regiones = [('Región · Western Europe', 0.009235465455893092), ('Región · North America', 0.001093176839097354),
            ('Región · Asia', 0.04389385452476601), ('Región · Central and South America', 0.05748136916616984),
            ('Región · Eastern Europe & Russia', 0.04680664819022259), ('Región · Middle East', 0.04651642971936808),
            ('Región · Africa', 0.07852163271737761), ('Región · Australia & New Zealand', 0.014837359275977242),
            ('Región · Caribbean', 0.05851953133049615)]
R = wb.create_sheet('Riesgo país')
title(R, 1, '  RIESGO PAÍS · prima por país de Damodaran (1-jul-2026)', 5)
label(R, 'A2', 'Fecha de las primas por país', bold=True)
inp(R, 'B2', datetime.date(2026, 7, 1), 'yyyy-mm-dd')
note(R, 'D2', 'La usa la comprobación de vigencia (Diagnóstico V6, parámetro C94).')
label(R, 'A3', 'Prima madura de renta variable (mercado Aaa)', bold=True)
inp(R, 'C3', 0.042, PCT)
note(R, 'D3', 'Damodaran, 1-jul-2026. Entra en la r mínima.')
header(R, 5, ['País o región', 'Región', 'Rating Moody\'s', 'Prima país (CRP)', 'Prima total (ERP)'])
rr = 6
for p in paises:
    R.cell(rr, 1, p[0]); R.cell(rr, 2, p[1]); R.cell(rr, 3, p[2])
    R.cell(rr, 4, p[3]).number_format = PCT2
    R.cell(rr, 5, p[4]).number_format = PCT2
    rr += 1
for nm, crp in regiones:
    R.cell(rr, 1, nm); R.cell(rr, 2, 'Media simple de la región')
    R.cell(rr, 4, crp).number_format = PCT2
    rr += 1
RP_LAST = rr - 1
for row in R.iter_rows(min_row=6, max_row=RP_LAST):
    for c in row:
        c.font = Font(name=F, size=10)
widths(R, {'A': 38, 'B': 28, 'C': 14, 'D': 14, 'E': 14})
R.freeze_panes = 'A6'
wb.defined_names['Lista_Paises'] = DefinedName('Lista_Paises', attr_text=f"'Riesgo país'!$A$6:$A${RP_LAST}")

# ================================================================== Historia
H = wb.create_sheet(HI)
title(H, 1, '  HISTORIA · 10 años de datos y anclas de la empresa', 13)
note(H, 'A2', 'Una columna por año, del más antiguo (C) al más reciente (L). Con menos de 10 años, deja vacías las '
               'primeras columnas: el año más reciente va SIEMPRE en L. Millones y moneda del modelo, como en Análisis. '
               'Capex, adquisiciones y SBC en positivo. El aumento del circulante, en positivo cuando consume caja.')
H.merge_cells('A2:M2')
H.row_dimensions[2].height = 34
header(H, 4, ['Concepto', 'Nota'] + [f'Año {i}' for i in range(1, 11)] + ['Fuente / observación'])
HROWS = [
    (5, 'Año fiscal (ej. 2025)', 'Número de año', '0'),
    (6, 'Ventas', 'Cuenta de resultados', NUM),
    (7, 'Resultado operativo (EBIT)', 'Antes de intereses e impuestos', NUM),
    (8, 'Amortizaciones (D&A)', 'Estado de flujos', NUM),
    (9, 'Beneficio neto atribuible', 'Cuenta de resultados', NUM),
    (10, 'Tipo impositivo efectivo', 'Impuesto ÷ beneficio antes de impuestos', PCT),
    (11, 'Caja de las operaciones (CFO)', 'Estado de flujos', NUM),
    (12, 'Capex (positivo)', 'Estado de flujos', NUM),
    (13, 'Adquisiciones netas (positivo)', 'Compras − ventas de negocios', NUM),
    (14, 'Aumento del circulante (+ consume caja)', 'Cambio en capital circulante', NUM),
    (15, 'Intereses pagados (total)', 'Estado de flujos o nota de deuda', NUM),
    (16, 'Intereses pagados en financiación (IFRS)', 'Solo la parte en financiación', NUM),
    (17, 'Principal de arrendamientos (IFRS 16)', 'Estado de flujos, financiación', NUM),
    (18, 'SBC (compensación en acciones)', 'Estado de flujos', NUM),
    (19, 'I+D (gasto del año)', 'Vacío si no tiene', NUM),
    (20, 'Acciones diluidas (mm)', 'Media diluida del año', NUM1),
    (21, 'Patrimonio neto atribuible', 'Balance al cierre', NUM),
    (22, 'Deuda financiera', 'Corto + largo plazo, sin arrendamientos', NUM),
    (23, 'Pasivo por arrendamientos', 'Balance (IFRS 16)', NUM),
    (24, 'Caja y equivalentes', 'Balance', NUM),
    (25, 'Déficit neto de pensiones', '0 si no hay', NUM),
    (26, 'Minoritarios', 'Intereses no dominantes', NUM),
]
for r, nm, nt, fmt in HROWS:
    label(H, f'A{r}', nm)
    note(H, f'B{r}', nt)
    for col in range(3, 13):
        inp(H, f'{CL(col)}{r}', None, fmt)
subband(H, 27, 'Series calculadas (no tocar)', 13)
DROWS = [
    (28, 'Crecimiento de ventas', PCT), (29, 'Margen EBIT', PCT),
    (30, 'Reinversión neta orgánica (capex − D&A + circulante)', NUM),
    (31, 'Reinversión neta total (+ adquisiciones)', NUM),
    (32, 'Capital invertido (patrimonio + deuda + arrend. − caja)', NUM),
    (33, 'ROIC (EBIT × (1 − t) ÷ capital invertido)', PCT), (34, 'ROE (beneficio ÷ patrimonio)', PCT),
    (35, 'FCF al accionista (CFO − capex − int. fin. − arrend. − SBC)', NUM),
    (36, 'Activo de I+D capitalizado', NUM), (37, 'Amortización del activo de I+D', NUM),
    (38, 'ROIC con I+D como inversión', PCT),
]
for r, nm, fmt in DROWS:
    label(H, f'A{r}', nm)
    for col in range(3, 13):
        x, pv = CL(col), CL(col - 1)
        f_ = {
            28: '' if col == 3 else f'=IF(AND(ISNUMBER({x}6),ISNUMBER({pv}6),N({pv}6)>0),{x}6/{pv}6-1,"")',
            29: f'=IF(AND(ISNUMBER({x}7),ISNUMBER({x}6),N({x}6)<>0),{x}7/{x}6,"")',
            30: f'=IF(AND(ISNUMBER({x}12),ISNUMBER({x}8)),{x}12-{x}8+N({x}14),"")',
            31: f'=IF(ISNUMBER({x}30),{x}30+N({x}13),"")',
            32: f'=IF(AND(ISNUMBER({x}21),ISNUMBER({x}22)),{x}21+{x}22+N({x}23)-N({x}24),"")',
            33: f'=IF(AND(ISNUMBER({x}7),ISNUMBER({x}32),N({x}32)>0),{x}7*(1-N({x}10))/{x}32,"")',
            34: f'=IF(AND(ISNUMBER({x}9),ISNUMBER({x}21),N({x}21)>0),{x}9/{x}21,"")',
            35: f'=IF(AND(ISNUMBER({x}11),ISNUMBER({x}12)),{x}11-{x}12-N({x}16)-N({x}17)-N({x}18),"")',
            36: (f'=IF(AND($C$68="Sí",ISNUMBER($C$69),$C$69>=1,ISNUMBER({x}19)),SUMPRODUCT($C$19:{x}19,'
                 f'(($C$69-(COLUMN({x}19)-COLUMN($C$19:{x}19)))/$C$69)*((COLUMN({x}19)-COLUMN($C$19:{x}19))<$C$69)),"")'),
            37: ('' if col == 3 else
                 f'=IF(AND($C$68="Sí",ISNUMBER($C$69),$C$69>=1,ISNUMBER({x}19)),SUMPRODUCT($C$19:{pv}19,'
                 f'((COLUMN({x}19)-COLUMN($C$19:{pv}19))<=$C$69)/$C$69),"")'),
            38: (f'=IF(AND(ISNUMBER({x}7),ISNUMBER({x}32),ISNUMBER({x}36)),({x}7+N({x}19)-N({x}37))*(1-N({x}10))'
                 f'/({x}32+{x}36),"")'),
        }[r]
        out(H, f'{x}{r}', f_ or None, fmt)
band(H, 41, '  ANCLAS DE LA EMPRESA (se calculan solas)', 13)
header(H, 42, ['Ancla', '', 'Valor', 'Qué es y para qué sirve'])
H.merge_cells('A42:B42')
ANC = [
    (43, 'Años con ventas', '=COUNT(C6:L6)', '0', 'Mínimo 5 para que las anclas sirvan.'),
    (44, 'Ventas del último año (V0)', '=IF(ISNUMBER(L6),L6,"")', NUM, 'Base de los motores A y B.'),
    (45, 'Crecimiento anual de ventas · 3 años',
     '=IF(AND(ISNUMBER(L6),ISNUMBER(I6),N(I6)>0,N(L6)>0),(L6/I6)^(1/3)-1,"")', PCT, ''),
    (46, 'Crecimiento anual de ventas · 5 años',
     '=IF(AND(ISNUMBER(L6),ISNUMBER(G6),N(G6)>0,N(L6)>0),(L6/G6)^(1/5)-1,"")', PCT,
     'Ancla del crecimiento en la hoja Palancas.'),
    (47, 'Crecimiento anual de ventas · toda la serie',
     '=IF(AND(C43>=3,ISNUMBER(L6),N(L6)>0),IF(N(INDEX(C6:L6,11-C43))>0,(L6/INDEX(C6:L6,11-C43))^(1/(C43-1))-1,""),"")',
     PCT, 'Crecer más de 1,5 veces esto pide explicación.'),
    (48, 'Margen EBIT del último año', '=IF(ISNUMBER(L29),L29,"")', PCT, 'Base «último año».'),
    (49, 'Margen EBIT medio (toda la serie)', '=IF(COUNT(C29:L29)>0,AVERAGE(C29:L29),"")', PCT,
     'Base «media del ciclo» y ancla del margen.'),
    (50, 'Margen EBIT mínimo', '=IF(COUNT(C29:L29)>0,MIN(C29:L29),"")', PCT, ''),
    (51, 'Margen EBIT máximo', '=IF(COUNT(C29:L29)>0,MAX(C29:L29),"")', PCT,
     'Un margen objetivo por encima de esto pide explicación.'),
    (52, 'Tipo impositivo medio · 5 años', '=IF(COUNT(H10:L10)>0,AVERAGE(H10:L10),"")', PCT, 'Impuesto del motor.'),
    (53, 'S2C MARGINAL · 5 años (ventas nuevas por euro reinvertido)',
     '=IF(AND(ISNUMBER(L6),ISNUMBER(G6),COUNT(H31:L31)>=3),IF(SUM(H31:L31)>0,(L6-G6)/SUM(H31:L31),""),"")', DEC2,
     'Aumento de ventas ÷ reinversión neta acumulada. Es la palanca S2C, y su ancla propia.'),
    (54, 'S2C MEDIO (ventas ÷ capital invertido)', '=IF(AND(ISNUMBER(L6),ISNUMBER(L32),N(L32)>0),L6/L32,"")', DEC2,
     'Medida distinta: es la que publica Damodaran por sector. No se compara con la palanca.'),
    (55, 'ROIC medio · 5 años',
     '=IF($C$68="Sí",IF(COUNT(H38:L38)>0,AVERAGE(H38:L38),""),IF(COUNT(H33:L33)>0,AVERAGE(H33:L33),""))', PCT,
     'Con I+D capitalizada si está activada en Palancas.'),
    (56, 'ROE medio · 5 años', '=IF(COUNT(H34:L34)>0,AVERAGE(H34:L34),"")', PCT, 'Ancla del motor C.'),
    (57, 'Años de la media del FCF base (Análisis C46)', None, '0',
     'DATO: los mismos años que usaste en C46–C50 (3 a 5). Debe ser ≤ los años con ventas.'),
    (58, 'Fugas al accionista (f, % de ventas)',
     '=IF(OR(NOT(ISNUMBER($C$70)),NOT(ISNUMBER($C$57)),$C$57<1,$C$43<$C$57,SUMPRODUCT(--($C$6:$L$14<>""),--NOT(ISNUMBER($C$6:$L$14)))>0),"",'
     'IF(SUMPRODUCT(--(COLUMN($C$6:$L$6)>12-$C$57),$C$6:$L$6)<=0,"",'
     '((SUMPRODUCT(--(COLUMN($C$6:$L$6)>12-$C$57),$C$7:$L$7,1-$C$10:$L$10)'
     '-SUMPRODUCT(--(COLUMN($C$6:$L$6)>12-$C$57),$C$12:$L$12-$C$8:$L$8+$C$14:$L$14))/$C$57-$C$70)'
     '/(SUMPRODUCT(--(COLUMN($C$6:$L$6)>12-$C$57),$C$6:$L$6)/$C$57)))', PCT,
     'Lo que separa el EBIT después de impuestos de la caja del accionista: intereses, arrendamientos y demás. '
     'El motor A la supone proporcional a las ventas; si no lo es, usa el motor B.'),
    (59, 'Patrimonio neto del último año (B0)', '=IF(ISNUMBER(L21),L21,"")', NUM, 'Base del motor C.'),
    (60, 'ROE del último año', '=IF(ISNUMBER(L34),L34,"")', PCT, 'ROE de partida del motor C.'),
    (61, 'Beneficio neto del último año', '=IF(ISNUMBER(L9),L9,"")', NUM, 'Para el PER.'),
    (62, 'EBITDA del último año', '=IF(AND(ISNUMBER(L7),ISNUMBER(L8)),L7+L8,"")', NUM, 'Para EV/EBITDA.'),
    (63, 'Coste de la deuda (intereses ÷ deuda media)',
     '=IF(AND(ISNUMBER(L15),(N(K22)+N(K23)+N(L22)+N(L23))>0),L15/((N(K22)+N(K23)+N(L22)+N(L23))/2),"")', PCT,
     'Para la r operativa del motor B.'),
    (64, 'Deuda + arrendamientos (último año)', '=IF(COUNT(L22,L23)>0,N(L22)+N(L23),"")', NUM, ''),
    (65, 'Pensiones + minoritarios (último año)', '=N(L25)+N(L26)', NUM, ''),
    (66, 'Caja (último año)', '=IF(ISNUMBER(L24),L24,"")', NUM, ''),
    (67, 'S2C marginal con I+D como inversión (informativo)',
     '=IF(AND($C$68="Sí",ISNUMBER(C53),COUNT(H37:L37)>0),(L6-G6)/(SUM(H31:L31)+SUM(H19:L19)-SUM(H37:L37)),"")',
     DEC2, 'Solo para entender la empresa.'),
    (68, '¿I+D capitalizada en las anclas?', f'={PAL}!${C_IDA}', None, 'Se elige en Palancas.'),
    (69, 'Vida útil de la I+D (años)', f'={PAL}!${C_IDV}', '0', 'Se elige en Palancas.'),
    (70, 'FCF base usado para calibrar f',
     f'=IF(NOT(ISNUMBER(Análisis!$C$52)),"",IF(AND(Análisis!$C$52<=0,OR({PAL}!${C_FCFNAT}="Transitorio",'
     f'{PAL}!${C_FCFNAT}="Extraordinario"),ISNUMBER({PAL}!${C_FCFNORM}),N({PAL}!${C_FCFNORM})>0),'
     f'{PAL}!${C_FCFNORM},Análisis!$C$52))', NUM1,
     'Es Análisis C52, salvo que el FCF base sea ≤ 0, su naturaleza sea transitoria o extraordinaria y haya un FCF '
     'normalizado > 0 en Palancas C44: entonces usa ese. Solo lo usa el motor A.'),
    (71, 'Procedencia del FCF que calibra f',
     f'=IF(NOT(ISNUMBER($C$70)),"—",IF($C$70=Análisis!$C$52,"Análisis C52 (FCF base)",'
     f'"Palancas C44 (FCF normalizado · "&{PAL}!${C_FCFNAT}&")"))', None, 'Trazabilidad del dato.'),
]
for r, nm, f_, fmt, nt in ANC:
    label(H, f'A{r}', nm)
    H.merge_cells(f'A{r}:B{r}')
    if f_ is None:
        inp(H, f'C{r}', 3 if r == 57 else None, fmt)
    else:
        out(H, f'C{r}', f_, fmt, bold=True)
    note(H, f'D{r}', nt)
    H.merge_cells(f'D{r}:M{r}')
widths(H, {'A': 42, 'B': 26, **{CL(c): 12 for c in range(3, 13)}, 'M': 30})
H.freeze_panes = 'C5'

# ================================================================== Palancas (todo lo que se rellena)
P = wb.create_sheet(PAL)
title(P, 1, '  PALANCAS · todo lo que rellena el analista', 10)
note(P, 'A2', 'Las celdas de entrada (fondo azul oscuro y texto azul claro) son las únicas que se escriben. Todo lo que se calcula está en la hoja '
               '«Diagnóstico V6». Cada palanca se juzga contra la historia de la empresa (◆) y su sector (▒).')
P.merge_cells('A2:J2')
P.row_dimensions[2].height = 28

band(P, 4, '  1 · TIPO DE EMPRESA')
TIPO = [(5, 'Etapa del ciclo de vida', 'Lista_Etapa', 'Damodaran, cap. 2: los problemas de valoración cambian con la etapa.'),
        (6, 'Caso especial', 'Lista_Caso', 'Financiera → motor C. Cíclica → media del ciclo. Intangibles → I+D.'),
        (7, 'Sector de Damodaran', 'Lista_Sectores', 'El más parecido de la hoja Sector. Da los cuartiles.'),
        (8, 'Base de partida del margen', 'Lista_Base', '«Media del ciclo» para cíclicas: parte del margen medio.'),
        (9, '¿I+D capitalizada en las anclas?', 'Lista_SiNo', 'Solo cambia las anclas (ROIC). El valor no cambia.'),
        (10, 'Vida útil de la I+D (años)', None, 'Típico: 3 software, 5 tecnología, 10 farmacia.')]
for r, nm, lst, nt in TIPO:
    label(P, f'A{r}', nm)
    inp(P, f'C{r}', None, '0' if lst is None else None)
    if lst:
        dv_list(P, f'C{r}', lst)
    P.merge_cells(f'C{r}:D{r}')
    note(P, f'E{r}', nt)
    P.merge_cells(f'E{r}:J{r}')

band(P, 12, '  2 · LAS CINCO PALANCAS POR ESCENARIO')
header(P, 13, ['Palanca', 'MALO', 'NORMAL', 'BUENO', 'Media propia', 'Sector Q1', 'Sector mediana', 'Sector Q3',
               '', 'Pista del NORMAL    ▒ sector   ◆ propia   ● NORMAL'])
LEV = [
    (R_CREC, f'=IF({DG}!${D_MOTOR}="C","Crecimiento del patrimonio · años 1–5","Crecimiento de ventas · años 1–5")',
     PCT, f'=IF({DG}!${D_MOTOR}="C","",{HI}!$C$46)', sect_of('gq1'), sect_of('gmed'), sect_of('gq3'), (-0.10, 0.30)),
    (R_MARG, f'=IF({DG}!${D_MOTOR}="C","ROE objetivo (se alcanza en el año 5)","Margen operativo objetivo (año 5)")',
     PCT, f'=IF({DG}!${D_MOTOR}="C",{HI}!$C$56,{HI}!$C$49)',
     f'IF({DG}!${D_MOTOR}="C","",{sect_of("mq1")})', f'IF({DG}!${D_MOTOR}="C",{sect_of("roe")},{sect_of("mmed")})',
     f'IF({DG}!${D_MOTOR}="C","",{sect_of("mq3")})', (-0.10, 0.50)),
    (R_S2C, f'=IF({DG}!${D_MOTOR}="C","Ventas por euro reinvertido · no se usa en el motor C",'
            '"Ventas por euro reinvertido (S2C)")',
     DEC2, f'=IF({DG}!${D_MOTOR}="C","",{HI}!$C$53)', None, None, None, (0, 5)),
    (R_G, '="g para siempre (se escribe en Análisis B68:D68)"', PCT, None, '0.01', None, '0.03', (0, 0.04)),
    (R_ROIC, f'=IF({DG}!${D_MOTOR}="C","ROE a largo plazo (tras el año 10)","ROIC a largo plazo (tras el año 10)")',
     PCT, f'=IF({DG}!${D_MOTOR}="C",{HI}!$C$56,{HI}!$C$55)', None,
     f'IF({DG}!${D_MOTOR}="C",{sect_of("roe")},{sect_of("roic")})', None, (0, 0.50)),
]


def pos(v, lo, hi, w=26):
    return f'MAX(1,MIN({w},ROUND(({v}-({lo}))/(({hi})-({lo}))*{w - 1},0)+1))'


def track(rv, q1, q3, own, lo, hi, you=None, w=26):
    base = f'REPT("─",{w})'
    s = (f'IF(AND(ISNUMBER({q1}),ISNUMBER({q3})),REPLACE({base},{pos(q1, lo, hi, w)},'
         f'{pos(q3, lo, hi, w)}-{pos(q1, lo, hi, w)}+1,REPT("▒",{pos(q3, lo, hi, w)}-{pos(q1, lo, hi, w)}+1)),{base})')
    s = f'IF(ISNUMBER({own}),REPLACE({s},{pos(own, lo, hi, w)},1,"◆"),{s})'
    s = f'IF(ISNUMBER({rv}),REPLACE({s},{pos(rv, lo, hi, w)},1,"●"),{s})'
    if you:
        s = (f'IF(AND(ISNUMBER({you}),ISNUMBER({rv}),ABS({you}-{rv})>0.0000001),'
             f'REPLACE({s},{pos(you, lo, hi, w)},1,"▲"),{s})')
    return f'=IFERROR({s},REPT("─",{w}))'


for r, nm, fmt, own, q1, med, q3, (lo, hi) in LEV:
    out(P, f'A{r}', nm, bold=True)
    for col in 'BCD':
        if r == R_G:
            out(P, f'{col}{r}', f'=IF(ISNUMBER(Análisis!{col}68),Análisis!{col}68,"")', fmt)
        else:
            inp(P, f'{col}{r}', None, fmt)
    for colL, v in zip('FGHI', (own, q1, med, q3)):
        if v is None:
            continue
        val = v if str(v).startswith('=') else ('=' + str(v))
        out(P, f'{colL}{r}', val, fmt)
    note(P, f'F{r}' if own is None else f'Z{r}', None)
    c = out(P, f'J{r}', track(f'C{r}', f'G{r}', f'I{r}', f'F{r}', lo, hi))
    c.font = Font(name='Consolas', size=11)
    c.alignment = Alignment(vertical='center')
note(P, 'G16', 'el sector mide el S2C medio → fila 19')
P.merge_cells('G16:I16')
LEVNOTE = {R_CREC: 'En los años 6–10 baja en línea recta hasta el g para siempre.',
           R_MARG: 'Parte del margen de partida y llega a este en el año 5.',
           R_S2C: 'Cada euro de ventas nuevas exige 1 ÷ S2C de inversión.',
           R_G: 'Del 1 al 3 %. Nunca ≥ la tasa de descuento del motor.',
           R_ROIC: 'Si es igual a la tasa de descuento, crecer ya no crea valor.'}
label(P, 'A19', 'Tu S2C MEDIO (ventas ÷ capital), solo para comparar con el sector', size=10)
P.merge_cells('A19:D19')
out(P, 'F19', f'={HI}!$C$54', DEC2)
for colL, k in zip('GHI', ('sq1', 'smed', 'sq3')):
    out(P, f'{colL}19', '=' + sect_of(k), DEC2)
note(P, 'J19', 'Medida distinta de la palanca: media, no marginal.')

band(P, 21, '  3 · OPCIONES DEL ESCENARIO')
OPC = [(22, 'Probabilidad de quiebra en 10 años (vacío = 0)', PCT,
        'Guía por rating (Damodaran): BBB ≈ 1,6 % a 5 años; BB ≈ 6,5 %; B ≈ 16,9 %.'),
       (23, 'Lo que recuperaría el accionista si quiebra (mm)', NUM, 'Casi siempre 0.'),
       (24, 'Tamaño del mercado en el año 10 (mm, opcional)', NUM, 'Para calcular la cuota implícita.')]
for r, nm, fmt, nt in OPC:
    label(P, f'A{r}', nm)
    inp(P, f'C{r}', None, fmt)
    P.merge_cells(f'C{r}:D{r}')
    note(P, f'E{r}', nt)
    P.merge_cells(f'E{r}:J{r}')

band(P, 26, '  4 · DÓNDE VENDE (riesgo país)')
header(P, 27, ['País o región', '% de las ventas', 'Prima país', 'Contribución a la r mínima'])
for i in range(6):
    r = PAIS0 + i
    inp(P, f'A{r}')
    inp(P, f'B{r}', None, PCT)
    out(P, f'C{r}', f'=IF(A{r}="","",IFERROR(INDEX({RP}!$D$6:$D${RP_LAST},MATCH(A{r},{RP}!$A$6:$A${RP_LAST},0)),""))', PCT2)
    out(P, f'D{r}', f'=IF(AND(ISNUMBER(B{r}),ISNUMBER(C{r})),B{r}*C{r},"")', PCT2)
dv_list(P, f'A{PAIS0}:A{PAIS0 + 5}', 'Lista_Paises')
PTOT = PAIS0 + 6
label(P, f'A{PTOT}', 'Total', bold=True)
out(P, f'B{PTOT}', f'=SUM(B{PAIS0}:B{PAIS0 + 5})', PCT, bold=True)
out(P, f'D{PTOT}', f'=SUM(D{PAIS0}:D{PAIS0 + 5})', PCT2, bold=True)
out(P, f'E{PTOT}', f'=IF(N(B{PTOT})=0,"—",IF(ABS(B{PTOT}-1)>0.02,"⚠ REVISAR · los % no suman 100 %","✓ PASA"))')
verdict_cf(P, f'E{PTOT}')

band(P, 36, '  5 · PREDICCIONES (medibles, salidas del escenario NORMAL)')
header(P, 37, ['Predicción (qué, métrica y umbral)', 'Fecha de comprobación', 'Probabilidad', 'Resultado'])
for i in range(3):
    r = PRED0 + i
    inp(P, f'A{r}')
    inp(P, f'B{r}', None, 'dd/mm/yyyy')
    inp(P, f'C{r}', None, '0%')
    inp(P, f'D{r}')
note(P, 'E38', 'Ejemplo: «Ventas FY2026 ≥ 17.000 mm» · 31/03/2027 · 70 %.')
P.merge_cells('E38:J38')
band(P, 42, '  6 · AJUSTES Y METADATOS (solo cuando hagan falta)')
META = [
    (C_FCFNAT, 'Naturaleza del FCF base ≤ 0 (solo motor A)', 'Lista_FCFNat', None,
     'Solo si Análisis C52 ≤ 0. Transitorio o extraordinario permiten calibrar con el FCF normalizado de abajo; '
     'estructural deja el motor A sin aplicar. Nunca descarta la empresa.'),
    (C_FCFNORM, 'FCF base normalizado (mm)', None, NUM1,
     'Numérico y > 0. Se usa solo con naturaleza transitoria o extraordinaria.'),
    (C_FPRECIO, 'Fecha del precio', None, 'dd/mm/yyyy', 'Fecha de la cotización de Análisis C37.'),
    (C_FACC, 'Fecha de las acciones diluidas', None, 'dd/mm/yyyy',
     'Fecha del dato de Análisis C55. Si difiere más de 90 días de la del precio, avisa.'),
    (C_CAUSA, 'Causa declarada de la diferencia de capitalización', 'Lista_CausaCap', None,
     'Vacío y «Ninguna» = causa no declarada. Declararla explica la diferencia y quita el bloqueo, pero no demuestra '
     'que esté corregida: queda una nota visible.'),
    (C_MONEDA, 'Moneda de cotización (EUR, USD, CHF…)', None, None,
     'Metadato obligatorio para leer el precio. Vacía: no se compara precio con valor hasta declararla. Si difiere de la del modelo (Control maestro H4), no hay '
     'conversión: se conserva el valor y queda sin calcular el margen de seguridad.'),
]
for ref, nm, lst, fmt, nt in META:
    r = int(ref[1:])
    label(P, f'A{r}', nm)
    inp(P, ref, None, fmt)
    if lst:
        dv_list(P, ref, lst)
    P.merge_cells(f'C{r}:D{r}')
    note(P, f'E{r}', nt)
    P.merge_cells(f'E{r}:J{r}')
    P.row_dimensions[r].height = 28
widths(P, {'A': 50, 'B': 13, 'C': 13, 'D': 13, 'E': 14, 'F': 13, 'G': 13, 'H': 13, 'I': 13, 'J': 42})
P.freeze_panes = 'B4'
P.sheet_view.showGridLines = False

# ================================================================== Diagnóstico V6 (todo lo que se calcula)
D = wb.create_sheet('Diagnóstico V6')
title(D, 1, '  DIAGNÓSTICO V6 · todo lo que calcula la hoja', 10)

band(D, 3, '  1 · MOTOR Y BASE DEL CÁLCULO')
label(D, 'A5', 'Motor de valoración (sale de Análisis C62)', bold=True)
out(D, f'{D_MOTOR}', '=IF(Análisis!$C$62="Sí","A",IF(Análisis!$C$62="No · financiación cambia mucho","B",'
                     'IF(OR(Análisis!$C$62="No · banco o aseguradora",Análisis!$C$62="No · banco, aseguradora o regulada"),"C",IF(Análisis!$C$62="","","—"))))', bold=True)
out(D, 'D5', f'=IF({D_MOTOR}="A","Accionista",IF({D_MOTOR}="B","Operativo con deuda",'
             f'IF({D_MOTOR}="C","ROE (patrimonio)",IF({D_MOTOR}="—","Sin motor",""))))', bold=True)
note(D, 'E5', 'A: flujo del accionista a tu r. B: flujo operativo a una r mezclada, menos la deuda. C: patrimonio y ROE.')
D.merge_cells('E5:J5')
label(D, 'A6', 'Coherencia entre tipo de empresa y motor')
out(D, f'{D_COHER}', f'=IF(OR({PAL}!${C_ETAPA}="",{PAL}!${C_CASO}=""),"—",'
                     f'IF(AND({PAL}!${C_CASO}="Financiera (banco o aseguradora)",{D_MOTOR}<>"C"),'
                     '"⚠ REVISAR · financiera: usa el motor C en Análisis C62",'
                     f'IF(AND({PAL}!${C_CASO}="Cíclica o materias primas",{PAL}!${C_BASE}<>"Media del ciclo"),'
                     '"⚠ REVISAR · cíclica: usa la media del ciclo como base",'
                     f'IF(AND({PAL}!${C_CASO}="Intangibles (I+D, marca)",{PAL}!${C_IDA}<>"Sí"),'
                     '"⚠ REVISAR · intangibles: activa la I+D en las anclas",'
                     f'IF({PAL}!${C_CASO}="Multinegocio o conglomerado",'
                     '"⚠ REVISAR · conglomerado: un solo juego de palancas mezcla negocios distintos; considera valorar por partes",'
                     f'IF(AND({PAL}!${C_CASO}="Emergente (riesgo país)",N({PAL}!$B${PTOT})=0),'
                     '"⚠ REVISAR · emergente: rellena dónde vende (Palancas, bloque 4)",'
                     f'IF(AND({PAL}!${C_ETAPA}="En declive",N(Análisis!$C$68)>0.01),'
                     '"⚠ REVISAR · en declive: g para siempre ≤ 1 %",'
                     f'IF(AND({PAL}!${C_ETAPA}="Joven (sin beneficios estables)",N({PAL}!${C_PQ})=0),'
                     '"⚠ REVISAR · joven: ¿probabilidad de quiebra?","✓ PASA · tipo y motor coherentes"))))))))', wrap=True)
D.merge_cells(f'{D_COHER}:D6')
subband(D, 8, 'Base del motor (automática)')
BASE = [
    (D_V0, 'Ventas de partida (V0)', f'={HI}!$C$44', NUM, 'Último año de Historia.'),
    (D_M0, 'Margen EBIT de partida (m0)', f'=IF({PAL}!${C_BASE}="Media del ciclo",{HI}!$C$49,{HI}!$C$48)', PCT, ''),
    (D_TAU, 'Tipo impositivo (t)', f'={HI}!$C$52', PCT, 'Media de 5 años.'),
    (D_F, 'Fugas al accionista (f, % de ventas)', f'={HI}!$C$58', PCT,
     'Calibra el motor A con tu FCF base (Análisis C52). Supuesto: proporcional a las ventas.'),
    (D_B0, 'Patrimonio de partida (B0) · motor C', f'={HI}!$C$59', NUM, ''),
    (D_ROE0, 'ROE de partida · motor C', f'={HI}!$C$60', PCT, ''),
    (D_ROP, 'r operativa · motor B', f'=IF(AND(ISNUMBER(Análisis!$C$56),N({HI}!$C$64)=0),Análisis!$C$56,'
     f'IF(AND(ISNUMBER(Análisis!$C$56),ISNUMBER(Análisis!$C$41),N(Análisis!$C$41)>0,ISNUMBER({HI}!$C$63),'
     f'ISNUMBER({HI}!$C$64)),(Análisis!$C$56*Análisis!$C$41+{HI}!$C$63*(1-N(${D_TAU}))*{HI}!$C$64)'
     f'/(Análisis!$C$41+{HI}!$C$64),""))', PCT,
     'Tu r y el coste real de su deuda, con pesos de mercado. Sin deuda, es tu r.'),
    (D_PAS, 'Pasivos netos que se restan · motor B', f'=IF(ISNUMBER({HI}!$C$64),{HI}!$C$64+{HI}!$C$65-N({HI}!$C$66),"")',
     NUM, 'Deuda + arrendamientos + pensiones + minoritarios − caja.'),
    (D_RMIN, 'r mínima por moneda y país',
     f'=IF(ISNUMBER(Análisis!$C$57),Análisis!$C$57+{RP}!$C$3+N({PAL}!$D${PTOT}),"")', PCT,
     'Tasa sin riesgo de la moneda + prima madura + prima de los países donde vende.'),
]
for i, (ref, nm, f_, fmt, nt) in enumerate(BASE):
    r = int(ref[1:])
    label(D, f'A{r}', nm)
    out(D, ref, f_, fmt, bold=True)
    note(D, f'E{r}', nt)
    D.merge_cells(f'E{r}:J{r}')
label(D, f'A{D_RVS[1:]}', 'Tu r frente a la r mínima')
out(D, D_RVS, f'=IF(OR(${D_RMIN}="",NOT(ISNUMBER(Análisis!$C$56))),"—",IF(Análisis!$C$56>=${D_RMIN},'
              f'"✓ PASA · r ≥ r mínima","⚠ REVISAR · tu r ("&FIXED(100*Análisis!$C$56,1)&" %) < r mínima ("'
              f'&FIXED(100*${D_RMIN},1)&" %)"))', wrap=True)
D.merge_cells(f'{D_RVS}:D{D_RVS[1:]}')
note(D, 'E18', 'Tu r la eliges tú (decisión D2): esto es solo un aviso.')
D.merge_cells('E18:J18')

band(D, 20, '  2 · RESULTADOS POR ESCENARIO')
header(D, 21, ['Resultado', 'MALO', 'NORMAL', 'BUENO', 'Cómo leerlo'])
D.merge_cells('E21:J21')
mrow = {'B': 6, 'C': 7, 'D': 8}
RES = [
    ('BR', NUM, 'Ventas en el año 10 (motor C: patrimonio)', ''),
    ('AU', NUM, 'FCF del año 1 (mm)', 'Crecer más baja el FCF de hoy: hay que reinvertir.'),
    ('BD', NUM, 'FCF del año 10 (mm)', ''),
    ('BM', PCT, 'Crecimiento anual del FCF implícito (años 1→10)', 'Es lo que recibe Análisis B67:D67.'),
    ('BE', NUM, 'Valor hoy de los años 1–10 (mm)', ''),
    ('BH', NUM, 'Valor hoy del «para siempre» (mm)', ''),
    ('BN', PCT, '% del valor en el «para siempre»', ''),
    ('M', NUM, 'Ajuste: exceso de caja (A) o − pasivos netos (B)', ''),
    ('BI', NUM, 'Valor total antes de quiebra (mm)', ''),
    ('BJ', NUM, 'Valor final para el accionista (mm)', 'Con la probabilidad de quiebra.'),
    ('BK', NUM2, 'VALOR POR ACCIÓN', 'Es lo que recibe Análisis B78:D78.'),
    ('BO', NUM2, 'Valor sin crecimiento (por acción)', 'Lo que vale si deja de crecer y no reinvierte.'),
    (None, NUM2, 'Valor del crecimiento y de la mejora de margen', 'Valor total − valor sin crecimiento.'),
    ('BQ', PCT, 'ROIC marginal implícito (lo nuevo)', 'Margen × (1 − t) × S2C.'),
    (None, PCT, 'Cuota de mercado implícita en el año 10', 'Solo si rellenas el tamaño del mercado.'),
]
for i, (mc, fmt, nm, nt) in enumerate(RES):
    r = RES0 + i
    label(D, f'A{r}', nm, bold=(fmt == NUM2 and mc == 'BK'))
    for col in 'BCD':
        n_ = mrow[col]
        if mc:
            f_ = f'=IF(OR({MO}!$B${AGG0_PLACEHOLDER},{MO}!{mc}{n_}=""),"",{MO}!{mc}{n_})'
        elif nm.startswith('Valor del crecimiento'):
            f_ = (f'=IF(AND(NOT({MO}!$B${AGG0_PLACEHOLDER}),ISNUMBER({MO}!BI{n_}),ISNUMBER({MO}!BO{n_}),N(Análisis!$C$55)>0),'
                  f'{MO}!BI{n_}/Análisis!$C$55-{MO}!BO{n_},"")')
        else:
            f_ = (f'=IF(AND(ISNUMBER({col}{RES0}),ISNUMBER({PAL}!${C_MKT}),N({PAL}!${C_MKT})>0,${D_MOTOR}<>"C"),'
                  f'{col}{RES0}/{PAL}!${C_MKT},"")')
        out(D, f'{col}{r}', f_, fmt, bold=(mc == 'BK'))
    note(D, f'E{r}', nt)
    D.merge_cells(f'E{r}:J{r}')
R_VSG, R_VGR = RES0 + 11, RES0 + 12

band(D, 38, '  3 · DIAGNÓSTICOS (cada uno defiende un principio)')
header(D, 39, ['Comprobación', 'MALO', 'NORMAL', 'BUENO', 'Principio que defiende'])
D.merge_cells('E39:J39')
DIAGS = [
    ('Crecimiento frente al sector y a su historia',
     lambda c: f'=IF(NOT(ISNUMBER({PAL}!{c}{R_CREC})),"—",IF(OR(AND(ISNUMBER({PAL}!$I${R_CREC}),'
               f'{PAL}!{c}{R_CREC}>N({PAL}!$I${R_CREC})),AND(ISNUMBER({PAL}!$F${R_CREC}),N({PAL}!$F${R_CREC})>0,'
               f'{PAL}!{c}{R_CREC}>1.5*N({PAL}!$F${R_CREC}))),"⚠ REVISAR · por encima del Q3 del sector o de 1,5× su '
               'historia"&IF(Análisis!$C$18="Sí"," (hay moat: justifícalo)"," · y sin moat"),"✓ PASA"))',
     '«El crecimiento tiene que ganarse» (Damodaran, principio 4).'),
    ('Margen frente a su máximo y al sector',
     lambda c: f'=IF(NOT(ISNUMBER({PAL}!{c}{R_MARG})),"—",IF(${D_MOTOR}="C",IF(AND(ISNUMBER({PAL}!$H${R_MARG}),'
               f'{PAL}!{c}{R_MARG}>1.5*N({PAL}!$H${R_MARG})),"⚠ REVISAR · ROE muy por encima del sector","✓ PASA"),'
               f'IF(OR(AND(ISNUMBER({PAL}!$I${R_MARG}),{PAL}!{c}{R_MARG}>N({PAL}!$I${R_MARG})),'
               f'AND(ISNUMBER({HI}!$C$51),{PAL}!{c}{R_MARG}>N({HI}!$C$51))),'
               '"⚠ REVISAR · margen por encima de su máximo o del Q3 del sector","✓ PASA")))',
     '«Todo lo bueno se acaba»: la competencia muerde los márgenes (principio 5).'),
    ('ROIC marginal frente a su historia',
     lambda c: f'=IF(NOT(ISNUMBER({c}{RES0 + 13})),"—",IF(AND(ISNUMBER({PAL}!$F${R_ROIC}),N({PAL}!$F${R_ROIC})>0,'
               f'{c}{RES0 + 13}>2*N({PAL}!$F${R_ROIC})),"⚠ REVISAR · cada euro nuevo rendiría "'
               f'&FIXED(100*{c}{RES0 + 13},0)&" %, más del doble de su historia","✓ PASA"))',
     '«El crecimiento no es gratis y no siempre crea valor».'),
    ('ROIC (o ROE) a largo plazo',
     lambda c: f'=IF(NOT(ISNUMBER({PAL}!{c}{R_ROIC})),"—",IF(AND(ISNUMBER({PAL}!{c}{R_G}),'
               f'{PAL}!{c}{R_ROIC}<={PAL}!{c}{R_G}),"✗ BANDERA · ROIC ≤ g: crecer para siempre no se paga",'
               f'IF(AND(ISNUMBER(Análisis!$C$56),{PAL}!{c}{R_ROIC}>Análisis!$C$56+0.1),'
               '"⚠ REVISAR · muy por encima de r para siempre: exige moat duradero","✓ PASA")))',
     'Sin un moat duradero, nadie gana más que su coste para siempre.'),
    ('Peso del «para siempre»',
     lambda c: f'=IF(NOT(ISNUMBER({c}{RES0 + 6})),"—",IF({c}{RES0 + 6}>0.75,"⚠ REVISAR · "'
               f'&FIXED(100*{c}{RES0 + 6},0)&" % del valor está después del año 10","✓ PASA"))',
     '«Acepta la incertidumbre»: no la escondas en el valor final (principio 9).'),
    ('Cuota de mercado implícita',
     lambda c: f'=IF(NOT(ISNUMBER({c}{RES0 + 14})),"—",IF({c}{RES0 + 14}>0.3,"⚠ REVISAR · cuota implícita "'
               f'&FIXED(100*{c}{RES0 + 14},0)&" %","✓ PASA"))',
     '«Las leyes de la oferta y la demanda no se derogan» (principio 1).'),
]
for i, (nm, fn, pr) in enumerate(DIAGS):
    r = DIAG0 + i
    label(D, f'A{r}', nm)
    for col in 'BCD':
        out(D, f'{col}{r}', fn(col), size=9, wrap=True)
    note(D, f'E{r}', pr)
    D.merge_cells(f'E{r}:J{r}')
    D.row_dimensions[r].height = 30
SOLO = [
    (DIAG0 + 6, 'S2C medio frente al sector',
     f'=IF(OR(${D_MOTOR}="C",NOT(ISNUMBER({PAL}!$F$19)),NOT(ISNUMBER({PAL}!$G$19)),NOT(ISNUMBER({PAL}!$I$19))),"—",'
     f'IF(OR({PAL}!$F$19<N({PAL}!$G$19),{PAL}!$F$19>N({PAL}!$I$19)),'
     '"⚠ REVISAR · su capital por euro de ventas está fuera del rango del sector","✓ PASA"))',
     'Comparación media con media: la palanca S2C es marginal y no se compara aquí.'),
    (DIAG0 + 7, 'Orden de los escenarios (MALO ≤ NORMAL ≤ BUENO)',
     f'=IF(COUNT({PAL}!B{R_CREC}:D{R_MARG})<6,"—",IF(OR({PAL}!B{R_CREC}>{PAL}!C{R_CREC},'
     f'{PAL}!C{R_CREC}>{PAL}!D{R_CREC},{PAL}!B{R_MARG}>{PAL}!C{R_MARG},{PAL}!C{R_MARG}>{PAL}!D{R_MARG}),'
     '"✗ BANDERA · crecimiento o margen desordenados entre escenarios",'
     f'IF(OR(AND(${D_MOTOR}<>"C",COUNT({PAL}!B{R_S2C}:D{R_S2C})=3,OR({PAL}!B{R_S2C}>{PAL}!C{R_S2C},'
     f'{PAL}!C{R_S2C}>{PAL}!D{R_S2C})),AND(COUNT({PAL}!B{R_ROIC}:D{R_ROIC})=3,OR({PAL}!B{R_ROIC}>{PAL}!C{R_ROIC},'
     f'{PAL}!C{R_ROIC}>{PAL}!D{R_ROIC})),AND(COUNT({PAL}!B{R_G}:D{R_G})=3,OR({PAL}!B{R_G}>{PAL}!C{R_G},'
     f'{PAL}!C{R_G}>{PAL}!D{R_G}))),"⚠ REVISAR · S2C, g o ROIC desordenados: explícalo","✓ PASA")))',
     '«Convierte historias en números» (principio 10).'),
    (DIAG0 + 8, 'Tu r frente a la r mínima', f'=${D_RVS}', '«El riesgo importa» (principio 3).'),
    (DIAG0 + 9, 'Tipo de empresa frente a motor', f'=${D_COHER}', 'Elige el modelo según la empresa (cap. 8).'),
    (DIAG0 + 10, 'Fugas al accionista (f) en un rango razonable',
     f'=IF(NOT(ISNUMBER(${D_F})),"—",IF(OR(${D_F}<-0.02,${D_F}>0.05),"⚠ REVISAR · f = "&FIXED(100*${D_F},1)'
     '&" % de las ventas: revisa Análisis C52 y el EBIT de Historia","✓ PASA"))',
     'Un f raro casi siempre es un dato mal puesto.'),
]
for r, nm, f_, pr in SOLO:
    label(D, f'A{r}', nm)
    out(D, f'C{r}', f_, size=9, wrap=True)
    D.merge_cells(f'C{r}:D{r}')
    note(D, f'E{r}', pr)
    D.merge_cells(f'E{r}:J{r}')
verdict_cf(D, f'B{DIAG0}:D{DIAG0 + DIAGN - 1}')
verdict_cf(D, f'{D_COHER}:D6')
verdict_cf(D, f'{D_RVS}:D18')

band(D, 52, '  4 · ¿CUÁNTO PAGAS POR CRECER? (escenario NORMAL)')
PG = [('Valor sin crecimiento (por acción)', f'=C{R_VSG}', NUM2),
      ('Precio actual', f'=IF(OR({GATEP_PLACEHOLDER},NOT(ISNUMBER(Análisis!$C$37))),"",Análisis!$C$37)', NUM2),
      ('Lo que pagas por crecimiento = precio − valor sin crecimiento',
       f'=IF(AND(ISNUMBER(C{PG0 + 1}),ISNUMBER(C{PG0})),C{PG0 + 1}-C{PG0},"")', NUM2),
      ('Lo que vale el crecimiento (y la mejora de margen) en tu NORMAL', f'=C{R_VGR}', NUM2),
      ('Pagas ÷ vale', f'=IF(AND(ISNUMBER(C{PG0 + 2}),ISNUMBER(C{PG0 + 3}),N(C{PG0 + 3})>0),C{PG0 + 2}/C{PG0 + 3},"")',
       '0.0"x"')]
for i, (nm, f_, fmt) in enumerate(PG):
    r = PG0 + i
    label(D, f'A{r}', nm)
    out(D, f'C{r}', f_, fmt, bold=True)
out(D, f'D{PG0 + 4}', f'=IF(OR(NOT(ISNUMBER(C{PG0 + 2})),NOT(ISNUMBER(C{PG0 + 3}))),"—",'
                      f'IF(C{PG0 + 2}<=0,"✓ PASA · el precio no paga nada por crecimiento",'
                      f'IF(C{PG0 + 3}<=0,"⚠ REVISAR · pagas por un crecimiento que, con tus palancas, no añade valor",'
                      f'IF(C{PG0 + 4}>1.5,"⚠ REVISAR · pagas "&FIXED(C{PG0 + 4},1)&" veces lo que vale","✓ PASA"))))',
    size=9, wrap=True)
D.merge_cells(f'D{PG0 + 4}:F{PG0 + 4}')
verdict_cf(D, f'D{PG0 + 4}:F{PG0 + 4}')
note(D, f'G{PG0}', 'Damodaran, growthbreakdown: separa los activos que ya tiene del crecimiento futuro.')
D.merge_cells(f'G{PG0}:J{PG0}')

band(D, 59, '  5 · MÚLTIPLOS CON SU VARIABLE COMPAÑERA')
header(D, 60, ['Múltiplo', 'Hoy', 'Sector (media)', 'Justificado por tu NORMAL', 'Variable compañera (lo que lo explica)'])
D.merge_cells('E60:J60')
EVNOW = f'(Análisis!$C$41+N({HI}!$C$64)+N({HI}!$C$65)-N({HI}!$C$66))'
EVJ = f'({MO}!$BJ$7+N({HI}!$C$64)+N({HI}!$C$65)-N({HI}!$C$66))'
MULTS = [
    ('PER (precio ÷ beneficio)', f'=IFERROR(IF(N({HI}!$C$61)>0,Análisis!$C$41/{HI}!$C$61,""),"")', None,
     f'=IFERROR(IF(N({HI}!$C$61)>0,{MO}!$BJ$7/{HI}!$C$61,""),"")',
     f'=IF(ISNUMBER({PAL}!$C${R_CREC}),"Crecimiento NORMAL: "&FIXED(100*{PAL}!$C${R_CREC},1)&" %","Crecimiento")'),
    ('Precio ÷ valor contable', f'=IFERROR(IF(N({HI}!$C$59)>0,Análisis!$C$41/{HI}!$C$59,""),"")', 'pb',
     f'=IFERROR(IF(N({HI}!$C$59)>0,{MO}!$BJ$7/{HI}!$C$59,""),"")',
     f'=IF(ISNUMBER({HI}!$C$60),"ROE último: "&FIXED(100*{HI}!$C$60,1)&" %","ROE")'),
    ('EV ÷ ventas', f'=IFERROR(IF(N({HI}!$C$44)>0,{EVNOW}/{HI}!$C$44,""),"")', 'evs',
     f'=IFERROR(IF(N({HI}!$C$44)>0,{EVJ}/{HI}!$C$44,""),"")',
     f'=IF(${D_MOTOR}="C","— motor C: usa precio ÷ valor contable",IF(AND(ISNUMBER({PAL}!$C${R_MARG}),'
     f'ISNUMBER(${D_TAU})),"Margen NORMAL tras impuestos: "&FIXED(100*{PAL}!$C${R_MARG}*(1-${D_TAU}),1)&" %",'
     '"Margen tras impuestos"))'),
    ('EV ÷ EBITDA', f'=IFERROR(IF(N({HI}!$C$62)>0,{EVNOW}/{HI}!$C$62,""),"")', 'eve',
     f'=IFERROR(IF(N({HI}!$C$62)>0,{EVJ}/{HI}!$C$62,""),"")',
     f'=IF(${D_MOTOR}="C","— motor C: usa precio ÷ valor contable",IF(AND(NOT({MO}!$B${AGG0_PLACEHOLDER}),ISNUMBER({MO}!$BP$7)),'
     f'"Tasa de reinversión año 1: "&FIXED(100*{MO}!$BP$7,0)&" %","Tasa de reinversión"))'),
    ('Precio ÷ FCF base', '=IFERROR(IF(N(Análisis!$C$52)>0,Análisis!$C$41/Análisis!$C$52,""),"")', None,
     f'=IFERROR(IF(N(Análisis!$C$52)>0,{MO}!$BJ$7/Análisis!$C$52,""),"")',
     '=IF(AND(ISNUMBER(Análisis!$C$52),N(Análisis!$C$41)>0),"Rentabilidad FCF hoy: "'
     '&FIXED(100*Análisis!$C$52/Análisis!$C$41,1)&" %","Rentabilidad FCF")'),
]
for i, (nm, now, sk, just, comp) in enumerate(MULTS):
    r = MU0 + i
    label(D, f'A{r}', nm)
    out(D, f'B{r}', (f'=IF({GATEP_PLACEHOLDER},"",' + now[1:] + ')') if isinstance(now, str) and now.startswith('=') else now, MULT)
    out(D, f'C{r}', ('=' + sect_of(sk)) if sk else None, MULT)
    out(D, f'D{r}', f'=IF({MO}!$B${AGG0_PLACEHOLDER},"",{just[1:]})', MULT, bold=True)
    out(D, f'E{r}', comp)
    D.merge_cells(f'E{r}:J{r}')
note(D, f'A{MU0 + 5}', 'Un múltiplo solo dice algo al lado de la variable que lo explica (Damodaran, cap. 6). El PER '
                        'medio de un sector puede salir inflado por empresas con poco beneficio: úsalo con cuidado.')
D.merge_cells(f'A{MU0 + 5}:J{MU0 + 5}')

band(D, 67, '  6 · AUTOCOMPROBACIONES DEL LIBRO')
header(D, 68, ['Comprobación', 'Resultado', '', '', 'Por qué importa'])
D.merge_cells('B68:D68')
D.merge_cells('E68:J68')
CHK = [
    ('Historia: al menos 5 años con ventas',
     f'=IF(N({HI}!$C$43)=0,"—",IF({HI}!$C$43>=5,"✓ PASA · "&{HI}!$C$43&" años","⚠ REVISAR · solo "&{HI}!$C$43&" años"))',
     'Sin historia no hay anclas con las que comparar.'),
    ('Historia: el año más reciente está en la columna L',
     f'=IF(COUNT({HI}!$C$6:$L$6)=0,"—",IF(ISNUMBER({HI}!$L$6),"✓ PASA","✗ BANDERA · la columna L está vacía"))',
     'Todas las anclas leen el último año en la columna L.'),
    ('Los años de la media del FCF caben en la historia',
     f'=IF(OR(N({HI}!$C$57)=0,N({HI}!$C$43)=0),"—",IF({HI}!$C$57<={HI}!$C$43,"✓ PASA",'
     '"✗ BANDERA · Historia C57 pide más años de los que hay"))',
     'Si no, las fugas f se calculan sobre años que no existen.'),
    ('Las probabilidades suman 100 %',
     '=IF(COUNT(Análisis!$B$69:$D$69)<3,"—",IF(ABS(SUM(Análisis!$B$69:$D$69)-1)<0.001,"✓ PASA",'
     '"✗ BANDERA · suman "&FIXED(100*SUM(Análisis!$B$69:$D$69),0)&" %"))',
     'Sin esto no hay valor ponderado ni lectura del precio.'),
    ('g para siempre < tasa de descuento en los tres escenarios',
     f'=IF(COUNT({MO}!$H$6:$H$8,{MO}!$J$6:$J$8)<6,"—",IF(AND({MO}!$J$6>{MO}!$H$6,{MO}!$J$7>{MO}!$H$7,'
     f'{MO}!$J$8>{MO}!$H$8),"✓ PASA","✗ BANDERA · algún g ≥ la tasa del motor"))',
     'Con g ≥ r el valor terminal no existe.'),
    ('S2C > 0 en los tres escenarios (motores A y B)',
     f'=IF(${D_MOTOR}="C","No aplica (motor C)",IF(COUNT({PAL}!$B${R_S2C}:$D${R_S2C})<3,"⚠ REVISAR · falta algún S2C",'
     f'IF(MIN({PAL}!$B${R_S2C}:$D${R_S2C})>0,"✓ PASA","✗ BANDERA · hay un S2C ≤ 0")))',
     'Sin S2C no se puede calcular la reinversión.'),
    ('ROIC a largo plazo > g en los tres escenarios',
     f'=IF(COUNT({PAL}!$B${R_ROIC}:$D${R_ROIC},{PAL}!$B${R_G}:$D${R_G})<6,"—",'
     f'IF(AND({PAL}!$B${R_ROIC}>{PAL}!$B${R_G},{PAL}!$C${R_ROIC}>{PAL}!$C${R_G},{PAL}!$D${R_ROIC}>{PAL}!$D${R_G}),'
     '"✓ PASA","✗ BANDERA · algún ROIC ≤ g"))',
     'Con ROIC ≤ g la reinversión terminal se come todo el flujo.'),
    ('Los países suman 100 % (si has rellenado alguno)',
     f'=IF(N({PAL}!$B${PTOT})=0,"No aplica",IF(ABS({PAL}!$B${PTOT}-1)<0.02,"✓ PASA",'
     f'"⚠ REVISAR · suman "&FIXED(100*{PAL}!$B${PTOT},0)&" %"))',
     'Si no suman 100 %, la r mínima sale baja.'),
    ('La SBC se resta del FCF base (Análisis C51)',
     '=IF(Análisis!$C$51="","—",IF(EXACT(Análisis!$C$51,"Sí"),"✓ PASA",IF(EXACT(Análisis!$C$51,"No"),"⚠ REVISAR · el procedimiento dice restarla siempre","⛔ TÉCNICO · solo Sí o No (exacto)")))',
     'Sin restarla, el valor por acción ignora la dilución.'),
    ('El exceso de caja no supera la caja del balance',
     '=IF(OR(N(Análisis!$C$76)=0,NOT(ISNUMBER(Análisis!$C$53))),"No aplica",'
     'IF(Análisis!$C$76<=Análisis!$C$53,"✓ PASA","⚠ REVISAR · el exceso de caja (C76) supera la caja del balance (C53)"))',
     'No puedes sumar más caja de la que hay.'),
    ('El DCF inverso es utilizable',
     f'=IF({MO}!$B${AGG0_PLACEHOLDER},"⛔ TÉCNICO · valor bloqueado",IF({MO}!$B$193="","—",{MO}!$B$193))', 'Con reinversión, más crecimiento no siempre significa más valor.'),
    ('Modo estudio apagado y ajustes a cero',
     f'=IF(AND({PA}!$F$6<>"ON",COUNTIF({PA}!$E$20:$E$25,20)=6),"✓ PASA",'
     f'IF({PA}!$F$6="ON","⚠ REVISAR · el Modo estudio está encendido (no afecta a Munger)",'
     '"⚠ REVISAR · hay deslizadores movidos"))',
     'Un libro se entrega con el Panel en su sitio.'),
    ('Las tres predicciones están escritas',
     f'=IF(COUNTA({PAL}!$A${PRED0}:$A${PRED0 + 2})=3,"✓ PASA","⚠ REVISAR · faltan "'
     f'&(3-COUNTA({PAL}!$A${PRED0}:$A${PRED0 + 2}))&" predicciones")',
     'Sin predicciones no se puede saber si el método acierta.'),
    ('Tipo de empresa y caso especial elegidos',
     f'=IF(COUNTA({PAL}!${C_ETAPA}:${C_CASO})=2,"✓ PASA","⚠ REVISAR · falta la etapa o el caso especial")',
     'Determinan qué comprobaciones aplican.'),
    ('El motor calcula un valor en los tres escenarios',
     f'=IF(Análisis!$C$62="","—",IF({MO}!$B${AGG0_PLACEHOLDER},"⛔ TÉCNICO · valor bloqueado: "&{MO}!$B${AGG0_PLACEHOLDER + 4},IF(COUNT({MO}!$BK$6:$BK$8)=3,"✓ PASA",'
     f'IF({MO}!$BT$7<>"","⛔ TÉCNICO · "&{MO}!$BT$7,"⚠ REVISAR · falta algún escenario"))))',
     'Si no, no hay lectura del precio.'),
]
for i, (nm, f_, why) in enumerate(CHK):
    r = AC0 + i
    label(D, f'A{r}', nm)
    out(D, f'B{r}', f_, size=9, wrap=True)
    D.merge_cells(f'B{r}:D{r}')
    note(D, f'E{r}', why)
    D.merge_cells(f'E{r}:J{r}')
verdict_cf(D, f'B{AC0}:B{AC0 + ACN - 1}')
RVER = AC0 + ACN
label(D, f'A{RVER}', 'VEREDICTO DEL LIBRO', bold=True, size=11)
out(D, f'B{RVER}', f'=IF(SUMPRODUCT(--ISNUMBER(SEARCH("BANDERA",B{AC0}:B{AC0 + ACN - 1})))>0,'
                   f'"✗ BANDERA · el libro tiene errores que impiden fiarse del valor",'
                   f'IF(SUMPRODUCT(--ISNUMBER(SEARCH("REVISAR",B{AC0}:B{AC0 + ACN - 1})))>0,'
                   f'"⚠ REVISAR · "&SUMPRODUCT(--ISNUMBER(SEARCH("REVISAR",B{AC0}:B{AC0 + ACN - 1})))'
                   '&" comprobaciones piden atención","✓ LIBRO COHERENTE"))', bold=True, size=11, wrap=True)
D.merge_cells(f'B{RVER}:D{RVER}')
verdict_cf(D, f'B{RVER}:D{RVER}')
widths(D, {'A': 52, 'B': 20, 'C': 20, 'D': 20, 'E': 13, 'F': 13, 'G': 13, 'H': 13, 'I': 13, 'J': 13})
D.freeze_panes = 'B3'
D.sheet_view.showGridLines = False

# ================================================================== Motor (oculta)
M = wb.create_sheet(MO)
M['A1'] = 'MOTOR V6 · una fila por cálculo. No tocar: lo usan Análisis, Palancas, Diagnóstico V6 y Panel.'
M['A1'].font = Font(name=F, size=10, bold=True)
for i, h in enumerate(['Cálculo', 'Motor', 'Nivel L0', 'm0', 'g años 1–5', 'm objetivo', 'S2C', 'g para siempre',
                       'ROIC/ROE largo', 'Tasa de descuento', 't', 'f', 'Ajuste', 'p quiebra', 'Recuperación', 'Acciones']):
    M.cell(4, 1 + i, h).font = Font(name=F, size=9, bold=True)
for nm, start in (('g_t', 17), ('L_t', 27), ('m_t', 37), ('flujo_t', 47)):
    for t in range(1, 11):
        M.cell(3, start + t - 1, t)
        M.cell(4, start + t - 1, f'{nm} {t}').font = Font(name=F, size=9, bold=True)
for i, h in enumerate(['VP flujos 1–10', 'Flujo año 11', 'Valor terminal', 'VP terminal', 'Total antes de quiebra',
                       'Valor final', 'Por acción', 'Sin crecimiento', 'Crec. FCF 1→10', '% terminal',
                       'Sin crecimiento por acción', 'Reinversión año 1', 'ROIC marginal', 'Nivel año 10', 'Válido',
                       'Motivo']):
    M.cell(4, 57 + i, h).font = Font(name=F, size=9, bold=True)


def engine_row(n, lab, motor, L0, m0, g1, mT, s2c, ginf, roic, d, tau, f_, adj, p, rec, sh, extra_ok=None):
    for i, v in enumerate([lab, motor, L0, m0, g1, mT, s2c, ginf, roic, d, tau, f_, adj, p, rec, sh]):
        M.cell(n, 1 + i, v)
    ok = f'$BS{n}'
    M[f'BS{n}'] = (f'=AND(OR($B{n}="A",$B{n}="B",$B{n}="C"),ISNUMBER($C{n}),ISNUMBER($D{n}),ISNUMBER($E{n}),'
                   f'ISNUMBER($F{n}),ISNUMBER($H{n}),ISNUMBER($I{n}),ISNUMBER($J{n}),ISNUMBER($K{n}),ISNUMBER($L{n}),'
                   f'$J{n}>$H{n},$I{n}>0,$I{n}>$H{n},N($C{n})>0,OR($B{n}="C",AND(ISNUMBER($G{n}),N($G{n})>0))'
                   f'{"," + extra_ok if extra_ok else ""})')
    for t in range(1, 11):
        gc, lc, mc, fc = CL(16 + t), CL(26 + t), CL(36 + t), CL(46 + t)
        prevL = f'$C{n}' if t == 1 else f'{CL(25 + t)}{n}'
        M[f'{gc}{n}'] = f'=IF({ok},IF({gc}$3<=5,$E{n},$E{n}-($E{n}-$H{n})*({gc}$3-5)/5),"")'
        M[f'{lc}{n}'] = f'=IF({ok},{prevL}*(1+{gc}{n}),"")'
        M[f'{mc}{n}'] = f'=IF({ok},$D{n}+($F{n}-$D{n})*MIN({mc}$3,5)/5,"")'
        M[f'{fc}{n}'] = (f'=IF({ok},IF($B{n}="C",{prevL}*{mc}{n}-({lc}{n}-{prevL}),'
                         f'{lc}{n}*({mc}{n}*(1-$K{n})-$L{n})-({lc}{n}-{prevL})/$G{n}),"")')
    M[f'BE{n}'] = f'=IF({ok},SUMPRODUCT(AU{n}:BD{n}/(1+$J{n})^$AU$3:$BD$3),"")'
    M[f'BF{n}'] = f'=IF({ok},IF($B{n}="C",AJ{n}*($I{n}-$H{n}),AJ{n}*(1+$H{n})*($F{n}*(1-$K{n})*(1-$H{n}/$I{n})-$L{n})),"")'
    M[f'BG{n}'] = f'=IF({ok},BF{n}/($J{n}-$H{n}),"")'
    M[f'BH{n}'] = f'=IF({ok},BG{n}/(1+$J{n})^10,"")'
    M[f'BI{n}'] = f'=IF({ok},BE{n}+BH{n}+$M{n},"")'
    M[f'BJ{n}'] = f'=IF({ok},(1-$N{n})*BI{n}+$N{n}*$O{n},"")'
    M[f'BK{n}'] = f'=IF(AND({ok},N($P{n})>0),BJ{n}/$P{n},"")'
    M[f'BL{n}'] = f'=IF({ok},IF($B{n}="C",$C{n}*$D{n}/$J{n},$C{n}*($D{n}*(1-$K{n})-$L{n})/$J{n})+$M{n},"")'
    M[f'BM{n}'] = f'=IF(AND({ok},N(AU{n})>0,N(BD{n})>0),(BD{n}/AU{n})^(1/9)-1,"")'
    M[f'BN{n}'] = f'=IF({ok},IF((BE{n}+BH{n})<>0,BH{n}/(BE{n}+BH{n}),""),"")'
    M[f'BO{n}'] = f'=IF(AND({ok},N($P{n})>0),BL{n}/$P{n},"")'
    M[f'BP{n}'] = (f'=IF({ok},IFERROR(IF($B{n}="C",(AA{n}-$C{n})/($C{n}*AK{n}),'
                   f'((AA{n}-$C{n})/$G{n})/(AA{n}*AK{n}*(1-$K{n}))),""),"")')
    M[f'BQ{n}'] = f'=IF(AND({ok},$B{n}<>"C"),$F{n}*(1-$K{n})*$G{n},"")'
    M[f'BR{n}'] = f'=IF({ok},AJ{n},"")'
    M[f'BT{n}'] = (f'=IF({ok},"",IF(NOT(OR($B{n}="A",$B{n}="B",$B{n}="C")),"Sin motor: C62 dice otro método",'
                   f'IF(NOT(AND(ISNUMBER($C{n}),ISNUMBER($D{n}))),"Falta Historia (ventas, margen o patrimonio)",'
                   f'IF(NOT(ISNUMBER($L{n})),"Falta f: revisa Historia C57 y Análisis C52",'
                   f'IF(NOT(AND(ISNUMBER($E{n}),ISNUMBER($F{n}),ISNUMBER($I{n}))),"Faltan palancas",'
                   f'IF(AND($B{n}<>"C",NOT(N($G{n})>0)),"Falta S2C (> 0)",'
                   f'IF(NOT(ISNUMBER($J{n})),"Falta la tasa de descuento",'
                   f'IF(NOT(ISNUMBER($H{n})),"Falta g para siempre",'
                   f'IF($J{n}<=$H{n},"g para siempre ≥ tasa de descuento",'
                   f'IF($I{n}<=0,"ROIC ≤ 0",IF($I{n}<=$H{n},"ROIC ≤ g para siempre",IF(N($C{n})<=0,"Ventas (o patrimonio) de partida ≤ 0","Revisa las palancas"))))))))))))')


MOTOR = f'{DG}!${D_MOTOR}'
L0 = f'IF({MOTOR}="C",{DG}!${D_B0},{DG}!${D_V0})'
M0 = f'IF({MOTOR}="C",{DG}!${D_ROE0},{DG}!${D_M0})'
TAU = f'IF({MOTOR}="C",0,N({DG}!${D_TAU}))'
FUG = f'IF({MOTOR}="A",{DG}!${D_F},0)'
ADJ = f'IF({MOTOR}="B",-N({DG}!${D_PAS}),IF({MOTOR}="A",N(Análisis!$C$76),0))'
DISC = f'IF({MOTOR}="B",{DG}!${D_ROP},Análisis!$C$56)'
PQ, REC, SH = f'N({PAL}!${C_PQ})', f'N({PAL}!${C_REC})', 'Análisis!$C$55'


def put_scen(n, lab, col, dr=0.0, dg=0.0, ov=None):
    o = ov or {}
    g1 = o.get('g1', f'{PAL}!{col}{R_CREC}')
    mT = o.get('mT', f'{PAL}!{col}{R_MARG}')
    s2c = o.get('s2c', f'IF({MOTOR}="C",1,{PAL}!{col}{R_S2C})')
    gi = o.get('ginf', f'Análisis!{col}68')
    ro = o.get('roic', f'{PAL}!{col}{R_ROIC}')
    d = o.get('d', DISC)
    engine_row(n, lab, f'={MOTOR}', f'={L0}', f'={M0}', f'={g1}', f'={mT}', f'={s2c}',
               f'=IF(ISNUMBER({gi}),{gi}+({dg}),"")', f'={ro}', f'=IF(ISNUMBER({d}),{d}+({dr}),"")',
               f'={TAU}', f'={FUG}', f'={ADJ}', f'={PQ}', f'={REC}', f'={SH}')


put_scen(6, 'MALO', 'B'); put_scen(7, 'NORMAL', 'C'); put_scen(8, 'BUENO', 'D')
IDX = f'MAX(1,IFERROR(MATCH({PA}!$C$6,Opciones!$O$3:$O$5,0),2))'
ON = f'({PA}!$F$6="ON")'
PR0 = 20   # primera fila de palancas del Panel (debe coincidir con la hoja Panel)
ST = {'g1': ('$E$20', 0.005), 'mT': ('$E$21', 0.005), 's2c': ('$E$22', 0.05), 'ginf': ('$E$23', 0.001),
      'roic': ('$E$24', 0.01), 'd': ('$E$25', 0.0025)}
ch = lambda row, sheet=PAL: f'CHOOSE({IDX},{sheet}!B{row},{sheet}!C{row},{sheet}!D{row})'
dl = lambda c, s: f'IF({ON},({PA}!{c}-20)*{s},0)'
est = {'g1': f'{ch(R_CREC)}+{dl(*ST["g1"])}', 'mT': f'{ch(R_MARG)}+{dl(*ST["mT"])}',
       's2c': f'IF({MOTOR}="C",1,MAX(0.05,{ch(R_S2C)}+{dl(*ST["s2c"])}))',
       'ginf': f'{ch(68, "Análisis")}+{dl(*ST["ginf"])}',
       'roic': f'MAX(0.001,{ch(R_ROIC)}+{dl(*ST["roic"])})', 'd': f'{DISC}+{dl(*ST["d"])}'}
engine_row(9, 'ESTUDIO (Panel)', f'={MOTOR}', f'={L0}', f'={M0}',
           *[f'=IFERROR({est[k]},"")' for k in ('g1', 'mT', 's2c', 'ginf', 'roic', 'd')],
           f'={TAU}', f'={FUG}', f'={ADJ}', f'={PQ}', f'={REC}', f'={SH}', extra_ok=f'INDEX($BS$6:$BS$8,{IDX})')
SENS, n = {}, 12
for col in 'BCD':
    for dr in (-0.02, 0.0, 0.02):
        for dg in (-0.005, 0.0, 0.005):
            put_scen(n, f'Sens {col} r{dr:+.2f} g{dg:+.3f}', col, dr, dg)
            SENS[(col, dr, dg)] = n
            n += 1
TOR, n = [], 41
TORDEF = [('Crecimiento 1–5 (±2 pts)', 'g1', f'{PAL}!C{R_CREC}', 0.02),
          ('Margen / ROE objetivo (±2 pts)', 'mT', f'{PAL}!C{R_MARG}', 0.02),
          ('S2C (±0,3)', 's2c', f'IF({MOTOR}="C",1,{PAL}!C{R_S2C})', 0.3),
          ('g perpetuo (±0,5 pts)', 'ginf', None, 0.005),
          ('ROIC / ROE largo plazo (±5 pts)', 'roic', f'{PAL}!C{R_ROIC}', 0.05),
          ('Tasa de descuento (±1 pt)', 'd', DISC, 0.01)]
for nm, key, base, step in TORDEF:
    pair = []
    for sgn in (-1, 1):
        if key == 'ginf':
            put_scen(n, f'T {nm} {sgn}', 'C', 0.0, sgn * step)
        elif key == 'd':
            put_scen(n, f'T {nm} {sgn}', 'C', sgn * step, 0.0)
        elif key == 's2c':
            put_scen(n, f'T {nm} {sgn}', 'C', ov={'s2c': f'IF(ISNUMBER({base}),MAX(0.05,{base}+({sgn * step})),"")'})
        else:
            put_scen(n, f'T {nm} {sgn}', 'C', ov={key: f'IF(ISNUMBER({base}),{base}+({sgn * step}),"")'})
        pair.append(n); n += 1
    TOR.append((nm, pair))
REV0 = 56
for i in range(81):
    put_scen(REV0 + i, f'Inverso {i}', 'C', ov={'g1': f'Análisis!$A${108 + i}'})
# comprobación de monotonía del DCF inverso
M['A190'] = 'DCF inverso · comprobación de la curva'
M['A191'] = 'Tramos al alza (de 80)'
M['B191'] = f'=IF(COUNT($BK${REV0}:$BK${REV0 + 80})<81,"",SUMPRODUCT(--($BK${REV0 + 1}:$BK${REV0 + 80}>$BK${REV0}:$BK${REV0 + 79})))'
M['A192'] = 'Recorrido del valor en la tabla'
M['B192'] = f'=IF(COUNT($BK${REV0}:$BK${REV0 + 80})<81,"",MAX($BK${REV0}:$BK${REV0 + 80})-MIN($BK${REV0}:$BK${REV0 + 80}))'
M['A193'] = 'Veredicto'
M['B193'] = ('=IF(B191="","—",IF(B191=0,"⚠ REVISAR · con tus palancas crecer destruye valor: el DCF inverso no aplica",'
             'IF(B191<80,"⚠ REVISAR · el valor no crece de forma continua con el crecimiento: el DCF inverso no aplica",'
             'IF(AND(ISNUMBER(Análisis!$C$37),N(Análisis!$C$37)>0),IF(B192<0.05*N(Análisis!$C$37),'
             '"⚠ REVISAR · el valor apenas depende del crecimiento: el DCF inverso no informa","✓ PASA"),"✓ PASA"))))')
# datos de los gráficos
CH = 140
M[f'A{CH}'] = 'GRÁFICO · ventas (historia y escenarios)'
for j, h in enumerate(['Año', 'Historia', 'MALO', 'NORMAL', 'BUENO']):
    M.cell(CH + 1, 1 + j, h)
for k in range(-9, 11):
    r_ = CH + 2 + (k + 9)
    M[f'A{r_}'] = (f'=IF(ISNUMBER({HI}!$L$5),"FY"&({HI}!$L$5+({k})),"t{k:+d}")' if k != 0
                   else f'=IF(ISNUMBER({HI}!$L$5),"FY"&{HI}!$L$5,"t0")')
    if k <= 0:
        hc = CL(12 + k)
        M[f'B{r_}'] = (f'=IF({MOTOR}="C",IF(ISNUMBER({HI}!{hc}21),{HI}!{hc}21,NA()),'
                       f'IF(ISNUMBER({HI}!{hc}6),{HI}!{hc}6,NA()))')
    else:
        M[f'B{r_}'] = '=NA()'
    for j, srow in enumerate((6, 7, 8)):
        colL = CL(3 + j)
        if k < 0:
            M[f'{colL}{r_}'] = '=NA()'
        elif k == 0:
            M[f'{colL}{r_}'] = f'=IF(OR($B$' + str(AGG0_PLACEHOLDER) + f',NOT(ISNUMBER({MO}!$C${srow}))),NA(),{MO}!$C${srow})'
        else:
            M[f'{colL}{r_}'] = f'=IF(OR($B$' + str(AGG0_PLACEHOLDER) + f',NOT(ISNUMBER({MO}!{CL(26 + k)}{srow}))),NA(),{MO}!{CL(26 + k)}{srow})'
VG = 164
M[f'A{VG}'] = 'GRÁFICO · valor por acción frente al precio'
for j, h in enumerate(['Escenario', 'Valor por acción', 'Precio']):
    M.cell(VG + 1, 1 + j, h)
for j, (lab, ref) in enumerate([('MALO', 'Análisis!B78'), ('NORMAL', 'Análisis!C78'), ('BUENO', 'Análisis!D78'),
                                ('Ponderado', 'Análisis!C83')]):
    r_ = VG + 2 + j
    M[f'A{r_}'] = lab
    M[f'B{r_}'] = f'=IF(ISNUMBER({ref}),{ref},NA())'
    M[f'C{r_}'] = f'=IF(OR({GATEP_PLACEHOLDER},NOT(ISNUMBER(Análisis!$C$37))),NA(),Análisis!$C$37)'
TG = 172
M[f'A{TG}'] = 'GRÁFICO · tornado (NORMAL)'
for j, h in enumerate(['Palanca', 'Baja', 'Sube', 'Palanca baja', 'Palanca sube', 'Base']):
    M.cell(TG + 1, 1 + j, h)
for j, (nm, (a_, b_)) in enumerate(TOR):
    r_ = TG + 2 + j
    M[f'A{r_}'] = nm
    M[f'B{r_}'] = f'=IF(OR($B$' + str(AGG0_PLACEHOLDER) + f',NOT(ISNUMBER(BK{a_}))),"",BK{a_})'
    M[f'C{r_}'] = f'=IF(OR($B$' + str(AGG0_PLACEHOLDER) + f',NOT(ISNUMBER(BK{b_}))),"",BK{b_})'
    M[f'D{r_}'] = f'=IF(AND(ISNUMBER(B{r_}),ISNUMBER(BK7)),B{r_}-BK7,0)'
    M[f'E{r_}'] = f'=IF(AND(ISNUMBER(C{r_}),ISNUMBER(BK7)),C{r_}-BK7,0)'
    M[f'F{r_}'] = '=IF(ISNUMBER(BK7),BK7,"")'

# ================================================================== Motor · ESTADO DEL MODELO (validación de dominio)
# Cada regla devuelve en E un texto codificado: "INC|…" (incompleto), "INV|…" (datos inválidos), "NOA|…" (modelo no
# aplicable), "AVI|…" (aviso) o "" (OK). D traduce el código; F muestra la causa; G es el nivel: 1 = bloquea el valor,
# 2 = bloquea la lectura de precio, 3 = solo completitud del libro. El motor NO consulta este bloque (sin circularidad):
# el bloqueo se aplica en las celdas que consumen el resultado.
isA, isB, isC, isAB = f'({MOTOR}="A")', f'({MOTOR}="B")', f'({MOTOR}="C")', f'OR({MOTOR}="A",{MOTOR}="B")'
AN_ = 'Análisis!'
PL_ = f'{PAL}!'
HI_ = f'{HI}!'
nH = f'COUNT({HI_}$C$6:$L$6)'
MON_DIF = (f'AND({PL_}${C_MONEDA}<>"",{MONEDA_MODELO}<>"",UPPER(TRIM({PL_}${C_MONEDA}))<>UPPER(TRIM({MONEDA_MODELO})))')
MON_OK = (f'AND({PL_}${C_MONEDA}<>"",{MONEDA_MODELO}<>"",UPPER(TRIM({PL_}${C_MONEDA}))=UPPER(TRIM({MONEDA_MODELO})))')
# ratio ADR = acciones ordinarias por cada ADR/ADS (número). Solo 1 demuestra que precio y valor usan la misma unidad.
ADR_OK = f'AND(ISNUMBER({RATIO_ADR}),N({RATIO_ADR})=1)'
ADR_NV = (f'OR(AND({PL_}${C_CAUSA}="ADR o ADS",NOT({ADR_OK})),AND({RATIO_ADR}<>"",NOT({ADR_OK})))')
CAUSA_DECL = f'AND({PL_}${C_CAUSA}<>"",{PL_}${C_CAUSA}<>"Ninguna")'
DESV = f'ABS({AN_}$C$41/({AN_}$C$37*{AN_}$C$55)-1)'
TOL1, TOL2 = f'{DG}!$C$91', f'{DG}!$C$92'
RUL0 = 201
RULES = [
 ('V01', 'Motor elegido (Análisis C62)', '1', 'TRUE',
  f'=IF({AN_}$C$62="","INC|Falta elegir el motor en Análisis C62",IF({MOTOR}="—","NOA|Análisis C62 dice que esta empresa requiere otro método",""))'),
 ('V02', 'Historia: al menos 5 ejercicios con ventas', '1', 'TRUE',
  f'=IF({nH}=0,"INC|Historia vacía: faltan los años de datos (Historia C6:L6)",IF({nH}<5,"INC|Historia con solo "&{nH}&" ejercicios (mínimo 5)",""))'),
 ('V03', 'Historia: el año más reciente en la columna L', '1', 'TRUE',
  f'=IF(AND({nH}>0,NOT(ISNUMBER({HI_}$L$6))),"INV|El año más reciente no está en la columna L de Historia","")'),
 ('V04', 'Historia: años consecutivos y sin huecos', '1', 'TRUE',
  f'=IF({nH}<2,"",IF(COUNT(OFFSET({HI_}$L$5,0,1-{nH},1,{nH}))<>{nH},"INV|Años de Historia (fila 5) no numéricos o incompletos",IF(MAX(OFFSET({HI_}$L$5,0,1-{nH},1,{nH}))>3000,"INV|Años de Historia (fila 5) escritos como fecha: escribe solo el año (p. ej. 2025)",'
  f'IF(OR(COUNT(OFFSET({HI_}$L$6,0,1-{nH},1,{nH}))<>{nH},SUMPRODUCT(--(OFFSET({HI_}$L$5,0,2-{nH},1,{nH}-1)-OFFSET({HI_}$L$5,0,1-{nH},1,{nH}-1)<>1))>0),'
  f'"INV|Historia con huecos, años repetidos o no consecutivos (fila 5 y ventas)",""))))'),
 ('V05', 'Años de la media del FCF base (Historia C57) · motor A', '1', isA,
  f'=IF({HI_}$C$57="","INC|Falta Historia C57 (años de la media del FCF base)",IF(NOT(ISNUMBER({HI_}$C$57)),"INV|Historia C57 no es un número",'
  f'IF({HI_}$C$57<>INT({HI_}$C$57),"INV|Historia C57 ("&{HI_}$C$57&") debe ser un número entero de ejercicios",IF({nH}=0,"",IF(OR({HI_}$C$57<1,{HI_}$C$57>{nH}),'
  f'"INV|Historia C57 ("&{HI_}$C$57&") fuera de rango: entre 1 y los ejercicios con ventas ("&{nH}&")","")))))'),
 ('V06', 'Precio actual (Análisis C37)', '1', 'TRUE',
  f'=IF({AN_}$C$37="","INC|Falta el precio (Análisis C37)",IF(OR(NOT(ISNUMBER({AN_}$C$37)),{AN_}$C$37<=0),"INV|Precio (Análisis C37) no numérico o ≤ 0",""))'),
 ('V07', 'Acciones diluidas (Análisis C55)', '1', 'TRUE',
  f'=IF({AN_}$C$55="","INC|Faltan las acciones diluidas (Análisis C55)",IF(OR(NOT(ISNUMBER({AN_}$C$55)),{AN_}$C$55<=0),"INV|Acciones diluidas (Análisis C55) no numéricas o ≤ 0",""))'),
 ('V08', 'Rentabilidad exigida r (Análisis C56)', '1', 'TRUE',
  f'=IF({AN_}$C$56="","INC|Falta la rentabilidad exigida r (Análisis C56)",IF(OR(NOT(ISNUMBER({AN_}$C$56)),{AN_}$C$56<=0),"INV|r (Análisis C56) no numérica o ≤ 0",""))'),
 ('V09', 'Datos del FCF base (Análisis C46–C51): tipo y dominio', '1', 'TRUE',
  f'=IF(OR(AND({AN_}$C$46<>"",NOT(ISNUMBER({AN_}$C$46))),AND({AN_}$C$47<>"",NOT(ISNUMBER({AN_}$C$47))),AND({AN_}$C$50<>"",NOT(ISNUMBER({AN_}$C$50)))),"INV|Texto donde va un número en los datos del FCF base (Análisis C46, C47 o C50)",'
  f'IF(OR(AND({AN_}$C$48<>"",NOT(ISNUMBER({AN_}$C$48))),AND({AN_}$C$49<>"",NOT(ISNUMBER({AN_}$C$49)))),"INV|Texto donde va un número en intereses o arrendamientos (Análisis C48, C49)",'
  f'IF(AND({AN_}$C$51<>"",NOT(OR(EXACT({AN_}$C$51,"Sí"),EXACT({AN_}$C$51,"No")))),"INV|Análisis C51 fuera de dominio: solo Sí o No (exacto)",IF(AND(ISNUMBER({AN_}$C$47),{AN_}$C$47<0),"INV|Capex negativo en Análisis C47: escríbelo en positivo",'
  f'IF(AND({isA},OR({AN_}$C$46="",{AN_}$C$47="",{AN_}$C$50="",{AN_}$C$51="")),"INC|Faltan datos del FCF base (Análisis C46, C47, C50 o C51)","")))))'),
 ('V10', 'FCF base ≤ 0 · motor A', '1', isA,
  f'=IF(NOT(ISNUMBER({AN_}$C$52)),"",IF({AN_}$C$52>0,"",IF(AND(OR({PL_}${C_FCFNAT}="Transitorio",{PL_}${C_FCFNAT}="Extraordinario"),'
  f'ISNUMBER({PL_}${C_FCFNORM}),N({PL_}${C_FCFNORM})>0),"AVI|FCF base ≤ 0 declarado "&LOWER({PL_}${C_FCFNAT})&": f se calibra con el FCF normalizado de Palancas C44 ("'
  f'&FIXED({PL_}${C_FCFNORM},0)&" mm)",IF({PL_}${C_FCFNAT}="Estructural","NOA|FCF base ≤ 0 declarado estructural: el motor A no puede calibrarse; usa el motor B (Análisis C62)",'
  f'"NOA|FCF base ≤ 0: declara su naturaleza en Palancas C43 y, si procede, un FCF normalizado en C44; o usa el motor B"))))'),
 ('V11', 'Tipo de empresa frente a motor (Palancas C6)', '1', 'TRUE',
  f'=IF({PL_}${C_CASO}="","",IF(AND({PL_}${C_CASO}="Financiera (banco o aseguradora)",{isAB}),"NOA|Una financiera no puede valorarse con los motores A o B: usa el motor C (Análisis C62)",'
  f'IF({PL_}${C_CASO}="Regulada (red, concesión)","AVI|Regulada: el modelo no recoge el marco regulatorio ni la base de activos; lee el valor con cautela",'
  f'IF({PL_}${C_CASO}="Multinegocio o conglomerado","AVI|Conglomerado: un solo juego de palancas mezcla negocios distintos; considera valorar por partes",""))))'),
 ('V12', 'Crecimiento años 1–5 (Palancas B14:D14)', '1', 'TRUE',
  f'=IF(COUNTA({PL_}$B${R_CREC}:$D${R_CREC})>COUNT({PL_}$B${R_CREC}:$D${R_CREC}),"INV|Crecimiento no numérico en Palancas B14:D14",IF(COUNT({PL_}$B${R_CREC}:$D${R_CREC})<3,"INC|Faltan palancas de crecimiento (Palancas B14:D14)",IF(MIN({PL_}$B${R_CREC}:$D${R_CREC})<=-1,"INV|Crecimiento ≤ −100 % en Palancas B14:D14",IF(MAX({PL_}$B${R_CREC}:$D${R_CREC})>1,"AVI|Crecimiento anual superior al 100 % en Palancas B14:D14: revisa que no sea un error de unidades",""))))'),
 ('V13', 'Margen o ROE objetivo (Palancas B15:D15)', '1', 'TRUE',
  f'=IF(COUNTA({PL_}$B${R_MARG}:$D${R_MARG})>COUNT({PL_}$B${R_MARG}:$D${R_MARG}),"INV|Margen o ROE objetivo no numérico en Palancas B15:D15",IF(COUNT({PL_}$B${R_MARG}:$D${R_MARG})<3,"INC|Faltan márgenes objetivo (Palancas B15:D15)",""))'),
 ('V14', 'Ventas por euro reinvertido (Palancas B16:D16) · motores A y B', '1', isAB,
  f'=IF(COUNTA({PL_}$B${R_S2C}:$D${R_S2C})>COUNT({PL_}$B${R_S2C}:$D${R_S2C}),"INV|S2C no numérico en Palancas B16:D16 (con los motores A y B tiene que ser un número > 0)",IF(COUNT({PL_}$B${R_S2C}:$D${R_S2C})<3,"INC|Faltan ventas por euro reinvertido (Palancas B16:D16)",IF(MIN({PL_}$B${R_S2C}:$D${R_S2C})<=0,"INV|S2C ≤ 0 en Palancas B16:D16",IF(MIN({PL_}$B${R_S2C}:$D${R_S2C})<0.05,"AVI|S2C menor que 0,05 en Palancas B16:D16: cada euro de ventas nuevas exigiría más de 20 de inversión; revisa unidades",""))))'),
 ('V15', 'g para siempre (Análisis B68:D68)', '1', 'TRUE',
  f'=IF(COUNTA({AN_}$B$68:$D$68)>COUNT({AN_}$B$68:$D$68),"INV|g para siempre no numérico en Análisis B68:D68",IF(COUNT({AN_}$B$68:$D$68)<3,"INC|Faltan crecimientos perpetuos (Análisis B68:D68)",IF(OR(MIN({AN_}$B$68:$D$68)<-0.1,MAX({AN_}$B$68:$D$68)>0.1),'
  f'"INV|g para siempre fuera de [−10 %, 10 %] (Análisis B68:D68)",IF(AND(COUNT($J$6:$J$8)=3,OR({AN_}$B$68>=$J$6,{AN_}$C$68>=$J$7,{AN_}$D$68>=$J$8)),'
  f'"INV|g para siempre ≥ tasa de descuento del motor ("&FIXED(100*$J$7,1)&" %) en algún escenario",""))))'),
 ('V16', 'ROIC o ROE a largo plazo (Palancas B18:D18)', '1', 'TRUE',
  f'=IF(COUNTA({PL_}$B${R_ROIC}:$D${R_ROIC})>COUNT({PL_}$B${R_ROIC}:$D${R_ROIC}),"INV|ROIC a largo plazo no numérico en Palancas B18:D18",IF(COUNT({PL_}$B${R_ROIC}:$D${R_ROIC})<3,"INC|Faltan ROIC a largo plazo (Palancas B18:D18)",IF(MIN({PL_}$B${R_ROIC}:$D${R_ROIC})<=0,"INV|ROIC a largo plazo ≤ 0 (Palancas B18:D18)",'
  f'IF(OR({PL_}$B${R_ROIC}<=N({AN_}$B$68),{PL_}$C${R_ROIC}<=N({AN_}$C$68),{PL_}$D${R_ROIC}<=N({AN_}$D$68)),"INV|ROIC a largo plazo ≤ g para siempre en algún escenario",""))))'),
 ('V17', 'Probabilidades de los escenarios (Análisis B69:D69)', '1', 'TRUE',
  f'=IF(COUNTA({AN_}$B$69:$D$69)>COUNT({AN_}$B$69:$D$69),"INV|Probabilidad no numérica en Análisis B69:D69",IF(COUNT({AN_}$B$69:$D$69)<3,"INC|Faltan probabilidades (Análisis B69:D69)",IF(OR(ROUND(MIN({AN_}$B$69:$D$69),9)<0,ROUND(MAX({AN_}$B$69:$D$69),9)>1),'
  f'"INV|Alguna probabilidad fuera de [0, 1] (Análisis B69:D69)",IF(ROUND(ABS(SUM({AN_}$B$69:$D$69)-1),9)>0.001,"INV|Las probabilidades suman "&FIXED(100*SUM({AN_}$B$69:$D$69),1)&" %, no 100 %",""))))'),
 ('V18', 'Tipo impositivo medio (Historia C52) · motores A y B', '1', isAB,
  f'=IF(NOT(ISNUMBER({HI_}$C$52)),"INC|Falta el tipo impositivo medio (Historia fila 10, últimos 5 años)",IF(OR({HI_}$C$52<0,{HI_}$C$52>1),'
  f'"INV|Tipo impositivo fuera de [0, 1] (Historia C52 = "&FIXED(100*{HI_}$C$52,1)&" %)",IF(OR(MIN({HI_}$C$10:$L$10)<0,MAX({HI_}$C$10:$L$10)>1),"AVI|Algún año de Historia tiene un tipo impositivo fuera de [0, 1] (fila 10): revisa que no sea un error","")))'),
 ('V19', 'Probabilidad de quiebra (Palancas C22)', '1', 'TRUE',
  f'=IF({PL_}${C_PQ}="","",IF(OR(NOT(ISNUMBER({PL_}${C_PQ})),{PL_}${C_PQ}<0,{PL_}${C_PQ}>1),"INV|Probabilidad de quiebra fuera de [0, 1] (Palancas C22)",""))'),
 ('V20', 'Recuperación si quiebra (Palancas C23)', '1', 'TRUE',
  f'=IF({PL_}${C_REC}="","",IF(NOT(ISNUMBER({PL_}${C_REC})),"INV|Recuperación si quiebra no numérica (Palancas C23)",IF({PL_}${C_REC}<0,"INV|Recuperación si quiebra negativa (Palancas C23)",'
  f'IF(AND(ISNUMBER($BI$8),N({PL_}${C_PQ})>0,{PL_}${C_REC}>$BI$8),"AVI|La recuperación si quiebra ("&FIXED({PL_}${C_REC},0)&" mm) supera el valor del escenario BUENO antes del ajuste ("&FIXED($BI$8,0)&" mm)",""))))'),
 ('V21', 'Historia de cada escenario (Análisis B65:D65)', '1', 'TRUE',
  f'=IF(OR({AN_}$B$65="",{AN_}$C$65="",{AN_}$D$65=""),"INC|Falta «¿qué tiene que pasar?» en algún escenario (Análisis B65:D65)","")'),
 ('V22', 'Capitalización (Análisis C41)', '1', 'TRUE',
  f'=IF({AN_}$C$41="","INC|Falta la capitalización (Análisis C41)",IF(OR(NOT(ISNUMBER({AN_}$C$41)),{AN_}$C$41<=0),"INV|Capitalización (Análisis C41) no numérica o ≤ 0",""))'),
 ('V23', 'Deuda y r operativa · motor B', '1', isB,
  f'=IF(OR(AND({HI_}$L$15<>"",NOT(ISNUMBER({HI_}$L$15))),AND({HI_}$L$22<>"",NOT(ISNUMBER({HI_}$L$22))),AND({HI_}$L$23<>"",NOT(ISNUMBER({HI_}$L$23)))),"INV|Motor B: intereses o deuda del último año no numéricos (Historia L15, L22, L23)",IF(NOT(ISNUMBER({HI_}$C$64)),"INC|Motor B: falta la deuda del último año (Historia L22:L23)",IF(NOT(ISNUMBER({DG}!${D_ROP})),"INC|Motor B: no se puede calcular la r operativa (Historia L15, L22, L23 y Análisis C41)","")))'),
 ('V24', 'Patrimonio y ROE de partida · motor C', '1', isC,
  f'=IF(OR(ISTEXT({HI_}$L$9),ISTEXT({HI_}$L$21)),"INV|Motor C: patrimonio o beneficio del último año no numéricos (Historia L9, L21)",IF(OR(NOT(ISNUMBER({HI_}$C$59)),NOT(ISNUMBER({HI_}$C$60))),"INC|Motor C: faltan patrimonio o beneficio del último año (Historia L9, L21)",""))'),
 ('V25', 'Moneda de cotización frente a moneda del modelo', '2', 'TRUE',
  f'=IF({PL_}${C_MONEDA}="","AVI|Moneda de cotización no declarada (Palancas C48): sin ella no se compara precio con valor",'
  f'IF({MONEDA_MODELO}="","AVI|Moneda del modelo no declarada (Control maestro H4): sin ella no se compara precio con valor",IF({MON_DIF},"AVI|Moneda de cotización ("&{PL_}${C_MONEDA}&") distinta de la del modelo ("&{MONEDA_MODELO}&"): sin margen de seguridad ni conclusiones de precio","")))'),
 ('V26', 'ADR: unidad cotizada frente a la unidad del valor', '2', 'TRUE',
  f'=IF({PL_}${C_CAUSA}="ADR o ADS",IF(OR({RATIO_ADR}="",NOT(ISNUMBER({RATIO_ADR})),N({RATIO_ADR})<=0),"AVI|ADR declarado sin ratio numérico documentado (Control maestro D5 = acciones ordinarias por ADR): comparabilidad no verificada",'
  f'IF(N({RATIO_ADR})<>1,"AVI|Precio por ADR y valor por acción ordinaria son unidades distintas (ratio "&{RATIO_ADR}&"): convierte el precio de Análisis C37 a por acción, documéntalo y pon el ratio en 1","")),'
  f'IF(AND({RATIO_ADR}<>"",NOT({ADR_OK})),"AVI|Control maestro D5 contiene «"&{RATIO_ADR}&"»"&IF(ISNUMBER({RATIO_ADR}),""," (como texto)")&" sin causa ADR declarada (Palancas C47): escribe el número 1 si el precio ya es por acción ordinaria, o declara la causa; hasta entonces la unidad queda sin verificar",""))'),
 ('V27', 'Conciliación: capitalización ≈ precio × acciones', f'=IF({isB},1,2)', 'TRUE',
  f'=IF(OR(NOT(ISNUMBER({AN_}$C$37)),NOT(ISNUMBER({AN_}$C$41)),NOT(ISNUMBER({AN_}$C$55)),N({AN_}$C$37)<=0,N({AN_}$C$41)<=0,N({AN_}$C$55)<=0),"NEV|Conciliación no evaluable: faltan precio, capitalización o acciones válidos",'
  f'IF(NOT({MON_OK}),"AVI|Conciliación de capitalización no evaluable: moneda sin declarar o distinta",IF({ADR_NV},"AVI|Conciliación de capitalización: comparabilidad no verificada (unidad cotizada)",'
  f'IF({DESV}<={TOL1},"",IF({CAUSA_DECL},"AVI|Capitalización difiere "&FIXED(100*{DESV},1)&" % de precio × acciones; causa declarada: "&{PL_}${C_CAUSA}&" (no demuestra que esté corregida)",'
  f'IF({DESV}<={TOL2},"AVI|Capitalización difiere "&FIXED(100*{DESV},1)&" % de precio × acciones: declara la causa en Palancas C47",'
  f'"INV|Capitalización difiere "&FIXED(100*{DESV},1)&" % de precio × acciones sin causa declarada: revisa unidades, moneda, ADR o split"))))))'),
 ('V28', 'Fechas del precio y de las acciones', '3', 'TRUE',
  f'=IF(OR(AND({PL_}${C_FPRECIO}<>"",NOT(ISNUMBER({PL_}${C_FPRECIO}))),AND({PL_}${C_FACC}<>"",NOT(ISNUMBER({PL_}${C_FACC})))),"AVI|Fecha del precio o de las acciones escrita como texto (Palancas C45, C46): escríbela como fecha",IF(OR(NOT(ISNUMBER({PL_}${C_FPRECIO})),NOT(ISNUMBER({PL_}${C_FACC}))),"NEV|Fechas del precio y de las acciones sin informar (Palancas C45, C46)",IF(ABS({PL_}${C_FPRECIO}-{PL_}${C_FACC})>{DG}!$C$93,"AVI|Precio y acciones con fechas separadas más de "&{DG}!$C$93&" días (Palancas C45, C46)","")))'),
 ('V30', 'Los países suman 100 %', '3', 'TRUE',
  f'=IF(COUNTA({PL_}$A${PAIS0}:$A${PAIS0 + 5})>COUNT({PL_}$C${PAIS0}:$C${PAIS0 + 5}),"AVI|Algún país o región de Palancas A28:A33 no está en la hoja Riesgo país: su prima cuenta como 0",IF(N({PL_}$B${PTOT})=0,"",IF(ABS({PL_}$B${PTOT}-1)>0.02,"AVI|Los países de Palancas no suman 100 % ("&FIXED(100*{PL_}$B${PTOT},0)&" %)","")))'),
 ('V31', 'Vigencia de las tablas de sector y país', '3', 'TRUE',
  f'=IF(AND({AN_}$D$4<>"",NOT(ISNUMBER({AN_}$D$4))),"AVI|Fecha de análisis escrita como texto (Análisis D4): escríbela como fecha",IF(NOT(ISNUMBER({AN_}$D$4)),"",IF(OR(AND(ISNUMBER({SE}!$B$3),{AN_}$D$4<{SE}!$B$3),AND(ISNUMBER(\'Riesgo país\'!$B$2),{AN_}$D$4<\'Riesgo país\'!$B$2)),"AVI|La fecha de análisis (Análisis D4) es anterior a la fecha de las tablas de sector o país: revisa las fechas",IF(OR(AND(ISNUMBER({SE}!$B$3),{AN_}$D$4-{SE}!$B$3>30.4*\'Diagnóstico V6\'!$C$94),AND(ISNUMBER(\'Riesgo país\'!$B$2),{AN_}$D$4-\'Riesgo país\'!$B$2>30.4*\'Diagnóstico V6\'!$C$94)),"AVI|Tablas de sector o de país con más de "&\'Diagnóstico V6\'!$C$94&" meses respecto a la fecha de análisis: actualízalas (Sector, Riesgo país)",""))))'),
 ('V32', 'Ventas o patrimonio del último año > 0 (Historia L6 / L21)', '1', 'TRUE',
  f'=IF({nH}=0,"",IF({isC},IF({HI_}$L$21="","",IF(OR(NOT(ISNUMBER({HI_}$L$21)),N({HI_}$L$21)<=0),"INV|Patrimonio del último año no numérico o ≤ 0 (Historia L21): el motor C no puede partir de ahí","")),'
  f'IF(OR(NOT(ISNUMBER({HI_}$L$6)),N({HI_}$L$6)<=0),"INV|Ventas del último año no numéricas o ≤ 0 (Historia L6)","")))'),
 ('V33', 'EBIT del último año (Historia L7) · motores A y B', '1', isAB,
  f'=IF({nH}=0,"",IF({HI_}$L$7="","INC|Falta el EBIT del último año (Historia L7): sin él no hay margen de partida",IF(NOT(ISNUMBER({HI_}$L$7)),"INV|EBIT del último año no numérico (Historia L7)","")))'),
 ('V34', 'Exceso de caja no operativo (Análisis C76)', '2', 'TRUE',
  f'=IF({AN_}$C$76="","",IF(NOT(ISNUMBER({AN_}$C$76)),"INV|Exceso de caja (Análisis C76) no numérico",IF(NOT({isA}),IF(N({AN_}$C$76)<>0,"AVI|Análisis C76 no se usa con el motor "&{MOTOR}&": déjalo vacío",""),IF({AN_}$C$76<0,"INV|Exceso de caja (Análisis C76) negativo",IF(AND(ISNUMBER({AN_}$C$53),{AN_}$C$76>{AN_}$C$53),"AVI|El exceso de caja (Análisis C76) supera la caja del balance (Análisis C53)","")))))'),
 ('V37', 'Historia: solo números en C5:L26', '1', 'TRUE',
  f'=IF(SUMPRODUCT(--({HI_}$C$5:$L$26<>""),--NOT(ISNUMBER({HI_}$C$5:$L$26)))>0,"INV|Texto u otros valores no numéricos en Historia C5:L26 ("&SUMPRODUCT(--({HI_}$C$5:$L$26<>""),--NOT(ISNUMBER({HI_}$C$5:$L$26)))&" celda(s)): escribe solo números o deja la celda vacía","")'),
 ('V38', 'Valor de la fuente externa (Análisis C38)', '3', 'TRUE',
  f'=IF(AND({AN_}$C$38<>"",NOT(ISNUMBER({AN_}$C$38))),"AVI|Valor intrínseco de la fuente externa (Análisis C38) no numérico: se ignora","")'),
 ('V39', 'Celdas de salida intactas (sin sobrescribir)', '1', 'TRUE',
  f'=IF(AND(_xlfn.ISFORMULA({AN_}$C$52),_xlfn.ISFORMULA({AN_}$B$78),_xlfn.ISFORMULA({AN_}$C$78),_xlfn.ISFORMULA({AN_}$D$78),_xlfn.ISFORMULA({AN_}$C$83),_xlfn.ISFORMULA({AN_}$C$84),_xlfn.ISFORMULA({AN_}$C$86),_xlfn.ISFORMULA({AN_}$C$85),_xlfn.ISFORMULA({AN_}$B$67),'
  f'_xlfn.ISFORMULA({HI_}$C$44),_xlfn.ISFORMULA({HI_}$C$48),_xlfn.ISFORMULA({HI_}$C$52),_xlfn.ISFORMULA({HI_}$C$58),_xlfn.ISFORMULA({HI_}$C$70),_xlfn.ISFORMULA({DG}!$C$5),_xlfn.ISFORMULA({DG}!$C$12),_xlfn.ISFORMULA({DG}!$C$32),_xlfn.ISFORMULA({PA}!$K$20),_xlfn.ISFORMULA({PA}!$K$25)),"",'
  f'"INV|Alguna celda de salida (Análisis C52, B67, B78:D78, C83:C86; Historia C44, C48, C52, C58, C70; Diagnóstico C5, C12, C32; Panel K20, K25) ha sido sobrescrita con un valor: restaura la fórmula")'),
 ('V35', 'Motor calculable (red de seguridad)', '1', 'TRUE',
  f'=IF(AND(COUNT($BK$6:$BK$8)<3,COUNTIF($D${RUL0}:$D${{RUL_V35 - 1}},"DATOS INVÁLIDOS")+COUNTIF($D${RUL0}:$D${{RUL_V35 - 1}},"MODELO NO APLICABLE")+COUNTIFS($G${RUL0}:$G${{RUL_V35 - 1}},1,$D${RUL0}:$D${{RUL_V35 - 1}},"INCOMPLETO")=0),'
  f'"INC|El motor no puede calcular: "&IF($BT$7<>"",$BT$7,IF($BT$6<>"",$BT$6,IF($BT$8<>"",$BT$8,"revisa Historia y Palancas"))),"")'),
 ('C01', 'Identificación (Análisis B3, D3)', f'=IF({AN_}$B$3="",1,3)', 'TRUE',
  f'=IF({AN_}$B$3="","INC|Falta el nombre de la empresa (Análisis B3)",IF({AN_}$D$3="","INC|Falta el ticker (Análisis D3)",""))'),
 ('C02', 'Filtro Pabrai (Análisis C11:C13)', '3', 'TRUE',
  f'=IF(SUMPRODUCT(--EXACT({AN_}$C$11:$C$13,"Sí"))+SUMPRODUCT(--EXACT({AN_}$C$11:$C$13,"No"))<COUNTA({AN_}$C$11:$C$13),"INV|Respuesta fuera de dominio en el filtro Pabrai (Análisis C11:C13): solo Sí o No (exacto)",IF(COUNTA({AN_}$C$11:$C$13)<3,"INC|Filtro Pabrai sin completar (Análisis C11:C13)",""))'),
 ('C03', 'Tipo de empresa (Palancas C5, C6)', '3', 'TRUE',
  f'=IF(OR({PL_}${C_ETAPA}="",{PL_}${C_CASO}=""),"INC|Falta la etapa o el caso especial (Palancas C5, C6)","")'),
 ('C04', 'Sector de Damodaran (Palancas C7)', '3', 'TRUE',
  f'=IF({PL_}${C_SECTOR}="","INC|Falta el sector de Damodaran (Palancas C7)","")'),
 ('C05', 'Tesis y tesis inversa (Análisis B101, B102)', '3', 'TRUE',
  f'=IF(OR({AN_}$B$101="",{AN_}$B$102=""),"INC|Faltan la tesis o la tesis inversa (Análisis B101, B102)","")'),
 ('C06', 'Gestión (Análisis C97, C98)', '3', 'TRUE',
  f'=IF(OR({AN_}$C$97="",{AN_}$C$98=""),"INC|Faltan insiders o asignación de capital (Análisis C97, C98)","")'),
 ('C07', 'Predicciones (Palancas A38:A40)', '3', 'TRUE',
  f'=IF(COUNTA({PL_}$A${PRED0}:$A${PRED0 + 2})<3,"INC|Faltan "&(3-COUNTA({PL_}$A${PRED0}:$A${PRED0 + 2}))&" predicciones (Palancas A38:A40)","")'),
 ('C08', 'Etapas 1 y 2 de Análisis (13 respuestas)', '3', 'TRUE',
  f'=IF(COUNTA({AN_}$C$17:$C$20,{AN_}$C$24:$C$28,{AN_}$C$31:$C$34)<13,"INC|Faltan "&(13-COUNTA({AN_}$C$17:$C$20,{AN_}$C$24:$C$28,{AN_}$C$31:$C$34))&" respuestas de las etapas 1 y 2","")'),
 ('C09', 'Escenarios en tus palabras (Análisis B66:D66)', '3', 'TRUE',
  f'=IF(OR({AN_}$B$66="",{AN_}$C$66="",{AN_}$D$66=""),"INC|Falta «en tus palabras» en algún escenario (Análisis B66:D66)","")'),
 ('C10', 'Cierre (Análisis C14, C93, C103, C104)', '3', 'TRUE',
  f'=IF(OR({AN_}$C$14="",{AN_}$C$93="",{AN_}$C$103="",{AN_}$C$104=""),"INC|Faltan respuestas de cierre (Análisis C14, C93, C103 o C104)","")'),
 ('V29', 'DCF inverso utilizable', '3', 'TRUE',
  f'=IF(OR(NOT(COUNTIF($D${RUL0}:$D${{RUL_PREV}},"DATOS INVÁLIDOS")+COUNTIF($D${RUL0}:$D${{RUL_PREV}},"MODELO NO APLICABLE")+COUNTIFS($G${RUL0}:$G${{RUL_PREV}},1,$D${RUL0}:$D${{RUL_PREV}},"INCOMPLETO")=0),$B$193="",$B$193="—",$B$193="✓ PASA"),"","AVI|DCF inverso: "&MID($B$193,FIND("·",$B$193)+2,999))'),
 ('V36', 'Valor por acción positivo en los tres escenarios', '3', 'TRUE',
  f'=IF(OR(NOT(COUNTIF($D${RUL0}:$D${{RUL_PREV}},"DATOS INVÁLIDOS")+COUNTIF($D${RUL0}:$D${{RUL_PREV}},"MODELO NO APLICABLE")+COUNTIFS($G${RUL0}:$G${{RUL_PREV}},1,$D${RUL0}:$D${{RUL_PREV}},"INCOMPLETO")=0),COUNT($BK$6:$BK$8)<3),"",IF(MIN($BK$6:$BK$8)<=0,"AVI|Algún escenario da un valor por acción ≤ 0 ("&FIXED(MIN($BK$6:$BK$8),2)&"): revisa palancas, deuda y unidades; no hay margen de seguridad posible",""))'),
]
RUL_V35 = RUL0 + [r[0] for r in RULES].index('V35')
RULES = [(rid, nm, tier, ap, f_.replace('{RUL_V35 - 1}', str(RUL_V35 - 1)).replace('{RUL_PREV}', str(RUL0 + i - 1))) for i, (rid, nm, tier, ap, f_) in enumerate(RULES)]
M['A199'] = 'ESTADO DEL MODELO · reglas de validación (no tocar)'
M['A199'].font = Font(name=F, size=10, bold=True)
for j, h in enumerate(['Id', 'Regla', 'Aplica', 'Resultado', 'Código', 'Causa', 'Nivel', 'Prioridad', 'Nº causa activa']):
    M.cell(200, 1 + j, h).font = Font(name=F, size=9, bold=True)
for i, (rid, nm, tier, aplica, causa) in enumerate(RULES):
    r = RUL0 + i
    M[f'A{r}'] = rid
    M[f'B{r}'] = nm
    M[f'C{r}'] = f'={aplica}'
    M[f'E{r}'] = f'=IF(C{r},{causa[1:]},"")'
    M[f'D{r}'] = (f'=IF(NOT(C{r}),"N/A",IF(E{r}="","OK",IF(LEFT(E{r},3)="INC","INCOMPLETO",IF(LEFT(E{r},3)="INV",'
                  f'"DATOS INVÁLIDOS",IF(LEFT(E{r},3)="NOA","MODELO NO APLICABLE",IF(LEFT(E{r},3)="NEV","N/A","AVISO"))))))')
    M[f'F{r}'] = f'=IF(E{r}="","",MID(E{r},5,999))'
    M[f'G{r}'] = tier if str(tier).startswith('=') else int(tier)
    M[f'H{r}'] = (f'=IF(D{r}="DATOS INVÁLIDOS",1,IF(D{r}="MODELO NO APLICABLE",2,IF(AND(D{r}="INCOMPLETO",G{r}=1),3,9)))')
    M[f'I{r}'] = f'=IF(OR(D{r}="OK",D{r}="N/A"),"",COUNTIFS($D${RUL0}:D{r},"<>OK",$D${RUL0}:D{r},"<>N/A"))'
RUL1 = RUL0 + len(RULES) - 1
RD, RG, RF, RH, RI, RC = (f'$D${RUL0}:$D${RUL1}', f'$G${RUL0}:$G${RUL1}', f'$F${RUL0}:$F${RUL1}',
                           f'$H${RUL0}:$H${RUL1}', f'$I${RUL0}:$I${RUL1}', f'$C${RUL0}:$C${RUL1}')
AGG0 = RUL1 + 3
AGG = [
 ('BLOQUEO DEL VALOR', f'=(COUNTIF({RD},"DATOS INVÁLIDOS")+COUNTIF({RD},"MODELO NO APLICABLE")+COUNTIFS({RG},1,{RD},"INCOMPLETO"))>0'),
 ('COMPARABLE precio ↔ valor', f'=AND({MON_OK},NOT({ADR_NV}))'),
 ('BLOQUEO DE LA LECTURA DE PRECIO', f'=OR(B{AGG0},NOT(B{AGG0 + 1}),(COUNTIFS({RG},2,{RD},"DATOS INVÁLIDOS")+COUNTIFS({RG},2,{RD},"INCOMPLETO"))>0)'),
 ('ESTADO TÉCNICO', f'=IF(COUNTIF({RD},"DATOS INVÁLIDOS")>0,"DATOS INVÁLIDOS",IF(COUNTIF({RD},"MODELO NO APLICABLE")>0,"MODELO NO APLICABLE",IF(COUNTIF({RD},"INCOMPLETO")>0,"INCOMPLETO","COMPLETO Y VÁLIDO")))'),
 ('CAUSA TÉCNICA PRINCIPAL', f'=IF(B{AGG0 + 3}="COMPLETO Y VÁLIDO","",IF(MIN({RH})<9,INDEX({RF},MATCH(MIN({RH}),{RH},0)),INDEX({RF},MATCH(B{AGG0 + 3},{RD},0))))'),
 ('CAUSA DEL BLOQUEO DEL VALOR', f'=IF(NOT(B{AGG0}),"",INDEX({RF},MATCH(MIN({RH}),{RH},0)))'),
 ('ESTADO DE INVERSIÓN', f'=IF(SUMPRODUCT(--EXACT({AN_}$C$11:$C$13,"No"))>0,"DESCARTADA POR FILTRO PABRAI",IF(SUMPRODUCT(--EXACT({AN_}$C$11:$C$13,"Sí"))=3,"DENTRO DEL CÍRCULO","PENDIENTE DE FILTRO"))'),
 ('MOTIVO PABRAI', f'=IF(EXACT({AN_}$C$11,"No"),"no entiendo el negocio (C11)",IF(EXACT({AN_}$C$12,"No"),"fuera del círculo de competencia (C12)",IF(EXACT({AN_}$C$13,"No"),"el valor no es claro sin modelos (C13)","")))'),
 ('Nº AVISOS', f'=COUNTIF({RD},"AVISO")'),
 ('Nº CAUSAS ACTIVAS', f'=COUNTIFS({RD},"<>OK",{RD},"<>N/A")'),
 ('COMPLETITUD · reglas aplicables', f'=COUNTIF({RC},TRUE)'),
 ('COMPLETITUD · reglas con dato', f'=COUNTIF({RC},TRUE)-COUNTIFS({RC},TRUE,{RD},"INCOMPLETO")-COUNTIFS({RC},TRUE,{RD},"N/A")'),
 ('CORRECCIÓN · reglas evaluables', f'=COUNTIFS({RC},TRUE,{RD},"<>INCOMPLETO",{RD},"<>N/A")'),
 ('CORRECCIÓN · reglas correctas', f'=COUNTIFS({RC},TRUE,{RD},"OK")+COUNTIFS({RC},TRUE,{RD},"AVISO")'),
 ('ESTADO DEL LIBRO', f'=IF(COUNTIF({RD},"DATOS INVÁLIDOS")>0,"NO LISTO · datos inválidos",IF(COUNTIF({RD},"MODELO NO APLICABLE")>0,"NO LISTO · modelo no aplicable",IF(COUNTIF({RD},"INCOMPLETO")>0,"NO LISTO · incompleto ("&COUNTIF({RD},"INCOMPLETO")&" pendientes)",IF(NOT(ISNUMBER({AN_}$C$83)),"NO LISTO · sin valor ponderado",IF(NOT(B{AGG0 + 1}),"NO LISTO · precio no comparable (moneda o unidad)","LISTO")))))'),
 ('LECTURA DE PRECIO', f'=IF(B{AGG0},"",IF(NOT(B{AGG0 + 1}),"precio no comparable (moneda o unidad)",IF(B{AGG0 + 2},"sin lectura de precio",IF(ISNUMBER(SEARCH("BANDERA",{AN_}$D$84)),"sin margen: tu DCF no da colchón",IF(ISNUMBER(SEARCH("BANDERA",{AN_}$D$85)),"asimetría débil: revisa escenarios",IF(ISNUMBER(SEARCH("BANDERA",{AN_}$D$86)),"precio exigente: el mercado descuenta demasiado",IF(ISNUMBER(SEARCH("BANDERA",{AN_}$D$93)),"terminal no sostenible: revisa g",IF(ISNUMBER({AN_}$C$84),"margen de seguridad "&FIXED(100*{AN_}$C$84,0)&" %",IF({AN_}$C$83="","sin valor ponderado",IF(NOT(B{AGG0 + 1}),"precio no comparable",""))))))))))'),
 ('VEREDICTO PRINCIPAL', f'=IF(B{AGG0 + 3}="DATOS INVÁLIDOS","DATOS INVÁLIDOS · "&B{AGG0 + 4},IF(B{AGG0 + 3}="MODELO NO APLICABLE","MODELO NO APLICABLE · "&B{AGG0 + 4},'
                         f'IF(B{AGG0 + 6}="DESCARTADA POR FILTRO PABRAI","DESCARTADA POR FILTRO PABRAI · "&B{AGG0 + 7},IF(B{AGG0 + 3}="INCOMPLETO","INCOMPLETA · faltan "&COUNTIF({RD},"INCOMPLETO")&" · "&B{AGG0 + 4},'
                         f'IF({AN_}$C$83="","INCOMPLETA · sin valor ponderado (revisa el motor y las probabilidades)",IF({AN_}$C$7>0,"CANDIDATA VÁLIDA · resuelve "&{AN_}$C$7&" bandera(s)"&IF(B{AGG0 + 15}<>""," · "&B{AGG0 + 15},""),'
                         f'IF({AN_}$D$7>=4,"CANDIDATA VÁLIDA · demasiadas dudas ("&{AN_}$D$7&")"&IF(B{AGG0 + 15}<>""," · "&B{AGG0 + 15},""),"CANDIDATA VÁLIDA"&IF(B{AGG0 + 15}<>""," · "&B{AGG0 + 15},""))))))))'),
]
for i, (nm, f_) in enumerate(AGG):
    M[f'A{AGG0 + i}'] = nm
    M[f'B{AGG0 + i}'] = f_
    M[f'A{AGG0 + i}'].font = Font(name=F, size=9, bold=True)
assert AGG0 == AGG0_PLACEHOLDER, f'AGG0={AGG0}: actualiza AGG0_PLACEHOLDER'
ST_BLOQ, ST_COMP, ST_BLOQP, ST_TEC, ST_CAUSA, ST_CAUSAV, ST_INV, ST_PAB, ST_NAV, ST_NC, ST_CA, ST_CD, ST_RE, ST_RC, ST_LIBRO, ST_PRECIO, ST_VER = \
    [f'{MO}!$B${AGG0 + i}' for i in range(len(AGG))]
GATE = f'{ST_BLOQ}'                     # TRUE = valor bloqueado
GATEP = f'{ST_BLOQP}'                   # TRUE = lectura de precio bloqueada
# causas activas en orden (para Diagnóstico y Panel)
CA0 = AGG0 + len(AGG) + 2
M[f'A{CA0 - 1}'] = 'CAUSAS ACTIVAS (en orden)'
for k in range(1, 13):
    r = CA0 + k - 1
    M[f'A{r}'] = f'=IFERROR(INDEX({RD},MATCH({k},{RI},0)),"")'
    M[f'B{r}'] = f'=IFERROR(INDEX({RF},MATCH({k},{RI},0)),"")'

M.sheet_state = 'hidden'

# ================================================================== Diagnóstico V6 · bloques 7–9 (necesitan el Motor)
RMAP = {69: 'V02', 70: 'V03', 71: 'V05', 72: 'V17', 73: 'V15', 74: 'V14', 75: 'V16', 76: 'V30', 81: 'C07', 82: 'C03'}
RIDX = {rid: RUL0 + i for i, (rid, *_rest) in enumerate(RULES)}
for r_, rid in RMAP.items():
    mr = RIDX[rid]
    D[f'B{r_}'] = (f'=IF({MO}!$D${mr}="N/A","No aplica (motor "&{DG}!${D_MOTOR}&")",IF({MO}!$D${mr}="OK","✓ PASA",'
                   f'IF({MO}!$D${mr}="AVISO","⚠ REVISAR · "&{MO}!$F${mr},"⛔ TÉCNICO · "&{MO}!$F${mr})))')
D[f'B{RVER}'] = f'={ST_LIBRO}'
D[f'A{RVER}'] = 'ESTADO DEL LIBRO (completo y correcto = LISTO)'
D.conditional_formatting.add(f'B{RVER}:D{RVER}', FormulaRule(formula=[f'LEFT(B{RVER},5)="LISTO"'], fill=fill(GOOD_BG),
                                                              font=Font(color=GOOD_FG, bold=True)))
D.conditional_formatting.add(f'B{RVER}:D{RVER}', FormulaRule(formula=[f'LEFT(B{RVER},8)="NO LISTO"'], fill=fill(WARN_BG),
                                                              font=Font(color=WARN_FG, bold=True)))
# bloque 7 · parámetros
band(D, 89, '  7 · PARÁMETROS DE LA CONCILIACIÓN (ajustables)')
header(D, 90, ['Parámetro', 'Valor', '', '', 'Qué hace'])
D.merge_cells('E90:J90')
for r_, nm, v, fmt, nt in ((91, 'Tolerancia de la capitalización: pasa en silencio', 0.05, PCT, 'Desviación = |cap ÷ (precio × acciones) − 1|.'),
                           (92, 'Corte de la capitalización: bloquea sin causa declarada', 0.25, PCT, 'Entre la tolerancia y el corte, avisa y pide la causa en Palancas C47.'),
                           (93, 'Separación máxima entre la fecha del precio y la de las acciones (días)', 90, '0', 'Más allá, avisa.'),
                           (94, 'Vigencia máxima de las tablas de sector y país (meses)', 18, '0', 'Se compara la fecha de análisis (Análisis D4) con Sector B3 y Riesgo país B2. Más allá, avisa.')):
    label(D, f'A{r_}', nm)
    inp(D, f'C{r_}', v, fmt)
    note(D, f'E{r_}', nt)
    D.merge_cells(f'E{r_}:J{r_}')
# bloque 8 · inventario de reglas
band(D, 95, '  8 · ESTADO DEL MODELO · inventario de reglas por motor')
header(D, 96, ['Regla', 'Aplica', 'Resultado', 'Nivel', 'Causa'])
D.merge_cells('E96:J96')
INV0 = 97
for i, (rid, nm, tier, aplica, causa) in enumerate(RULES):
    r_ = INV0 + i
    mr = RUL0 + i
    out(D, f'A{r_}', f'="{rid} · {nm}"')
    out(D, f'B{r_}', f'=IF({MO}!$C${mr},"Sí","No")')
    out(D, f'C{r_}', f'={MO}!$D${mr}', bold=True)
    out(D, f'D{r_}', f'=CHOOSE({MO}!$G${mr},"1 · bloquea el valor","2 · bloquea la lectura de precio","3 · completitud del libro")', size=9)
    out(D, f'E{r_}', f'={MO}!$F${mr}', size=9, wrap=True)
    D.merge_cells(f'E{r_}:J{r_}')
INV1 = INV0 + len(RULES) - 1
for word, bg, fg in (('DATOS INVÁLIDOS', BAD_BG, BAD_FG), ('MODELO NO APLICABLE', WARN_BG, WARN_FG),
                     ('INCOMPLETO', 'EDEDED', 'FF404040'), ('AVISO', WARN_BG, WARN_FG), ('OK', GOOD_BG, GOOD_FG)):
    D.conditional_formatting.add(f'C{INV0}:C{INV1}', FormulaRule(formula=[f'C{INV0}="{word}"'], fill=fill(bg),
                                                                 font=Font(color=fg, bold=(word != 'OK')), stopIfTrue=True))
# bloque 9 · veredictos
VB0 = INV1 + 2
band(D, VB0, '  9 · DOS DIAGNÓSTICOS Y UN VEREDICTO')
VB = [('Diagnóstico técnico', ST_TEC, 'DATOS INVÁLIDOS · MODELO NO APLICABLE · INCOMPLETO · COMPLETO Y VÁLIDO'),
      ('Causa técnica principal', ST_CAUSA, ''),
      ('Diagnóstico de inversión', ST_INV, 'PENDIENTE DE FILTRO · DESCARTADA POR FILTRO PABRAI · DENTRO DEL CÍRCULO'),
      ('Motivo del filtro Pabrai', ST_PAB, 'Se conserva el registro para reconsiderarla.'),
      ('Completitud', f'={ST_CD}&" de "&{ST_CA}&" comprobaciones de completitud con dato"', 'Una comprobación en «—» no cuenta como aprobada.'),
      ('Corrección', f'={ST_RC}&" de "&{ST_RE}&" comprobaciones evaluables correctas (los avisos cuentan como correctas)"', ''),
      ('Precio comparable con el valor', f'=IF({ST_COMP},"Sí","No · "&IF(NOT({MON_OK}),"moneda sin declarar o distinta","unidad cotizada (ADR) no verificada"))', 'Sin comparabilidad no hay margen de seguridad.'),
      ('Lectura de precio', ST_PRECIO, 'Separada de la validez técnica: un modelo válido puede tener un precio caro.'),
      ('Precio de Sí (definición del kit)', f'=IF(OR({GATEP},NOT(ISNUMBER(Análisis!$B$78)),NOT(ISNUMBER(Análisis!$C$83))),"",MIN(Análisis!$B$78,0.75*Análisis!$C$83))', 'mín(valor del escenario MALO, 75 % del ponderado). El cubo (Sí · Vigilar · No · Demasiado difícil) lo decide el personaje del kit con esta cifra, el precio y el veredicto; la hoja no lo asigna.'),
      ('ESTADO DEL LIBRO', ST_LIBRO, 'LISTO solo si está completo y es correcto.'),
      ('VEREDICTO PRINCIPAL (Análisis A6)', ST_VER, 'Prioridad: datos inválidos › modelo no aplicable › filtro Pabrai › incompleta › candidata válida.')]
for i, (nm, f_, nt) in enumerate(VB):
    r_ = VB0 + 1 + i
    label(D, f'A{r_}', nm, bold=(nm.isupper()))
    out(D, f'C{r_}', f_ if f_.startswith('=') else f'={f_}', bold=True, wrap=True)
    D.merge_cells(f'C{r_}:E{r_}')
    note(D, f'F{r_}', nt)
    D.merge_cells(f'F{r_}:J{r_}')
    D.row_dimensions[r_].height = 28
verdict_cf(D, f'C{VB0 + 1}:E{VB0 + 11}')
D[f'C{VB0 + 9}'].number_format = NUM2
CA_ROW = VB0 + 13
label(D, f'A{CA_ROW}', 'Causas activas, en orden (todas, aunque el veredicto solo muestre la prioritaria)', bold=True)
for k in range(12):
    r_ = CA_ROW + 1 + k
    out(D, f'A{r_}', f'=IF({MO}!$B${CA0 + k}="","",{k + 1}&". "&{MO}!$A${CA0 + k}&" · "&{MO}!$B${CA0 + k})', size=9, wrap=True)
    D.merge_cells(f'A{r_}:J{r_}')
D.conditional_formatting.add(f'A{CA_ROW + 1}:J{CA_ROW + 12}', FormulaRule(formula=[f'ISNUMBER(SEARCH("DATOS INVÁLIDOS",$A{CA_ROW + 1}))'], font=Font(color=BAD_FG, bold=True)))
D.conditional_formatting.add(f'A{CA_ROW + 1}:J{CA_ROW + 12}', FormulaRule(formula=[f'ISNUMBER(SEARCH("NO APLICABLE",$A{CA_ROW + 1}))'], font=Font(color=WARN_FG, bold=True)))

# ================================================================== Análisis: recableado
AN['A1'] = ('  HOJA DE EVALUACIÓN DE EMPRESAS — V6.1 · Checklist + calidad financiera + valoración por palancas '
            '(Damodaran) con criterio Munger')
AN['A7'] = '(tu checklist + TU DCF; una valoración externa es solo contraste, nunca referencia)'
AN['A35'] = '  ETAPA 3 · VALORACIÓN (tu DCF manda; una fuente externa es solo contraste)'
AN['A38'] = 'Valor intrínseco de una fuente externa (opcional)'
AN['B38'] = 'Cualquier valoración ajena que quieras contrastar. Úsala para contrastar, no para decidir. Vacío si no tienes.'
AN['E38'] = 'Opcional. Si la rellenas, di la fuente en Control maestro.'
AN['A39'] = '→ Margen de seguridad frente a la fuente externa (referencia)'
AN['D39'] = ('=IF(C39="","—",IF(C39>=0.3,"✓ DESCUENTO · fuente externa",IF(C39>=0.1,"ℹ fuente externa · descuento justo",'
             '"⚠ fuente externa · sin descuento")))')
AN['E39'] = 'Solo si rellenaste C38.'
AN['A87'] = 'Tu valor frente al de la fuente externa'
AN['B87'] = '¿Tu número ponderado y el externo se parecen?'
AN['E43'] = ('=IF(C83="","Valor ponderado de tus 3 escenarios · se rellena al completar el desglose","Valor ponderado · margen "'
             '&TEXT(C84,"0%")&IF(C87="",""," · vs fuente externa "&TEXT(C87,"+0%;-0%")))')
for ref, txt in (('E19', 'Historia, filas 6 y 9.'), ('E25', 'Historia, fila 35 (FCF al accionista).'),
                 ('E27', 'Historia, fila 29 (margen EBIT).'), ('E28', 'Historia, fila 20 (acciones diluidas).'),
                 ('E31', "'No' es lo bueno. Balance y Historia, fila 14."), ('E34', 'Balance: caja frente a deuda a corto.'),
                 ('E46', 'Estado de flujos de caja.'), ('E96', 'Mete el % (ej. 5%). Informe anual o registro del regulador.'),
                 ('E97', 'Registro del regulador o informe anual (transacciones de directivos).')):
    AN[ref] = txt
AN['E84'] = 'Este es el margen principal: sale de TU DCF ponderado, no de ninguna fuente externa.'
CM['C39'] = 'Valor intrínseco de una fuente externa (opcional)'
for col in 'BCD':
    AN[f'{col}67'] = f'=IF({DG}!{col}{R_GFCF}="","",{DG}!{col}{R_GFCF})'
    AN[f'{col}67'].font = Font(name=F, size=10)
    AN[f'{col}67'].fill = PatternFill(fill_type=None)
AN['A67'] = 'Crecimiento de la caja libre · años 1–10 (V6: lo calculan las palancas)'
AN['E67'] = ('V6: ya no se escribe. Sale de las palancas de la hoja «Palancas» (ventas, margen, reinversión). '
             'Es el crecimiento anual del FCF entre el año 1 y el 10.')
for dv in list(AN.data_validations.dataValidation):
    if str(dv.sqref) in ('B67', 'C67', 'D67', 'C62'):
        AN.data_validations.dataValidation.remove(dv)
dv_list(AN, 'C62', 'Lista_C62')
row_of = {'B': 6, 'C': 7, 'D': 8}
for col in 'BCD':
    n_ = row_of[col]
    AN[f'{col}71'] = f'=IF(OR({col}65="",{GATE}),"",IF({MO}!BD{n_}="","",{MO}!BD{n_}))'
    AN[f'{col}72'] = f'=IF(OR({col}65="",{GATE}),"",IF({MO}!BE{n_}="","",{MO}!BE{n_}))'
    AN[f'{col}73'] = f'=IF(OR({col}65="",{GATE}),"",IF({MO}!BH{n_}="","",{MO}!BH{n_}))'
    AN[f'{col}75'] = f'=IF(OR({col}65="",{GATE},{MO}!BG{n_}="",N({MO}!BD{n_})<=0),"",{MO}!BG{n_}/{MO}!BD{n_})'
    if col != 'C':
        AN[f'{col}76'] = f'=IF(OR({col}65="",{GATE}),"",{MO}!M{n_})'
    AN[f'{col}77'] = f'=IF(OR(NOT(ISNUMBER({col}72)),NOT(ISNUMBER({col}73))),"",{col}72+{col}73+N({MO}!M{n_}))'
    AN[f'{col}78'] = (f'=IF({col}65="","Falta: ¿qué tiene que pasar?",IF({GATE},{ST_CAUSAV},IF({MO}!BK{n_}="",'
                      f'IF({MO}!BT{n_}="","",{MO}!BT{n_}),{MO}!BK{n_})))')
    AN[f'{col}79'] = f'=IF({GATEP},"",IF(OR(NOT(ISNUMBER({col}78)),$C$37=""),"",IF({col}78<=0,"",({col}78-$C$37)/{col}78)))'
    AN[f'{col}80'] = f'=IF({GATEP},"",IF(OR(NOT(ISNUMBER({col}78)),$C$37="",$C$37=0),"",{col}78/$C$37-1))'
AN['A76'] = (f'=IF({DG}!${D_MOTOR}="B","Ajuste del motor B: − pasivos netos (mm) · C76 no se usa",'
             f'IF({DG}!${D_MOTOR}="C","Motor C: no se suma caja (C76 no se usa)",'
             '"Exceso de caja NO operativa que sumas (mm) · opcional"))')
AN['A75'] = "Tu 'para siempre' = vender en el año 10 a… (veces su FCF)"
AN['A78'] = 'VALOR INTRÍNSECO POR ACCIÓN (con probabilidad de quiebra si la hay)'
AN['D52'] = (f'=IF(C52="","—",IF(C52>0,"✓ PASA",IF({DG}!${D_MOTOR}="A","ℹ FCF base ≤ 0 · declara su naturaleza en Palancas C43 '
             '(no es un error ni un descarte)","ℹ FCF base ≤ 0 · este motor no lo usa para calibrar")))')
AN['C84'] = f'=IF({GATEP},"",IF(OR(C83="",$C$37=""),"",IF(C83<=0,"",(C83-$C$37)/C83)))'
AN['C85'] = f'=IF({GATEP},"",IF(OR(NOT(ISNUMBER(B80)),NOT(ISNUMBER(D80))),"",TEXT(B80,"+0%;-0%;0%")&" / "&TEXT(D80,"+0%;-0%;0%")))'
AN['A6'] = f'={ST_VER}'
AN['A6'].alignment = Alignment(horizontal='left', vertical='center', indent=1, wrap_text=True)
AN.row_dimensions[6].height = 32
AN['E6'] = f'=IF({ST_NC}=0,"Sin causas activas","Causas activas: "&{ST_NC}&" · estado técnico: "&{ST_TEC}&" · inversión: "&{ST_INV})'
AN['E6'].font = Font(name=F, size=9)
AN['E6'].alignment = Alignment(wrap_text=True, vertical='center')
# formato condicional de A6: se sustituyen las reglas antiguas por las de los cuatro estados
_cf_new = openpyxl.formatting.formatting.ConditionalFormattingList()
for _cf in AN.conditional_formatting:
    if 'A6' not in str(_cf.sqref):
        for _r in _cf.rules:
            _cf_new.add(str(_cf.sqref), _r)
AN.conditional_formatting = _cf_new
for word, bg, fg in (('DATOS INVÁLIDOS', BAD_BG, BAD_FG), ('MODELO NO APLICABLE', WARN_BG, WARN_FG),
                     ('DESCARTADA POR FILTRO PABRAI', 'D9E1F2', 'FF1F3A4D'), ('INCOMPLETA', 'EDEDED', 'FF404040'),
                     ('CANDIDATA VÁLIDA', GOOD_BG, GOOD_FG)):
    AN.conditional_formatting.add('A6:B6', FormulaRule(formula=[f'ISNUMBER(SEARCH("{word}",$A$6))'], fill=fill(bg),
                                                       font=Font(name=F, size=13, bold=True, color=fg), stopIfTrue=True))
AN['B53'] = 'Dato de balance. Los motores A y C no la suman: usa C76 para el exceso claramente no operativo.'
AN['B54'] = 'Dato de balance. El motor A no la resta; el motor B sí resta la deuda neta (ver Diagnóstico V6).'
AN['D62'] = ('=IF(C62="","—",IF(C62="Sí","✓ PASA · motor A (accionista)",IF(C62="No · financiación cambia mucho",'
             '"ℹ Motor B · operativo con deuda",IF(OR(C62="No · banco o aseguradora",C62="No · banco, aseguradora o regulada"),'
             '"ℹ Motor C · ROE (patrimonio)","✗ BANDERA · usa otro método"))))')
AN['E62'] = ('V6: «Sí» = motor A. «Financiación cambia mucho» = motor B (flujo operativo, r mezclada, se resta la '
             'deuda). «Banco o aseguradora» = motor C (patrimonio y ROE); una regulada puede ir con A o B (aviso). «Otro método» = sin valoración.')
KEY_OLD = 'COUNTA(B67:D69)'
KEY_NEW = (f'COUNTA(B68:D69)+COUNTA({PAL}!B{R_CREC}:D{R_MARG})+IF({DG}!${D_MOTOR}="C",3,COUNTA({PAL}!B{R_S2C}:D{R_S2C}))'
           f'+COUNTA({PAL}!B{R_ROIC}:D{R_ROIC})+COUNTA({PAL}!{C_ETAPA}:{C_CASO})')
v = AN['E7'].value
assert KEY_OLD in v
AN['E7'] = v.replace(KEY_OLD, KEY_NEW).replace('(41-', '(52-').replace('/41', '/52')
_dgB, _dgC, _dgD = (f'{DG}!B{DIAG0}:B{DIAG0 + DIAGN - 1}', f'{DG}!C{DIAG0}:C{DIAG0 + DIAGN - 1}', f'{DG}!D{DIAG0}:D{DIAG0 + DIAGN - 1}')
_band_row = f'((ISNUMBER(SEARCH("BANDERA",{_dgB}))+ISNUMBER(SEARCH("BANDERA",{_dgC}))+ISNUMBER(SEARCH("BANDERA",{_dgD})))>0)'
_rev_row = f'((ISNUMBER(SEARCH("REVISAR",{_dgB}))+ISNUMBER(SEARCH("REVISAR",{_dgC}))+ISNUMBER(SEARCH("REVISAR",{_dgD})))>0)'
AN['C7'] = (AN['C7'].value + f'+SUMPRODUCT(--{_band_row})'
            f'+SUMPRODUCT(--ISNUMBER(SEARCH("BANDERA",{DG}!D{PG0 + 4})))'
            f'+SUMPRODUCT(--ISNUMBER(SEARCH("BANDERA",{DG}!B{AC0}:B{AC0 + ACN - 1})))')
AN['D7'] = (AN['D7'].value + f'+SUMPRODUCT(--{_rev_row},--NOT({_band_row}))'
            f'+SUMPRODUCT(--ISNUMBER(SEARCH("REVISAR",{DG}!D{PG0 + 4})))'
            f'+SUMPRODUCT(--ISNUMBER(SEARCH("REVISAR",{DG}!B{AC0}:B{AC0 + ACN - 1})))')
GUARD = f'$B$65="",$C$65="",$D$65="",ROUND(ABS(SUM($B$69:$D$69)-1),9)>0.001,{GATE}'
for ri, dr in ((90, -0.02), (91, 0.0), (92, 0.02)):
    for ci, dg in (('B', -0.005), ('C', 0.0), ('D', 0.005)):
        a_, b_, c_ = SENS[('B', dr, dg)], SENS[('C', dr, dg)], SENS[('D', dr, dg)]
        AN[f'{ci}{ri}'] = (f'=IF(OR({GUARD},COUNT({MO}!BK{a_},{MO}!BK{b_},{MO}!BK{c_})<3),"",'
                           f'($B$69*{MO}!BK{a_}+$C$69*{MO}!BK{b_}+$D$69*{MO}!BK{c_})/SUM($B$69:$D$69))')
for ri, d_ in ((90, '-2 pts'), (91, 'base'), (92, '+2 pts')):
    AN[f'A{ri}'] = (f'=IF({DG}!${D_MOTOR}="B","r operativa "&"{d_}"&" ("&FIXED(100*(N({DG}!${D_ROP})'
                    f'{"+0.02" if ri == 92 else ("-0.02" if ri == 90 else "")}),1)&" %)",'
                    f'"Tu r {d_} ("&FIXED(100*(N(Análisis!$C$56)'
                    f'{"+0.02" if ri == 92 else ("-0.02" if ri == 90 else "")}),1)&" %)")')
AN['A106'] = '▸ Tabla auxiliar del DCF inverso (no tocar) · V6: crecimiento del año 1–5 con el resto del NORMAL'
AN['A107'] = 'Crecimiento años 1–5'
for i in range(81):
    AN[f'B{108 + i}'] = f'=IF(OR({GATE},{MO}!BK{REV0 + i}=""),"",{MO}!BK{REV0 + i})'
AN['A86'] = 'Crecimiento que el precio ya da por hecho'
AN['B86'] = ('DCF inverso V6: crecimiento de los años 1–5 (ventas, o patrimonio en el motor C) que haría que tu valor '
             'NORMAL igualara el precio, con tu margen, reinversión y ROIC del NORMAL.')
AN['D86'] = (f'=IF(AND({MO}!$B$193<>"—",{MO}!$B$193<>"✓ PASA"),{MO}!$B$193,IF(C86="","—",'
             'IF(C86="< -10%","✓ PASA · precio descuenta caída",IF(C86="> 30%","✗ BANDERA · exige >30%",'
             f'IF(NOT(ISNUMBER(C86)),"—",IF(C86<={PAL}!C{R_CREC},"✓ PASA · ≤ NORMAL",'
             f'IF(C86<={PAL}!D{R_CREC},"⚠ REVISAR · exige escenario BUENO","✗ BANDERA · > BUENO")))))))')
AN['D42'] = '=IF(C42="","—","ℹ COMPARA · ver múltiplos con su variable compañera (Diagnóstico V6, bloque 5)")'
_c86 = AN['C86'].value
assert _c86.startswith('=IF(OR(B108="",$C$37=""),"",')
AN['C86'] = f'=IF(OR({GATEP},{MO}!$B$193<>"✓ PASA"),"",' + _c86[1:].replace('$C$52<=0', f'N({HI}!$C$70)<=0') + ')'
AN['D86'] = f'=IF({GATEP},"—",' + AN['D86'].value[1:] + ')'

# ---- helper: banderas y avisos financieros en orden (para el Panel)
FL0 = CA0 + 14
M[f'A{FL0 - 1}'] = 'BANDERAS Y AVISOS FINANCIEROS (en orden; B = bandera, C = aviso, D/E = nº)'
M[f'A{FL0 - 1}'].font = Font(name=F, size=9, bold=True)
_fl = []
for _r in list(range(11, 15)) + list(range(17, 21)) + list(range(24, 29)) + list(range(31, 35)) + [52] + list(range(59, 63)) + list(range(84, 99)):
    _fl.append((f'Análisis!$A${_r}', f'Análisis!$D${_r}'))
for _r in range(DIAG0, DIAG0 + DIAGN):
    _fl.append((f'{DG}!$A${_r}', f'IF(ISNUMBER(SEARCH("BANDERA",{DG}!$C${_r})),{DG}!$C${_r},IF(ISNUMBER(SEARCH("BANDERA",{DG}!$B${_r})),{DG}!$B${_r},IF(ISNUMBER(SEARCH("BANDERA",{DG}!$D${_r})),{DG}!$D${_r},IF(ISNUMBER(SEARCH("REVISAR",{DG}!$C${_r})),{DG}!$C${_r},IF(ISNUMBER(SEARCH("REVISAR",{DG}!$B${_r})),{DG}!$B${_r},{DG}!$D${_r})))))'))
_fl.append((f'{DG}!$A${PG0 + 4}', f'{DG}!$D${PG0 + 4}'))
for _r in range(AC0, AC0 + ACN):
    _fl.append((f'{DG}!$A${_r}', f'{DG}!$B${_r}'))
for _i, (_lab, _val) in enumerate(_fl):
    _r = FL0 + _i
    M[f'A{_r}'] = f'={_lab}'
    M[f'B{_r}'] = f'=IF(ISNUMBER(SEARCH("BANDERA",{_val})),A{_r}&": "&{_val},"")'
    M[f'C{_r}'] = f'=IF(AND(B{_r}="",ISNUMBER(SEARCH("REVISAR",{_val}))),A{_r}&": "&{_val},"")'
    M[f'D{_r}'] = f'=IF(B{_r}="","",SUMPRODUCT(--($B${FL0}:B{_r}<>"")))'
    M[f'E{_r}'] = f'=IF(C{_r}="","",SUMPRODUCT(--($C${FL0}:C{_r}<>"")))'
FL1 = FL0 + len(_fl) - 1

# ================================================================== Control maestro
# FCF yield y margen frente a la fuente externa solo si el precio (y la capitalización, en su misma moneda) es comparable con el valor
AN['D41'] = f'=IF({GATE},"—",IF({GATEP},"— precio no comparable (moneda o unidad): sin FCF yield",' + AN['D41'].value[1:] + '))'
AN['B41'] = AN['B41'].value + ' La capitalización va en la moneda de cotización: si no coincide con la del modelo, este ratio no se calcula.'
AN['E54'] = ('La deuda importa para la fiabilidad del flujo y el riesgo. Si cambia mucho o domina la estructura financiera, '
             'elige en la fila 62 «No · financiación cambia mucho» (motor B): el valor se calcula con el flujo operativo y la deuda neta se resta en Diagnóstico V6.')
CM['A93'] = 'Valor terminal'
# Revisión 2 (punto 2): respuestas Pabrai fuera de dominio no cuentan como Sí ni como No
for _r in (11, 12, 13):
    AN[f'D{_r}'] = f'=IF(C{_r}="","—",IF(EXACT(C{_r},"Sí"),"✓ PASA",IF(EXACT(C{_r},"No"),"✗ BANDERA","⛔ TÉCNICO · solo Sí o No (exacto)")))'
# G3 · validación numérica en las celdas de precio, capitalización, acciones, r y exceso de caja (no mueve nada)
from openpyxl.worksheet.datavalidation import DataValidation as _DV
_covered = set()
for _dv in AN.data_validations.dataValidation:
    for _rng in str(_dv.sqref).split():
        _covered.add(_rng)
for _ref, _op, _f1 in (('C37', 'greaterThan', '0'), ('C41', 'greaterThan', '0'), ('C55', 'greaterThan', '0'), ('C76', 'greaterThanOrEqual', '0')):
    if not any(_ref == _c or _ref in _c.split(':') for _c in _covered):
        _d = _DV(type='decimal', operator=_op, formula1=_f1, allow_blank=True, showErrorMessage=True,
                 errorTitle='Dato no válido', error='Escribe un número (sin texto ni unidades).')
        AN.add_data_validation(_d)
        _d.add(_ref)
# Revisión 2 (punto 1): C52 y C59 distinguen vacío, cero y texto; nada se convierte en 0 en silencio
AN['C52'] = ('=IF(OR(C46="",C47="",C50="",C51="",NOT(ISNUMBER(C46)),NOT(ISNUMBER(C47)),NOT(ISNUMBER(C50)),'
             'AND(C48<>"",NOT(ISNUMBER(C48))),AND(C49<>"",NOT(ISNUMBER(C49))),NOT(OR(EXACT(C51,"Sí"),EXACT(C51,"No"))),N(C47)<0),"",'
             'C46-C47-IF(C48="",0,C48)-IF(C49="",0,C49)-IF(EXACT(C51,"No"),0,C50))')
AN['C59'] = ('=IF(OR(NOT(ISNUMBER(C50)),NOT(ISNUMBER(C46)),NOT(ISNUMBER(C47)),AND(C48<>"",NOT(ISNUMBER(C48))),AND(C49<>"",NOT(ISNUMBER(C49)))),"",'
             'IF((C46-C47-IF(C48="",0,C48)-IF(C49="",0,C49))<=0,"",C50/(C46-C47-IF(C48="",0,C48)-IF(C49="",0,C49))))')
AN['D46'] = '=IF(C46="","—",IF(NOT(ISNUMBER(C46)),"⛔ TÉCNICO · escribe un número (texto no vale)","ℹ dato"))'
AN['D47'] = '=IF(C47="","—",IF(NOT(ISNUMBER(C47)),"⛔ TÉCNICO · escribe un número (texto no vale)",IF(C47<0,"⛔ TÉCNICO · el capex va en positivo","ℹ dato")))'
for _ref in ('D48', 'D49', 'D50'):
    AN[_ref] = AN[_ref].value.replace('"⚠ REVISAR · escribe un número"', '"⛔ TÉCNICO · escribe un número (texto no vale)"')
AN['D51'] = ('=IF(C51="",IF(OR(C46="",C47=""),"—","⚠ REVISAR · elige Sí o No"),IF(NOT(OR(EXACT(C51,"Sí"),EXACT(C51,"No"))),"⛔ TÉCNICO · solo Sí o No (exacto)",'
             'IF(C50="","⚠ REVISAR · falta la SBC (fila 50)",IF(EXACT(C51,"No"),"ℹ FCF sin restar SBC","ℹ FCF neto de SBC"))))')
AN['D52'] = AN['D52'].value.replace('=IF(C52="","—",', '=IF(C52="",IF(OR(AND(C46<>"",NOT(ISNUMBER(C46))),AND(C47<>"",NOT(ISNUMBER(C47))),AND(C48<>"",NOT(ISNUMBER(C48))),AND(C49<>"",NOT(ISNUMBER(C49))),AND(C50<>"",NOT(ISNUMBER(C50))),N(C47)<0,AND(C51<>"",NOT(OR(EXACT(C51,"Sí"),EXACT(C51,"No"))))),"⛔ TÉCNICO · texto, signo o dominio incorrectos en C46:C51","—"),', 1)
assert 'dominio incorrectos en C46:C51' in AN['D52'].value
AN.conditional_formatting.add('D11:D104', FormulaRule(formula=['ISNUMBER(SEARCH("TÉCNICO",D11))'], fill=fill(BAD_BG), font=Font(color=BAD_FG, bold=True)))
AN['B53'] = 'Dato de balance. Motor A: usa C76 solo para el exceso claramente no operativo. Motores B y C: no se suma caja (C76 no se usa).'
AN['E7'] = AN['E7'].value.replace('COUNTA(C46:C47)+COUNTA(C50:C51)', "IF('Diagnóstico V6'!$C5=\"A\",COUNTA(C46:C47)+COUNTA(C50:C51),4)")
assert "COUNTA(C50:C51),4)" in AN['E7'].value
# E76: la deuda solo se resta en el motor B (Diagnóstico V6), nunca aquí
AN['E76'] = ('Solo motor A: escríbelo en C (se aplica a los 3 escenarios); vacío = 0; solo caja claramente sobrante (no la necesaria para operar) y ≤ caja de la fila 53; '
             'NO restes deuda aquí, el FCF ya va después de intereses. Motores B y C: déjalo vacío (no se usa; la hoja avisa si lo rellenas). La deuda neta del motor B se resta en Diagnóstico V6.')
# validación numérica de C46:C50 (donde no exista ya)
for _ref, _op, _f1 in (('C46', 'greaterThanOrEqual', '-1E+12'), ('C47', 'greaterThanOrEqual', '0'), ('C48', 'greaterThanOrEqual', '0'), ('C49', 'greaterThanOrEqual', '0'), ('C50', 'greaterThanOrEqual', '0')):
    if not any(_ref == _c or _ref in _c.split(':') for _c in _covered):
        _d = _DV(type='decimal', operator=_op, formula1=_f1, allow_blank=True, showErrorMessage=True,
                 errorTitle='Dato no válido', error='Escribe un número en millones (sin texto ni unidades).')
        AN.add_data_validation(_d)
        _d.add(_ref)
AN['C83'] = AN['C83'].value.replace('ROUND(SUM(B69:D69),4)<>1', 'ROUND(ABS(SUM(B69:D69)-1),9)>0.001').replace('SUMPRODUCT(B78:D78,B69:D69)', 'SUMPRODUCT(B78:D78,B69:D69)/SUM(B69:D69)')
AN['E69'] = AN['E69'].value.replace('ROUND(SUM(B69:D69),4)=1', 'ROUND(ABS(SUM(B69:D69)-1),9)<=0.001').replace('TEXT(SUM(B69:D69),"0%")', 'TEXT(SUM(B69:D69),"0.0%")')
assert '0.0%' in AN['E69'].value
# valor ponderado ≤ 0: bandera explícita en la lectura del margen
AN['D84'] = '=IF(AND(ISNUMBER(C83),C83<=0),"✗ BANDERA · valor ponderado ≤ 0: no hay margen posible",' + AN['D84'].value[1:] + ')'.replace('TEXT(SUM(B69:D69),"0%")', 'TEXT(SUM(B69:D69),"0.0%")')
assert 'ROUND(SUM' not in AN['C83'].value and 'ROUND(SUM' not in AN['E69'].value
# M6 · con lectura de precio bloqueada no se compara el precio con nada
AN['C39'] = f'=IF(OR({GATEP},C37="",C38="",NOT(ISNUMBER(C38)),N(C38)=0),"",(C38-C37)/C38)'
AN['C87'] = f'=IF(OR({GATEP},C83="",$C$38="",NOT(ISNUMBER($C$38)),N($C$38)=0),"",C83/$C$38-1)'
# M10 · «FCF ≤ 0» en C86 solo tiene sentido en el motor A
AN['C86'] = AN['C86'].value.replace(f'N({HI}!$C$70)<=0', f'AND({DG}!${D_MOTOR}="A",N({HI}!$C$70)<=0)')
# L7 · notas heredadas de la V5.3 que ya no describen el motor V6
AN['E52'] = ('Se calcula solo. Si sale ≤ 0 no es un error: con el motor A declara su naturaleza en Palancas C43 (y un FCF '
             'normalizado en C44 si procede); los motores B y C no lo usan para calibrar.')
AN['E71'] = 'Suma de los flujos de los años 1–10 del motor (ventas × margen tras impuestos − fugas − reinversión), traída a hoy.'
AN['E73'] = 'Flujo del año 11 ÷ (r − g), traído a hoy ÷ (1 + r)^10. El flujo 11 ya descuenta la reinversión g ÷ ROIC (Guía V6).'
CM['B93'] = 'Verificar el valor terminal del motor: flujo del año 11 (con reinversión g ÷ ROIC) ÷ (r − g), y que r > g.'
AN['A105'] = AN['A105'].value.replace('Amarillo = lo rellenas tú', 'Celdas de entrada (azul oscuro, texto azul claro) = lo rellenas tú')
OP['A1'] = OP['A1'].value.replace('celdas amarillas vacías', 'celdas de entrada vacías (fondo azul oscuro)')
OP['A18'] = OP['A18'].value.replace('PRIMERA celda amarilla vacía', 'PRIMERA celda de entrada vacía')
CM['A3'] = ('Versión V6.1 (26-oct-2026) · EN PRUEBAS: estados técnico y de inversión separados (Motor, filas 201–268), '
            'bloqueo de salidas con datos inválidos o modelo no aplicable, FCF base normalizado, comprobaciones de '
            'capitalización y moneda, tema oscuro. Ninguna celda de Análisis cambia de sitio.')
CM['A3'].font = Font(name=F, size=10, bold=True, color='FF7F6000')
for r_ in (60, 65, 70):
    CM.cell(r_, 3).value = {60: 'MALO', 65: 'NORMAL', 70: 'BUENO'}[r_] + ': crecimiento FCF años 1–10 (V6: calculado)'
    CM.cell(r_, 4).value = 'Automático V6'
CM['B94'] = ('Motores A y C: el FCF ya es del accionista y la deuda no se resta. Motor B: se descuenta el flujo '
             'operativo y se restan deuda, arrendamientos, pensiones y minoritarios (Diagnóstico V6).')
band(CM, 105, '  TRAZABILIDAD V6 · celdas nuevas (fase 1 y juicio)', 14)
header(CM, 106, [CM.cell(16, c).value for c in range(1, 15)])
rows = [('Historia', f'Historia!C{r}:L{r}', nm, 'Dato objetivo / serie histórica', 'Pendiente de investigación')
        for r, nm, _, _ in HROWS]
rows.append(('Historia', 'Historia!C57', 'Años de la media del FCF base', 'Dato objetivo / metadata', 'Pendiente de carga'))
rows.append(('Palancas', f'Palancas!{C_SECTOR}', 'Sector de Damodaran', 'Dato objetivo / clasificación',
             'Pendiente de investigación'))
for i in range(6):
    rows.append(('Palancas', f'Palancas!A{PAIS0 + i}:B{PAIS0 + i}', f'Dónde vende · fila {i + 1} (país y %)',
                 'Dato objetivo / reparto de ventas', 'Pendiente de investigación'))
J = [(C_ETAPA, 'Etapa del ciclo de vida'), (C_CASO, 'Caso especial'), (C_BASE, 'Base de partida del margen'),
     (C_IDA, 'I+D capitalizada en las anclas'), (C_IDV, 'Vida útil de la I+D')]
for lab, cc in (('MALO', 'B'), ('NORMAL', 'C'), ('BUENO', 'D')):
    J += [(f'{cc}{R_CREC}', f'{lab}: crecimiento años 1–5'), (f'{cc}{R_MARG}', f'{lab}: margen (o ROE) objetivo'),
          (f'{cc}{R_S2C}', f'{lab}: ventas por euro reinvertido'), (f'{cc}{R_ROIC}', f'{lab}: ROIC a largo plazo')]
J += [(C_PQ, 'Probabilidad de quiebra'), (C_REC, 'Recuperación si quiebra'), (C_MKT, 'Tamaño del mercado año 10')]
for i in range(3):
    J += [(f'A{PRED0 + i}', f'Predicción {i + 1}'), (f'B{PRED0 + i}', f'Predicción {i + 1}: fecha'),
          (f'C{PRED0 + i}', f'Predicción {i + 1}: probabilidad')]
for ref, nm in J:
    rows.append(('Palancas', f'Palancas!{ref}', nm, 'Juicio del inversor / V6', 'Pendiente de inversor'))
# V6.1 · seis celdas nuevas de ajustes y metadatos (bloque 6 de Palancas)
rows += [('Palancas', f'Palancas!{C_FCFNAT}', 'Naturaleza del FCF base ≤ 0 (motor A)', 'Juicio del inversor / V6.1', 'Pendiente de inversor'),
         ('Palancas', f'Palancas!{C_FCFNORM}', 'FCF base normalizado (mm)', 'Juicio del inversor / V6.1 · documentar el cálculo', 'Pendiente de inversor'),
         ('Palancas', f'Palancas!{C_FPRECIO}', 'Fecha del precio (Análisis C37)', 'Dato objetivo / metadata V6.1', 'Pendiente de carga'),
         ('Palancas', f'Palancas!{C_FACC}', 'Fecha de las acciones diluidas (Análisis C55)', 'Dato objetivo / metadata V6.1', 'Pendiente de carga'),
         ('Palancas', f'Palancas!{C_CAUSA}', 'Causa declarada de la diferencia precio × acciones frente a capitalización', 'Juicio del inversor / V6.1', 'Pendiente de inversor'),
         ('Palancas', f'Palancas!{C_MONEDA}', 'Moneda de cotización (comparabilidad con Control maestro H4)', 'Dato objetivo / metadata V6.1', 'Pendiente de carga'),
         ('Control maestro', "'Control maestro'!H4", 'Moneda base del modelo (la usan las comprobaciones de moneda)', 'Dato objetivo / metadata', 'Pendiente de carga'),
         ('Control maestro', "'Control maestro'!D5", 'Ratio ADR/ADS = acciones ordinarias por cada ADR (número; 1 = el precio ya es por acción). Obligatorio si la causa declarada es «ADR o ADS»', 'Dato objetivo / metadata', 'Pendiente de carga')]
CM['C5'] = 'Ratio ADR/ADS (acciones ordinarias por ADR; 1 = misma unidad)'
for i, vals in enumerate(rows):
    r_ = 107 + i
    for c, v in enumerate(vals, start=1):
        x = CM.cell(r_, c, v)
        x.font = Font(name=F, size=10)
        x.border = BOX
    for c in range(6, 15):
        CM.cell(r_, c).border = BOX
CM_LAST = 107 + len(rows) - 1
dv_list(CM, f'E107:E{CM_LAST}',
        '"Pendiente de investigación,Pendiente de inversor,Pendiente de carga,Listo para auditoría,Revisar"')
dv_list(CM, f'F107:F{CM_LAST}', '"Rellenado y verificado,Pendiente de inversor,No aplicable,Dato no verificable"')

# ================================================================== Panel (oscuro, por paneles)
PN = wb.create_sheet(PA)
PR0 = 20   # primera fila de palancas (deslizadores D20:D25, celdas vinculadas E20:E25)
widths(PN, {'A': 1.5, 'B': 34, 'C': 11, 'D': 12, 'E': 5, 'F': 11, 'G': 28, 'H': 7, 'I': 1.5,
            'J': 33, 'K': 12, 'L': 12, 'M': 12, 'N': 12, 'O': 1.5})
LASTC = 14


def tile(r1, c1, r2, c2, titulo):
    """Cabecera de panel: una fila de título sobre el bloque."""
    for c in range(c1, c2 + 1):
        PN.cell(r1, c).fill = fill(HDR_BG)
    x = PN.cell(r1, c1, titulo)
    x.font = Font(name=F, size=9, bold=True, color=MUTED)
    x.alignment = Alignment(vertical='center', indent=1)


def pcell(ref, val, fmt=None, bold=False, size=10, color=None, align=None, wrap=False):
    c = PN[ref]
    c.value = val
    c.font = Font(name=F, size=size, bold=bold, color=color)
    c.alignment = Alignment(vertical='center', horizontal=align, indent=(1 if align is None else 0), wrap_text=wrap)
    if fmt:
        c.number_format = fmt
    return c


# ---- cabecera
title(PN, 1, '', LASTC)
PN['A1'] = '="  DCF V6.1 · ANÁLISIS Y FILTRO   |   "&IF(Análisis!$B$3="","(empresa sin nombre)",Análisis!$B$3)&IF(Análisis!$D$3="",""," · "&Análisis!$D$3)'
PN['J1'] = (f'=IF(ISNUMBER(Análisis!$C$37),"Precio "&FIXED(Análisis!$C$37,2),"Precio —")&IF({PAL}!${C_MONEDA}="",""," "&{PAL}!${C_MONEDA})'
            f'&"   ·   Cap. "&IF(ISNUMBER(Análisis!$C$41),FIXED(Análisis!$C$41,0)&" mm"&IF({PAL}!${C_MONEDA}="",""," "&{PAL}!${C_MONEDA}),"—")&"   ·   "&IF({PAL}!${C_SECTOR}="","Sector —",{PAL}!${C_SECTOR})')
PN['J1'].font = Font(name=F, size=10, bold=True, color=WHITE)
PN['J1'].alignment = Alignment(vertical='center', horizontal='right', indent=1)
PN.merge_cells('J1:N1')
pcell('B2', f'={ST_VER}', bold=True, size=12)
PN.merge_cells('B2:H2')
pcell('J2', f'=IF({ST_LIBRO}="","",{ST_LIBRO})', bold=True, size=10, align='right')
PN.merge_cells('J2:N2')
PN.row_dimensions[2].height = 22
for word, fg in (('DATOS INVÁLIDOS', BAD_FG), ('MODELO NO APLICABLE', WARN_FG), ('DESCARTADA', 'FF8EA1FF'),
                 ('INCOMPLETA', MUTED), ('CANDIDATA', GOOD_FG)):
    PN.conditional_formatting.add('B2:H2', FormulaRule(formula=[f'ISNUMBER(SEARCH("{word}",$B$2))'],
                                                       font=Font(name=F, size=12, bold=True, color=fg), stopIfTrue=True))
PN.conditional_formatting.add('J2:N2', FormulaRule(formula=['LEFT($J$2,5)="LISTO"'], font=Font(name=F, size=10, bold=True, color=GOOD_FG)))
PN.conditional_formatting.add('J2:N2', FormulaRule(formula=['LEFT($J$2,8)="NO LISTO"'], font=Font(name=F, size=10, bold=True, color=WARN_FG)))

# ---- interruptores
band(PN, 4, '  INTERRUPTORES', LASTC)
SW = [('B', 'MOTOR', f'={DG}!$D$5', f'=IF({DG}!${D_MOTOR}="A","● A   ○ B   ○ C",'
                                    f'IF({DG}!${D_MOTOR}="B","○ A   ● B   ○ C",'
                                    f'IF({DG}!${D_MOTOR}="C","○ A   ○ B   ● C","○ A   ○ B   ○ C")))'),
      ('C', 'ESCENARIO', None, '=IF($C$6="MALO","●MALO ○NORMAL ○BUENO",'
                               'IF($C$6="BUENO","○MALO ○NORMAL ●BUENO","○MALO ●NORMAL ○BUENO"))'),
      ('F', 'ESTUDIO', None, '=IF($F$6="ON","━━━●","●━━━")'),
      ('G', 'BASE DEL MARGEN', f'=IF({PAL}!${C_BASE}="","Último año",{PAL}!${C_BASE})', None),
      ('J', 'I+D EN LAS ANCLAS', f'=IF({PAL}!${C_IDA}="Sí","ON","OFF")', None),
      ('L', 'QUIEBRA', f'=IF(N({PAL}!${C_PQ})>0,"ON · "&FIXED(100*{PAL}!${C_PQ},0)&" %","OFF")', None)]
for col, nm, val, glyph in SW:
    PN[f'{col}5'] = nm
    PN[f'{col}5'].font = Font(name=F, size=9, bold=True, color=MUTED)
    PN[f'{col}5'].alignment = Alignment(indent=1)
    if val is not None:
        pcell(f'{col}6', val, bold=True, size=11)
    if glyph:
        c = pcell(f'{col}7', glyph, size=11, bold=True)
        c.font = Font(name='Consolas', size=(10 if col == 'C' else 11), bold=True)
    for rr_ in ((6, 7) if glyph else (6,)):
        PN[f'{col}{rr_}'].border = BOX
PN.merge_cells('C5:D5'); PN.merge_cells('C6:D6'); PN.merge_cells('C7:D7')
PN.merge_cells('G5:H5'); PN.merge_cells('G6:H6')
PN.merge_cells('J5:K5'); PN.merge_cells('J6:K6')
PN.merge_cells('L5:N5'); PN.merge_cells('L6:N6')
PN['C6'] = 'NORMAL'
PN['F6'] = 'OFF'
dv_list(PN, 'C6', 'Lista_Escenario', prompt='Elige qué escenario estudias en el Panel.')
dv_list(PN, 'F6', 'Lista_OnOff', prompt='ON: tus ajustes cambian la columna «Tú». Munger no cambia nunca.')
for ref in ('C6', 'F6'):
    PN[ref].fill = fill(IN_BG)
    PN[ref].font = Font(name=F, size=11, bold=True, color=IN_FG)
for rng, on in (('F6:F7', '$F$6="ON"'), ('J6:K6', f'{PAL}!${C_IDA}="Sí"'),
                ('L6:N6', f'N({PAL}!${C_PQ})>0'), ('G6:H6', f'{PAL}!${C_BASE}="Media del ciclo"')):
    PN.conditional_formatting.add(rng, FormulaRule(formula=[on], fill=fill(BLUE_D),
                                                   font=Font(name=F, size=11, bold=True, color=WHITE)))
PN.row_dimensions[6].height = 18
PN.row_dimensions[7].height = 18

# ---- tres paneles de estado
tile(9, 2, 4, 4, 'ESTADO DEL MODELO')
tile(9, 6, 9, 8, 'DECISIÓN DE INVERSIÓN')
tile(9, 10, 9, 14, 'COMPROBACIONES Y AVISOS')
RD_, RF_ = f'{MO}!$D${RUL0}:$D${RUL1}', f'{MO}!$F${RUL0}:$F${RUL1}'
EST = [
    ('Datos obligatorios', f'=IF(COUNTIF({RD_},"INCOMPLETO")=0,"● completos","● "&COUNTIF({RD_},"INCOMPLETO")&" pendientes")'),
    ('Dominios de entrada', f'=IF(COUNTIF({RD_},"DATOS INVÁLIDOS")=0,"● válidos","● "&COUNTIF({RD_},"DATOS INVÁLIDOS")&" inválidos")'),
    ('Aplicabilidad del motor', f'=IF(COUNTIF({RD_},"MODELO NO APLICABLE")=0,"● motor "&{DG}!${D_MOTOR}&" aplicable","● no aplicable")'),
    ('Coherencia financiera (banderas · avisos)', f'=IF(N(Análisis!$C$7)>0,"● "&Análisis!$C$7&" bandera(s) · "&Análisis!$D$7&" aviso(s)",IF(N(Análisis!$D$7)>0,"● "&Análisis!$D$7&" aviso(s)","● sin banderas ni avisos"))'),
    ('DCF inverso', f'=IF({GATE},"● sin calcular",IF({MO}!$B$193="✓ PASA","● utilizable",IF({MO}!$B$193="—","● sin calcular","● no utilizable")))'),
    ('Probabilidades de escenario', f'=IF({MO}!$D${RIDX["V17"]}="OK","● correctas",IF({MO}!$D${RIDX["V17"]}="INCOMPLETO","● faltan","● inválidas"))'),
    ('Conciliación de capitalización', f'=IF({MO}!$D${RIDX["V27"]}="OK","● cuadra",IF({MO}!$D${RIDX["V27"]}="AVISO","● con aviso",IF({MO}!$D${RIDX["V27"]}="DATOS INVÁLIDOS","● no cuadra","● sin evaluar")))'),
    ('Estado del libro', f'={ST_LIBRO}'),
]
for i, (nm, f_) in enumerate(EST):
    r = 10 + i
    pcell(f'B{r}', nm, size=10)
    pcell(f'C{r}', f_, bold=True, size=10)
    PN.merge_cells(f'C{r}:D{r}')
    for col in 'BCD':
        PN[f'{col}{r}'].border = BOX
for kw, fg in (('inválid', BAD_FG), ('banderas', BAD_FG), ('● no cuadra', BAD_FG), ('NO LISTO', WARN_FG),
               ('● no aplicable', WARN_FG), ('● no utilizable', WARN_FG), ('● con aviso', WARN_FG),
               ('pendientes', MUTED), ('● sin calcular', MUTED), ('● faltan', MUTED), ('● sin evaluar', MUTED),
               ('● sin avisos', GOOD_FG), ('● sin banderas', GOOD_FG), ('bandera(s)', BAD_FG), ('aviso(s)', WARN_FG), ('avisos', WARN_FG),
               ('● completos', GOOD_FG), ('● válidos', GOOD_FG), ('aplicable', GOOD_FG), ('● utilizable', GOOD_FG),
               ('● correctas', GOOD_FG), ('● cuadra', GOOD_FG), ('LISTO', GOOD_FG)):
    PN.conditional_formatting.add('C10:D17', FormulaRule(formula=[f'ISNUMBER(SEARCH("{kw}",$C10))'],
                                                         font=Font(name=F, size=10, bold=True, color=fg), stopIfTrue=True))
# decisión de inversión
PAB = [('Filtro Pabrai · ¿entiendo el negocio? (C11)', 'Análisis!$C$11'),
       ('Filtro Pabrai · ¿círculo de competencia? (C12)', 'Análisis!$C$12'),
       ('Filtro Pabrai · ¿valor claro sin modelos? (C13)', 'Análisis!$C$13')]
for i, (nm, ref) in enumerate(PAB):
    r = 10 + i
    pcell(f'F{r}', nm, size=9)
    PN.merge_cells(f'F{r}:G{r}')
    pcell(f'H{r}', f'=IF({ref}="","—",IF(EXACT({ref},"Sí"),"✓",IF(EXACT({ref},"No"),"✗","?")))', bold=True, size=12, align='center')
    for col in 'FGH':
        PN[f'{col}{r}'].border = BOX
PN.conditional_formatting.add('H10:H12', FormulaRule(formula=['H10="✓"'], font=Font(name=F, size=12, bold=True, color=GOOD_FG)))
PN.conditional_formatting.add('H10:H12', FormulaRule(formula=['H10="✗"'], font=Font(name=F, size=12, bold=True, color=BAD_FG)))
PN.conditional_formatting.add('H10:H12', FormulaRule(formula=['H10="?"'], font=Font(name=F, size=12, bold=True, color=WARN_FG)))
pcell('F13', f'={ST_INV}', bold=True, size=11, align='center', wrap=True)
PN.merge_cells('F13:H14')
pcell('F15', f'=IF({ST_PAB}="",IF({ST_INV}="DENTRO DEL CÍRCULO","Tres «Sí» explícitos",IF(SUMPRODUCT(--EXACT(Análisis!$C$11:$C$13,"Sí"))+SUMPRODUCT(--EXACT(Análisis!$C$11:$C$13,"No"))<COUNTA(Análisis!$C$11:$C$13),"Hay una respuesta fuera de dominio (solo Sí o No): incidencia técnica","Faltan respuestas del filtro")),"Motivo: "&{ST_PAB}&". Se conserva para reconsiderarla.")', size=9, align='center', wrap=True)
PN.merge_cells('F15:H17')
for r in range(13, 18):
    for col in 'FGH':
        PN[f'{col}{r}'].border = BOX
PN.conditional_formatting.add('F13:H14', FormulaRule(formula=['$F$13="DENTRO DEL CÍRCULO"'], fill=fill(GOOD_BG), font=Font(name=F, size=11, bold=True, color=GOOD_FG)))
PN.conditional_formatting.add('F13:H14', FormulaRule(formula=['LEFT($F$13,10)="DESCARTADA"'], fill=fill('D9E1F2'), font=Font(name=F, size=11, bold=True, color='FF1F3A4D')))
PN.conditional_formatting.add('F13:H14', FormulaRule(formula=['LEFT($F$13,9)="PENDIENTE"'], fill=fill('EDEDED'), font=Font(name=F, size=11, bold=True, color='FF404040')))
# comprobaciones y avisos
CHK = [('Precio × acciones ≈ capitalización', f'=IF({MO}!$D${RIDX["V27"]}="N/A","— "&{MO}!$F${RIDX["V27"]},IF({MO}!$F${RIDX["V27"]}="",IF({MO}!$D${RIDX["V27"]}="OK","✓ cuadra (±"&FIXED(100*{DG}!$C$91,0)&" %)","— sin evaluar"),{MO}!$F${RIDX["V27"]}))'),
       ('Moneda de cotización frente a la del modelo', f'=IF({MO}!$F${RIDX["V25"]}="","✓ misma moneda: "&{MONEDA_MODELO},{MO}!$F${RIDX["V25"]})'),
       ('Unidad cotizada (ADR)', f'=IF({MO}!$F${RIDX["V26"]}="",IF({PAL}!${C_CAUSA}="ADR o ADS","✓ ratio 1: misma unidad que el valor","✓ sin ADR declarado"),{MO}!$F${RIDX["V26"]})'),
       ('Fechas del precio y de las acciones', f'=IF({MO}!$D${RIDX["V28"]}="N/A","— "&{MO}!$F${RIDX["V28"]},IF({MO}!$F${RIDX["V28"]}="",IF(AND(ISNUMBER({PAL}!${C_FPRECIO}),ISNUMBER({PAL}!${C_FACC})),"✓ coherentes","— sin fechas"),{MO}!$F${RIDX["V28"]}))')]
for i, (nm, f_) in enumerate(CHK):
    r = 10 + i
    pcell(f'J{r}', nm, size=9)
    pcell(f'K{r}', f_, size=9, wrap=True)
    PN.merge_cells(f'K{r}:N{r}')
    for col in 'JKLMN':
        PN[f'{col}{r}'].border = BOX
pcell('J14', f'="Causas técnicas: "&{ST_NC}&"   ·   Banderas financieras: "&N(Análisis!$C$7)&"   ·   Avisos financieros: "&N(Análisis!$D$7)', bold=True, size=10)
PN.merge_cells('J14:N14')
for k in range(2):
    r = 15 + k
    extra = f'&IF({ST_NC}>2," · … y "&({ST_NC}-2)&" más en Diagnóstico V6 (bloque 9)","")' if k == 1 else ''
    pcell(f'J{r}', f'=IF({MO}!$B${CA0 + k}="",IF({k}=0,"Sin causas técnicas activas",""),"Técnica "&{k + 1}&" · "&{MO}!$A${CA0 + k}&" · "&{MO}!$B${CA0 + k}{extra})', size=9, wrap=True)
    PN.merge_cells(f'J{r}:N{r}')
    PN.row_dimensions[r].height = 24
pcell('J17', f'=IF(N(Análisis!$C$7)>0,"Bandera financiera · "&IFERROR(INDEX({MO}!$B${FL0}:$B${FL1},MATCH(1,{MO}!$D${FL0}:$D${FL1},0)),"ver Análisis y Diagnóstico V6")&IF(N(Análisis!$C$7)>1," · … y "&(N(Análisis!$C$7)-1)&" más",""),'
             f'IF(N(Análisis!$D$7)>0,"Aviso financiero · "&IFERROR(INDEX({MO}!$C${FL0}:$C${FL1},MATCH(1,{MO}!$E${FL0}:$E${FL1},0)),"ver Análisis y Diagnóstico V6")&IF(N(Análisis!$D$7)>1," · … y "&(N(Análisis!$D$7)-1)&" más",""),"Sin banderas ni avisos financieros"))', size=9, wrap=True)
PN.merge_cells('J17:N17')
PN.row_dimensions[17].height = 24
PN.conditional_formatting.add('K10:N13', FormulaRule(formula=['LEFT($K10,1)="✓"'], font=Font(name=F, size=9, color=GOOD_FG)))
PN.conditional_formatting.add('J15:N17', FormulaRule(formula=['ISNUMBER(SEARCH("DATOS INVÁLIDOS",$J15))'], font=Font(name=F, size=9, bold=True, color=BAD_FG)))
PN.conditional_formatting.add('J15:N17', FormulaRule(formula=['ISNUMBER(SEARCH("NO APLICABLE",$J15))'], font=Font(name=F, size=9, bold=True, color=WARN_FG)))
PN.conditional_formatting.add('J17:N17', FormulaRule(formula=['LEFT($J17,8)="Bandera "'], font=Font(name=F, size=9, bold=True, color=BAD_FG)))
PN.conditional_formatting.add('J17:N17', FormulaRule(formula=['LEFT($J17,6)="Aviso "'], font=Font(name=F, size=9, bold=True, color=WARN_FG)))
for r in range(10, 18):
    PN.row_dimensions[r].height = max(PN.row_dimensions[r].height or 15, 18)

# ---- palancas + valor
tile(PR0 - 1, 2, PR0 - 1, 8, 'PALANCAS DEL ESCENARIO ELEGIDO')
for col, h in zip('BCDFGH', ['Palanca', 'Munger', 'Deslizador', 'Tú', 'Pista', 'Aviso']):
    c = PN[f'{col}{PR0 - 1}']
    c.value = h
    c.font = Font(name=F, size=9, bold=True, color=MUTED)
    c.fill = fill(HDR_BG)
    c.alignment = Alignment(vertical='center', indent=1)
PN[f'E{PR0 - 1}'].fill = fill(HDR_BG)
PAL_ROWS = [
    (PR0, f'={PAL}!$A${R_CREC}', f'=CHOOSE({IDX},{PAL}!$B${R_CREC},{PAL}!$C${R_CREC},{PAL}!$D${R_CREC})', 'E', PCT, R_CREC, (-0.10, 0.30), DIAG0),
    (PR0 + 1, f'={PAL}!$A${R_MARG}', f'=CHOOSE({IDX},{PAL}!$B${R_MARG},{PAL}!$C${R_MARG},{PAL}!$D${R_MARG})', 'F', PCT, R_MARG, (-0.10, 0.50), DIAG0 + 1),
    (PR0 + 2, f'={PAL}!$A${R_S2C}', f'=CHOOSE({IDX},{PAL}!$B${R_S2C},{PAL}!$C${R_S2C},{PAL}!$D${R_S2C})', 'G', DEC2, R_S2C, (0, 5), DIAG0 + 6),
    (PR0 + 3, '="g para siempre"', f'=CHOOSE({IDX},Análisis!$B$68,Análisis!$C$68,Análisis!$D$68)', 'H', PCT2, R_G, (0, 0.04), DIAG0 + 4),
    (PR0 + 4, f'={PAL}!$A${R_ROIC}', f'=CHOOSE({IDX},{PAL}!$B${R_ROIC},{PAL}!$C${R_ROIC},{PAL}!$D${R_ROIC})', 'I', PCT, R_ROIC, (0, 0.50), DIAG0 + 3),
    (PR0 + 5, '="Tasa de descuento del motor"', f'=INDEX({MO}!$J$6:$J$8,{IDX})', 'J', PCT2, None, (0.03, 0.16), DIAG0 + 8),
]
for r, nm, mung, mcol, fmt, erow, (lo, hi), drow in PAL_ROWS:
    pcell(f'B{r}', nm, bold=True)
    pcell(f'C{r}', mung, fmt)
    pcell(f'F{r}', f'=IF(OR({GATE},{MO}!{mcol}9=""),"",{MO}!{mcol}9)', fmt, bold=True, color=ACCENT)
    if erow:
        tf = track(f'C{r}', f'{PAL}!$G${erow}', f'{PAL}!$I${erow}', f'{PAL}!$F${erow}', lo, hi, you=f'F{r}')
    else:
        tf = track(f'C{r}', '""', '""', f'{DG}!${D_RMIN}', lo, hi, you=f'F{r}')
    c = pcell(f'G{r}', tf)
    c.font = Font(name='Consolas', size=11)
    c = pcell(f'H{r}', f'=IFERROR(LEFT(INDEX({DG}!$B${drow}:$D${drow},{IDX}),1),"—")'
                        if drow < DIAG0 + 6 else f'=IFERROR(LEFT({DG}!$C${drow},1),"—")', bold=True, size=12, align='center')
    PN[f'E{r}'] = 20
    PN[f'E{r}'].font = Font(name=F, size=9, color=MUTED)
    PN[f'E{r}'].alignment = Alignment(horizontal='center', vertical='center')
    for col in 'BCDEFGH':
        PN[f'{col}{r}'].border = BOX
    PN.row_dimensions[r].height = 19
dv = DataValidation(type='whole', operator='between', formula1='0', formula2='40', showErrorMessage=True)
PN.add_data_validation(dv)
dv.add(f'E{PR0}:E{PR0 + 5}')
for sym, col_ in (('✓', GOOD_FG), ('⚠', WARN_FG), ('✗', BAD_FG)):
    PN.conditional_formatting.add(f'H{PR0}:H{PR0 + 5}', FormulaRule(formula=[f'H{PR0}="{sym}"'],
                                                                     font=Font(name=F, size=12, bold=True, color=col_)))
note(PN, f'B{PR0 + 6}', 'Pista:  ▒ rango del sector   ◆ media de la empresa   ● Munger   ▲ tú.   El número gris (0–40, 20 = sin '
                        'cambio) es el que mueve el deslizador; con el Modo estudio apagado, «Tú» es igual a Munger.')
PN.merge_cells(f'B{PR0 + 6}:H{PR0 + 6}')
PN.row_dimensions[PR0 + 6].height = 26

tile(PR0 - 1, 10, PR0 - 1, 14, 'VALOR')
for col, h in (('K', 'Munger'), ('L', 'Tú')):
    c = PN[f'{col}{PR0 - 1}']
    c.value = h
    c.font = Font(name=F, size=9, bold=True, color=MUTED)
    c.alignment = Alignment(horizontal='right', indent=1, vertical='center')
VAL = [(PR0, 'Valor por acción', f'=IF({GATE},"",INDEX({MO}!$BK$6:$BK$8,{IDX}))', f'=IF({GATE},"",{MO}!$BK$9)', NUM2),
       (PR0 + 1, 'Margen de seguridad', f'=IF(OR({GATEP},NOT(ISNUMBER(K{PR0})),N(K{PR0})<=0,NOT(ISNUMBER(Análisis!$C$37))),"",(K{PR0}-Análisis!$C$37)/K{PR0})',
        f'=IF(OR({GATEP},NOT(ISNUMBER(L{PR0})),N(L{PR0})<=0,NOT(ISNUMBER(Análisis!$C$37))),"",(L{PR0}-Análisis!$C$37)/L{PR0})', '0%;[Red]-0%'),
       (PR0 + 2, 'FCF del año 1 (mm)', f'=IF({GATE},"",INDEX({MO}!$AU$6:$AU$8,{IDX}))', f'=IF({GATE},"",{MO}!$AU$9)', NUM),
       (PR0 + 3, 'Valor sin crecimiento (por acción)', f'=IF({GATE},"",INDEX({MO}!$BO$6:$BO$8,{IDX}))', f'=IF({GATE},"",{MO}!$BO$9)', NUM2),
       (PR0 + 4, 'Valor del crecimiento (por acción)',
        f'=IF({GATE},"",IFERROR(INDEX({MO}!$BI$6:$BI$8,{IDX})/Análisis!$C$55-INDEX({MO}!$BO$6:$BO$8,{IDX}),""))',
        f'=IF({GATE},"",IFERROR({MO}!$BI$9/Análisis!$C$55-{MO}!$BO$9,""))', NUM2),
       (PR0 + 5, 'Valor ponderado de los 3 escenarios', f'=IF({GATE},"",Análisis!$C$83)', None, NUM2)]
for r, nm, a_, b_, fmt in VAL:
    pcell(f'J{r}', nm)
    pcell(f'K{r}', a_, fmt, bold=True)
    if b_:
        pcell(f'L{r}', b_, fmt, bold=True, color=ACCENT)
    for col in 'JKLMN':
        PN[f'{col}{r}'].border = BOX
pcell(f'M{PR0}', f'=IF({GATEP},"",IF(ISNUMBER(Análisis!$C$37),"precio "&FIXED(Análisis!$C$37,2),""))', size=9, color=MUTED)
PN.merge_cells(f'M{PR0}:N{PR0}')
pcell(f'M{PR0 + 1}', f'=IF({GATEP},IF({GATE},"","sin lectura de precio"),"")', size=9, color=MUTED)
PN.merge_cells(f'M{PR0 + 1}:N{PR0 + 1}')
pcell(f'M{PR0 + 2}', f'=IF(AND({ON},NOT({GATE}),NOT({MO}!$BS$9)),"⚠ estudio no calculable: "&{MO}!$BT$9,"")', size=9, color=WARN_FG, wrap=True)
PN.merge_cells(f'M{PR0 + 2}:N{PR0 + 3}')
pcell(f'M{PR0 + 5}', f'=IF(OR({GATEP},NOT(ISNUMBER(Análisis!$B$78)),NOT(ISNUMBER(Análisis!$C$83))),"","precio de Sí (kit) "&FIXED(MIN(Análisis!$B$78,0.75*Análisis!$C$83),2))', size=9, color=MUTED)
PN.merge_cells(f'M{PR0 + 5}:N{PR0 + 5}')
note(PN, f'J{PR0 + 6}', 'Margen de seguridad (tú), de −50 % a +50 %:')
pcell(f'L{PR0 + 6}', f'=IF(ISNUMBER(L{PR0 + 1}),REPT("█",MAX(0,MIN(20,ROUND((L{PR0 + 1}+0.5)*20,0))))&'
                     f'REPT("░",20-MAX(0,MIN(20,ROUND((L{PR0 + 1}+0.5)*20,0)))),"")')
PN[f'L{PR0 + 6}'].font = Font(name='Consolas', size=11, color=ACCENT)
PN.merge_cells(f'L{PR0 + 6}:N{PR0 + 6}')
PN.conditional_formatting.add(f'L{PR0 + 6}:N{PR0 + 6}', FormulaRule(formula=[f'AND(ISNUMBER($L${PR0 + 1}),$L${PR0 + 1}<0.1)'], font=Font(name='Consolas', size=11, color=WARN_FG)))
PN.conditional_formatting.add(f'L{PR0 + 6}:N{PR0 + 6}', FormulaRule(formula=[f'AND(ISNUMBER($L${PR0 + 1}),$L${PR0 + 1}<0)'], font=Font(name='Consolas', size=11, color=BAD_FG)))

# ---- cuatro preguntas + proyección
Q0 = PR0 + 8
tile(Q0, 2, Q0, 8, 'LAS CUATRO PREGUNTAS DE DAMODARAN')
mB = lambda c: f'INDEX({MO}!${c}$6:${c}$8,{IDX})'
Q = [('1 · ¿Qué dan los activos que ya tiene?',
      f'=IF({GATE},"— valor bloqueado",IFERROR("Valor sin crecimiento "&FIXED({mB("BO")},2)&" por acción · el "&FIXED(100*{mB("BO")}/{mB("BK")},0)'
      '&" % del valor del escenario; el resto depende de crecer.",""))'),
     ('2 · ¿Cuánto vale el crecimiento y cuánto pagas por él?',
      f'=IF({GATE},"— valor bloqueado",IFERROR("Vale "&FIXED({mB("BI")}/Análisis!$C$55-{mB("BO")},2)&" por acción."&IF({GATEP},""," En el NORMAL pagas "'
      f'&FIXED({DG}!$C${PG0 + 2},2)&" · "&{DG}!$D${PG0 + 4}),""))'),
     ('3 · ¿Cuánto riesgo hay?',
      f'=IFERROR("Tasa del motor "&FIXED(100*INDEX({MO}!$J$6:$J$8,{IDX}),1)&" % · r mínima "'
      f'&FIXED(100*{DG}!${D_RMIN},1)&" % · quiebra "&FIXED(100*N({PAL}!${C_PQ}),0)&" %"&IF({GATE},""," · el «para siempre» pesa el "'
      f'&FIXED(100*{mB("BN")},0)&" %."),"")'),
     ('4 · ¿Cuándo madura y qué lo frena?',
      f'=IFERROR("Crece "&FIXED(100*$C${PR0},1)&" % en los años 1–5 y baja hasta "&FIXED(100*$C${PR0 + 3},1)'
      f'&" % en el año 10. ROIC a largo plazo "&FIXED(100*$C${PR0 + 4},0)&" % frente a "&FIXED(100*$C${PR0 + 5},1)&" %: "'
      f'&IF($C${PR0 + 4}<=$C${PR0 + 5},"crecer ya no crea valor.","crecer sigue creando valor."),"")')]
for i, (t_, l_) in enumerate(Q):
    r = Q0 + 1 + 2 * i
    pcell(f'B{r}', t_, bold=True)
    PN.merge_cells(f'B{r}:H{r}')
    pcell(f'B{r + 1}', l_, wrap=True, size=9)
    PN.merge_cells(f'B{r + 1}:H{r + 1}')
    PN.row_dimensions[r + 1].height = 24
note(PN, f'B{Q0 + 9}', 'Lo que se rellena está en «Palancas»; lo que se calcula, en «Diagnóstico V6»; las fórmulas y los principios, en «Guía V6».')
PN.merge_cells(f'B{Q0 + 9}:H{Q0 + 9}')
tile(Q0, 10, Q0, 14, 'PROYECCIÓN DEL ESCENARIO NORMAL (mm)')
for col, h in zip('JKLMN', ['Año', 'Ventas', 'EBIT', 'EBIT neto', 'FCF']):
    c = PN[f'{col}{Q0 + 1}']
    c.value = h
    c.font = Font(name=F, size=9, bold=True, color=MUTED)
    c.alignment = Alignment(horizontal=('left' if col == 'J' else 'right'), indent=1)
    c.border = BOX
for i, t in enumerate(range(1, 11)):
    r = Q0 + 2 + i
    lc, mc, fc = CL(26 + t), CL(36 + t), CL(46 + t)
    pcell(f'J{r}', f'=IF(ISNUMBER({HI}!$L$5),"FY"&({HI}!$L$5+{t}),"Año {t}")', size=9)
    pcell(f'K{r}', f'=IF(OR({GATE},{MO}!{lc}7=""),"",{MO}!{lc}7)', NUM, size=9)
    pcell(f'L{r}', f'=IF(OR({GATE},{MO}!{lc}7=""),"",{MO}!{lc}7*{MO}!{mc}7)', NUM, size=9)
    pcell(f'M{r}', f'=IF(OR({GATE},{MO}!{lc}7=""),"",{MO}!{lc}7*{MO}!{mc}7*(1-{MO}!$K$7))', NUM, size=9)
    pcell(f'N{r}', f'=IF(OR({GATE},{MO}!{fc}7=""),"",{MO}!{fc}7)', NUM, size=9)
    for col in 'JKLMN':
        PN[f'{col}{r}'].border = BOX

# ---- gráficos y sensibilidad
G0 = Q0 + 14
band(PN, G0, '  GRÁFICOS Y SENSIBILIDAD', LASTC)
lc = LineChart()
lc.title = 'Ventas: historia y escenarios (mm)'
lc.height, lc.width = 7.0, 12.4
lc.y_axis.numFmt = '#,##0'
lc.add_data(Reference(M, min_col=2, max_col=5, min_row=CH + 1, max_row=CH + 21), titles_from_data=True)
lc.set_categories(Reference(M, min_col=1, min_row=CH + 2, max_row=CH + 21))
for _s in lc.series:
    _s.cat = AxDataSource(strRef=StrRef(f=f"'Motor'!$A${CH + 2}:$A${CH + 21}"))
for s_, col_ in zip(lc.series, (GRAY, BLUE_L, BLUE_M, BLUE_D)):
    s_.graphicalProperties.line.solidFill = col_
    s_.graphicalProperties.line.width = 22225
    s_.smooth = False
lc.x_axis.delete = False
lc.y_axis.delete = False
lc.dispBlanksAs = 'gap'
PN.add_chart(lc, f'B{G0 + 1}')
bc = BarChart()
bc.type = 'col'
bc.title = 'Valor por acción frente al precio'
bc.height, bc.width = 7.0, 13.6
bc.add_data(Reference(M, min_col=2, min_row=VG + 1, max_row=VG + 5), titles_from_data=True)
bc.set_categories(Reference(M, min_col=1, min_row=VG + 2, max_row=VG + 5))
for _s in bc.series:
    _s.cat = AxDataSource(strRef=StrRef(f=f"'Motor'!$A${VG + 2}:$A${VG + 5}"))
bc.series[0].graphicalProperties.solidFill = BLUE_M
pl = LineChart()
pl.add_data(Reference(M, min_col=3, min_row=VG + 1, max_row=VG + 5), titles_from_data=True)
pl.series[0].graphicalProperties.line.solidFill = GRAY
pl.series[0].graphicalProperties.line.width = 25400
pl.series[0].smooth = False
bc += pl
bc.x_axis.delete = False
bc.y_axis.delete = False
bc.y_axis.tickLblPos = 'low'
PN.add_chart(bc, f'J{G0 + 1}')
tc = BarChart()
tc.type = 'bar'
tc.grouping = 'stacked'
tc.overlap = 100
tc.title = 'Qué palanca mueve más el valor · cambio por acción sobre la base (NORMAL)'
tc.height, tc.width = 8.2, 12.4
tc.add_data(Reference(M, min_col=4, max_col=5, min_row=TG + 1, max_row=TG + 7), titles_from_data=True)
tc.set_categories(Reference(M, min_col=1, min_row=TG + 2, max_row=TG + 7))
for _s in tc.series:
    _s.cat = AxDataSource(strRef=StrRef(f=f"'Motor'!$A${TG + 2}:$A${TG + 7}"))
tc.series[0].graphicalProperties.solidFill = GRAY
tc.series[1].graphicalProperties.solidFill = BLUE_M
tc.legend.position = 'b'
tc.x_axis.delete = False
tc.y_axis.delete = False
tc.y_axis.tickLblPos = 'low'
tc.x_axis.tickLblPos = 'low'
PN.add_chart(tc, f'B{G0 + 17}')
# sensibilidad r × g como mapa de calor
S0 = G0 + 17
tile(S0, 10, S0, 14, 'SENSIBILIDAD · valor ponderado, r × g para siempre')
for j, (h, ref) in enumerate((('', None), ('g − 0,5 pts', None), ('g base', None), ('g + 0,5 pts', None))):
    c = PN.cell(S0 + 1, 10 + j, h)
    c.font = Font(name=F, size=9, bold=True, color=MUTED)
    c.alignment = Alignment(horizontal='center')
for i, ri in enumerate((90, 91, 92)):
    r = S0 + 2 + i
    pcell(f'J{r}', f'=Análisis!$A${ri}', size=9)
    for j, ci in enumerate('BCD'):
        c = pcell(f'{CL(11 + j)}{r}', f'=IF(Análisis!{ci}{ri}="","",Análisis!{ci}{ri})', NUM2, size=10, align='center')
        c.border = BOX
    PN[f'J{r}'].border = BOX
from openpyxl.formatting.rule import ColorScaleRule
PN.conditional_formatting.add(f'K{S0 + 2}:M{S0 + 4}', ColorScaleRule(start_type='min', start_color='3B1A1A', mid_type='percentile',
                                                                      mid_value=50, mid_color='2A2F36', end_type='max', end_color='12301F'))
pcell(f'J{S0 + 6}', f'=IF({GATE},"",IF({GATEP},"Precio no comparable (moneda o unidad): el mapa no se compara con el precio.",IF(ISNUMBER(Análisis!$C$37),"Precio actual: "&FIXED(Análisis!$C$37,2)&" · las celdas por encima del precio son verdes.","")))', size=9, color=MUTED, wrap=True)
PN.merge_cells(f'J{S0 + 6}:N{S0 + 7}')
PN.sheet_view.showGridLines = False
PN.freeze_panes = 'A3'

# ================================================================== Guía V6
G = wb.create_sheet('Guía V6')
title(G, 1, '  GUÍA V6.1 · cómo funciona la hoja y por qué', 3)
GUIA = [
    ('S', 'La idea en una línea'),
    ('T', 'Cada número de un escenario tiene que salir de una historia y compararse con la realidad: la de la propia '
          'empresa (hoja Historia) y la de su sector (hoja Sector). Lo demás es aritmética.'),
    ('S', 'El recorrido'),
    ('T', '1. Historia: 10 años de datos de fase 1. De ahí salen las anclas: crecimiento, márgenes, capital por euro '
          'de ventas, ROIC y ROE.'),
    ('T', '2. Palancas: el analista elige el tipo de empresa y escribe cinco palancas por escenario. Es la ÚNICA hoja '
          'nueva que se rellena.'),
    ('T', '3. Motor (hoja oculta): convierte las palancas en flujos año a año y en valor. Análisis C62 elige el motor.'),
    ('T', '4. Diagnóstico V6: resultados, semáforos, cuánto pagas por crecer, múltiplos y autocomprobaciones.'),
    ('T', '5. Análisis: recibe el valor de cada escenario (B78:D78) y sigue igual que en la V5.3: ponderado, margen de '
          'seguridad, asimetría, DCF inverso y sensibilidad.'),
    ('T', '6. Panel: para estudiar. Mueves palancas en Modo estudio y ves qué cambia, sin tocar lo de Munger.'),
    ('S', 'V6.1 · Los dos estados de la hoja (Motor, filas 201–268; resumen en Panel y Análisis A6)'),
    ('T', 'ESTADO TÉCNICO: DATOS INVÁLIDOS (un dato fuera de su dominio: probabilidades fuera de [0, 1] o que no suman '
          '100 %, p de quiebra fuera de [0, 1], recuperación negativa, tipo impositivo fuera de [0, 1], g ≥ r, '
          'S2C ≤ 0, acciones ≤ 0, historia con huecos o fuera de sitio, texto donde va un número) › MODELO NO APLICABLE '
          '(financiera con motor A o B; FCF base ≤ 0 con motor A sin declarar o declarado estructural) › INCOMPLETO (falta un dato obligatorio) › COMPLETO Y '
          'VÁLIDO. Una celda obligatoria vacía es INCOMPLETO; rellena con un valor imposible es DATOS INVÁLIDOS.'),
    ('T', 'ESTADO DE INVERSIÓN, calculado aparte: PENDIENTE DE FILTRO (Análisis C11:C13 sin responder) · DESCARTADA '
          'POR FILTRO PABRAI (algún «No»; el registro se conserva para reconsiderarla) · DENTRO DEL CÍRCULO.'),
    ('T', 'El veredicto principal (Análisis A6 y Panel) sigue esta prioridad: inválidos › no aplicable › Pabrai › '
          'incompleta › candidata válida. La lista completa de causas activas está siempre a la vista (Panel, Diagnóstico '
          'V6 bloque 9, Motor filas 271+). Los AVISOS nunca bloquean: solo piden una explicación.'),
    ('T', 'Qué se bloquea: con DATOS INVÁLIDOS, MODELO NO APLICABLE o un dato obligatorio del motor ausente, la hoja no '
          'muestra valor por acción, ponderado, margen de seguridad, DCF inverso, sensibilidad ni gráficos '
          'de valor. Faltar la empresa, el precio o la capitalización también bloquea el valor (T01). Si las monedas no '
          'están declaradas o difieren, o la unidad cotizada no está verificada, se muestran las valoraciones pero no '
          'su lectura frente al precio. El DCF inverso que no supera su comprobación de monotonía solo se bloquea a sí '
          'mismo (Análisis C86 y su vista en el Panel). La falta de textos cualitativos (tesis, predicciones, etapas) '
          'deja el libro en NO LISTO, pero no esconde los números.'),
    ('S', 'V6.1 · FCF base ≤ 0 (solo motor A)'),
    ('T', 'Un FCF base ≤ 0 (Análisis C52) no es un error ni un descarte. Declara su naturaleza en Palancas C43: '
          'TRANSITORIO o EXTRAORDINARIO permiten escribir un FCF base normalizado (Palancas C44, estrictamente > 0, en mm '
          'y moneda del modelo) con el que se calibra f (Historia C70 dice cuál se ha usado y C71 de dónde sale); '
          'ESTRUCTURAL deja el motor A como NO APLICABLE: usa el motor B (Análisis C62). Los motores B y C no usan C52 '
          'para calibrar, así que no les afecta. El FCF normalizado nunca sustituye al histórico en los ratios de '
          'Análisis.'),
    ('S', 'V6.1 · Comprobaciones de comparabilidad (Palancas, bloque 6)'),
    ('T', '1) Precio × acciones frente a capitalización: desviación = |cap ÷ (precio × acciones) − 1|. Hasta el 5 % '
          'no se dice nada; entre el 5 % y el 25 % hay un AVISO que pide la causa (Palancas C47); por encima del 25 % '
          'sin causa declarada, DATOS INVÁLIDOS. «Ninguna» o vacío cuentan como no declarada. Los umbrales son '
          'parámetros (Diagnóstico V6, bloque 7).'),
    ('T', '2) Moneda: la cotización (Palancas C48) y el modelo (Control maestro H4) tienen que coincidir para leer el '
          'precio frente al valor; si no, se conservan las valoraciones y se dejan en blanco el margen de seguridad y '
          'las conclusiones de precio. La hoja NO convierte divisas: conviértelas tú, documéntalo y escribe la '
          'moneda del modelo. Un ADR declarado explica la diferencia, pero no demuestra que esté corregida: sin el '
          'ratio en Control maestro D5 queda como «comparabilidad no verificada».'),
    ('T', '3) Fechas: si la fecha del precio y la de las acciones (Palancas C45:C46) difieren más de 90 días '
          '(parámetro), AVISO.'),
    ('S', 'V6.1 · Lo que consume el kit del personaje (precio de Sí y cubo)'),
    ('T', 'El precio de Sí y el cubo (Sí · Vigilar · No · Demasiado difícil) son resultado del proceso que ejecuta el '
          'personaje del kit con estas salidas de la V6.1: valor por escenario (Análisis B78:D78), valor ponderado (C83), '
          'margen de seguridad (C84), precio (C37), veredicto (A6) y estado del libro. El precio de Sí lo calcula la hoja '
          'con la definición del kit, mín(valor del escenario MALO, 75 % del valor ponderado), en Diagnóstico V6 (bloque 9) '
          'y en el Panel, en blanco si no hay lectura de precio. El cubo lo decide el personaje con esa cifra, el precio y '
          'el veredicto: la hoja no lo asigna. La integración con el kit v1.3 queda por verificar cuando el kit esté disponible.'),
    ('S', 'V6.1 · Otras decisiones'),
    ('T', 'Reguladas y conglomerados: AVISO visible, nunca bloqueo. Financieras: bloqueo con motores A y B.'),
    ('T', 'Recuperación si quiebra (Palancas C23): total recuperable por los accionistas tras las obligaciones con '
          'terceros, en mm y moneda del modelo. Negativa → DATOS INVÁLIDOS; mayor que el valor BUENO antes del ajuste → '
          'solo AVISO. Se valida aunque p sea 0.'),
    ('T', 'Las pestañas conservan sus nombres (el kit de Munger y la migración dependen de ellos).'),
    ('S', 'Las cinco palancas'),
    ('T', 'Crecimiento de ventas (años 1–5). En los años 6–10 baja en línea recta hasta el g para siempre.'),
    ('T', 'Margen operativo objetivo. Parte del margen de hoy (o del medio del ciclo) y llega al objetivo en el año 5.'),
    ('T', 'Ventas por euro reinvertido (S2C marginal). Cada euro de ventas nuevas exige 1 ÷ S2C de inversión.'),
    ('T', 'g para siempre (Análisis B68:D68). Del 1 al 3 %; nunca ≥ la tasa de descuento del motor.'),
    ('T', 'ROIC a largo plazo. Tras el año 10, crecer al g exige reinvertir g ÷ ROIC del beneficio. Si ROIC es igual a '
          'la tasa de descuento, crecer ya no crea valor (el supuesto por defecto de Damodaran).'),
    ('S', 'Las dos medidas de S2C, que no son la misma'),
    ('T', 'S2C MARGINAL (Historia C53) = aumento de ventas ÷ reinversión neta acumulada. Es la palanca, y se compara '
          'con la historia de la propia empresa.'),
    ('T', 'S2C MEDIO (Historia C54) = ventas ÷ capital invertido. Es lo que publica Damodaran por sector, y solo se '
          'compara con el sector (Palancas, fila 19). Mezclarlas deforma las hipótesis de reinversión.'),
    ('S', 'Las fórmulas del motor A (accionista)'),
    ('F', 'FCF del año t = ventas_t × (margen_t × (1 − t) − f) − (ventas_t − ventas_t−1) ÷ S2C'),
    ('F', 'FCF del año 11 = ventas_11 × (margen objetivo × (1 − t) × (1 − g ÷ ROIC) − f)'),
    ('F', 'Valor = Σ FCF_t ÷ (1 + r)^t + FCF_11 ÷ ((r − g)(1 + r)^10) + exceso de caja'),
    ('T', 'f = fugas al accionista: lo que separa el EBIT después de impuestos de la caja que llega al accionista '
          '(intereses, arrendamientos y demás). Se calibra para que el motor reproduzca tu FCF base de Análisis C52. '
          'AVISO: el motor la supone proporcional a las ventas. Si la financiación cambia mucho, usa el motor B.'),
    ('S', 'Motor B (cuando la deuda cambia mucho)'),
    ('T', 'Flujo = ventas × margen × (1 − t) − reinversión, sin fugas. Se descuenta a la r operativa: tu r mezclada '
          'con el coste real de la deuda, con pesos de mercado. Al final se restan deuda, arrendamientos, pensiones y '
          'minoritarios, y se suma la caja.'),
    ('S', 'Motor C (bancos, aseguradoras, reguladas)'),
    ('T', 'Las palancas pasan a ser crecimiento del patrimonio, ROE objetivo y ROE a largo plazo. Reparto = beneficio '
          '− aumento del patrimonio. Para siempre: patrimonio × (ROE − g) ÷ (r − g).'),
    ('S', 'Los semáforos y el principio que defiende cada uno'),
    ('T', 'Crecimiento sobre el sector o su historia → «el crecimiento tiene que ganarse».'),
    ('T', 'Margen sobre su máximo o el sector → «todo lo bueno se acaba».'),
    ('T', 'ROIC marginal muy alto → «el crecimiento no es gratis».'),
    ('T', 'ROIC a largo plazo muy alto → sin moat duradero, nadie gana más que su coste para siempre.'),
    ('T', 'Mucho valor en el «para siempre» → «acepta la incertidumbre», no la escondas al final.'),
    ('T', 'Cuota de mercado implícita alta → «la oferta y la demanda no se derogan».'),
    ('T', 'Escenarios desordenados → «convierte historias en números».'),
    ('T', 'r por debajo de la r mínima → «el riesgo importa».'),
    ('S', 'El DCF inverso, y cuándo no sirve'),
    ('T', 'Busca el crecimiento que haría que tu valor igualara el precio. Con reinversión, más crecimiento no siempre '
          'significa más valor: si la curva no es creciente, o si el valor apenas se mueve, la hoja lo dice y no da un '
          'número. En la V5.3 esto no podía pasar porque crecer era gratis.'),
    ('S', 'Múltiplos con su variable compañera (Damodaran, cap. 6)'),
    ('T', 'PER ↔ crecimiento · Precio/valor contable ↔ ROE · EV/ventas ↔ margen · EV/EBITDA ↔ reinversión. Un múltiplo '
          'solo dice algo al lado de la variable que lo explica. Las medias de sector son agregados: el PER medio '
          'puede salir inflado por empresas con poco beneficio.'),
    ('S', 'Lo que NO hace la hoja'),
    ('T', 'No proyecta los tres estados financieros, ni la evolución de la deuda año a año, ni el calendario de una '
          'quiebra. Es un filtro para decidir qué empresas merecen un estudio profundo, no el estudio profundo.'),
    ('T', 'No mejora la calidad de los datos ni adivina el futuro. Los semáforos están para que no te engañes; las '
          'predicciones (Palancas, bloque 5) para saber, con el tiempo, si aciertas.'),
    ('S', 'Fuentes'),
    ('T', 'Damodaran: The uValue Companion y archivos Ginzu (fcffsimpleginzu, growthbreakdown, divginzu, model, '
          'ctryprem de julio de 2026).'),
]
r_ = 3
for kind, text in GUIA:
    if kind == 'S':
        subband(G, r_, text, 3)
        G.row_dimensions[r_].height = 20
    else:
        c = G.cell(r_, 1, text)
        G.merge_cells(start_row=r_, start_column=1, end_row=r_, end_column=3)
        c.alignment = Alignment(wrap_text=True, vertical='top', indent=1)
        c.font = Font(name='Consolas' if kind == 'F' else F, size=10)
        G.row_dimensions[r_] = G.row_dimensions[r_]
        G.row_dimensions[r_].height = 16 + 14 * (len(text) // 115)
    r_ += 1
widths(G, {'A': 70, 'B': 36, 'C': 36})
G.sheet_view.showGridLines = False

# ================================================================== TEXT() → FIXED() (independiente del idioma)
def _split_top(a):
    depth, parts, cur, inq = 0, [], '', False
    for ch in a:
        if ch == '"':
            inq = not inq
        if not inq:
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
            elif ch == ',' and depth == 0:
                parts.append(cur); cur = ''; continue
        cur += ch
    parts.append(cur)
    return parts


def fix_text(f_):
    out_, i = '', 0
    while True:
        j = f_.find('TEXT(', i)
        if j < 0:
            return out_ + f_[i:]
        if j > 0 and (f_[j - 1].isalpha() or f_[j - 1] == '_'):
            out_ += f_[i:j + 5]; i = j + 5; continue
        depth, k, inq = 0, j + 4, False
        while k < len(f_):
            ch = f_[k]
            if ch == '"':
                inq = not inq
            elif not inq:
                if ch == '(':
                    depth += 1
                elif ch == ')':
                    depth -= 1
                    if depth == 0:
                        break
            k += 1
        parts = _split_top(f_[j + 5:k])
        if len(parts) != 2:
            out_ += f_[i:k + 1]; i = k + 1; continue
        x, fmt = fix_text(parts[0]), parts[1].strip().strip('"')
        rep = {'0.0%': f'FIXED(100*({x}),1)&" %"', '0%': f'FIXED(100*({x}),0)&" %"',
               '0.00%': f'FIXED(100*({x}),2)&" %"', '#,##0.00': f'FIXED({x},2)', '#,##0': f'FIXED({x},0)',
               '+0%;-0%': f'IF(({x})>=0,"+","")&FIXED(100*({x}),0)&" %"'}.get(fmt)
        out_ += f_[i:j] + (rep if rep else f'TEXT({x},"{fmt}")')
        i = k + 1


for ws_ in (PN, P, D):
    for row in ws_.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith('=') and 'TEXT(' in c.value:
                c.value = fix_text(c.value)
for ref in ('D52', 'D62', 'D86', 'D42', 'A76', 'A90', 'A91', 'A92'):
    if isinstance(AN[ref].value, str) and 'TEXT(' in AN[ref].value:
        AN[ref] = fix_text(AN[ref].value)

# ================================================================== orden de hojas
del wb['Guía Simply Wall St']
order = ['Panel', 'Análisis', 'Palancas', 'Diagnóstico V6', 'Historia', 'Sector', 'Riesgo país', 'Guía V6',
         'Opciones', 'Control maestro', 'Motor']
wb._sheets = [wb[n] for n in order]
wb.active = 0
for ws in wb.worksheets:
    ws.sheet_view.tabSelected = (ws.title == 'Panel')
wb.calculation = CalcProperties(fullCalcOnLoad=True)
if '--claro' not in sys.argv:
    sys.path.insert(0, HERE)
    from theme_dark import apply_dark
    apply_dark(wb)
wb.save(OUT)
json.dump({'SENS': {f'{k[0]}|{k[1]}|{k[2]}': v for k, v in SENS.items()}, 'TOR': TOR, 'REV0': REV0, 'CH': CH,
           'VG': VG, 'TG': TG, 'CM_LAST': CM_LAST, 'RP_LAST': RP_LAST, 'SEC_LAST': SEC_LAST, 'PTOT': PTOT,
           'RES0': RES0, 'DIAG0': DIAG0, 'AC0': AC0, 'RVER': RVER},
          open(os.path.join(HERE, 'layout.json'), 'w'), indent=1)
print('OK', OUT)
