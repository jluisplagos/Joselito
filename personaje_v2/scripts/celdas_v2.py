#!/usr/bin/env python3
"""Inventario de las 68 celdas de juicio del personaje v2 (Anexo A) y de las filas de Control maestro.

Fuente: ANEXO_A_celdas_de_juicio_V6_3.md (versión 0.2.1). Si la plantilla real discrepa, manda la
plantilla y se anota en DECISIONES.md.
"""
# --- A.1 Análisis (34, heredadas) ---
ANALISIS = {
    "C11": {"fase": "A", "cm": 21, "lista": ["Sí", "No"], "heredada": True},
    "C12": {"fase": "A", "cm": 22, "lista": ["Sí", "No"], "heredada": True},
    "C13": {"fase": "A", "cm": 23, "lista": ["Sí", "No"], "heredada": True},
    "C14": {"fase": "A", "cm": 24, "lista": ["Compounder", "Calidad a precio razonable", "Deep value / especial",
                                             "Cíclica / commodity", "Turnaround / situación especial"], "heredada": True},
    "C17": {"fase": "A", "cm": 25, "lista": ["Sí", "No"], "heredada": True},
    "C18": {"fase": "A", "cm": 26, "lista": ["Sí", "No"], "heredada": True},
    "C19": {"fase": "A", "cm": 27, "lista": ["Sí", "No"], "heredada": True},
    "C20": {"fase": "A", "cm": 28, "lista": ["Incert. alta + riesgo bajo", "Ambos bajos", "Riesgo real alto"], "heredada": True},
    "C25": {"fase": "A", "cm": 30, "lista": ["Sí", "No"], "heredada": True},
    "C27": {"fase": "A", "cm": 32, "lista": ["Expandiendo", "Estable", "Comprimiendo"], "heredada": True},
    "C51": {"fase": "A", "cm": 49, "lista": ["Sí", "No"], "heredada": True},
    "C56": {"fase": "A", "cm": 53, "tipo": "decimal", "heredada": True},
    "C61": {"fase": "A", "cm": 56, "lista": ["Sí", "No", "No está claro"], "heredada": True},
    "C62": {"fase": "A", "cm": 57, "lista": ["Sí", "No · financiación cambia mucho", "No · banco o aseguradora",
                                             "No · este tipo de empresa requiere otro método"], "heredada": True},
    "B65": {"fase": "A", "cm": 58, "tipo": "texto", "heredada": True},
    "C65": {"fase": "A", "cm": 63, "tipo": "texto", "heredada": True},
    "D65": {"fase": "A", "cm": 68, "tipo": "texto", "heredada": True},
    "B66": {"fase": "A", "cm": 59, "tipo": "texto", "heredada": True},
    "C66": {"fase": "A", "cm": 64, "tipo": "texto", "heredada": True},
    "D66": {"fase": "A", "cm": 69, "tipo": "texto", "heredada": True},
    "B68": {"fase": "B", "cm": 61, "lista_num": [0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03], "heredada": True},
    "C68": {"fase": "B", "cm": 66, "lista_num": [0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03], "heredada": True},
    "D68": {"fase": "B", "cm": 71, "lista_num": [0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03], "heredada": True},
    "B69": {"fase": "B", "cm": 62, "lista_num": [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6], "heredada": True},
    "C69": {"fase": "B", "cm": 67, "lista_num": [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6], "heredada": True},
    "D69": {"fase": "B", "cm": 72, "lista_num": [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6], "heredada": True},
    "C76": {"fase": "B", "cm": 82, "tipo": "decimal", "condicional": "solo motor A", "heredada": True},
    "C93": {"fase": "C", "cm": 74, "lista": ["Sí", "No", "No lo sé"], "heredada": True},
    "C97": {"fase": "A", "cm": 76, "lista": ["Comprando", "Neutral", "Vendiendo"], "heredada": True},
    "C98": {"fase": "A", "cm": 77, "lista": ["Buena", "Aceptable", "Dudosa"], "heredada": True},
    "B101": {"fase": "C", "cm": 78, "tipo": "texto", "heredada": True},
    "B102": {"fase": "C", "cm": 79, "tipo": "texto", "heredada": True},
    "C103": {"fase": "C", "cm": 80, "lista": ["Sí", "No"], "heredada": True},
    "C104": {"fase": "C", "cm": 81, "tipo": "texto", "heredada": True},
}
# --- A.2 Palancas (32, nuevas) ---
PALANCAS = {
    "C5": {"fase": "A", "cm": 137, "lista": ["Joven (sin beneficios estables)", "En crecimiento", "Madura en crecimiento", "Madura", "En declive"]},
    "C6": {"fase": "A", "cm": 138, "lista": ["Ninguno", "Financiera (banco o aseguradora)", "Regulada (red, concesión)",
                                             "Cíclica o materias primas", "Intangibles (I+D, marca)", "Emergente (riesgo país)",
                                             "Multinegocio o conglomerado"]},
    "C8": {"fase": "A", "cm": 139, "lista": ["Último año", "Media del ciclo"]},
    "C9": {"fase": "A", "cm": 140, "lista": ["Sí", "No"]},
    "C10": {"fase": "A", "cm": 141, "tipo": "entero", "condicional": "vacío si C9 = No"},
    "B14": {"fase": "B", "cm": 142, "tipo": "decimal"}, "C14": {"fase": "B", "cm": 146, "tipo": "decimal"}, "D14": {"fase": "B", "cm": 150, "tipo": "decimal"},
    "B15": {"fase": "B", "cm": 143, "tipo": "decimal"}, "C15": {"fase": "B", "cm": 147, "tipo": "decimal"}, "D15": {"fase": "B", "cm": 151, "tipo": "decimal"},
    "B16": {"fase": "B", "cm": 144, "tipo": "decimal", "condicional": "vacío en motor C"},
    "C16": {"fase": "B", "cm": 148, "tipo": "decimal", "condicional": "vacío en motor C"},
    "D16": {"fase": "B", "cm": 152, "tipo": "decimal", "condicional": "vacío en motor C"},
    "B18": {"fase": "B", "cm": 145, "tipo": "decimal"}, "C18": {"fase": "B", "cm": 149, "tipo": "decimal"}, "D18": {"fase": "B", "cm": 153, "tipo": "decimal"},
    "C22": {"fase": "B", "cm": 154, "tipo": "decimal", "condicional": "vacío = 0"},
    "C23": {"fase": "B", "cm": 155, "tipo": "decimal", "condicional": "solo con C22 > 0"},
    "C24": {"fase": "B", "cm": 156, "tipo": "decimal", "condicional": "solo con cifra de fuente primaria"},
    "A38": {"fase": "C", "cm": 157, "tipo": "texto"}, "A39": {"fase": "C", "cm": 160, "tipo": "texto"}, "A40": {"fase": "C", "cm": 163, "tipo": "texto"},
    "B38": {"fase": "C", "cm": 158, "tipo": "fecha"}, "B39": {"fase": "C", "cm": 161, "tipo": "fecha"}, "B40": {"fase": "C", "cm": 164, "tipo": "fecha"},
    "C38": {"fase": "C", "cm": 159, "tipo": "decimal"}, "C39": {"fase": "C", "cm": 162, "tipo": "decimal"}, "C40": {"fase": "C", "cm": 165, "tipo": "decimal"},
    "C43": {"fase": "A", "cm": 166, "lista": ["No aplica", "Transitorio", "Extraordinario", "Estructural"]},
    "C44": {"fase": "B", "cm": 167, "tipo": "decimal", "condicional": "solo con Transitorio/Extraordinario"},
    "C47": {"fase": "A", "cm": 170, "lista": ["Ninguna", "ADR o ADS", "Split o contrasplit", "Básicas frente a diluidas",
                                              "Fechas distintas", "Otra (explicada en Control maestro)"]},
}
# --- A.3 Diagnóstico V6 (2, sin fila en Control maestro) ---
DIAGNOSTICO = {"B222": {"fase": "C", "cm": None, "tipo": "texto"}, "B223": {"fase": "C", "cm": None, "tipo": "texto"}}

CELDAS = {"Análisis": ANALISIS, "Palancas": PALANCAS, "Diagnóstico V6": DIAGNOSTICO}
FILAS_CM = sorted({d["cm"] for h in CELDAS.values() for d in h.values() if d.get("cm")})
assert len(FILAS_CM) == 66 and sum(len(h) for h in CELDAS.values()) == 68

E_LISTO = "Listo para auditoría"
F_ESTIMACION = "Estimación declarada"
CLASES = ("fundamentada", "convención", "técnico", "sin juicio propio")
CONFIANZAS = ("alta", "media", "baja")
MOTIVOS_HERENCIA = ("misma_evidencia", "evidencia_nueva", "razonamiento_corregido", "definicion_o_medicion_distinta")
ESTADOS = ("concluido", "pendiente_de_datos", "pendiente_de_investigacion", "modelo_no_aplicable", "no_entregable")
ACCIONES = ("comprar", "esperar", "descartar", "demasiado_dificil")
CUBOS = ("Sí", "Vigilar", "No", "Demasiado difícil")
ZONAS = ("caro", "vigilar", "cumple_regla_k", "bajo_malo")
C104_PREFIJO = "Pendiente de decisión de cartera"


def celdas_de_fase(fase):
    return {f"{h}!{ref}" for h, d in CELDAS.items() for ref, meta in d.items() if meta["fase"] == fase}


def lista_blanca_juicio():
    """{hoja: set(refs)} con las 68 celdas y las columnas E, F y N de las 66 filas de Control maestro."""
    lb = {h: set(d) for h, d in CELDAS.items()}
    lb["Control maestro"] = {f"{col}{r}" for r in FILAS_CM for col in "EFN"}
    return lb


def fila_cm(hoja, ref):
    return CELDAS[hoja][ref].get("cm")


def heredadas():
    return [f"Análisis!{r}" for r, m in ANALISIS.items() if m.get("heredada")]


if __name__ == "__main__":
    print("68 celdas:", {h: len(d) for h, d in CELDAS.items()})
    print("66 filas CM:", FILAS_CM)
    print("fase A:", len(celdas_de_fase("A")), "fase B:", len(celdas_de_fase("B")), "fase C:", len(celdas_de_fase("C")))
