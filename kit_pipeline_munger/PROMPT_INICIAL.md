# Texto para pegar como primer mensaje en la ventana nueva (Opus 5.5 · esfuerzo Alto)

Adjunta en ese mismo mensaje: `kit_pipeline_munger.zip` y el ZIP del primer lote (`lote_01.zip`, una carpeta por empresa con su Excel y sus PDF).

---

Vamos a pasar 50 empresas por un procedimiento de análisis a lo Munger que ya está construido. Todo lo que necesitas saber está en el ZIP `kit_pipeline_munger.zip`: empieza por `CONTEXTO.md` y léelo entero antes de hacer nada; después `prompts/`, `scripts/` y `esquema/`. No reabras decisiones que ahí figuran como tomadas.

Pasos:
1. Descomprime el kit en `kit/` y el lote en `empresas/`. Comprueba que los scripts corren (`python3 kit/scripts/verify_excel.py --help`) y que `soffice` y `pdftotext` existen.
2. Haz el paso 0 de la sección 5 bis: revisa la parte automática de todas las empresas del lote y hazme en un solo mensaje todas las preguntas que falten, con tu recomendación. Aplica mis respuestas.
3. Haz la primera empresa del lote completa, paso a paso según la sección 6 de CONTEXTO.md, y mándame su Excel evaluado y su respuesta.md en cuanto pasen la verificación. Dime en tres líneas qué midió: tiempo, palabras del extracto, intentos.
4. Si la primera sale bien, sigue con las demás del lote, hasta 3 en paralelo, y envía cada una cuando pase. Al terminar el lote, `resumen.csv` y el balance en tres líneas.
5. Si algo te obliga a elegir entre dos lecturas razonables, elige, dilo en una línea y sigue. Solo me preguntas si una decisión no se puede deshacer.

Yo no ejecuto comandos ni instalo nada: lo haces tú aquí. Respuestas cortas, resultado primero.
