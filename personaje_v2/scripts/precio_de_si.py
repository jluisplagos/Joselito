#!/usr/bin/env python3
"""Precio de Sí y escalera de precios (Anexo C; decisión D11: convención experimental del ejercicio).

Uso:
  precio_de_si.py resultados.json precio.json [--k 3] [--copia]
  precio_de_si.py --autotest            (los cinco casos del Anexo C §C.5 y las propiedades de §C.2)

Lee resultados.json (leer_resultados.py) y escribe precio.json. El script NO decide nada: produce una
lectura aritmética de los valores y probabilidades introducidos; la conclusión depende además del
fundamento material (D10) y de los bloqueos (D17). `--copia` marca que la lectura es de la copia de
prueba de la comprobación conjunta (D10).
Códigos: 0 ok (incluye «sin lectura» documentada) · 2 uso · 3 autotest fallido · 5 valores desordenados (error G19).
"""
import json
import sys

K_DEFECTO = 3
TOL = 1e-9
ROTULO_TASA = "Tasa de descuento (±1 pt)"


def p_estrella(V, p, k):
    """Precio más alto con G(P) ≥ k·L(P). Forma cerrada por tramos (Anexo C §C.3)."""
    s = sorted(zip(V, p))
    for j in (1, 2):
        bajo, alto = s[:j], s[j:]
        num = sum(pp * v for v, pp in alto) + k * sum(pp * v for v, pp in bajo)
        den = sum(pp for v, pp in alto) + k * sum(pp for v, pp in bajo)
        P = num / den
        if s[j - 1][0] - 1e-12 <= P <= s[j][0] + 1e-12:
            return P
    raise AssertionError("P* no cae en ningún tramo: revisa valores y probabilidades")


def G(V, p, P):
    return sum(pp * max(v - P, 0.0) for v, pp in zip(V, p))


def L(V, p, P):
    return sum(pp * max(P - v, 0.0) for v, pp in zip(V, p))


def zona(precio, malo, precio_si, pond):
    if malo is not None and precio <= malo:
        return "bajo_malo"
    if precio <= precio_si:
        return "cumple_regla_k"
    if precio <= pond:
        return "vigilar"
    return "caro"


def interpolar(tabla, x):
    """tabla: [[g, valor]] creciente en g. Devuelve el valor en x (lineal) o None fuera de rango."""
    pares = [(g, v) for g, v in tabla if isinstance(g, (int, float)) and isinstance(v, (int, float))]
    if len(pares) < 2 or x < pares[0][0] or x > pares[-1][0]:
        return None
    for (g0, v0), (g1, v1) in zip(pares, pares[1:]):
        if g0 <= x <= g1:
            return v0 if g1 == g0 else v0 + (v1 - v0) * (x - g0) / (g1 - g0)
    return None


def interpolar_inversa(tabla, valor):
    """crecimiento implícito en un valor por acción (tabla estrictamente creciente en valor)."""
    pares = [(g, v) for g, v in tabla if isinstance(g, (int, float)) and isinstance(v, (int, float))]
    if len(pares) < 2:
        return None
    if valor < pares[0][1]:
        return "< -10%"
    if valor > pares[-1][1]:
        return "> 30%"
    for (g0, v0), (g1, v1) in zip(pares, pares[1:]):
        if v0 <= valor <= v1:
            return g0 if v1 == v0 else g0 + (g1 - g0) * (valor - v0) / (v1 - v0)
    return None


def es_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def calcular(res, k=K_DEFECTO, copia=False):
    val = res["valores"]
    est = res["estados"]
    notas = []
    out = {"k": k, "convencion": "escalera experimental del ejercicio (D11), k = 3; la zona no es la conclusión: no mide riesgo ni fundamento",
           "copia_de_prueba": copia}
    V = [val.get("B78"), val.get("C78"), val.get("D78")]
    p = res.get("probabilidades") or [None, None, None]
    precio = val.get("C37")
    motivo = None
    if est.get("bloqueo_valor_B252"):
        motivo = f"Motor!B252 = bloqueo del valor (estado técnico {est.get('estado_tecnico_B255')!r})"
    elif not est.get("comparable_B253"):
        motivo = "precio no comparable (moneda o unidad, Motor!B253 falso)"
    elif est.get("bloqueo_lectura_B254"):
        motivo = f"Motor!B254 = bloqueo de la lectura de precio (estado técnico {est.get('estado_tecnico_B255')!r})"
    elif any(not es_num(x) for x in V):
        motivo = f"valor por acción no numérico: {V}"
    elif not isinstance(p, (list, tuple)) or len(p) != 3 or any(not es_num(x) for x in p) or abs(sum(p) - 1) > 1e-3 or any(x < 0 for x in p):
        motivo = f"probabilidades inválidas: {p}"
    elif not es_num(precio) or precio <= 0:
        motivo = "sin precio actual positivo (Análisis!C37)"
    elif not es_num(k) or k < 1:
        motivo = f"k = {k!r} no válido (k ≥ 1)"
    if motivo:
        out.update({"sin_lectura": motivo, "V": V, "p": p, "precio": precio})
        return out, 0
    if est.get("estado_tecnico_B255") != "COMPLETO Y VÁLIDO":
        notas.append(f"estado técnico {est.get('estado_tecnico_B255')!r} (completitud pendiente, normal entre las fases B y C): escalera provisional; el valor no está bloqueado (B252/B254 falsos)")
    if not (V[0] <= V[1] <= V[2]):
        out.update({"sin_escalera": "valores desordenados", "error": "G19", "V": V, "p": p, "precio": precio})
        return out, 5
    pond = val.get("C83")
    pond_calc = sum(v * pp for v, pp in zip(V, p))
    if isinstance(pond, (int, float)) and abs(pond - pond_calc) > 1e-6 * max(1, abs(pond)):
        notas.append(f"C83 = {pond} difiere del ponderado recalculado {pond_calc:.6f}")
    pond = pond if isinstance(pond, (int, float)) else pond_calc
    P = p_estrella(V, p, k)
    assert abs(G(V, p, P) - k * L(V, p, P)) < 1e-6 * max(1.0, abs(P)), "G(P*) ≠ k·L(P*)"
    assert P >= min(V) - 1e-9 and P <= pond + 1e-9, "P* fuera de [mín V, ponderado]"
    V_normal = V[1]
    precio_si = min(P, V_normal)
    malo = V[0] if V[0] > 0 else None
    if malo is None:
        notas.append("sin precio del escenario MALO: B78 ≤ 0 (la hoja avisa V36)")
    tabla = res.get("tabla_dcf_inverso") or []
    c14 = (res.get("palancas") or {}).get("C14")
    b193 = est.get("dcf_inverso_monotono_B193")
    tabla_ok = False
    if b193 == "✓ PASA" and isinstance(c14, (int, float)) and -0.10 <= c14 <= 0.30:
        vt = interpolar(tabla, c14)
        tabla_ok = vt is not None and abs(vt - V_normal) <= 0.01 * abs(V_normal)
        if not tabla_ok:
            notas.append(f"la tabla del DCF inverso en C14 = {c14} da {vt}, no el valor NORMAL {V_normal}: crecimiento implícito no utilizable")
    else:
        notas.append(f"tabla del DCF inverso no utilizable (B193 = {b193!r}, C14 = {c14!r})")
    if tabla_ok:
        g_actual = interpolar_inversa(tabla, precio)
        g_si = interpolar_inversa(tabla, precio_si)
        c86 = val.get("C86")
        coincide_c86 = None
        if es_num(c86) and es_num(g_actual):
            coincide_c86 = abs(g_actual - c86) <= 0.005
            if not coincide_c86:
                notas.append(f"crecimiento implícito {g_actual:.4f} ≠ Análisis!C86 {c86} (tolerancia 0,5 pt, §10.2.6): fallo que verificar_todo.sh no deja pasar")
        elif isinstance(c86, str) and es_num(g_actual):
            # la hoja dice «< -10%» / «> 30%» y el script obtiene un número: se conserva el número y se anota la discrepancia
            notas.append(f"Análisis!C86 = {c86!r} (texto) frente al crecimiento implícito calculado {g_actual:.4f}: no comparable")
    else:
        g_actual = g_si = "no utilizable"
        coincide_c86 = None
    torn = res.get("tornado") or {}
    efectos = torn.get("efectos") or []
    hay_tornado = any(isinstance(e[0], (int, float)) and e[0] > 0 for e in efectos if e)
    aviso_tasa = (torn.get("mas_influyente") == ROTULO_TASA) if hay_tornado else "sin tornado"
    z = zona(precio, malo, precio_si, pond)
    out.update({
        "V": V, "p": p, "precio": precio, "P_estrella": P, "precio_si": precio_si, "tope_normal_aplicado": P > V_normal,
        "precio_escenario_malo": malo, "nota_malo": "no es un suelo de valor ni la pérdida máxima posible (D11)",
        "ponderado": pond, "zona": z, "G": G(V, p, P), "L": L(V, p, P),
        "g_impl_actual": g_actual, "g_impl_si": g_si, "tabla_dcf_inverso_ok": tabla_ok, "coincide_C86": coincide_c86,
        "C156_regla_antigua": res.get("precio_referencia_hoja_C156"),
        "distancias": {"a_precio_si": (precio - precio_si) / precio, "a_malo": ((precio - malo) / precio) if malo else None},
        "aviso_tasa_descuento_mas_influyente": aviso_tasa, "notas": notas,
    })
    return out, 0


def autotest():
    casos = [((60, 100, 150), (0.25, 0.5, 0.25), 265 / 3, 102.5, 265 / 3, 60),
             ((90, 100, 160), (0.2, 0.6, 0.2), 1330 / 13, 110, 100, 90),
             ((100, 100, 100), (0.2, 0.6, 0.2), 100, 100, 100, 100),
             ((-20, 80, 200), (0.2, 0.6, 0.2), 380 / 7, 84, 380 / 7, None),
             ((40, 70, 300), (0.3, 0.5, 0.2), 1005 / 13, 107, 70, 40)]
    fallos = []
    for V, p, Pesp, pond, psi, malo in casos:
        P = p_estrella(list(V), list(p), 3)
        if abs(P - Pesp) > 1e-9:
            fallos.append(f"P* {V}: {P} ≠ {Pesp}")
        if abs(G(V, p, P) - 3 * L(V, p, P)) > 1e-9:
            fallos.append(f"G ≠ 3L en {V}")
        if abs(min(P, V[1]) - psi) > 1e-9:
            fallos.append(f"precio de Sí {V}: {min(P, V[1])} ≠ {psi}")
        if abs(sum(v * q for v, q in zip(V, p)) - pond) > 1e-9:
            fallos.append(f"ponderado {V}")
        if (V[0] if V[0] > 0 else None) != malo:
            fallos.append(f"precio MALO {V}")
        if P < min(V) - 1e-9 or P > sum(v * q for v, q in zip(V, p)) + 1e-9:
            fallos.append(f"P* fuera de rango en {V}")
        # decrece con k
        if p_estrella(list(V), list(p), 4) > P + 1e-9:
            fallos.append(f"P* no decrece con k en {V}")
        # independiente del orden
        if abs(p_estrella([V[2], V[0], V[1]], [p[2], p[0], p[1]], 3) - P) > 1e-9:
            fallos.append(f"P* depende del orden en {V}")
    try:
        calcular({"valores": {"B78": 1, "C78": 2, "D78": 3, "C37": 2, "C83": 2}, "probabilidades": [0.5, 0.5, 0.5],
                  "estados": {"estado_tecnico_B255": "COMPLETO Y VÁLIDO", "bloqueo_valor_B252": False, "comparable_B253": True}})
        r, _ = calcular({"valores": {"B78": 1, "C78": 2, "D78": 3, "C37": 2, "C83": 2}, "probabilidades": [0.5, 0.5, 0.5],
                         "estados": {"estado_tecnico_B255": "COMPLETO Y VÁLIDO", "bloqueo_valor_B252": False, "comparable_B253": True}})
        if "sin_lectura" not in r:
            fallos.append("no se niega con probabilidades que no suman 1")
    except Exception as e:  # noqa
        fallos.append(f"excepción con probabilidades inválidas: {e}")
    for caso, res_ in (("k < 1", ({"valores": {"B78": 1, "C78": 2, "D78": 3, "C37": 2, "C83": 2}, "probabilidades": [0.2, 0.6, 0.2],
                                   "estados": {"estado_tecnico_B255": "COMPLETO Y VÁLIDO", "bloqueo_valor_B252": False, "comparable_B253": True}}, 0.5)),
                       ("precio 0", ({"valores": {"B78": 1, "C78": 2, "D78": 3, "C37": 0, "C83": 2}, "probabilidades": [0.2, 0.6, 0.2],
                                      "estados": {"estado_tecnico_B255": "COMPLETO Y VÁLIDO", "bloqueo_valor_B252": False, "comparable_B253": True}}, 3)),
                       ("booleano como número", ({"valores": {"B78": True, "C78": 2, "D78": 3, "C37": 2, "C83": 2}, "probabilidades": [0.2, 0.6, 0.2],
                                                  "estados": {"estado_tecnico_B255": "COMPLETO Y VÁLIDO", "bloqueo_valor_B252": False, "comparable_B253": True}}, 3))):
        try:
            r, _ = calcular(res_[0], k=res_[1])
            if "sin_lectura" not in r:
                fallos.append(f"no se niega con {caso}")
        except Exception as e:  # noqa
            fallos.append(f"excepción con {caso}: {e}")
    print("autotest precio_de_si: " + ("PASA (5 casos + propiedades)" if not fallos else "FALLA: " + "; ".join(fallos)))
    return 0 if not fallos else 3


def main():
    if "--autotest" in sys.argv:
        return autotest()
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    k = float(sys.argv[sys.argv.index("--k") + 1]) if "--k" in sys.argv else K_DEFECTO
    res = json.load(open(sys.argv[1], encoding="utf-8"))
    out, code = calcular(res, k=k, copia="--copia" in sys.argv)
    json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "sin_lectura" in out:
        print(f"SIN LECTURA DE PRECIO: {out['sin_lectura']} → {sys.argv[2]}")
    elif "sin_escalera" in out:
        print(f"SIN ESCALERA (error G19, valores desordenados) → {sys.argv[2]}")
    else:
        print(f"OK: precio {out['precio']} · esc. MALO {out['precio_escenario_malo']} · precio de Sí {out['precio_si']:.4f} (P* {out['P_estrella']:.4f}) · ponderado {out['ponderado']:.4f} · zona {out['zona']}")
    return code


if __name__ == "__main__":
    sys.exit(main())
