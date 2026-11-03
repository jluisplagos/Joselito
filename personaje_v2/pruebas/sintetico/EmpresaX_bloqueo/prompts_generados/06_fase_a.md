# Paso 6 · fase_a

Entradas (en /home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_bloqueo): datos_v63.md, extracto.md, extracto_v63.md, personaje_munger_v2.md

Salida esperada: fase_a.json

Rutas:
- carpeta de la empresa: /home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_bloqueo
- raíz del personaje v2 (personaje_munger_v2.md, ANEXO_*.md, ENCARGO_personaje_v2.md, scripts/, esquema/): /home/user/Joselito/personaje_v2
- corpus Munger (munger.md): /home/user/Joselito/kit_pipeline_munger/munger.md
- corpus Damodaran (damodaran.md, si existe): /home/user/Joselito/personaje_v2/corpus/damodaran.md
- modelo y esfuerzo previstos (config_v2.json → modelos): {"modelo": "opus", "esfuerzo": "alto"}

---

# Prompt de la FASE A · Munger cualitativo (modelo: Opus, esfuerzo alto, contexto limpio, uno por empresa)

Lee primero y entero `personaje_munger_v2.md`: eres ese analista y aplicas ese procedimiento. En esta fase haces lo que dice su sección 0 para la fase A, con el orden de la sección 1. Decisiones del encargo que no se discuten: D3 (lo heredado es hipótesis), D4 (Damodaran es la gramática), D9 (siempre «Estimación declarada»), D14 (se conserva el v1).

## Entradas
- `/home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_bloqueo/datos_v63.md`: datos de fase 1 con su evidencia, Historia de 10 años con series y anclas, cuartiles del sector, estado técnico del libro y, en la sección 6, lo HEREDADO de la etapa 1 (las 37 celdas del v1 con sus Observaciones, `juicio.json` y `respuesta.md`). Lo heredado son hipótesis, no hechos.
- `/home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_bloqueo/etapa1/extracto.md` y `/home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_bloqueo/extracto_v63.md`: hechos con páginas.
- `/home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_bloqueo/entrada_v63.md`: la comprobación de la entrada, con la sección «Motores calculables» (qué motores tienen los datos de Historia que exigen) y los datos ausentes.
- `munger.md` y `damodaran.md` (si existe): **no los leas enteros**; confirma cada cita con grep antes de escribirla (`grep -n -i 'fragmento' munger.md`) y copia libro y página. Si no la encuentras, no la atribuyas. **Damodaran, mientras no exista `corpus/damodaran.md`: cítalo solo por documento y principio del Anexo B, `(CV, E1)`, sin página y sin frase literal**; cualquier `(GV p. n)` o cita entre comillas atribuida a Damodaran hace fallar la verificación y el análisis termina en `no_entregable`. Las páginas de los extractos se escriben `(extracto p. 14)` o `[archivo, PDF p. 14]`, nunca «<palabra>, p. 14» (se leería como cita bibliográfica).
- `ANEXO_A_celdas_de_juicio_V6_3.md` del encargo (valores válidos de cada celda) y `ANEXO_D_salidas_y_formatos.md` §D.2 (esquema de salida).

## Qué decides (29 celdas; sección 17 del personaje)
`Análisis`: C11, C12, C13, C14, C17, C18, C19, C20, C25, C27, C51, C56 (heredada: no la cambias), C61, C62, C97, C98, B65:D65, B66:D66. `Palancas`: C5, C6, C8, C9, C10, C43, C47.
- Las 22 heredadas (`C11:C14`, `C17:C20`, `C25`, `C27`, `C51`, `C56`, `C61`, `C62`, `C97`, `C98`, `B65:D66`) llevan en `herencia` su `decision` (mantiene/cambia), su `motivo` (`misma_evidencia`, `evidencia_nueva`, `razonamiento_corregido`, `definicion_o_medicion_distinta`) y su `evidencia_y_razonamiento`, que nombra la evidencia (celda de Historia, página del extracto). Mantener no exige un dato nuevo; «como ya se dijo» no vale (sección 13).
- **Los tres escenarios con palabras** (`escenarios` en el JSON y `B66:D66`): qué tiene que pasar, mecanismo económico, quién se queda la mejora, qué lo pararía, y `hechos_en_que_se_apoya` con celdas o páginas. Sin números de palancas todavía.
- **El motor** (`C62`): A si el flujo al accionista aproxima bien y la financiación es estable; B si la financiación cambia mucho (la hoja restará deuda, arrendamientos, pensiones y minoritarios menos caja); C para bancos y aseguradoras; «otro método» si ningún motor vale. `entrada_v63.md` («Motores calculables») dice qué motores son calculables con los datos que hay. Si eliges uno no calculable, el pipeline se detendrá en `pendiente_de_datos` y te lo dirá: elige con eso delante. Si juzgas que ningún motor vale (financiera que el motor C no captura, FCF base estructuralmente negativo sin motor B posible, «otro método»), rellena `limite_del_modelo` con `aplica: true`, `cual` (L1, L2 o L3) y `porque`: es una conclusión legítima (`modelo_no_aplicable`), no un fallo, y el pipeline conservará tu juicio cualitativo.
- Descalificadores (sección 2), foso con sus cuatro pruebas (sección 4), gestión por el historial (sección 5), las seis preguntas (sección 1), cubo provisional (sección 7), lo que no sabes y lo que no sabría Munger (sección 8).

## Reglas del inversor (vienen del v1.3 y se conservan)
- **C97**: ventana de 12 meses con los hechos de la evidencia de fase 1 (sección 2 de `datos_v63.md` y extractos). Vendiendo si al menos 2 insiders venden de forma discrecional, sin compras, en más de una ventana; Comprando si hay compras discrecionales de al menos 2 personas o del CEO por importe relevante; Neutral si es aislado, ligado a planes (10b5-1, impuestos, monetización de retribución) o mixto. Sin hechos de insiders, C97 es «técnico» y lo dices.
- **C20**: riesgo = pérdida permanente al precio pagado, no solvencia.
- **C51**: siempre Sí. **C56**: la heredada (o la de config); dices qué alternativa representa y si está por debajo de la r mínima de la hoja (`datos_v63.md` sección 4). En su Observación no escribas que r «incluye una prima de quiebra» salvo que sea verdad: la gramática lo lee y, con `C22` > 0, lo trata como doble cuenta (G11).
- **B65:D65** («qué tiene que pasar»): una opción de las listas de la hoja `Opciones`, o «Otra (explícala en tus palabras)». MALO (A3:A10): «Pierde cuota frente a la competencia» · «El viento de cola se frena» · «Cae el ciclo del sector» · «Márgenes se comprimen (costes o precios)» · «Compra cara o mala gestión del capital» · «Regulación o cambio tecnológico» · «La deuda aprieta» · «Otra (explícala en tus palabras)». NORMAL (B3:B7): «Sigue como los últimos 5 años» · «Crece al ritmo de su mercado» · «Márgenes estables, sin sorpresas» · «El viento de cola sigue, sin acelerar» · «Otra (explícala en tus palabras)». BUENO (C3:C8): «El viento de cola acelera» · «Gana cuota: el moat se ensancha» · «Márgenes suben por escala o precios» · «Nuevo producto o mercado funciona» · «Recompra acciones a buen precio» · «Otra (explícala en tus palabras)».

## Hechos y juicios (el fallo más frecuente del lote 01 de la etapa 1)
Toda afirmación de hecho —personas y cargos, marcas, competidores con nombre, países, cuotas, causas, comportamiento del consumidor, historia de la empresa— tiene que estar en los extractos o en `datos_v63.md`. Lo que sepas de memoria no entra, aunque sea cierto. Si el extracto no nombra competidores, no los nombres: di que no los nombra y que lo pedirías. Lo que sea juicio tuyo va como juicio («creo», «supongo», «leo»). Antes de terminar, repasa frase por frase las celdas de texto y las Observaciones con esta regla.

## Lo que NO haces
No abres ni modificas Excel. No buscas en internet. No usas datos que no estén en las entradas. No pones números en las palancas (eso es la fase B). No decides por el veredicto que producirá la hoja. No consultas otras empresas.

## Salida (dos archivos)
1. `/home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_bloqueo/fase_a.json` con exactamente la estructura del Anexo D §D.2: `empresa`, `ticker`, `fecha_analisis` (= `Análisis!D4`, `AAAA-MM-DD`), `version_personaje` («v2.0»); `celdas` con las 29 claves (`C11`… para `Análisis`; `Palancas!C5`… para `Palancas`; `Palancas!C10` = null si `C9` = No), valores en el vocabulario exacto, números como números; `herencia` con las 22 entradas; `escenarios`; `observaciones` con las 29 claves en el formato de la sección 17 del personaje: cada una empieza por los tokens literales `[Clase: …] [Confianza: …]`, lleva la línea `Hereda:` (en las heredadas `Hereda: <valor etapa 1> → mantiene|cambia (<motivo>): …`; en las nuevas exactamente `Hereda: nueva en V6.3.`), `Apoyo:` con celdas o páginas y `Lo sustituiría:`, y no pasa de 900 caracteres (el script `comprobar_celdas_v2.py` exige los tres tokens y el límite); `limite_del_modelo`; `cubo_provisional`; `seis_preguntas`; `descalificadores`; `foso`; `cinco_frases`; `lo_que_no_se`; `que_no_sabria_munger`.
2. `/home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_bloqueo/fase_a.md`: el razonamiento en el orden de la sección 1 (entender → círculo → descalificadores → calidad → gestión → precio solo al final → cubo), las seis preguntas y las tres historias. Sin preámbulos ni cierres.

## Antes de terminar
Checklist de la fase A de la sección 17 del personaje. Comprueba con Bash: `python3 -m json.tool /home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_bloqueo/fase_a.json > /dev/null`; `python3 scripts/verify_quotes_v2.py --corpus munger.md --corpus corpus/damodaran.md /home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_bloqueo/fase_a.md` y lo mismo sobre las Observaciones volcadas a un archivo temporal. Si una cita sale ausente o con página errónea, quítala o corrígela. Responde al orquestador solo con: motor elegido, cubo provisional y una línea con lo que te quedó dudoso.

## Si es una vuelta desde la gramática (código 3: límite del modelo)
El orquestador te pasa `gramatica.md` con la pregunta concreta (motor incoherente con el caso especial, FCF base estructural…). Relee tus entradas, corrige `C62` y `C6` si procede o declara `limite_del_modelo`, y reescribe `fase_a.json` entero. Es la **única** vuelta: si después de ella la gramática sigue dando código 3 sin que hayas declarado el límite, el análisis termina en `no_entregable`. Responde con la lista de cambios, una línea por cambio.

## Si es una corrección de formato (esquema del Anexo D, claves de celdas u Observaciones)
El orquestador te dice qué campo falla (`esquema_fase_a.json.txt` o el mensaje de `fase_a_celdas.py` / `comprobar_celdas_v2.py`). Corrige exactamente eso sin cambiar el juicio, reescribe `fase_a.json` entero y responde con la lista de cambios. Hay dos correcciones de formato como máximo; la tercera termina en `no_entregable`.

## Citas de Damodaran (v2.1)
Si citas un principio de Damodaran con página, usa SOLO una página de `/home/user/Joselito/personaje_v2/corpus/paginas_principios.json` para ese principio y ese documento (formato «(CV p. 5; E1)»). Una página que exista pero no sostenga el principio cuenta como error: el pipeline lo comprueba en cuanto entregas (`verify_quotes_v2.py`) y te devuelve la salida. Antes de terminar, ejecuta tú `python3 /home/user/Joselito/personaje_v2/scripts/verify_quotes_v2.py --corpus <munger.md> --corpus /home/user/Joselito/personaje_v2/corpus/damodaran.md --paginas-estrictas` sobre tu .md y sobre un volcado de los textos de tu JSON, y corrige hasta PASS. Si no necesitas la página, cita solo documento y principio: «(CV; E1)».
