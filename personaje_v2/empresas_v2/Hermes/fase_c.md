# Hermès International SCA (RMS) · fase C · turno 1 · 2026-11-04

Reviso la fase A y la fase B como si fueran de otro: «consider any evidence tending to disconfirm any hypothesis» (PCA p.528; HIM). Cuando escribo «estimación mía», la cifra sale de una réplica aproximada del motor A hecha fuera de la hoja. Reproduce B78:D78 con menos de un 1 % de error y solo la uso para medir efectos y materialidad. La escalera oficial es la de `precio.json`, y no la discuto.

## 1. Una sola historia

**Lo que calcula la hoja.** MALO 542,70 €, NORMAL 842,11 €, BUENO 1.144,94 €, ponderado 842,80 € (B78:D78, C83). Precio 1.312,5 € (C37). La escalera de `precio.json` da precio de Sí 757,05 € (P\*, sin tope del NORMAL), zona **caro**, con el precio un 42 % por encima del precio de Sí y un 59 % por encima del MALO. La regla antigua (C156) da 542,70 €.

- **Semáforos.** El margen sale en REVISAR en los tres escenarios por el Q3 del sector (0,086), y está justificado en la fase B. El ROIC terminal del BUENO sale en REVISAR («muy por encima de r para siempre»), justificado por G4. Peso del terminal 0,47 / 0,55 / 0,61, PASA (G16 no salta). Cuota implícita no calculable, porque C24 está vacía (G17 no aplica). La r (0,09) queda por debajo de la r mínima (0,0987): se informa y no la toco.
- **Salto del año 11.** 0,32 / 0,53 / 0,71. El terminal no está en la tasa del motor (0,12 / 0,16 / 0,33), así que el salto es una hipótesis mía sobre la ventaja. La justifico en el punto 2.
- **DCF inverso.** El precio descuenta un 17,2 % anual de ventas en los años 1–5 con el resto de mi NORMAL (C86). El precio de Sí descuenta un 5,7 %. Mi NORMAL es 8 % y la Historia da 9,8 % en 2016–2019 y 13,3 % en diez años. El precio está incluso por encima del BUENO (D86). Pagas 2,5 veces lo que vale el crecimiento de mi NORMAL.
- **Tornado** (información, no criterio). La tasa de descuento mueve ±146 € y el crecimiento ±84 €; el resto, menos de 40 €. El valor depende sobre todo de la r exigida, que es heredada.

**Incoherencias que encuentro** (todas en `una_sola_historia.incoherencias`):

1. **El S2C del NORMAL contradice la historia de la fase A.** Con 2,4, la rentabilidad marginal de los años 1–10 es 0,69, por encima del ROIC de 2025 (0,489): el NORMAL haría subir el ROIC. La fase A cuenta lo contrario. Entre 2022 y 2025 el capital invertido pasó de 5.149 a 8.947 M€ y el ROIC bajó de 0,655 a 0,489. La rentabilidad incremental fue de 0,26–0,35: el NOPAT creció entre 1.000 y 1.319 M€, según el tipo impositivo, sobre 3.798 M€ más de capital. Una parte es de perímetro. La serie de reinversión de la hoja resta toda la amortización, incluida la de derechos de uso (351 M€ en 2025 [AR_2025, PDF p. 368]), y no suma los pagos de arrendamientos (277, 305 y 332 M€ en 2023–2025). Con esos pagos, los S2C serían 1,3 / 1,6 / 2,3 y la marginal del NORMAL 0,46, en línea con el ROIC de hoy. Efecto en el precio de Sí: −1,6 % (−3,5 % si tomo todo el aumento del capital invertido, que además incluye inversiones financieras). La zona sigue en caro y el cubo en Vigilar. Por la regla v2.1 no vuelvo a la fase B. Lo dejo escrito en `celdas_corregidas` y lo contará la tesis.
2. **C76 = 6.000 M€** coincide con la etapa 1, y su derivación resta también el rendimiento de la caja operativa que no se suma. Bien hecha daría 6.600–6.800 M€: +0,9 % en el precio de Sí, sin cambio de zona.
3. **El FCF del año 1 del motor** (4.245,6 M€ en el NORMAL) está un 13 % por encima del de 2025 (3.749 M€) con solo un 8 % de crecimiento. Lo explican el tipo medio de cinco años de la hoja (0,295, frente a 0,334 en 2025 con la contribución francesa) y el perímetro anterior. El tipo es una celda de datos: no la toco. Si la contribución fuera permanente, el precio de Sí bajaría un 5 %.
4. **B101, B102 y C104 todavía traen el texto de la etapa 1:** «A 1.280 €», precio de Sí de unos 520 €, datos del primer semestre de 2026 que no están en mis entradas y un porcentaje de posición en C104, que choca con D16. Los reescribe el turno 2.
5. **El veredicto A6** («DESCARTADA POR FILTRO PABRAI») y mi cubo difieren, como ya explicó la fase A.

Ninguna de estas incoherencias cambia la historia: un negocio excepcional, con un ROIC que baja porque el capital crece más que el beneficio, a un precio que pide más que mi escenario bueno. Las 52 celdas y la hoja cuentan eso.

## 2. Desviaciones pendientes (G8)

`gramatica.md` deja pendiente solo G8, en los tres escenarios. G16 y G17 no saltan. Justifico los tres saltos con el mecanismo y no cambio la clase de ninguna palanca.

- **MALO, 0,44 → 0,12.** Lo que se pierde en el año 11 es vender cada unidad nueva al precio de la escasez. En el MALO la marca gastó deseabilidad subiendo precios contra las divisas, y la capacidad comprometida hasta 2030 [AR_2025, PDF p. 29] no se llena. El capital nuevo rinde poco más que r. Pesa poco en el valor: el terminal reinvierte 0,015 ÷ 0,12 del beneficio.
- **NORMAL, 0,69 → 0,16.** La escasez, un taller al año [AR_2025, PDF p. 43], sostiene la rentabilidad de lo nuevo durante diez años. Después, el crecimiento que quede (g 0,025) sale de capital nuevo en un negocio maduro, y supongo que rinde la media de su sector (H18 = 0,161). Lo sostiene que la rentabilidad incremental ya ha caído a 0,26–0,35. Sin ningún salto, el precio de Sí subiría alrededor de un 6 %: la hipótesis es prudente. «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM).
- **BUENO, 1,04 → 0,33.** El 1,04 sale de 2024, el año en que se llenó capacidad ya pagada, y no vale para siempre. El foso conserva a perpetuidad su peor año (2020, 0,332). Lo que se pierde es el efecto de llenar capacidad, no la marca.

## 3. ¿Hay que mover palancas?

No. Las palancas mal derivadas que encuentro son el perímetro de arrendamientos de B16:D16 y la resta de C76. Las he calculado: corregirlas no cambia ni el cubo ni la zona, y mueven el precio de Sí un −1,6 % y un +0,9 % (−0,8 % juntas; −3,5 % en el perímetro más duro). Quedan en `celdas_corregidas` con despues = antes. No veo ninguna celda de la fase A mal puesta. Reviso C62 y sigue el motor A: el perímetro se arregla en el S2C, no cambiando de motor. `revisar_palancas = false`.

## 4. Autocomprobación

Las diez entradas están en el JSON. Lo que encontré:

- **Anclaje en la etapa 1.** C76, g y probabilidades son idénticos a la etapa 1. C76 está mal derivado (+0,9 %), y g y probabilidades pasan a la lista de hipótesis sin fundamento.
- **Anclaje en el precio o en la fuente externa.** Mi ponderado está a un 1,6 % del Simply Wall St (856,32 €). Ninguna palanca lo usa. Lo anoto como coincidencia que no puedo excluir del todo.
- **Consistencia y compromiso.** El cubo Vigilar resiste a todas las palancas en el extremo favorable de sus rangos a la vez: ponderado de unos 1.067 € y precio de Sí de unos 993 €, frente a un precio de 1.312,5 €.
- **Historia bonita.** El margen del NORMAL es el escalón de 2021. El escalón aguantó en 2025 con Asia floja, y eso es mérito de la empresa. El BUENO se apoya en 2024, que incluye la consolidación de Emiratos.
- **Optimismo del BUENO.** El BUENO pide una marginal tres veces la incremental observada y un ROIC terminal de 0,33. No necesita más mercado del que existe. D18 va a la lista de hipótesis sin fundamento.
- **Doble castigo.** No lo hay: el riesgo de Asia y divisas está solo en el MALO (PA, E6).
- **Disponibilidad.** Los talleres con nombre pesaron más que la caída del ROIC en la Historia, y eso está detrás de la incoherencia 1.
- **Autoridad.** El «taller al año» es un plan contrastado con hechos, no una cifra copiada. La guía de capex se incumplió.
- **¿El MALO es de verdad malo?** Es un MALO de márgenes, no una recesión. Un MALO más duro bajaría el precio de Sí un 6 %. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM).
- **Lo no numerable.** La comandita, la escasez como política o como límite, la deseabilidad entre generaciones y la caída de la cotización en 2026, que no sé explicar.

## 5. Cubo y conclusión provisionales

Sigo el orden de mando. Bloqueo: no hay (gramática sin errores en las celdas de A y B; G13 espera las predicciones del turno 2). Límite del modelo: no hay. Descalificador: ninguno (fase A). Dato ausente material: ninguno (punto 6). Fundamento material: con conclusión no favorable a comprar, no limita (punto 7). Zona: caro.

**Cubo provisional Vigilar · conclusión provisional esperar**, con precio objetivo = precio de Sí de `precio.json` (757,05 €). El precio objetivo es **provisional** porque lo condicionan Palancas!C18 y B68:D68, que no tienen base para acotarse. «I know it's wonderful, but is it wonderful enough to justify that big a premium?» (DR p.308; HIM). Estoy más cerca del error de pagar cualquier cosa por calidad. La escalera es una convención del ejercicio (k = 3), no una medida del riesgo.

## 6. Datos ausentes (S-19)

Reviso los 20 datos de `datos_ausentes.json`, uno a uno, en el JSON. Ninguno es material para esperar con precio objetivo: `alguno_material = false`. Los dos que más se acercan:

- **Informe semestral a 30-jun-2026.** Diría si el MALO ya está en curso. Si lo estuviera, p(MALO) subiría a 0,3 y el precio de Sí bajaría alrededor de un 8 %, pero la acción seguiría siendo esperar, porque el precio está por encima del BUENO. Un semestre no cambia escenarios construidos con diez años: «we have never given a damn whether any quarter's earnings were up or down» (PCA p.88; HIM). Lo pido en B223.
- **Precio frente a volumen.** Es la variable central del foso. Pero el NORMAL está acotado por hechos que no dependen de ese reparto (9,8 % en 2016–2019, 8,9 % cst en 2025), y lo que el reparto cambiaría, la duración del foso, ya está en la lista del punto 7.

## 7. Fundamento material (D10)

Las clases de la fase B son todas fundamentada o convención, con hechos en su apoyo, y las narrativas de A citan hechos específicos. La lista mecánica saldría vacía. Por juicio, cuatro hipótesis no tienen fundamento suficiente:

1. **B69:D69, probabilidades 0,2 / 0,6 / 0,2** (convención, copiadas). Hay base por frecuencias observadas. MALO entre 0,1 (solo 2020 cumplió a la vez ventas bajas y margen del MALO) y 0,4 (4 de 10 años con margen ≤ 0,35). BUENO entre 0,1 (solo 2023) y 0,3 (2019, 2023 y 2024). En ese rango el precio de Sí va de unos 660 € a 842 €.
2. **Palancas!C18, ROIC terminal del NORMAL 0,16.** Sale de la media del sector. Por arriba lo acota la rentabilidad incremental de 2022–2025 (0,26–0,35); por abajo ningún hecho, porque Hermès nunca ganó menos de 0,33. Sin base.
3. **Palancas!D18, ROIC terminal del BUENO 0,33.** Sale de un solo año. Hay base: entre 0,26 (la incremental de 2022–2025) y 0,49 (el ROIC de 2025).
4. **B68:D68, g 0,015 / 0,025 / 0,03** (convención, copiadas). El techo lo da el mercado de 2017–2019 (3,5 % anual [AR_2019, PDF p. 13]); no hay suelo. Sin base.

Con la conclusión esperar, `resultado = no_procede` y no hago la comprobación conjunta (`procede = false`, `sobrevive = null`). Con todas las hipótesis a la vez en su extremo favorable, el precio sigue en caro; en el desfavorable, el precio de Sí baja, pero la acción no cambia.

## 8. La hipótesis que más condiciona

**B69:D69.** Es la que más mueve el precio objetivo (de unos 660 € a 842 €), aunque la conclusión no cambia. De las que no tienen base, la que deja provisional el precio objetivo es C18.

**Qué lo resolvería.** El informe semestral a 30-jun-2026: ventas a tipo constante de Asia-Pacífico sin Japón y margen operativo recurrente del semestre. Con Asia por debajo del 3 % y margen por debajo del 39 %, p(MALO) pasa a 0,3. Para C18, el coste y las ventas del primer año completo de los talleres de Riom y L'Isle-d'Espagnac, que hay que pedir a Relación con Inversores.
