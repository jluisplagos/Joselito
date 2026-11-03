#!/usr/bin/env python3
"""informe.md por empresa (Anexo D §D.8): trece secciones en orden fijo; las que no aplican al estado dicen «No aplica en estado …».

Uso: informe.py CARPETA   (lee ficha.json y los JSON de las fases; escribe informe.md)
Sin preámbulos ni cierres. Todo hecho con su fuente; todo juicio como juicio. Ningún tamaño de posición.
"""
import json
import os
import sys


def cargar(c, n):
    p = os.path.join(c, n)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def f(x, pct=False):
    if x is None:
        return "—"
    if isinstance(x, float):
        if pct:
            return f"{x:.1%}"
        if abs(x) < 1:  # tasas y ratios (g = 0,015, S2C…): sin redondear a dos decimales (0,015 no es 0,01)
            return (f"{x:.4f}".rstrip("0").rstrip(".")) or "0"
        return f"{x:,.2f}"
    return str(x)


def main():
    c = sys.argv[1]
    F = cargar(c, "ficha.json") or {}
    fa, fb, fc = cargar(c, "fase_a.json") or {}, cargar(c, "fase_b.json") or {}, cargar(c, "fase_c.json") or {}
    refs = cargar(c, "referencias_mecanicas.json") or {}
    precio = F.get("escalera") or {}
    estado = F.get("estado_analisis")
    na = lambda: f"No aplica en estado {estado}."  # noqa: E731
    S = []
    # 1
    dec = F.get("decision") or {}
    linea = f"**Estado `{estado}` · cubo {F.get('cubo') or F.get('cubo_cualitativo_fase_a') or '—'} · acción {dec.get('accion') or 'ninguna'}**"
    if precio and "precio_si" in precio:
        linea += f" · precio {f(precio.get('precio'))} {F.get('moneda') or ''} · zona {precio.get('zona')} · precio de Sí {f(precio.get('precio_si'))} · precio esc. MALO {f(precio.get('precio_escenario_malo'))} · ponderado {f(precio.get('ponderado'))}"
    if dec.get("precio_objetivo"):
        linea += f" · precio objetivo {f(dec['precio_objetivo'])}"
    if dec.get("condicion"):
        linea += f" · condición: {dec['condicion']}"
    S.append(("1. Estado, cubo y conclusión", linea))
    # 2
    cambios = F.get("cambios_vs_etapa1") or []
    if cambios:
        t = ["| Celda | Etapa 1 | Etapa 2 | Decisión | Motivo | Evidencia y razonamiento |", "|---|---|---|---|---|---|"]
        t += [f"| {x['celda']} | {f(x.get('antes'))} | {f(x.get('despues'))} | {x.get('decision')} | {x.get('motivo')} | {x.get('evidencia_y_razonamiento')} |" for x in cambios]
        comp = F.get("comparacion_etapa_1") or {}
        if comp:
            t.append(f"\nCubo v1 {comp.get('cubo_v1')} → v2 {comp.get('cubo_v2')} · precio de Sí v1 {f(comp.get('precio_de_si_v1'))} → v2 {f(comp.get('precio_de_si_v2'))}. {comp.get('por_que_difieren') or ''}")
        S.append(("2. Qué cambió respecto a la etapa 1 y por qué", "\n".join(t)))
    else:
        S.append(("2. Qué cambió respecto a la etapa 1 y por qué", "Sin herencia registrada (la fase A no se ejecutó o no hay etapa 1)."))
    # 3
    sp = F.get("seis_preguntas") or {}
    S.append(("3. Las seis preguntas", "\n".join(f"- **{k.replace('_', ' ')}**: {v}" for k, v in sp.items()) if sp else na()))
    # 4
    esc = F.get("escenarios") or {}
    t = []
    for e in ("MALO", "NORMAL", "BUENO"):
        x = esc.get(e) or {}
        h = x.get("historia") or {}
        t.append(f"**{e}** (p = {f(x.get('probabilidad'))}; valor por acción {f(x.get('valor_accion'))}): {x.get('frase') or ''}\n" + ("\n".join(f"  - {k}: {v}" for k, v in h.items()) if isinstance(h, dict) else str(h)))
    S.append(("4. Los tres escenarios contados", "\n".join(t) if fa else na()))
    # 5
    if fb:
        t = ["| Palanca | Escenario | Referencia mecánica | Decisión | Desviación | Clase | Por qué |", "|---|---|---|---|---|---|---|"]
        for pal in ("crecimiento_1_5", "margen_objetivo", "s2c", "g_perpetuo", "roic_lp", "probabilidades"):
            for e in ("MALO", "NORMAL", "BUENO"):
                x = ((fb.get("palancas") or {}).get(pal) or {}).get(e) or {}
                if x:
                    t.append(f"| {pal} | {e} | {f(x.get('referencia_mecanica'))}{(' (' + x['referencia_no_disponible_motivo'] + ')') if x.get('referencia_no_disponible_motivo') else ''} | {f(x.get('valor'))} | {f(x.get('desviacion'))} | {x.get('clase')} | {x.get('porque')} |")
        q = fb.get("quiebra") or {}
        t.append(f"\nQuiebra C22 = {f(q.get('C22'))} (disparadores: {', '.join(q.get('disparadores') or []) or 'ninguno'}): {q.get('porque') or ''} · Exceso de caja C76 = {f((fb.get('exceso_caja') or {}).get('C76'))} · Mercado C24 = {f((fb.get('mercado') or {}).get('C24'))}")
        t.append(f"Referencias mecánicas: versión {refs.get('version_referencias_mecanicas')} (convención del ejercicio; no son estimaciones de Damodaran).")
        S.append(("5. Tabla de palancas: referencia mecánica → decisión → desviación → clase → por qué", "\n".join(t)))
    else:
        S.append(("5. Tabla de palancas", na()))
    # 6
    sem = F.get("semaforos") or {}
    res = cargar(c, "resultados.json") or {}
    if res:
        t = ["Semáforos (Diagnóstico V6, bloque 3):"] + [f"- {v[0]}: {' · '.join(str(x) for x in v[1:] if x)}" for v in sem.values()]
        pt = F.get("peso_terminal") or [None] * 3
        t.append(f"- Peso del terminal (MALO/NORMAL/BUENO): {f(pt[0], True)} / {f(pt[1], True)} / {f(pt[2], True)}")
        sj = F.get("salto_anio_11") or [None] * 4
        t.append(f"- Salto del año 11 (MALO/NORMAL/BUENO): {f(sj[1])} / {f(sj[2])} / {f(sj[3])}" if isinstance(sj, list) and len(sj) >= 4 else "- Salto del año 11: —")
        t.append(f"- DCF inverso: el precio actual descuenta un crecimiento de ventas a cinco años de {f(precio.get('g_impl_actual'), True) if isinstance(precio.get('g_impl_actual'), float) else precio.get('g_impl_actual')} (NORMAL: {f((res.get('palancas') or {}).get('C14'), True)})")
        torn = res.get("tornado") or {}
        t.append(f"- Tornado (información, no criterio): palanca más influyente {torn.get('mas_influyente')}; efectos {torn.get('efectos')}")
        S.append(("6. Lo que dice la hoja", "\n".join(t)))
    else:
        S.append(("6. Lo que dice la hoja", na()))
    # 7
    if precio and "precio_si" in precio:
        t = [f"Escalera (convención experimental, k = {precio.get('k')}): precio del escenario MALO {f(precio.get('precio_escenario_malo'))} (no es un suelo de valor) · precio de Sí {f(precio.get('precio_si'))} · ponderado {f(precio.get('ponderado'))}. Zona del precio actual {f(precio.get('precio'))}: **{precio.get('zona')}**. La zona dice si el precio cumple la regla de precio con mis valores; la conclusión depende además del fundamento material (D10) y de los bloqueos (D17). Regla antigua de la hoja (mín(MALO, 0,75 × ponderado)): {f(precio.get('C156_regla_antigua'))}."]
        if precio.get("aviso_tasa_descuento_mas_influyente") is True:
            t.append("El valor depende sobre todo de tu rentabilidad exigida (r heredada, S-3).")
        fm = F.get("fundamento_material") or {}
        if fm:
            hs = fm.get("hipotesis_sin_fundamento") or []
            t.append(f"\nFundamento material (D10): {len(hs)} hipótesis sin fundamento suficiente → resultado **{fm.get('resultado')}**.")
            for h in hs:
                ad = h.get("alternativas_defendibles") or {}
                t.append(f"- {h.get('celda')} · {h.get('hipotesis')} · clase {h.get('clase')} · {h.get('porque_sin_fundamento')} · alternativas: {'rango ' + json.dumps(ad.get('rango'), ensure_ascii=False) + ' · ' if ad.get('hay_base') else 'SIN BASE PARA ACOTAR · '}{ad.get('evidencia')}")
            cc = F.get("comprobacion_conjunta") or {}
            if cc:
                eb = cc.get("escalera_bajo_combinacion") or {}
                t.append(f"- Comprobación conjunta: combinación {json.dumps(cc.get('combinacion'), ensure_ascii=False)} · {cc.get('coherencia_economica')} · bajo la combinación el precio de Sí sería {f(eb.get('precio_si'))} y la zona {eb.get('zona_precio_actual')} → **{'superada' if cc.get('sobrevive') else 'no superada'}**; superarla no es una garantía de seguridad.")
        de = F.get("dos_errores") or {}
        if de:
            t.append(f"\nLos dos errores opuestos: más cerca de «{de.get('mas_cerca_de')}» porque {de.get('porque')}")
        S.append(("7. Escalera de precios (convención experimental), fundamento material y los dos errores opuestos", "\n".join(t)))
    else:
        S.append(("7. Escalera de precios, fundamento material y los dos errores opuestos", (precio or {}).get("sin_lectura") and f"Sin lectura de precio: {precio['sin_lectura']}" or na()))
    # 8
    cel = fc.get("celdas") or {}
    S.append(("8. Tesis y tesis inversa", f"**Tesis:** {cel.get('B101')}\n\n**Tesis inversa:** {cel.get('B102')}" if cel.get("B101") else na()))
    # 9
    pr = F.get("predicciones")
    S.append(("9. Predicciones", "\n".join(f"- {p['texto']} · comprobar el {p['fecha']} · probabilidad dado el NORMAL {f(p['prob'])}" for p in pr) if pr and pr[0].get("texto") else na()))
    # 10
    cb = F.get("cambiaria_de_cubo") or {}
    S.append(("10. Qué me haría cambiar de cubo", "\n".join(f"- {k}: {v}" for k, v in cb.items()) if cb else na()))
    # 11
    ac = F.get("autocomprobacion") or []
    S.append(("11. Autocomprobación", "\n".join(f"- **{x.get('sesgo')}**: {x.get('hallazgo')} → {x.get('cambio')}" for x in ac) if ac else na()))
    # 12
    t = []
    for k in ("lo_que_no_se", "que_no_sabria_munger"):
        for x in (fa.get(k) or []):
            t.append(f"- {x}")
    rda = F.get("revision_datos_ausentes") or {}
    for x in (rda.get("revisados") or []):
        t.append(f"- Dato ausente {x.get('dato')} ({x.get('que_falta')}): afecta a {x.get('conclusion_afectada')} · {'MATERIAL' if x.get('material_para_conclusion_favorable') else 'no material'} · {x.get('porque')}")
    if F.get("que_lo_resolveria"):
        t.append(f"- Lo que haría falta para continuar: {F.get('incertidumbre_pendiente') or ''} → {F.get('que_lo_resolveria')}")
    S.append(("12. Qué no sé y qué pediría", "\n".join(t) if t else "Nada registrado."))
    # 13
    ci = F.get("citas") or {}
    S.append(("13. Citas usadas", f"Munger: {ci.get('munger')} citas con página · Damodaran: {ci.get('damodaran')} citas con página (verificadas por verify_quotes_v2.py en verificacion_citas.txt)."))
    md = [f"# {F.get('empresa')} ({F.get('ticker')}) · informe del personaje v2 · {F.get('fecha')}\n"]
    for titulo, cuerpo in S:
        md.append(f"## {titulo}\n\n{cuerpo}\n")
    open(os.path.join(c, "informe.md"), "w", encoding="utf-8").write("\n".join(md))
    print(f"OK: informe.md ({len(S)} secciones)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
