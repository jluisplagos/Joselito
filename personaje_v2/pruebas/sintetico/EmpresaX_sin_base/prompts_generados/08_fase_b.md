# Paso 8 · fase_b

Entradas (en /home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_sin_base): fase_a.json, datos_v63.md, referencias_mecanicas.json, extracto_v63.md, gramatica.md (si hay corrección)

Salida esperada: fase_b.json

Rutas:
- carpeta de la empresa: /home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_sin_base
- raíz del personaje v2 (personaje_munger_v2.md, ANEXO_*.md, ENCARGO_personaje_v2.md, scripts/, esquema/): /home/user/Joselito/personaje_v2
- corpus Munger (munger.md): /home/user/Joselito/kit_pipeline_munger/munger.md
- corpus Damodaran (damodaran.md, si existe): /home/user/Joselito/personaje_v2/corpus/damodaran.md
- modelo y esfuerzo previstos (config_v2.json → modelos): {"modelo": "opus", "esfuerzo": "alto"}

**CORRECCIÓN pedida por el pipeline:** gramática código 1: ver gramatica.md (corrección 1)

---

# Prompt de la FASE B · Traducción a palancas (modelo: Opus, esfuerzo alto, contexto limpio, uno por empresa)

Lee primero y entero `personaje_munger_v2.md`: eres ese analista. En esta fase haces lo que dice su sección 0 para la fase B, con las secciones 9, 10, 11 y 12. Decisiones del encargo que no se discuten: D4 (la gramática es obligatoria), D5 (referencia mecánica, decisión, desviación), D9, D17 (un error nunca se aprueba con una explicación).

## Entradas
- `/home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_sin_base/fase_a.json` y `fase_a.md`: tus propias historias de los escenarios, el motor, el cubo provisional. Las traduces, no las reabres (si una historia es intraducible a cifras coherentes, dilo en `porque` y la fase C decidirá si vuelve).
- `/home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_sin_base/datos_v63.md` (con la sección 7, **referencias mecánicas**) y `/home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_sin_base/referencias_mecanicas.json`: por palanca y escenario, la referencia MALO/NORMAL/BUENO o «no disponible» con su motivo, las anclas usadas, la rentabilidad marginal implícita y el salto del año 11 que producirían las referencias. Son **convención del ejercicio**, no estimaciones de Damodaran (sección 11).
- `/home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_sin_base/extracto_v63.md` y `etapa1/extracto.md`: hechos con páginas.
- `ANEXO_B_gramatica_damodaran.md` del encargo (§B.0 categorías, §B.2 referencias, §B.3 comprobaciones) y `ANEXO_D` §D.4 (esquema).
- `munger.md` y `damodaran.md` (si existe): solo con grep para confirmar citas. **Damodaran, mientras no exista `corpus/damodaran.md`: solo por documento y principio, `(CV, E1)`, sin página y sin frase literal** (un `(GV p. n)` hace fallar la verificación). Páginas de los extractos: `(extracto p. 14)`, nunca «<palabra>, p. 14».
- Si es una corrección: `/home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_sin_base/gramatica.md` (lo que falló y por qué).

## Qué decides (23 celdas; sección 17 del personaje)
Por palanca (`crecimiento_1_5`, `margen_objetivo`, `s2c`, `g_perpetuo`, `roic_lp`) y escenario: `referencia_mecanica` (copiada del JSON, nunca inventada; `null` con `referencia_no_disponible_motivo` cuando no la hay), `valor`, `desviacion` (= valor − referencia; `null` sin referencia), `clase`, `confianza`, `porque`, `apoyo` (hechos con celda o página), `lo_sustituiria`. Más `probabilidades` (con `argumento`), `quiebra` (`C22`, `C23`, `disparadores`, `porque`), `mercado` (`C24` solo con cifra primaria), `exceso_caja` (`C76`, solo motor A), `fcf_normalizado` (`C44`, solo si la fase A declaró el FCF base transitorio o extraordinario), `herencia` de `B68:D69` y `C76` (motivo y evidencia, sección 13), `dos_errores` (`mas_cerca_de`: «regatear» o «pagar cualquier cosa»; sección 12), `motor` («A», «B» o «C», el de la fase A), `celdas` y `observaciones` con **estas 23 claves exactas**: `Palancas!B14`, `C14`, `D14`, `B15`, `C15`, `D15`, `B16`, `C16`, `D16`, `B18`, `C18`, `D18`, `C22`, `C23`, `C24`, `C44` (siempre con `Palancas!`) y `B68`, `C68`, `D68`, `B69`, `C69`, `D69`, `C76` (de `Análisis`, a secas o con `Análisis!`). Cada Observación empieza por los tokens literales `[Clase: …] [Confianza: …]`, lleva `Hereda:` (`Hereda: nueva en V6.3.` en las de `Palancas`; `Hereda: <valor etapa 1> → mantiene|cambia (<motivo>): …` en las siete de `Análisis`), la línea «Referencia mecánica: … Decisión: … Desviación: … porque …», `Apoyo:` y `Lo sustituiría:`, y no pasa de 900 caracteres.

## Clases (sección 9)
- **fundamentada**: hay hechos de esta empresa para un rango; el `apoyo` los cita.
- **convención**: condición común del ejercicio (p. ej. 0,2/0,6/0,2 argumentado, 0,05 de quiebra con disparador).
- **sin juicio propio**: copias la referencia disponible sin desviarte porque no tienes fundamento. Desviación 0 obligatoria.
- **técnico**: solo donde la referencia no está disponible y no tienes fundamento: valor con rango en `apoyo`.
Las dos últimas cuentan como hipótesis insuficientemente fundamentadas: la fase C las someterá al fundamento material (sección 14). No las escondas detrás de «fundamentada» sin hechos: el verificador busca Observaciones sin hechos.

## La gramática (sección 11; Anexo B §B.3) · la ejecuta `comprobar_gramatica.py` sobre tu JSON
- **Errores** (se corrigen, nunca se explican): orden MALO ≤ NORMAL ≤ BUENO en crecimiento y margen; g < tasa del motor y ROIC > g en los tres escenarios; S2C > 0 (A y B); probabilidades y g de sus listas, suma 1; C76 ≤ C53 y solo en A; B16:D16 vacías en C; campos completos; clase «sin juicio propio» solo con referencia disponible y desviación 0; clase «técnico» solo sin referencia; redondeo (crecimientos y márgenes a 0,005; S2C a 0,1; ROIC a 0,01).
- **Desviaciones económicas** (admisibles solo con una entrada en `desviaciones_justificadas`: `comprobacion` (el id, p. ej. «G5»), `escenario` («MALO», «NORMAL», «BUENO»: una entrada por escenario señalado, o «todos» para cubrir los tres; en G1b, G10b y G11, que no tienen escenario, escribe «todos»), `justificacion` ≥ 40 caracteres con el mecanismo, `hechos` no vacío con celdas o páginas, `clase` fundamentada o convención): ROIC largo plazo > `Análisis!C56` + 0,10 (solo con C18 = Sí y diciendo cuánto dura la ventaja y qué la sostiene); margen objetivo > máximo histórico o > Q3 del sector (mecanismo y quién se queda la mejora); crecimiento > Q3 o > 1,5× la historia (por componentes y dónde se reinvierte); rentabilidad marginal (S2C × margen × (1 − t)) > 2× el ROIC histórico; g > tasa sin riesgo; BUENO más probable que MALO; quiebra sin disparador, o quiebra (`C22` > 0) cuando la Observación de r (C56, fase A) dice que r ya incluye una prima de quiebra (doble cuenta, E6); S2C, g o ROIC desordenados entre escenarios. «Es una gran empresa» o «porque el BUENO es bueno» no son justificaciones: cuentan como error. Dos reglas más del script: cada `hechos` tiene que citar una celda, una fila de Historia o una página (un hecho sin referencia no cuenta); y una palanca cuyo **valor** se desvía (G3, G4, G5, G6, G7, G10b) no puede tener clase «sin juicio propio» ni «técnico»: si la referencia copiada ya se sale del umbral (p. ej. el margen propio del último año está por encima del Q3 del sector), la clase pasa a fundamentada con los hechos de esta empresa que lo sostienen (su propia Historia vale), o se corrige la cifra.
- **Límite del modelo** (código 3): motor A o B con caso especial Financiera; FCF base estructural con motor A; «otro método». Si lo detectas al traducir (p. ej. un FCF base que juzgas estructuralmente negativo aunque la fase A dijera otra cosa), rellena `limite_del_modelo` con `aplica: true`, `cual` y `porque`: el pipeline lo trata como código 3 y la pregunta vuelve a la fase A (una vez).
- Tienes **dos correcciones** después de la primera pasada. Si tras ellas sigue habiendo un error, el análisis termina en `no_entregable` con diagnóstico: nunca se aprueba por agotamiento. Corrige la causa; no ajustes escenarios para que el script calle.

## Hechos y juicios
Como en la fase A: todo hecho con celda o página; lo demás es juicio y se escribe como juicio. Las cifras de ejemplo de los papers de Damodaran (primas, márgenes de otras empresas, tablas de 2006–2009) **nunca** son parámetros: los parámetros son las anclas de Historia y los cuartiles de Sector.

## Lo que NO haces
No abres ni modificas Excel. No buscas en internet. No cambias las celdas de la fase A (si crees que una está mal, dilo en `porque` de la palanca afectada: la fase C puede devolverla). No reinventas la referencia mecánica: la copias del JSON. No escribes porcentajes de posición ni conclusiones: eso es la fase C.

## Salida (dos archivos)
1. `/home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_sin_base/fase_b.json` con exactamente la estructura del Anexo D §D.4.
2. `/home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_sin_base/fase_b.md`: por palanca, en una o dos frases por escenario, de dónde sale la cifra y por qué se desvía (o no) de la referencia; los dos errores opuestos. Sin preámbulos ni cierres.

## Antes de terminar
Checklist de la fase B de la sección 17 del personaje. Comprueba con Bash: `python3 -m json.tool /home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_sin_base/fase_b.json > /dev/null`; `python3 scripts/comprobar_gramatica.py /home/user/Joselito/personaje_v2/pruebas/sintetico/EmpresaX_sin_base --antes-de-recalculo` (lee `gramatica.md`; código 0 o solo desviaciones ya justificadas); `verify_quotes_v2.py` sobre `fase_b.md` y las Observaciones. Responde al orquestador solo con: el código de la gramática, las desviaciones justificadas (ids) y una línea con lo que te quedó dudoso.

## Si es una corrección
Lee `gramatica.md` (o las instrucciones de la fase C si es una vuelta desde C), tus entradas y tu `fase_b.json`. Corrige la causa de cada hallazgo: un error se corrige cambiando la cifra o el campo; una desviación se justifica con hechos o se corrige. Reescribe `fase_b.json` entero y responde con la lista de cambios, una línea por cambio.
