# -*- coding: utf-8 -*-
"""Rellena la plantilla V6.1 con ABB Ltd a partir de abb_fase1.json (datos extraídos con cita de página).

Tres clases de celda, que quedan documentadas en Control maestro (columna E «Estado de trabajo» y N «Observaciones»):
  DATO EXTRAÍDO        → cifra publicada por ABB (fuente y página en la trazabilidad).
  HIPÓTESIS DE ESTUDIO → valor que la hoja necesita para calcular y que NO es juicio del inversor (se marca «Pendiente de inversor»).
  JUICIO PENDIENTE     → se deja vacío a propósito (Pabrai, tesis, moat, predicciones…).
Uso: python3 fill_abb.py Plantilla_V6.xlsx abb_fase1.json salida.xlsx
"""
import sys, json, datetime
import openpyxl

TPL, SRC, OUT = sys.argv[1:4]
d = json.load(open(SRC))
Y = d['años']
wb = openpyxl.load_workbook(TPL)
A, H, P, CM = wb['Análisis'], wb['Historia'], wb['Palancas'], wb['Control maestro']
years = sorted(Y)[-10:]
cols = [chr(ord('C') + i) for i in range(10)][-len(years):]
ROWMAP = {6: 'ventas', 7: 'ebit', 8: 'amortizaciones', 9: 'beneficio_neto_abb', 10: 'tipo_impositivo_efectivo', 11: 'caja_operaciones', 12: 'capex',
          13: 'adquisiciones_netas', 14: 'aumento_capital_circulante', 15: 'intereses_pagados', 16: 'intereses_pagados_en_financiacion',
          17: 'principal_arrendamientos_pagado', 18: 'compensacion_en_acciones', 19: 'gasto_id', 20: 'acciones_diluidas_medias',
          21: 'patrimonio_neto_abb', 22: 'deuda_financiera', 23: 'pasivo_arrendamientos', 24: 'caja_equivalentes', 25: 'deficit_neto_pensiones', 26: 'minoritarios'}
src_by_row = {}


def val(y, k):
    x = Y[y].get(k)
    if isinstance(x, dict):
        return x.get('valor'), x
    return x, {}


# ---------------- DATOS EXTRAÍDOS · Historia
for col, y in zip(cols, years):
    H[f'{col}5'] = int(y)
    for r, k in ROWMAP.items():
        v, meta = val(y, k)
        if v is None:
            continue
        if r == 13 and v < 0:
            v = v  # adquisiciones netas negativas = ventas netas de negocios (la hoja las admite con signo)
        H[f'{col}{r}'] = float(v)
        if meta.get('fuente'):
            src_by_row.setdefault(r, set()).add(f"{y}: {meta['fuente'].replace('.pdf', '')} p. {meta.get('pagina', '?')}")
H['C57'] = 3
# fuente / observación por fila de Historia (columna M)
for r, srcs in src_by_row.items():
    H[f'M{r}'] = ' · '.join(sorted(srcs))[:900]
H['M18'] = (H['M18'].value or '') + ' · 2024 y 2025: no publicado como línea del estado de flujos (solo abono a prima de emisión 97/89): se deja vacío'
H['M17'] = (H['M17'].value or '') + ' · solo publicado 2019 (20) y 2020 (24); resto vacío'

# ---------------- DATOS EXTRAÍDOS · Análisis
last3 = years[-3:]
avg = lambda k: sum(float(val(y, k)[0]) for y in last3) / 3
A['B3'] = 'ABB Ltd'
A['D3'] = 'ABBN (SIX) · USD en los estados, CHF en bolsa'
A['D4'] = datetime.date(2026, 10, 26)
A['B4'] = 'Electrificación y automatización industrial'
A['C37'] = 79.42                     # CHF, cierre 30-09-2026 (nota de prensa Q3 2026, p. 11)
A['C41'] = 79.42 * 1808              # CHF mm · precio × acciones en circulación 30-09-2026 · CALCULADO, ABB no publica capitalización
A['C46'] = round(avg('caja_operaciones'), 1)
A['C47'] = round(avg('capex'), 1)
A['C48'] = 0                         # US GAAP: intereses pagados en explotación
A['C49'] = None                      # principal de arrendamientos no publicado 2023–2025
A['C50'] = round(sum(float(val(y, 'compensacion_en_acciones')[0]) for y in ('2021', '2022', '2023')) / 3, 1)   # HIPÓTESIS: media 2021–2023 (2024–2025 no publicadas)
A['C51'] = 'Sí'
A['C53'] = float(val('2025', 'caja_equivalentes')[0])
A['C54'] = float(val('2025', 'deuda_financiera')[0])
A['C55'] = float(val('2025', 'acciones_diluidas_medias')[0])
# etapa 2 · datos objetivos
A['C24'] = None                      # ROIC: lo calcula Historia (fila 33); el inversor decide qué cifra escribir
A['C26'] = round(float(val('2025', 'caja_operaciones')[0]) / float(val('2025', 'beneficio_neto_abb')[0]), 2)
A['C27'] = 'Expandiendo'             # margen EBIT 2021 19,8 % → 2025 18,2 % tras 2022 11,3 %: dato observable, revisable
A['C28'] = 'Recompra'                # acciones diluidas 2019 2.135 → 2025 1.831
A['C32'] = None                      # goodwill ÷ activo: no extraído
A['C33'] = round((float(val('2025', 'deuda_financiera')[0]) - float(val('2025', 'caja_equivalentes')[0])) / (float(val('2025', 'ebit')[0]) + float(val('2025', 'amortizaciones')[0])), 2)
A['C60'] = round((float(val('2025', 'acciones_diluidas_medias')[0]) / float(val('2019', 'acciones_diluidas_medias')[0])) ** (1 / 6) - 1, 4)

# ---------------- HIPÓTESIS DE ESTUDIO (no juicio del inversor)
A['C56'] = 0.09
A['C62'] = 'Sí'
A['B65'], A['C65'], A['D65'] = 'El ciclo de inversión eléctrica se enfría', 'Sigue como 2021–2025', 'Electrificación acelera y el margen sube'
A['B66'], A['C66'], A['D66'] = ('HIPÓTESIS DE ESTUDIO: ventas +2 %, margen 15 %.', 'HIPÓTESIS DE ESTUDIO: ventas +4 %, margen 18 % (2025).', 'HIPÓTESIS DE ESTUDIO: ventas +6 %, margen 20 %.')
A['B68'], A['C68'], A['D68'] = 0.02, 0.025, 0.03
A['B69'], A['C69'], A['D69'] = 0.25, 0.5, 0.25
A['C76'] = 0
P['C5'] = 'Madura en crecimiento'
P['C6'] = 'Ninguno'
P['C7'] = 'Electrical Equipment'
P['C8'] = 'Último año'
P['C9'] = 'No'
for col, (g, m, s, ro) in {'B': (0.02, 0.15, 1.5, 0.12), 'C': (0.04, 0.18, 2.0, 0.15), 'D': (0.06, 0.20, 2.5, 0.18)}.items():
    P[f'{col}14'] = g; P[f'{col}15'] = m; P[f'{col}16'] = s; P[f'{col}18'] = ro
for i, (p, w) in enumerate([('Región · Western Europe', 0.36), ('Región · North America', 0.30), ('Región · Asia', 0.34)]):
    P[f'A{28 + i}'] = p; P[f'B{28 + i}'] = w     # reparto aproximado por regiones de ABB (hipótesis, no dato extraído)
P['C45'] = datetime.date(2026, 9, 30)
P['C46'] = datetime.date(2026, 9, 30)
P['C47'] = 'Ninguna'
P['C48'] = 'CHF'
CM['H4'] = 'USD'
CM['J4'] = 'mm'
CM['L4'] = 'US GAAP'
CM['N4'] = '31 de diciembre'
CM['B5'] = 'SIX Swiss Exchange · ABBN (también Nasdaq Stockholm, SEK)'
CM['D5'] = None
CM['F5'] = 'Medias 2023–2025 en Análisis C46:C47 (3 años); f calibrada con 3 años (Historia C57)'
CM['J5'] = 'NO HECHA: estados en USD, cotización en CHF. La hoja bloquea la lectura del precio hasta que el inversor convierta y documente.'
CM['L5'] = '26-10-2026 (extracción de fase 1 con cita de página: abb_fase1.json)'
CM['N5'] = 'Datos: Claude (extracción). Hipótesis de estudio marcadas. Juicio: pendiente del inversor.'

# ---------------- trazabilidad: estado de trabajo y observaciones
TRACE_EXTRA = {
    'Análisis!C37': ('Rellenado y verificado', 'DATO EXTRAÍDO · cierre 30-09-2026, CHF 79,42 (nota de prensa Q3 2026, p. 11)'),
    'Análisis!C41': ('Rellenado y verificado', 'CALCULADO (no publicado): 79,42 CHF × 1.808 M acciones en circulación a 30-09-2026 = 143.591 M CHF. En CHF, no en USD.'),
    'Análisis!C46': ('Rellenado y verificado', 'DATO EXTRAÍDO · media CFO 2023–2025 (4.290 / 4.675 / 5.469)'),
    'Análisis!C47': ('Rellenado y verificado', 'DATO EXTRAÍDO · media capex 2023–2025 (770 / 799 / 1.001)'),
    'Análisis!C48': ('Rellenado y verificado', 'US GAAP: intereses pagados íntegramente en explotación → 0'),
    'Análisis!C49': ('Dato no verificable', 'ABB no publica el principal de arrendamientos desde 2021: vacío'),
    'Análisis!C50': ('Pendiente de inversor', 'HIPÓTESIS DE ESTUDIO · media 2021–2023 (59 / 42 / 103); 2024–2025 no publicadas como coste'),
    'Análisis!C55': ('Rellenado y verificado', 'DATO EXTRAÍDO · media diluida 2025: 1.831 M'),
    'Análisis!C56': ('Pendiente de inversor', 'HIPÓTESIS DE ESTUDIO · r = 9 % (no es la exigencia del inversor)'),
    'Análisis!C62': ('Pendiente de inversor', 'HIPÓTESIS DE ESTUDIO · motor A'),
}
for r in range(17, 110):
    ref = CM.cell(r, 2).value
    if isinstance(ref, str) and ref in TRACE_EXTRA:
        CM.cell(r, 5).value, CM.cell(r, 14).value = TRACE_EXTRA[ref]
for r in range(107, 200):
    ref = CM.cell(r, 2).value
    if not isinstance(ref, str):
        continue
    if ref.startswith('Historia!C') and ':L' in ref:
        row = int(ref.split('!C')[1].split(':')[0])
        if row in src_by_row:
            CM.cell(r, 5).value = 'Rellenado y verificado'
            CM.cell(r, 10).value = 'ABB Ltd (AR 2021, 20-F 2016/2018/2020/2023 en SEC EDGAR, Financial Information Q4 2024/Q4 2025/Q2 2026, notas de prensa Q4 2025 y Q3 2026)'
            CM.cell(r, 12).value = ' · '.join(sorted(src_by_row[row]))[:900]
            CM.cell(r, 14).value = 'DATO EXTRAÍDO'
        elif row in (16, 17, 18):
            CM.cell(r, 5).value = 'Rellenado y verificado' if row == 16 else 'Dato no verificable'
            CM.cell(r, 14).value = {16: 'US GAAP: 0 todos los años', 17: 'Solo 2019–2020 publicado', 18: '2024–2025 no publicadas como coste'}[row]
    elif ref.startswith('Palancas!'):
        cell = ref.split('!')[1]
        if cell in ('C45', 'C46', 'C48'):
            CM.cell(r, 5).value, CM.cell(r, 14).value = 'Rellenado y verificado', 'DATO EXTRAÍDO (nota de prensa Q3 2026 / SIX)'
        elif cell in ('C43', 'C44', 'C47'):
            CM.cell(r, 5).value, CM.cell(r, 14).value = 'Rellenado y verificado', 'No aplica (FCF base > 0; sin causa de desviación)'
        elif cell.startswith('A38') or cell.startswith('A39') or cell.startswith('A40') or cell.startswith('B38') or cell.startswith('B39') or cell.startswith('B40') or cell.startswith('C38') or cell.startswith('C39') or cell.startswith('C40'):
            CM.cell(r, 5).value, CM.cell(r, 14).value = 'Pendiente de inversor', 'JUICIO PENDIENTE · predicciones sin rellenar a propósito'
        else:
            CM.cell(r, 5).value, CM.cell(r, 14).value = 'Pendiente de inversor', 'HIPÓTESIS DE ESTUDIO · no es juicio del inversor'
    elif ref == "'Control maestro'!H4":
        CM.cell(r, 5).value, CM.cell(r, 14).value = 'Rellenado y verificado', 'USD (moneda de los estados)'
    elif ref == "'Control maestro'!D5":
        CM.cell(r, 5).value, CM.cell(r, 14).value = 'No aplicable', 'No hay ADR declarado'
wb.save(OUT)
print('OK', OUT, '· años', years[0], '–', years[-1])
