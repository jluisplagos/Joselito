#!/usr/bin/env python3
"""Orquestador del pipeline por empresa (encargo §4.7, pasos 0–14). Una orden por paso; cada paso deja un archivo.

Uso: pipeline.py CARPETA_EMPRESA [--config config_v2.json] [--agentes-simulados DIR] [--hasta N] [--reiniciar] [--desde N]

CARPETA_EMPRESA contiene: etapa1/<E>_evaluada.xlsx (+ respuesta.md, juicio.json, extracto.md), fase1_v63.json, texto/ (opcional).
Los pasos de agente (5 extracción, 6 fase A, 8 fase B, 10 fase C en dos turnos, 13 verificación) NO se ejecutan aquí: el pipeline
escribe prompts_generados/<paso>.md con el prompt y las entradas, deja ESPERANDO.md y termina con código 10. Cuando el archivo
de salida del agente exista (fase_a.json, fase_b.json, fase_c.json, extracto_v63.md, auditoria.md), se vuelve a lanzar y continúa.
Con --agentes-simulados DIR, toma de DIR los archivos de los agentes (fase_a.json, fase_b.json, fase_b.intento2.json, fase_c.turno1.json,
fase_c.turno2.json, auditoria.md …) para las pruebas con datos sintéticos (§10.2).
Estados finales: concluido · pendiente_de_datos · pendiente_de_investigacion · modelo_no_aplicable · no_entregable. Agotar un límite
de correcciones NUNCA aprueba: termina en no_entregable con diagnostico.md (D17, D18).
Códigos: 0 terminado (cualquier estado final, con sus salidas) · 10 esperando a un agente · 2 uso · 1 fallo mecánico no previsto.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import config_v2  # noqa: E402
import celdas_v2 as C  # noqa: E402

PY = sys.executable


class Esperando(Exception):
    pass


class Pipeline:
    def __init__(self, carpeta, cfg, simulados=None):
        self.c = os.path.abspath(carpeta)
        self.E = os.path.basename(self.c)
        self.cfg = cfg
        self.sim = simulados
        self.lim = cfg.get("limites", {})
        # perfil de LibreOffice propio de cada empresa (recalc.sh lo crea): dos soffice sobre el mismo perfil se bloquean (§4.7, en paralelo)
        self.perfil = os.path.join(self.c, ".lo_perfil") if cfg.get("recalc", {}).get("perfil_por_empresa", True) else cfg.get("recalc", {}).get("perfil", os.path.join(self.c, ".lo_perfil"))
        self.estado_path = os.path.join(self.c, "estado_pipeline.json")
        self.st = json.load(open(self.estado_path, encoding="utf-8")) if os.path.exists(self.estado_path) else {
            "paso": 0, "estado_analisis": None, "intentos": {"fase_b": 0, "fase_c": 0, "auditoria": 0, "vueltas_c_a_b": 0, "vueltas_b_a_a": 0},
            "historial": [], "motor": None, "fase_b_escrita": False, "fase_c_escrita": False, "esperando": None, "inicio": dt.datetime.now().isoformat(timespec="seconds")}

    # ---------- utilidades ----------
    def p(self, *x):
        return os.path.join(self.c, *x)

    def guardar(self):
        json.dump(self.st, open(self.estado_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    def log(self, msg):
        self.st["historial"].append(f"{dt.datetime.now().isoformat(timespec='seconds')} · paso {self.st['paso']} · {msg}")
        print(f"[paso {self.st['paso']}] {msg}")
        self.guardar()

    def run(self, cmd, ok=(0,)):
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=self.c)
        salida = (r.stdout + r.stderr).strip()
        self.st["historial"].append(f"  $ {' '.join(os.path.basename(str(x)) for x in cmd)} → {r.returncode} · {salida.splitlines()[-1][:200] if salida else ''}")
        return r.returncode, salida

    def script(self, nombre):
        return os.path.join(AQUI, nombre)

    def comprobaciones_dagger(self):
        """Criterios † de §10.2 (1 y 3), exigidos en todos los estados: libro evaluado íntegro y celdas de las fases escritas
        correctas. Devuelve None si pasan (o no hay libro evaluado todavía) o el detalle del fallo."""
        libro_ev = self.p(f"{self.E}_v63_evaluada.xlsx")
        libro_datos = self.p(f"{self.E}_v63_datos.xlsx")
        if not os.path.exists(libro_ev):
            return None
        rc, out = self.run([PY, self.cfg["plantilla"]["verificador"], libro_ev, self.cfg["plantilla"]["referencia"]])
        if rc != 0:
            return "criterio 1 †: verificar_v63.py sobre el libro evaluado: " + out[-300:]
        fases = "A" + (",B" if self.st.get("fase_b_escrita") else "") + (",C" if self.st.get("fase_c_escrita") else "")
        if os.path.exists(libro_datos):
            # el motor de la fase A manda sobre las reglas condicionales (C76, B16:D16) aunque C62 se haya corregido a «otro método»
            rc, out = self.run([PY, self.script("comprobar_celdas_v2.py"), libro_ev, libro_datos, "--fases", fases] + (["--motor", self.st["motor"]] if self.st.get("motor") else []))
            if rc != 0:
                return f"criterio 3 †: comprobar_celdas_v2.py (fases {fases}): " + out[-300:]
        return None

    def terminar(self, estado, tipo, detalle, paso, comprobacion=None, categoria=None, que_hace_falta="", desde=None):
        if estado != "no_entregable":
            fallo = self.comprobaciones_dagger()
            if fallo:
                self.log(f"el estado {estado} no se puede entregar: {fallo[:160]}")
                estado, tipo, detalle = "no_entregable", "fallo_de_implementacion", f"{fallo} (estado previsto: {estado}; {detalle})"
        self.st["estado_analisis"] = estado
        self.guardar()
        self.run([PY, self.script("diagnostico.py"), self.c, "--estado", estado, "--tipo", tipo, "--detalle", detalle, "--paso", str(paso)]
                 + (["--comprobacion", comprobacion] if comprobacion else []) + (["--categoria", categoria] if categoria else [])
                 + ["--que-hace-falta", que_hace_falta or detalle, "--desde-paso", str(desde if desde is not None else paso)])
        self.salidas_finales()
        self.log(f"FIN · estado {estado} · {tipo}: {detalle[:160]}")

    def salidas_finales(self):
        if self.st.get("estado_analisis") == "concluido":
            # un diagnóstico de una ejecución anterior no debe quedar junto a un resultado concluido (p. ej. al reanudar con --desde)
            for f in ("diagnostico.md", "diagnostico.json"):
                if os.path.exists(self.p(f)):
                    os.replace(self.p(f), self.p(f + ".anterior"))
        self.run([PY, self.script("ficha.py"), self.c, "--estado", self.st["estado_analisis"]])
        rc, out = self.run([PY, self.script("validar_esquema.py"), self.p("ficha.json"), "ficha", "--salida", self.p("esquema_ficha.json.txt")])
        self.st["ficha_valida"] = rc == 0
        if rc != 0 and self.st["estado_analisis"] != "no_entregable":
            # criterio 7 †: una ficha que no cumple su esquema es un fallo de implementación, no un aviso
            previo = self.st["estado_analisis"]
            self.st["estado_analisis"] = "no_entregable"
            self.guardar()
            self.run([PY, self.script("diagnostico.py"), self.c, "--estado", "no_entregable", "--tipo", "fallo_de_implementacion",
                      "--detalle", f"ficha.json no cumple su esquema (criterio 7 †; estado previsto: {previo}): " + out[-300:], "--paso", str(self.st.get("paso", 14)),
                      "--que-hace-falta", "corregir ficha.py o el esquema (ver esquema_ficha.json.txt)", "--desde-paso", str(self.st.get("paso", 14))])
            self.run([PY, self.script("ficha.py"), self.c, "--estado", "no_entregable"])
            rc2, _ = self.run([PY, self.script("validar_esquema.py"), self.p("ficha.json"), "ficha", "--salida", self.p("esquema_ficha.json.txt")])
            self.st["ficha_valida"] = rc2 == 0
            self.log(f"ficha.json no cumplía su esquema: estado {previo} → no_entregable")
        self.run([PY, self.script("informe.py"), self.c])
        csv = self.cfg.get("resumen_csv") or os.path.join(os.path.dirname(self.c), "resumen_v2.csv")
        self.run([PY, self.script("resumen.py"), self.c, csv])

    def consumir(self, salida):
        """Registra que la salida actual del agente ya se usó: una petición posterior del mismo archivo exige uno más nuevo
        (vuelta C→B, vuelta B→A, auditoría tras una corrección de la fase C)."""
        destino = self.p(salida)
        self.st.setdefault("consumidos", {})[salida] = os.path.getmtime(destino) if os.path.exists(destino) else 0
        self.st["esperando"] = None
        self.st["motivo_correccion"] = None
        self.guardar()

    def agente(self, paso, nombre, salida, entradas, alternativas=()):
        """Si existe una salida del agente NUEVA (o una simulada), la consume y sigue; si no, deja el prompt y ESPERANDO.md
        y lanza Esperando. Tras pedir una corrección (pedir_correccion), exige un archivo más nuevo que la petición; tras
        consumir una salida, exige un archivo más nuevo que el consumido (nunca se relee la misma salida como si fuera otra)."""
        destino = self.p(salida)
        marca = f"{paso}:{salida}"
        if self.sim:
            for alt in list(alternativas) + [salida]:
                src = os.path.join(self.sim, alt)
                if os.path.exists(src):
                    shutil.copy(src, destino)
                    os.utime(destino, None)
                    self.log(f"agente simulado: {alt} → {salida}")
                    self.consumir(salida)
                    return
        consumido = self.st.get("consumidos", {}).get(salida)
        if os.path.exists(destino):
            mt = os.path.getmtime(destino)
            if self.st.get("esperando") == marca:
                if mt >= self.st.get("esperando_desde", 0) and (consumido is None or mt > consumido):
                    self.consumir(salida)
                    return
            elif consumido is None or mt > consumido:
                self.consumir(salida)
                return
        motivo = self.st.get("motivo_correccion") if self.st.get("esperando") == marca else None
        self.escribir_prompt(paso, nombre, salida, entradas, motivo)
        if self.st.get("esperando") != marca or "esperando_desde" not in self.st:
            self.st["esperando_desde"] = dt.datetime.now().timestamp()
        self.st["esperando"] = marca
        self.guardar()
        raise Esperando(f"{nombre} → {salida}")

    def validar_esquema(self, archivo, esquema, paso, nombre, turno=None):
        """Valida la salida de un agente contra su esquema (Anexo D). Inválida → corrección al mismo agente; agotadas
        max_correcciones_esquema (2) → no_entregable (nunca se sigue con un JSON que no cumple el esquema). Devuelve
        None si es válida, "continuar" si se pidió corrección, o "fin" si terminó."""
        cmd = [PY, self.script("validar_esquema.py"), self.p(archivo), esquema] + (["--turno", str(turno)] if turno else []) + ["--salida", self.p(f"esquema_{archivo}.txt")]
        rc, out = self.run(cmd)
        if rc == 0:
            return None
        if rc != 1:
            return self.terminar("no_entregable", "fallo_de_implementacion", f"validar_esquema.py no pudo validar {archivo}: " + out[-300:], paso) or "fin"
        clave = f"esquema_{nombre}"
        self.st["intentos"][clave] = self.st["intentos"].get(clave, 0) + 1
        if self.st["intentos"][clave] > self.lim.get("max_correcciones_esquema", 2):
            self.terminar("no_entregable", "fallo_de_implementacion", f"{archivo} ({nombre}) no cumple su esquema tras {self.lim.get('max_correcciones_esquema', 2)} correcciones: " + out[-300:], paso,
                          que_hace_falta=f"revisar el prompt de {nombre} (esquema del Anexo D) · ver esquema_{archivo}.txt", desde=paso)
            return "fin"
        self.pedir_correccion(paso, nombre, archivo, f"{archivo} no cumple el esquema del Anexo D (ver esquema_{archivo}.txt): " + out[:600])
        self.log(f"esquema de {archivo} inválido: corrección {self.st['intentos'][clave]} a {nombre}")
        return "continuar"

    def correccion_formato(self, archivo, paso, nombre, motivo):
        """Defecto de formato de una salida de agente detectado después del esquema (claves de celdas, Observaciones, vocabulario):
        corrección al mismo agente con el contador de esquema (max_correcciones_esquema por agente); agotado → no_entregable."""
        clave = f"esquema_{nombre}"
        self.st["intentos"][clave] = self.st["intentos"].get(clave, 0) + 1
        if self.st["intentos"][clave] > self.lim.get("max_correcciones_esquema", 2):
            self.terminar("no_entregable", "fallo_de_implementacion", f"{archivo} ({nombre}) sigue fuera de formato tras {self.lim.get('max_correcciones_esquema', 2)} correcciones: {motivo[:300]}", paso,
                          que_hace_falta=f"revisar el prompt de {nombre} (Anexo A / Anexo D)", desde=paso)
            return "fin"
        self.st["paso"] = paso
        self.pedir_correccion(paso, nombre, archivo, motivo[:600])
        self.log(f"formato de {archivo}: corrección {self.st['intentos'][clave]} a {nombre}")
        return "continuar"

    def pedir_correccion(self, paso, nombre, salida, motivo):
        self.st["esperando"] = f"{paso}:{salida}"
        self.st["esperando_desde"] = dt.datetime.now().timestamp()
        self.st["motivo_correccion"] = motivo
        self.escribir_prompt(paso, nombre, salida, ["gramatica.md / motivo de la corrección"], motivo)
        self.guardar()

    def escribir_prompt(self, paso, nombre, salida, entradas, motivo=None):
        os.makedirs(self.p("prompts_generados"), exist_ok=True)
        plantilla = os.path.join(AQUI, "..", "prompts", f"{nombre}.md")
        texto = open(plantilla, encoding="utf-8").read() if os.path.exists(plantilla) else f"(prompt de {nombre}: pendiente de la pieza 4)"
        texto = texto.replace("{CARPETA}", self.c).replace("{EMPRESA}", self.E)
        raiz = os.path.abspath(os.path.join(AQUI, ".."))
        rutas = [f"carpeta de la empresa: {self.c}", f"raíz del personaje v2 (personaje_munger_v2.md, ANEXO_*.md, ENCARGO_personaje_v2.md, scripts/, esquema/): {raiz}",
                 f"corpus Munger (munger.md): {self.cfg.get('kit_v1', {}).get('corpus_munger', '')}", f"corpus Damodaran (damodaran.md, si existe): {self.cfg.get('corpus', {}).get('damodaran', '')}",
                 f"modelo y esfuerzo previstos (config_v2.json → modelos): {json.dumps(self.cfg.get('modelos', {}).get(nombre.replace('_turno1', '').replace('_turno2', ''), {}), ensure_ascii=False)}"]
        cab = f"# Paso {paso} · {nombre}\n\nEntradas (en {self.c}): " + ", ".join(entradas) + f"\n\nSalida esperada: {salida}\n\nRutas:\n" + "".join(f"- {r}\n" for r in rutas) + "\n"
        if motivo:
            cab += f"**CORRECCIÓN pedida por el pipeline:** {motivo}\n\n"
        open(self.p("prompts_generados", f"{paso:02d}_{nombre}.md"), "w", encoding="utf-8").write(cab + "---\n\n" + texto)
        open(self.p("ESPERANDO.md"), "w", encoding="utf-8").write(f"ESPERANDO al agente **{nombre}** (paso {paso}). " + (f"CORRECCIÓN: {motivo} " if motivo else "") + f"Entradas: {', '.join(entradas)}. Escribe **{salida}** en esta carpeta y vuelve a lanzar pipeline.py.\n")

    # ---------- pasos mecánicos ----------
    def escribir(self, fase_json, fase, libro_in, libro_out):
        cj = self.p(f"celdas_{fase}.json")
        rc, out = self.run([PY, self.script("fase_a_celdas.py"), self.p(fase_json), fase, cj])
        if rc != 0:
            return 11, out  # 11 = claves u Observaciones de la fase ausentes (defecto del agente, no del libro)
        return self.run([PY, self.script("escribir_v63.py"), libro_in, libro_out, "--celdas", cj, "--verificar", self.cfg["plantilla"]["referencia"]])

    def bloqueo_de_lectura(self):
        """Tras la fase B, precio.json con `sin_lectura` significa que la hoja bloquea el valor o la lectura del precio
        (Motor!B252/B253/B254). Un bloqueo nunca se convierte en aviso: según su causa (reglas del Motor) termina en
        pendiente_de_datos (DATOS INVÁLIDOS), modelo_no_aplicable solo si la fase A lo declaró, o no_entregable."""
        pr = json.load(open(self.p("precio.json"), encoding="utf-8")) if os.path.exists(self.p("precio.json")) else {}
        if "sin_lectura" not in pr:
            return False
        res = json.load(open(self.p("resultados.json"), encoding="utf-8")) if os.path.exists(self.p("resultados.json")) else {}
        reglas = [r for r in (res.get("reglas_motor") or []) if r.get("aplica") and r.get("resultado") in ("DATOS INVÁLIDOS", "MODELO NO APLICABLE", "INCOMPLETO") and r.get("nivel") in (1, 2)]
        detalle = f"la hoja bloquea la lectura del precio tras la fase B: {pr['sin_lectura']} · reglas: " + "; ".join(f"{r.get('id')} {r.get('resultado')} ({r.get('causa', '')})" for r in reglas)[:400]
        if any(r.get("resultado") == "DATOS INVÁLIDOS" for r in reglas):
            self.terminar("pendiente_de_datos", "falta_de_datos", detalle, self.st["paso"], que_hace_falta="corregir el dato inválido en fase1_v63.json o en la etapa 1", desde=2)
        else:
            self.terminar("no_entregable", "fallo_de_implementacion", detalle, self.st["paso"], desde=8)
        return True

    def recalc_leer_precio(self, libro):
        rc, out = self.run(["bash", self.script("recalc.sh"), libro, self.p("recalc"), self.perfil])
        if rc != 0:
            return False, "recálculo: " + out[-300:]
        rec = self.p("recalc", os.path.basename(libro))
        rc, out = self.run([PY, self.script("leer_resultados.py"), rec, self.p("resultados.json"), "--exigir-recalculo-forzado"])
        if rc != 0:
            return False, "lectura/recálculo no forzado: " + out[-300:]
        if os.path.exists(self.p("precio.json")):
            os.remove(self.p("precio.json"))  # nunca se lee una escalera de una pasada anterior
        rc, out = self.run([PY, self.script("precio_de_si.py"), self.p("resultados.json"), self.p("precio.json"), "--k", str(self.cfg.get("convenciones", {}).get("k_asimetria", 3))])
        if rc not in (0, 5) or not os.path.exists(self.p("precio.json")):
            return False, f"precio_de_si.py terminó con código {rc}: " + out[-300:]
        return True, rec

    # ---------- flujo ----------
    def correr(self, hasta=14):
        st = self.st
        libro_base, libro_datos, libro_ev = self.p(f"{self.E}_v63_base.xlsx"), self.p(f"{self.E}_v63_datos.xlsx"), self.p(f"{self.E}_v63_evaluada.xlsx")
        while st["paso"] <= hasta and st["estado_analisis"] is None:
            paso = st["paso"]
            if paso == 0:
                rc, out = self.run(["bash", self.script("comprobar_entorno.sh")])
                if rc != 0:
                    return self.terminar("no_entregable", "fallo_de_implementacion", "entorno incompleto: " + out[-300:], 0)
            elif paso == 1:
                ev = [f for f in os.listdir(self.p("etapa1")) if f.endswith(".xlsx")] if os.path.isdir(self.p("etapa1")) else []
                if not ev:
                    return self.terminar("pendiente_de_datos", "falta_de_datos", "falta etapa1/<E>_evaluada.xlsx (V5.3 decidida por el v1, D2)", 1, que_hace_falta="José Luis: la V5.3 evaluada de la etapa 1 (S-1)", desde=1)
                rc, out = self.run([PY, self.script("migrar_v53_a_v63.py"), self.p("etapa1", ev[0]), self.cfg["plantilla"]["archivo"], libro_base])
                if rc != 0:
                    return self.terminar("no_entregable", "fallo_de_implementacion", "migración: " + out[-300:], 1)
            elif paso == 2:
                if not os.path.exists(self.p("fase1_v63.json")):
                    # pieza 7: si hay informes en texto/, la Historia y los metadatos se construyen con agentes (fase1_historia.py)
                    if not glob.glob(self.p("texto", "*.txt")):
                        return self.terminar("pendiente_de_datos", "falta_de_datos", "falta fase1_v63.json y no hay informes en texto/ para construirlo", 2, que_hace_falta="José Luis: informes anuales de 10 años (PDF → texto/) o fase1_v63.json (S-2)", desde=2)
                    rc, out = self.run([PY, self.script("fase1_historia.py"), "preparar", self.c, self.E])
                    if rc == 10:
                        self.st["esperando"] = "2:fase1"
                        self.guardar()
                        open(self.p("ESPERANDO.md"), "w", encoding="utf-8").write(open(self.p("ESPERANDO_FASE1.md"), encoding="utf-8").read())
                        raise Esperando("fase 1 · Historia por año y metadatos (ver ESPERANDO.md)")
                    if rc != 0:
                        return self.terminar("pendiente_de_datos", "falta_de_datos", "fase1_historia preparar: " + out[-300:], 2, que_hace_falta="informes anuales con estados financieros en texto/", desde=2)
                    rc, out = self.run([PY, self.script("fase1_historia.py"), "construir", self.c])
                    if rc != 0:
                        return self.terminar("pendiente_de_datos", "falta_de_datos", "fase1_historia construir: " + out[-400:], 2, que_hace_falta="ver historia_revision.md (datos esenciales ausentes o salidas inválidas)", desde=2)
                    self.st["esperando"] = None
                rc, out = self.run([PY, self.script("rellenar_fase1_v63.py"), libro_base, self.p("fase1_v63.json"), libro_datos])
                if rc != 0:
                    return self.terminar("no_entregable" if rc == 1 else "pendiente_de_datos", "fallo_de_implementacion" if rc == 1 else "falta_de_datos", "rellenar_fase1: " + out[-300:], 2)
            elif paso == 3:
                rc, out = self.run([PY, self.script("comprobar_entrada_v63.py"), libro_datos, self.c])
                if rc == 1 and not os.path.exists(self.p("entrada_v63.json")):
                    return self.terminar("no_entregable", "fallo_de_implementacion", "comprobar_entrada_v63.py terminó con 1 sin escribir entrada_v63.json: " + out[-300:], 3)
                if rc == 1:
                    ent = json.load(open(self.p("entrada_v63.json"), encoding="utf-8"))
                    return self.terminar("pendiente_de_datos", "falta_de_datos", "bloqueante en la entrada: " + "; ".join(f"{x['dato']}: {x.get('que', '')}" for x in ent["bloqueantes"])[:600], 3,
                                         que_hace_falta="; ".join(f"{x['dato']} ← {x.get('origen_esperado', '')}" for x in ent["bloqueantes"])[:600], desde=2)
                if rc not in (0,):
                    return self.terminar("no_entregable", "fallo_de_implementacion", "comprobar_entrada: " + out[-300:], 3)
            elif paso == 4:
                rc, out = self.run([PY, self.script("volcar_datos_v63.py"), self.p("recalc", os.path.basename(libro_datos)), self.c])
                if rc != 0:
                    return self.terminar("no_entregable", "fallo_de_implementacion", "volcar_datos: " + out[-300:], 4)
            elif paso == 5:
                self.agente(5, "extraccion_v63", "extracto_v63.md", ["texto/", "extracto.md (etapa1)", "datos_v63.md"])
            elif paso == 6:
                self.agente(6, "fase_a", "fase_a.json", ["datos_v63.md", "extracto.md", "extracto_v63.md", "personaje_munger_v2.md"], alternativas=["fase_a.intento2.json"] if st["intentos"]["vueltas_b_a_a"] else [])
                v = self.validar_esquema("fase_a.json", "fase_a", 6, "fase_a")
                if v == "continuar":
                    continue
                if v == "fin":
                    return
                fa = json.load(open(self.p("fase_a.json"), encoding="utf-8"))
                motor = {"Sí": "A", "No · financiación cambia mucho": "B", "No · banco o aseguradora": "C"}.get((fa.get("celdas") or {}).get("C62"))
                st["motor"] = motor
                c62 = (fa.get("celdas") or {}).get("C62")
                if motor is None and c62 != "No · este tipo de empresa requiere otro método":
                    return self.terminar("no_entregable", "fallo_de_implementacion", f"Análisis!C62 = {c62!r} fuera del vocabulario (el esquema debía rechazarlo)", 6)
                if (fa.get("limite_del_modelo") or {}).get("aplica") or motor is None:
                    rc, out = self.escribir("fase_a.json", "A", libro_datos, libro_ev)
                    if rc != 0:
                        return self.terminar("no_entregable", "fallo_de_implementacion", "escritura de la fase A: " + out[-300:], 6)
                    rc, out = self.run([PY, self.script("comprobar_celdas_v2.py"), libro_ev, libro_datos, "--fases", "A"])
                    if rc != 0:
                        return self.terminar("no_entregable", "fallo_de_implementacion", "celdas de la fase A (límite del modelo): " + out[-400:], 6)
                    return self.terminar("modelo_no_aplicable", "limite_del_modelo", (fa.get("limite_del_modelo") or {}).get("porque") or "C62 = otro método", 6, comprobacion=(fa.get("limite_del_modelo") or {}).get("cual"), categoria="límite del modelo")
            elif paso == 7:
                rc, out = self.escribir("fase_a.json", "A", libro_datos, libro_ev)
                if rc == 11:  # claves u Observaciones de la fase A que faltan: es el agente quien corrige (D17), no un fallo mecánico
                    v = self.correccion_formato("fase_a.json", 6, "fase_a", "celdas u Observaciones de la fase A ausentes o mal nombradas: " + out[-400:])
                    if v == "continuar":
                        continue
                    return
                if rc != 0:
                    return self.terminar("no_entregable", "fallo_de_implementacion", "escritura de la fase A: " + out[-300:], 7)
                rc, out = self.run([PY, self.script("comprobar_celdas_v2.py"), libro_ev, libro_datos, "--fases", "A"])
                if rc != 0:
                    v = self.correccion_formato("fase_a.json", 6, "fase_a", "celdas de la fase A fuera de regla (comprobar_celdas_v2): " + out[-400:])
                    if v == "continuar":
                        continue
                    return
                rc, out = self.run([PY, self.script("comprobar_entrada_v63.py"), libro_ev, self.c, "--motor", st["motor"]])
                if rc == 1 and "Traceback" in out:
                    return self.terminar("no_entregable", "fallo_de_implementacion", "comprobar_entrada_v63.py falló: " + out[-300:], 7)
                if rc == 1:
                    return self.terminar("pendiente_de_datos", "falta_de_datos", f"el motor {st['motor']} elegido por la fase A no es calculable: " + out[-300:], 7, que_hace_falta="datos de Historia que exige el motor (Contrato_de_relleno_V6.3.csv)", desde=2)
                rc, out = self.run([PY, self.script("volcar_datos_v63.py"), self.p("recalc", os.path.basename(libro_ev)), self.c, "--referencias-mecanicas"])
                if rc != 0:
                    return self.terminar("no_entregable", "fallo_de_implementacion", "referencias mecánicas: " + out[-300:], 7)
            elif paso == 8:
                n = st["intentos"]["fase_b"]
                if st["intentos"]["vueltas_b_a_a"] and not st.get("esperando") and not self.sim and st.get("consumidos", {}).get("fase_b.json"):
                    self.pedir_correccion(8, "fase_b", "fase_b.json", f"la fase A corrigió el motor o el caso especial tras un límite del modelo (vuelta B→A única): el motor es ahora {st.get('motor')}; traduce de nuevo las palancas con las referencias mecánicas nuevas")
                self.agente(8, "fase_b", "fase_b.json", ["fase_a.json", "datos_v63.md", "referencias_mecanicas.json", "extracto_v63.md", "gramatica.md (si hay corrección)"],
                            alternativas=[f"fase_b.intento{n + 1}.json"] if n else [])
                v = self.validar_esquema("fase_b.json", "fase_b", 8, "fase_b")
                if v == "continuar":
                    continue
                if v == "fin":
                    return
                rc, out = self.run([PY, self.script("comprobar_gramatica.py"), self.c, "--antes-de-recalculo"])
                if rc not in (0, 1, 2, 3):
                    return self.terminar("no_entregable", "fallo_de_implementacion", f"comprobar_gramatica.py terminó con código {rc}: " + out[-300:], 8)
                fb = json.load(open(self.p("fase_b.json"), encoding="utf-8"))
                if (fb.get("limite_del_modelo") or {}).get("aplica") and rc != 3:
                    # la fase B señala un límite del modelo al traducir (Anexo D §D.4): misma vuelta a la fase A que el código 3
                    rc, out = 3, "límite del modelo declarado por la fase B: " + str((fb.get("limite_del_modelo") or {}).get("porque"))[:300]
                if rc == 3:
                    if st["intentos"]["vueltas_b_a_a"] >= self.lim.get("max_vueltas_fase_b_a_a_por_limite_del_modelo", 1):
                        # nadie declaró el límite (la fase A tuvo su vuelta y no corrigió el motor ni lo declaró): no es un estado legítimo, es un fallo
                        return self.terminar("no_entregable", "fallo_de_implementacion", "límite del modelo (código 3) que la fase A no resolvió ni declaró en su vuelta: " + out[-200:], 8, categoria="límite del modelo", desde=6)
                    st["intentos"]["vueltas_b_a_a"] += 1
                    st["paso"] = 6
                    self.pedir_correccion(6, "fase_a", "fase_a.json", "gramática código 3 (límite del modelo): la fase A tiene que corregir el motor o declarar el límite (una vuelta)")
                    self.log("gramática código 3: vuelve a la fase A con la pregunta concreta (una vez)")
                    continue
                if rc in (1, 2):
                    st["intentos"]["fase_b"] += 1
                    if st["intentos"]["fase_b"] > self.lim.get("max_correcciones_fase_b", 2):
                        g = json.load(open(self.p("gramatica.json"), encoding="utf-8")) if os.path.exists(self.p("gramatica.json")) else {"hallazgos": []}
                        h = next((x for x in g["hallazgos"] if x["categoria"] == "error"), next((x for x in g["hallazgos"] if x["categoria"] == "desviación" and not x["justificada"]), {}))
                        return self.terminar("no_entregable", "fallo_de_implementacion", f"gramática código {rc} tras {self.lim.get('max_correcciones_fase_b', 2)} correcciones de la fase B: {h.get('id')} {h.get('detalle', '')[:200]}", 8,
                                             comprobacion=h.get("id"), categoria=h.get("categoria"), que_hace_falta="revisar el prompt de la fase B en la regla indicada (nunca se aprueba por agotamiento)", desde=8)
                    self.pedir_correccion(8, "fase_b", "fase_b.json", f"gramática código {rc}: ver gramatica.md (corrección {st['intentos']['fase_b']})")
                    self.log(f"gramática código {rc}: corrección {st['intentos']['fase_b']} de la fase B (gramatica.md)")
                    continue
            elif paso == 9:
                rc, out = self.escribir("fase_b.json", "B", libro_ev, libro_ev + ".tmp.xlsx")
                if rc == 11:
                    v = self.correccion_formato("fase_b.json", 8, "fase_b", "celdas u Observaciones de la fase B ausentes o mal nombradas: " + out[-400:])
                    if v == "continuar":
                        continue
                    return
                if rc != 0:
                    return self.terminar("no_entregable", "fallo_de_implementacion", "escritura de la fase B: " + out[-300:], 9)
                os.replace(libro_ev + ".tmp.xlsx", libro_ev)
                st["fase_b_escrita"] = True
                rc, out = self.run([PY, self.script("comprobar_celdas_v2.py"), libro_ev, libro_datos, "--fases", "A,B"])
                if rc != 0:
                    v = self.correccion_formato("fase_b.json", 8, "fase_b", "celdas de la fase B fuera de regla (comprobar_celdas_v2): " + out[-400:])
                    if v == "continuar":
                        continue
                    return
                ok, rec = self.recalc_leer_precio(libro_ev)
                if not ok:
                    return self.terminar("no_entregable", "fallo_de_implementacion", rec, 9)
                rc, out = self.run([PY, self.script("comprobar_gramatica.py"), self.c, "--tras-recalculo"])
                if rc not in (0, 1, 2, 3):
                    return self.terminar("no_entregable", "fallo_de_implementacion", f"comprobar_gramatica.py terminó con código {rc}: " + out[-300:], 9)
                if rc == 3:
                    return self.terminar("no_entregable", "fallo_de_implementacion", "límite del modelo detectado tras el recálculo (debió detectarse antes del recálculo): " + out[-200:], 9, categoria="límite del modelo", desde=6)
                if rc < 2 and self.bloqueo_de_lectura():
                    return
                if rc >= 2:
                    g = json.load(open(self.p("gramatica.json"), encoding="utf-8")) if os.path.exists(self.p("gramatica.json")) else {"hallazgos": []}
                    solo_g19 = all(x["id"] == "G19" for x in g["hallazgos"] if x["categoria"] == "error")
                    if solo_g19:
                        # G19 (valores por acción desordenados): vuelta a la fase B UNA vez; si persiste, no_entregable (§B.3)
                        st["intentos"]["vueltas_g19"] = st["intentos"].get("vueltas_g19", 0) + 1
                        if st["intentos"]["vueltas_g19"] > 1:
                            return self.terminar("no_entregable", "fallo_de_implementacion", "G19 persiste tras su única vuelta a la fase B: " + out[-200:], 9, comprobacion="G19", categoria="error", desde=8)
                    else:
                        st["intentos"]["fase_b"] += 1
                        if st["intentos"]["fase_b"] > self.lim.get("max_correcciones_fase_b", 2):
                            return self.terminar("no_entregable", "fallo_de_implementacion", "error de gramática tras el recálculo que persiste: " + out[-200:], 9, categoria="error", desde=8)
                    st["paso"] = 8
                    self.pedir_correccion(8, "fase_b", "fase_b.json", f"gramática tras el recálculo código {rc}: ver gramatica.md (" + ("vuelta única por G19" if solo_g19 else f"corrección {st['intentos']['fase_b']}") + ")")
                    self.log(f"gramática tras recálculo código {rc}: vuelve a la fase B")
                    continue
            elif paso == 10:
                n = st["intentos"]["fase_c"]
                if st.get("turno_c") != 2:
                    if st["intentos"]["vueltas_c_a_b"] and not st.get("esperando") and not self.sim:
                        # la única vuelta C→B ya se consumió: el turno 1 nuevo tiene que saberlo (un segundo revisar_palancas termina en no_entregable)
                        self.pedir_correccion(10, "fase_c_turno1", "fase_c.json", "la fase B ya revisó las palancas en la única vuelta C→B admitida (§4.5): el libro está recalculado con las palancas nuevas; otro revisar_palancas termina en no_entregable")
                    self.agente(10, "fase_c_turno1", "fase_c.json", ["fase_a.json", "fase_b.json", "resultados.json", "precio.json", "gramatica.md", "datos_ausentes.json", "datos_v63.md", "extractos"],
                                alternativas=[f"fase_c.turno1.intento{n + 1}.json"] if n else ["fase_c.turno1.json"])
                    v = self.validar_esquema("fase_c.json", "fase_c", 10, "fase_c_turno1", turno=1)
                    if v == "continuar":
                        continue
                    if v == "fin":
                        return
                    fc = json.load(open(self.p("fase_c.json"), encoding="utf-8"))
                    if fc.get("revisar_palancas"):
                        if st["intentos"]["vueltas_c_a_b"] >= self.lim.get("max_vueltas_fase_c_a_b", 1):
                            return self.terminar("no_entregable", "fallo_de_implementacion", "la fase C pide revisar palancas por segunda vez (máximo una vuelta)", 10, desde=8)
                        st["intentos"]["vueltas_c_a_b"] += 1
                        st["paso"] = 8
                        self.pedir_correccion(8, "fase_b", "fase_b.json", "la fase C pide revisar palancas: " + str(fc.get("instrucciones_revision"))[:400])
                        self.log("fase C pide revisar_palancas: vuelve a la fase B una sola vez")
                        continue
                    if (fc.get("limite_del_modelo") or {}).get("aplica"):
                        fin = self.limite_declarado_por_c(fc, libro_ev)
                        if fin == "continuar":
                            continue
                        return
                    fm = fc.get("fundamento_material") or {}
                    rda = fc.get("revision_datos_ausentes") or {}
                    da = json.load(open(self.p("datos_ausentes.json"), encoding="utf-8")) if os.path.exists(self.p("datos_ausentes.json")) else []
                    revisados = {x.get("dato") for x in (rda.get("revisados") or [])}
                    sin_revisar = [x["dato"] for x in da if x["dato"] not in revisados]
                    if sin_revisar:
                        if self.correccion_c("revisión de datos ausentes incompleta (S-19): faltan " + ", ".join(sin_revisar)[:300], 10) == "continuar":
                            continue
                        return
                    if (fm.get("comprobacion_conjunta") or {}).get("procede") and not rda.get("alguno_material"):
                        if os.path.exists(self.p("comprobacion_conjunta.json")):
                            os.remove(self.p("comprobacion_conjunta.json"))  # nunca se lee la de una pasada anterior
                        rc, out = self.run([PY, self.script("comprobacion_conjunta.py"), self.c, libro_ev])
                        if rc == 3:
                            # combinación mal formada por el agente (celda ajena, de la fase C, valor no numérico): corrección a la fase C (D17), no fallo mecánico
                            if self.correccion_c("combinación de la comprobación conjunta mal formada: " + out[-300:], 10) == "continuar":
                                continue
                            return
                        if rc != 0:
                            return self.terminar("no_entregable", "fallo_de_implementacion", "comprobación conjunta: " + out[-300:], 10)
                if st.get("turno_c") != 2:
                    st["turno_c"] = 2
                    pendiente = st.get("motivo_correccion_c")
                    self.pedir_correccion(10, "fase_c_turno2", "fase_c.json", "segundo turno de la fase C: lee comprobacion_conjunta.json (si existe) y cierra fase_c.json (turno 2)" + (f" · CORRECCIÓN PENDIENTE que motivó esta pasada: {pendiente}" if pendiente else ""))
                self.agente(10, "fase_c_turno2", "fase_c.json", ["fase_c.json (turno 1)", "comprobacion_conjunta.json (si existe)"],
                            alternativas=[f"fase_c.turno2.intento{n + 1}.json"] if n else ["fase_c.turno2.json"])
                v = self.validar_esquema("fase_c.json", "fase_c", 10, "fase_c_turno2", turno=2)
                if v == "continuar":
                    continue
                if v == "fin":
                    return
                st["turno_c"] = None
                st["estado_pendiente"] = None
                st["estado_analisis_fase_c"] = None
                st["motivo_correccion_c"] = None
                fc = json.load(open(self.p("fase_c.json"), encoding="utf-8"))
                if (fc.get("limite_del_modelo") or {}).get("aplica"):
                    # límite declarado en el segundo turno: mismo tratamiento que en el primero (no se escriben las 16 celdas ni hay escalera)
                    fin = self.limite_declarado_por_c(fc, libro_ev)
                    if fin == "continuar":
                        continue
                    return
                err = self.coherencia_fase_c(fc)
                if err:
                    if self.correccion_c("fase C incoherente: " + err, 10) == "continuar":
                        continue
                    return
                rc, out = self.escribir("fase_c.json", "C", libro_ev, libro_ev + ".tmp.xlsx")
                if rc == 11:
                    if self.correccion_c("celdas u Observaciones de la fase C ausentes o mal nombradas: " + out[-400:], 10) == "continuar":
                        continue
                    return
                if rc != 0:
                    return self.terminar("no_entregable", "fallo_de_implementacion", "escritura de la fase C: " + out[-300:], 10)
                os.replace(libro_ev + ".tmp.xlsx", libro_ev)
                st["fase_c_escrita"] = True
                rc, out = self.run([PY, self.script("comprobar_celdas_v2.py"), libro_ev, libro_datos, "--fases", "A,B,C"])
                if rc != 0:
                    if self.correccion_c("celdas de la fase C: " + out[-400:], 10) == "continuar":
                        continue
                    return
                ok, rec = self.recalc_leer_precio(libro_ev)
                if not ok:
                    return self.terminar("no_entregable", "fallo_de_implementacion", rec, 10)
                if self.bloqueo_de_lectura():
                    return
                rc, out = self.run([PY, self.script("comprobar_gramatica.py"), self.c, "--tras-recalculo", "--con-fase-c"])
                if rc not in (0, 1, 2, 3):
                    return self.terminar("no_entregable", "fallo_de_implementacion", f"comprobar_gramatica.py terminó con código {rc}: " + out[-300:], 10)
                if rc >= 1:
                    if self.correccion_c(f"gramática código {rc} tras la fase C (toda desviación tiene que estar justificada; ningún error): " + out[-200:], 10) == "continuar":
                        continue
                    return
                st["estado_analisis_fase_c"] = fc.get("estado_analisis")
            elif paso == 11:
                est = st.get("estado_analisis_fase_c") or "concluido"
                if est == "concluido":
                    for f in ("diagnostico.md", "diagnostico.json"):
                        if os.path.exists(self.p(f)):
                            os.replace(self.p(f), self.p(f + ".anterior"))
                    st["estado_pendiente"] = None
                if est != "concluido":
                    tipo = {"pendiente_de_investigacion": "incertidumbre_no_acotada", "pendiente_de_datos": "falta_de_datos", "modelo_no_aplicable": "limite_del_modelo"}[est]
                    fc = json.load(open(self.p("fase_c.json"), encoding="utf-8"))
                    fm = fc.get("fundamento_material") or {}
                    det = fm.get("hipotesis_que_mas_condiciona") or ""
                    que_falta, desde = (fm.get("que_lo_resolveria") or det or ""), "8"
                    if est == "pendiente_de_datos":
                        materiales = [x for x in (fc.get("revision_datos_ausentes") or {}).get("revisados", []) if x.get("material_para_conclusion_favorable")]
                        det = "; ".join(f"{x.get('dato')}: {x.get('porque', '')}" for x in materiales)
                        que_falta = "; ".join(f"{x.get('dato')} ← {x.get('que_falta') or 'dato ausente'} (afecta a: {x.get('conclusion_afectada', '')})" for x in materiales)
                        desde = "2"  # los datos entran por fase1_v63.json / etapa 1: se reanuda desde el relleno de la fase 1
                    st["estado_analisis"] = est
                    self.guardar()
                    self.run([PY, self.script("diagnostico.py"), self.c, "--estado", est, "--tipo", tipo, "--detalle", (det or est)[:500], "--paso", "10",
                              "--que-hace-falta", que_falta[:500], "--desde-paso", desde, "--quien", "José Luis (datos o documentos) / Claude Code"])
                    st["estado_analisis"] = None  # sigue hasta el paso 14 con las salidas
                    st["estado_pendiente"] = est
                self.run([PY, self.script("ficha.py"), self.c, "--estado", st.get("estado_pendiente") or "concluido"])
                self.run([PY, self.script("informe.py"), self.c])
            elif paso == 12:
                # se verifica siempre sobre un recálculo del libro tal como está ahora (al reanudar con --desde, resultados.json
                # y recalc/ podían ser de una pasada anterior: visto con Vidrala, 3-nov-2026)
                ok, rec = self.recalc_leer_precio(libro_ev)
                if not ok:
                    return self.terminar("no_entregable", "fallo_de_implementacion", rec, 12)
                rc, out = self.run(["bash", self.script("verificar_todo.sh"), self.c, libro_ev, libro_datos])
                if rc != 0:
                    fallos = [l.strip() for l in out.splitlines() if l.strip().startswith("FAIL")]
                    return self.terminar("no_entregable", "fallo_de_implementacion", "verificar_todo.sh con FAIL: " + ("; ".join(fallos) or out[-400:])[:500], 12, que_hace_falta="ver verificacion_*.txt en la carpeta")
            elif paso == 13:
                n = st["intentos"]["auditoria"]
                self.agente(13, "verificacion", "auditoria.md", ["todo lo de la carpeta salvo los prompts de las fases"], alternativas=[f"auditoria.intento{n + 1}.md"] if n else [])
                txt = open(self.p("auditoria.md"), encoding="utf-8").read()
                st["auditoria"] = self.veredicto_auditoria(txt)
                if st["auditoria"] == "REPETIR":
                    st["intentos"]["auditoria"] += 1
                    if st["intentos"]["auditoria"] > self.lim.get("max_correcciones_auditoria", 2):
                        return self.terminar("no_entregable", "fallo_de_implementacion", "auditoría en REPETIR tras agotar las correcciones (nunca se aprueba por agotamiento)", 13, desde=10)
                    st["paso"] = 10
                    st["turno_c"] = 1
                    st["intentos"]["fase_c"] = max(st["intentos"]["fase_c"], 1)
                    self.pedir_correccion(10, "fase_c_turno1", "fase_c.json", "auditoría REPETIR: ver auditoria.md")
                    self.log(f"auditoría REPETIR: corrección {st['intentos']['auditoria']} desde el paso 10 (fase C)")
                    continue
            elif paso == 14:
                est = st.get("estado_pendiente") or "concluido"
                st["estado_analisis"] = est
                st["fin"] = dt.datetime.now().isoformat(timespec="seconds")
                self.guardar()
                self.salidas_finales()
                self.log(f"FIN · estado {est} · auditoría {st.get('auditoria')}")
                return
            st["paso"] += 1
            self.guardar()

    def limite_declarado_por_c(self, fc, libro_ev):
        """Límite del modelo declarado por la fase C (en cualquiera de los dos turnos): si corrige C62, se escribe (con E/F/N de su
        fila; la clase y la confianza son convención del pipeline para esta única corrección mecánica, el apoyo es el motivo del
        personaje) y se verifica; el análisis termina en modelo_no_aplicable sin escribir las 16 celdas ni escalera (§4.7, §7.3)."""
        corr = {k: v for k, v in (fc.get("celdas_corregidas") or {}).items() if k in ("C62", "Análisis!C62") and v.get("despues") != v.get("antes")}
        if corr:
            v = list(corr.values())[0]
            if v.get("despues") not in C.CELDAS["Análisis"]["C62"]["lista"]:
                return self.correccion_c(f"la fase C corrige C62 a {v.get('despues')!r}, fuera del vocabulario de Análisis!C62", 10)
            fila = C.CELDAS["Análisis"]["C62"]["cm"]
            obs = f"[Clase: convención] [Confianza: media]\nHereda: {v.get('antes')} → cambia (razonamiento_corregido): corregida en la fase C al declarar el límite del modelo (clase y confianza: convención del pipeline para esta corrección). Apoyo (motivo del personaje): {str(v.get('motivo'))[:550]}. Lo sustituiría: un motor que capture esta empresa."
            cj = self.p("celdas_C_limite.json")
            json.dump({"Análisis!C62": v.get("despues"), f"Control maestro!E{fila}": C.E_LISTO, f"Control maestro!F{fila}": C.F_ESTIMACION, f"Control maestro!N{fila}": obs[:900]}, open(cj, "w", encoding="utf-8"), ensure_ascii=False)
            rc, out = self.run([PY, self.script("escribir_v63.py"), libro_ev, libro_ev + ".tmp.xlsx", "--celdas", cj, "--verificar", self.cfg["plantilla"]["referencia"]])
            if rc != 0:
                if os.path.exists(libro_ev + ".tmp.xlsx"):
                    os.remove(libro_ev + ".tmp.xlsx")
                self.terminar("no_entregable", "fallo_de_implementacion", "escritura de C62 corregida por la fase C: " + out[-300:], 10)
                return "fin"
            os.replace(libro_ev + ".tmp.xlsx", libro_ev)
        self.terminar("modelo_no_aplicable", "limite_del_modelo", (fc.get("limite_del_modelo") or {}).get("porque") or "límite del modelo declarado por la fase C", 10, categoria="límite del modelo")
        return "fin"

    def correccion_c(self, motivo, paso):
        st = self.st
        st["intentos"]["fase_c"] += 1
        if st["intentos"]["fase_c"] > self.lim.get("max_correcciones_fase_c", self.lim.get("max_correcciones_fase_b", 2)):
            self.terminar("no_entregable", "fallo_de_implementacion", f"fase C tras agotar las correcciones: {motivo}", paso, desde=10, que_hace_falta="revisar el prompt de la fase C en la regla indicada")
            return "fin"
        st["turno_c"] = 1
        st["paso"] = 10
        st["motivo_correccion_c"] = motivo[:400]
        self.pedir_correccion(10, "fase_c_turno1", "fase_c.json", motivo[:400])
        self.log(f"corrección {st['intentos']['fase_c']} de la fase C: {motivo[:200]}")
        return "continuar"

    @staticmethod
    def veredicto_auditoria(txt):
        """APROBADO solo si hay exactamente una línea «Veredicto: APROBADO» (sin coletillas) y ningún punto 1, 4, 11, 12 o 16
        contiene FALLA (D.9). Los puntos se reconocen por el número al principio de la línea tras marcas de markdown (`**`, `-`, `#`,
        `|`, `(`), con `.`, `)`, `:`, `·`, `-` o `|` detrás; el FALLA puede estar en esa línea o en las siguientes hasta el punto
        siguiente. Cualquier otra cosa es REPETIR: la duda nunca aprueba (D17)."""
        import re
        limpio = txt.replace("\\.", ".")
        lineas = [l for l in limpio.splitlines() if re.match(r"^[\s>*#_-]*veredicto[\s*_]*:", l, re.I)]
        if len(lineas) != 1:
            return "REPETIR"
        resto = re.sub(r"^[\s>*#_-]*veredicto[\s*_]*:", "", lineas[0], flags=re.I).strip().strip("*_ ").strip()
        if not re.fullmatch(r"APROBADO[\s.]*", resto, flags=re.I):
            return "REPETIR"
        actual = None
        for l in limpio.splitlines():
            m = re.match(r"^[\s>*#_|-]*\(?(\d{1,2})\)?[\s]*(?:[.):·|–—-]|\*\*|\s)[\s*_|]*", l)
            if m and not re.match(r"^[\s>*#_|-]*\d{1,2}[,.]\d", l):  # un número decimal al principio no es un punto
                actual = int(m.group(1))
            if actual in (1, 4, 11, 12, 16) and re.search(r"\bFALLA\b", l):
                return "REPETIR"
            if re.match(r"^[\s>*#_-]*veredicto", l, re.I):
                actual = None
        return "APROBADO"

    def coherencia_fase_c(self, fc):
        """Coherencia del cierre de la fase C (encargo §8, Anexo D §D.6, S-19, D10, D16). No se fía solo de lo que escribe el
        agente: cruza con precio.json (zona), comprobacion_conjunta.json (sobrevive del script) y la lista de hipótesis."""
        est = fc.get("estado_analisis")
        dec = fc.get("decision") or {}
        acc = dec.get("accion")
        cubo = fc.get("cubo_final")
        fm = fc.get("fundamento_material") or {}
        cc = fm.get("comprobacion_conjunta") or {}
        hs = fm.get("hipotesis_sin_fundamento") or []
        rda = fc.get("revision_datos_ausentes") or {}
        revisados = rda.get("revisados") or []
        precio = json.load(open(self.p("precio.json"), encoding="utf-8")) if os.path.exists(self.p("precio.json")) else {}
        ccj = json.load(open(self.p("comprobacion_conjunta.json"), encoding="utf-8")) if os.path.exists(self.p("comprobacion_conjunta.json")) else None
        zona = precio.get("zona")
        if est not in ("concluido", "pendiente_de_investigacion", "modelo_no_aplicable", "pendiente_de_datos"):
            return f"estado_analisis {est!r} no válido"
        if cubo not in C.CUBOS:
            return f"cubo_final {cubo!r} no válido"
        if acc not in C.ACCIONES + (None,):
            return f"accion {acc!r} no válida"
        # S-19: la materialidad declarada por dato manda sobre el resumen
        material_real = any(x.get("material_para_conclusion_favorable") for x in revisados)
        if bool(rda.get("alguno_material")) != material_real:
            return f"alguno_material = {rda.get('alguno_material')} pero los datos revisados dicen {material_real} (S-19)"
        if material_real and est != "pendiente_de_datos" and not (est == "concluido" and acc in ("descartar", "demasiado_dificil")) and est != "modelo_no_aplicable":
            # un dato material para la conclusión favorable solo convive con descartar/demasiado_dificil (§8: el descalificador va antes) o con el límite del modelo
            return "revisión de datos ausentes material pero estado ≠ pendiente_de_datos (S-19); solo descartar/demasiado_dificil pueden convivir con un dato material"
        if est == "pendiente_de_datos" and not material_real:
            return "pendiente_de_datos sin ningún dato ausente declarado material (S-19)"
        if est == "pendiente_de_datos" and (acc is not None or cubo == "Sí"):
            return "pendiente_de_datos exige acción null y cubo ≠ Sí"
        if est == "pendiente_de_investigacion" and (acc is not None or cubo != "Vigilar"):
            return "pendiente_de_investigacion exige cubo Vigilar y acción null"
        if est == "modelo_no_aplicable":
            if not (fc.get("limite_del_modelo") or {}).get("aplica"):
                return "modelo_no_aplicable sin limite_del_modelo.aplica"
            if acc in ("comprar", "esperar") or cubo == "Sí":
                return "modelo_no_aplicable no admite comprar/esperar ni cubo Sí"
        # autocomprobación (P-1): diez entradas que cubran las diez tendencias de la sección 16 (se reconocen por palabras clave)
        claves = [("anclaje", "etapa 1"), ("precio|fuente externa",), ("consistencia|compromiso",), ("historia bonita|viento de cola",),
                  ("optimismo|tasa base",), ("doble castigo|mismo riesgo",), ("disponibilidad|v[ií]vido",), ("autoridad|gu[ií]a de la direcci",),
                  ("malo",), ("no numerable|no está en las palancas|no esta en las palancas",)]
        sesgos = [str(x.get("sesgo") or "").lower() for x in (fc.get("autocomprobacion") or [])]
        if len(sesgos) != 10:
            return f"autocomprobacion con {len(sesgos)} entradas (tienen que ser las diez tendencias de la sección 16)"
        for patrones in claves:
            if not any(all(re.search(pt, sg) for pt in patrones) for sg in sesgos):
                return f"autocomprobacion: falta la tendencia «{' + '.join(patrones)}» (sección 16)"
        # celdas_corregidas: solo C62 (límite del modelo) puede cambiar de valor; lo demás se documenta sin cambiar (una vuelta C→A no existe)
        for k, v in (fc.get("celdas_corregidas") or {}).items():
            if k not in ("C62", "Análisis!C62") and v.get("despues") != v.get("antes"):
                return f"celdas_corregidas[{k}] cambia el valor ({v.get('antes')!r} → {v.get('despues')!r}): la fase C no reescribe celdas de A/B; pide revisar_palancas o deja despues = antes y lo anota en incoherencias"
        # fundamento material (D10)
        sin_base = [h.get("celda") for h in hs if not ((h.get("alternativas_defendibles") or {}).get("hay_base"))]
        res_fm = fm.get("resultado")
        if est == "concluido":
            if acc is None:
                return "concluido sin acción"
            if (acc == "comprar") != (cubo == "Sí"):
                return "comprar ⇔ cubo Sí"
            if acc == "comprar":
                if "sin_lectura" in precio or "sin_escalera" in precio or zona not in ("cumple_regla_k", "bajo_malo"):
                    return f"comprar con zona {zona!r} de precio.json (solo cumple_regla_k o bajo_malo)"
                if not hs:
                    if res_fm != "sin_limitacion":
                        return f"comprar sin hipótesis sin fundamento exige resultado sin_limitacion (hay {res_fm!r})"
                else:
                    if res_fm != "comprobacion_conjunta_superada":
                        return f"comprar con {len(hs)} hipótesis sin fundamento exige comprobacion_conjunta_superada (hay {res_fm!r})"
                    if sin_base:
                        return f"comprar con hipótesis sin base para acotar: {sin_base}"
                    if not cc.get("procede") or not cc.get("combinacion"):
                        return "comprar con hipótesis sin fundamento pero sin comprobación conjunta (procede/combinacion)"
                    if ccj is None:
                        return "comprar con comprobación conjunta declarada pero sin comprobacion_conjunta.json (el script no la ejecutó)"
                    if cc.get("sobrevive") is not True or ccj.get("sobrevive") is not True:
                        return f"comprar con comprobación conjunta no superada (fase C: {cc.get('sobrevive')}; script: {ccj.get('sobrevive')})"
            if acc == "esperar":
                if cubo != "Vigilar":
                    return "esperar ⇔ cubo Vigilar"
                po = dec.get("precio_objetivo"); psi = precio.get("precio_si")
                if zona in ("cumple_regla_k", "bajo_malo"):
                    if not (dec.get("condicion") or "").strip():
                        return f"esperar con zona {zona}: exige una condición concreta que no sea de precio"
                elif not (isinstance(po, (int, float)) and isinstance(psi, (int, float)) and abs(po - psi) <= 0.005 * max(1, abs(psi))):
                    return f"esperar: precio_objetivo {po!r} ≠ precio de Sí de precio.json {psi!r}"
            if acc == "descartar" and cubo != "No":
                return "descartar ⇔ cubo No"
            if acc == "demasiado_dificil" and cubo != "Demasiado difícil":
                return "demasiado_dificil ⇔ cubo Demasiado difícil"
            if res_fm == "pendiente_de_investigacion":
                return "fundamento_material pendiente_de_investigacion con estado concluido"
        if est == "pendiente_de_investigacion" and res_fm != "pendiente_de_investigacion":
            return f"pendiente_de_investigacion exige fundamento_material.resultado = pendiente_de_investigacion (hay {res_fm!r})"
        if cc.get("sobrevive") is not None and ccj is not None and cc.get("sobrevive") != ccj.get("sobrevive"):
            return f"sobrevive de la fase C ({cc.get('sobrevive')}) ≠ sobrevive del script ({ccj.get('sobrevive')})"
        if cc.get("sobrevive") is not None and ccj is None:
            return "sobrevive informado sin comprobacion_conjunta.json"
        # C104 (D16) coherente con el estado y la acción
        c104 = str((fc.get("celdas") or {}).get("C104") or "")
        if not c104.startswith(C.C104_PREFIJO) or "%" in c104:
            return f"C104 no empieza por «{C.C104_PREFIJO}» o contiene un porcentaje (D16)"
        esperado = {"comprar": "comprar al precio actual", "esperar": "esperar", "descartar": "descartar", "demasiado_dificil": "demasiado difícil"}.get(acc)
        if est == "pendiente_de_datos":
            esperado = "sin conclusión (pendiente de datos"
        elif est == "pendiente_de_investigacion":
            esperado = "sin conclusión (pendiente de investigación)"
        if esperado and esperado.lower() not in c104.lower():
            return f"C104 no dice «{esperado}» (estado {est}, acción {acc})"
        sin_escalera = "sin escalera aplicable" in c104.lower()
        if sin_escalera and (acc in ("comprar", "esperar") or est in ("pendiente_de_datos", "pendiente_de_investigacion")):
            return "C104 dice «sin escalera aplicable» con una conclusión que necesita la escalera"
        if not sin_escalera:
            for clave, valor in (("precio de Sí", precio.get("precio_si")), ("precio esc. MALO", precio.get("precio_escenario_malo")), ("ponderado", precio.get("ponderado"))):
                if isinstance(valor, (int, float)):
                    formas = {f"{valor:.2f}", f"{valor:.1f}", f"{valor:.0f}"}
                    formas |= {f.replace(".", ",") for f in formas}
                    if not any(f in c104 for f in formas):
                        if acc in ("descartar", "demasiado_dificil") or est == "modelo_no_aplicable":
                            return f"C104 no lleva el {clave} de precio.json ({valor:.2f}) ni dice «sin escalera aplicable»"
                        return f"C104 no lleva el {clave} de precio.json ({valor:.2f})"
        return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("--config", default=os.path.join(AQUI, "..", "config_v2.json"))
    ap.add_argument("--agentes-simulados")
    ap.add_argument("--hasta", type=int, default=14)
    ap.add_argument("--reiniciar", action="store_true")
    ap.add_argument("--desde", type=int)
    a = ap.parse_args()
    cfg = config_v2.cargar(a.config)
    if a.reiniciar and os.path.exists(os.path.join(a.carpeta, "estado_pipeline.json")):
        os.remove(os.path.join(a.carpeta, "estado_pipeline.json"))
    p = Pipeline(a.carpeta, cfg, a.agentes_simulados)
    if a.desde is not None:
        p.st["paso"] = a.desde
        p.st["estado_analisis"] = None
        p.st["esperando"] = None
        p.guardar()  # verificar_todo.sh lee estado_pipeline.json del disco: no debe ver el estado final de la ejecución anterior
    try:
        p.correr(a.hasta)
    except Esperando as e:
        print(f"ESPERANDO: {e} (ver ESPERANDO.md y prompts_generados/)")
        return 10
    if os.path.exists(p.p("ESPERANDO.md")) and p.st.get("esperando") is None:
        os.remove(p.p("ESPERANDO.md"))
    print(f"estado final: {p.st.get('estado_analisis')} · paso {p.st['paso']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
