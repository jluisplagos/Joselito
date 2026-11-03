# -*- coding: utf-8 -*-
"""Rellena la plantilla V6 con la Empresa X (inventada) y calcula en Python el valor esperado con las mismas fórmulas."""
import sys, json, datetime
import openpyxl

SRC, OUT, MOTOR = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else 'A')
wb = openpyxl.load_workbook(SRC)
A, H, E = wb['Análisis'], wb['Historia'], wb['Palancas']

years = list(range(2016, 2026))
V = [1000 / 1.08 ** (9 - i) for i in range(10)]
rows = {}
for i, y in enumerate(years):
    col = chr(ord('C') + i)
    v = V[i]
    ebit, da, tax = 0.20 * v, 0.04 * v, 0.25
    dwc = 0.01 * v
    capex = da + 0.04 * v
    sbc = 0.005 * v
    intfin = 0.008 * v
    lease = 0.004 * v
    cfo = ebit * (1 - tax) + da - dwc + sbc - 0.002 * v
    ni = (ebit - 0.01 * v) * (1 - tax)
    vals = {5: y, 6: v, 7: ebit, 8: da, 9: ni, 10: tax, 11: cfo, 12: capex, 13: 0, 14: dwc, 15: 0.01 * v, 16: intfin,
            17: lease, 18: sbc, 19: 0.03 * v, 20: 100, 21: 0.6 * v, 22: 0.2 * v, 23: 0.05 * v, 24: 0.1 * v, 25: 0, 26: 0}
    for r, x in vals.items():
        H[f'{col}{r}'] = x
    rows[y] = vals
H['C57'] = 3
last3 = [rows[y] for y in (2023, 2024, 2025)]
avg = lambda k: sum(r[k] for r in last3) / 3
A['B3'] = 'Empresa X (inventada)'; A['D3'] = 'EMPX'; A['D4'] = datetime.date(2026, 10, 20)
A['C11'] = 'Sí'; A['C12'] = 'Sí'; A['C13'] = 'Sí'
A['C37'] = 22.0
A['C41'] = 2200.0
A['C46'] = avg(11); A['C47'] = avg(12); A['C48'] = avg(16); A['C49'] = avg(17); A['C50'] = avg(18); A['C51'] = 'Sí'
A['C53'] = rows[2025][24]; A['C54'] = rows[2025][22]; A['C55'] = 100; A['C56'] = 0.09; A['C57'] = 0.03
A['C62'] = {'A': 'Sí', 'B': 'No · financiación cambia mucho', 'C': 'No · banco, aseguradora o regulada'}[MOTOR]
A['B65'] = 'El viento de cola se frena'; A['C65'] = 'Sigue como los últimos 5 años'; A['D65'] = 'Gana cuota: el moat se ensancha'
A['B68'] = 0.02; A['C68'] = 0.025; A['D68'] = 0.03
A['B69'] = 0.2; A['C69'] = 0.6; A['D69'] = 0.2
A['C76'] = 0
E['C45'] = datetime.date(2026, 10, 20); E['C46'] = datetime.date(2026, 9, 30); E['C48'] = 'EUR'
wb['Control maestro']['H4'] = 'EUR'
E['C5'] = 'Madura en crecimiento'; E['C6'] = 'Ninguno'; E['C7'] = 'Machinery'; E['C8'] = 'Último año'; E['C9'] = 'No'
P = {'B': (0.03, 0.18, 1.2, 0.10), 'C': (0.08, 0.22, 1.5, 0.15), 'D': (0.12, 0.25, 2.0, 0.20)}
if MOTOR == 'C':
    P = {'B': (0.03, 0.10, None, 0.10), 'C': (0.06, 0.14, None, 0.13), 'D': (0.08, 0.16, None, 0.15)}
for col, (g, m, s, ro) in P.items():
    E[f'{col}14'] = g; E[f'{col}15'] = m; E[f'{col}16'] = s if s else 'n/a'; E[f'{col}18'] = ro

# cualitativo (para que el ejemplo quede COMPLETO)
A['C14'] = 'Calidad a precio razonable'
for ref in ('C17', 'C18', 'C19', 'C25', 'C34'): A[ref] = 'Sí'
A['C31'] = 'No'; A['C20'] = 'Incert. alta + riesgo bajo'; A['C24'] = 0.18; A['C26'] = 1.1; A['C27'] = 'Estable'; A['C28'] = 'Estable'
A['C32'] = 0.12; A['C33'] = 0.8
A['C93'] = 'Sí'; A['C97'] = 'Neutral'; A['C98'] = 'Buena'; A['C103'] = 'No'; A['C104'] = 0.04
A['B66'] = 'Pierde cuota y el margen baja.'; A['C66'] = 'Sigue creciendo al 8 % con el margen actual.'; A['D66'] = 'Gana cuota y mejora el margen.'
A['B101'] = 'Negocio sencillo, con caja y sin deuda relevante, a un precio razonable.'
A['B102'] = 'Que el crecimiento se frene y el margen no suba.'
for i, t in enumerate(('Las ventas crecen al menos un 5 % anual.', 'El margen operativo se mantiene por encima del 18 %.', 'No emite acciones.')):
    E[f'A{38 + i}'] = t
for i, (p, w) in enumerate([('Germany', 0.6), ('Brazil', 0.3), ('United States', 0.1)]):
    E[f'A{28 + i}'] = p; E[f'B{28 + i}'] = w
wb.save(OUT)

# ---------- réplica en Python de las fórmulas del motor
c52 = A['C46'].value - A['C47'].value - A['C48'].value - A['C49'].value - A['C50'].value
N = 3
yrs = years[-N:]
f = ((sum(rows[y][7] * (1 - rows[y][10]) for y in yrs) - sum(rows[y][12] - rows[y][8] + rows[y][14] for y in yrs)) / N - c52) \
    / (sum(rows[y][6] for y in yrs) / N)
V0, m0, tau = rows[2025][6], 0.20, 0.25
debt = rows[2025][22] + rows[2025][23]
i_d = rows[2025][15] / ((rows[2024][22] + rows[2024][23] + rows[2025][22] + rows[2025][23]) / 2)
r = 0.09
rop = (r * 2200 + i_d * (1 - tau) * debt) / (2200 + debt)
claims = debt - rows[2025][24]
B0, ROE0 = rows[2025][21], rows[2025][9] / rows[2025][21]


def value(g1, mT, s2c, ginf, roic, motor=MOTOR):
    L = [B0 if motor == 'C' else V0]
    m0_ = ROE0 if motor == 'C' else m0
    d = rop if motor == 'B' else r
    tau_ = 0 if motor == 'C' else tau
    f_ = f if motor == 'A' else 0
    adj = -claims if motor == 'B' else 0
    flows = []
    for t in range(1, 11):
        g = g1 if t <= 5 else g1 - (g1 - ginf) * (t - 5) / 5
        L.append(L[-1] * (1 + g))
        m = m0_ + (mT - m0_) * min(t, 5) / 5
        if motor == 'C':
            flows.append(L[t - 1] * m - (L[t] - L[t - 1]))
        else:
            flows.append(L[t] * (m * (1 - tau_) - f_) - (L[t] - L[t - 1]) / s2c)
    pv = sum(x / (1 + d) ** t for t, x in enumerate(flows, 1))
    if motor == 'C':
        f11 = L[10] * (roic - ginf)
    else:
        f11 = L[10] * (1 + ginf) * (mT * (1 - tau_) * (1 - ginf / roic) - f_)
    tv = f11 / (d - ginf) / (1 + d) ** 10
    return (pv + tv + adj) / 100


res = {}
for col, gi in zip('BCD', (0.02, 0.025, 0.03)):
    g, m, s, ro = P[col]
    res[col] = value(g, m, s or 1, gi, ro)
res['pond'] = 0.2 * res['B'] + 0.6 * res['C'] + 0.2 * res['D']
res['f'] = f
res['c52'] = c52
json.dump(res, open(OUT + '.expected.json', 'w'), indent=1)
print(json.dumps(res, indent=1))
