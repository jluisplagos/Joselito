# Comprobación de entrada · EmpresaX_sin_precio_v63_datos.xlsx

- Íntegro (verificar_v63.py): True · estado técnico: INCOMPLETO (Falta el precio (Análisis C37)) · estado del libro: NO LISTO · incompleto (7 pendientes) · comparable precio↔valor: True · años con ventas: 10

## Motores calculables (simulación con palancas de prueba)

- Motor A: NO calculable · reglas de nivel 1 que fallan: V06 INCOMPLETO: Falta el precio (Análisis C37)
- Motor B: NO calculable · reglas de nivel 1 que fallan: V06 INCOMPLETO: Falta el precio (Análisis C37)
- Motor C: NO calculable · reglas de nivel 1 que fallan: V06 INCOMPLETO: Falta el precio (Análisis C37)

## BLOQUEANTE (el pipeline se detiene: pendiente_de_datos)

- Análisis!C37: precio actual (en la moneda del modelo) · de dónde: fase1_v63.json (precio con fecha y, si hace falta, tipo de cambio)
- Historia / datos: ningún motor calcula con los datos presentes · de dónde: fase1_v63.json (Contrato_de_relleno_V6.3.csv) · A: V06 INCOMPLETO: Falta el precio (Análisis C37) · B: V06 INCOMPLETO: Falta el precio (Análisis C37) · C: V06 INCOMPLETO: Falta el precio (Análisis C37)

## Necesario para LISTO · PROVISIONAL (no para el valor)

- evidencia Análisis!C46: Caja de las operaciones (media 3–5 años): no verificable · de dónde: fase1_v63.json (fuente y página del dato) o etapa 1 · el dato está pero su clasificación/documento no permite LISTO·PROVISIONAL; la fase C juzga si es material
- evidencia Análisis!C47: Capex (positivo; media 3–5 años): no verificable · de dónde: fase1_v63.json (fuente y página del dato) o etapa 1 · el dato está pero su clasificación/documento no permite LISTO·PROVISIONAL; la fase C juzga si es material
- evidencia Análisis!C48: Intereses pagados clasificados en financiación · IFRS: no verificable · de dónde: fase1_v63.json (fuente y página del dato) o etapa 1 · el dato está pero su clasificación/documento no permite LISTO·PROVISIONAL; la fase C juzga si es material
- evidencia Análisis!C49: Principal de lease liabilities · IFRS 16: no verificable · de dónde: fase1_v63.json (fuente y página del dato) o etapa 1 · el dato está pero su clasificación/documento no permite LISTO·PROVISIONAL; la fase C juzga si es material
- evidencia Análisis!C50: Stock-based compensation (SBC): no verificable · de dónde: fase1_v63.json (fuente y página del dato) o etapa 1 · el dato está pero su clasificación/documento no permite LISTO·PROVISIONAL; la fase C juzga si es material

## No bloqueante

- Palancas!C24: tamaño del mercado año 10 · de dónde: extractos (solo con cifra de fuente primaria)
- Análisis!C88: P/FCF histórico · de dónde: fase1_v63.json
- Análisis!C38: valor intrínseco de fuente externa (contraste) · de dónde: fase1_v63.json (opcional)

## Avisos de la hoja

- V19 AVISO: Probabilidad de quiebra vacía (Palancas C22): se asume 0 por convención, no es un riesgo medido
- V31 AVISO: Fecha de análisis escrita como texto (Análisis D4): escríbela como fecha
