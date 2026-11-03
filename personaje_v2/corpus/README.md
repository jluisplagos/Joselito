# corpus/ · Damodaran (pieza 3 del encargo, §6.1 y Anexo B)

Estado (3-nov-2026): **corpus construido** con los siete PDF (203 citas literales verificadas; ver `trazabilidad_damodaran.md`).
contenedor solo admite registros de paquetes y GitHub) y la lectura web de este chat no devuelve el texto literal con páginas, así que
el corpus no se puede construir sin los archivos. Plan B del encargo (§0.2c): José Luis adjunta los PDF.

| Código | Documento | Archivo esperado en `corpus/pdf/` |
|---|---|---|
| NN | Numbers and Narrative: Modeling, Story Telling and Investing | `narrative&numbers.pdf` |
| GV | Growth and Value: Past Growth, Predicted Growth and Fundamental Growth (2008) | `growthorigins.pdf` |
| MR | Return on Capital (ROC), ROIC and ROE: Measurement and Implications (2007) | `returnmeasures.pdf` |
| CV | Closure in Valuation: Estimating Terminal Value | `termvalue.pdf` |
| PA | Probabilistic Approaches: Scenario Analysis, Decision Trees and Simulations | `probabilistic.pdf` |
| UD | Ups and Downs: Valuing Cyclical and Commodity Companies (2009) | `commodity.pdf` |
| FS | Valuing Financial Service Firms (2009) | `finfirm09.pdf` |

Cuando estén los PDF:

1. `python3 scripts/construir_corpus_damodaran.py --pdf corpus/pdf --out corpus/texto` → un `.txt` por documento con marcas `[PDF PAGE n]` y un índice.
2. Lectura por bloques de páginas (agente de lectura, Sonnet, o la ventana de claude.ai) y entradas en `corpus/damodaran.md` con el formato de `munger.md`:
   `- **<sección>** — *<principio en una línea>.* "<cita literal>" (<Título corto completo>, p. <n>)`.
   El título corto va completo (es lo que lee `cit_corpus_re` de `verify_quotes_v2.py`): «Growth and Value», no «GV».
3. `corpus/trazabilidad_damodaran.md`: para cada principio [I] y [E] del Anexo B §B.0 y cada comprobación que lo invoca, documento y página. La plantilla está ya escrita con las páginas en blanco.
4. `python3 scripts/verify_quotes_v2.py --corpus <munger.md> --corpus corpus/damodaran.md <textos>` → PASS.

Lo que ya existe: `scripts/verify_quotes_v2.py` (probado con citas de Munger contra `munger.md`), `scripts/construir_corpus_damodaran.py`, la plantilla de trazabilidad y, en el Anexo B §B.4, la lista de lo que hay que localizar en cada paper.
