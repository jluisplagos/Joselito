# Instrucciones del agente de lectura (un documento de Damodaran)

Trabajas con UN documento: `corpus/texto/<COD>.txt`, texto extraído con marcas `[PDF PAGE n]` (n = página del PDF; es la página que se cita).
Lee TODO el documento, página por página, en bloques de unas 15 páginas (Read con offset/limit). No uses memoria ni conocimiento externo sobre Damodaran: solo lo que dice el texto.

## Qué escribir
1. `corpus/partes/<COD>.md`: entre 15 y 30 entradas, una por línea, con este formato exacto:
   `- **<sección o tema>** — *<el principio en una línea, en español>.* “<cita literal>” (<Título corto completo>, p. <n>)`
   - Título corto completo, no el código: Numbers and Narrative · Growth and Value · Measuring Returns · Closure in Valuation · Probabilistic Approaches · Ups and Downs · Financial Service Firms.
   - La cita es LITERAL, copiada del texto: entre 12 y 60 palabras, una sola frase o dos seguidas, sin saltos de página dentro, sin tablas ni columnas partidas. Une los saltos de línea con un espacio. Si falta un trozo, no lo rellenes: elige otra frase. Usa comillas curvas “…”; no pongas comillas rectas dentro de la cita.
   - `p. <n>` es la marca `[PDF PAGE n]` de la página donde empieza la cita. Si cruza dos páginas, elige otra cita.
   - Cubre el documento entero (entradas repartidas por todos los bloques) y, sobre todo, los puntos de la lista «Qué buscar» de abajo. Si un punto de la lista NO tiene apoyo literal en el texto, dilo en el informe; no lo inventes ni lo aproximes.
   - La primera línea del archivo: `Reading log: <COD>, páginas 1–<N>: leídas todas (indica qué páginas son portada, índice, tablas ilegibles, imágenes sin texto).`
2. `corpus/partes/<COD>_trazabilidad.md`: una fila por cada principio de la lista (Id, página(s), frase literal más corta que lo sostiene, y si el texto lo sostiene del todo, en parte o no). Si el texto lo contradice o lo matiza (por ejemplo una fórmula impresa al revés), cítalo y dilo.
3. Tu mensaje final: máximo 10 líneas: nº de entradas, qué principios quedaron sin apoyo literal, anomalías (texto ilegible, fórmulas rotas por el extractor).

No leas ni escribas nada fuera de `corpus/texto/<COD>.txt` y `corpus/partes/`. No leas el repositorio de GitHub. Las cifras de ejemplo del paper (tasas, márgenes, años concretos) son del paper: cítalas solo como ejemplo, nunca como parámetro.
