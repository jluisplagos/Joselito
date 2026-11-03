# NIKE, Inc. (NKE) · fase C · turno 1 (tras la vuelta a la fase B) · 2026-11-03

**Motor y escalera.** Motor A, r 0,09 (heredada; la r mínima es 0,102). El libro está recalculado con las palancas que la fase B revisó en la única vuelta C→B. La escalera de `precio.json` es una convención experimental (k = 3):

- precio actual: 39,12
- precio del escenario MALO: 10,22
- precio de Sí: 18,69 (P\*, sin tope del NORMAL)
- ponderado: 23,77
- zona: **caro**

La gramática sale con código 0. Reviso lo de A y B como si fuera de otro: “intensively consider any evidence tending to disconfirm any hypothesis of his” (PCA p.528; HIM).

## 1. Una sola historia

**Lo que calcula la hoja.** Los valores son 10,22 / 25,92 / 38,70, y el precio está por encima incluso del BUENO. El DCF inverso dice que a 39,12 el precio descuenta un crecimiento de ventas del ≈12,5 % anual en cinco años con el resto del NORMAL (C86). En diez años solo 2021 superó esa cifra, con el rebote de la pandemia. El precio de Sí descuenta −4,2 %. El resto de lecturas:

- **Peso del terminal:** 35 / 52 / 55 %; todo PASA.
- **Tornado:** manda el margen (±2 puntos → ±7,10 por acción). La tasa no es la palanca más influyente, y el tornado es información, no criterio.
- **Cuánto pagas por crecer:** el precio paga 2,4 veces lo que vale el crecimiento del NORMAL.
- **Veredicto de la hoja:** A6 dice DESCARTADA POR FILTRO PABRAI porque C13 = No. Mi cubo es Vigilar.

**Lo que corrigió la vuelta a la fase B.**

- **B15 (margen del MALO), 0,08 → 0,065.** Se ancla en FY2026 sin el reembolso IEEPA (≈6,2 %), con las reestructuraciones como gasto que se repite. El MALO ya no es mejor que el año publicado.
- **D15 (margen del BUENO), 0,135 → 0,13.** Usa 2021–2022 menos el arancel, sin el dato erróneo de 2024. El EBIT de 2024 en la Historia (7.089 en vez de 6.311) sigue mal. No es celda mía y lo dejo dicho para la fase 1.
- **B16 (S2C del MALO), 3,7 → 5,0.** Ahora el porqué tiene el signo correcto.

**Lo que queda.**

- **C18 (ROIC terminal del NORMAL), 0,12 → 0,15.** Ya no está en el umbral G4, pero se ancla en la media del sector (H18 = 15,3 %), que es un dato de otras empresas. Su rango con hechos de Nike es 0,09–0,18, y mueve el precio de Sí entre −4,7 % y +1,2 % sin cambiar la zona ni el cubo. No es un error de derivación (aritmética, perímetro o dato): es un fundamento débil y va a la lista de la sección 7.
- **C18 = D18 = 0,15.** El NORMAL y el BUENO tienen el mismo ROIC terminal. Lo resuelvo con palabras: D18 está bajo porque el ROIC propio está inflado por el gasto de marca, y el BUENO se separa por margen y S2C.
- **C14 frente a la escalera.** El precio de Sí (18,69) queda un 83 % por encima del MALO (10,22). No pagar el arreglo quiere decir no pagar las metas de la dirección, que no se cumplieron. El NORMAL (10,5 %) queda por debajo de la media de diez años de la propia empresa. “What is working poorly is usually either uncorrectable or 10 times harder to correct than you may think” (AIWTK p.12; HIM). Va a la tesis del turno 2.
- **Año 1 del modelo.** La Historia termina en FY2025, así que el año 1 es un FY2026 ya publicado, que arranca desde el margen de 2025. El efecto es pequeño.

## 2. Desviaciones

No queda ninguna sin justificar. La fase B justificó G4 (NORMAL y BUENO), G5 (BUENO) y G8 en los tres escenarios. No hay G16 (peso del NORMAL 52 %) ni G17 (C24 vacía). Repito G8 en `desviaciones_justificadas` con las cifras nuevas y con lo que se pierde en el año 11:

- **MALO (0,187; convención).** El ROIC terminal está en la tasa del motor. La marca deja de rendir sobre el capital nuevo, como Converse (extracto p. 40). “We don't think because it's never happened that it won't” (AIWTK p.55; HIM).
- **NORMAL (0,298).** En los años 1–10 se recupera precio sobre una red que ya existe (capex 430 frente a una amortización de 775, extracto p. 62). En el año 11 el foso se ha estrechado. “The question of how long your period in the sun will be is a very good one” (AIWTK p.127; HIM).
- **BUENO (0,538).** La mejora por precio es finita (GV; I1). La rentabilidad marginal de 0,688 supera el mejor ROIC de la década; el efecto en el precio de Sí es −0,3 %.

## 3. Palancas

No hay otra vuelta: `revisar_palancas = false`. Lo comprobé con una réplica del motor A, que reproduce exactamente B78:D78. Ninguna alternativa defendible de una palanca revisada cambia la zona o el cubo ni mueve el precio de Sí un 5 % o más:

| Palanca | Alternativa | Efecto en el precio de Sí |
|---|---|---|
| C18 | 0,09 / 0,18 | −4,7 % / +1,2 % |
| B15 | 0,06 / 0,07 | −3,6 % / +3,6 % |
| D15 | 0,125 / 0,14 | −1,3 % / +2,7 % |
| D18 | 0,12 / 0,18 | −1,3 % / +0,9 % |
| B16 | 3,7 | +0,2 % |
| D16 | 5,0 | −0,3 % |

Las probabilidades moverían más: 0,4/0,5/0,1 bajaría el precio de Sí un 13,5 %. Pero están fundamentadas por frecuencia observada, y no hay error de derivación en ellas. No hay límite del modelo.

## 4. Autocomprobación

- **Anclaje en la etapa 1:** la condición que el v1 puso a C14 se cumple; la anoto.
- **Anclaje en el precio:** el BUENO queda cerca del precio y de Simply Wall St, pero no sale de ellos. La vuelta a la fase B alejó mis valores de la cotización.
- **Consistencia:** ni el BUENO llega a comprar a 39,12, así que el cubo no depende de palancas acomodadas. C18 subió, pero su efecto es pequeño.
- **Historia bonita:** el +8 % del BUENO imita FY2023, que llevaba la reposición del canal. “carefully examine each past success, looking for accidental, non causative factors” (PCA pp.548–549; HIM).
- **Optimismo del BUENO:** cuatro de diez años llegaron al margen del BUENO, y el BUENO necesita menos capital del que Nike ha necesitado nunca.
- **Doble castigo:** el mismo hecho fija el nivel del MALO y su probabilidad, que son dos dimensiones; no está en la r ni en la quiebra (PA; E6).
- **Disponibilidad:** Converse y el reembolso IEEPA son lo más vívido. “An idea or a fact is not worth more merely because it is easily available to you” (PCA p.587; HIM).
- **Autoridad:** ninguna palanca descansa ya en la guía.
- **¿El MALO es malo?:** ahora sí, con el margen por debajo de cualquier año de la década.
- **Lo no numerable:** el control de Swoosh, el dividendo por encima del FCF, la reestructuración permanente, la concentración de fabricantes y la reclamación aduanera belga. Va a B102.

## 5. Cubo y conclusión provisionales

Sigo el orden de mando:

1. **Bloqueo:** no hay. El estado técnico INCOMPLETO solo se debe a las predicciones.
2. **Límite del modelo:** no hay.
3. **Descalificador:** no hay. La reestructuración se considera y la vigila C14.
4. **Dato ausente material:** no hay.
5. **Fundamento:** la conclusión no es favorable, así que no la limita.
6. **Zona:** caro. El precio está un 65 % por encima del ponderado, y el precio de Sí un 52 % por debajo del precio.

**Cubo provisional: Vigilar. Conclusión provisional: esperar**, con precio objetivo igual al precio de Sí (18,69). Me siento más cerca del error de pagar por la marca de antes: “Since it's so obvious that investing in great companies works, it gets horribly overdone” (PCA p.214; HIM).

## 6. Datos ausentes (S-19)

Reviso los 22 datos, uno a uno, en el JSON. `alguno_material = false`. Los que más pesan:

- **El importe de los aranceles.** B15 está acotado con FY2026 sin el reembolso; el importe cerraría B223.
- **La cuota y el orden de los competidores.** Condicionan la duración del foso y serían lo primero antes de comprar.
- **El texto del 10-K de FY2026.** Sus cifras están en celdas verificadas; falta poder citarlas con página.

Los demás no tocan ninguna celda de juicio con el motor A, no existen o los cubren datos que ya tengo.

## 7. Fundamento material (D10)

Hay una hipótesis de fundamento débil: **Palancas!C18 = 0,15**, anclada en la media del sector. Su rango es 0,09–0,18, con cada límite atado a un hecho de Nike:

- **Techo:** el ROIC publicado de FY2026 (18,7 %) en el fondo del ciclo.
- **Suelo:** la caída de C24 y Converse.

No uso como límite ni la media del sector ni el umbral C56 + 0,03. El resto de las hipótesis materiales tiene hechos propios en su apoyo:

- probabilidades por frecuencia observada;
- quiebra vacía con caja neta;
- C76 sin doble cuenta;
- motor, base del margen, caso especial y narrativas con páginas;
- las tres palancas corregidas en la vuelta.

Como la conclusión no es favorable, `resultado = no_procede` y no hago la comprobación conjunta. Como orientación, sin que cambie el estado: los extremos adversos de C18, B15, D15 y D18 a la vez dan un precio de Sí de ≈16,6.

## 8. Qué condiciona y qué lo resolvería

- **De la lista:** C18. Lo resolvería el ROIC publicado de FY2027–FY2028 con la definición de C24.
- **A mi juicio, entre las hipótesis fundamentadas:** cuánto margen recupera Nike sin el arancel (B15 y C15). Lo resolverían el 10-K de FY2027, con el margen sin partidas únicas y el arancel separado del reembolso, y la pregunta a Relación con Inversores sobre el coste de los aranceles y qué parte se repercute.
