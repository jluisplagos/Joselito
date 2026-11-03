# Kit del pipeline «personaje Munger» — cómo usarlo

Tres pasos:

1. **Prepara el primer lote.** Una carpeta por empresa con su Excel (parte automática rellena; si trae también tus juicios, llámalo `<Empresa>_mia.xlsx`) y sus PDF (informes anuales y semestral). Comprime las carpetas en `lote_01.zip`. Empieza por 5 empresas.
2. **Abre una conversación nueva** en Claude con Opus 5.5 y esfuerzo Alto. Adjunta `kit_pipeline_munger.zip` y `lote_01.zip`.
3. **Pega el texto de `PROMPT_INICIAL.md`** (lo que hay debajo de la línea) como primer mensaje.

Claude leerá `CONTEXTO.md` (incluida la sección 10, con lo aprendido en el lote 01), hará la primera empresa entera, te enviará su Excel evaluado y su respuesta, y seguirá con las demás. Tú no ejecutas nada.

Qué hay dentro:

- `CONTEXTO.md` — lo que la ventana nueva necesita saber: decisiones, archivos, hechos de la plantilla, procedimiento paso a paso, qué entregar, qué medir.
- `PROMPT_INICIAL.md` — el primer mensaje.
- `personaje_munger_v1.md`, `instrucciones_proyecto_B.md`, `trazabilidad.md`, `munger.md` — el procedimiento, su resumen, su evidencia y el corpus.
- `prompts/` — los tres agentes (extracción, juicio, verificación).
- `esquema/juicio.ejemplo.json` — formato de la respuesta del agente de juicio.
- `scripts/` — escritura y verificación del Excel, extracción de PDF, recálculo, resumen. Probados con el Excel de Hermès.

Si más adelante prefieres el Claude Code de terminal con tus créditos, este mismo kit sirve: los scripts y los prompts no cambian.
