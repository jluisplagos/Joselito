# RATIONAL AG (RAA) · fase C · turnos 1 y 2 · motor A · 2026-11-03

Reviso A y B como si fueran de otro: «intensively consider any evidence tending to disconfirm any hypothesis of his» (PCA p.528; HIM).

## 1. Una sola historia

Lo que calcula la hoja con mis 52 celdas:

- **Valores por acción:** MALO 241,38 · NORMAL 376,21 · BUENO 505,29. Ponderado (C83) 375,06.
- **Escalera (precio.json):** precio de Sí 336,87, sin tope del NORMAL. Zona **caro**: 630 € está por encima del ponderado. Faltan un 46,5 % hasta el precio de Sí y un 61,7 % hasta el precio del MALO. La regla antigua (C156) da 241,38.
- **DCF inverso:** con mis demás palancas del NORMAL, 630 € descuentan un crecimiento de ventas del 16,5 % anual durante cinco años (C86). Es más que mi BUENO (10 %), más que el +11,2 % de 2016–2019 y más que cualquier quinquenio de la Historia que no arranque en 2020. El precio de Sí descuenta un 3,7 %.
- **Lo que pago por crecer:** el valor sin crecimiento es 254,9 €. A 630 € pago 375 € por crecer, 3,1 veces lo que vale el crecimiento en mi NORMAL (121 €).
- **Peso del terminal:** 0,45 / 0,54 / 0,59. Pasa: el valor no vive del año 30.
- **Salto del año 11:** 0,224 / 0,516 / 0,586 (punto 2).
- **Tornado** (información, no criterio): manda la tasa de descuento (±65,5 € por punto en el NORMAL). Le siguen el crecimiento (±38,5 €), el margen (±26,8 €), g (±13,1 €), el ROIC LP (±12,7 €) y el S2C (±1,2 €). El valor depende sobre todo de la r exigida, que es heredada.
- **Estado del libro:** el técnico es INCOMPLETO solo porque faltan las tres predicciones, que van al turno 2. El valor no está bloqueado. A6 dice «DESCARTADA POR FILTRO PABRAI» por C13 = No; mi cubo es Vigilar porque falla el precio, no el negocio.

La historia es una: un negocio de calidad, sin deuda, que crece a un dígito medio, a un precio que pide más que mi escenario bueno. Las incoherencias que encuentro son menores y ninguna cambia la zona ni la conclusión:

1. **Cita de C55.** La fase A escribe «ROIC medio 5 años 54 % (C55)» en C14 y C18. C55 vale 0,407 con I+D capitalizada; el 54 % es la serie sin I+D. Con 0,407 frente a 0,118 del sector, C18 = Sí y C14 = Compounder se sostienen. Lo registro sin cambiar valor.
2. **Crecimiento NORMAL (`Palancas!C14` = 0,06).** El argumento mete en el volumen repetible el +12 % de 2022, que fue recuperación tras 2020 (extracto AR22 p. 21). Pero la misma fase B rechaza C46 por medir desde la base de 2020. Sin 2022, el volumen es ≈ 3 % anual en 2023–2025 y ≈ 4 % en 2019–2025 (ventas ×1,49 con ≈ 18 puntos de precio; extracto AR22 p. 13; AR23 p. 14). Las ventas de 2024–2025 (+6,0 % y +5,5 %, Historia fila 28) siguen sosteniendo el 0,06, pero en el extremo favorable de 0,05–0,06. Un punto menos baja el precio de Sí ≈ 8 €.
3. **S2C del BUENO (`Palancas!D16` = 3,9).** El periodo que el BUENO copia (2017–2019) dio ≈ 2,1. Pasa a la lista D10.
4. **Base de capital.** La rentabilidad marginal de los años 1–10 sale de un S2C sobre capital sin I+D capitalizada. El ROIC terminal se calibró con la serie con I+D: peor año 0,225, frente a 0,278 sin I+D. Parte del salto es de medida, del lado prudente.
5. **China en el MALO.** B66 pesa mucho la caída de China (−29 %). Asia Norte es el 8 % de las ventas (extracto AR25 p. 11), y la empresa atribuye parte de la caída a un pedido grande del año anterior (extracto AR25 p. 15). La cifra del MALO sale del volumen de 2023–2024.

No pido revisar palancas. Ninguna incoherencia exige mover una celda para que la historia cuadre. La más grande (punto 2) cambia el precio de Sí en unos 8 € y deja intacta la conclusión.

## 2. Desviaciones pendientes

La gramática tras el recálculo solo deja pendiente G8, en los tres escenarios. G16 no salta (peso 0,54 < 0,75). G17 no se evalúa (sin C24). G4 y G5 ya están justificadas en la fase B.

El salto del año 11 no es la convención del ROIC igual a la tasa: mis tres ROIC terminales están por encima de 0,09. Es mi hipótesis sobre qué ventaja se pierde, y la escribo por escenario:

- **MALO (0,34 → 0,12).** Lo que se pierde es la ventaja de precio. La restauración ya busca proveedores más baratos (extracto AR25 p. 14) y hay unos 100 fabricantes sin nombre (extracto AR25 p. 11). El capital nuevo pasa a rendir como la maquinaria media. La cota alta la pone la empresa: en 2020, con ventas −23 %, rindió 0,225 (Historia, serie roic_con_id).
- **NORMAL (0,70 → 0,18).** En los años 1–10, cada euro nuevo rinde lo que rindió en la década: el NOPAT sube ≈ 120 mm con 178,7 mm de reinversión neta, ≈ 0,67. En el año 11, lo nuevo ya no convierte cocinas en un nicho donde tiene la mitad del mercado. La penetración que estima la empresa está quieta en ~25 % desde 2019 (extracto AR19 p. 3; AR25 p. 4). Lo nuevo va a reposición, a clientes que compran por precio (Suzhou, extracto AR25 p. 13) y a más I+D (del 4,7 % al 6,0 % de las ventas, Historia fila id). La erosión ya se ve: el ROCE publicado pasa del 41–45 % al 37–39 % (extracto AR25 p. 187). El retorno converge hacia el sector salvo ventaja duradera (CV p. 11; E2), y el marginal suele quedar por debajo del medio (MR p. 51; E2).
- **BUENO (0,81 → 0,22).** Lo que se pierde es el recorrido. Las ventas del año 10 son 2,1 veces las de 2025, con una cuota ya del ~50 %. Lo que queda por ganar está donde gana menos: Asia Norte da un margen EBIT del 17,8 %, frente al 26–28 % de EMEA y Norteamérica (cálculo mío, extracto AR25 p. 141). «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM).

Sin salto en el NORMAL (ROIC terminal 0,70), el valor subiría ≈ 23 €, hasta ≈ 399 €. El salto no decide nada frente a 630 €. Entradas en `desviaciones_justificadas` con hechos y clase fundamentada; el turno 2 lo cuenta en la tesis.

## 3. Palancas

`revisar_palancas = false`. No cambio ninguna celda. En `celdas_corregidas` quedan, con `despues = antes` y su motivo: C18 y C14 (la cita de C55), `Palancas!C14` (extremo favorable del rango) y `Palancas!D16` (S2C generoso).

## 4. Autocomprobación

Las diez tendencias están en el JSON. Lo que cambia algo:

- **Historia bonita.** El viento de sustitución lo aprovechan también unos 100 fabricantes. El 6,9 % anual de 2019–2025 lleva dentro ≈ 18 puntos de precio. De ahí sale la incoherencia 2.
- **Optimismo del BUENO.** Necesita 10 % anual sobre una base doble, margen en el máximo y un S2C que no tuvo cuando creció así. «most big businesses eventually fall into mediocrity or worse» (AIWTK p.140; HIM). `D16` va a la lista D10.
- **Autoridad.** El NORMAL cae dentro de la guía y en su parte alta. La guía de volumen falló dos de cuatro años (extracto AR23 p. 22; AR24 p. 12): «A projection prepared by anybody who stands to earn a commission or an executive trying to justify a particular course of action will frequently be a lie» (TCI p.60; HIM). Las cifras tienen apoyo propio, pero coincidir con la guía no prueba nada.
- **¿El MALO es malo?** Sí frente a la Historia: 241 €, por debajo del valor sin crecimiento. No recoge lo peor plausible, una pérdida de cuota ante un competidor con nombre. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM).

**Anclaje en el precio o en la fuente externa:** ninguno. Hasta mi BUENO queda un 20 % por debajo de 630 € y muy lejos de los 734 € de C38. «For a security to be mispriced, someone else must be a damn fool» (TCI p.17; HIM): quien paga 630 € supone ≈ 16,5 % de crecimiento o una r mucho menor.

**Disponibilidad:** China pesa el 8 % de las ventas. «extra vivid evidence, being so memorable and thus more available in cognition, should often consciously be underweighted» (PCA p.587; HIM).

**Doble castigo:** no hay (PA p. 9; E6). El MALO no baja g ni sube la probabilidad, y el euro resta crecimiento y margen porque son dos efectos reales.

## 5. Cubo y conclusión provisionales

En orden de mando:

1. Sin bloqueo: 0 errores, 0 límites.
2. Sin límite del modelo: motor A coherente.
3. Sin descalificador: los nueve revisados en la fase A siguen sin aplicar, y nada del recálculo los reabre.
4. Sin dato ausente material (punto 6).
5. Hay hipótesis sin base (punto 7). No limitan una conclusión no favorable; marcan el precio objetivo como provisional.
6. Zona **caro**.

**Cubo provisional Vigilar · conclusión provisional `esperar`.** Precio objetivo: precio de Sí 336,87, provisional por `Palancas!C18`. El error que tengo más cerca sigue siendo pagar por calidad: «Since it's so obvious that investing in great companies works, it gets horribly overdone» (PCA p.214; HIM). El opuesto también existe: «We left a lot of money on the table through early fretting» (TCI p.79; HIM). Un precio de Sí de 337 € no es regatear: es el NORMAL con un descuento de un 10 %.

## 6. Datos ausentes (S-19)

Reviso los catorce, uno por uno, en el JSON. Ninguno es material para esperar con precio objetivo. El que más pesa es el nombre de los competidores: «I think it's important to know which competitor is most likely to do you in» (AIWTK p.131; HIM). Aun así no impide fijar el precio de Sí, por tres razones:

- el resultado competitivo de diez años está medido: margen de 26–27 % fuera de 2020–2022 y ROIC con I+D nunca por debajo de 0,225;
- la cuota declarada se ha mantenido estable;
- el MALO ya lleva el ROIC terminal a la media del sector.

Lo que hace esa carencia es dejar sin base el nivel del ROIC terminal (punto 7). El margen por segmento no falta en sustancia: lo calculo con los importes (extracto AR25 p. 141). `alguno_material = false`.

## 7. Fundamento material (D10)

Ninguna palanca es «sin juicio propio» ni «técnico». Todas las Observaciones citan hechos y las narrativas tienen mecanismo y hechos. Probabilidades, g, C76, C62, C8 y C6 tienen argumento y hechos propios. Aun así, tres hipótesis no se sostienen en hechos de la empresa:

- **`Palancas!C18` (ROIC LP del NORMAL, 0,18).** Es un punto entre el peor año propio (0,225) y la media del sector. Techo con base: 0,225. Suelo sin base, porque la tasa del motor es convención y el sector son otras empresas. `hay_base = false`.
- **`Palancas!B18` (ROIC LP del MALO, 0,12).** Es la media del sector, y los hechos propios apuntan más arriba. `hay_base = false`.
- **`Palancas!D16` (S2C del BUENO, 3,9).** Rango 2,1–4,2. El suelo es lo que necesitó en 2017–2019 al crecer a ese ritmo (Historia). El techo es el circulante del 22 % de las ventas (extracto AR25 p. 187) más el capex de 2026 frente a la amortización (extracto AR25 p. 18; Historia fila da). `hay_base = true`.

La conclusión provisional no es favorable: `resultado = no_procede`. No hago la comprobación conjunta: dos hipótesis no tienen rango defendible. Con `esperar` y hipótesis sin base, el precio objetivo va provisional en C104, condicionado por `Palancas!C18`.

## 8. Lo que más condiciona y lo que lo resolvería

**Lo que más condiciona: `Palancas!C18`,** cuánto exceso de retorno conserva el capital nuevo después del año 10. No mueve la conclusión, porque a 630 € el precio supera hasta el BUENO. Sí mueve el precio objetivo: ±5 puntos de ROIC LP son ±12,7 € en el NORMAL y ≈ ±5 € en el precio de Sí.

**Lo que lo resolvería:** preguntas a Relación con Inversores y las notas de segmentos de 2026.

1. Margen y capital de la posventa frente a los aparatos, y tamaño y vida media de la base instalada.
2. Los dos o tres competidores principales en combi, con su cuota y su margen.
3. El ROCE de 2026–2027 sin el reembolso arancelario.

## 9. Conclusión

No existe `comprobacion_conjunta.json`, porque la comprobación no procedía. `sobrevive` queda en `null` y `resultado` en `no_procede`.

**Estado `concluido` (provisional hasta la auditoría) · cubo Vigilar · acción `esperar` · precio objetivo 336,87.** El precio objetivo es el precio de Sí de precio.json, y es provisional porque lo condiciona `Palancas!C18`.

C104: «Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 336.87 (provisional…) · zona caro · precio de Sí ≤ 336.87 · precio esc. MALO 241.38 · ponderado 375.06 · fundamento pendiente de investigación (…)». No lleva ningún porcentaje: el tamaño de la posición es de José Luis.

Otras celdas de la conclusión:
- **C93 = Sí.** g = 0,025 queda bajo rf. Reinvierte ≈ 14 % del NOPAT con ROIC 0,18. El terminal pesa 0,54.
- **C103 = Sí.** «Nunca vender» es propiedad del negocio: posventa del 31 % (extracto AR25 p. 10), sin deuda y diez años de margen estable. No dice nada de comprar hoy.
- **Confianza global: media.**

## 10. Tesis y tesis inversa

**Tesis (B101).** Rational vende hornos combinados y el iVario, y cobra un 31 % de sus ventas en posventa (extracto AR25 p. 10). En diez años duplicó las ventas sin deuda, sin adquisiciones y sin acciones nuevas, con un margen EBIT del 26–27 % fuera de 2020–2022 (Historia fila 29). Con mis escenarios vale 241, 376 o 505 € por acción, y el precio de Sí es 336,87 €.

En el año 11 supongo que el capital nuevo pierde parte de su ventaja:
- **NORMAL:** rinde 0,18 en vez de ≈ 0,70. Con la penetración quieta en ~25 % y una cuota del ~50 %, lo que queda es reposición, clientes que compran por precio y más I+D (extracto AR19 p. 3; AR25 p. 4).
- **MALO:** baja a la media de la maquinaria, 0,12.
- **BUENO:** baja a su peor año, 0,22.

A 630 € el precio descuenta un 16,5 % anual de crecimiento durante cinco años (C86), más que mi BUENO.

**Tesis inversa (B102).** Es el No, defendido con hechos:

1. **Volumen.** Sin las subidas de precio, fue 0 % en 2023 y +3 % en 2024, por debajo de la guía (extracto AR23 p. 22; AR24 p. 12). Fue ≈ 4 % anual en 2019–2025, y la penetración no se mueve desde 2019 (extracto AR19 p. 3; AR25 p. 4).
2. **Precio con techo.** En 2025 bajó los precios de cuidado (extracto AR24 p. 12), y la restauración busca proveedores más baratos (extracto AR25 p. 14).
3. **Competidor sin nombre.** Hay unos 100 fabricantes que el informe no nombra (extracto AR25 p. 11). El ROCE bajó del 41–45 % al 37–39 % (extracto AR25 p. 187). Asia Norte gana un 17,8 % de margen frente al 26–28 % de EMEA y Norteamérica (extracto AR25 p. 141).
4. **Aranceles y euro.** La empresa fabrica solo en Europa (extracto AR25 p. 20; AR25 p. 22; AR25 p. 16).
5. **Gobierno y caja.** El derecho de W. Kurtz a nombrar consejeros, el Vorstand sin participación encontrada (C96) y una caja del 46 % del activo (extracto AR25 p. 17).
6. **Precio.** 28 veces el beneficio. Ni el BUENO llega a 630 €, y el MALO no es un suelo.

«I'm not entitled to have an opinion unless I can state the arguments against my position better than the people who are in opposition» (PCA pp.467–468; HIM).

## 11. Predicciones (fecha 2028-04-30, informe anual 2027)

Cada probabilidad es la de que se cumpla la predicción dado el NORMAL:

1. **Ventas de 2027 ≥ 1.390 mm** (≈ +5 % anual desde 1.259,6). Probabilidad 0,65. Pone a prueba el punto débil del NORMAL.
2. **Margen EBIT de 2027 entre el 24,5 % y el 27,5 %.** Probabilidad 0,7. Separa el NORMAL del MALO.
3. **ROCE publicado de 2027 ≥ 33 %, sin deuda bancaria.** Probabilidad 0,7. Pone a prueba la deriva del foso que condiciona C18 (B222).

Ninguna habla del precio ni de macro, y ninguna copia la guía.

## 12. Qué me haría cambiar de cubo

- **A Sí:** un precio ≤ 336,87 con la tesis intacta. Antes tendría que acotar `Palancas!C18` con los datos de B223; sin eso, una compra quedaría pendiente de investigación.
- **A No:** cualquiera de estas tres cosas:
  - un competidor con nombre que deje el margen bruto bajo el 55 % dos años;
  - un ROCE por debajo del 30 % dos años sin choque externo;
  - la caja usada fuera del núcleo.
- **A Demasiado difícil:** que el valor pase a depender de aranceles o del euro, o que el software cambie la ventaja a un ritmo que no pueda juzgar.

«Missing out on some opportunity never bothers us» (TCI p.57; HIM).

## 13. Comparación con la etapa 1

El cubo es el mismo, Vigilar, por la misma razón: el negocio es bueno y el precio no deja margen.

El precio de Sí sube de ≈ 288 a 336,87 por la regla, no por los valores:
- **La regla.** La etapa 1 usaba mín(MALO, 0,75 × ponderado). La V6.3 usa la escalera k = 3 sobre tres valores que calcula la hoja.
- **Los valores bajan.** MALO de ≈ 288 a 241, NORMAL de ≈ 413 a 376 y BUENO de ≈ 583 a 505. El MALO lleva un margen de 0,225 y un ROIC de 0,12 para siempre, y el foso se erosiona en el año 11.
- **La regla antigua sobre los valores nuevos** (C156) daría 241,38, por debajo del 288 de la etapa 1.

El precio pasó de 566,5 a 630 €: la etapa 1 veía la cotización en su BUENO, y hoy está un 25 % por encima de él. La tesis inversa conserva lo verificable. Quito dos datos que el extracto v6.3 no recoge: el margen del primer semestre de 2026 sin reembolso y el voto de remuneración.
