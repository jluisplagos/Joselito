# Vidrala · cambios v1 → v2 (25-oct-2026)

## Celdas cuyo valor cambia
- C97 · Neutral → Comprando · fallo A confirmado + regla C97 del inversor: la sección 3 de datos_automaticos (C97, oct-2025 a oct-2026, insiderscreener) trae 19 compras y 1 venta pequeña, compras concentradas mar–jul 2026, director general 19.000 acciones ≈1,41 mm€. No es aislada ni mixta ni ligada a planes; Comprando por la rama del primer ejecutivo con importe relevante (que el DG sea el primer ejecutivo y que el importe sea relevante es lectura mía). Confianza baja: fuente secundaria, CNMV art. 19 MAR no consultada, fase 1 «celda vacía hasta verificar».
- B101 · «en Iberia, Reino Unido y Brasil» / «(0,2x EBITDA en 2025)» → «en Iberia, Reino Unido e Irlanda, Brasil y, desde el 30-mar-2026, Chile» / «(0,69x EBITDA a 30-jun-2026 según C33; 0,2x a cierre de 2025 según la empresa)» · texto mal: faltaba Chile (datos_automaticos §2, B4) y el apalancamiento estaba desfasado (§2, C33). El resto del texto no cambia.
- B102 · «porque ningún documento lo nombra» → «los informes no nombran competidores, y los pares de múltiplos que cita Control maestro (Verallia, O-I, Vetropack, Zignago, fuente secundaria) no traen cuotas ni mercados» · texto mal: datos_automaticos §2, C42, sí nombra pares. El resto no cambia.
- Cubo (VIGILAR), precio de Sí (≈48,06 €; malo 48,06, ponderado 76,54, ¾ 57,41), escenarios, probabilidades, g, C76, C104 y las demás celdas: sin cambio.

## Observaciones cambiadas (texto; el valor de la celda no cambia salvo C97)
- C97 · reescrita · regla C97 con los hechos de la sección 3 (C97); confianza media → baja por fuente secundaria pendiente de verificar.
- C76 · «C54 y C34 no cuadran» → explicado por fecha: C54 = 169,6 + 240,1 a 30-jun-2026, C34 = 109,4 ÷ 240,1 = 0,46; a 31-dic-2025 262,9 mm y C34 = Sí (1,62); deuda corriente ×3,6 en el semestre (§2, C34, C54). Deuda neta actualizada a 300,2 mm con arrendamientos / 252,3 mm APM (§2, C33, C54); dividendo de 16,5 mm pagado el 15-jul (§2, C53); caja operativa 29-44 mm y recomendación 0 (§3, C76); «compra de Chile pendiente» → consolida desde 30-mar-2026 (§2, B4). Fallo B aceptado.
- C20, C62 · «deuda neta 0,2x EBITDA» → 0,69x a 30-jun-2026 (C33), 0,36x a 31-dic-2025 mismo criterio; C20 añade C34 = No y líneas de 258 mm (§2, C33, C34); C62 añade que la base de 3 años es decisión del inversor (§2, C40). Fallo B aceptado; C62 = Sí se mantiene (umbral 2x).
- D65, D66, D67, D69 · «Chile pendiente / si Chile no se cierra» → Chile consolida desde 30-mar-2026 (§2, B4); los disparadores pasan a «si Chile no crece en euros / el real sigue cayendo». Fallo B aceptado; valores iguales.
- C14, C18 · ROIC 13 % precisado como ROIC después de impuestos (definición A, LTM 30-jun-2026, decisión del inversor), con ROCE antes de impuestos 17,2 % y serie 2019-2025 16,3-19,8 % (§2, C24). Fallo B aceptado; C14 y C18 sin cambio.
- C18, C12 · «ningún documento nombra competidores» → los informes no los nombran; Control maestro C42 cita pares de fuente secundaria sin cuotas (§2, C42). Hallado en el repaso.
- C13, C25 · el FCF publicado por la empresa es una APM (variación de deuda neta), no comparable (§2, C40); se añaden FCF por fórmula 185,9 mm (2025), media 5 años 129,5 mm y LTM 94,6 mm con circulante −130,9 mm y existencias +17,8 % (§2, C40, C31). C25 sigue en Sí (bache de circulante), confianza media → baja. Hallado en el repaso.
- C98 · añade recompras 2026 (≈1,02 mm acciones a 25-sep; 52,7 mm en 1S) y deuda neta 300,2 mm (§2, C28, C33, C34); el precio medio de las recompras no está en las entradas. Valor Buena sin cambio.
- B101, B102 · nota de la corrección del texto de la celda.

## respuesta.md
- Primera línea de v2; §1 (b): C55 explicado (35,206 emitidas − ≈1,021 autocartera, §2 C55) y efecto de la liberada 1×20 (≈35,89 mm, precio ex ≈84,48 €, §2 C37); §2: competidores (C42), notificaciones CNMV de insiders (C97), precio de las recompras 2026, desglose de deuda a 30-jun-2026 en lugar de «datos que no cuadran»; §3 pregunta 1: compras de insiders de fuente secundaria; §4 y §5 regenerados desde juicio.json.

## Fallos del barrido no aceptados o aceptados solo en parte
- Fallo 4 (respuesta §2, base de acciones): aceptado como texto; no hay discrepancia que corregir en ninguna celda.
- Fallo 2 (C76/§2 y «0,2x» en C20/C62/B101): aceptado; C76 = 0 y C62 = Sí se mantienen. En B101 se conserva el 0,2x de cierre de 2025 de la empresa junto al 0,69x actual, porque el dato es correcto con su fecha.
- Fallo 5 y B102: el «ROIC de la plantilla es del 13 %» de B102 es correcto (C24) y se deja palabra por palabra.
- Fallo 5 (C14/C18): aceptado solo como precisión de texto; la serie estable de ROCE no cambia C14 (Cíclica / commodity) ni C18 (Sí).
- Ninguno rechazado por ser falso: los cinco se comprobaron en datos_automaticos.
