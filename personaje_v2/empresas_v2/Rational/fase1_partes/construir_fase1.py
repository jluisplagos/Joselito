"""Construye empresas_v2/Rational/fase1_v63.json desde fase1_partes/AR_*.json (kEUR → mm), aplicando y declarando las
reexpresiones y convenciones. Cada valor lleva fuente (informe y página)."""
import json, re, sys
BASE = sys.argv[1]
A = {y: json.load(open(f"{BASE}/fase1_partes/AR_{y}.json")) for y in range(2016, 2026)}
C = json.load(open(f"{BASE}/fase1_partes/consolidado.json"))
T, COMP = C["tabla"], C["comparativos"]
Y = list(range(2016, 2026))
def pg(y, k, cual="actual"):
    e = A[y]["partidas"].get(k) or {}
    for cand in (e.get(cual), e.get(f"componentes_{cual}")):
        if isinstance(cand, dict) and cand.get("pagina"): return cand["pagina"]
        if isinstance(cand, dict) and isinstance(cand.get("componentes"), list) and cand["componentes"]: return cand["componentes"][0]["pagina"]
        if isinstance(cand, list) and cand: return cand[0].get("pagina")
    return None
def serie(k, abs_=True, reexp=None, fijos=None, notas=None):
    vals, fu = [], []
    for y in Y:
        v, src = T[k].get(str(y)), f"AR{y} p.{pg(y, k)}"
        if reexp and y in reexp:
            v = COMP[k][str(y)]; src = f"AR{y+1} p.{pg(y+1, k, 'anterior')} (reexpresado)"
        if fijos and y in fijos:
            v, src = fijos[y]
        if v is not None:
            v = abs(v) if abs_ else v
            v = round(v / 1000, 3)
        vals.append(v); fu.append(src)
    return vals, fu
H = {}
def poner(k, vals, fu, nota=None):
    H[k] = {"valores": vals, "fuente": "Rational AG, Annual Report: " + "; ".join(f"{y} {s}" for y, s in zip(Y, fu)), "pagina": None, "nota": nota}
poner("ventas", *serie("ventas"))
poner("ebit", *serie("ebit"), nota="EBIT de la cuenta de resultados (Operating result).")
poner("da", *serie("da"), nota="Estado de flujos. Salto en 2019 por IFRS 16 (amortización del derecho de uso).")
poner("beneficio_neto", *serie("beneficio_neto", reexp={2023}), nota="Sin minoritarios: todo atribuible. 2023 reexpresado en AR2024 (IAS 8, activo por impuesto diferido en Suiza).")
imp, fi = serie("impuestos", reexp={2023}); bai, fb = serie("bai")
H["tipo_impositivo"] = {"valores": [round(i / b, 4) for i, b in zip(imp, bai)], "fuente": "Income taxes ÷ Earnings before taxes; " + "; ".join(f"{y} {a} / {b}" for y, a, b in zip(Y, fi, fb)), "pagina": None, "nota": "Impuesto 2023 reexpresado (AR2024)."}
poner("cfo", *serie("cfo", reexp={2021}), nota="2021 reexpresado en AR2022 (IAS 8.14: intereses pagados).")
poner("capex", *serie("capex"), nota="Pagos por inmovilizado material e intangible (positivo).")
poner("adquisiciones", [0.0]*10, ["sin línea de compra/venta de negocios en el estado de flujos"]*10, nota="0: ningún informe trae línea de adquisiciones de negocios.")
# circulante: aumento = -(efecto en caja de las 4 líneas: inventarios, cuentas a cobrar y otros activos, provisiones, cuentas a pagar y otros pasivos)
vc, fc = [], []
for y in Y:
    v = T["circulante"][str(y)]; s = f"AR{y} p.{C['fuentes']['circulante'][str(y)][0]}"
    if y == 2021: v = COMP["circulante"]["2021"]; s = "AR2022 p.38 (reexpresado)"
    vc.append(round(v / 1000, 3)); fc.append(s)
poner("circulante", vc, fc, nota="Convención del ejercicio: −(variación de inventarios + cuentas a cobrar y otros activos + provisiones + cuentas a pagar y otros pasivos) del estado de flujos; excluye impuestos pagados, intereses y otros no monetarios. 2021 reexpresado (AR2022).")
poner("intereses", *serie("intereses", reexp={2021}), nota="Interest paid; Rational lo presenta en financiación. 2021 reexpresado (AR2022: incluye intereses de arrendamiento).")
poner("intereses_financiacion", *serie("intereses_financiacion", reexp={2021}), nota="Igual que la fila 15: todo el interés pagado figura en financiación.")
v, f = serie("arrendamientos_principal", fijos={y: (0.0, "antes de IFRS 16: sin pagos de pasivos por arrendamiento") for y in (2016, 2017, 2018)})
poner("arrendamientos_principal", v, f, nota="Payments for lease liabilities (desde 2019, IFRS 16, sin reexpresar 2018). En 2020–2021 la línea incluye intereses del arrendamiento.")
poner("sbc", [0.0]*10, [f"AR{y}: sin acuerdos de pagos basados en acciones (nota de partes vinculadas/remuneración)" for y in Y], nota="0: los diez informes dicen que no hubo acuerdos de pagos basados en acciones; el plan de opciones de 2000 se liquidó en efectivo.")
v, f = serie("id", fijos={2024: (65959.0, "AR2025 p.102 (gasto en cuenta de resultados)")})
poner("id", v, f, nota="Gasto de I+D de la cuenta de resultados (sin la parte capitalizada, pequeña: 1,0 mm en 2024).")
poner("acciones_diluidas", [11.37]*10, [f"AR{y} p.{pg(y,'acciones_diluidas')}" for y in Y], nota="11.370.000 acciones; básicas = diluidas.")
poner("patrimonio", *serie("patrimonio", reexp={2023}), nota="2023 reexpresado en AR2024 (IAS 8).")
v, f = serie("deuda", fijos={2025: (0.0, "AR2025 p.130 (nota 18: sin deudas con bancos)"), 2024: (0.0, "AR2024 p.19 (Financial debt –)")})
poner("deuda", v, f, nota="Deudas con bancos / Financial debt, corriente + no corriente, sin arrendamientos. Sumas de componentes impresos.")
v, f = serie("arrendamientos", fijos={y: (0.0, "antes de IFRS 16: sin pasivo por arrendamiento en balance") for y in (2016, 2017, 2018)})
poner("arrendamientos", v, f, nota="Lease liabilities corriente + no corriente (sumas de componentes impresos). 0 antes de 2019: los arrendamientos operativos no estaban en balance (discontinuidad en el capital invertido).")
cj, fj = [], []
for y in Y:
    c = T["caja"][str(y)]; o = T["otros_activos_financieros"][str(y)]; so = f"AR{y} p.{pg(y,'otros_activos_financieros')}"
    if y == 2017: o = COMP["otros_activos_financieros"]["2017"]; so = "AR2018 p.71 (reclasificado)"
    if y in (2023, 2024): o = {2023: 267634.0, 2024: 350002.0}[y]; so = {2023: "AR2023 p.37", 2024: "AR2025 p.103"}[y]
    cj.append(round((c + o) / 1000, 3)); fj.append(f"caja AR{y} p.{pg(y,'caja')} + otros activos financieros corrientes {so}")
poner("caja", cj, fj, nota="Convención del ejercicio: Cash and cash equivalents + Other financial assets corrientes (depósitos a plazo y otras inversiones financieras líquidas, con derivados menores). Rational mantiene buena parte de su liquidez en depósitos a más de tres meses. Solo efectivo y equivalentes (mm): " + ", ".join(f"{y} {round(T['caja'][str(y)]/1000,1)}" for y in Y) + ".")
poner("pensiones", *serie("pensiones", reexp={2017}), nota="Provisiones por pensiones (pasivo neto). 2017 según la reclasificación de AR2018.")
poner("minoritarios", [0.0]*10, [f"AR{y}: sin línea de intereses no dominantes" for y in Y], nota="0: ningún balance trae intereses no dominantes.")
for k, d in H.items():
    assert len(d["valores"]) == 10 and all(isinstance(x, (int, float)) for x in d["valores"]), k
f1 = {
 "empresa": "RATIONAL AG", "ticker": "RAA", "fecha_analisis": "2026-11-03",
 "sector_texto": "Equipos de cocina profesional (hornos combinados iCombi e iVario) y posventa",
 "moneda_modelo": "EUR", "unidad": "mm", "norma_contable": "IFRS", "cierre_fiscal": "diciembre", "mercado": "XETRA (Börse Frankfurt)",
 "ratio_adr": None, "sector_damodaran": "Machinery", "anios_fcf_base": 3,
 "historia": {"anios": Y, "partidas": H},
 "precio": {"valor": 630.0, "moneda_cotizacion": "EUR", "fecha": "2026-11-03", "fx": None, "fx_fecha": None,
            "fuente": "boerse.de (Börse Stuttgart), 03-11-2026 09:14:03: 630,00 EUR. Otras referencias vistas: cierre 02-11-2026 638,00 (boerse.de) y XETRA 622,50 (finanzen.net, cierre previo)."},
 "acciones_diluidas": {"valor": 11.37, "fecha": "2025-12-31", "fuente": "Rational AG, Annual Report 2025, beneficio por acción", "pagina": str(pg(2025, "acciones_diluidas"))},
 "capitalizacion": {"valor": round(630.0 * 11.37, 1), "fecha": "2026-11-03", "fuente": "precio × acciones diluidas (630,00 × 11,37 mm)"},
 "tasa_sin_riesgo": {"valor": 0.0329, "fuente": "Bund a 10 años, 3,29 % (dpa-AFX vía ariva.de, 02-11-2026 17:34)"},
 "analisis": {},
 "geografia": [
   {"pais": "Germany", "pct": 0.1026}, {"pais": "Región · Western Europe", "pct": 0.4256, "nota": "Europe (excl. Germany) 536.064 k€; aproximación: incluye algo de Europa del Este"},
   {"pais": "Región · North America", "pct": 0.2417}, {"pais": "Región · Central and South America", "pct": 0.0672},
   {"pais": "Región · Asia", "pct": 0.1074}, {"pais": "Región · Middle East", "pct": 0.0555, "nota": "Rest of the world 69.925 k€ (Australia, Nueva Zelanda, Oriente Medio, África, sin desglose): Oriente Medio como aproximación; convención del ejercicio"}],
 "geografia_fuente": {"fuente": "Rational AG, Annual Report 2025, ventas por región (ubicación del cliente), miles de EUR", "pagina": "117"},
 "_notas": ["Geografía: ventas por ubicación del cliente 2025 (AR2025 p.117). «Europe (excl. Germany)» → Región · Western Europe (incluye algo de Europa del Este: aproximación). «Rest of the world» (Australia, Nueva Zelanda, Oriente Medio, África, sin desglose) → Región · Middle East como aproximación intermedia entre Australia (1,5 %) y África (7,9 %): convención del ejercicio.",
            "Historia construida por la pieza 7 (extracción por año con lectores Sonnet; cada cifra comprobada por script en su página; cada año cruzado con el comparativo del informe siguiente). Reexpresiones aplicadas: 2017 (pensiones, otros activos financieros; AR2018), 2021 (CFO, intereses, circulante; AR2022), 2023 (beneficio, impuestos, patrimonio; AR2024).",
            "Fuente y página de cada año en el campo «fuente» de cada partida."]}
s = sum(g["pct"] for g in f1["geografia"]); assert abs(s - 1) < 0.002, s
json.dump(f1, open(f"{BASE}/fase1_v63.json", "w"), ensure_ascii=False, indent=1)
for k, d in H.items(): print(f"{k:24s}", d["valores"])
print("geo", s)
