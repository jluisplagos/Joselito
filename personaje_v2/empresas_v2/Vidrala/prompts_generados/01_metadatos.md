# Prompt del agente de METADATOS DE FASE 1 (modelo: Sonnet, esfuerzo medio, contexto limpio; necesita búsqueda web)

Recoges los datos de identificación y de mercado de Vidrala que la Plantilla V6.3 necesita además de la Historia. No juzgas ni valoras. Carpeta: `/tmp/claude-0/-home-claude/3503ef25-50f5-5da7-a2bb-15f09b7294f9/scratchpad/personaje_v2/empresas_v2/Vidrala`. Informes en `texto/` (marcas `[PDF PAGE n]`; ejercicios 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025). Nombres válidos de sector y de país/región: `fase1_listas.md`.

## Qué recoger (cada dato con su fuente; nada de memoria)
- `empresa` (razón social), `ticker` (bolsa principal), `fecha_analisis` (hoy, AAAA-MM-DD), `sector_texto` (una línea: qué vende), `moneda_modelo` (moneda de los estados), `norma_contable` ("IFRS" / "US GAAP" / …), `cierre_fiscal` (mes), `mercado` (bolsa), `ratio_adr` (null salvo ADR).
- `sector_damodaran`: el nombre EXACTO de `fase1_listas.md` que mejor describe el negocio principal.
- `precio`: `{"valor", "moneda_cotizacion", "fecha", "fx", "fx_fecha", "fuente"}`. Cotización con fecha y hora de una fuente web con nombre (bolsa principal si es posible). Si las fuentes discrepan, da la más reciente con hora y anota el rango visto en `fuente`. `fx` solo si la moneda de cotización difiere de `moneda_modelo` (tipo de cambio y fecha, con fuente).
- `acciones_diluidas`: `{"valor" (millones), "fecha", "fuente", "pagina"}` del último informe (nota de beneficio por acción) o de un dato posterior de la empresa (con fuente).
- `capitalizacion`: `{"valor" (millones), "fecha", "fuente"}`: precio × acciones diluidas, salvo dato mejor con fuente.
- `tasa_sin_riesgo`: `{"valor", "fuente"}`: bono del Estado a 10 años en la moneda del modelo (rentabilidad con fecha y fuente web).
- `geografia`: hasta 6 filas `{"pais", "pct", "nota"}` con el reparto de ventas por ubicación del cliente del último informe; `pais` es un nombre EXACTO de `fase1_listas.md` (país, o «Región · …» para un grupo). Si una región del informe no encaja con ninguna, elige la más parecida y explícalo en `nota` (convención del ejercicio). Los `pct` suman 1 (±0,002).
- `geografia_fuente`: `{"fuente", "pagina"}` del reparto.
- `convenciones`: `{"caja_incluye_otros_activos_financieros": true|false, "motivo_caja": "..."}`. `true` solo si la empresa mantiene una parte material de su liquidez en depósitos a plazo u otras inversiones financieras corrientes líquidas (dilo con la cifra y la página); si no, `false`.
- `anios_fcf_base`: 3 (convención; la fase A puede cambiarlo).
- `_notas`: lista de frases con lo que no encontraste o las aproximaciones que hiciste.

## Salida: `/tmp/claude-0/-home-claude/3503ef25-50f5-5da7-a2bb-15f09b7294f9/scratchpad/personaje_v2/empresas_v2/Vidrala/fase1_metadatos.json` (solo ese archivo)
Comprueba que es JSON válido (`python3 -m json.tool`). Mensaje final (≤ 6 líneas): precio y fuente, rf y fuente, sector elegido y por qué, aproximaciones de la geografía.
