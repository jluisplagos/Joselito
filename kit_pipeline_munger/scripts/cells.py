# -*- coding: utf-8 -*-
"""Definición compartida de la plantilla «Hoja de evaluación de empresas V5.3».

Las 37 celdas de juicio (tipo S en Control maestro), sus tipos y los vocabularios
de los desplegables tal y como están en la plantilla (leídos de las validaciones de datos).
"""

SHEET_ANALISIS = "Análisis"
SHEET_CONTROL = "Control maestro"
CONTROL_COL_REF = 2      # columna B: 'Análisis!C11'
CONTROL_COL_OBS = 14     # columna N: Observaciones
CONTROL_COL_TIPO = 15    # columna O: Tipo (R/C/M/S) — solo existe en algunas versiones del libro; no se usa para localizar filas

# Orden canónico de las 37 celdas de juicio
JUDGMENT_CELLS = [
    "C11", "C12", "C13", "C14", "C17", "C18", "C19", "C20", "C25", "C27",
    "C51", "C56", "C61", "C62",
    "B65", "C65", "D65", "B66", "C66", "D66",
    "B67", "C67", "D67", "B68", "C68", "D68", "B69", "C69", "D69",
    "C76", "C93", "C97", "C98", "B101", "B102", "C103", "C104",
]
assert len(JUDGMENT_CELLS) == 37

# Celdas de datos (parte automática): no se tocan nunca
DATA_CELLS = ["B3", "D3", "B4", "D4", "C24", "C26", "C28", "C31", "C32", "C33", "C34", "C37",
              "C40", "C41", "C42", "C46", "C47", "C48", "C49", "C50", "C52", "C53", "C54", "C55",
              "C57", "C60", "C88", "C96"]

# Vocabularios con error activado en la plantilla (valor obligatorio de la lista)
ENFORCED = {
    "C11": ["Sí", "No"], "C12": ["Sí", "No"], "C13": ["Sí", "No"],
    "C17": ["Sí", "No"], "C18": ["Sí", "No"], "C19": ["Sí", "No"],
    "C25": ["Sí", "No"], "C103": ["Sí", "No"], "C51": ["Sí", "No"],
    "C14": ["Compounder", "Calidad a precio razonable", "Deep value / especial",
            "Cíclica / commodity", "Turnaround / situación especial"],
    "C20": ["Incert. alta + riesgo bajo", "Ambos bajos", "Riesgo real alto"],
    "C27": ["Expandiendo", "Estable", "Comprimiendo"],
    "C97": ["Comprando", "Neutral", "Vendiendo"],
    "C98": ["Buena", "Aceptable", "Dudosa"],
    "C61": ["Sí", "No", "No está claro"],
    "C62": ["Sí", "No · financiación cambia mucho", "No · este tipo de empresa requiere otro método"],
    "C93": ["Sí", "No", "No lo sé"],
}

# Listas sugeridas (sin error activado: se admiten otros valores, pero se prefieren estos)
SUGGESTED = {
    "B65": ["Pierde cuota frente a la competencia", "El viento de cola se frena", "Cae el ciclo del sector",
            "Márgenes se comprimen (costes o precios)", "Compra cara o mala gestión del capital",
            "Regulación o cambio tecnológico", "La deuda aprieta", "Otra (explícala en tus palabras)"],
    "C65": ["Sigue como los últimos 5 años", "Crece al ritmo de su mercado", "Márgenes estables, sin sorpresas",
            "El viento de cola sigue, sin acelerar", "Otra (explícala en tus palabras)"],
    "D65": ["El viento de cola acelera", "Gana cuota: el moat se ensancha", "Márgenes suben por escala o precios",
            "Nuevo producto o mercado funciona", "Recompra acciones a buen precio", "Otra (explícala en tus palabras)"],
    "B67": [-0.1, -0.05, -0.02, 0, 0.02, 0.03, 0.04],
    "C67": [0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09],
    "D67": [0.08, 0.1, 0.12, 0.15, 0.18, 0.2, 0.25],
    "B68": [0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03],
    "C68": [0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03],
    "D68": [0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03],
    "B69": [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6],
    "C69": [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6],
    "D69": [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6],
    "C56": [0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.15],
}

NUMERIC = {"C56", "B67", "C67", "D67", "B68", "C68", "D68", "B69", "C69", "D69", "C76"}
TEXT_FREE = {"B66", "C66", "D66", "B101", "B102", "C104"}


def to_number(v):
    """Convierte '0,03', '3%', '3 %', 0.03 → float. Lanza ValueError si no puede."""
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(" ", "")
    pct = s.endswith("%")
    s = s.rstrip("%").replace(",", ".")
    x = float(s)
    return x / 100.0 if pct else x


def judgment_rows(cm):
    """Fila de Control maestro de cada celda de juicio, localizada por la referencia de la columna B
    ('Análisis!C11'). No depende de la columna Tipo, que no existe en todas las versiones de la plantilla."""
    rows = {}
    for row in range(1, cm.max_row + 1):
        ref = cm.cell(row, CONTROL_COL_REF).value
        if isinstance(ref, str) and ref.startswith("Análisis!"):
            key = ref.split("!")[-1].strip()
            if key in JUDGMENT_CELLS and key not in rows:
                rows[key] = row
    return rows
