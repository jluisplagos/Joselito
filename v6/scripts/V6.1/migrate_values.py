# -*- coding: utf-8 -*-
"""Migra una hoja terminada con la V5.3 a la plantilla V6.1 copiando SOLO una lista explícita de celdas.

Ninguna celda cambia de sitio. No se copian etiquetas, notas ni fórmulas: solo los datos de fase 1, el juicio del
inversor y la trazabilidad de Control maestro. Al final escribe una conciliación (JSON) con cada valor no vacío y
sin fórmula del archivo original clasificado como CONSERVADO, EXCLUIDO (etiqueta o texto fijo de la plantilla) o
TRANSFORMADO (en V6.1 esa celda es ahora una fórmula).

Uso: python3 migrate_values.py origen_v53.xlsx Plantilla_V6.1.xlsx salida.xlsx [conciliacion.json]
"""
import sys, json
import openpyxl
from openpyxl.utils import range_boundaries, get_column_letter

SRC, TPL, OUT = sys.argv[1:4]
REC = sys.argv[4] if len(sys.argv) > 4 else OUT + '.conciliacion.json'

# ---------------------------------------------------------------- lista blanca
WHITELIST = {
    'Análisis': [
        'B3', 'D3', 'B4', 'D4',                                  # identificación
        'C11:C14', 'C17:C20', 'C24:C28', 'C31:C34',             # etapas 0, 1 y 2 («Tu dato»)
        'C37', 'C38', 'C40', 'C41', 'C42',                       # precio, capitalización, caja, deuda
        'C46:C51', 'C53:C57',                                    # datos base del DCF (C52 es fórmula)
        'C60', 'C61', 'C62',                                     # decisiones del motor
        'B65:D66', 'B68:D69',                                    # escenarios: nombre, en tus palabras, g, probabilidad
        'C76', 'C88', 'C93', 'C96:C98', 'B101', 'B102', 'C103', 'C104',
    ],
    'Control maestro': [
        'H4', 'J4', 'L4', 'N4', 'B5', 'D5', 'F5', 'J5', 'L5', 'N5',   # cabecera: moneda, unidad, norma, cierre, mercado, ADR…
        'E17:N82',                                                   # trazabilidad por celda (estado, fuente, URL, nota)
        'C86:N102',                                                  # auditoría del modelo (estado, evidencia, acción)
    ],
}
# Celdas de datos de la V5.3 que en V6.1 son fórmula: su valor no se copia y se registra como TRANSFORMADO.
TRANSFORMED = {'Análisis': ['B67:D67']}


def cells(rng):
    c1, r1, c2, r2 = range_boundaries(rng)
    return {f'{get_column_letter(c)}{r}' for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)}


WL = {k: set().union(*(cells(x) for x in v)) for k, v in WHITELIST.items()}
TR = {k: set().union(*(cells(x) for x in v)) for k, v in TRANSFORMED.items()}

src = openpyxl.load_workbook(SRC)
tpl = openpyxl.load_workbook(TPL)
rec = {'origen': SRC, 'plantilla': TPL, 'conservados': [], 'excluidos': [], 'transformados': [], 'conflictos': []}
for name in WHITELIST:
    if name not in src.sheetnames:
        rec['conflictos'].append(f'hoja {name} no existe en el origen')
        continue
    a, b = src[name], tpl[name]
    for row in a.iter_rows():
        for c in row:
            v = c.value
            if v is None or (isinstance(v, str) and v.startswith('=')):
                continue
            ref = c.coordinate
            entry = {'hoja': name, 'celda': ref, 'valor': v if isinstance(v, (int, float)) else str(v)[:80]}
            if ref in TR.get(name, set()):
                entry['motivo'] = 'en V6.1 es fórmula (calculado)'
                rec['transformados'].append(entry)
                continue
            if ref not in WL[name]:
                entry['motivo'] = 'etiqueta o texto fijo de la plantilla'
                rec['excluidos'].append(entry)
                continue
            tgt = b[ref]
            if isinstance(tgt.value, str) and tgt.value.startswith('='):
                entry['motivo'] = 'la celda destino es fórmula en V6.1'
                rec['conflictos'].append(entry)
                continue
            tgt.value = v
            rec['conservados'].append(entry)
tpl.save(OUT)
tot = sum(len(rec[k]) for k in ('conservados', 'excluidos', 'transformados', 'conflictos'))
rec['resumen'] = {'total_no_formula_origen': tot, 'conservados': len(rec['conservados']), 'excluidos': len(rec['excluidos']),
                  'transformados': len(rec['transformados']), 'conflictos': len(rec['conflictos'])}
json.dump(rec, open(REC, 'w'), ensure_ascii=False, indent=1, default=str)
print('OK', OUT, rec['resumen'])
