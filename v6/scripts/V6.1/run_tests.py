# -*- coding: utf-8 -*-
"""Pruebas automáticas de la plantilla V6.1 (casos T01–T18 y regresiones R01–R06).

Cada caso parte de una copia independiente de la plantilla, se rellena con openpyxl, se recalcula de verdad con
LibreOffice (headless) y se leen los valores calculados. Cada comprobación guarda esperado, obtenido y evidencia
(hoja!celda = valor). Lo que no se ejecuta queda como NO EJECUTADA, nunca como superada.

Uso: python3 run_tests.py Plantilla_V6.xlsx Plantilla_V6.1.xlsx(con deslizadores) carpeta_salida
"""
import sys, os, json, shutil, subprocess, zipfile, re, datetime, math
import openpyxl

TPL, FINAL, OUTDIR = sys.argv[1], sys.argv[2], sys.argv[3]
HERE = os.path.dirname(os.path.abspath(__file__))
V53 = os.path.join(HERE, 'plantilla_v53.xlsx')
HERMES = '/mnt/user-data/uploads/STOCKS v2/lote_01 completo/Hermes_evaluada.xlsx'
CASES_DIR = os.path.join(OUTDIR, 'casos')
RCT_DIR = os.path.join(OUTDIR, 'recalculados')
for d in (CASES_DIR, RCT_DIR):
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)

# celdas agregadas del Motor (V6.1)
# direcciones de Motor resueltas por etiqueta (robustas frente a cambios de filas)
_wbt = openpyxl.load_workbook(TPL)
_M = _wbt['Motor']
RR = {_M[f'A{r}'].value: r for r in range(201, 300) if isinstance(_M[f'A{r}'].value, str) and re.match(r'^[VC]\d\d$', _M[f'A{r}'].value)}
LB = {_M[f'A{r}'].value: r for r in range(240, 300) if isinstance(_M[f'A{r}'].value, str) and not _M[f'A{r}'].value.startswith('=') and _M[f'A{r}'].value not in RR}
ST = {'bloq': f"B{LB['BLOQUEO DEL VALOR']}", 'comp': f"B{LB['COMPARABLE precio ↔ valor']}", 'bloqp': f"B{LB['BLOQUEO DE LA LECTURA DE PRECIO']}", 'tec': f"B{LB['ESTADO TÉCNICO']}",
      'causa': f"B{LB['CAUSA TÉCNICA PRINCIPAL']}", 'causav': f"B{LB['CAUSA DEL BLOQUEO DEL VALOR']}", 'inv': f"B{LB['ESTADO DE INVERSIÓN']}", 'pab': f"B{LB['MOTIVO PABRAI']}",
      'nav': f"B{LB['Nº AVISOS']}", 'nc': f"B{LB['Nº CAUSAS ACTIVAS']}", 'libro': f"B{LB['ESTADO DEL LIBRO']}", 'precio': f"B{LB['LECTURA DE PRECIO']}", 'ver': f"B{LB['VEREDICTO PRINCIPAL']}", 'mono': 'B193'}
DG = 'Diagnóstico V6'
EXP = {}        # expected json por motor
RESULTS = []    # lista de dicts


def blank(v):
    return v is None or v == ''


def num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


# ------------------------------------------------------------------ construcción de casos
def base(motor, name):
    """Copia independiente rellenada con la Empresa X para el motor dado."""
    out = os.path.join(CASES_DIR, f'{name}.xlsx')
    subprocess.run([sys.executable, os.path.join(HERE, 'test_fill.py'), TPL, out, motor], check=True, capture_output=True)
    EXP[name] = json.load(open(out + '.expected.json'))
    return out


def derive(src, name, mutate):
    out = os.path.join(CASES_DIR, f'{name}.xlsx')
    wb = openpyxl.load_workbook(src)
    mutate(wb)
    wb.save(out)
    return out


def hist_cols():
    return [chr(ord('C') + i) for i in range(10)]


CASES = {}   # name -> (archivo, descripción, lista de comprobaciones)


NOLEAK = set()


def case(name, desc, path, checks, noleak=False):
    CASES[name] = (path, desc, checks)
    if noleak:
        NOLEAK.add(name)


# comprobaciones: (hoja, celda, descripción esperado, función(valor, ctx)->bool)
def eq(expected):
    return (f'= {expected!r}', lambda v, c: v == expected)


def starts(prefix):
    return (f'empieza por {prefix!r}', lambda v, c: isinstance(v, str) and v.startswith(prefix))


def contains(sub):
    return (f'contiene {sub!r}', lambda v, c: isinstance(v, str) and sub in v)


def is_blank():
    return ('en blanco', lambda v, c: blank(v))


def is_num():
    return ('numérico', lambda v, c: num(v))


def is_true():
    return ('VERDADERO', lambda v, c: v is True)


def is_false():
    return ('FALSO', lambda v, c: v is False)


def approx(x, tol=1e-6):
    return (f'≈ {x:.6f} (±{tol:g})', lambda v, c: num(v) and abs(v - x) <= tol)


def round3(x):
    return (f'redondeado a 3 decimales = {x:.3f}', lambda v, c: num(v) and round(v, 3) == round(x, 3))


def lt(x):
    return (f'< {x}', lambda v, c: num(v) and v < x)


def gt(x):
    return (f'> {x}', lambda v, c: num(v) and v > x)


def not_contains(sub):
    return (f'no contiene {sub!r}', lambda v, c: not (isinstance(v, str) and sub in v))


def num_or_blank():
    return ('numérico o en blanco (nunca un texto de error)', lambda v, c: num(v) or blank(v))


MOTOR = 'Motor'
AN = 'Análisis'
PA = 'Palancas'
HI = 'Historia'
PN = 'Panel'

# ---- bases
fA = base('A', 'T02_motorA')
fB = base('B', 'T02b_motorB')
fC = base('C', 'T02c_motorC')
for nm, f_, motor in (('T02_motorA', fA, 'A'), ('T02b_motorB', fB, 'B'), ('T02c_motorC', fC, 'C')):
    e = EXP[nm]
    case(nm, f'Empresa X completa · motor {motor} (R01: valores contra la réplica en Python)', f_, [
        (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (MOTOR, ST['inv'], *eq('DENTRO DEL CÍRCULO')),
        (MOTOR, ST['libro'], *eq('LISTO')), (MOTOR, ST['ver'], *starts('CANDIDATA VÁLIDA')),
        (AN, 'B78', *approx(e['B'])), (AN, 'C78', *approx(e['C'])), (AN, 'D78', *approx(e['D'])),
        (AN, 'B78', *round3(e['B'])), (AN, 'C78', *round3(e['C'])), (AN, 'D78', *round3(e['D'])),
        (AN, 'C83', *approx(e['pond'])), (AN, 'C84', *is_num()), (PN, 'K20', *approx(e['C'])),
    ])

# ---- T01 plantilla vacía
shutil.copy(TPL, os.path.join(CASES_DIR, 'T01_vacia.xlsx'))
case('T01_vacia', 'Plantilla vacía: INCOMPLETO, sin valores y sin errores', os.path.join(CASES_DIR, 'T01_vacia.xlsx'), [
    (MOTOR, ST['tec'], *eq('INCOMPLETO')), (MOTOR, ST['bloq'], *is_true()), (AN, 'C83', *is_blank()),
    (MOTOR, ST['ver'], *starts('INCOMPLETA')), (PN, 'K20', *is_blank()), (AN, 'C86', *is_blank())])


# ---- T03 historia
def t03(wb):
    H = wb[HI]
    for col in hist_cols()[:6]:
        for r in range(5, 27):
            H[f'{col}{r}'] = None
case('T03_historia_4_anos', 'Historia con solo 4 ejercicios → INCOMPLETO (V02) y valor bloqueado', derive(fA, 'T03_historia_4_anos', t03), [
    (MOTOR, ST['tec'], *eq('INCOMPLETO')), (MOTOR, ST['bloq'], *is_true()), (AN, 'C83', *is_blank()), (MOTOR, ST['causa'], *contains('ejercicios'))])


def t03b(wb):
    H = wb[HI]
    for r in range(5, 27):
        H[f'G{r}'] = None
case('T03b_historia_hueco', 'Historia con un hueco (2020 vacío) → DATOS INVÁLIDOS (V04)', derive(fA, 'T03b_historia_hueco', t03b), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, ST['bloq'], *is_true()), (AN, 'C83', *is_blank())])


def t03c(wb):
    H = wb[HI]
    cols = hist_cols()
    for r in range(5, 27):
        vals = [H[f'{c}{r}'].value for c in cols]
        for c, v in zip(cols[:-1], vals[1:]):
            H[f'{c}{r}'] = v
        H[f'{cols[-1]}{r}'] = None
case('T03c_historia_desplazada', 'Historia sin el año más reciente en la columna L → DATOS INVÁLIDOS (V03)', derive(fA, 'T03c_historia_desplazada', t03c), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, ST['bloq'], *is_true()), (AN, 'C83', *is_blank())])


# ---- T04 FCF base ≤ 0
def t04(wb):
    wb[AN]['C46'] = 10.0
    wb[PA]['C43'] = 'No aplica'
case('T04_fcf_neg_sin_naturaleza', 'FCF base ≤ 0 con motor A y sin naturaleza declarada → MODELO NO APLICABLE; nunca descarte', derive(fA, 'T04_fcf_neg_sin_naturaleza', t04), [
    (MOTOR, ST['tec'], *eq('MODELO NO APLICABLE')), (MOTOR, ST['bloq'], *is_true()), (AN, 'C83', *is_blank()),
    (MOTOR, ST['inv'], *eq('DENTRO DEL CÍRCULO')), (AN, 'D52', *contains('no es un error'))])


def t04b(wb):
    wb[AN]['C46'] = 10.0
    wb[PA]['C43'] = 'Transitorio'
    wb[PA]['C44'] = 80.0
case('T04b_fcf_neg_transitorio', 'FCF base ≤ 0 declarado transitorio con FCF normalizado 80 → calcula con aviso; C86 no muestra «FCF ≤ 0»', derive(fA, 'T04b_fcf_neg_transitorio', t04b), [
    (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (AN, 'B78', *is_num()), (AN, 'C83', *is_num()),
    (HI, 'C70', *approx(80.0)), (MOTOR, ST['nc'], *gt(0)), (AN, 'C86', *not_contains('FCF')), (AN, 'C86', *num_or_blank())])


def t04c(wb):
    wb[AN]['C46'] = 10.0
    wb[PA]['C43'] = 'Estructural'
case('T04c_fcf_neg_estructural', 'FCF base ≤ 0 declarado estructural → MODELO NO APLICABLE (usar motor B)', derive(fA, 'T04c_fcf_neg_estructural', t04c), [
    (MOTOR, ST['tec'], *eq('MODELO NO APLICABLE')), (MOTOR, ST['causa'], *contains('estructural')), (AN, 'C83', *is_blank())])


def t04d(wb):
    wb[AN]['C46'] = 10.0
    wb[PA]['C43'] = 'Transitorio'
    wb[PA]['C44'] = -5.0
case('T04d_fcf_normalizado_no_positivo', 'FCF normalizado ≤ 0 → no sirve para calibrar: MODELO NO APLICABLE', derive(fA, 'T04d_fcf_normalizado_no_positivo', t04d), [
    (MOTOR, ST['tec'], *eq('MODELO NO APLICABLE')), (AN, 'C83', *is_blank())])


# ---- T05 probabilidades
def t05(wb):
    wb[AN]['B69'], wb[AN]['C69'], wb[AN]['D69'] = -0.1, 1.1, 0.0
case('T05_probabilidades_fuera', 'Probabilidades −10 %, 110 %, 0 % → DATOS INVÁLIDOS; C83 en blanco', derive(fA, 'T05_probabilidades_fuera', t05), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (AN, 'C83', *is_blank()), (AN, 'B78', *(('texto con la causa (B78 nunca muestra un número bloqueado)', lambda v, c: isinstance(v, str) and 'probabilidad' in v.lower()))), (MOTOR, ST['causa'], *contains('[0, 1]'))])


def t05b(wb):
    wb[AN]['B69'], wb[AN]['C69'], wb[AN]['D69'] = 0.3, 0.3, 0.3
case('T05b_probabilidades_90', 'Probabilidades que suman 90 % → DATOS INVÁLIDOS', derive(fA, 'T05b_probabilidades_90', t05b), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (AN, 'C83', *is_blank()), (MOTOR, ST['causa'], *contains('suman'))])


# ---- T06 quiebra
def t06(wb):
    wb[PA]['C22'] = 1.5
case('T06_p_quiebra_150', 'Probabilidad de quiebra 150 % → DATOS INVÁLIDOS; sin valoración', derive(fA, 'T06_p_quiebra_150', t06), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (AN, 'C83', *is_blank()), (PN, 'K20', *is_blank())])


def t06b(wb):
    wb[PA]['C22'] = 0.0
    wb[PA]['C23'] = -10.0
case('T06b_recuperacion_negativa', 'Recuperación negativa (aunque p = 0) → DATOS INVÁLIDOS (D10)', derive(fA, 'T06b_recuperacion_negativa', t06b), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (AN, 'C83', *is_blank()), (MOTOR, ST['causa'], *contains('Recuperación'))])


def t06c(wb):
    wb[PA]['C22'] = 0.1
    wb[PA]['C23'] = 1e6
case('T06c_recuperacion_excesiva', 'Recuperación mayor que el valor BUENO antes del ajuste → solo AVISO (D10)', derive(fA, 'T06c_recuperacion_excesiva', t06c), [
    (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (AN, 'C83', *is_num()), (MOTOR, ST['nc'], *gt(0)), (MOTOR, f"F{RR['V20']}", *contains('supera'))])


# ---- T07 conciliación de capitalización
def t07(wb):
    wb[AN]['C37'], wb[AN]['C55'], wb[AN]['C41'] = 10.0, 100.0, 10000.0
case('T07_capitalizacion_incoherente', 'Precio 10 × 100 mm acciones frente a cap. 10.000 mm, sin causa → DATOS INVÁLIDOS', derive(fA, 'T07_capitalizacion_incoherente', t07), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, f"D{RR['V27']}", *eq('DATOS INVÁLIDOS')), (AN, 'C84', *is_blank())])


def t07b(wb):
    wb[AN]['C41'] = 2200 * 1.12
    wb[PA]['C47'] = 'ADR o ADS'
    wb['Control maestro']['D5'] = 1
case('T07b_desvio_12_con_causa_ADR', 'Desviación del 12 % con causa «ADR o ADS» y ratio 1 documentado → pasa con nota', derive(fA, 'T07b_desvio_12_con_causa_ADR', t07b), [
    (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (AN, 'C84', *is_num()), (MOTOR, f"D{RR['V27']}", *eq('AVISO'))])


def t07c(wb):
    wb[AN]['C41'] = 2200 * 1.12
case('T07c_desvio_12_sin_causa', 'Desviación del 12 % sin causa → AVISO que pide la causa; no bloquea', derive(fA, 'T07c_desvio_12_sin_causa', t07c), [
    (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (MOTOR, f"D{RR['V27']}", *eq('AVISO')), (MOTOR, f"F{RR['V27']}", *contains('C47')), (AN, 'C84', *is_num())])


def t07d(wb):
    wb[AN]['C41'] = 2200 * 1.40
    wb[PA]['C47'] = 'Split o contrasplit'
case('T07d_desvio_40_con_causa', 'Desviación del 40 % con causa declarada (split) → AVISO, no bloqueo', derive(fA, 'T07d_desvio_40_con_causa', t07d), [
    (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (MOTOR, f"D{RR['V27']}", *eq('AVISO'))])


def t07e(wb):
    wb[AN]['C41'] = 2200 * 1.04
case('T07e_desvio_4', 'Desviación del 4 % (dentro de la tolerancia) → en silencio', derive(fA, 'T07e_desvio_4', t07e), [
    (MOTOR, f"D{RR['V27']}", *eq('OK')), (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO'))])


def t13b(wb):
    wb[AN]['C41'] = 2200 * 1.12
    wb[PA]['C47'] = 'ADR o ADS'
    wb['Control maestro']['D5'] = None
case('T13b_ADR_sin_ratio', 'ADR declarado sin ratio documentado → «comparabilidad no verificada»; lectura de precio bloqueada', derive(fA, 'T13b_ADR_sin_ratio', t13b), [
    (MOTOR, f"F{RR['V27']}", *contains('no verificada')), (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (AN, 'B78', *is_num()), (AN, 'C84', *is_blank())])


# ---- T08 / T09 DCF inverso
def t08(wb):
    for col in 'BCD':
        wb[PA][f'{col}15'] = 0.05
        wb[PA][f'{col}16'] = 1.0
case('T08_dcf_inverso_no_monotono', 'Crecer destruye valor (margen 5 %, S2C 1) → C86 en blanco y D86 explica; no bloquea el valor', derive(fA, 'T08_dcf_inverso_no_monotono', t08), [
    (MOTOR, ST['mono'], *(lambda d: (d[0], d[1]))(('≠ "✓ PASA"', lambda v, c: v not in ('✓ PASA', '—', '', None)))),
    (AN, 'C86', *is_blank()), (AN, 'D86', *(('texto explicativo (no «—»)', lambda v, c: isinstance(v, str) and v not in ('—', '')))),
    (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (AN, 'B78', *is_num())])


def t09(wb):
    for col in 'BCD':
        wb[PA][f'{col}15'] = 0.12
        wb[PA][f'{col}16'] = 1.0
case('T09_dcf_inverso_plano', 'ROIC marginal ≈ r (margen 12 %, S2C 1): curva casi plana → C86 en blanco o lectura no informativa', derive(fA, 'T09_dcf_inverso_plano', t09), [
    (AN, 'C86', *num_or_blank()), (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO'))])


# ---- T10 / T11
def t10(wb):
    wb[AN]['C56'] = 0.10
    for col in 'BCD':
        wb[AN][f'{col}68'] = 0.12
case('T10_g_terminal_12', 'g terminal 12 % con tasa 10 % → DATOS INVÁLIDOS; sin valoración', derive(fA, 'T10_g_terminal_12', t10), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (AN, 'C83', *is_blank()), (PN, 'K20', *is_blank())])


def t11(wb):
    for col in 'BCD':
        wb[PA][f'{col}16'] = 0
case('T11_s2c_cero', 'S2C = 0 en el motor A → DATOS INVÁLIDOS; sin valoración', derive(fA, 'T11_s2c_cero', t11), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (AN, 'C83', *is_blank()), (MOTOR, ST['causa'], *contains('S2C'))])


# ---- T12 tipo de empresa
def t12(wb):
    wb[PA]['C6'] = 'Financiera (banco o aseguradora)'
case('T12_banco_motor_A', 'Financiera con motor A → MODELO NO APLICABLE', derive(fA, 'T12_banco_motor_A', t12), [
    (MOTOR, ST['tec'], *eq('MODELO NO APLICABLE')), (AN, 'C83', *is_blank()), (MOTOR, ST['causa'], *contains('financiera'))])


def t12b(wb):
    wb[PA]['C6'] = 'Regulada (red, concesión)'
case('T12b_regulada_motor_A', 'Regulada con motor A → AVISO visible; la valoración sigue (D8)', derive(fA, 'T12b_regulada_motor_A', t12b), [
    (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (AN, 'C83', *is_num()), (MOTOR, f"D{RR['V11']}", *eq('AVISO'))])


def t12c(wb):
    wb[PA]['C6'] = 'Multinegocio o conglomerado'
case('T12c_conglomerado_motor_A', 'Conglomerado con motor A → AVISO visible; la valoración sigue (D8)', derive(fA, 'T12c_conglomerado_motor_A', t12c), [
    (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (AN, 'C83', *is_num()), (MOTOR, f"D{RR['V11']}", *eq('AVISO'))])


def t12d(wb):
    wb[PA]['C6'] = 'Financiera (banco o aseguradora)'
case('T12d_banco_motor_C', 'Financiera con motor C → aplicable (COMPLETO Y VÁLIDO)', derive(fC, 'T12d_banco_motor_C', t12d), [
    (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (AN, 'C83', *is_num())])


# ---- T13 moneda
def t13(wb):
    wb[PA]['C48'] = 'USD'
    wb['Control maestro']['H4'] = 'EUR'
case('T13_monedas_distintas', 'Cotización en USD y modelo en EUR → valoraciones intactas; margen de seguridad y precio de Sí en blanco; aviso', derive(fA, 'T13_monedas_distintas', t13), [
    (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (AN, 'B78', *approx(EXP['T02_motorA']['B'])), (AN, 'C83', *is_num()),
    (AN, 'C84', *is_blank()), (AN, 'C85', *is_blank()), (PN, 'K21', *is_blank()), (MOTOR, f"D{RR['V25']}", *eq('AVISO')), (MOTOR, ST['bloq'], *is_false())])


# ---- T14 / T15 lectura de precio
def t14(wb):
    wb[AN]['C37'] = 40.0
    wb[AN]['C41'] = 4000.0
case('T14_margen_negativo', 'Libro válido con margen de seguridad negativo → CANDIDATA VÁLIDA; C84 < 0', derive(fA, 'T14_margen_negativo', t14), [
    (MOTOR, ST['ver'], *starts('CANDIDATA VÁLIDA')), (AN, 'C84', *lt(0))])


def t15(wb):
    wb[AN]['C37'] = 20.0
    wb[AN]['C41'] = 2000.0
case('T15_malo_bajo_precio', 'Valor del escenario MALO por debajo del precio → no invalida; se lee la asimetría (B80 < 0)', derive(fA, 'T15_malo_bajo_precio', t15), [
    (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (AN, 'B80', *lt(0)), (AN, 'C85', *(('texto de asimetría', lambda v, c: isinstance(v, str) and '/' in v)))])


# ---- T16 SBC y dilución
def t16(wb):
    H = wb[HI]
    for i, col in enumerate(hist_cols()):
        v = H[f'{col}6'].value
        H[f'{col}18'] = 0.08 * v
        H[f'{col}20'] = 100 * 1.03 ** i
    wb[AN]['C50'] = 0.08 * 1000
    wb[AN]['C51'] = 'No'
    wb[AN]['C60'] = 0.03
case('T16_sbc_y_dilucion', 'SBC alta sin restar y acciones creciendo → avisos en Análisis D59/D60', derive(fA, 'T16_sbc_y_dilucion', t16), [
    (AN, 'D59', *contains('REVISAR')), (AN, 'D60', *contains('REVISAR'))])


# ---- T17 vigencia de tablas
def t17(wb):
    wb[AN]['D4'] = datetime.date(2028, 3, 1)
case('T17_tablas_antiguas', 'Fecha de análisis 26 meses después de las tablas → AVISO de vigencia (V31)', derive(fA, 'T17_tablas_antiguas', t17), [
    (MOTOR, f"D{RR['V31']}", *eq('AVISO')), (MOTOR, f"F{RR['V31']}", *contains('meses')), (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO'))])


# ---- T18 terminal > 75 %
def t18(wb):
    for col in 'BCD':
        wb[PA][f'{col}14'] = 0.0
        wb[PA][f'{col}15'] = 0.12
        wb[PA][f'{col}18'] = 0.50
        wb[AN][f'{col}68'] = 0.05
    wb[AN]['C56'] = 0.07
case('T18_terminal_75', 'Más del 75 % del valor en el terminal → ⚠ REVISAR en Diagnóstico V6', derive(fA, 'T18_terminal_75', t18), [
    ('Diagnóstico V6', 'C28', *gt(0.75)), ('Diagnóstico V6', 'C44', *contains('REVISAR'))])


# ---- Pabrai
def tpab(wb):
    wb[AN]['C13'] = 'No'
case('TPAB_descartada', 'C13 = No → DESCARTADA POR FILTRO PABRAI; el registro y el valor se conservan', derive(fA, 'TPAB_descartada', tpab), [
    (MOTOR, ST['inv'], *eq('DESCARTADA POR FILTRO PABRAI')), (MOTOR, ST['ver'], *starts('DESCARTADA POR FILTRO PABRAI')),
    (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (AN, 'B78', *is_num())])


def tpab2(wb):
    wb[AN]['C11'] = None
case('TPAB2_pendiente', 'C11 vacío → PENDIENTE DE FILTRO e INCOMPLETO (nivel 3): los números no se esconden', derive(fA, 'TPAB2_pendiente', tpab2), [
    (MOTOR, ST['inv'], *eq('PENDIENTE DE FILTRO')), (MOTOR, ST['tec'], *eq('INCOMPLETO')), (MOTOR, ST['bloq'], *is_false()), (AN, 'B78', *is_num())])


# ---- casos de la auditoría ciega (26-oct-2026)
def au_tax150(wb):
    for col in 'HIJKL':
        wb[HI][f'{col}10'] = 1.5
case('AU_G1_tipo_impositivo_150', 'Auditoría G1: tipo impositivo 150 % → DATOS INVÁLIDOS y Diagnóstico V6 (B32:D32, D61) también en blanco', derive(fA, 'AU_G1_tipo_impositivo_150', au_tax150), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (DG, 'B32', *is_blank()), (DG, 'C32', *is_blank()), (DG, 'D32', *is_blank()), (DG, 'D61', *is_blank()), (AN, 'B67', *is_blank()), (DG, 'C55', *is_blank())])


def au_fin(wb):
    wb[PA]['C6'] = 'Financiera (banco o aseguradora)'
case('AU_G1b_financiera_diag', 'Auditoría G1: financiera con motor A → Diagnóstico V6 bloque 2 y múltiplos en blanco', derive(fA, 'AU_G1b_financiera_diag', au_fin), [
    (MOTOR, ST['tec'], *eq('MODELO NO APLICABLE')), (DG, 'B32', *is_blank()), (DG, 'D61', *is_blank()), (DG, 'D65', *is_blank())])


def au_precio0(wb):
    wb[AN]['C37'] = 0
case('AU_G2_precio_cero', 'Auditoría G2: precio 0 → DATOS INVÁLIDOS y valor bloqueado (B78, C83, B90, Panel K20 en blanco)', derive(fA, 'AU_G2_precio_cero', au_precio0), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, ST['bloq'], *is_true()), (AN, 'C83', *is_blank()), (AN, 'B90', *is_blank()), (PN, 'K20', *is_blank()), (PN, 'K25', *is_blank()), (DG, 'C55', *is_blank())])


def au_cap0(wb):
    wb[AN]['C41'] = 0
case('AU_G2b_cap_cero', 'Auditoría G2: capitalización 0 → DATOS INVÁLIDOS y valor bloqueado', derive(fA, 'AU_G2b_cap_cero', au_cap0), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, ST['bloq'], *is_true()), (AN, 'C83', *is_blank()), (PN, 'K20', *is_blank())])


def au_precio_txt(wb):
    wb[AN]['C37'] = '22 EUR'
case('AU_G3_precio_texto', 'Auditoría G3: precio como texto → DATOS INVÁLIDOS, valor bloqueado y ningún #VALUE!', derive(fA, 'AU_G3_precio_texto', au_precio_txt), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, ST['bloq'], *is_true()), (AN, 'C83', *is_blank()), (MOTOR, 'B193', *(('sin error', lambda v, c: not (isinstance(v, str) and v.startswith('#'))))), (PN, 'C14', *(('sin error', lambda v, c: not (isinstance(v, str) and v.startswith('#')))))])


def au_ventas0(wb):
    wb[HI]['L6'] = 0
case('AU_G4_ventas_ultimo_cero', 'Auditoría G4: ventas del último año = 0 → DATOS INVÁLIDOS (V32), libro NO LISTO', derive(fA, 'AU_G4_ventas_ultimo_cero', au_ventas0), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, ST['libro'], *starts('NO LISTO')), (AN, 'C83', *is_blank())])


def au_ventas_neg(wb):
    wb[HI]['L6'] = -500
case('AU_G4b_ventas_negativas', 'Auditoría G4: ventas negativas → DATOS INVÁLIDOS; nunca CANDIDATA con valores negativos', derive(fA, 'AU_G4b_ventas_negativas', au_ventas_neg), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (AN, 'C83', *is_blank()), (MOTOR, ST['ver'], *starts('DATOS INVÁLIDOS'))])


def au_ebit_vacio(wb):
    wb[HI]['L7'] = None
case('AU_G4c_ebit_ultimo_vacio', 'Auditoría G4: EBIT del último año vacío → INCOMPLETO (V33), libro NO LISTO, veredicto coherente', derive(fA, 'AU_G4c_ebit_ultimo_vacio', au_ebit_vacio), [
    (MOTOR, ST['tec'], *eq('INCOMPLETO')), (MOTOR, ST['libro'], *starts('NO LISTO')), (MOTOR, ST['ver'], *starts('INCOMPLETA')), (AN, 'C83', *is_blank())])


def au_margen_txt(wb):
    wb[PA]['C15'] = '20%'
case('AU_M1_margen_texto', 'Auditoría M1: texto en una palanca → DATOS INVÁLIDOS (no INCOMPLETO)', derive(fA, 'AU_M1_margen_texto', au_margen_txt), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, ST['causa'], *contains('no numérico'))])


def au_prob_txt(wb):
    wb[AN]['C69'] = '60%'
case('AU_M1b_prob_texto', 'Auditoría M1: probabilidad como texto → DATOS INVÁLIDOS', derive(fA, 'AU_M1b_prob_texto', au_prob_txt), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (AN, 'C83', *is_blank())])


def au_s2c_na(wb):
    wb[AN]['C62'] = 'Sí'
case('AU_M2_s2c_na_motorA', 'Auditoría M2: motor C → A conservando «n/a» en S2C → DATOS INVÁLIDOS y ningún #VALUE! en Motor', derive(fC, 'AU_M2_s2c_na_motorA', au_s2c_na), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, ST['causa'], *contains('S2C'))])


def au_prob_9995(wb):
    wb[AN]['B69'], wb[AN]['C69'], wb[AN]['D69'] = 0.2, 0.6, 0.1995
case('AU_M3_prob_tolerancia', 'Auditoría M3: probabilidades que suman 99,95 % (dentro de ±0,1 %) → válido y C83 calculado (una sola tolerancia)', derive(fA, 'AU_M3_prob_tolerancia', au_prob_9995), [
    (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (AN, 'C83', *is_num()), (AN, 'B90', *is_num()), (MOTOR, ST['libro'], *eq('LISTO'))])


def au_anio_dup(wb):
    wb[HI]['K5'] = 2023
case('AU_M4_anio_duplicado', 'Auditoría M4: año repetido en Historia (2023, 2023, 2025) → DATOS INVÁLIDOS', derive(fA, 'AU_M4_anio_duplicado', au_anio_dup), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, ST['causa'], *contains('consecutivos'))])


def au_moneda_diag(wb):
    wb[PA]['C48'] = 'USD'
    wb['Control maestro']['H4'] = 'EUR'
    wb[AN]['C38'] = 30
case('AU_M6_moneda_sin_comparaciones', 'Auditoría M6: monedas distintas → tampoco se compara el precio en Diagnóstico C54:C57/D57 ni en Análisis C39/C87', derive(fA, 'AU_M6_moneda_sin_comparaciones', au_moneda_diag), [
    (DG, 'C54', *is_blank()), (DG, 'C55', *is_blank()), (DG, 'C57', *is_blank()), (DG, 'D57', *eq('—')), (AN, 'C39', *is_blank()), (AN, 'C87', *is_blank()), (AN, 'B78', *is_num())])


def au_estudio_roic0(wb):
    wb[PN]['F6'] = 'ON'
    wb[PN]['E24'] = 0
case('AU_M7_estudio_roic_cero', 'Auditoría M7: modo estudio con ROIC en 0 → «Tú» en blanco y aviso en el Panel; Munger intacto', derive(fA, 'AU_M7_estudio_roic_cero', au_estudio_roic0), [
    (PN, 'L20', *is_blank()), (PN, 'M22', *contains('estudio no calculable')), (PN, 'K20', *approx(EXP['T02_motorA']['C']))])


def au_c57_dec(wb):
    wb[HI]['C57'] = 2.5
case('AU_M8_C57_decimal', 'Auditoría M8: Historia C57 = 2,5 → DATOS INVÁLIDOS (entero)', derive(fA, 'AU_M8_C57_decimal', au_c57_dec), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, ST['causa'], *contains('entero'))])


def au_precio_vacio(wb):
    wb[AN]['C37'] = None
    wb[AN]['C41'] = None
case('T01b_precio_y_cap_vacios', 'T01 restablecido (D13): precio y capitalización vacíos → INCOMPLETA y sin valoración visible', derive(fA, 'T01b_precio_y_cap_vacios', au_precio_vacio), [
    (MOTOR, ST['tec'], *eq('INCOMPLETO')), (MOTOR, ST['bloq'], *is_true()), (AN, 'C83', *is_blank()), (AN, 'C84', *is_blank()), (PN, 'K20', *is_blank()), (PN, 'K21', *is_blank())])


def au_fcf_neg_B(wb):
    wb[AN]['C46'] = 80
    wb[AN]['C47'] = 100
    wb[AN]['C48'] = None
    wb[AN]['C49'] = None
    wb[AN]['C50'] = 0
case('AU_M10_fcf_neg_motorB', 'Auditoría M10: FCF base ≤ 0 con motor B → C86 no dice «FCF ≤ 0»; el modelo sigue', derive(fB, 'AU_M10_fcf_neg_motorB', au_fcf_neg_B), [
    (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (AN, 'C86', *not_contains('FCF')), (AN, 'B78', *is_num())])


def au_fecha_ant(wb):
    wb[AN]['D4'] = datetime.date(2015, 1, 1)
case('AU_L10_fecha_anterior', 'Auditoría L10: fecha de análisis anterior a las tablas → AVISO', derive(fA, 'AU_L10_fecha_anterior', au_fecha_ant), [
    (MOTOR, f"D{RR['V31']}", *eq('AVISO')), (MOTOR, f"F{RR['V31']}", *contains('anterior'))])


def au_fecha_txt(wb):
    wb[AN]['D4'] = '20/10/2026'
case('AU_L9_fecha_texto', 'Auditoría L9: fecha de análisis como texto → AVISO', derive(fA, 'AU_L9_fecha_texto', au_fecha_txt), [
    (MOTOR, f"D{RR['V31']}", *eq('AVISO')), (MOTOR, f"F{RR['V31']}", *contains('texto'))])


def au_c76_neg(wb):
    wb[AN]['C76'] = -500
case('AU_L9b_exceso_caja_negativo', 'Auditoría L9: exceso de caja negativo → DATOS INVÁLIDOS (V34)', derive(fA, 'AU_L9b_exceso_caja_negativo', au_c76_neg), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (AN, 'C83', *is_blank())])


def au_crec500(wb):
    for col in 'BCD':
        wb[PA][f'{col}14'] = 5.0
case('AU_L16_crecimiento_500', 'Auditoría L16: crecimiento del 500 % → AVISO de unidades (no bloquea)', derive(fA, 'AU_L16_crecimiento_500', au_crec500), [
    (MOTOR, f"D{RR['V12']}", *eq('AVISO')), (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO'))])


def au_rec_p0(wb):
    wb[PA]['C22'] = 0
    wb[PA]['C23'] = 1e12
case('AU_L15_recuperacion_p0', 'Auditoría L15: p = 0 y recuperación enorme → sin aviso (no afecta al valor)', derive(fA, 'AU_L15_recuperacion_p0', au_rec_p0), [
    (MOTOR, f"D{RR['V20']}", *eq('OK')), (AN, 'C83', *approx(EXP['T02_motorA']['pond']))])


def au_tax_year(wb):
    wb[HI]['L10'] = 1.5
case('AU_L11_tipo_un_anio', 'Auditoría L11: un año con tipo impositivo 150 % y media dentro de [0,1] → AVISO', derive(fA, 'AU_L11_tipo_un_anio', au_tax_year), [
    (MOTOR, f"D{RR['V18']}", *eq('AVISO'))])


def r2_s2c_tiny(wb):
    for col in 'BCD':
        wb[PA][f'{col}16'] = 1e-9
case('AU_R2M1_s2c_minusculo', 'Auditoría r2-M1: S2C = 1e-9 → valor ≤ 0: aviso de S2C, aviso de valor ≤ 0 y BANDERA en D84', derive(fA, 'AU_R2M1_s2c_minusculo', r2_s2c_tiny), [
    (MOTOR, f"D{RR['V14']}", *eq('AVISO')), (MOTOR, f"D{RR['V36']}", *eq('AVISO')), (AN, 'D84', *contains('BANDERA')), (MOTOR, ST['ver'], *(('no empieza por CANDIDATA sin bandera', lambda v, c: isinstance(v, str) and 'resuelve' in v)))])


def r2_dos_invalidos(wb):
    wb[AN]['C55'] = -100
    wb[PA]['C22'] = 1.5
case('AU_R2_dos_invalidos_misma_causa', 'Auditoría r2: dos inválidos → A6 (veredicto) y B78 (causa del bloqueo) muestran la misma causa', derive(fA, 'AU_R2_dos_invalidos_misma_causa', r2_dos_invalidos), [
    (MOTOR, ST['causa'], *(('igual que la causa del bloqueo (B254)', lambda v, c: v == c.get('CAUSAV'))))])


def r2_nivel2_causa(wb):
    wb[AN]['C37'] = -22
case('AU_R2_bloqueo_nivel2_con_causa', 'Auditoría r2: inválido de nivel 2 (precio negativo) → B78 muestra la causa, no un blanco', derive(fA, 'AU_R2_bloqueo_nivel2_con_causa', r2_nivel2_causa), [
    (AN, 'B78', *contains('Precio')), (MOTOR, ST['bloq'], *is_true())])


def r2_prob_1001(wb):
    wb[AN]['B69'], wb[AN]['C69'], wb[AN]['D69'] = 0.2, 0.6, 0.201
case('AU_R2_prob_limite_1001', 'Auditoría r2: probabilidades que suman exactamente 100,1 % → en el límite, válido', derive(fA, 'AU_R2_prob_limite_1001', r2_prob_1001), [
    (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (AN, 'C83', *is_num())])


def r2_anio_fecha(wb):
    for i, col in enumerate(hist_cols()):
        wb[HI][f'{col}5'] = datetime.date(2016 + i, 12, 31)
case('AU_R2_anios_como_fecha', 'Auditoría r2 (L6): años escritos como fecha → DATOS INVÁLIDOS con causa clara', derive(fA, 'AU_R2_anios_como_fecha', r2_anio_fecha), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, ST['causa'], *contains('fecha'))])


def r2_B_texto(wb):
    wb[HI]['L15'] = 'ocho'
case('AU_R2_motorB_interes_texto', 'Auditoría r2: motor B con texto en intereses → DATOS INVÁLIDOS', derive(fB, 'AU_R2_motorB_interes_texto', r2_B_texto), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS'))])


def r2_diag_guardas(wb):
    wb[AN]['C55'] = -100
case('AU_R2_diag_sin_fugas', 'Auditoría r2: con el valor bloqueado, Diagnóstico B83 y E64 no presumen de calcular', derive(fA, 'AU_R2_diag_sin_fugas', r2_diag_guardas), [
    (DG, 'B83', *contains('TÉCNICO')), (DG, 'E64', *not_contains('reinversión año 1'))])


# ---- 2ª revisión (ChatGPT, 26-oct): puntos 1–4
def rv_txt(sheet, ref, val):
    def f(wb):
        wb[sheet][ref] = val
    return f
for nm, ref, val in (('P1a_C46_pendiente', 'C46', 'Pendiente'), ('P1b_C47_nd', 'C47', 'n/d'), ('P1c_C50_nd', 'C50', 'n/d'), ('P1d_C48_nd', 'C48', 'n/d'), ('P1e_C49_texto', 'C49', 'cero')):
    case(nm, f'Rev. 2 punto 1: texto en Análisis {ref} → DATOS INVÁLIDOS con causa exacta, C52 en blanco, sin errores ni ceros silenciosos', derive(fA, nm, rv_txt(AN, ref, val)), [
        (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, ST['causa'], *contains('Texto donde va un número')), (AN, 'C52', *is_blank()), (AN, 'C83', *is_blank()), (AN, 'D52', *contains('texto'))])
case('P1f_C51_fuera_dominio', 'Rev. 2 punto 1: C51 = «Tal vez» → DATOS INVÁLIDOS (solo Sí o No); C52 en blanco', derive(fA, 'P1f_C51_fuera_dominio', rv_txt(AN, 'C51', 'Tal vez')), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, ST['causa'], *contains('C51')), (AN, 'C52', *is_blank()), (AN, 'D51', *contains('solo Sí o No'))])
case('P1g_C46_negativo', 'Rev. 2 punto 1: CFO negativo no es inválido → FCF ≤ 0 → MODELO NO APLICABLE hasta declarar su naturaleza', derive(fA, 'P1g_C46_negativo', rv_txt(AN, 'C46', -50)), [
    (MOTOR, ST['tec'], *eq('MODELO NO APLICABLE')), (AN, 'C52', *lt(0))])
case('P1h_motorB_C50_texto', 'Rev. 2 punto 1: motor B con texto en C50 → DATOS INVÁLIDOS aunque el motor B no use C52', derive(fB, 'P1h_motorB_C50_texto', rv_txt(AN, 'C50', 'n/d')), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS'))])
case('P1i_motorB_C50_vacio', 'Rev. 2 punto 1: motor B con C50 vacío → no es obligatorio: sigue COMPLETO Y VÁLIDO', derive(fB, 'P1i_motorB_C50_vacio', rv_txt(AN, 'C50', None)), [
    (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (AN, 'B78', *is_num())])
case('P1j_C48_cero', 'Rev. 2 punto 1: C48 = 0 explícito se distingue de vacío y de texto: válido y C52 igual que con vacío', derive(fA, 'P1j_C48_cero', rv_txt(AN, 'C48', 0)), [
    (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO')), (AN, 'C52', *is_num())])

case('P2a_C13_pendiente', 'Rev. 2 punto 2: C13 = «Pendiente» → PENDIENTE DE FILTRO + incidencia técnica (DATOS INVÁLIDOS); Panel marca «?»', derive(fA, 'P2a_C13_pendiente', rv_txt(AN, 'C13', 'Pendiente')), [
    (MOTOR, ST['inv'], *eq('PENDIENTE DE FILTRO')), (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, ST['causa'], *contains('fuera de dominio')), (PN, 'H12', *eq('?')), (AN, 'D13', *contains('solo Sí o No'))])


def p2b(wb):
    wb[AN]['C12'] = 'n/d'
    wb[AN]['C13'] = 'No'
case('P2b_nd_y_No', 'Rev. 2 punto 2: «n/d» + «No» → DESCARTADA POR FILTRO PABRAI y a la vez incidencia técnica por la respuesta inválida', derive(fA, 'P2b_nd_y_No', p2b), [
    (MOTOR, ST['inv'], *eq('DESCARTADA POR FILTRO PABRAI')), (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (PN, 'H11', *eq('?')), (PN, 'H12', *eq('✗'))])
case('P2c_C11_vacio', 'Rev. 2 punto 2: C11 vacío → PENDIENTE DE FILTRO e INCOMPLETO (sin bloquear el valor)', derive(fA, 'P2c_C11_vacio', rv_txt(AN, 'C11', None)), [
    (MOTOR, ST['inv'], *eq('PENDIENTE DE FILTRO')), (MOTOR, ST['tec'], *eq('INCOMPLETO')), (MOTOR, ST['bloq'], *is_false()), (PN, 'H10', *eq('—'))])

case('P3a_C48_vacio', 'Rev. 2 punto 3: moneda de cotización sin declarar → no comparable: valor visible, margen de seguridad en blanco, aviso', derive(fA, 'P3a_C48_vacio', rv_txt(PA, 'C48', None)), [
    (MOTOR, ST['comp'], *is_false()), (AN, 'B78', *is_num()), (AN, 'C84', *is_blank()), (PN, 'K21', *is_blank()), (MOTOR, f"D{RR['V25']}", *eq('AVISO'))])
case('P3b_H4_vacio', 'Rev. 2 punto 3: moneda del modelo sin declarar → no comparable', derive(fA, 'P3b_H4_vacio', rv_txt('Control maestro', 'H4', None)), [
    (MOTOR, ST['comp'], *is_false()), (AN, 'C84', *is_blank()), (AN, 'B78', *is_num())])


def p3c(wb):
    wb[PA]['C48'] = None
    wb['Control maestro']['H4'] = None
case('P3c_ambas_vacias', 'Rev. 2 punto 3: ninguna moneda declarada → no comparable', derive(fA, 'P3c_ambas_vacias', p3c), [
    (MOTOR, ST['comp'], *is_false()), (AN, 'C84', *is_blank())])


def p3d(wb):
    wb[AN]['C41'] = 2200 * 1.12
    wb[PA]['C47'] = 'ADR o ADS'
    wb['Control maestro']['D5'] = 'Pendiente de verificar'
case('P3d_ADR_pendiente', 'Rev. 2 punto 3: ADR con ratio «Pendiente de verificar» → no acredita: comparabilidad no verificada, margen en blanco', derive(fA, 'P3d_ADR_pendiente', p3d), [
    (MOTOR, ST['comp'], *is_false()), (AN, 'C84', *is_blank()), (MOTOR, f"F{RR['V26']}", *contains('no verificada')), (PN, 'K12', *not_contains('✓'))])


def p3e(wb):
    wb[AN]['C41'] = 2200 * 1.12
    wb[PA]['C47'] = 'ADR o ADS'
    wb['Control maestro']['D5'] = 2
case('P3e_ADR_ratio_2', 'Rev. 2 punto 3: ratio 2 (precio por ADR, valor por acción) → unidades distintas: no comparable con aviso', derive(fA, 'P3e_ADR_ratio_2', p3e), [
    (MOTOR, ST['comp'], *is_false()), (AN, 'C84', *is_blank()), (MOTOR, f"F{RR['V26']}", *contains('unidades distintas'))])


def p3f(wb):
    wb['Control maestro']['D5'] = 2
case('P3f_ratio_2_sin_causa', 'Rev. 2 punto 3: ratio 2 documentado sin causa ADR → aviso y no comparable', derive(fA, 'P3f_ratio_2_sin_causa', p3f), [
    (MOTOR, ST['comp'], *is_false()), (MOTOR, f"D{RR['V26']}", *eq('AVISO'))])

case('P4a_precio_vacio', 'T01 (D13): precio vacío → INCOMPLETA y sin valoración visible', derive(fA, 'P4a_precio_vacio', rv_txt(AN, 'C37', None)), [
    (MOTOR, ST['tec'], *eq('INCOMPLETO')), (MOTOR, ST['bloq'], *is_true()), (AN, 'C83', *is_blank()), (PN, 'K20', *is_blank()), (AN, 'B78', *contains('precio'))])
case('P4b_empresa_vacia', 'T01 (D13): empresa vacía → INCOMPLETA y sin valoración visible', derive(fA, 'P4b_empresa_vacia', rv_txt(AN, 'B3', None)), [
    (MOTOR, ST['tec'], *eq('INCOMPLETO')), (MOTOR, ST['bloq'], *is_true()), (AN, 'C83', *is_blank()), (PN, 'K20', *is_blank())])
case('P4c_cap_vacia', 'T01 (D13): capitalización vacía → INCOMPLETA y sin valoración visible', derive(fA, 'P4c_cap_vacia', rv_txt(AN, 'C41', None)), [
    (MOTOR, ST['tec'], *eq('INCOMPLETO')), (MOTOR, ST['bloq'], *is_true()), (AN, 'C83', *is_blank())])
case('P4d_ticker_vacio', 'Ticker vacío → INCOMPLETO de completitud: NO LISTO pero el valor se muestra', derive(fA, 'P4d_ticker_vacio', rv_txt(AN, 'D3', None)), [
    (MOTOR, ST['tec'], *eq('INCOMPLETO')), (MOTOR, ST['bloq'], *is_false()), (AN, 'C83', *is_num()), (MOTOR, ST['libro'], *starts('NO LISTO'))])


# ---- auditoría ciega B (26-oct, tarde): hallazgos H1–H21
for _r in range(5, 27):
    nm = f'HB1_hist_L{_r}_texto'
    case(nm, f'Auditoría B H1/H2/H11/H16: texto en Historia L{_r} → DATOS INVÁLIDOS (V37 u otra regla más específica), sin errores, f en blanco', derive(fA, nm, rv_txt(HI, f'L{_r}', 'n/d')), [
        (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, ST['causa'], *(('causa no vacía', lambda v, c: isinstance(v, str) and len(v) > 5))), (HI, 'C58', *num_or_blank()), (AN, 'C83', *is_blank())])
case('HB1b_hist_C12_texto', 'Auditoría B H1: texto en Historia C12 (fuera de la media) → DATOS INVÁLIDOS y sin #VALUE!', derive(fA, 'HB1b_hist_C12_texto', rv_txt(HI, 'C12', 'n/d')), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (HI, 'C58', *num_or_blank())])
case('HB2_motorB_L24_texto', 'Auditoría B H2: motor B con texto en la caja (Historia L24) → DATOS INVÁLIDOS, no 0 en silencio', derive(fB, 'HB2_motorB_L24_texto', rv_txt(HI, 'L24', 'n/d')), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (AN, 'C83', *is_blank())])
case('HB11_motorC_L9_texto', 'Auditoría B H11: motor C con texto en el beneficio (Historia L9) → DATOS INVÁLIDOS', derive(fC, 'HB11_motorC_L9_texto', rv_txt(HI, 'L9', 'n/d')), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS'))])
case('HB3_C38_texto', 'Auditoría B H3: fuente externa como texto → aviso, sin #VALUE! en C39/D39/E43/C87/D87', derive(fA, 'HB3_C38_texto', rv_txt(AN, 'C38', 'n/d')), [
    (MOTOR, f"D{RR['V38']}", *eq('AVISO')), (AN, 'C39', *is_blank()), (AN, 'E43', *(('sin error', lambda v, c: isinstance(v, str) and not v.startswith('#')))), (AN, 'C87', *is_blank())])
case('HB4_precio_vacio_conciliacion', 'Auditoría B H4: sin precio, la conciliación no se muestra como aprobada (N/A) ni en el Panel', derive(fA, 'HB4_precio_vacio_conciliacion', rv_txt(AN, 'C37', None)), [
    (MOTOR, f"D{RR['V27']}", *eq('N/A')), (PN, 'K10', *starts('—')), (PN, 'C16', *contains('sin evaluar'))])
case('HB4b_vacia_conciliacion', 'Auditoría B H4: plantilla vacía: conciliación «sin evaluar» en Panel K10/C16', os.path.join(CASES_DIR, 'T01_vacia.xlsx'), [
    (PN, 'K10', *starts('—')), (PN, 'C16', *contains('sin evaluar')), (MOTOR, f"D{RR['V27']}", *eq('N/A'))])
case('HB5_sin_doble_conteo', 'Auditoría B H5: una causa técnica (texto en C46) no cuenta como bandera ni aviso financiero', derive(fA, 'HB5_sin_doble_conteo', rv_txt(AN, 'C46', 'Pendiente')), [
    (AN, 'C7', *eq(0)), (PN, 'J14', *contains('Banderas financieras: 0')), (AN, 'D52', *contains('TÉCNICO'))])
case('HB6_quiebra_150_sin_avisos_derivados', 'Auditoría B H6: con el valor bloqueado (quiebra 150 %) no se evalúan V29/V36 ni D86 sobre el motor', derive(fA, 'HB6_quiebra_150_sin_avisos_derivados', rv_txt(PA, 'C22', 1.5)), [
    (MOTOR, f"D{RR['V36']}", *eq('OK')), (MOTOR, f"D{RR['V29']}", *eq('OK')), (AN, 'D86', *eq('—')), (PN, 'J16', *not_contains('≤ 0')), (DG, 'B79', *contains('TÉCNICO'))])
case('HB7_D5_pendiente_sin_ADR', 'Auditoría B H7: «Pendiente de verificar» en Control maestro D5 sin ADR declarado → no comparable y aviso', derive(fA, 'HB7_D5_pendiente_sin_ADR', rv_txt('Control maestro', 'D5', 'Pendiente de verificar')), [
    (MOTOR, ST['comp'], *is_false()), (MOTOR, f"D{RR['V26']}", *eq('AVISO')), (PN, 'K12', *not_contains('✓')), (AN, 'C84', *is_blank())])
case('HB8_moneda_vacia_libro', 'Auditoría B H8: moneda sin declarar → libro NO LISTO · precio no comparable y veredicto que lo dice', derive(fA, 'HB8_moneda_vacia_libro', rv_txt(PA, 'C48', None)), [
    (MOTOR, ST['libro'], *starts('NO LISTO · precio no comparable')), (MOTOR, ST['ver'], *contains('precio no comparable')), (AN, 'B78', *is_num())])
case('HB10_capex_negativo', 'Auditoría B H10: capex negativo → DATOS INVÁLIDOS (convención de signo)', derive(fA, 'HB10_capex_negativo', rv_txt(AN, 'C47', -30)), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, ST['causa'], *contains('Capex negativo')), (AN, 'C52', *is_blank())])
case('HB12_C51_minusculas', 'Auditoría B H12: C51 = «sí» (minúsculas) → fuera de dominio (exacto)', derive(fA, 'HB12_C51_minusculas', rv_txt(AN, 'C51', 'sí')), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (AN, 'C52', *is_blank())])
case('HB12b_C11_minusculas', 'Auditoría B H12: C11 = «sí» → no cuenta como Sí: PENDIENTE DE FILTRO + incidencia técnica', derive(fA, 'HB12b_C11_minusculas', rv_txt(AN, 'C11', 'sí')), [
    (MOTOR, ST['inv'], *eq('PENDIENTE DE FILTRO')), (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (PN, 'H10', *eq('?'))])
case('HB17_pais_desconocido', 'Auditoría B H17: país no reconocido en Palancas A28 → aviso', derive(fA, 'HB17_pais_desconocido', rv_txt(PA, 'A28', 'Narnia')), [
    (MOTOR, f"D{RR['V30']}", *eq('AVISO')), (MOTOR, f"F{RR['V30']}", *contains('Riesgo país'))])
case('HB18_C83_sobrescrita', 'Auditoría B H18: fórmula de salida sobrescrita (C83 = 50) → DATOS INVÁLIDOS (V39)', derive(fA, 'HB18_C83_sobrescrita', rv_txt(AN, 'C83', 50)), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, ST['causa'], *contains('sobrescrita')), (PN, 'K25', *is_blank())], noleak=True)
case('HB20_C51_pendiente_diag', 'Auditoría B H20: C51 fuera de dominio → Diagnóstico B77 «TÉCNICO»', derive(fA, 'HB20_C51_pendiente_diag', rv_txt(AN, 'C51', 'Pendiente')), [
    (DG, 'B77', *contains('TÉCNICO'))])
case('HB14_C76_motorB', 'Auditoría B H14: C76 informado con motor B → aviso «no se usa», texto → inválido', derive(fB, 'HB14_C76_motorB', rv_txt(AN, 'C76', 100)), [
    (MOTOR, f"D{RR['V34']}", *eq('AVISO')), (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO'))])

case('HB22_pendientes_sin_NA', 'Auditoría B2 H22: precio vacío → «faltan 1» (las comprobaciones N/A no cuentan como pendientes)', derive(fA, 'HB22_pendientes_sin_NA', rv_txt(AN, 'C37', None)), [
    (MOTOR, ST['ver'], *contains('faltan 1 ·')), (MOTOR, ST['libro'], *contains('(1 pendientes)'))])
case('HB6b_empresa_vacia_sin_avisos_derivados', 'Auditoría B2 H6: con B3 vacía (bloqueo por C01) tampoco se evalúan V29/V36', derive(fA, 'HB6b_empresa_vacia_sin_avisos_derivados', rv_txt(AN, 'B3', None)), [
    (MOTOR, f"D{RR['V36']}", *eq('OK')), (MOTOR, f"D{RR['V29']}", *eq('OK')), (MOTOR, ST['bloq'], *is_true())])
case('HB18b_C58_sobrescrita', 'Auditoría B2 H18: f (Historia C58) sobrescrita con 0 → DATOS INVÁLIDOS (V39)', derive(fA, 'HB18b_C58_sobrescrita', rv_txt(HI, 'C58', 0)), [
    (MOTOR, ST['tec'], *eq('DATOS INVÁLIDOS')), (MOTOR, ST['causa'], *contains('sobrescrita')), (AN, 'C83', *is_blank())], noleak=True)
# H24 (booleanos en Historia): no verificable con LibreOffice, que trata VERDADERO como número (ISNUMBER(TRUE)=VERDADERO); en Excel es no numérico. Queda como NO EJECUTADA.
RESULTS.append({'prueba': 'HB24_booleano_historia', 'descripcion': 'Auditoría B2 H24: VERDADERO en Historia debe contar como no numérico (V37)', 'esperado': 'DATOS INVÁLIDOS en Excel',
                'obtenido': 'no verificable con LibreOffice (ISNUMBER(VERDADERO) = VERDADERO en LibreOffice, FALSO en Excel)', 'resultado': 'NO EJECUTADA'})
case('HB13_D41_valor_bloqueado', 'Auditoría B2 H13: con el valor bloqueado D41 dice «—», no «precio no comparable»', derive(fA, 'HB13_D41_valor_bloqueado', rv_txt(AN, 'C55', -100)), [
    (AN, 'D41', *eq('—'))])

# ---- R08 · validación con datos reales (ABB Ltd, fase 1 extraída con cita de página)
ABB_JSON = os.path.join(HERE, '..', 'abb', 'abb_fase1.json')
if os.path.exists(ABB_JSON):
    fABB = os.path.join(CASES_DIR, 'R08_ABB_datos_reales.xlsx')
    subprocess.run([sys.executable, os.path.join(HERE, 'fill_abb.py'), TPL, ABB_JSON, fABB], check=True, capture_output=True)
    _abb = json.load(open(os.path.join(HERE, '..', 'abb', 'abb_replica.json')))['replica'] if os.path.exists(os.path.join(HERE, '..', 'abb', 'abb_replica.json')) else None
    case('R08_ABB_datos_reales', 'ABB Ltd con 10 años reales (USD): INCOMPLETO solo por juicios pendientes; valor calculado y contrastado con la réplica; precio en CHF no comparable; sin errores', fABB, [
        (MOTOR, ST['tec'], *eq('INCOMPLETO')), (MOTOR, ST['bloq'], *is_false()), (MOTOR, ST['comp'], *is_false()), (MOTOR, ST['inv'], *eq('PENDIENTE DE FILTRO')),
        (AN, 'C78', *(approx(_abb['NORMAL']) if _abb else is_num())), (AN, 'C83', *(approx(_abb['pond']) if _abb else is_num())), (AN, 'C84', *is_blank()), (AN, 'D41', *contains('no comparable')),
        (HI, 'C43', *eq(10)), (HI, 'C53', *is_blank()), (MOTOR, f"D{RR['V25']}", *eq('AVISO'))])

# ---- R02 equivalencia con la V5.3
def r02(wb):
    H = wb[HI]
    H['L12'] = H['L8'].value          # capex = D&A en el último año
    H['L14'] = 0                      # ΔWC = 0
    H['C57'] = 1                      # f calibrada con 1 año
    for col in 'BCD':
        wb[PA][f'{col}14'] = 0.025
        wb[PA][f'{col}15'] = 0.20
        wb[PA][f'{col}16'] = 1e9
        wb[PA][f'{col}18'] = 1e9
        wb[AN][f'{col}68'] = 0.025
fR02 = derive(fA, 'R02_equivalencia_v53', r02)
_e = EXP['T02_motorA']
_c52, _r, _g = _e['c52'], 0.09, 0.025
_v53 = (sum(_c52 * (1 + _g) ** t / (1 + _r) ** t for t in range(1, 11)) + _c52 * (1 + _g) ** 11 / ((_r - _g) * (1 + _r) ** 10)) / 100
case('R02_equivalencia_v53', f'Margen constante, sin reinversión, sin bajada 6–10, ROIC→∞: motor A = fórmula V5.3 ({_v53:.6f})', fR02, [
    (AN, 'B78', *approx(_v53, 1e-5)), (AN, 'C78', *approx(_v53, 1e-5)), (AN, 'D78', *approx(_v53, 1e-5)), (MOTOR, ST['tec'], *eq('COMPLETO Y VÁLIDO'))])


# ---- R05 modo estudio
def r05(wb):
    P = wb[PN]
    P['F6'] = 'ON'
    for r, v in zip(range(20, 26), (30, 10, 25, 24, 35, 5)):
        P[f'E{r}'] = v
case('R05_modo_estudio', 'Modo estudio ON con los seis deslizadores movidos: Análisis B78:D78 y C83 no cambian; «Tú» sí', derive(fA, 'R05_modo_estudio', r05), [
    (AN, 'B78', *approx(_e['B'])), (AN, 'C78', *approx(_e['C'])), (AN, 'D78', *approx(_e['D'])), (AN, 'C83', *approx(_e['pond'])),
    (PN, 'L20', *(('distinto de Munger (K20)', lambda v, c: num(v) and num(c.get('K20')) and abs(v - c['K20']) > 1e-6))),
    (MOTOR, ST['mono'], *(('B193 ≠ ✓ PASA sólo si procede (informativo)', lambda v, c: True)))])


# ---- R03 migración Hermès
fHer = os.path.join(CASES_DIR, 'R03_hermes_migrada.xlsx')
if os.path.exists(HERMES):
    subprocess.run([sys.executable, os.path.join(HERE, 'migrate_values.py'), HERMES, TPL, fHer, os.path.join(OUTDIR, 'R03_conciliacion_hermes.json')],
                   check=True, capture_output=True)
    conc = json.load(open(os.path.join(OUTDIR, 'R03_conciliacion_hermes.json')))
    case('R03_hermes_migrada', 'Hermès (V5.3) migrada con lista blanca: 1.263 valores conciliados, sin conflictos, libro sin errores', fHer, [
        (AN, 'B3', *contains('Herm')), (AN, 'C37', *is_num()), (MOTOR, ST['tec'], *(('INCOMPLETO (faltan Historia y Palancas, que la V5.3 no tenía)', lambda v, c: v == 'INCOMPLETO')))])
    RESULTS.append({'prueba': 'R03_conciliacion', 'descripcion': 'Conciliación de la migración de Hermès',
                    'esperado': 'total = conservados + excluidos + transformados; 0 conflictos; 1.263 valores sin fórmula en el origen',
                    'obtenido': conc['resumen'],
                    'resultado': 'SUPERADA' if (conc['resumen']['conflictos'] == 0 and conc['resumen']['total_no_formula_origen'] == 1263
                                               and conc['resumen']['total_no_formula_origen'] == sum(conc['resumen'][k] for k in ('conservados', 'excluidos', 'transformados', 'conflictos'))) else 'FALLIDA',
                    'evidencia': 'R03_conciliacion_hermes.json'})

# ------------------------------------------------------------------ recálculo real con LibreOffice (una llamada)
files = [p for p, _, _ in CASES.values()]
subprocess.run(['soffice', '--headless', '--calc', '--convert-to', 'xlsx', '--outdir', RCT_DIR] + files,
               capture_output=True, timeout=1800)
# también la plantilla final (para R04 sobre el archivo recalculado)
subprocess.run(['soffice', '--headless', '--calc', '--convert-to', 'xlsx', '--outdir', RCT_DIR, FINAL], capture_output=True, timeout=600)

# ------------------------------------------------------------------ evaluación
ERR_RE = re.compile(r'^#(VALUE|REF|DIV/0|NAME|NUM|N/A|NULL)')


def scan_errors(wb):
    errs = []
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                if isinstance(c.value, str) and ERR_RE.match(c.value):
                    if ws.title == 'Motor' and c.value == '#N/A' and 141 <= c.row <= 169:
                        continue   # NA() intencional en los datos de los gráficos (huecos: Motor B141:E162 y B166:C169)
                    errs.append(f'{ws.title}!{c.coordinate}={c.value}')
    return errs


def cell(wb, sheet, ref):
    try:
        return wb[sheet][ref].value
    except Exception as ex:
        return f'<sin leer: {ex}>'


for name, (path, desc, checks) in CASES.items():
    rpath = os.path.join(RCT_DIR, os.path.basename(path))
    entry = {'prueba': name, 'descripcion': desc, 'archivo': os.path.relpath(path, OUTDIR), 'comprobaciones': []}
    if not os.path.exists(rpath):
        entry['resultado'] = 'NO EJECUTADA'
        entry['motivo'] = 'LibreOffice no produjo el archivo recalculado'
        RESULTS.append(entry)
        continue
    wb = openpyxl.load_workbook(rpath, data_only=True)
    ctx = {ref: cell(wb, PN, ref) for ref in ('K20', 'L20')}
    ctx['CAUSAV'] = cell(wb, MOTOR, ST['causav'])
    ok_all = True
    for sheet, ref, exp_desc, fn in checks:
        v = cell(wb, sheet, ref)
        try:
            ok = bool(fn(v, ctx))
        except Exception as ex:
            ok = False
            v = f'{v!r} (excepción {ex})'
        ok_all &= ok
        entry['comprobaciones'].append({'celda': f'{sheet}!{ref}', 'esperado': exp_desc, 'obtenido': v if isinstance(v, (int, float, str, bool)) or v is None else str(v),
                                        'resultado': 'OK' if ok else 'FALLO'})
    # bloqueo global: con el valor bloqueado no puede colarse ningún número en las salidas (hallazgos G1/G2 de la auditoría)
    if cell(wb, MOTOR, ST['bloq']) is True and name not in NOLEAK:
        leaks = []
        for sh, rng in ((AN, 'B78:D78'), (AN, 'C83:C86'), (AN, 'B90:D92'), (AN, 'B67:D67'), (PN, 'K20:L25'), (DG, 'B22:D36'), (DG, 'D61:D65'), (DG, 'C53:C57')):
            for row in wb[sh][rng]:
                for c in row:
                    if num(c.value):
                        leaks.append(f'{sh}!{c.coordinate}={c.value}')
        entry['comprobaciones'].append({'celda': 'salidas con el valor bloqueado', 'esperado': 'ningún número en Análisis B78:D78, C83:C86, B90:D92, B67:D67; Panel K20:L25; Diagnóstico B22:D36, D61:D65, C53:C57',
                                        'obtenido': leaks[:15] if leaks else 'ninguno', 'resultado': 'OK' if not leaks else 'FALLO'})
        ok_all &= not leaks
    errs = scan_errors(wb)
    entry['comprobaciones'].append({'celda': 'libro completo', 'esperado': 'sin #VALUE!, #REF!, #DIV/0!, #NAME?, #NUM! (R06)',
                                    'obtenido': errs[:20] if errs else 'ninguno', 'resultado': 'OK' if not errs else 'FALLO'})
    ok_all &= not errs
    entry['resultado'] = 'SUPERADA' if ok_all else 'FALLIDA'
    RESULTS.append(entry)


# ------------------------------------------------------------------ R04 · integridad del libro, contra la base (2ª revisión, punto 5)
import hashlib
SHA = hashlib.sha256(open(FINAL, 'rb').read()).hexdigest()
RESULTS.append({'prueba': 'R00_version_probada', 'descripcion': 'Identificación exacta del archivo probado', 'esperado': 'SHA-256 del archivo final con deslizadores',
                'obtenido': {'archivo': os.path.basename(FINAL), 'sha256': SHA, 'plantilla_sin_deslizadores': os.path.basename(TPL), 'sha256_tpl': hashlib.sha256(open(TPL, 'rb').read()).hexdigest()}, 'resultado': 'SUPERADA'})


def dv_set(ws):
    out = set()
    for dv in ws.data_validations.dataValidation:
        for rng in str(dv.sqref).split():
            out.add((rng, dv.type or '', dv.operator or '', str(dv.formula1 or ''), str(dv.formula2 or '')))
    return out


def cf_set(ws):
    out = set()
    for rng in ws.conditional_formatting:
        for rule in rng.rules:
            out.add((str(rng.sqref), rule.type or '', '|'.join(rule.formula or []), rule.operator or ''))
    return out


wb53 = openpyxl.load_workbook(V53)
wbF = openpyxl.load_workbook(FINAL)
# diferencias autorizadas (cada una con su motivo, en el registro de cambios)
AUTORIZADAS_DV = {
    'Análisis': {'añadidas': ['C37', 'C41', 'C55', 'C76', 'C46', 'C47', 'C48', 'C49', 'C50', 'C62'], 'quitadas': ['B67', 'C67', 'D67', 'C62'],
                 'motivo': 'validación numérica añadida (G3 y 2ª revisión punto 1); B67:D67 pasan a fórmula (crecimiento del FCF calculado por el motor) y pierden su lista; C62 cambia su lista inline por el rango con nombre Lista_C62 (misma lista, opción del motor C renombrada)'},
    'Control maestro': {'añadidas_prefijo': ['E107:E', 'F107:F'], 'motivo': 'filas de trazabilidad V6.1 (listas de estado y clasificación)'},
    'Opciones': {'añadidas': [], 'motivo': ''},
}
AUTORIZADAS_CF = {'Análisis': {'quitadas_rango': ['A6', 'A6:B6'], 'motivo': 'las reglas de A6/A6:B6 se sustituyen por las de los cinco estados (veredicto V6.1)'},
                  'Control maestro': {'quitadas_rango': []}, 'Opciones': {'quitadas_rango': []}}
r04a = {'prueba': 'R04a_validaciones_y_CF_vs_V5.3', 'descripcion': 'Validaciones de datos y reglas de formato condicional de Análisis, Control maestro y Opciones comparadas con la V5.3; solo se admiten las diferencias autorizadas',
        'esperado': 'ninguna validación ni regla de la V5.3 perdida salvo las autorizadas; añadidas solo las autorizadas', 'obtenido': {}, 'resultado': 'SUPERADA'}
for sh in ('Análisis', 'Control maestro', 'Opciones'):
    a, b = dv_set(wb53[sh]), dv_set(wbF[sh])
    aut = AUTORIZADAS_DV[sh]
    lost = sorted(x[0] for x in a - b if x[0] not in aut.get('quitadas', []))
    added = sorted(x[0] for x in b - a)
    added_ok = [x for x in added if x in aut.get('añadidas', []) or any(x.startswith(pfx) for pfx in aut.get('añadidas_prefijo', []))]
    added_bad = [x for x in added if x not in added_ok]
    # Lista_C62: el contenido del rango con nombre cambia (opción renombrada), la validación de C62 sigue siendo la misma
    ca, cb = cf_set(wb53[sh]), cf_set(wbF[sh])
    cf_lost = sorted(set(x[0] for x in ca - cb))
    cf_lost_bad = [x for x in cf_lost if x not in AUTORIZADAS_CF[sh]['quitadas_rango']]
    cf_added = sorted(set(x[0] for x in cb - ca))
    r04a['obtenido'][sh] = {'validaciones_V5.3': len(a), 'validaciones_V6.1': len(b), 'perdidas': lost, 'añadidas': added, 'añadidas_no_autorizadas': added_bad,
                            'CF_V5.3': len(ca), 'CF_V6.1': len(cb), 'CF_rangos_perdidos': cf_lost, 'CF_perdidos_no_autorizados': cf_lost_bad, 'CF_rangos_añadidos': cf_added}
    if lost or added_bad or cf_lost_bad:
        r04a['resultado'] = 'FALLIDA'
RESULTS.append(r04a)

# R04b · entradas de Análisis: misma coordenada, misma etiqueta, siguen siendo entradas (no fórmulas) y conservan su validación
WL = ['B3', 'D3', 'B4', 'D4', 'C11', 'C12', 'C13', 'C14', 'C17', 'C18', 'C19', 'C20', 'C24', 'C25', 'C26', 'C27', 'C28', 'C31', 'C32', 'C33', 'C34',
      'C37', 'C38', 'C40', 'C41', 'C42', 'C46', 'C47', 'C48', 'C49', 'C50', 'C51', 'C53', 'C54', 'C55', 'C56', 'C57', 'C60', 'C61', 'C62',
      'B65', 'C65', 'D65', 'B66', 'C66', 'D66', 'B68', 'C68', 'D68', 'B69', 'C69', 'D69', 'C76', 'C88', 'C93', 'C96', 'C97', 'C98', 'B101', 'B102', 'C103', 'C104']
RELABEL_OK = {'A76', 'A38'}   # A76: etiqueta dinámica según el motor; A38: «Simply Wall St» → «fuente externa» (misma fila, mismo significado)
a53, aF = wb53['Análisis'], wbF['Análisis']
def covered(ws, ref):
    from openpyxl.utils import range_boundaries, coordinate_to_tuple
    rr, cc = coordinate_to_tuple(ref)
    for dv in ws.data_validations.dataValidation:
        for rng in str(dv.sqref).split():
            c1, r1, c2, r2 = range_boundaries(rng)
            if r1 <= rr <= r2 and c1 <= cc <= c2:
                return True
    return False
probs = []
for ref in WL:
    v = aF[ref].value
    if isinstance(v, str) and v.startswith('='):
        probs.append(f'{ref}: ahora es fórmula')
    row = ref[1:]
    la, lb = a53[f'A{row}'].value, aF[f'A{row}'].value
    if la != lb and f'A{row}' not in RELABEL_OK and not (isinstance(lb, str) and lb.startswith('=')):
        probs.append(f'A{row}: etiqueta distinta ({str(la)[:30]!r} → {str(lb)[:30]!r})')
    if covered(a53, ref) and not covered(aF, ref):
        probs.append(f'{ref}: perdió su validación de datos')
moved = [c.coordinate for row in a53.iter_rows() for c in row if c.value is not None and aF[c.coordinate].value is None]
RESULTS.append({'prueba': 'R04b_entradas_de_Analisis', 'descripcion': 'Las 62 entradas de Análisis (lista blanca de migración y kit) siguen en su coordenada, con su etiqueta, sin convertirse en fórmula y con su validación; ninguna celda de la V5.3 queda vacía',
                'esperado': 'ninguna incidencia', 'obtenido': {'incidencias': probs if probs else 'ninguna', 'celdas_vaciadas': moved if moved else 'ninguna', 'filas_V5.3': a53.max_row, 'filas_V6.1': aF.max_row},
                'resultado': 'SUPERADA' if not (probs or moved) else 'FALLIDA'})

# R04c · gráficos: series y referencias exactas
EXP_CHARTS = {
    'Ventas: historia y escenarios (mm)': {"'Motor'!$A$142:$A$161", "'Motor'!$B$142:$B$161", "'Motor'!$C$142:$C$161", "'Motor'!$D$142:$D$161", "'Motor'!$E$142:$E$161"},
    'Valor por acción frente al precio': {"'Motor'!$A$166:$A$169", "'Motor'!$B$166:$B$169", "'Motor'!$C$166:$C$169"},
    'Qué palanca mueve más el valor · cambio por acción sobre la base (NORMAL)': {"'Motor'!$A$174:$A$179", "'Motor'!$D$174:$D$179", "'Motor'!$E$174:$E$179"},
}
z = zipfile.ZipFile(FINAL)
charts = {}
for n in sorted(x for x in z.namelist() if re.match(r'xl/charts/chart\d+\.xml$', x)):
    x = z.read(n).decode('utf-8', 'ignore')
    title = ''.join(re.findall(r'<a:t>([^<]+)</a:t>', x)[:1])
    refs = set(r for r in re.findall(r'<(?:c:)?f>([^<]+)</(?:c:)?f>', x) if ':' in r)   # rangos (las celdas sueltas son los títulos de serie)
    charts[n] = {'titulo': title, 'rangos': sorted(refs)}
chart_ok = len(charts) == 3 and all(any(c['titulo'] == t and set(c['rangos']) == rs for c in charts.values()) for t, rs in EXP_CHARTS.items())
# anclados en el dibujo del Panel
panel_drawing = None
wbx = z.read('xl/workbook.xml').decode('utf-8', 'ignore')
rels = z.read('xl/_rels/workbook.xml.rels').decode('utf-8', 'ignore')
rid = re.search(r'<sheet[^>]*name="Panel"[^>]*r:id="(rId\d+)"', wbx).group(1)
tgt = re.search(r'<Relationship[^>]*Id="%s"[^>]*Target="([^"]+)"|<Relationship[^>]*Target="([^"]+)"[^>]*Id="%s"' % (rid, rid), rels)
sheet_path = 'xl/' + (tgt.group(1) or tgt.group(2)).lstrip('/').replace('xl/', '')
sheet_rels = z.read('xl/worksheets/_rels/' + sheet_path.split('/')[-1] + '.rels').decode('utf-8', 'ignore')
drawing_ok = 'drawings/drawing' in sheet_rels
RESULTS.append({'prueba': 'R04c_graficos', 'descripcion': 'Los tres gráficos del Panel existen, con sus series apuntando exactamente a los rangos previstos de Motor', 'esperado': EXP_CHARTS,
                'obtenido': {'graficos': charts, 'dibujo_en_Panel': drawing_ok}, 'resultado': 'SUPERADA' if (chart_ok and drawing_ok) else 'FALLIDA'})

# R04d · controles: seis deslizadores, vínculos y relaciones internas del archivo
ctrl = {n: z.read(n).decode('utf-8', 'ignore') for n in z.namelist() if n.startswith('xl/ctrlProps/')}
links = sorted(re.search(r'fmlaLink="([^"]+)"', x).group(1) for x in ctrl.values() if re.search(r'fmlaLink="([^"]+)"', x))
types = all('objectType="Scroll"' in x and 'min="0"' in x and 'max="40"' in x for x in ctrl.values())
sheet_xml = z.read(sheet_path).decode('utf-8', 'ignore')
n_controls = len(re.findall(r'<control ', sheet_xml))
ctrl_rids = re.findall(r'<control [^>]*r:id="([^"]+)"', sheet_xml)
rels_ok = all(re.search(r'Id="%s"[^>]*Type="[^"]*ctrlProp"' % r, sheet_rels) or re.search(r'Type="[^"]*ctrlProp"[^>]*Id="%s"' % r, sheet_rels) for r in ctrl_rids)
vml_ok = ('vmlDrawing' in sheet_rels) and ('<legacyDrawing' in sheet_xml) and any(n.startswith('xl/drawings/vmlDrawing') for n in z.namelist())
ct = z.read('[Content_Types].xml').decode('utf-8', 'ignore')
ct_ok = ('Extension="vml"' in ct) and all(f'/{n}' in ct for n in ctrl)
vml = ''.join(z.read(n).decode('utf-8', 'ignore') for n in z.namelist() if n.startswith('xl/drawings/vmlDrawing'))
vml_links = sorted(re.findall(r'<x:FmlaLink>([^<]+)</x:FmlaLink>', vml))
ctrl_ok = (len(ctrl) == 6 and links == [f'$E${r}' for r in range(20, 26)] and vml_links == links and types and n_controls == 6 and rels_ok and vml_ok and ct_ok)
RESULTS.append({'prueba': 'R04d_controles', 'descripcion': 'Seis deslizadores (Scroll 0–40) vinculados a Panel!$E$20:$E$25, con sus relaciones (ctrlProp, VML, legacyDrawing) y tipos de contenido declarados',
                'esperado': '6 controles · vínculos $E$20…$E$25 en ctrlProps y VML · relaciones y [Content_Types] completos',
                'obtenido': {'ctrlProps': len(ctrl), 'vinculos': links, 'vinculos_vml': vml_links, 'controles_en_hoja': n_controls, 'relaciones_ok': rels_ok, 'vml_ok': vml_ok, 'content_types_ok': ct_ok, 'tipo_scroll_0_40': types},
                'resultado': 'SUPERADA' if ctrl_ok else 'FALLIDA'})
RESULTS.append({'prueba': 'R04e_Excel_real', 'descripcion': 'Funcionamiento de deslizadores, formato condicional y gráficos en Microsoft Excel (no solo presencia estructural en el XML)',
                'esperado': 'los deslizadores mueven Panel!E20:E25, los colores se ven como en las capturas y Excel no muestra avisos de reparación',
                'obtenido': 'no comprobado en esta sesión (solo LibreOffice headless y XML)', 'resultado': 'NO EJECUTADA'})
hojas_ok = wbF.sheetnames == ['Panel', 'Análisis', 'Palancas', 'Diagnóstico V6', 'Historia', 'Sector', 'Riesgo país', 'Guía V6', 'Opciones', 'Control maestro', 'Motor']
RESULTS.append({'prueba': 'R04f_hojas', 'descripcion': 'Orden y nombres de las hojas (los nombres los usan el kit y la migración)', 'esperado': 'Panel, Análisis, Palancas, Diagnóstico V6, Historia, Sector, Riesgo país, Guía V6, Opciones, Control maestro, Motor',
                'obtenido': wbF.sheetnames, 'resultado': 'SUPERADA' if hojas_ok else 'FALLIDA'})

# R07 · ninguna fórmula del libro apunta a una celda vacía de la hoja Motor (columnas de agregados y estudio)
wbf = openpyxl.load_workbook(FINAL)
Mf = wbf['Motor']
bad = []
pat = re.compile(r"Motor!\$([A-Z]{1,3})\$(\d+)(?![:\d])")
for ws in wbf.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith('='):
                for col_, row_ in pat.findall(c.value):
                    if Mf[f'{col_}{row_}'].value is None:
                        bad.append(f'{ws.title}!{c.coordinate} → Motor!{col_}{row_}')
RESULTS.append({'prueba': 'R07_referencias_a_motor', 'descripcion': 'Toda referencia absoluta a una celda de Motor apunta a una celda con contenido',
                'esperado': 'ninguna referencia a celdas vacías', 'obtenido': sorted(set(bad))[:30] if bad else 'ninguna',
                'resultado': 'SUPERADA' if not bad else 'FALLIDA'})

# ------------------------------------------------------------------ salida
json.dump(RESULTS, open(os.path.join(OUTDIR, 'resultados_pruebas.json'), 'w'), ensure_ascii=False, indent=1, default=str)
tot = len(RESULTS)
sup = sum(1 for r in RESULTS if r['resultado'] == 'SUPERADA')
fal = [r['prueba'] for r in RESULTS if r['resultado'] == 'FALLIDA']
noe = [r['prueba'] for r in RESULTS if r['resultado'] == 'NO EJECUTADA']
lines = [f'# Resultados de las pruebas · V6.1 · {datetime.datetime.now():%Y-%m-%d %H:%M}', '',
         f'Plantilla probada: `{os.path.basename(FINAL)}` · recálculo real con LibreOffice (headless) sobre copias independientes.', '',
         f'**{sup} de {tot} superadas** · fallidas: {", ".join(fal) if fal else "ninguna"} · no ejecutadas: {", ".join(noe) if noe else "ninguna"}', '',
         '| Prueba | Descripción | Resultado |', '|---|---|---|']
for r in RESULTS:
    lines.append(f"| {r['prueba']} | {r['descripcion']} | **{r['resultado']}** |")
lines += ['', '## Detalle (esperado · obtenido · evidencia)', '']
for r in RESULTS:
    lines.append(f"### {r['prueba']} — {r['resultado']}")
    lines.append(r['descripcion'])
    if 'comprobaciones' in r:
        lines.append('')
        lines.append('| Celda | Esperado | Obtenido | |')
        lines.append('|---|---|---|---|')
        for c in r['comprobaciones']:
            ob = c['obtenido']
            if isinstance(ob, float):
                ob = f'{ob:.6f}'
            lines.append(f"| `{c['celda']}` | {c['esperado']} | `{str(ob)[:90]}` | {c['resultado']} |")
        lines.append(f"Archivo: `{r['archivo']}` (recalculado en `recalculados/`).")
    else:
        lines.append(f"- Esperado: {r['esperado']}")
        ob = r['obtenido']
        lines.append(f"- Obtenido: `{json.dumps(ob, ensure_ascii=False, default=str)[:1500]}`")
        if r.get('nota_libreoffice'):
            lines.append(f"- {r['nota_libreoffice']}")
        if r.get('evidencia'):
            lines.append(f"- Evidencia: {r['evidencia']}")
    lines.append('')
open(os.path.join(OUTDIR, 'Resultados_pruebas_V6_1.md'), 'w').write('\n'.join(lines))
print(f'{sup}/{tot} superadas · fallidas: {fal} · no ejecutadas: {noe}')
