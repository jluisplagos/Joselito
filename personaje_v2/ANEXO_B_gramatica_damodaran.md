# ANEXO B · Referencias mecánicas, principios de Damodaran y comprobaciones

Versión 0.2.1 (2-nov-2026). Tres cosas distintas, que la versión 0.1 mezclaba:

1. **Las referencias mecánicas** (§B.2): cifras reproducibles, calculadas por script a partir de la historia de la empresa y de los cuartiles de su sector, desde las que se mide la desviación de Munger. Son **convención del ejercicio**, versionada (`config_v2.json` → `version_referencias_mecanicas`). No son una estimación de Damodaran de la empresa y no se le atribuyen.
2. **Los principios de Damodaran** (§B.0, categorías [I] y [E]): identidades con sus condiciones y criterios económicos con su documento y página. Son la gramática de D4, junto con las condiciones necesarias del modelo.
3. **Las comprobaciones** (§B.3): cada una con su categoría (error · límite del modelo · desviación económica · aviso), los motores a los que aplica y su consecuencia. Un error nunca se aprueba con una explicación (D17).

## B.0 Clasificación de las reglas teóricas

Toda regla de este anexo lleva una etiqueta: **[I]** identidad matemática o contable (verdadera por definición, con sus condiciones), **[N]** condición necesaria para que los motores de la V6.3 sean válidos, **[E]** criterio económico u orientación de valoración (de Damodaran, con documento; no es una ley), **[C]** convención de la plantilla o del ejercicio. Las páginas de los documentos de Damodaran se fijan en la pieza 3 (`trazabilidad_damodaran.md`); hasta entonces se cita el documento.

### [I] Identidades, con sus condiciones

- **I1 · Crecimiento fundamental.** El crecimiento del beneficio operativo que financia la empresa con capital nuevo es `g = tasa de reinversión × rentabilidad del capital nuevo` (tasa de reinversión = reinversión neta ÷ NOPAT). Con la rentabilidad medida como NOPAT adicional ÷ reinversión neta la igualdad es una definición; la forma útil de Damodaran usa el **ROIC (medio) aplicado al capital nuevo** y supone que la rentabilidad del capital ya invertido **no cambia**: solo con esa condición es una identidad. Si cambia (mejora de márgenes o de rotación del capital), aparece un segundo término, el **crecimiento por eficiencia**: `g ≈ reinversión × ROIC_nuevo + (ROIC_t − ROIC_{t−1}) ÷ ROIC_{t−1}`. Ese segundo término es finito: la eficiencia no puede mejorar indefinidamente, así que el crecimiento por eficiencia se agota (GV). En la V6.3 los dos efectos están separados por construcción: la palanca de **margen objetivo** recoge la eficiencia (el margen converge en cinco años) y la palanca de **crecimiento de ventas** recoge el volumen; el motor carga la reinversión de las ventas nuevas vía S2C. De ahí sale otra identidad del propio motor: la rentabilidad marginal implícita de los años 1–10 es `S2C × margen × (1 − t)` (`Diagnóstico V6!C176`).
- **I2 · Reinversión en estado estable.** Si en el estado estable el crecimiento se financia enteramente con reinversión a una rentabilidad del capital constante, la tasa de reinversión es `g ÷ ROIC` (CV pp. 12–15 y 17: fórmula y ejemplos, verificados en el PDF). Es la que aplica el flujo del año 11 de la V6.3 (factor `1 − g ÷ ROIC`). Condición: ROIC constante y **mayor que g**; si ROIC ≤ g la reinversión absorbe todo el flujo (de ahí N2).
- **I3 · Valor terminal de Gordon.** `VT = flujo₁₁ ÷ (r − g)` es la suma de una progresión geométrica y solo converge si `r > g` (de ahí N1).
- **I4 · Aritmética de la escalera** (Anexo C): el precio de Sí, el margen y la asimetría son definiciones sobre los valores y probabilidades introducidos; no miden riesgo (D11).

### [N] Condiciones necesarias para que los motores de la V6.3 sean válidos

| Id | Condición | Motores | Regla de la hoja |
|---|---|---|---|
| N1 | g para siempre < tasa de descuento del motor (`Análisis!C56` en A y C; `Diagnóstico V6!C15` en B), en los tres escenarios | A, B, C | `Motor` V15 |
| N2 | ROIC (ROE en C) a largo plazo > g, en los tres escenarios | A, B, C | V16 |
| N3 | S2C > 0 | A, B | V14 |
| N4 | Probabilidades en [0, 1] que suman 1; p de quiebra en [0, 1]; recuperación ≥ 0 | A, B, C | V17, V19, V20 |
| N5 | Dominios de Historia y del FCF base; `C76` ≤ `C53`; moneda comparable para leer el precio | A, B, C (C76 solo A) | V09, V37, V34, V25 |
| N6 | Los escenarios respetan su etiqueta: MALO ≤ NORMAL ≤ BUENO en crecimiento y margen, y en valor por acción (sin esto la escalera no significa nada) | A, B, C | `Diagnóstico V6` fila 47; Anexo C §C.4.0 |
| N7 | Motor coherente con el tipo de empresa: financiera → motor C | A, B | V11 |

### [E] Criterios económicos y orientaciones (Damodaran; documento entre paréntesis)

- **E1** El crecimiento estable no debería superar el crecimiento nominal de la economía; como regla práctica, no superar la tasa sin riesgo usada en la valoración (CV). Es una **orientación**, no una ley.
- **E2** En el estado estable la rentabilidad del capital tiende hacia la media del sector o hacia el coste de capital por efecto de la competencia; mantenerla muy por encima durante décadas exige una ventaja competitiva duradera (CV, MR). Es un **criterio**: existen empresas que la mantienen; la carga de la prueba es de quien lo afirma.
- **E3** Si la rentabilidad del capital iguala el coste de capital, el crecimiento no añade valor; solo crea valor el crecimiento con retorno por encima del coste (GV, CV).
- **E4** El crecimiento histórico predice mal el futuro, y el crecimiento alto decae con el tamaño (GV).
- **E5** Cíclicas y materias primas: normalizar sobre el ciclo (5–10 años) y no extrapolar un pico ni un valle (UD).
- **E6** Escenarios: pocos factores; las probabilidades suman 1 solo si los escenarios cubren el rango; no contar el mismo riesgo en la tasa de descuento y en los escenarios o en la distribución (PA).
- **E7** Historia → números: comprobar el relato contra la historia de la empresa, los principios económicos y el sentido común (NN pp. 14, 17). La cuota de mercado implícita como prueba de realismo **no** está en NN: es convención del ejercicio (trazabilidad, 3-nov-2026).
- **E8** Medición del ROIC: NOPAT ÷ capital invertido del año anterior, neto de caja; I+D y arrendamientos capitalizados; partidas no recurrentes depuradas (MR).
- **E9** Financieras: valorar por patrimonio y ROE; el capital regulatorio limita el crecimiento; el motor C no valida la solvencia (FS).

### [C] Convenciones

- **De la plantilla** (`Convenciones_financieras_V6_3.md`): ROIC histórico sobre el capital invertido del **mismo** ejercicio (`Historia` fila 33: EBIT × (1 − t) ÷ capital invertido), no del anterior como en E8; convergencias lineales en 5 años (crecimiento hacia g en los años 6–10, margen hacia el objetivo); S2C marginal como palanca y S2C medio solo como contexto; r del inversor, no coste de capital; r operativa del motor B como tasa personalizada; quiebra como recorte único; listas de los desplegables; y los **umbrales de los semáforos**, elegidos por el autor de la hoja: Q3 del sector y 1,5× la historia (crecimiento), máximo histórico y Q3 (margen), 2× el ROIC histórico (rentabilidad marginal), `C56` + 10 pts (ROIC largo plazo), 75 % (peso del terminal), 30 % (cuota implícita), 5 pts (salto del año 11), 5 % (tolerancia, `Diagnóstico V6!C91`) y 25 % (corte, `C92`) de la conciliación precio × acciones frente a capitalización, 90 días entre fechas (`C93`).
- **Del ejercicio** (este encargo): las reglas de la referencia mecánica (§B.2); probabilidades 0,2/0,6/0,2 como referencia; k = 3; horizonte de 12–24 meses de las predicciones; redondeos; disparadores de quiebra y el 0,05 con disparador; umbral del 5 % de ventas para capitalizar I+D; vidas útiles de la I+D. Cada una se declara como tal en las Observaciones.

**Lo que esto implica para el personaje.** «Damodaran es la gramática» (D4) quiere decir [I] y [N] como obligatorias y [E] como criterios que hay que respetar o rebatir con evidencia. Las cifras de §B.2 son [C]: Munger se desvía de ellas con motivo, y la desviación se estudia; pero desviarse de una convención no es rebatir a Damodaran.

## B.1 Corpus y códigos

`damodaran.md` se construye como `munger.md`: por bloques de páginas, con entradas `- **<sección>** — *<principio en una línea>.* "<cita literal>" (<Título corto>, p. <n>)`, donde el título corto va **completo**, como los nombres de libro en `munger.md` (es lo que lee `cit_corpus_re`). Títulos cortos y códigos: **NN** Numbers and Narrative · **GV** Growth and Value · **MR** Measuring Returns · **CV** Closure in Valuation · **PA** Probabilistic Approaches · **UD** Ups and Downs · **FS** Financial Service Firms. Las citas en el personaje y en las Observaciones llevan el código o el título: `(GV p. 12)`; `verify_quotes_v2.py` (encargo §6.1) las comprueba igual que las de Munger. Las cifras de ejemplo de los papers (primas, márgenes de Toyota, tablas de 2006–2009) **nunca** se usan como parámetros actuales: los parámetros actuales son las anclas de `Historia`, los cuartiles de `Sector` (enero 2026) y las primas de `Riesgo país` (julio 2026).

## B.2 Referencias mecánicas por palanca (convención del ejercicio; las calcula `volcar_datos_v63.py --referencias-mecanicas`)

Qué son y qué no son: una cifra reproducible por escenario, obtenida de las anclas de `Historia` y de los cuartiles de `Sector` con las reglas de abajo, para que la fase B tenga de dónde partir y para que la desviación de Munger sea medible y comparable entre empresas. **No son una estimación de Damodaran** ni una predicción; la columna «Criterio relacionado» dice qué principio de §B.0 recuerda cada regla, sin que ese principio respalde la cifra. Las reglas son la versión 0.2 y se ajustarán tras las primeras empresas, versionando.

Notación: anclas de `Historia` (`C45`…`C66`, series de las filas 28, 29, 33, 34, 35), cuartiles del sector según `Palancas!G14:I14` (crecimiento), `G15:I15` (margen), `G19:I19` (S2C medio) y la media del ROIC del sector en `H18`; tasa del motor = `Análisis!C56` (A y C) o `Diagnóstico V6!C15` (B); rf = `Análisis!C57`; σ = desviación típica **muestral** (n − 1). «Ajustar a la lista» = elegir el valor de la lista del desplegable más cercano (hacia abajo en caso de empate). «Redondear» = múltiplos de 0,005 para crecimientos y márgenes, 0,1 para S2C, 0,01 para ROIC. Se calculan **después** de la fase A (dependen del motor, de `C8`, `C5`, `C9`, `C10` y `C7`) y siempre se fuerza MALO_ref ≤ NORMAL_ref ≤ BUENO_ref (si una regla da lo contrario, se iguala al NORMAL_ref y se anota).

**Referencia no disponible.** Si los datos no permiten calcular una referencia defendible, el script la registra como `null` con el motivo (`referencia_no_disponible_motivo`) y **no la sustituye** por otra medida (ni la mediana del sector, ni el S2C medio, que es otra magnitud). Sin referencia, la palanca no puede tomar la clase «sin juicio propio» (no hay nada que copiar): Munger la decide con clase *fundamentada* o *convención*, o escribe un valor *técnico* declarado («solo permite calcular», con su rango). *Técnico* cuenta como insuficientemente fundamentada a efectos de D10 (§B.6).

| Palanca | NORMAL_ref | MALO_ref | BUENO_ref | No disponible cuando | Criterio relacionado (no respalda la cifra) |
|---|---|---|---|---|---|
| **Crecimiento ventas 1–5** (`B14:D14`; en C, del patrimonio con la serie anual de la fila 21) | `C46` (CAGR propio 5 años) acotado al rango [Q1, Q3] del sector. «En declive» → mín(NORMAL_ref, 0). | mín(NORMAL_ref, máx(mín(Q1 sector, NORMAL_ref − σ), −0,10)), con σ de la serie anual (fila 28; si hay < 4 tasas, σ = 0,03). | máx(NORMAL_ref, mín(NORMAL_ref + σ, Q3 sector, 1,5 × `C46` si `C46` > 0)). | `C46` no es número, o faltan los cuartiles del sector. | E4 (el pasado predice mal; el crecimiento alto decae); I1 (el crecimiento se paga con reinversión). |
| **Margen objetivo año 5** (`B15:D15`; ROE objetivo en C) | m₀ = `C48` si `C8` = Último año, `C49` si Media del ciclo (motor C: `C60` / `C56`). | máx(mín(m₀, `C49`), `C50`) (motor C: con la fila 34). | máx(m₀, mín(`C51`, Q3 sector)). Si m₀ es ya el máximo histórico, BUENO_ref = m₀. | m₀ no es número (menos de un ejercicio con margen). | E2 (la competencia muerde los márgenes); E5 (cíclicas: media del ciclo); E7 (comprobar contra la historia). |
| **S2C marginal** (`B16:D16`; motores A y B) | `C53` si es número > 0. Tope: si m_obj_ref(NORMAL) × (1 − `C52`) × S2C_ref > 2 × `C55` (la rentabilidad marginal de `Diagnóstico V6!C176`, umbral de la plantilla), se reduce S2C_ref hasta que esa rentabilidad sea 2 × `C55`. | 0,75 × NORMAL_ref. | 1,25 × NORMAL_ref (mismo tope, con el margen objetivo del BUENO). | `C53` no es número o es ≤ 0 (reinversión neta acumulada ≤ 0): **no se sustituye** por el S2C medio del sector, que es otra medida. | I1 (reinversión = Δventas ÷ S2C). La banda ±25 % es convención del ejercicio. |
| **g para siempre** (`B68:D68`) | mín(0,025; rf), ajustado a la lista. «En declive» → ≤ 0,01. Si rf no está: 0,025. | NORMAL_ref − 0,01 (suelo 0), ajustado a la lista. | mín(NORMAL_ref + 0,005; rf; 0,03), ajustado a la lista (0,03 es el máximo de la lista). | nunca (0,025 es convención del ejercicio si falta rf). | E1 (g estable ≤ tasa sin riesgo, orientación). N1 (g < tasa del motor). |
| **ROIC largo plazo** (`B18:D18`; ROE en C) | = tasa del motor. **Convención del ejercicio** que recuerda E2/E3 (sin retornos en exceso a perpetuidad como caso neutro), no una ley: Munger se desvía hacia arriba si defiende la duración del foso (G4). Se muestra al lado la media del ROIC del sector (`H18`) como alternativa. | = tasa del motor. | mín(`C55`; `Análisis!C56` + 0,10) (motor C: `Historia!C56`, ROE medio). Si `C55` < tasa del motor: tasa del motor. | `C55` no es número (menos de 5 ejercicios con ROIC): BUENO_ref no disponible; NORMAL_ref y MALO_ref sí. | E2, E3; I2 (reinversión terminal g ÷ ROIC). El umbral + 0,10 es de la plantilla. |
| **Probabilidades** (`B69:D69`) | 0,6 | 0,2 | 0,2 | nunca | E6 (suman 1 si cubren el rango). 0,2/0,6/0,2 es convención del ejercicio heredada del v1 (S-6). |
| **Quiebra** (`C22`, `C23`) | vacío (= 0) salvo disparadores (convención del ejercicio): `Análisis!C33` > 4, `C34` = No, `C5` = Joven, o deuda + arrendamientos (`Historia!C64`) > 3 × FCF base. Con disparador: 0,05 como convención y obligación de argumentar. `C23` = 0. | igual | igual | nunca | E6 (no contar el riesgo dos veces). Las tablas por rating de Damodaran son a 5 años, no a 10 (`Palancas!E22`). |
| **Exceso de caja** (`C76`, solo A) | 0 | 0 | 0 | nunca | Regla del inversor v1.2. |
| **Tamaño de mercado** (`C24`) | vacío | | | siempre, salvo cifra de fuente primaria en los extractos | convención del ejercicio (cuota implícita como prueba de realismo; no es de NN). |

La tabla que recibe la fase B incluye, por palanca: NORMAL_ref/MALO_ref/BUENO_ref (o `null` con motivo), las anclas usadas con su valor, los cuartiles del sector, la **rentabilidad marginal implícita** de cada escenario con las referencias (S2C × m × (1 − t)) y el **salto del año 11** que producirían frente al ROIC_ref. Así la fase B ve de antemano dónde la gramática va a chirriar.

## B.3 Comprobaciones (`comprobar_gramatica.py`)

**Categorías y consecuencias (D17).**

- **Error** (incumple [I], [N] o una regla de formato del ejercicio): bloquea. Lo corrige la fase responsable (B o C); si tras `max_correcciones_fase_b` (o `max_correcciones_auditoria`, según la fase) persiste, el pipeline termina en `no_entregable` con diagnóstico (D18). **Ninguna explicación lo aprueba.**
- **Límite del modelo**: el motor elegido no puede valorar esta empresa. No es un fallo del prompt: la fase A elige otro motor coherente si lo hay, o el análisis termina en `modelo_no_aplicable`, estado legítimo que conserva el juicio cualitativo (cubo cualitativo, descalificadores, gestión) y renuncia a la escalera.
- **Desviación económica**: valor admisible solo con evidencia y razonamiento específicos. Exige una entrada en `desviaciones_justificadas` con `justificacion` no vacía que cite hechos del extracto o de la Historia (celda o página), clase *fundamentada* o *convención* (nunca *sin juicio propio* ni *técnico*) y, si invoca a Munger o a Damodaran, cita verificable. Una justificación vacía, genérica («es una gran empresa») o circular («porque el BUENO es bueno») **no es una justificación y cuenta como error**.
- **Aviso**: se informa en `gramatica.md`, la ficha y el informe; no bloquea por sí solo.

**Interfaz.** Entradas: `fase_b.json`, `referencias_mecanicas.json`, las anclas y cuartiles (los mismos que usó `volcar_datos_v63.py`), `config_v2.json` y, en el modo `--tras-recalculo`, `resultados.json` (y `fase_c.json` si existe). Salida: `gramatica.json` (lista de `{id, categoria, escenario, motor, detalle, requiere_justificacion, justificada, consecuencia}`) y `gramatica.md` (el texto que recibe el agente para corregir). Código de salida: 0 sin errores ni desviaciones sin justificar; 1 desviaciones sin justificar; 2 errores; 3 límite del modelo detectado (la fase A tiene que pronunciarse). Si coinciden varias categorías, prevalece el código mayor: 3 › 2 › 1. Se ejecuta `--antes-de-recalculo` sobre `fase_b.json` (paso 8: G1–G7, G9–G12, G14, G15, G18) y `--tras-recalculo` (pasos 9, 10 y 12: G8, G16, G17, G19 y de nuevo las anteriores sobre las celdas escritas; **G13 solo en los pasos 10 y 12**, cuando las predicciones existen). En el paso 9 del pipeline un código 1 por G8/G16/G17 no detiene: `gramatica.md` entra en la fase C, que es quien justifica o corrige; en el paso 10 (tras escribir la fase C) y en el paso 12 toda desviación tiene que estar justificada.

| Id | Comprobación | Categoría | Motores | Base (§B.0) | Consecuencia |
|---|---|---|---|---|---|
| G1a | MALO ≤ NORMAL ≤ BUENO en crecimiento (`B14:D14`) y margen (`B15:D15`) | error | A, B, C | N6 | corregir en la fase B |
| G1b | S2C, g y ROIC ordenados entre escenarios | desviación | A, B (C: g y ROE) | convención del ejercicio (la hoja lo marca REVISAR en la fila 47) | justificar por qué un escenario peor reinvierte mejor, o corregir |
| G2 | g < tasa del motor; ROIC LP > g, en los tres escenarios | error | A, B, C | N1, N2 | corregir |
| G3 | g > rf (`C57`) | desviación | A, B, C | E1 | justificar con el crecimiento nominal esperado de la economía donde vende |
| G4 | ROIC LP > `Análisis!C56` + 0,10 (como `Diagnóstico V6!C43`, en los tres motores) | desviación | A, B, C (ROE en C) | E2; umbral de la plantilla | solo con `C18` = Sí y una justificación que diga **cuánto dura** la ventaja y qué la sostiene |
| G5 | Margen objetivo > `C51` (máximo histórico) o > Q3 del sector (C: ROE > 1,5 × sector) | desviación | A, B, C | E2, E5; umbral de la plantilla | justificar con el mecanismo (precio, mezcla, escala) y quién se queda la mejora |
| G6 | Crecimiento 1–5 > Q3 del sector o > 1,5 × `C46` | desviación | A, B, C | E4; umbral de la plantilla | justificar por componentes (unidades, precio, mezcla) y dónde se reinvierte |
| G7 | Rentabilidad marginal (S2C × m × (1 − t)) > 2 × `C55` | desviación | A, B | I1, E3; umbral de la plantilla | justificar por qué cada euro nuevo rendiría el doble que la historia |
| G8 | Salto del año 11 (rentabilidad marginal años 1–10 − ROIC LP) > 0,05 en valor absoluto | desviación (tras recálculo) | A, B | I2, E2; umbral de la plantilla | la tesis (`B101`/`B102`) o la Observación de `B18:D18` explica la pérdida (o ganancia) de ventaja en el año 11 |
| G9 | S2C ≤ 0 | error | A, B | N3 | corregir |
| G10a | Probabilidades fuera de su lista o que no suman 1; g para siempre fuera de su lista | error | A, B, C | N4; convención del ejercicio (solo valores de la lista; la hoja admite otros, `Opciones!A18`) | corregir |
| G10b | BUENO con más probabilidad que MALO sin justificación | desviación | A, B, C | convención del ejercicio (S-6) | justificar con una razón estructural escrita |
| G11 | `C22` > 0 sin disparador declarado, o `C22` > 0 cuando la Observación de r dice que r ya incluye prima de quiebra | desviación | A, B, C | E6 | justificar o quitar la doble cuenta |
| G12 | `C76` > `C53`, o `C76` informado con motor B o C | error | A (B, C: no informar) | N5 | corregir |
| G13 | Tres predicciones con texto, fecha entre 12 y 24 meses y probabilidad en [0, 1]; ninguna sobre el precio de la acción ni sobre macro (solo se evalúa tras la fase C) | error | A, B, C | convención del ejercicio (S-9); completitud C07 | corregir en la fase C |
| G14 | Cada palanca con `referencia_mecanica` (o `null` + motivo), `valor`, `desviacion`, `clase`, `confianza`, `porque`, `lo_sustituiria`; desviación ≠ 0 con clase *sin juicio propio*; clase *sin juicio propio* con referencia `null` | error (implementación) | A, B, C | — | corregir |
| G15 | Cifras con más precisión que el redondeo de §B.2 | error (formato) | A, B, C | convención del ejercicio | corregir |
| G16 | Peso del terminal > 75 % en el NORMAL | desviación (tras recálculo) | A, B, C | E7; umbral de la plantilla | la fase C explica por qué el valor lejano es defendible |
| G17 | Cuota implícita > 30 % si hay `C24` | desviación (tras recálculo) | A, B | E7; umbral de la plantilla | justificar o revisar el BUENO |
| G18 | Motor C con `B16:D16` informado; motor A o B con `C6` = Financiera | error (coherencia motor/caso) | A, B, C | N7 | `B16:D16` informados con motor C: la fase B los vacía (código 2). Motor A o B con `C6` = Financiera: el script devuelve código 3 y la pregunta vuelve a la fase A una vez (`max_vueltas_fase_b_a_a_por_limite_del_modelo`), que corrige el motor o declara L2 |
| G19 | Valores por acción desordenados tras recálculo (`B78` ≤ `C78` ≤ `D78`) | error | A, B, C | N6 | vuelta a la fase B (una vez); si persiste, `no_entregable` |
| L1 | FCF base ≤ 0 con naturaleza «Estructural» (`Palancas!C43`) y motor A | límite del modelo | A | regla de la hoja (`Guía V6` filas 17–18) | la fase A elige B si la financiación lo permite; si no, `modelo_no_aplicable` |
| L2 | Financiera (`C6`) cuyo negocio el personaje juzga que el motor C no captura (capital regulatorio, cartera, seguros) | límite del modelo | C | E9 | `modelo_no_aplicable`, con el juicio cualitativo conservado |
| L3 | `C62` = «No · este tipo de empresa requiere otro método» | límite del modelo | — | decisión del personaje | `modelo_no_aplicable` |
| A1 | S2C medio fuera del rango del sector (fila 46) | aviso | A, B | — | se informa |
| A2 | r < r mínima (fila 48; `Diagnóstico V6!C18`) | aviso | A, B, C | — | se informa (r es heredada, S-3) |
| A3 | Fechas del precio y de las acciones separadas más de 90 días (V28) | aviso | A, B, C | — | se informa |
| A4 | Regulada o conglomerado (fila 49) | aviso | A, B, C | — | se informa; conglomerado: Munger suele llevarlo a Demasiado difícil |
| A5 | La palanca más influyente del tornado (`C221`) es la tasa de descuento | aviso | A, B, C | — | la ficha dice que el valor depende sobre todo de la r exigida |
| A6 | f (`Diagnóstico V6!C12` = `Historia!C58`) fuera de [−0,02; 0,05] (fila 50: «un f raro casi siempre es un dato mal puesto») | aviso | A | regla de la hoja (fila 50) | se informa; la fase A revisa el FCF base (`C43`/`C44`) y considera el motor B; si el dato de entrada está mal, lo declara y el pipeline lo trata como dato inválido en la comprobación de entrada (`pendiente_de_datos`) |

## B.4 Qué buscar en cada paper para la trazabilidad (`trazabilidad_damodaran.md`)

Para cada principio [I] y [E] de §B.0 y para cada comprobación que lo invoque, Claude Code localiza en el texto extraído la frase que lo sostiene y registra documento y página. Lista orientativa de lo que hay que encontrar:

- **NN**: los pasos historia → comprobación contra la realidad (historia de la empresa, principios económicos, sentido común) → variables de valor (mercado, cuota, ingresos, margen, reinversión, riesgo, probabilidad de fracaso) → valor → bucle de contraste.
- **GV**: g = tasa de reinversión × retorno, con sus condiciones; crecimiento por eficiencia y su duración limitada; el crecimiento histórico como mal predictor; el crecimiento solo crea valor si el retorno supera el coste.
- **MR**: definición de ROIC (NOPAT ÷ capital invertido del año anterior, neto de caja); capitalización de I+D (vida útil por sector) y de arrendamientos; partidas no recurrentes; cómo tratar las participaciones; desvanecimiento de los retornos en exceso con la competencia.
- **CV**: g estable ≤ tasa sin riesgo como regla práctica; reinversión = g ÷ ROC (pp. 12–13 y ejemplos pp. 14–15, 17; la advertencia de una fórmula impresa al revés no se confirma en el PDF aportado); ROC estable hacia la media del sector; si ROC = coste de capital el crecimiento no cambia el valor; duración del periodo de crecimiento alto según tamaño, ventaja y barreras.
- **PA**: número de escenarios y factores; probabilidades que suman 1 si los escenarios cubren el rango; doble cuenta del riesgo (tasa + escenarios, o tasa + distribución); árboles de decisión para riesgos secuenciales (no se usan en la plantilla).
- **UD**: media del ciclo (5–10 años) aplicada a las ventas actuales; peligro de extrapolar pico o valle; normalización selectiva como pecado.
- **FS**: patrimonio y ROE como base; capital regulatorio como límite al crecimiento; límites del modelo simplificado (lo que el motor C **no** valida: solvencia ni capital regulatorio).

Si un principio no encuentra apoyo literal, se reclasifica como **convención del ejercicio** o **convención de la plantilla**; nunca se atribuye.

## B.5 La capa de traducción Munger → palancas (para `personaje_munger_v2.md` §5.2)

| Idea de Munger (cita a verificar en `munger.md`) | Palanca | Cómo se aplica |
|---|---|---|
| «The question of how long your period in the sun will be is a very good one» (AIWTK p.127) · «most big businesses eventually fall into mediocrity» (AIWTK p.140) | ROIC LP, salto del año 11 | El ROIC terminal por encima de r es una afirmación sobre la **duración** del foso (E2). Se dice cuántos años y qué lo sostiene. |
| «The second earns 12 percent, but all the excess cash must be reinvested… We hate that kind of business» (PCA p.110; TCI p.95) | S2C, reinversión | Un S2C bajo con margen bajo es el negocio que odia: el motor ya lo castiga (I1); Munger lo nombra. |
| «Three things ruin people: drugs, liquor, and leverage» (TCI p.68) · «if the world suddenly didn't like our credit, we wouldn't even notice it for months» (TCI p.91) | Motor B, quiebra, C20 | Deuda que puede matar en un mal año → No; si solo cambia mucho → motor B; la quiebra solo con causa (E6: sin doble cuenta). |
| «how much is going to stay home and how much is just going to flow through to the customer» (PCA pp.187–189) | Margen objetivo | Toda mejora de margen tiene un dueño: se dice si es la empresa o el cliente (E2). |
| «all man's desired geometric progressions… at last come to grief on a finite earth» (PCA p.394) | g, años 6–10 | Nada crece deprisa para siempre: g bajo y decaimiento aceptado (E1, E4). |
| «if a company generates high returns on capital and reinvests at high returns, it will do well» (TCI p.70) | g = reinversión × retorno | La identidad del crecimiento fundamental (I1), con sus condiciones: el crecimiento del BUENO necesita dónde reinvertir y a qué retorno. |
| «Better roughly right than precisely wrong» (PCA p.451) | Todas | Cifra redonda con rango; el número prueba si el cubo sobrevive, no produce un valor exacto. |
| «Since it's so obvious that investing in great companies works, it gets horribly overdone» (PCA p.214) · «We left a lot of money on the table through early fretting» (TCI p.79) | Precio de Sí | Los dos errores opuestos, nombrados en cada análisis. |
| «a horse with one chance in two of winning, and that pays three to one» (TCI p.105; AIWTK p.153) | k = 3 | La convención del precio de Sí (D11), declarada como convención experimental; la metáfora inspira, no demuestra. |

Las páginas de esta tabla son las que usa el personaje v1 (las doce citas se han comprobado en `munger.md` el 30-oct-2026); `verify_quotes_v2.py` las vuelve a comprobar al construir el v2.

## B.6 Fundamento material y comprobación conjunta (D10)

**Hipótesis materiales** (mueven el valor o la conclusión): las cinco palancas en los tres escenarios (`B14:D16`, `B18:D18`, `B68:D68`), las probabilidades (`B69:D69`), la quiebra y su recuperación (`C22`, `C23`), el exceso de caja (`C76`), el FCF normalizado (`C44`), el motor (`C62`), la base del margen (`C8`), el caso especial (`C6`) y las **narrativas de los escenarios** (`B65:D66`), que son el fundamento de todo lo demás. La r (`C56`) no es decisión de Munger (S-3): se informa, no entra aquí.

**Insuficientemente fundamentada**: una hipótesis material cuya clase es *sin juicio propio* o *técnico*; o *fundamentada* / *convención* pero cuya Observación no cita ningún hecho del extracto o de la Historia; o una narrativa de escenario cuyo mecanismo y «qué lo pararía» son genéricos, sin hechos de los extractos (lo juzga la fase C y lo comprueba el agente de verificación).

**Procedimiento (fase C, en dos turnos del mismo agente; encargo §4.5 y §4.7, pasos 10–12):**

1. La fase C reúne la lista completa `hipotesis_sin_fundamento` (celda, clase, por qué no está fundamentada), dentro y fuera del tornado. **El tornado no mide incertidumbre** (una sensibilidad individual no dice cuánto puede estar equivocado un supuesto, y los efectos conjuntos no son aditivos): sirve para informar de qué palanca pesa, no para aprobar.
2. Si la lista está vacía, D10 no limita la conclusión.
3. Si no está vacía, para cada hipótesis la fase C busca **alternativas defendibles**. Un rango es defendible solo si **cada uno de sus dos límites está atado a un hecho de esta empresa** (una celda de `Historia`, una página del extracto, una cifra publicada por la empresa) y la fase C explica **por qué ese hecho acota el valor por ese lado**. No son fundamento por sí solos: una media o un cuartil del sector (son datos de otras empresas; sirven de contexto, no de suelo ni de techo de esta), un umbral de la plantilla (es una convención de aviso, no un techo económico), ni la variabilidad histórica de una serie para acotar probabilidades (la dispersión de los márgenes no dice cuánto vale p(MALO); hace falta decir qué frecuencia observada o qué mecanismo de esta empresa sostiene cada límite). Cuando no existe fundamento suficiente para acotar una hipótesis, se **registra la limitación** (`hay_base = false`, con lo que haría falta) y, si la conclusión provisional es favorable (`comprar`), el resultado es **`pendiente_de_investigacion`**: sin conclusión de compra, con esa hipótesis y lo que la resolvería en `Diagnóstico V6!B222:B223`, en la ficha y en el informe. Antes de este paso la fase C ha hecho la revisión de datos ausentes (S-19, encargo §4.5): si un dato ausente material ya impide la conclusión favorable, no se llega a la comprobación conjunta.
4. Si todas tienen alternativas defendibles, la fase C define **una combinación adversa económicamente coherente**: una sola historia en la que esas hipótesis toman a la vez sus valores defendibles menos favorables a la tesis, con la coherencia entre ellas explicada (por ejemplo: si el foso dura menos, bajan juntos el margen objetivo y el ROIC terminal y no mejora el S2C). No se perturba nada automáticamente ni se introduce ningún umbral nuevo. Es **una sola** combinación: definir varias abriría la puerta a elegir la que convenga.
5. `comprobacion_conjunta.py` copia el libro evaluado a `comprobacion_conjunta/<Empresa>_conj.xlsx` (copia de prueba: no es entregable y no sustituye nada), escribe la combinación con el método de la pieza 1, recalcula con recálculo forzado, lee `B78:D78`, `C83`, `Motor!B255` y los semáforos, ejecuta `precio_de_si.py` sobre esa copia y escribe `comprobacion_conjunta.json` con la combinación, la evidencia y los rangos usados, los resultados y la zona del precio actual bajo la combinación.
6. La fase C lee el resultado. Si la conclusión favorable **sobrevive** (la zona del precio actual sigue cumpliendo la regla de precio y no aparece ningún error), puede mantenerla, y la ficha y el informe la presentan como «comprobación conjunta superada: no es una garantía de seguridad». Si **no sobrevive**, la conclusión depende de hipótesis que no pueden sostenerse: **`pendiente_de_investigacion`**, con la lista.
7. Con conclusión provisional no favorable (`esperar`, `descartar`, `demasiado_dificil`) la comprobación conjunta es opcional; si se hace, su escalera bajo la combinación adversa se informa como rango del precio de Sí. Con `esperar` y alguna hipótesis sin base, el precio objetivo se marca **provisional** en `C104`, la ficha y el informe, con la hipótesis que lo condiciona (la lista de `hipotesis_sin_fundamento` se reúne siempre).

Lo que el personaje escribe en `B222` y `B223` sale de esta lista: la hipótesis sin fundamento que más condiciona la conclusión y el dato o documento concreto que la resolvería.
