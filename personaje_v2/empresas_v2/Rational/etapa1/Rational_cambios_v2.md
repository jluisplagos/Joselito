# Rational · cambios v1 → v2 (25-oct-2026)

## Celdas cuyo valor cambia
- C76 · 150 → 200 · fallo A confirmado. Se cumple la condición de v1: el dividendo se pagó el 5-may-26 y a 30-jun-2026 no hay nada comprometido. Caja literal 205,98 m y liquidez total 431,7 m (datos_automaticos, Control maestro C53). Resto arrendamientos de 27,6 m (C54), 13,5 m con controles de capital (C34) y la reserva de ≈135 m de v1. Queda ≈255 m, con tope en C53 (205,98) → 200, cifra redonda ≤ C53.
- B101 · «la compraría hacia 284 €» → «hacia 288 €» · coherencia: el precio de Sí sube por C76.
- B102 · «el valor queda un 28 % por debajo del precio» → «27 %» · coherencia: el normal estimado pasa de ≈409 € a ≈413 € por C76.
- C104 · «precio de Sí ≈ 284 €» → «≈ 288 €» · coherencia: el precio de Sí cambia con C76.
- precio_de_si · 284 → 288 (estimación) · coherencia con C76. Con la fórmula de la plantilla (FCF 219,2; r 0,09; 2/6/10 % y 1,5/2,5/3 %; C76 200; 11,37 m de acciones) salen: malo ≈288,2, normal ≈413,4, bueno ≈583,0, ponderado ≈422,3 y ¾ del ponderado ≈316,7 → mínimo 288. Es una estimación; el script recalcula el exacto.
- cubo · VIGILAR → VIGILAR (sin cambio).

## Observaciones y textos corregidos (valor de la celda sin cambio)
- C97 · Neutral → Neutral · fallo A, resuelto por la decisión del inversor (C97 = Neutral) y por la regla C97. La v1 decía «no hay registro de operaciones». La fase 1 trae una única operación en la ventana 8-oct-2025 a 8-oct-2026: el 9-dic-2025, Franziska Würbser, persona estrechamente vinculada a Dr. J. Würbser (Aufsichtsrat), vendió ~27.000 acciones (16,6 mm EUR) sin mención de plan (datos_automaticos §3, C97). Es una operación aislada → Neutral. Se reescribe la Observación y su «Lo sustituiría».
- C62 · texto · fallo B confirmado. C40 es el LTM jul-25–jun-26 y C52 la media FY2023–25 que decidió el inversor (Control maestro C40 y C46). Son ventanas distintas, no una discrepancia.
- C68 · texto · fallo B confirmado. C88 = 38,3 es el P/FCF histórico: mediana de FY2019 y FY2023–25, rango 36,5–54,7, y hoy cotiza a 25,8x el FCF LTM (Control maestro C88). El múltiplo implícito de mi normal (≈16x) queda por debajo de esa historia. C68 no cambia.
- C51 · texto · fallo B confirmado. No hay opciones vivas: el plan de 2000 se liquidó en 2002/2006 (Control maestro C50) y queda un capital condicional de 200.000 acciones sin opciones vivas (C28). Se quita «quedan 131.000 derechos».
- C61 · texto · el mismo motivo que C51 (Control maestro C28 y C50). El «Lo sustituiría» pasa a hablar de emisiones del capital condicional.
- C76 · texto · reescrita con datos a 30-jun-2026 (Control maestro C53, C54, C34, C33). Se corrige «el CFO resta los intereses netos»: los intereses cobrados van en inversión y los pagados en financiación, los dos fuera del CFO (Control maestro C26 y C48), y el FCF excluye ~11,5 m de intereses cobrados (C40). Se quitan «C53 no está en el extracto» y «C33 infravalora la caja neta»: C33 usa la caja literal y con depósitos sería −1,05x (C33).
- C13 · texto · precio de Sí 284 → 288 por C76. Se aclara que los 250,1 m de C40 son el LTM (Control maestro C40).
- C20 · texto · valores estimados por C76: bueno ≈583 € y ponderado ≈422 € (+34 %). Se fecha la caja de 539 m (31-12-2025) y se añaden los 431,7 m a 30-jun-2026 (Control maestro C53).
- C56 · texto · con r 0,08 el ponderado estimado pasa de ≈497 € a ≈502 € por C76.
- B67 · texto · valor del malo de ≈284 € a ≈288 € por C76.
- D67 · texto · valor del bueno de ≈578 € a ≈583 € por C76.
- B101 (Observación) · texto · nuevos valores estimados y C76 = 200 m.
- B102 (Observación) · texto · nota del 27 % (28 % en v1) por C76.
- C104 (Observación) · texto · ≈288 €.
- respuesta.md §1 · precio de Sí, valores por escenario, C76 y asimetría (≈+3 % / ≈−49 %) actualizados por C76.
- respuesta.md §2 · se quitan tres puntos ya resueltos por la fase 1: el resultado de la Junta y el dividendo (C53), el origen de C53/C54 y el periodo de C40 (C40, C53, C54), y el P/FCF histórico (C88). El punto de acciones y operaciones de directivos se corrige con Control maestro C96 y C97.
- respuesta.md §7 · «A Sí» pasa a ≈288 € y se quita «300–315 € si el script da un malo mayor».

## Fallos del barrido no aceptados
- Ninguno rechazado del todo. C76: acepto el fallo, pero no lo llevo a 206 como propone el barrido, sino a 200. 206 supera a C53 (205,98) y la regla pide C76 ≤ C53 y una cifra redonda. El efecto es ≈+4,4 €/acción, no ≈+4,9 €.
- Revisé y dejé sin cambiar C25, que no contradice la fase 1. La serie de FCF recurrente de la fase 1 (120→166→196→237→236, LTM 244) apoya el Sí, igual que v1.
- Revisé y dejé sin cambiar C27, que tampoco la contradice. La fase 1 da 25,9 % LTM sin reembolso y v1 da 24,3 % en H1-26 sin reembolso: son periodos distintos.
