"""Consolida fase1_partes/AR_*.json en una tabla por partida/año (kEUR) con fuentes, comprueba cada número contra su página
y cruza el valor de cada año con la columna comparativa del informe siguiente."""
import json, re, sys
BASE = sys.argv[1]
def pages(y):
    t = open(f"{BASE}/texto/AR_{y}.txt", encoding="utf-8").read()
    return {int(m.group(1)): m.group(2) for m in re.finditer(r"\[PDF PAGE (\d+)\]\n(.*?)(?=\[PDF PAGE \d+\]|\Z)", t, re.S)}
def num(s):
    s = s.strip().replace("−", "-").replace("–", "-").replace("—", "-")
    if s in ("-", "", "0"): return 0.0
    neg = s.startswith("(") or s.startswith("-")
    s = s.strip("()-+ ").replace(",", "").replace(".", "") if re.fullmatch(r"[\d.,()\-+ ]+", s) else None
    if s is None or not s.isdigit(): raise ValueError
    return -float(s) if neg else float(s)
def items(e):
    """lista de (impreso, pagina) de una entrada de cualquier forma."""
    out = []
    if e is None: return out
    if isinstance(e, list):
        for i in e: out += items(i)
        return out
    if isinstance(e, dict):
        if isinstance(e.get("componentes"), list):
            return items(e["componentes"])
        if isinstance(e.get("componentes"), str):
            c = e["componentes"]; m = re.search(r"=\s*([\d,]+)\s*$", c)
            if m: return [(m.group(1), e.get("pagina"), "suma declarada: " + c)]
        imp = e.get("impreso")
        if isinstance(imp, str):
            for part in imp.split(" + "):
                out.append((part, e.get("pagina"), e.get("linea")))
        if isinstance(e.get("impreso_no_corriente"), str):
            out.append((e["impreso_no_corriente"], e.get("pagina"), e.get("linea")))
    return out
def entrada(p, cual):
    e = p.get(cual)
    extra = []
    for k in (f"{cual}_corriente", f"{cual}_no_corriente", f"componentes_{cual}"):
        if k in p: extra.append(p[k])
    return [e] + extra
CLAVES = ["ventas","ebit","da","beneficio_neto","impuestos","bai","cfo","capex","adquisiciones","intereses","intereses_financiacion",
          "arrendamientos_principal","sbc","id","acciones_diluidas","patrimonio","deuda","arrendamientos","caja","otros_activos_financieros","pensiones","minoritarios"]
tabla, fuentes, problemas = {}, {}, []
anterior = {}
for y in range(2016, 2026):
    d = json.load(open(f"{BASE}/fase1_partes/AR_{y}.json")); P = pages(y)
    for k in CLAVES + ["circulante"]:
        if k == "circulante":
            cl = d["partidas"]["circulante_lineas"]
            for cual in ("actual", "anterior"):
                lin = cl.get(cual) or []
                v = 0.0; usadas = []
                for l in lin:
                    try: x = num(l["impreso"])
                    except Exception: problemas.append(f"{y} circulante {cual}: no numérico {l['impreso']!r}"); continue
                    norm = lambda s: re.sub(r"\s+", " ", s.replace("−","-").replace("–","-"))
                    if l.get("pagina") and norm(l["impreso"]) not in norm(P.get(int(l["pagina"]), "")):
                        problemas.append(f"{y} circulante {cual}: {l['impreso']} no está en p.{l['pagina']}")
                    v += x; usadas.append(l.get("concepto"))
                val = -v if lin else None   # el estado de flujos da el efecto en caja; aumento del circulante = -efecto
                if cual == "actual": tabla.setdefault(k, {})[y] = val; fuentes.setdefault(k, {})[y] = (lin[0]["pagina"] if lin else None, "; ".join(map(str, usadas)))
                else: anterior.setdefault(k, {})[y-1] = val
            continue
        p = d["partidas"].get(k)
        for cual in ("actual", "anterior"):
            if p is None: v=None; its=[]
            else:
                its = []
                for e in entrada(p, cual): its += items(e)
                v = None
                if its:
                    v = 0.0
                    for imp, pg, lin in its:
                        try: x = num(imp)
                        except Exception: problemas.append(f"{y} {k} {cual}: no numérico {imp!r}"); continue
                        if pg and imp.strip() not in ("-","–","—") and re.sub(r"[−–]", "-", imp.strip().lstrip("-−–")) not in re.sub(r"[−–]", "-", P.get(int(pg), "")):
                            problemas.append(f"{y} {k} {cual}: {imp} no está en p.{pg}")
                        v += x
            if cual == "actual":
                tabla.setdefault(k, {})[y] = v
                fuentes.setdefault(k, {})[y] = (its[0][1] if its else None, (p or {}).get("nota"))
            else:
                anterior.setdefault(k, {})[y-1] = v
# cruce
cruce = []
for k in tabla:
    for y in range(2016, 2025):
        a, b = tabla[k].get(y), anterior.get(k, {}).get(y)
        if a is None and b is None: continue
        if a is None or b is None or abs(abs(a) - abs(b)) > 0.5:
            cruce.append(f"{k} {y}: informe {y} = {a} · comparativo en informe {y+1} = {b}")
json.dump({"tabla": {k: {str(y): v for y, v in d.items()} for k, d in tabla.items()},
           "fuentes": {k: {str(y): v for y, v in d.items()} for k, d in fuentes.items()},
           "comparativos": {k: {str(y): v for y, v in d.items()} for k, d in anterior.items()}},
          open(f"{BASE}/fase1_partes/consolidado.json", "w"), ensure_ascii=False, indent=1)
print("PROBLEMAS DE PÁGINA/NÚMERO:", len(problemas)); print("\n".join(problemas))
print("\nDIFERENCIAS CON EL COMPARATIVO DEL AÑO SIGUIENTE:", len(cruce)); print("\n".join(cruce))
print()
for k in tabla:
    print(f"{k:26s}", " ".join(f"{(v if v is not None else float('nan')):>10.0f}" for y, v in sorted(tabla[k].items())))
