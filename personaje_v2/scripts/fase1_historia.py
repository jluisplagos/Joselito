#!/usr/bin/env python3
"""Pieza 7 · construye fase1_v63.json a partir de los informes anuales (texto/*.txt con marcas [PDF PAGE n]).

Procedimiento (generalización de lo hecho a mano con Rational, 3-nov-2026; DECISIONES.md):
  1. `preparar CARPETA`  elige un informe por ejercicio (los 10 más recientes con estados financieros), y escribe un prompt por
     año (prompts_generados/01_historia_<año>.md, agente Sonnet, en paralelo) y otro de metadatos (01_metadatos.md: precio,
     acciones, rf, sector, geografía; necesita web). Código 10 si falta alguna salida (lista en ESPERANDO_FASE1.md), 0 si están.
  2. Cada agente escribe fase1_partes/AR_<año>.json y comprueba su archivo con `comprobar-anio CARPETA AÑO`.
  3. `construir CARPETA` comprueba otra vez cada número en su página, consolida (regla: para cada año, la cifra MÁS RECIENTE
     publicada: el comparativo del informe siguiente si existe, que recoge reexpresiones y reclasificaciones; si no, la del propio
     informe), escribe historia_revision.md (todas las diferencias, ceros con evidencia, desconocidos, convenciones) y
     fase1_v63.json. Código 0 ok · 1 faltan datos esenciales o hay salidas inválidas (detalle en historia_revision.md) · 2 uso.

Convenciones (declaradas en las notas de cada partida y en historia_revision.md):
  - unidades a millones (mm) según `unidad` del informe; acciones a millones;
  - magnitudes de coste en positivo (capex, D&A, intereses, arrendamientos, I+D, SBC, impuestos); EBIT, beneficio y CFO con su signo;
  - adquisiciones = −(suma de lo impreso en el estado de flujos: pagos negativos, cobros positivos);
  - circulante (aumento = consume caja) = −(suma de las líneas de variación del circulante del estado de flujos);
  - tipo impositivo = impuestos ÷ resultado antes de impuestos (vacío si este ≤ 0);
  - caja = efectivo y equivalentes; + otros activos financieros corrientes SOLO si fase1_metadatos.json lo declara
    (convenciones.caja_incluye_otros_activos_financieros = true, con motivo);
  - un `cero` del agente (con motivo y página) es 0; un null sin `cero` es desconocido (celda vacía), nunca 0;
  - fase1_decisiones.json (opcional) fija a mano una cifra con su fuente: {"partida": {"año": {"valor_mm": x, "fuente": "..."}}}.
"""
import glob
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, ".."))
PARTIDAS = ["ventas", "ebit", "da", "beneficio_neto", "impuestos", "bai", "cfo", "capex", "adquisiciones", "circulante_lineas", "intereses",
            "intereses_financiacion", "arrendamientos_principal", "sbc", "id", "acciones_diluidas", "patrimonio", "deuda", "arrendamientos",
            "caja", "otros_activos_financieros", "pensiones", "minoritarios"]
CON_SIGNO = {"ebit", "beneficio_neto", "bai", "cfo", "patrimonio"}
ESENCIALES = ["ventas", "ebit", "beneficio_neto", "cfo", "capex", "patrimonio", "caja", "acciones_diluidas"]
ESCALA = {"unidades": 1e-6, "miles": 1e-3, "millones": 1.0}
CLAVE_ESTADOS = re.compile(r"balance sheet|statement of financial position|cash flow statement|statement of cash flows|estado de flujos|balance consolidado|estado de situaci", re.I)


def paginas(ruta):
    t = open(ruta, encoding="utf-8", errors="replace").read()
    return {int(m.group(1)): m.group(2) for m in re.finditer(r"\[PDF PAGE (\d+)\]\n(.*?)(?=\[PDF PAGE \d+\]|\Z)", t, re.S)}


def norm(s):
    return re.sub(r"\s+", " ", str(s).replace("−", "-").replace("–", "-").replace("—", "-")).strip()


def numero(s):
    """'1,125,977' · '(12.345)' · '-8,580' · '3.463' · '–' → float. Separadores de miles con coma o punto; sin decimales en los estados."""
    s = norm(s)
    if s in ("-", "", "—"):
        return 0.0
    neg = s.startswith("(") or s.startswith("-")
    d = s.strip("()-+ ")
    if not re.fullmatch(r"\d{1,3}([.,]\d{3})*([.,]\d{1,2})?|\d+([.,]\d{1,2})?", d):
        raise ValueError(f"no numérico: {s!r}")
    m = re.fullmatch(r"(.*?)([.,])(\d{1,2})", d)
    if m and not re.fullmatch(r"\d{1,3}([.,]\d{3})+", d):  # decimales reales (p. ej. 11.37)
        v = float(re.sub(r"[.,]", "", m.group(1)) + "." + m.group(3))
    else:
        v = float(re.sub(r"[.,]", "", d))
    return -v if neg else v


def componentes(x):
    if x is None:
        return []
    if isinstance(x, dict):
        if isinstance(x.get("componentes"), list):
            return x["componentes"]
        return [x] if "impreso" in x else []
    return [c for c in x if isinstance(c, dict)]


# ---------------------------------------------------------------- comprobar
def comprobar_anio(carpeta, anio):
    ruta = os.path.join(carpeta, "fase1_partes", f"AR_{anio}.json")
    if not os.path.exists(ruta):
        return [f"falta {ruta}"]
    try:
        d = json.load(open(ruta, encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"AR_{anio}.json no es JSON: {e}"]
    err = []
    arch = d.get("archivo")
    if not arch or not os.path.exists(os.path.join(carpeta, "texto", arch)):
        return [f"AR_{anio}: «archivo» ausente o inexistente en texto/: {arch!r}"]
    P = {k: norm(v) for k, v in paginas(os.path.join(carpeta, "texto", arch)).items()}
    if d.get("unidad") not in ESCALA:
        err.append(f"unidad {d.get('unidad')!r} no es una de {list(ESCALA)}")
    falt = [k for k in PARTIDAS if k not in (d.get("partidas") or {})]
    if falt:
        err.append("faltan claves: " + ", ".join(falt))
    for k, p in (d.get("partidas") or {}).items():
        if not isinstance(p, dict):
            err.append(f"{k}: no es un objeto")
            continue
        for cual in ("actual", "anterior"):
            for c in componentes(p.get(cual)):
                imp, pg, lin = c.get("impreso"), c.get("pagina"), c.get("linea")
                if c.get("signo", 1) not in (1, -1):
                    err.append(f"{k} {cual}: signo {c.get('signo')!r} no es 1 ni -1")
                try:
                    numero(imp)
                except Exception as e:
                    err.append(f"{k} {cual}: {e}")
                    continue
                if not isinstance(pg, int) or pg not in P:
                    err.append(f"{k} {cual}: página {pg!r} inexistente")
                    continue
                if not lin or norm(imp) not in norm(lin):
                    err.append(f"{k} {cual}: «{imp}» no está en su línea")
                elif norm(lin) not in P[pg]:
                    # la línea puede venir con espacios colapsados: basta con que el número esté en la página junto al concepto
                    if norm(imp) not in P[pg]:
                        err.append(f"{k} {cual}: «{imp}» no está en la página {pg}")
        cz = p.get("cero")
        if cz is not None and (not isinstance(cz, dict) or not cz.get("motivo") or cz.get("pagina") not in P):
            err.append(f"{k}: «cero» sin motivo o con página inexistente")
    return err


# ---------------------------------------------------------------- preparar
def elegir_fuentes(carpeta):
    fijo = os.path.join(carpeta, "fase1_fuentes.json")
    if os.path.exists(fijo):
        return {int(k): v for k, v in json.load(open(fijo, encoding="utf-8")).items()}
    por_anio = {}
    for ruta in sorted(glob.glob(os.path.join(carpeta, "texto", "*.txt"))):
        nombre = os.path.basename(ruta)
        anios = re.findall(r"(?<!\d)(20\d\d)(?!\d)", nombre)
        if not anios:
            continue
        txt = open(ruta, encoding="utf-8", errors="replace").read()
        puntos = len(CLAVE_ESTADOS.findall(txt))
        if puntos == 0:
            continue
        a = int(anios[-1])
        if a not in por_anio or puntos > por_anio[a][1]:
            por_anio[a] = (nombre, puntos)
    ult = sorted(por_anio)[-10:]
    out = {a: por_anio[a][0] for a in ult}
    json.dump({str(a): f for a, f in out.items()}, open(fijo, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return out


def listas_plantilla(carpeta):
    """Vuelca los nombres válidos de sector (hoja Sector) y de país/región (hoja Riesgo país) para el agente de metadatos."""
    sys.path.insert(0, AQUI)
    import config_v2
    import openpyxl
    cfg = config_v2.cargar()
    wb = openpyxl.load_workbook(cfg["plantilla"]["archivo"], read_only=True)
    sect = [r[0] for r in wb["Sector"].iter_rows(min_row=1, values_only=True) if r and isinstance(r[0], str) and r[0].strip()]
    paises = [r[0] for r in wb["Riesgo país"].iter_rows(min_row=6, values_only=True) if r and isinstance(r[0], str) and r[0].strip()]
    with open(os.path.join(carpeta, "fase1_listas.md"), "w", encoding="utf-8") as f:
        f.write("# Nombres válidos de la Plantilla V6.3\n\n## Sector de Damodaran (hoja Sector, columna A)\n" + "\n".join(f"- {s}" for s in sect)
                + "\n\n## País o región (hoja Riesgo país, columna A)\n" + "\n".join(f"- {p}" for p in paises) + "\n")


def preparar(carpeta, empresa):
    fuentes = elegir_fuentes(carpeta)
    if len(fuentes) < 3:
        print(f"solo {len(fuentes)} informes con estados financieros en texto/ (hacen falta los de 10 años; mínimo 3)")
        return 1
    os.makedirs(os.path.join(carpeta, "fase1_partes"), exist_ok=True)
    os.makedirs(os.path.join(carpeta, "prompts_generados"), exist_ok=True)
    plantilla = open(os.path.join(RAIZ, "prompts", "historia_anio.md"), encoding="utf-8").read()
    pendientes = []
    for a, arch in sorted(fuentes.items()):
        if os.path.exists(os.path.join(carpeta, "fase1_partes", f"AR_{a}.json")) and not comprobar_anio(carpeta, a):
            continue
        txt = (plantilla.replace("{CARPETA}", carpeta).replace("{EMPRESA}", empresa).replace("{ANIO}", str(a))
               .replace("{ARCHIVO}", arch).replace("{RAIZ}", RAIZ))
        errs = comprobar_anio(carpeta, a) if os.path.exists(os.path.join(carpeta, "fase1_partes", f"AR_{a}.json")) else []
        if errs:
            txt += "\n\n## CORRECCIÓN\nTu salida anterior no pasa la comprobación:\n" + "\n".join(f"- {e}" for e in errs[:40]) + "\n"
        p = os.path.join(carpeta, "prompts_generados", f"01_historia_{a}.md")
        open(p, "w", encoding="utf-8").write(txt)
        pendientes.append((f"historia {a}", p, f"fase1_partes/AR_{a}.json"))
    if not os.path.exists(os.path.join(carpeta, "fase1_metadatos.json")):
        listas_plantilla(carpeta)
        txt = open(os.path.join(RAIZ, "prompts", "metadatos_fase1.md"), encoding="utf-8").read()
        txt = txt.replace("{CARPETA}", carpeta).replace("{EMPRESA}", empresa).replace("{ANIOS}", ", ".join(str(a) for a in sorted(fuentes)))
        p = os.path.join(carpeta, "prompts_generados", "01_metadatos.md")
        open(p, "w", encoding="utf-8").write(txt)
        pendientes.append(("metadatos", p, "fase1_metadatos.json"))
    if pendientes:
        with open(os.path.join(carpeta, "ESPERANDO_FASE1.md"), "w", encoding="utf-8") as f:
            f.write(f"# ESPERANDO · fase 1 (Historia de 10 años y metadatos) · {empresa}\n\nLanza estos agentes EN PARALELO, cada uno con su prompt como instrucción "
                    "(historia: Sonnet, esfuerzo medio; metadatos: Sonnet, esfuerzo medio, con búsqueda web). Cuando todos hayan escrito su salida, vuelve a lanzar pipeline.py.\n\n")
            for n, p, s in pendientes:
                f.write(f"- **{n}** · prompt `{os.path.relpath(p, carpeta)}` → escribe `{s}`\n")
        print(f"ESPERANDO fase 1: {len(pendientes)} agentes ({', '.join(n for n, _, _ in pendientes)})")
        return 10
    if os.path.exists(os.path.join(carpeta, "ESPERANDO_FASE1.md")):
        os.remove(os.path.join(carpeta, "ESPERANDO_FASE1.md"))
    return 0


# ---------------------------------------------------------------- construir
def construir(carpeta):
    fuentes = elegir_fuentes(carpeta)
    anios = sorted(fuentes)
    rev, problemas = [], []
    for a in anios:
        for e in comprobar_anio(carpeta, a):
            problemas.append(f"AR_{a}: {e}")
    meta_p = os.path.join(carpeta, "fase1_metadatos.json")
    if not os.path.exists(meta_p):
        problemas.append("falta fase1_metadatos.json")
    if problemas:
        open(os.path.join(carpeta, "historia_revision.md"), "w", encoding="utf-8").write("# Revisión de la Historia · SALIDAS INVÁLIDAS\n\n" + "\n".join(f"- {p}" for p in problemas) + "\n")
        print("\n".join(problemas[:30]))
        return 1
    meta = json.load(open(meta_p, encoding="utf-8"))
    dec_p = os.path.join(carpeta, "fase1_decisiones.json")
    dec = json.load(open(dec_p, encoding="utf-8")) if os.path.exists(dec_p) else {}
    AR = {a: json.load(open(os.path.join(carpeta, "fase1_partes", f"AR_{a}.json"), encoding="utf-8")) for a in anios}

    def leer(a, k, cual):
        """(valor_mm, fuente, cero_motivo) del informe a, columna cual; valor None si no hay."""
        d = AR[a]
        p = (d["partidas"] or {}).get(k) or {}
        esc = ESCALA[d["unidad"]]
        comps = componentes(p.get(cual))
        if comps:
            if k == "circulante_lineas":
                v = -sum(numero(c["impreso"]) * c.get("signo", 1) for c in comps)
            else:
                v = sum(numero(c["impreso"]) * c.get("signo", 1) for c in comps)
            if k == "acciones_diluidas":
                v = v / 1e6 if abs(v) > 1e5 else (v / 1e3 if abs(v) > 1e3 else v)
            else:
                v = v * esc
            pags = sorted({c["pagina"] for c in comps})
            return v, f"{d['archivo']} p.{','.join(map(str, pags))}", None
        cz = p.get("cero")
        if cz and cual == "actual":
            return 0.0, f"{d['archivo']} p.{cz['pagina']} (cero: {cz['motivo']})", cz["motivo"]
        return None, None, None

    def ajustar(k, v):
        if v is None:
            return None
        if k in CON_SIGNO or k == "circulante_lineas":
            return v
        if k == "adquisiciones":
            return -v
        return abs(v)

    serie, fuente, notas_k = {}, {}, {}
    for k in PARTIDAS:
        serie[k], fuente[k] = [], []
        for a in anios:
            v, f, _ = leer(a, k, "actual")
            usado = "propio"
            if a + 1 in AR:
                v2, f2, _ = leer(a + 1, k, "anterior")
                if v2 is not None:
                    if v is not None and abs(abs(v2) - abs(v)) > max(0.0005 * max(abs(v), 1), 0.0005):
                        rev.append(f"- **{k} {a}**: informe {a} = {round(ajustar(k, v), 3)} · comparativo del informe {a + 1} = {round(ajustar(k, v2), 3)} → se usa el más reciente ({f2}). Reexpresión, reclasificación o definición distinta: revisar si la diferencia es grande. Informe {a + 1}: «{(AR[a + 1].get('reexpresion') or 'sin nota de reexpresión')[:200]}»")
                    v, f, usado = v2, f2 + " (comparativo del informe siguiente)", "siguiente"
            if k in dec and isinstance(dec[k], dict) and str(a) in dec[k]:
                v, f = dec[k][str(a)]["valor_mm"], dec[k][str(a)]["fuente"] + " (fase1_decisiones.json)"
                rev.append(f"- **{k} {a}**: fijado a mano en fase1_decisiones.json = {v} ({f})")
                serie[k].append(v)
            else:
                serie[k].append(None if v is None else round(ajustar(k, v), 4))
            fuente[k].append(f or "desconocido")
    # tipo impositivo
    tipo = []
    for i in range(len(anios)):
        t, b = serie["impuestos"][i], serie["bai"][i]
        tipo.append(round(t / b, 4) if t is not None and b not in (None, 0) and b > 0 else None)
    caja = list(serie["caja"])
    conv = (meta.get("convenciones") or {})
    if conv.get("caja_incluye_otros_activos_financieros"):
        caja = [None if c is None else round(c + (o or 0.0), 4) for c, o in zip(serie["caja"], serie["otros_activos_financieros"])]
    H = {}

    origen = {"circulante": "circulante_lineas"}

    def poner(clave, vals, fu, nota):
        # notas de los lectores (lo que vieron: reexpresiones, partidas extraordinarias, ambigüedades), las más recientes primero
        k = origen.get(clave, clave)
        lect = [f"{a}: {AR[a]['partidas'].get(k, {}).get('nota')}" for a in sorted(anios, reverse=True) if isinstance(AR[a]["partidas"].get(k), dict) and AR[a]["partidas"][k].get("nota")]
        if k in dec and dec[k].get("_nota"):
            lect.insert(0, dec[k]["_nota"])
        extra = (" Notas de los lectores: " + " | ".join(lect))[:700] if lect else ""
        H[clave] = {"valores": vals, "fuente": "; ".join(f"{a} {s}" for a, s in zip(anios, fu)), "pagina": None, "nota": nota + extra}
    base = "Construido por fase1_historia.py: cifra más reciente publicada de cada año (comparativo del informe siguiente cuando existe)."
    for k in ["ventas", "ebit", "da", "beneficio_neto"]:
        poner(k, serie[k], fuente[k], base)
    H["tipo_impositivo"] = {"valores": tipo, "fuente": "impuestos ÷ resultado antes de impuestos; " + "; ".join(f"{a} {x} / {y}" for a, x, y in zip(anios, fuente["impuestos"], fuente["bai"])), "pagina": None, "nota": "Vacío si el resultado antes de impuestos es ≤ 0."}
    for k in ["cfo", "capex", "adquisiciones"]:
        poner(k, serie[k], fuente[k], base + (" Adquisiciones = −(pagos y cobros por negocios del estado de flujos)." if k == "adquisiciones" else ""))
    poner("circulante", serie["circulante_lineas"], fuente["circulante_lineas"], base + " Aumento del circulante = −(suma de las líneas de variación del circulante del estado de flujos): convención del ejercicio.")
    for k in ["intereses", "intereses_financiacion", "arrendamientos_principal", "sbc", "id", "acciones_diluidas", "patrimonio", "deuda", "arrendamientos"]:
        poner(k, serie[k], fuente[k], base)
    poner("caja", caja, fuente["caja"], base + (f" Incluye otros activos financieros corrientes: {conv.get('motivo_caja', '')} Solo efectivo (mm): " + ", ".join(f"{a} {c}" for a, c in zip(anios, serie['caja'])) if conv.get("caja_incluye_otros_activos_financieros") else " Solo efectivo y equivalentes (definición de la plantilla)."))
    for k in ["pensiones", "minoritarios"]:
        poner(k, serie[k], fuente[k], base)
    # esenciales
    falt = [f"{k} {a}" for k in ESENCIALES for a, v in zip(anios, serie[k]) if v is None and a >= anios[-3]]
    f1 = {k: meta.get(k) for k in ("empresa", "ticker", "fecha_analisis", "sector_texto", "moneda_modelo", "norma_contable", "cierre_fiscal", "mercado", "ratio_adr", "sector_damodaran", "precio", "acciones_diluidas", "capitalizacion", "tasa_sin_riesgo", "geografia", "geografia_fuente")}
    f1["unidad"] = "mm"
    f1["anios_fcf_base"] = meta.get("anios_fcf_base", 3)
    f1["historia"] = {"anios": anios, "partidas": H}
    f1["analisis"] = meta.get("analisis") or {}
    if not f1.get("capitalizacion") and f1.get("precio") and f1.get("acciones_diluidas"):
        f1["capitalizacion"] = {"valor": round(f1["precio"]["valor"] * f1["acciones_diluidas"]["valor"], 1), "fecha": f1["precio"].get("fecha"), "fuente": "precio × acciones diluidas"}
    f1["_notas"] = ["Historia construida por scripts/fase1_historia.py (pieza 7); revisión completa en historia_revision.md."] + list(meta.get("_notas") or [])
    faltan_meta = [k for k in ("empresa", "ticker", "moneda_modelo", "precio", "acciones_diluidas", "sector_damodaran") if not f1.get(k)]
    # revisión
    with open(os.path.join(carpeta, "historia_revision.md"), "w", encoding="utf-8") as f:
        f.write(f"# Revisión de la Historia · {f1.get('empresa')}\n\nInformes usados: " + ", ".join(f"{a} {fuentes[a]}" for a in anios) + "\n\n")
        f.write("## Tabla (mm)\n\n| Partida | " + " | ".join(map(str, anios)) + " |\n|---|" + "---|" * len(anios) + "\n")
        for k, d in H.items():
            f.write(f"| {k} | " + " | ".join("—" if v is None else f"{v:,.3f}" for v in d["valores"]) + " |\n")
        f.write("\n## Diferencias entre el informe de cada año y el comparativo del siguiente (se usa la más reciente)\n\n" + ("\n".join(rev) or "- ninguna") + "\n")
        ceros = [f"- {k} {a}: {s}" for k in PARTIDAS for a, s in zip(anios, fuente[k]) if "(cero:" in s]
        desc = [f"- {k} {a}" for k in PARTIDAS for a, v in zip(anios, serie[k]) if v is None]
        f.write("\n## Ceros con evidencia\n\n" + ("\n".join(ceros) or "- ninguno") + "\n\n## Desconocidos (celda vacía, nunca 0)\n\n" + ("\n".join(desc) or "- ninguno") + "\n")
        f.write("\n## Convenciones\n\n" + json.dumps(conv, ensure_ascii=False) + "\n")
        if falt or faltan_meta:
            f.write("\n## BLOQUEA\n\n" + "\n".join(f"- falta {x}" for x in falt + faltan_meta) + "\n")
    if falt or faltan_meta:
        print("faltan datos esenciales: " + ", ".join(falt + faltan_meta))
        return 1
    json.dump(f1, open(os.path.join(carpeta, "fase1_v63.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"fase1_v63.json escrito ({len(anios)} años, {len(rev)} diferencias con el comparativo, ver historia_revision.md)")
    return 0


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    cmd, carpeta = sys.argv[1], os.path.abspath(sys.argv[2])
    if cmd == "comprobar-anio":
        errs = comprobar_anio(carpeta, int(sys.argv[3]))
        print("OK" if not errs else "\n".join(errs))
        return 0 if not errs else 1
    if cmd == "preparar":
        return preparar(carpeta, sys.argv[3] if len(sys.argv) > 3 else os.path.basename(carpeta))
    if cmd == "construir":
        return construir(carpeta)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
