# ANEXO A · Las 68 celdas de juicio de la V6.3 que decide el personaje v2

Versión 0.2.1 (2-nov-2026). Fuente: `Plantilla_V6.3.xlsx` (validaciones de datos, hoja `Opciones`, nombres definidos y filas de `Control maestro`), leída el 30-oct-2026. Si al construir aparece una discrepancia con la plantilla real del repositorio, **manda la plantilla** y se anota en `DECISIONES.md`.

Convenciones de la tabla: **CM** = fila de `Control maestro` cuya columna B apunta a la celda (ahí van E, F y N). **Mat.** = la celda está en el inventario de entradas materiales del motor (`Control maestro` 179–236): mueve el valor y la hoja exige su justificación para `LISTO`; entre paréntesis, la comprobación de completitud (C05…C10) cuando la celda cuenta para el estado del libro sin ser material. **Fase** = quién la decide (A cualitativa · B palancas · C revisión); C puede corregir cualquiera en su única vuelta. Las 34 celdas de A.1 son heredadas de la etapa 1 (las copia `migrate_values.py`; el v2 las re-decide); las de A.2 y A.3 son nuevas en la V6.3.

Los valores de los desplegables se escriben **exactamente** como aquí (acentos, mayúsculas, puntos medios). Los porcentajes, como decimales (0,07, no «7 %»). Las listas marcadas «sugerida» admiten otros valores; g para siempre (`B68:D68`) y probabilidades (`B69:D69`) toman **solo** valores de su lista (`comprobar_celdas_v2.py` y G10a lo tratan como error; cerrar la lista es convención del ejercicio: la hoja admite otros valores).

Aviso para los scripts: en `Palancas` las cabeceras `E13:H13` («Media propia · Sector Q1 · Sector mediana · Sector Q3») están desplazadas una columna respecto a los valores: `F` = media propia, `G`/`H`/`I` = Q1/mediana/Q3. Las columnas citadas en este anexo (`F14`, `I14`, `I15`, `H18`, `G19:I19`) son las de los valores.

## A.1 Hoja `Análisis` (34 celdas, todas heredadas)

| Celda | Concepto | Valores válidos | CM | Mat. | Fase | Reglas del v2 |
|---|---|---|---|---|---|---|
| C11 | ¿Entiendo el negocio en ≤ 5 frases? | `Sí` / `No` (exacto) | 21 | no | A | Literal. Cinco frases en `fase_a.md`: qué vende, quién paga, por qué, de dónde sale la caja. `No` → cubo Demasiado difícil. |
| C12 | ¿Círculo de competencia? | `Sí` / `No` (exacto) | 22 | no | A | Prueba del v1: ¿puedo juzgar si el foso dura diez años? |
| C13 | ¿Valor claro sin modelos? | `Sí` / `No` (exacto) | 23 | no | A | Literal, **al precio actual**. Si hace falta la hoja para ver que está barata: `No`. Con `No` la hoja dirá «DESCARTADA POR FILTRO PABRAI»: se documenta como el v1 (regla 4). |
| C14 | Tipo de oportunidad | `Compounder` / `Calidad a precio razonable` / `Deep value / especial` / `Cíclica / commodity` / `Turnaround / situación especial` | 24 | no (C10) | A | Condiciona los umbrales de `D24` y `D19`. Nunca se elige por el veredicto que produce. |
| C17 | ¿Viento de cola duradero? | `Sí` / `No` | 25 | no | A | Viento del sector, no mérito de la empresa (v1 §4). Anotar cuál. |
| C18 | ¿Moat sostenible? | `Sí` / `No` | 26 | no | A | Marco del v1 §4 (tipos de foso, sobrino idiota, quién me mata). Es la celda que después justifica cualquier ROIC largo plazo por encima de r. |
| C19 | ¿Crecen ingresos/beneficios de forma consistente? | `Sí` / `No` | 27 | no | A | Con la Historia de 10 años delante (filas 6, 9 y 28). Un bache cíclico no es `No`. |
| C20 | Riesgo ≠ incertidumbre | `Incert. alta + riesgo bajo` / `Ambos bajos` / `Riesgo real alto` | 28 | no | A | Regla del inversor (v1.2): riesgo = pérdida permanente **al precio pagado**. |
| C25 | ¿FCF creciente? | `Sí` / `No` | 30 | no | A | Con `Historia` fila 35 (FCF al accionista por año). FCF normalizado y recurrente, no la cifra de un año. |
| C27 | Tendencia de márgenes 5–10 años | `Expandiendo` / `Estable` / `Comprimiendo` | 32 | no | A | Con `Historia` fila 29. Capex de capacidad con retorno alto no es deterioro. |
| C51 | ¿Restar SBC del FCF base? | `Sí` / `No` | 49 | sí (motor A y `C50` ≠ 0) | A | **Siempre `Sí`** (v1; `Diagnóstico V6!B77` avisa si `No`). |
| C56 | r (rentabilidad exigida) | decimal; lista sugerida 0,08 … 0,15 | 53 | sí | A | **Heredada, no se cambia** (S-3). Si viene vacía: `config_v2.json`. La Observación dice qué alternativa representa y si r < r mínima (`Diagnóstico V6!C17:C18`). |
| C61 | ¿Recompras neutralizan la SBC? | `Sí` / `No` / `No está claro` | 56 | no | A | Con `Historia` fila 20 (acciones diluidas) y `C60`. |
| C62 | Motor / aplicabilidad del DCF | `Sí` / `No · financiación cambia mucho` / `No · banco o aseguradora` / `No · este tipo de empresa requiere otro método` | 57 | sí | A | `Sí` = motor A; «financiación cambia mucho» = motor B; «banco o aseguradora» = motor C; «otro método» = sin valoración (entonces el cubo no puede ser Sí). Criterios en el personaje v2 (deuda que cambia, f fuera de rango en `Diagnóstico V6!C50`, financieras → sesgo a Demasiado difícil). |
| B65 / C65 / D65 | MALO / NORMAL / BUENO: ¿qué tiene que pasar? | listas de `Opciones` A3:A10 / B3:B7 / C3:C8, u `Otra (explícala en tus palabras)` | 58 / 63 / 68 | no (V21 exige valor) | A | Obligatorias: sin historia el escenario no se calcula. |
| B66 / C66 / D66 | Escenario en una frase | texto | 59 / 64 / 69 | no (C09) | A | La frase nombra el mecanismo económico y quién se queda la mejora. |
| B68 / C68 / D68 | g para siempre | `0` / `0,005` / `0,01` / `0,015` / `0,02` / `0,025` / `0,03` (lista) | 61 / 66 / 71 | sí | B | < tasa de descuento del motor en los tres escenarios (condición necesaria N1, error G2); > tasa sin riesgo (`C57`) solo con justificación (criterio E1, desviación G3). «En declive» → ≤ 0,01. Referencia mecánica: Anexo B §B.2. |
| B69 / C69 / D69 | Probabilidades | `0,1` / `0,15` / `0,2` / `0,25` / `0,3` / `0,4` / `0,5` / `0,6` (lista); suman 1 | 62 / 67 / 72 | sí | B | Referencia mecánica 0,2/0,6/0,2 (convención del ejercicio); se argumenta (S-6). Hipótesis material para D10 aunque no esté en el tornado. |
| C76 | Exceso de caja no operativa (mm) | motor A: número ≥ 0 y ≤ `C53` (0 si no hay); motores B y C: **vacío** | 82 | sí (si ≠ 0) | B | Regla del v1.2 (intereses cobrados, caja comprometida). Nunca restar deuda aquí. Hipótesis material para D10. |
| C93 | ¿g NORMAL sostenible? | `Sí` / `No` / `No lo sé` | 74 | no (C10) | C | Se decide **después** de ver el salto del año 11 (`Diagnóstico V6` bloque 10) y el peso del terminal. `No lo sé` obliga a listar qué falta. |
| C97 | Insiders | `Comprando` / `Neutral` / `Vendiendo` | 76 | no (C06) | A | Regla del inversor del 25-oct-2026 (kit v1.3, prompt de juicio): ventana 12 meses, hechos de la evidencia de fase 1. |
| C98 | Asignación de capital | `Buena` / `Aceptable` / `Dudosa` | 77 | no (C06) | A | Historial, no promesas (v1 §5). Con `Historia` filas 12, 13, 18 y 20 delante (capex, adquisiciones, SBC, acciones). |
| B101 | Tesis en ≤ 5 frases | texto (celda combinada B101:D101) | 78 | no (C05) | C | Se reescribe en la etapa 2 (S-8). |
| B102 | Tesis inversa | texto (B102:D102) | 79 | no (C05) | C | Defender el No mejor que un bajista, con hechos de los extractos y de la Historia. |
| C103 | ¿«Nunca vender»? | `Sí` / `No` | 80 | no (C10) | C | Propiedad del negocio, no de si se compró (v1). |
| C104 | Tamaño de posición | texto (sin validación en la plantilla) | 81 | no (C10) | C | **El personaje no decide tamaño ni escribe porcentajes, tampoco «0 %» (D16, S-18).** Formato: `«Pendiente de decisión de cartera · conclusión del personaje: <comprar al precio actual | esperar: precio de Sí ≤ P | descartar (No) | demasiado difícil | sin conclusión (pendiente de investigación) | sin conclusión (pendiente de datos: <celdas>)> · zona <zona> · precio de Sí ≤ P · precio esc. MALO Q · ponderado R · fundamento <lista vacía | comprobación conjunta superada | pendiente de investigación | pendiente de datos>»`. Si `B78` ≤ 0: «precio esc. MALO: sin precio». Con descartar, demasiado difícil o modelo no aplicable, los insumos de escalera pueden ser «sin escalera aplicable». |

Celdas de `Análisis` que **no** escribe el v2 aunque sean de entrada: `B67:D67` (fórmula en V6.3), `C24`, `C26`, `C28`, `C31:C34`, `C37`, `C38`, `C40:C42`, `C46:C50`, `C53:C55`, `C57`, `C60`, `C88`, `C96` (datos de fase 1 / etapa 1).

## A.2 Hoja `Palancas` (32 celdas, todas nuevas en la V6.3)

| Celda | Concepto | Valores válidos | CM | Mat. | Fase | Reglas del v2 |
|---|---|---|---|---|---|---|
| C5 | Etapa del ciclo de vida | `Joven (sin beneficios estables)` / `En crecimiento` / `Madura en crecimiento` / `Madura` / `En declive` | 137 | no (C03) | A | Por el patrón de crecimiento, reinversión y márgenes de la Historia (NN; GV). «Joven» obliga a pensar la quiebra; «En declive» acota g. |
| C6 | Caso especial | `Ninguno` / `Financiera (banco o aseguradora)` / `Regulada (red, concesión)` / `Cíclica o materias primas` / `Intangibles (I+D, marca)` / `Emergente (riesgo país)` / `Multinegocio o conglomerado` | 138 | sí | A | Coherente con el motor (`Diagnóstico V6!C6`). Conglomerado → aviso: Munger lo lleva a Demasiado difícil salvo que lo entienda por partes. |
| C8 | Base de partida del margen | `Último año` / `Media del ciclo` | 139 | sí | A | «Media del ciclo» si `C6` = cíclica o si el margen del último año es el máximo o el mínimo de la serie (UD). |
| C9 | ¿I+D capitalizada en las anclas? | `Sí` / `No` | 140 | no | A | `Sí` si `C6` = Intangibles o si la I+D (`Historia` fila 19) supera el 5 % de las ventas (MR). Solo cambia las anclas. |
| C10 | Vida útil de la I+D (años) | entero ≥ 1 (vacío si `C9` = No) | 141 | no | A | 3 software · 5 tecnología/industrial · 10 farmacia (pista de la hoja; MR). Convención. |
| B14 / C14 / D14 | Crecimiento de ventas años 1–5 (motor C: del patrimonio) | decimal | 142 / 146 / 150 | sí | B | Referencia mecánica: Anexo B §B.2 (o «no disponible»). Desviación económica G6: > Q3 del sector (`Palancas!I14`) o > 1,5× la historia (`F14`) exige justificación específica. |
| B15 / C15 / D15 | Margen operativo objetivo año 5 (motor C: ROE objetivo) | decimal | 143 / 147 / 151 | sí | B | Referencia mecánica: Anexo B §B.2. Desviación económica G5: > máximo histórico (`Historia!C51`) o > Q3 (`I15`) exige justificación específica. Recoge el crecimiento por eficiencia (I1). |
| B16 / C16 / D16 | Ventas por euro reinvertido (S2C marginal) | decimal > 0 (motor C: no se usa, dejar vacío) | 144 / 148 / 152 | sí (A, B) | B | Referencia mecánica: `Historia!C53` si es > 0; si no, **no disponible** (no se sustituye por el S2C medio del sector, medida distinta, fila 19). S2C ≤ 0 es error (N3, G9). |
| B18 / C18 / D18 | ROIC a largo plazo (motor C: ROE) | decimal > g | 145 / 149 / 153 | sí | B | Referencia mecánica = tasa del motor (convención del ejercicio que recuerda el criterio E2/E3; no una ley). > `Análisis!C56` + 0,10 solo con `C18` = Sí y justificación que diga cuánto dura la ventaja (G4); ≤ g es error (N2, G2). |
| C22 | Probabilidad de quiebra en 10 años | decimal en [0, 1]; **vacío = 0** por convención | 154 | sí (si > 0) | B | Solo con causa concreta de apalancamiento o liquidez (disparadores, convención del ejercicio); si se rellena, no se castiga también en r (E6, G11). Hipótesis material para D10. |
| C23 | Recuperación si quiebra (mm, valor presente) | número ≥ 0 | 155 | sí (si C22 > 0) | B | Casi siempre 0. Se escribe 0 explícito cuando C22 > 0. Hipótesis material para D10 si > 0. |
| C24 | Tamaño del mercado en el año 10 (mm) | número > 0, opcional | 156 | no | B | Solo con cifra de fuente primaria en los extractos; si no, vacío. Techo, no promesa. |
| A38 / A39 / A40 | Predicción 1 / 2 / 3 (qué, métrica, umbral) | texto | 157 / 160 / 163 | no (C07) | C | Sobre el negocio; falsable con datos publicados. Ejemplo de la hoja: «Ventas FY2026 ≥ 17.000 mm». |
| B38 / B39 / B40 | Fecha de comprobación | fecha | 158 / 161 / 164 | no | C | 12–24 meses desde la fecha de análisis (S-9). |
| C38 / C39 / C40 | Probabilidad | decimal en [0, 1] | 159 / 162 / 165 | no | C | Probabilidad propia de cada predicción: la de que se cumpla **dado el escenario NORMAL** (no la probabilidad del escenario, `C69`). |
| C43 | Naturaleza del FCF base ≤ 0 (solo motor A) | `No aplica` / `Transitorio` / `Extraordinario` / `Estructural` | 166 | sí (si `Análisis!C52` ≤ 0) | A | Si `C52` > 0: `No aplica`. «Estructural» deja el motor A sin aplicar (L1): entonces B si la financiación lo permite; si no, `modelo_no_aplicable` con el cubo cualitativo (normalmente Demasiado difícil). |
| C44 | FCF base normalizado (mm) | número > 0 (solo con Transitorio/Extraordinario); si no, vacío | 167 | sí (condicional) | B | Cálculo documentado en N (qué años, qué se excluye y por qué). Hipótesis material para D10. |
| C47 | Causa declarada de la diferencia de capitalización | `Ninguna` / `ADR o ADS` / `Split o contrasplit` / `Básicas frente a diluidas` / `Fechas distintas` / `Otra (explicada en Control maestro)` | 170 | sí (si la desviación > `Diagnóstico V6!C91`) | A | Solo si la conciliación precio × acciones ≈ capitalización lo pide (`Diagnóstico V6!C91:C92`). Si no: `Ninguna`. Es una explicación, no una corrección. |

Celdas de `Palancas` que **no** escribe el v2: `C7` (sector de Damodaran: dato de fase 1 y bloqueante, S-10), `A28:B33` (reparto geográfico: fase 1), `C45`, `C46`, `C48` (fecha del precio, fecha de las acciones, moneda de cotización: metadatos de fase 1), `D38:D40` (resultado de las predicciones: José Luis, al vencer), `B17:D17`, `E14:J19`, `C28:D34` (fórmulas).

## A.3 Hoja `Diagnóstico V6` (2 celdas)

| Celda | Concepto | Valores | CM | Fase | Reglas |
|---|---|---|---|---|---|
| B222 | Incertidumbre material pendiente (una línea) | texto | — | C | La hipótesis de la lista `hipotesis_sin_fundamento` (D10, Anexo B §B.6) que más condiciona la conclusión, y lo que no se sabe de ella. Si la lista está vacía: la hipótesis fundamentada de la que más depende la conclusión según la fase C (el tornado `C221` es información, no criterio). |
| B223 | Qué dato o documento la resolvería | texto | — | C | Concreto: qué documento, qué cifra, qué pregunta a Relación con Inversores. En `pendiente_de_investigacion`, es lo que haría falta para continuar. |

## A.4 Filas de `Control maestro` que escribe el v2

Para cada celda de A.1 y A.2 (66 filas: 21–28, 30, 32, 49, 53, 56–59, 61–64, 66–69, 71, 72, 74, 76–82 y 137–167, 170):

- **E** («Estado de trabajo») = `Listo para auditoría`.
- **F** («Clasificación final») = `Estimación declarada` (D9). Nunca `Hipótesis confirmada`, nunca `Rellenado y verificado`.
- **N** («Observaciones») = la Observación con el formato del Anexo D (§D.3).
- **G, H, I, J, K, L, M**: no se tocan (para las filas de juicio están vacías o con la evidencia de fase 1; esa evidencia se conserva).

Las filas 60, 65 y 70 (`B67:D67`, automáticas en V6.3) no las escribe el v2. `migrate_values.py` copia en su columna N las Observaciones que el v1 escribió sobre el crecimiento del FCF; `migrar_v53_a_v63.py` les antepone «HEREDADO · V5.3 (fórmula en V6.3): » para que no se lean como justificación vigente (S-16).

## A.5 Recuento

34 (`Análisis`) + 32 (`Palancas`) + 2 (`Diagnóstico V6`) = **68 celdas**. De ellas, condicionales: `C76` (solo motor A), `B16:D16` (no en C), `C22`/`C23` (solo con apalancamiento), `C24` (solo con cifra), `C43`/`C44` (solo con FCF base ≤ 0), `C47` (solo si la conciliación lo pide), `C10` (solo con `C9` = Sí). Una celda condicional que no aplica se deja según su regla (vacía o `No aplica`) **y su fila de Control maestro se documenta igual**.

El script `comprobar_celdas_v2.py` comprueba: vocabulario exacto; números bien formados; probabilidades de la lista y suma 1; g para siempre de la lista y < tasa de descuento del motor; ROIC > g; S2C > 0 (A, B); `C76` ≤ `C53` y vacío en B/C; `C22` en [0, 1]; `C23` ≥ 0; tres predicciones con texto, fecha y probabilidad; `B66:D66` no vacías; `C104` empieza por «Pendiente de decisión de cartera» y no contiene ningún porcentaje ni el símbolo «%» (D16); 66 filas de Control maestro con E, F y N; ninguna celda fuera de las 68 cambiada respecto al libro de entrada (salvo las que `rellenar_fase1_v63.py` rellenó por convención antes de la fase A: `C51`, `C56`). Cualquier incumplimiento es un **error** (D17): se corrige o el análisis termina en `no_entregable`. En los estados sin fase B o sin fase C (`modelo_no_aplicable` tras la fase A, `pendiente_de_datos` tras ella) comprueba solo las celdas que la fase escrita decidió y sus filas.
