#!/usr/bin/env python3
"""Comprobaciones de la gramática (Anexo B §B.3; decisión D17) sobre las palancas del personaje v2.

Uso:
  comprobar_gramatica.py CARPETA --antes-de-recalculo            (paso 8: sobre fase_b.json)
  comprobar_gramatica.py CARPETA --tras-recalculo [--con-fase-c] (pasos 9, 10 y 12: sobre resultados.json; G13 solo con --con-fase-c)
  comprobar_gramatica.py CARPETA --tras-recalculo --copia-de-prueba (comprobación conjunta, §B.6: sobre la copia; las reglas [I]/[N]
      y de formato se aplican a los valores de la combinación; se omiten las comprobaciones G14 de coherencia clase↔valor de la
      fase B, porque la combinación cambia a propósito los valores de hipótesis «sin juicio propio» o «técnico»)
Lee de CARPETA: fase_b.json, referencias_mecanicas.json, datos_v63.json, (resultados.json, fase_c.json, fase_a.json), ../config_v2.json.
Escribe: gramatica.json y gramatica.md.
Categorías: error (bloquea; ninguna explicación lo aprueba) · límite del modelo (vuelve a la fase A) · desviación económica
(exige entrada en desviaciones_justificadas con justificación, hechos y clase fundamentada/convención) · aviso (informa).
Código de salida: 0 sin errores ni desviaciones sin justificar · 1 desviaciones sin justificar · 2 errores · 3 límite del modelo.
Si coinciden varias, prevalece el mayor (3 › 2 › 1). Código 4: el script no pudo ejecutarse (archivo ausente, excepción): el
pipeline lo trata como fallo de implementación, nunca como una desviación ni como un «sigue».
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import config_v2  # noqa: E402
ESC = ("MALO", "NORMAL", "BUENO")
PAL = ("crecimiento_1_5", "margen_objetivo", "s2c", "g_perpetuo", "roic_lp")
LISTA_G = [0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03]
LISTA_P = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6]
CELDA = {"crecimiento_1_5": ("Palancas", "B14", "C14", "D14"), "margen_objetivo": ("Palancas", "B15", "C15", "D15"), "s2c": ("Palancas", "B16", "C16", "D16"),
         "g_perpetuo": ("Análisis", "B68", "C68", "D68"), "roic_lp": ("Palancas", "B18", "C18", "D18"), "probabilidades": ("Análisis", "B69", "C69", "D69")}
CLASES = ("fundamentada", "convención", "técnico", "sin juicio propio")


def num(x):
    return x if isinstance(x, (int, float)) and not isinstance(x, bool) else None


def en_lista(x, lista):
    return any(abs(x - v) < 1e-9 for v in lista)


class Gramatica:
    def __init__(self, carpeta, modo, con_fase_c, cfg, copia=False):
        self.carpeta, self.modo, self.con_fase_c, self.cfg = carpeta, modo, con_fase_c, cfg
        self.h = []  # hallazgos
        self.fb = self._json("fase_b.json", obligatorio=True)
        self.refs = self._json("referencias_mecanicas.json", obligatorio=True)
        self.d = self._json("datos_v63.json", obligatorio=True)
        self.res = self._json("resultados.json", obligatorio=(modo == "tras")) if modo == "tras" else None
        self.fc = self._json("fase_c.json") if con_fase_c else None
        self.fa = self._json("fase_a.json")
        self.copia = bool(copia or (self.res or {}).get("copia_de_prueba"))
        self.motor = (self.res or {}).get("motor") or self.d["diagnostico"]["motor"] or self.fb.get("motor")
        just = list(self.fb.get("desviaciones_justificadas") or [])
        if self.fc:
            just += list(self.fc.get("desviaciones_justificadas") or [])
        self.just = just

    def _json(self, nombre, obligatorio=False):
        p = os.path.join(self.carpeta, nombre)
        if not os.path.exists(p):
            if obligatorio:
                raise FileNotFoundError(f"falta {p}")
            return None
        return json.load(open(p, encoding="utf-8"))

    # ---- valores ----
    def valor(self, pal, esc):
        if self.res:
            hoja, *refs = CELDA[pal]
            ref = refs[ESC.index(esc)]
            if pal == "probabilidades":
                return num(self.res["probabilidades"][ESC.index(esc)])
            if pal == "g_perpetuo":
                return num(self.res["g_perpetuo"][ESC.index(esc)])
            return num(self.res["palancas"].get(ref))
        return num(((self.fb.get("palancas") or {}).get(pal) or {}).get(esc, {}).get("valor"))

    def entrada(self, pal, esc):
        return ((self.fb.get("palancas") or {}).get(pal) or {}).get(esc) or {}

    # comprobaciones cuyo VALOR se desvía (la palanca tiene que ser fundamentada o convención para justificarlo). G8, G16 y G17 son
    # propiedades del resultado tras el recálculo que explica la fase C (tesis u Observación de B18:D18): no exigen cambiar la clase.
    PAL_DE = {"G4": "roic_lp", "G5": "margen_objetivo", "G6": "crecimiento_1_5", "G7": "s2c", "G3": "g_perpetuo", "G10b": "probabilidades"}
    # un hecho «con referencia»: celda (mayúsculas, con o sin hoja), rango, página, fila/nota/sección numeradas, Historia o extracto
    # seguidos de una celda/fila/página, o un documento con un número (año, nota). Palabras sueltas («Historia», «según el extracto») no valen.
    REF_HECHO = re.compile(r"(?:[A-Za-zÁÉÍÓÚáéíóú ]+!)?(?<![A-Za-z0-9])(?!Q[1-4](?![0-9]))[A-Z]{1,3}\d{1,3}(?![A-Za-z0-9])(?::[A-Z]{1,3}\d{1,3})?"
                           r"|(?i:\bpp?\.?\s*\d+|p[áa]g(?:ina)?s?\.?\s*\d+|\bfila\s*\d+|\bnota\s*\d+|\bsecci[óo]n\s*\d+"
                           r"|\b(?:historia|extracto)\b[^,;]{0,25}(?:fila\s*\d+|p\.?\s*\d+|[A-Z]\d)"
                           r"|\b(?:informe|cuentas|memoria|presentaci[óo]n|10-K|20-F|annual report)\b[^,;]{0,40}\d)")

    def add(self, id_, categoria, detalle, escenario=None, motores="A, B, C", consecuencia="", requiere_justificacion=False, pal=None):
        just = None
        motivo = None
        if requiere_justificacion:
            just, motivo = self.justificada(id_, escenario, pal or self.PAL_DE.get(id_))
        self.h.append({"id": id_, "categoria": categoria, "escenario": escenario, "motor": self.motor, "motores": motores, "detalle": detalle + (f" · justificación rechazada: {motivo}" if motivo else ""),
                       "requiere_justificacion": requiere_justificacion, "justificada": just, "consecuencia": consecuencia})

    def justificada(self, id_, escenario, pal=None):
        """(True/False, motivo). Una desviación solo se justifica con: entrada para esa comprobación y escenario, justificación ≥ 40
        caracteres, hechos con celda o página, clase fundamentada o convención, y la palanca afectada con clase fundamentada o
        convención en fase_b.json (una palanca «sin juicio propio» o «técnico» no puede sostener una desviación: §B.3)."""
        base = id_.rstrip("ab") if id_ in ("G1b", "G10b") else id_
        if pal and pal in PAL + ("probabilidades",):
            for e_ in ([escenario] if escenario else list(ESC)):
                clase_pal = (self.entrada(pal, e_) or {}).get("clase")
                if clase_pal in ("sin juicio propio", "técnico"):
                    return False, f"la palanca {pal} {e_} tiene clase «{clase_pal}»: no puede sostener una desviación (fundamentada o convención con hechos, o corregir)"
        candidatas = [j for j in self.just if j.get("comprobacion") in (id_, base)]
        if not candidatas:
            return False, "sin entrada en desviaciones_justificadas"
        for j in candidatas:
            e = j.get("escenario")
            if escenario and e and str(e).upper() not in (escenario, "TODOS"):
                continue
            txt = (j.get("justificacion") or "").strip()
            hechos = [str(x).strip() for x in (j.get("hechos") or []) if str(x).strip()]
            clase = j.get("clase")
            if len(txt) < 40:
                return False, "justificación de menos de 40 caracteres"
            if not hechos:
                return False, "sin hechos"
            if not any(self.REF_HECHO.search(h) for h in hechos):
                return False, "ningún hecho cita una celda, una fila de Historia o una página"
            if clase not in ("fundamentada", "convención"):
                return False, f"clase {clase!r} (solo fundamentada o convención)"
            return True, None
        return False, f"la entrada no cubre el escenario {escenario}"

    # ---- comprobaciones ----
    def correr(self):
        fb, refs, d, motor = self.fb, self.refs, self.d, self.motor
        an = d["analisis"]; anc = d["historia"]["anclas"]; sec = d["palancas"]["sector"]
        tasa = num(refs.get("tasa_del_motor"))
        if tasa is None:
            tasa = num(an.get("C56")) if motor in ("A", "C") else (num((self.res or {}).get("r_operativa_C15")) if self.res else num(d["diagnostico"].get("r_operativa")))
        if tasa is None:
            self.add("G2", "error", f"tasa del motor {motor} no disponible como número (Análisis!C56 o Diagnóstico V6!C15): N1 (g < tasa) no se puede comprobar", consecuencia="dato de entrada: fallo del pipeline o de la fase 1, nunca se da por bueno")
        rf = num(an.get("C57")); t = num(anc.get("tipo_impositivo_5")); c55 = num(anc.get("roic_medio_5")); c56a = num(an.get("C56"))
        c46 = num(anc.get("cagr_5")); c51 = num(anc.get("margen_max")); q3c = num(sec.get("crecimiento_q3")); q3m = num(sec.get("margen_q3"))
        c18 = an.get("C18") if not self.res else (self.res.get("celdas_juicio_analisis") or {}).get("C18", an.get("C18"))
        c6 = d["palancas"].get("C6"); c62 = an.get("C62") if not self.res else (self.res.get("celdas_juicio_analisis") or {}).get("C62", an.get("C62"))
        c43 = d["palancas"].get("C43") if not self.res else (self.res.get("palancas") or {}).get("C43")
        V = {pal: {e: self.valor(pal, e) for e in ESC} for pal in PAL + ("probabilidades",)}
        # --- límites del modelo ---
        if c62 == "No · este tipo de empresa requiere otro método":
            self.add("L3", "límite del modelo", "Análisis!C62 = «otro método»: ningún motor valora esta empresa", motores="—", consecuencia="modelo_no_aplicable")
        if motor == "A" and c43 == "Estructural":
            self.add("L1", "límite del modelo", "FCF base ≤ 0 estructural con motor A", motores="A", consecuencia="la fase A elige B si la financiación lo permite; si no, modelo_no_aplicable")
        if c6 == "Financiera (banco o aseguradora)" and motor in ("A", "B"):
            self.add("G18", "límite del modelo", f"motor {motor} con Palancas!C6 = Financiera", motores="A, B", consecuencia="vuelve a la fase A (código 3): corrige el motor o declara L2")
        # --- valores presentes y campos (G14) ---
        for pal in PAL + ("probabilidades",):
            if pal == "s2c" and motor == "C":
                for e in ESC:
                    if V["s2c"][e] is not None:
                        self.add("G18", "error", f"motor C con S2C informado en {e} (Palancas B16:D16 deben quedar vacías)", e, "C", "la fase B las vacía")
                continue
            for e in ESC:
                ent = self.entrada(pal, e)
                v = V[pal][e]
                if v is None:
                    self.add("G14" if pal != "probabilidades" else "G10a", "error", f"{pal} {e}: sin valor numérico", e, consecuencia="corregir en la fase B")
                    continue
                faltan = [k for k in ("referencia_mecanica", "valor", "desviacion", "clase", "confianza", "porque", "lo_sustituiria") if k not in ent]
                if faltan:
                    self.add("G14", "error", f"{pal} {e}: faltan campos {faltan}", e, consecuencia="corregir en la fase B")
                clase = ent.get("clase")
                if clase not in CLASES:
                    self.add("G14", "error", f"{pal} {e}: clase {clase!r} no válida", e, consecuencia="corregir en la fase B")
                ref = ent.get("referencia_mecanica"); refm = (refs["palancas"].get(pal) or {}).get(e)
                if ref is not None and refm is not None and abs(ref - refm) > 1e-9:
                    self.add("G14", "error", f"{pal} {e}: referencia_mecanica {ref} ≠ la calculada {refm}", e, consecuencia="corregir en la fase B (no se inventa la referencia)")
                if clase == "sin juicio propio" and (ref is None or refm is None):
                    self.add("G14", "error", f"{pal} {e}: clase «sin juicio propio» sin referencia disponible", e, consecuencia="clase técnico con rango, o fundamentada")
                if clase == "técnico" and refm is not None:
                    self.add("G14", "error", f"{pal} {e}: clase «técnico» con referencia disponible ({refm}); «técnico» es solo para celdas sin referencia", e, consecuencia="sin juicio propio (copiando) o fundamentada/convención")
                if not self.copia:
                    # coherencia clase ↔ valor de la fase B (en la copia de prueba la combinación cambia estos valores a propósito, §B.6)
                    if clase == "sin juicio propio" and refm is not None and abs(v - refm) > 1e-9:
                        self.add("G14", "error", f"{pal} {e}: clase «sin juicio propio» con desviación ({v} ≠ {refm})", e, consecuencia="copiar la referencia o cambiar la clase")
                    if self.res:
                        vfb = num(ent.get("valor"))
                        if vfb is not None and abs(vfb - v) > 1e-9:
                            self.add("G14", "error", f"{pal} {e}: el libro tiene {v} y fase_b.json {vfb} (escritura incoherente)", e, consecuencia="fallo de implementación: no_entregable si persiste")
                    dv = num(ent.get("desviacion")); vfb = num(ent.get("valor"))
                    if refm is not None and vfb is not None and dv is not None and abs(dv - (vfb - refm)) > 1e-6:
                        self.add("G14", "error", f"{pal} {e}: desviacion {dv} ≠ valor − referencia ({vfb} − {refm})", e, consecuencia="corregir en la fase B")
                if pal == "probabilidades":
                    continue
                # G15 redondeo (también sobre la combinación de la copia: la fase C usa las listas y los redondeos de la hoja)
                paso = {"crecimiento_1_5": 0.005, "margen_objetivo": 0.005, "s2c": 0.1, "g_perpetuo": 0.005, "roic_lp": 0.01}[pal]
                paso = self.cfg.get("convenciones", {}).get("redondeo", {}).get({"crecimiento_1_5": "crecimiento", "margen_objetivo": "margen", "s2c": "s2c", "roic_lp": "roic"}.get(pal, "crecimiento"), paso) if pal != "g_perpetuo" else 0.005
                if abs(v / paso - round(v / paso)) > 1e-6:
                    self.add("G15", "error", f"{pal} {e} = {v}: más precisión que el redondeo {paso}", e, consecuencia="cifra redonda (§B.2)")
        for e in ESC:
            p = V["probabilidades"][e]
            if p is None:
                self.add("G10a", "error", f"probabilidad {e} sin valor", e, consecuencia="corregir")
        # --- orden (G1a error / G1b desviación) ---
        def ordenada(pal):
            vs = [V[pal][e] for e in ESC]
            return all(x is not None for x in vs) and vs[0] <= vs[1] <= vs[2]
        for pal, nombre in (("crecimiento_1_5", "crecimiento"), ("margen_objetivo", "margen/ROE objetivo")):
            if all(V[pal][e] is not None for e in ESC) and not ordenada(pal):
                self.add("G1a", "error", f"{nombre} desordenado entre escenarios: {[V[pal][e] for e in ESC]}", consecuencia="corregir en la fase B")
        for pal, nombre in (("s2c", "S2C"), ("g_perpetuo", "g para siempre"), ("roic_lp", "ROIC/ROE largo plazo")):
            if pal == "s2c" and motor == "C":
                continue
            if all(V[pal][e] is not None for e in ESC) and not ordenada(pal):
                self.add("G1b", "desviación", f"{nombre} desordenado entre escenarios: {[V[pal][e] for e in ESC]}", requiere_justificacion=True,
                         consecuencia="justificar por qué un escenario peor reinvierte o rinde mejor, o corregir")
        # --- G2 (N1, N2) ---
        for e in ESC:
            g = V["g_perpetuo"][e]; r_lp = V["roic_lp"][e]
            if g is not None and tasa is not None and g >= tasa:
                self.add("G2", "error", f"g para siempre {e} = {g} ≥ tasa del motor {tasa} (N1)", e, consecuencia="corregir")
            if g is not None and r_lp is not None and r_lp <= g:
                self.add("G2", "error", f"ROIC/ROE largo plazo {e} = {r_lp} ≤ g {g} (N2)", e, consecuencia="corregir")
            if g is not None and rf is not None and g > rf + 1e-9:
                self.add("G3", "desviación", f"g para siempre {e} = {g} > rf {rf} (E1)", e, requiere_justificacion=True, consecuencia="justificar con el crecimiento nominal esperado de la economía donde vende")
            if g is not None and not en_lista(g, LISTA_G):
                self.add("G10a", "error", f"g para siempre {e} = {g} fuera de la lista", e, consecuencia="corregir")
        # --- G4 ROIC LP ---
        for e in ESC:
            r_lp = V["roic_lp"][e]
            if r_lp is not None and c56a is not None and r_lp > c56a + 0.10 + 1e-9:
                if c18 != "Sí":
                    self.add("G4", "desviación", f"ROIC/ROE largo plazo {e} = {r_lp} > C56 + 0,10 = {c56a + 0.10:.3f} con C18 (foso) = {c18!r}: no justificable sin foso", e,
                             requiere_justificacion=True, consecuencia="con foso ≠ Sí no hay justificación posible: bajar el ROIC")
                    self.h[-1]["justificada"] = False
                else:
                    self.add("G4", "desviación", f"ROIC/ROE largo plazo {e} = {r_lp} > C56 + 0,10 = {c56a + 0.10:.3f} (E2; umbral de la plantilla)", e,
                             requiere_justificacion=True, consecuencia="justificar cuánto dura la ventaja y qué la sostiene")
        # --- G5 margen ---
        for e in ESC:
            m = V["margen_objetivo"][e]
            if m is None:
                continue
            if motor == "C":
                sroe = num(sec.get("roic_media"))
                if sroe is not None and m > 1.5 * sroe + 1e-9:
                    self.add("G5", "desviación", f"ROE objetivo {e} = {m} > 1,5 × ROE del sector ({sroe})", e, "C", requiere_justificacion=True, consecuencia="justificar el mecanismo")
            else:
                if (c51 is not None and m > c51 + 1e-9) or (q3m is not None and m > q3m + 1e-9):
                    self.add("G5", "desviación", f"margen objetivo {e} = {m} > máximo histórico ({c51}) o Q3 del sector ({q3m})", e, "A, B", requiere_justificacion=True,
                             consecuencia="justificar con el mecanismo (precio, mezcla, escala) y quién se queda la mejora")
        # --- G6 crecimiento ---
        for e in ESC:
            g5 = V["crecimiento_1_5"][e]
            if g5 is None:
                continue
            if (q3c is not None and g5 > q3c + 1e-9) or (c46 is not None and c46 > 0 and g5 > 1.5 * c46 + 1e-9):
                self.add("G6", "desviación", f"crecimiento 1–5 {e} = {g5} > Q3 del sector ({q3c}) o > 1,5 × historia ({c46})", e, requiere_justificacion=True,
                         consecuencia="justificar por componentes (unidades, precio, mezcla) y dónde se reinvierte")
        # --- G7, G9 S2C ---
        if motor in ("A", "B"):
            for e in ESC:
                s = V["s2c"][e]; m = V["margen_objetivo"][e]
                if s is None:
                    continue
                if s <= 0:
                    self.add("G9", "error", f"S2C {e} = {s} ≤ 0 (N3)", e, "A, B", consecuencia="corregir")
                elif m is not None and t is not None and c55 is not None and s * m * (1 - t) > 2 * c55 + 1e-9:
                    self.add("G7", "desviación", f"rentabilidad marginal {e} = S2C {s} × margen {m} × (1 − {t:.3f}) = {s * m * (1 - t):.3f} > 2 × ROIC histórico ({2 * c55:.3f})", e, "A, B",
                             requiere_justificacion=True, consecuencia="justificar por qué cada euro nuevo rendiría el doble que la historia")
        # --- G10 probabilidades ---
        ps = [V["probabilidades"][e] for e in ESC]
        if all(p is not None for p in ps):
            if abs(sum(ps) - 1) > 1e-6 or not all(en_lista(p, LISTA_P) for p in ps):
                self.add("G10a", "error", f"probabilidades {ps}: fuera de la lista o no suman 1 (N4)", consecuencia="corregir")
            if ps[2] > ps[0] + 1e-9:
                self.add("G10b", "desviación", f"p(BUENO) {ps[2]} > p(MALO) {ps[0]} (S-6)", requiere_justificacion=True, consecuencia="justificar con una razón estructural escrita")
        # --- G11 quiebra ---
        q = fb.get("quiebra") or {}
        c22 = num((self.res or {}).get("palancas", {}).get("C22")) if self.res else num(q.get("C22"))
        if c22 is not None and c22 > 0:
            if not (q.get("disparadores") or []):
                self.add("G11", "desviación", f"C22 = {c22} sin disparador declarado", requiere_justificacion=True, consecuencia="declarar el disparador o quitar la quiebra (E6)")
            obs_r = str(((self.fa or {}).get("observaciones") or {}).get("C56") or "")
            # segunda condición de G11: la Observación de r afirma (no niega) que r ya incluye una prima de quiebra
            for frase in re.split(r"[.;\n]", obs_r):
                if re.search(r"quiebra", frase, re.I) and re.search(r"\b(incluye|lleva|contiene|incorpora|recoge|con)\b", frase, re.I) \
                        and not re.search(r"\b(no|sin|ni|tampoco)\s+(?:\w+\s+){0,3}(incluye|lleva|contiene|incorpora|recoge|prima)", frase, re.I):
                    self.add("G11", "desviación", f"C22 = {c22} y la Observación de r (C56) dice que r ya incluye una prima de quiebra («{frase.strip()[:80]}»): doble cuenta (E6)", requiere_justificacion=True, consecuencia="justificar o quitar la doble cuenta")
                    break
            if c22 > 1:
                self.add("G10a", "error", f"C22 = {c22} fuera de [0, 1]", consecuencia="corregir")
            c23 = num((self.res or {}).get("palancas", {}).get("C23")) if self.res else num(q.get("C23"))
            if c23 is None or c23 < 0:
                self.add("G10a", "error", f"C23 = {c23!r} con C22 > 0: debe ser un número ≥ 0", consecuencia="corregir")
        # --- G12 C76 ---
        c76 = num((self.res or {}).get("valores", {}).get("C76")) if (self.res and "C76" in (self.res.get("valores") or {})) else num((fb.get("exceso_caja") or {}).get("C76"))
        c53_caja = num(an.get("C53"))
        if motor in ("B", "C") and c76 not in (None, 0):
            self.add("G12", "error", f"C76 = {c76} informado con motor {motor}", motores="B, C", consecuencia="vaciar C76")
        if motor == "A" and c76 is not None and c53_caja is not None and c76 > c53_caja + 1e-9:
            self.add("G12", "error", f"C76 = {c76} > caja del balance C53 = {c53_caja} (N5)", motores="A", consecuencia="corregir")
        # --- G13 predicciones (solo tras la fase C) ---
        if self.con_fase_c and self.fc:
            celdas = self.fc.get("celdas") or {}
            fecha0 = an.get("D4")
            try:
                f0 = dt.date.fromisoformat(str(fecha0)[:10])
            except Exception:
                f0 = None
            if f0 is None:
                self.add("G13", "error", f"fecha de análisis (Análisis!D4 = {fecha0!r}) ausente o no ISO: la ventana de 12–24 meses no se puede comprobar", consecuencia="dato de la fase 1: corregir D4")

            def sumar_meses(f, n):
                m = f.month - 1 + n
                y = f.year + m // 12
                m = m % 12 + 1
                import calendar
                return dt.date(y, m, min(f.day, calendar.monthrange(y, m)[1]))
            for i in (38, 39, 40):
                txt = celdas.get(f"Palancas!A{i}"); fch = celdas.get(f"Palancas!B{i}"); pr = num(celdas.get(f"Palancas!C{i}"))
                if not txt or not fch or pr is None or not 0 <= pr <= 1:
                    self.add("G13", "error", f"predicción {i - 37}: texto, fecha o probabilidad ausentes o fuera de [0, 1]", consecuencia="corregir en la fase C")
                    continue
                if f0:
                    try:
                        f1 = dt.date.fromisoformat(str(fch)[:10])
                        if not (sumar_meses(f0, 12) <= f1 <= sumar_meses(f0, 24)):
                            self.add("G13", "error", f"predicción {i - 37}: fecha {fch} fuera de la ventana [{sumar_meses(f0, 12)}, {sumar_meses(f0, 24)}] (12–24 meses desde {f0})", consecuencia="corregir en la fase C")
                    except Exception:
                        self.add("G13", "error", f"predicción {i - 37}: fecha {fch!r} no válida", consecuencia="corregir en la fase C")
                if re.search(r"cotizaci|precio de la acci|precio objetivo|PIB|inflaci|tipos de inter", str(txt), re.I):
                    self.add("G13", "error", f"predicción {i - 37} habla del precio de la acción o de macro: «{str(txt)[:60]}»", consecuencia="predicción sobre el negocio")
        # --- tras recálculo: G8, G16, G17, G19 y avisos ---
        if self.res:
            vals = self.res["valores"]
            b78, c78, d78 = num(vals.get("B78")), num(vals.get("C78")), num(vals.get("D78"))
            if None not in (b78, c78, d78) and not (b78 <= c78 <= d78):
                self.add("G19", "error", f"valores por acción desordenados: {b78}, {c78}, {d78} (N6)", consecuencia="vuelta a la fase B una vez; si persiste, no_entregable")
            filas = (self.res.get("salto_anio_11") or {}).get("filas") or []
            salto = filas[4][1:4] if len(filas) > 4 else [None, None, None]
            umbral = num(self.res.get("parametros_hoja", {}).get("C179")) or 0.05
            if motor in ("A", "B"):
                for e, sv in zip(ESC, salto):
                    if num(sv) is not None and abs(sv) > umbral + 1e-9:
                        self.add("G8", "desviación", f"salto del año 11 {e} = {sv:.3f} (> {umbral}): la rentabilidad marginal de los años 1–10 y el ROIC terminal se separan", e, "A, B",
                                 requiere_justificacion=True, consecuencia="la tesis o la Observación de B18:D18 explica la pérdida (o ganancia) de ventaja en el año 11")
            peso = (self.res.get("por_escenario") or {}).get("peso_terminal") or [None, None, None]
            if num(peso[1]) is not None and peso[1] > 0.75:
                self.add("G16", "desviación", f"peso del terminal en el NORMAL = {peso[1]:.2%} > 75 %", "NORMAL", requiere_justificacion=True, consecuencia="la fase C explica por qué el valor lejano es defendible")
            cuota = (self.res.get("por_escenario") or {}).get("cuota_implicita") or [None, None, None]
            for e, cu in zip(ESC, cuota):
                if num(cu) is not None and cu > 0.30:
                    self.add("G17", "desviación", f"cuota implícita {e} = {cu:.1%} > 30 %", e, "A, B", requiere_justificacion=True, consecuencia="justificar o revisar el BUENO")
            sem = self.res.get("semaforos") or {}
            def no_pasa(fila):
                x = sem.get(fila) or [None, None, None, None]
                return any(isinstance(v, str) and v and "PASA" not in v and v != "—" for v in x[1:])
            if no_pasa("fila46"):
                self.add("A1", "aviso", f"S2C medio fuera del rango del sector: {sem['fila46'][2]}", motores="A, B", consecuencia="se informa")
            if no_pasa("fila48"):
                self.add("A2", "aviso", f"r frente a r mínima: {sem['fila48'][2]}", consecuencia="se informa (r heredada, S-3)")
            if no_pasa("fila49"):
                self.add("A4", "aviso", f"tipo de empresa frente a motor: {sem['fila49'][2]}", consecuencia="se informa")
            if no_pasa("fila50"):
                self.add("A6", "aviso", f"f fuera de rango: {sem['fila50'][2]}", motores="A", consecuencia="la fase A revisa el FCF base y considera el motor B")
            for r_ in self.res.get("reglas_motor") or []:
                if r_.get("id") == "V28" and r_.get("resultado") not in ("OK", "N/A"):
                    self.add("A3", "aviso", f"fechas del precio y de las acciones: {r_.get('causa')}", consecuencia="se informa")
            torn = self.res.get("tornado") or {}
            if torn.get("mas_influyente") == "Tasa de descuento (±1 pt)" and any(num(x[0]) for x in (torn.get("efectos") or []) if x):
                self.add("A5", "aviso", "la palanca más influyente del tornado es la tasa de descuento (r heredada)", consecuencia="la ficha dice que el valor depende sobre todo de la r exigida")
        if c6 in ("Regulada (red, concesión)", "Multinegocio o conglomerado"):
            self.add("A4", "aviso", f"Palancas!C6 = {c6}", consecuencia="se informa; conglomerado: Munger suele llevarlo a Demasiado difícil")
        return self.h

    def codigo(self):
        cats = [x["categoria"] for x in self.h]
        if "límite del modelo" in cats:
            return 3
        if "error" in cats:
            return 2
        if any(x["categoria"] == "desviación" and not x["justificada"] for x in self.h):
            return 1
        return 0


def escribir(g, carpeta):
    code = g.codigo()
    out = {"modo": g.modo, "con_fase_c": g.con_fase_c, "motor": g.motor, "codigo": code, "hallazgos": g.h,
           "resumen": {"errores": sum(1 for x in g.h if x["categoria"] == "error"), "limites": sum(1 for x in g.h if x["categoria"] == "límite del modelo"),
                       "desviaciones": sum(1 for x in g.h if x["categoria"] == "desviación"), "desviaciones_sin_justificar": sum(1 for x in g.h if x["categoria"] == "desviación" and not x["justificada"]),
                       "avisos": sum(1 for x in g.h if x["categoria"] == "aviso")}}
    json.dump(out, open(os.path.join(carpeta, "gramatica.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = [f"# Gramática · modo {g.modo}{' (con fase C)' if g.con_fase_c else ''} · motor {g.motor} · código {code}\n",
          "Categorías (D17): **error** bloquea y ninguna explicación lo aprueba · **límite del modelo** vuelve a la fase A · **desviación** exige evidencia y razonamiento específicos en `desviaciones_justificadas` (justificación ≥ 40 caracteres, `hechos` no vacío, clase fundamentada o convención) · **aviso** informa.\n"]
    for cat in ("límite del modelo", "error", "desviación", "aviso"):
        xs = [x for x in g.h if x["categoria"] == cat]
        md.append(f"## {cat} ({len(xs)})\n")
        for x in xs:
            j = "" if not x["requiere_justificacion"] else (" · **justificada**" if x["justificada"] else " · **SIN JUSTIFICAR**")
            md.append(f"- **{x['id']}**{' · ' + x['escenario'] if x['escenario'] else ''} · {x['detalle']} → {x['consecuencia']}{j}")
        if not xs:
            md.append("- ninguno")
        md.append("")
    open(os.path.join(carpeta, "gramatica.md"), "w", encoding="utf-8").write("\n".join(md))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("--antes-de-recalculo", action="store_true")
    ap.add_argument("--tras-recalculo", action="store_true")
    ap.add_argument("--con-fase-c", action="store_true")
    ap.add_argument("--copia-de-prueba", action="store_true", help="comprobación conjunta (§B.6): sobre la copia de prueba")
    ap.add_argument("--config", default=os.path.join(AQUI, "..", "config_v2.json"))
    a = ap.parse_args()
    if a.antes_de_recalculo == a.tras_recalculo:
        print("elige --antes-de-recalculo o --tras-recalculo")
        return 2
    try:
        cfg = config_v2.cargar(a.config)
        g = Gramatica(a.carpeta, "antes" if a.antes_de_recalculo else "tras", a.con_fase_c, cfg, copia=a.copia_de_prueba)
        g.correr()
        out = escribir(g, a.carpeta)
    except Exception as e:  # noqa: BLE001 — un fallo del propio script no es una desviación ni un «sigue»: código 4
        print(f"FALLO del script (código 4, fallo de implementación): {type(e).__name__}: {e}")
        return 4
    r = out["resumen"]
    print(f"código {out['codigo']} · errores {r['errores']} · límites {r['limites']} · desviaciones {r['desviaciones']} (sin justificar {r['desviaciones_sin_justificar']}) · avisos {r['avisos']} → gramatica.md")
    return out["codigo"]


if __name__ == "__main__":
    sys.exit(main())
