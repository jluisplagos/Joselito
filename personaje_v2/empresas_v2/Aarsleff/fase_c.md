# Per Aarsleff Holding A/S (PAAL B) · fase C · turno 1 · 2026-11-04

Motor A · r 0,09 (heredada; r mínima 0,0772) · precio 729 · MALO 346,99 · NORMAL 515,69 · BUENO 708,00 · probabilidades 0,25/0,6/0,15 · ponderado 502,36 · precio de Sí 450,57 · zona **caro** (precio.json). Reviso lo de A y B como si fuera de otro: «intensively consider any evidence tending to disconfirm any hypothesis of his» (PCA p.528; HIM).

## 1. Una sola historia

Lo que la hoja calcula con mis 52 celdas cuenta la historia de la fase A: un contratista que rinde por encima de r porque usa poco capital, sin foso, a un precio que paga más que mi mejor escenario. El precio (729) está por encima del valor del BUENO (708). El DCF inverso pide 17,1% de crecimiento anual en los años 1-5 con el resto del NORMAL (C86); ninguna ventana de cinco años de la Historia pasó de 11,2%, y esa llevaba compras (Historia C46, filas 13 y 28). Pagas 352,6 por acción por un crecimiento que en el NORMAL vale 139,3.

Semáforos: margen del BUENO por encima del máximo (G5, ya justificado en B); S2C medio fuera del rango del sector (aviso A1), coherente con el cobro por avance; peso del terminal 0,46/0,59/0,66, bajo el 75% (G16 no aplica); cuota implícita no calculable sin C24 (G17 no aplica). Tornado del NORMAL, solo como información: el margen pesa más que nada (±2 puntos: 255,9), después la tasa (96,6) y el ROIC terminal (87,5).

Incoherencias que encontré:

- **Mecanismo del margen NORMAL (C66, Palancas!C15).** La fase A dice «ejecución y mezcla». La serie por segmento no muestra mezcla. Construction pasó de 3,4% y 3,0% (2020/21-2021/22) a 5,7%, 5,2% y 5,5% [AR_2025, PDF pp. 26-34], con un peso estable del 46-47% [AR_2025, PDF p. 115]. Eso explica por sí solo unos 1,2 de los 1,3 puntos del escalón del grupo de 2022 a 2023 (Historia fila 29). Pipe Technologies apenas ganó peso (10,9% → 11,5%). El escalón es del segmento más ligado a la obra pública danesa: más marea o ejecución en la ola que mezcla. No muevo la palanca porque 0,05 queda dentro de un rango atado a hechos (punto 7).
- **Probabilidades (B69:D69).** El hecho citado mide un nivel de margen (siete de diez años en la banda del MALO), no un escenario de cinco años. Las cinco ventanas de cinco años de la Historia crecieron entre 7,0% y 11,2% anual: la década es un solo ciclo al alza.
- **Base del margen (Palancas!C8) frente a la historia NORMAL.** El motor parte de m0 = 4,32% (datos_v63 §5) y llega al 5,0% en el año 5, mientras C66 dice que el margen se sostiene. Es la convención de una cíclica (UD p. 3; E5). Estimo que cuesta unos 11 por acción, el 2% del NORMAL. La fase B usó el mismo argumento para dejar el objetivo bajo la media de 2023-2025, pero sin efecto: 5,2% redondea a 0,05.
- **FCF base (C52 = 872,7, con unos 493 de circulante liberado).** El motor no proyecta desde C52 sino desde ventas × margen. El FCF del año 1 es 574 en el MALO y 387 en el NORMAL, así que no hay doble cuenta. Que el MALO dé más caja el año 1 es la reinversión del crecimiento, no un error.
- **Aviso A3 (fechas del precio y de las acciones).** Las recompras hasta febrero de 2026 bajan algo las acciones. El valor por acción está infravalorado en décimas, sin efecto en la zona.
- **A6 = DESCARTADA POR FILTRO PABRAI.** Mi cubo es Vigilar: el negocio es evaluable y aceptable, lo que falta es precio (regla 4 de la sección 17).

## 2. Desviaciones pendientes (gramatica.md)

Solo quedan G8 NORMAL (5,6 puntos) y G8 BUENO (8,6 puntos). G16 y G17 no se disparan.

- **G8 NORMAL.** Durante los años 1-10 cada euro nuevo rinde 4,1 × 0,05 × 0,76 = 15,6%, lo que la empresa ya hizo en diez años (ROIC 10,1-16,7%, Historia fila 33). Crece con poco capital porque cobra por avance: trabajos en curso netos de solo 390 sobre un precio de venta de 35.762 [AR_2025, PDF p. 130]. En el año 11 pierdo el exceso que ningún foso defiende. El escalón de margen es de Construction en plena ola. Ground Engineering, con el mismo grupo detrás, cayó de 4,9% a 2,6% de margen y a un ROIC de 3,8% en un año cuando llegó la competencia de precio [AR_2025, PDF pp. 33 y 115]. Conservo lo que la década demuestra sin marea: 0,10 es el suelo propio (10,1% en 2017), un punto sobre r y no tres (MR p. 63; E2).
- **G8 BUENO.** En el BUENO, 4,7 × 0,055 × 0,76 = 19,6% es una renta de escasez de capacidad: 'it is largely our own capacity that determines what and how much we in the Aarsleff Group can bid for' [AR_2025, PDF p. 7]. Se pierde cuando la escasez termina. Pongo 0,11, entre el suelo de diez años y el 12% que la empresa exige a su capital nuevo [AR_2025, PDF p. 18]. No sostengo a perpetuidad más de lo que la propia empresa pide.

Las dos van con clase fundamentada y con hechos de celda y página en `desviaciones_justificadas`. «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM): la respuesta aquí es que dura el poco capital y no dura la ola.

## 3. Palancas: no las muevo

No encuentro ninguna palanca mal derivada. Rehice las cuentas de la fase B: S2C del MALO 9.325 ÷ 3.120 = 3,0; del NORMAL 12.200 ÷ 2.988 = 4,1; cartera +4,9% anual en tres cierres; las tres rentabilidades marginales; margen pro forma del BUENO 5,7%. Todas cuadran, y el perímetro de la S2C incluye las compras igual que el crecimiento. Las dos dudas de fondo (mecanismo del margen y probabilidades) son de fundamento, no de aritmética. Además, con cualquier valor de sus rangos la zona sigue siendo caro: el precio de Sí no puede pasar del NORMAL (515,7), y el precio es 729. `revisar_palancas = false`. En `celdas_corregidas` dejo C66, Palancas!C15, B69:D69 y Palancas!C8 con despues = antes y el motivo.

## 4. Autocomprobación

- **Anclaje en la etapa 1.** El precio de Sí v1 era ≈ 465 y el v2 es 450,57, por caminos distintos (ponderado v1 ≈ 775, v2 502). Las celdas mantenidas nombran su evidencia. No cambio nada.
- **Anclaje en el precio o en la fuente externa.** Mis valores quedan muy por debajo de 729 y del valor externo de C38 (1.030,6). La pregunta contraria: «For a security to be mispriced, someone else must be a damn fool» (TCI p.17; HIM). El mercado paga que el ROIC de 14-15% no decaiga. Si me equivoco, es en C18. La empresa descuenta sus segmentos al 9,4-9,8% [AR_2025, PDF p. 125], así que no es mi r lo que separa los dos números.
- **Consistencia y compromiso.** Las desviaciones de la fase B van en los dos sentidos, y el cubo no dependía de ellas. Reabro dos hipótesis mías en vez de defenderlas.
- **Historia bonita / viento de cola.** El escalón es de Construction durante la ola, no de la mezcla. La hipótesis H2 entra en la lista.
- **Optimismo del BUENO.** Crece 10%, por debajo del mejor quinquenio propio. Su rentabilidad marginal está por debajo de 2 × C55 y su probabilidad por debajo de la del MALO. Sin C24 no puedo probar la cuota.
- **Doble castigo.** No hay prima en la r, la quiebra está vacía y las garantías van solo en el MALO (PA p. 20; E6). Hay un doble uso del argumento de la media del ciclo, pero sin efecto numérico.
- **Disponibilidad.** Fehmarnbelt pesa 0,05 de probabilidad. Un sobrecoste del 10% sobre 3,7 bn [AR_2025, PDF p. 128] serían unos 19 por acción, del mismo orden.
- **Autoridad.** El crecimiento y el margen NORMAL coinciden con el suelo de la guía, y el margen del BUENO con el objetivo. Cada uno tiene su hecho propio. Añado un dato de la dirección en contra: Construction guiado en 4,5-5,0% [AR_2025, PDF p. 9].
- **¿El MALO es malo?** Diez años sin crecer, margen de 4,0% y ROIC = r: vale 347, un 52% bajo el precio. Es real sin ser suelo: el mínimo propio fue 3,4% y no hay pérdida explícita de Fehmarnbelt. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM).
- **Lo no numerable.** La fundación con el 44,7% de los votos, la seguridad (14,6 frente a 5 [AR_2025, PDF p. 5]) y la responsabilidad solidaria de 2.095 [AR_2025, PDF p. 141]. Van a la tesis inversa.

## 5. Cubo y conclusión provisionales

Orden de mando:

- **Bloqueo:** ninguno (0 errores de gramática).
- **Límite del modelo:** no; el motor A vale.
- **Descalificador:** ninguno. Revisé otra vez «reinvierte todo para mantenerse». El FCF después de compras de cinco años es solo 234 (C40), pero el ROIC está entre 10,1% y 16,7%: reinvierte creciendo, no manteniéndose. Solo el MALO (rentabilidad marginal 9,1% = r) es ese negocio.
- **Dato ausente material:** ninguno (punto 6).
- **Fundamento material:** con esperar no limita la conclusión. Marca el precio objetivo como provisional por B69:D69.
- **Zona:** caro.

**Cubo provisional: Vigilar. Conclusión provisional: esperar**, con precio de Sí ≤ 450,57, provisional. Hace falta que el precio baje un 38%.

## 6. Datos ausentes (S-19)

Reviso los 21 de `datos_ausentes.json`, cada uno con su celda o conclusión afectada. Ninguno es material: `alguno_material = false`. Los que más miré:

- **Nueve meses de 2025/26.** El margen de nueve meses subestima el año por estacionalidad: en 2024/25 los tres primeros trimestres dieron 4,7% y el año cerró en 5,2% [AR_2025, PDF p. 25]. El disparador de Palancas!C15 es el cierre anual.
- **Tamaño de mercado y cuota (C24, G17).** El límite del BUENO es la capacidad propia [AR_2025, PDF p. 7], no el mercado.
- **Covenant y rating.** Deuda neta/EBITDA de 0,64 y 1.714 sin usar de la RCF [AR_2025, PDF p. 135].
- **Competidores.** El MALO se apoya en la presión de precio documentada por segmento.

## 7. Fundamento material (D10)

Dos hipótesis insuficientemente fundamentadas, aunque la fase B las clasificó como fundamentada o convención:

- **B69:D69 (0,25/0,6/0,15).** No hay frecuencia de escenarios en un solo ciclo al alza, y la dispersión no acota p(MALO). `hay_base = false`. Haría falta la serie de un ciclo bajo de la construcción danesa (informes anteriores a 2016) y la relación entre entrada de pedidos y ventas de 2025/26. Solo como información, con la misma fórmula del Anexo C: 0,2/0,6/0,2 daría un precio de Sí de unos 471 y 0,3/0,6/0,1 de unos 433. La zona es caro en todos los casos.
- **Palancas!C15 · C66 (margen NORMAL por mezcla).** `hay_base = true`, rango 0,045-0,05. El suelo es la media de diez años (4,32%, Historia C49), porque por debajo está el MALO. El techo es la media de los tres años del escalón (5,2%, Historia fila 29), porque por encima hace falta que Ground Engineering se recupere, y eso es el BUENO. El 0,05 está en el extremo favorable a la tesis.

La conclusión provisional no es favorable, así que `resultado = no_procede`, no hago comprobación conjunta y `sobrevive = null`. Con esperar y una hipótesis sin base, el precio objetivo va provisional en C104, condicionado a B69:D69.

## 8. Lo que más condiciona y qué lo resolvería

**Palancas!C15 · C66**: si el escalón de margen de 2023 es ejecución o marea. Lo resolvería el informe anual 2025/26 (cierre 30-sep-2026), con el margen de Construction y del grupo, el margen bruto y la entrada de pedidos frente a ventas:

- Si Construction se mantiene en 5% o más con Fehmarnbelt y Lynetteholm en marcha, el escalón es ejecución.
- Si Construction baja hacia su guía de 4,5% o el grupo cierra por debajo del 4,7%, es marea y el NORMAL pasa a 0,045.

Para B69:D69, los informes anteriores a 2016 y una pregunta a Relación con Inversores sobre el margen de Construction antes de 2020.

## 9. Turno 2 · conclusión

No hay `comprobacion_conjunta.json`, porque no procedía con una conclusión no favorable. `sobrevive = null` y `resultado = no_procede`.

**Estado concluido (provisional hasta la auditoría) · cubo Vigilar · acción esperar · precio objetivo 450,57.** El precio objetivo es provisional, condicionado a B69:D69. El precio tiene que bajar un 38% desde 729 para llegar ahí. No escribo ningún tamaño de posición: es decisión de José Luis.

C104: «Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 450.57 (provisional, condicionado a B69:D69) · zona caro · precio de Sí ≤ 450.57 · precio esc. MALO 346.99 · ponderado 502.36 · fundamento pendiente de investigación (probabilidades B69:D69 sin base para acotar)».

C93 = Sí. El g NORMAL de 0,02 queda bajo la rf (CV p. 5; E1) y sobre el 1,2% de las pruebas de deterioro. El peso del terminal es 0,59. C103 = No: sin foso, el negocio no aguanta mala gestión.

## 10. Tesis (B101)

- Aarsleff rinde por encima de r porque cobra por avance y usa poco capital: ROIC de 10,1 a 16,7% (Historia fila 33).
- No tiene foso. El escalón de margen de 2023 es de Construction durante la ola de obra pública (3,0 a 5,7% [AR_2025, PDF pp. 26-34]).
- Mis escenarios valen 347, 516 y 708 por acción. A 729 el precio paga más que mi BUENO y descuenta un 17,1% de crecimiento anual (C86).
- Espero. El precio de Sí es 450,57, provisional porque las probabilidades no tienen una frecuencia observada que las acote.

## 11. Tesis inversa (B102)

- El margen del grupo estuvo siete de diez años entre 3,4 y 4,4% (Historia fila 29).
- El escalón lo trajo un solo segmento, que su propia dirección ya guía en 4,5-5,0% [AR_2025, PDF p. 9].
- El FCF de 2025 lleva 1.036 de circulante que se devuelve (Historia fila 14). Después de compras, cinco años dejan 234 (C40).
- La solvencia está en 30,2%, por debajo de su objetivo (C54).
- Hay 12.135 de garantías y 2.095 de responsabilidad solidaria [AR_2025, PDF p. 141], y Fehmarnbelt tiene un 'wide outcome range' con riesgo creciente [AR_2025, PDF p. 97].
- Si el ROIC converge a r, el MALO vale 347, un 52% bajo el precio, y no es suelo. «What's the flip side, what can go wrong that I haven't seen?» (TCI p.15; HIM).

## 12. Predicciones (dado el NORMAL)

1. Margen EBIT de Construction de 2026/27 igual o superior al 5,0%: 2027-12-31, probabilidad 0,55. Pone a prueba directamente la hipótesis que más condiciona.
2. Ingresos del grupo de 2026/27 iguales o superiores a 25.000: 2027-12-31, probabilidad 0,6.
3. Cartera a 30-sep-2027 igual o superior a 26.408: 2027-12-31, probabilidad 0,7.

## 13. Qué me haría cambiar de cubo

- **A Sí:** precio por debajo de 450,57, con Construction en el 5% o más al cierre de 2025/26 y una base para acotar las probabilidades.
- **A No:** una pérdida en Fehmarnbelt que revele un grado de avance agresivo; compras con deuda hacia 1,5 veces el EBITDA que rindan bajo el 12%; o el ROIC por debajo de r dos años.
- **A Demasiado difícil:** que el resultado pase a depender de pocos megaproyectos, o que la caja deje de cuadrar con el beneficio reconocido por avance.

## 14. Comparación con la etapa 1

El cubo es el mismo (Vigilar) y el precio de Sí casi el mismo (465 en v1, 450,57 en v2), pero por caminos distintos:

- El v1 estimaba un ponderado de unos 775 con la fórmula antigua.
- El v2 da 502,36: no extrapola el escalón, arranca en la media del ciclo, hace converger el ROIC a 0,10 y sube el MALO a 0,25.
- El v2 deja fuera los hechos del v1 que no están en mis entradas (los nueve meses al 4,5%).

Con el precio en 729 (682 en el v1), los dos dicen lo mismo: buen negocio sin foso y sin margen al precio actual.
