# CONTEXTO — pipeline «personaje Munger» para 50 empresas

Este archivo es para la ventana nueva que va a orquestar el trabajo. Lo que no esté aquí no se da por sabido.

## 1. Qué estamos haciendo

José Luis (español; Europe/Amsterdam) tiene una plantilla Excel propia, «Hoja de evaluación de empresas V5.3» (DCF simplificado a 3 escenarios), y 50 empresas con la parte automática ya rellena. Ha construido un **procedimiento** —no un personaje que imite a Munger— que aplica la forma de decidir de Charlie Munger a las **37 celdas de juicio** de la plantilla. Ese procedimiento es `personaje_munger_v1.md`, trazado regla por regla a `munger.md`, un corpus de 1.899 entradas con cita de libro y página sacadas de cuatro libros (Damn Right!; Poor Charlie's Almanack; The Complete Investor; All I Want to Know). `trazabilidad.md` documenta la evidencia de cada regla. Es un ejercicio: nadie invierte con esto.

Objetivo de esta ventana: pasar las 50 empresas por el procedimiento, una tras otra, cada una con contexto limpio, dejar para cada una el Excel evaluado y la respuesta, verificarlo todo y acumular un resumen. Después, él compara las respuestas del procedimiento con las suyas.

## 2. Decisiones ya tomadas (no se reabren)

1. Es un procedimiento, no una imitación de estilo. Habla en primera persona como analista, en español, frases cortas.
2. Cuatro cubos: Sí / Vigilar / No / Demasiado difícil. Difícil ≠ No.
3. Ninguna celda de juicio queda vacía. Nunca. Vocabulario exacto de los desplegables.
4. La postura va en Control maestro → columna N (Observaciones), una fila por celda de juicio. La hoja Análisis solo recibe los valores. **La plantilla no se modifica**: ninguna fórmula, ninguna estructura.
5. Las celdas de datos (parte automática) se usan tal cual; no se recalculan ni se cambia la base del FCF (C52).
6. Datos de mercado solo los que vengan en el Excel. Nada de internet.
7. Citas a Munger solo con libro y página confirmadas en munger.md; si no hay entrada, no se atribuye.
8. Las convenciones del ejercicio (20/60/20, terminal 1–3 %, r = 0,09 si falta, precio de Sí = mín(B78, 0,75·C83)) se aplican y se declaran como convención.
9. Modelos: la ventana orquestadora en Opus 5.5 · Alto. Agentes: extracción con Sonnet (esfuerzo medio); juicio con Opus (esfuerzo alto); verificación con Opus (esfuerzo medio) y sin haber visto el trabajo.
10. Él no es programador. No se le pide ejecutar comandos ni instalar nada. Prefiere respuestas cortas, sin explicaciones largas, con el resultado primero.

## 3. Archivos del kit

| Archivo | Para qué |
|---|---|
| `personaje_munger_v1.md` | El procedimiento completo con evidencia. Lo lee entero el agente de juicio. |
| `instrucciones_proyecto_B.md` | Resumen de 6.700 caracteres de lo que no se puede incumplir. Lo lee el agente de juicio junto al procedimiento. (Es también el texto de las Instrucciones del Proyecto B de claude.ai, la vía manual anterior; para este pipeline no hace falta tocarlo.) |
| `trazabilidad.md` | Regla → entradas del corpus, descartes, convenciones. Referencia; no hace falta leerlo para ejecutar. |
| `munger.md` | Corpus (1 MB). Solo se consulta con grep; nunca se carga entero en un agente. |
| `prompts/extraccion.md`, `prompts/juicio.md`, `prompts/verificacion.md` | Prompts de los tres agentes. Se preparan con `scripts/preparar_prompt.py` (sustituye `{EMPRESA}`, `{CARPETA}`, `{LISTA_DE_DOCUMENTOS}`). Tras el lote 01 incluyen las reglas de hechos/juicios, el formato de citas, las comprobaciones propias y el modo corrección. |
| `esquema/juicio.ejemplo.json` | Estructura exacta del JSON que devuelve el agente de juicio. |
| `scripts/cells.py` | Las 37 celdas, vocabularios de los desplegables (leídos de la plantilla), localización de filas en Control maestro. |
| `scripts/extract_pdf_text.py` | PDF → .txt con marcas `[PDF PAGE n]`. |
| `scripts/pending_decisions.py` | Paso 0: lista lo que falta decidir en la parte automática (bloqueante o no). |
| `scripts/apply_decisions.py` | Paso 0: escribe las respuestas del inversor en celdas de datos y las registra en Control maestro. |
| `scripts/blank_judgment.py` | Copia del Excel con las 37 celdas y sus Observaciones en blanco (si el Excel trae los juicios del inversor). |
| `scripts/recalc.sh` | Recalcula con LibreOffice a una carpeta `recalc/`. La copia recalculada es solo para leer valores. |
| `scripts/dump_data_cells.py` | Celdas automáticas + Base financiera → `datos_automaticos.md` para el agente de juicio. |
| `scripts/fill_excel.py` | Escribe `juicio.json` en una copia del Excel: 37 celdas + 37 Observaciones. Nada más. |
| `scripts/verify_excel.py` | Integridad de fórmulas, vocabulario, sumas, Observaciones, A6, precio de Sí. Código de salida 0/1. |
| `scripts/verify_quotes.py` | Cada cita a Munger existe en munger.md con su página. |
| `scripts/append_summary.py` | Fila en `resumen.csv`; con `--mi-excel` cuenta las celdas distintas a las del inversor. |
| `scripts/add_cached_values.py` | (Añadido tras el lote 01.) Guarda en el Excel evaluado el resultado de cada fórmula, leído del recalculado. Sin esto, la vista previa, el móvil y la Vista protegida de Excel muestran vacíos el valor por escenario (B78:D78), el ponderado, los márgenes y A6. No toca fórmulas ni estructura. |
| `scripts/preparar_prompt.py` | (Añadido tras el lote 01.) Prepara el prompt de un agente para una empresa: sustituye los marcadores y pone rutas absolutas. |
| `scripts/paso6.sh` | (Añadido tras el lote 01.) El paso 6 entero en una orden, con resultado PASS/FAIL. |
| `scripts/xhtml_to_text.py` | (Añadido tras el lote 01.) Informes xhtml (ESEF/SEC) → .txt con marcas `[PDF PAGE n]`; añade filas a `textos_index.md`. Se ejecuta después de `extract_pdf_text.py`. |

Dependencias: Python 3 con openpyxl, pypdf, lxml y beautifulsoup4; `pdftotext` (poppler); LibreOffice (`soffice`). Todo está en el entorno de Claude en la nube; si falta algo, `pip install openpyxl pypdf lxml beautifulsoup4 --break-system-packages`.

## 4. Hechos de la plantilla que los scripts dan por supuestos

- Hojas: `Análisis`, `Guía Simply Wall St`, `Opciones`, `Control maestro`, `Base financiera`.
- 37 celdas de juicio en Análisis: C11 C12 C13 C14 C17 C18 C19 C20 C25 C27 C51 C56 C61 C62 B65 C65 D65 B66 C66 D66 B67 C67 D67 B68 C68 D68 B69 C69 D69 C76 C93 C97 C98 B101 B102 C103 C104.
- Celdas de datos: B3 D3 B4 D4 C24 C26 C28 C31–C34 C37 C40–C42 C46–C50 C52–C55 C57 C60 C88 C96. C52 (FCF base) es fórmula que depende de C51: con C51 = Sí, C52 = C46 − C47 − C48 − C49 − C50.
- A6 (veredicto automático): `DESCARTAR · demasiado difícil` si alguna de C11:C13 es No; si no, depende del margen del DCF. B78/C78/D78 = valor por acción malo/normal/bueno; C83 = valor ponderado; C85 = asimetría malo/bueno.
- Control maestro: columna B tiene la referencia (`Análisis!C11`), columna N las Observaciones. Hay dos versiones del libro: la plantilla vacía (14 columnas, 102 filas) y la versión de trabajo de José Luis (15 columnas con `Tipo R/C/M/S`, 108 filas). Los scripts localizan las filas por la columna B y funcionan con las dos. En la plantilla vacía, la columna N trae textos de guía en algunas filas: se sobrescriben con la postura, como hace él.
- Desplegables con error activado (valor obligatorio): C11–C13, C17–C19, C25, C103, C51 (Sí/No); C14 (Compounder / Calidad a precio razonable / Deep value / especial / Cíclica / commodity / Turnaround / situación especial); C20 (Incert. alta + riesgo bajo / Ambos bajos / Riesgo real alto); C27 (Expandiendo / Estable / Comprimiendo); C97 (Comprando / Neutral / Vendiendo); C98 (Buena / Aceptable / Dudosa); C61 (Sí / No / No está claro); C62 (Sí / No · financiación cambia mucho / No · este tipo de empresa requiere otro método); C93 (Sí / No / No lo sé). Listas sugeridas sin error: B65/C65/D65 (hoja Opciones), B67/C67/D67, B68:D68 (0–0,03), B69:D69 (0,1–0,6), C56 (0,08–0,15).
- Precio de Sí (regla del ejercicio) = mín(B78, 0,75 × C83), leído del recalculado.

## 5. Cómo llegan las empresas

Un ZIP por lote con una carpeta por empresa: `lote_01/<Empresa>/` con el Excel (parte automática rellena; puede traer además los juicios del inversor) y los PDF (informes anuales, semestral). Si el Excel trae los juicios del inversor, se conserva como `<Empresa>_mia.xlsx` para la comparación y se trabaja sobre la copia en blanco. Alternativa: su ordenador enlazado con la app de escritorio; entonces se lee la carpeta directamente y se dejan los resultados al lado.

## 5 bis. Paso 0 del lote: una sola ronda de preguntas a José Luis

Antes de empezar cualquier empresa del lote:

1. Para cada empresa: `python3 kit/scripts/pending_decisions.py --excel empresas/<Empresa>/<Empresa>.xlsx --json empresas/<Empresa>/pendientes.json`. Lista las decisiones abiertas de la PARTE AUTOMÁTICA: celdas obligatorias vacías (C46, C47, C50, C37, C53, C55) y filas marcadas «Pendiente de inversor» en Control maestro. Las marca como BLOQUEANTES (sin ellas no hay FCF base) o no bloqueantes.
2. Reúne todas las del lote en **un único mensaje** a José Luis, agrupado por empresa. Para cada decisión, con el formato de su prompt (sección 7) pero en corto: celda; qué está en juego, en una línea; opciones con su cifra y su efecto (por ejemplo «3 años: FCF base 3.280 · 5 años: 3.550 · LTM: 1.417 (−57 %)»); tu recomendación con el motivo; y la pregunta. Usa la herramienta de preguntas de opción múltiple si está disponible (hasta 4 preguntas por llamada; varias llamadas seguidas si hacen falta).
3. Con sus respuestas: `python3 kit/scripts/apply_decisions.py --source <Empresa>.xlsx --out <Empresa>_listo.xlsx --set C46=… --set C47=… --set C50=… --nota "Decisión del inversor (fecha): …" --periodo "…"`. Escribe solo celdas de datos, registra la decisión literal en Control maestro y nunca toca celdas de juicio ni fórmulas. A partir de aquí, el Excel de trabajo es `<Empresa>_listo.xlsx`.
4. Si no contesta una decisión BLOQUEANTE, esa empresa se aparta y se sigue con las demás; se le recuerda al final del lote. Las no bloqueantes sin respuesta se dejan como están y se menciona en la Observación que corresponda.
5. Después de esta ronda, el lote corre entero sin más preguntas, salvo que algo no se pueda deshacer.

Otras reglas de entrada:
- Las celdas de juicio (incluidas C51 y C97) las rellena siempre el personaje, aunque en el Excel del inversor vengan rellenas o escaladas.
- Los informes pueden venir en PDF o en xhtml (ESEF/SEC). `extract_pdf_text.py` solo lee PDF; los xhtml se convierten con `xhtml_to_text.py`.
- Los ZIP pueden traer una carpeta raíz (`kit_pipeline_munger/`, `lote_01/`): se aplana para que queden `kit/scripts/…` y `empresas/<Empresa>/…`. El Excel del lote se copia como `empresas/<Empresa>/<Empresa>.xlsx` (el original se conserva). Si solo trae C97 rellena y ningún otro juicio, no se crea `_mia`.
- Después del paso 0, el Excel de trabajo es `<Empresa>_listo.xlsx`: es el `--source` de `fill_excel.py` y de `verify_excel.py` (en la sección 6, donde pone `<Empresa>.xlsx` léase `<Empresa>_listo.xlsx` si existe).
- «Máximo dos intentos» (paso 8) = dos correcciones después del primer juicio (lectura aplicada en el lote 01).

## 6. Procedimiento por empresa (en este orden; cada paso deja un archivo)

```
EMP=empresas/<Empresa>   # carpeta de trabajo; el ZIP del lote se descomprime aquí
1. Si el Excel trae juicios: python3 kit/scripts/blank_judgment.py --source $EMP/<Empresa>_mia.xlsx --out $EMP/<Empresa>.xlsx
2. python3 kit/scripts/extract_pdf_text.py --folder $EMP --outdir $EMP/texto
   python3 kit/scripts/xhtml_to_text.py --folder $EMP --outdir $EMP/texto      # solo si hay xhtml
3. Agente EXTRACCIÓN (Sonnet) con prompts/extraccion.md  → $EMP/extracto.md   (≤ 25.000 palabras; comprobar wc -w)
4. bash kit/scripts/recalc.sh $EMP/<Empresa>_listo.xlsx $EMP/recalc        # (o <Empresa>.xlsx si no hubo paso 0)
   python3 kit/scripts/dump_data_cells.py --recalc $EMP/recalc/<Empresa>_listo.xlsx --out $EMP/datos_automaticos.md
5. Agente JUICIO (Opus, alto) con prompts/juicio.md  → $EMP/juicio.json y $EMP/respuesta.md
6. bash kit/scripts/paso6.sh <Empresa>
   (hace todo el paso 6: fill_excel → recalc → verify_excel → verify_quotes sobre respuesta.md y sobre las Observaciones
    → add_cached_values, OBLIGATORIO porque sin él los valores se ven vacíos; escribe verificacion_excel.txt y
    verificacion_citas.txt y termina con «PASO6: PASS» o «PASO6: FAIL»)
7. Agente VERIFICACIÓN (Opus, medio, contexto limpio) con prompts/verificacion.md → $EMP/auditoria.md
8. Si auditoría = REPETIR o algún script = FAIL: corregir con el agente de juicio (nuevo contexto, con la lista de fallos) y repetir 6–7. Máximo dos intentos; si sigue fallando, se marca y se sigue.
9. python3 kit/scripts/append_summary.py --csv resumen.csv --json $EMP/juicio.json --recalc $EMP/recalc/<Empresa>_evaluada.xlsx \
       --verificacion PASS|FAIL [--mi-excel $EMP/<Empresa>_mia.xlsx]
10. Entregar a José Luis: <Empresa>_evaluada.xlsx (el escrito por fill_excel.py y completado con add_cached_values.py, NO la copia recalc), respuesta.md y, al cerrar el lote, resumen.csv.
```

Varias empresas pueden ir en paralelo (3–5 agentes de juicio a la vez); cada agente ve solo su carpeta. Nunca se reutiliza el contexto de una empresa para otra.

## 7. Qué se entrega y cómo

- Por empresa: `<Empresa>_evaluada.xlsx` y `<Empresa>_respuesta.md`, enviados en cuanto pasan la verificación (no al final del lote).
- Por lote: `resumen.csv` y tres líneas: cuántas pasaron a la primera, cuántas se repitieron, cuántas quedaron marcadas, y reparto de cubos.
- Lo que falló y por qué, en una línea por empresa. Sin recapitular pasos.

## 8. Qué medir en el primer lote (5 empresas)

Tiempo por empresa, palabras del extracto, intentos de juicio por empresa, fallos de verificación más frecuentes, y si el límite de uso del plan frena el ritmo. Con eso José Luis decide si siguen aquí los 45 restantes o si se pasa el kit al Claude Code de terminal (los scripts y prompts son los mismos; solo cambia quién lanza los agentes).

## 9. Hermès como caso de calibración

Hermès ya tiene: la respuesta de José Luis (precio 1.294,50 €, r 9 %, crecimientos 3/8/13 %, terminal 2/2,5/3 %, probabilidades 15/65/20, C76 = 8.000, valor ponderado 1.058 €, A6 «SIN MARGEN»), y tres respuestas del procedimiento v0 (A sin corpus, B1 y B2 con corpus). Con la regla de v1 y los números de José Luis, el precio de Sí de Hermès es ≈ 686 € (manda el escenario malo). Si Hermès entra en el primer lote, sirve para comprobar que v1 reproduce eso.

## 10. Cómo lanzar los agentes (aprendido en el lote 01)

```
mkdir -p prompts_listos
python3 kit/scripts/preparar_prompt.py --tipo extraccion   --empresa "<Nombre de B3>" --carpeta empresas/<Empresa> --out prompts_listos/extraccion_<Empresa>.md
python3 kit/scripts/preparar_prompt.py --tipo juicio       --empresa "<Nombre de B3>" --carpeta empresas/<Empresa> --out prompts_listos/juicio_<Empresa>.md
python3 kit/scripts/preparar_prompt.py --tipo verificacion --empresa "<Nombre de B3>" --carpeta empresas/<Empresa> --out prompts_listos/verificacion_<Empresa>.md
```
(la extracción se prepara después del paso 2, para que la lista de documentos esté completa)

Cada agente se lanza con la herramienta de agentes (tipo general-purpose), con modelo y esfuerzo de la decisión 9 (extracción: sonnet/medium; juicio y corrección: opus/high; verificación: opus/medium), y con este mensaje: «Lee entero y sigue al pie de la letra el prompt de <ruta absoluta del prompt preparado>. Es tu único encargo: <Empresa>, carpeta <ruta absoluta>. Nada de internet.» Para una corrección, se añade: «Es un intento de corrección: la auditoría está en <carpeta>/auditoria_intentoN.md» (antes de relanzar la verificación, renombrar auditoria.md a auditoria_intentoN.md).

Lo que pasó en el lote 01 (Hermès, Jumbo, Nike; 3 de 3 aprobadas, las 3 en Vigilar):
- Tiempo por empresa: 25–45 min. Extracción 7–16 min; juicio 6–8 min; auditoría 1–2 min; cada corrección añade unos 5 min.
- Extracto: 7.000–11.000 palabras. Jumbo salió con 5.700 y le faltaban competencia y remuneración: se amplió. Revisar los extractos de menos de 8.000 palabras.
- Fallo más frecuente, y el único en el lote: el punto 10 de la auditoría (hechos de memoria que no estaban en el extracto). El prompt de juicio ya trae la regla para evitarlo.
- El límite de uso no frenó el ritmo con 2 empresas en paralelo.
- Paso 0: casi siempre son C46/C47/C49/C50 (periodo del FCF base: 3 años, 5 años o LTM) y C31. Recomendación por defecto: 3 años. C88 con P/(FCF−SBC), porque C51 = Sí.
- 25-oct-2026 · **kit v1.3**. Un barrido de las 39 empresas de los lotes 01–13 mostró que el personaje solo recibía el valor de las celdas de datos, no la evidencia de Control maestro, y por eso decía «no cuadra» o «sin dato» sobre cosas ya investigadas (sobre todo C97). Cambios: `dump_data_cells.py` vuelca también las columnas G–N de Control maestro (celdas de datos) y M–N (filas de juicio), y ya no pone 0 si faltan C46/C47/C50; `prompts/juicio.md` explica esa evidencia y trae la regla del inversor para C97; `prompts/verificacion.md` añade el punto 11; `verify_excel.py` avisa si r ≤ tasa sin riesgo (C57). Las 39 empresas anteriores se corrigen aparte (índice maestro en STOCKS v2).
- 18-oct-2026: `personaje_munger_v1.md` pasa a v1.2 con dos reglas del inversor: C20 mide el riesgo de pérdida permanente al precio pagado (no solo la solvencia), y C76 mira dónde clasifica la empresa los intereses cobrados y resta la caja comprometida. El lote 01 se hizo con la v1.1.
