# Comprobación de entrada · Nike_v63_datos.xlsx

- Íntegro (verificar_v63.py): True · estado técnico: INCOMPLETO (Faltan intereses en financiación o principal de arrendamientos (Análisis C48, C49): escribe 0 si la empresa no tiene; un vacío no es un cero) · estado del libro: NO LISTO · incompleto (7 pendientes) · comparable precio↔valor: True · años con ventas: 10

## Motores calculables (simulación con palancas de prueba)

- Motor A: NO calculable · reglas de nivel 1 que fallan: V09 INCOMPLETO: Faltan intereses en financiación o principal de arrendamientos (Análisis C48, C49): escribe 0 si la empresa no tiene; un vacío no es un cero
- Motor B: NO calculable · reglas de nivel 1 que fallan: V23 INCOMPLETO: Motor B: faltan pensiones o minoritarios del último año (Historia L25, L26); escribe 0 si no hay
- Motor C: CALCULABLE

## BLOQUEANTE (el pipeline se detiene: pendiente_de_datos)

- ninguno

## Necesario para LISTO · PROVISIONAL (no para el valor)

- evidencia Análisis!C48: Intereses pagados clasificados en financiación · IFRS: no aplicable indebido · de dónde: fase1_v63.json (fuente y página del dato) o etapa 1 · el dato está pero su clasificación/documento no permite LISTO·PROVISIONAL; la fase C juzga si es material
- evidencia Análisis!C49: Principal de lease liabilities · IFRS 16: no aplicable indebido · de dónde: fase1_v63.json (fuente y página del dato) o etapa 1 · el dato está pero su clasificación/documento no permite LISTO·PROVISIONAL; la fase C juzga si es material

## No bloqueante

- Palancas!C24: tamaño del mercado año 10 · de dónde: extractos (solo con cifra de fuente primaria)

## Avisos de la hoja

- V19 AVISO: Probabilidad de quiebra vacía (Palancas C22): se asume 0 por convención, no es un riesgo medido
- V28 AVISO: Precio y acciones con fechas separadas más de 90 días (Palancas C45, C46)
- V31 AVISO: Fecha de análisis escrita como texto (Análisis D4): escríbela como fecha
