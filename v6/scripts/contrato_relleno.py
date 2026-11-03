#!/usr/bin/env python3
"""Genera el contrato de relleno de la V6.3: qué celdas se escriben, cuáles se calculan
y qué exige cada motor. Pensado para quien (persona o agente) rellene la hoja.

Uso: python3 contrato_relleno.py Plantilla_V6.3.xlsx salida.csv
"""
import csv, sys
from openpyxl import load_workbook

HOJAS = ["Análisis", "Historia", "Palancas", "Control maestro"]

# Exigencia por motor de las filas de Historia, tal y como la aplican las reglas V05 y V23.
HIST = {
 5:("Año fiscal","obligatorio","obligatorio","obligatorio","sin huecos, el más reciente en L"),
 6:("Ventas","obligatorio en la ventana de f","obligatorio","—","vacío = desconocido"),
 7:("EBIT","obligatorio en la ventana de f","obligatorio","—","vacío = desconocido"),
 8:("Amortizaciones D&A","obligatorio en la ventana de f","—","—","vacío = desconocido"),
 9:("Beneficio neto","—","—","obligatorio","vacío = desconocido"),
 10:("Tipo impositivo","obligatorio en la ventana de f","obligatorio","—","vacío = desconocido"),
 11:("CFO","opcional","opcional","opcional","alimenta anclas informativas"),
 12:("Capex","obligatorio en la ventana de f","—","—","vacío = desconocido"),
 13:("Adquisiciones","opcional","opcional","opcional","no entra en la calibración de f"),
 14:("Circulante","obligatorio en la ventana de f","—","—","vacío = desconocido"),
 15:("Intereses pagados","—","obligatorio","—","define el coste histórico de la deuda"),
 16:("Intereses en financiación","opcional","opcional","opcional",""),
 17:("Principal de arrendamientos","opcional","opcional","opcional",""),
 18:("SBC","opcional","opcional","opcional",""),
 19:("I+D","opcional","opcional","opcional",""),
 20:("Acciones diluidas (media)","opcional","opcional","opcional","no es Análisis C55"),
 21:("Patrimonio neto","—","—","obligatorio","vacío = desconocido"),
 22:("Deuda financiera","—","obligatorio (L)","—","escribe 0 si no hay"),
 23:("Arrendamientos","—","obligatorio (L)","—","escribe 0 si no hay"),
 24:("Caja","—","obligatorio (L)","—","vacío = desconocido, nunca 0"),
 25:("Pensiones (posición neta)","—","obligatorio (L)","—","déficit > 0 se resta; superávit < 0 se trata como 0 con aviso; escribe 0 si no hay"),
 26:("Minoritarios","—","obligatorio (L)","—","escribe 0 si no hay"),
}

def main(src, dst):
    wb = load_workbook(src)
    filas = []
    for h in HOJAS:
        ws = wb[h]
        dv_coords = set()
        for dv in ws.data_validations.dataValidation:
            for rng in str(dv.sqref).split():
                dv_coords.add(rng)
        for row in ws.iter_rows():
            for c in row:
                if c.value is None:
                    continue
                es_formula = isinstance(c.value, str) and c.value.startswith("=")
                if h == "Historia" and c.column >= 3 and c.row in HIST and not es_formula:
                    continue  # se resume aparte
                if es_formula:
                    continue
                etiqueta = ws.cell(c.row, 1).value if c.column > 1 else c.value
                filas.append([h, c.coordinate, str(etiqueta)[:70], "entrada",
                              "lista" if c.coordinate in dv_coords else "", ""])
    with open(dst, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["CONTRATO DE RELLENO · Plantilla V6.3"])
        w.writerow(["Convención: en Historia una celda vacía significa DATO DESCONOCIDO, nunca cero."])
        w.writerow(["Para declarar un cero comprobado hay que escribir 0."])
        w.writerow([])
        w.writerow(["Historia · fila", "Concepto", "Motor A", "Motor B", "Motor C", "Nota"])
        for r, v in sorted(HIST.items()):
            w.writerow([r, *v])
        w.writerow([])
        w.writerow(["Dominios: deuda, arrendamientos, caja, minoritarios, D&A, capex, intereses, SBC, I+D y acciones no admiten negativos (DATOS INVÁLIDOS)."])
        w.writerow(["FCF, resultados, circulante y adquisiciones netas sí pueden ser negativos."])
        w.writerow([])
        w.writerow(["Evidencias (Control maestro, columnas F y J de cada entrada que usa el motor activo; inventario en el bloque 176+)"])
        w.writerow(["DATO: F = Rellenado y verificado + J con documento", "documentada (fuente declarada por el analista)"])
        w.writerow(["HIPÓTESIS o decisión: F = Hipótesis confirmada + justificación en J, M o N", "razonada y confirmada; marcarla como «Rellenado y verificado» es incoherente"])
        w.writerow(["F = Estimación declarada + justificación", "estimación: el libro queda LISTO · PROVISIONAL"])
        w.writerow(["F = Dato no verificable / Pendiente de inversor / vacío", "pendiente: el libro queda NO LISTO · evidencias incompletas"])
        w.writerow(["F = No aplicable en una entrada que el motor usa", "indebido: cuenta como pendiente"])
        w.writerow(["Qué es dato y qué es hipótesis, por motor y condición de uso", "scripts/relacion_entradas_materiales.py y docs/Matriz_cobertura_evidencias_V6_3.md"])
        w.writerow([])
        w.writerow(["Salidas que no se deben escribir nunca (las protege la regla V39 y el verificador externo)"])
        for s in ["Análisis!C52", "Análisis!B78:D78", "Análisis!C83:C86", "Historia!C44",
                  "Historia!C48", "Historia!C52", "Historia!C58", "Historia!C70",
                  "Diagnóstico V6!C5", "Diagnóstico V6!C12", "Diagnóstico V6!C32",
                  "Panel!K20", "Panel!K25"]:
            w.writerow([s])
        w.writerow([])
        w.writerow(["Salidas que lee el kit del personaje (direcciones estables)"])
        for s in ["Análisis!B78:D78 valores por escenario", "Análisis!C83 ponderado",
                  "Análisis!C84 margen de seguridad", "Análisis!C37 precio",
                  "Análisis!A6 veredicto", "Motor!B266 estado del libro",
                  "Motor!B268 veredicto principal", "Motor!B269 estado de las evidencias (Control maestro D212)",
                  "Diagnóstico V6!C156 precio de referencia"]:
            w.writerow([s])
        w.writerow([])
        w.writerow(["Hoja", "Celda", "Etiqueta", "Tipo", "Validación", ""])
        w.writerows(filas)
    print(f"{len(filas)} entradas · {dst}")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
