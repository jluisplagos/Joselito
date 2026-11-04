# Comprobación de entrada · Hermes_v63_evaluada.xlsx

- Íntegro (verificar_v63.py): True · estado técnico: INCOMPLETO (Faltan palancas de crecimiento (Palancas B14:D14)) · estado del libro: NO LISTO · incompleto (5 pendientes) · comparable precio↔valor: True · años con ventas: 10

## Motores calculables (simulación con palancas de prueba)

- Motor A: CALCULABLE
- Motor B: NO calculable · reglas de nivel 1 que fallan: V23 INCOMPLETO: Motor B: no se puede calcular la r operativa (Historia L15, L22, L23 y Análisis C41)
- Motor C: CALCULABLE
- Motor elegido por la fase A: A → calculable

## BLOQUEANTE (el pipeline se detiene: pendiente_de_datos)

- ninguno

## Necesario para LISTO · PROVISIONAL (no para el valor)

- ninguno

## No bloqueante

- Palancas!C24: tamaño del mercado año 10 · de dónde: extractos (solo con cifra de fuente primaria)

## Avisos de la hoja

- V19 AVISO: Probabilidad de quiebra vacía (Palancas C22): se asume 0 por convención, no es un riesgo medido
- V28 AVISO: Precio y acciones con fechas separadas más de 90 días (Palancas C45, C46)
- V31 AVISO: Fecha de análisis escrita como texto (Análisis D4): escríbela como fecha
