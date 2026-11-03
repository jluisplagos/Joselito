# Extracción de un año de Rational AG (fase1_v63, pieza 7)

Trabajas con UN informe anual: `texto/AR_<AÑO>.txt` (marcas `[PDF PAGE n]`; n es la página que se cita). Carpeta base:
`/tmp/claude-0/-home-claude/3503ef25-50f5-5da7-a2bb-15f09b7294f9/scratchpad/personaje_v2/empresas_v2/Rational`.
Localiza los estados financieros consolidados (Statement of Comprehensive Income, Balance Sheet, Cash Flow Statement) y las notas
con Grep y léelos con Read (offset/limit). No uses memoria ni internet: solo el texto. Si un dato no está, `null` y dilo; nunca estimes.

## Qué extraer (para el AÑO del informe; y también la columna del año anterior que trae el mismo informe)
Para cada partida: el número **tal como está impreso** (cadena, con sus separadores y signo, p. ej. "1,125,977" o "-12,345"), la unidad
impresa (p. ej. "kEUR"), la página, y la línea literal donde aparece (copiada del texto, recortada a ≤ 200 caracteres).

| clave | qué es | dónde |
|---|---|---|
| ventas | Sales revenues | cuenta de resultados |
| ebit | Operating result / EBIT tal como lo informa la cuenta de resultados | cuenta de resultados |
| da | Depreciation and amortisation (y deterioros si van en la misma línea) | estado de flujos |
| beneficio_neto | Profit after taxes atribuible a los accionistas de la dominante | cuenta de resultados |
| impuestos | Income taxes (gasto del año) | cuenta de resultados |
| bai | Earnings before taxes (EBT) | cuenta de resultados |
| cfo | Cash flow from operating activities | estado de flujos |
| capex | pagos por inmovilizado material + intangible (Investments / Payments for property, plant, equipment and intangible assets) | estado de flujos |
| adquisiciones | pagos por compra de negocios menos cobros por venta de negocios (si no hay línea: null y nota «sin línea») | estado de flujos |
| circulante_lineas | lista de TODAS las líneas de variación de activos/pasivos operativos del estado de flujos (inventarios, cuentas a cobrar y otros activos, cuentas a pagar y otros pasivos, provisiones…), cada una con su número impreso | estado de flujos |
| intereses | intereses pagados (total) | estado de flujos o notas |
| intereses_financiacion | la parte de intereses pagados que figura en actividades de financiación (null si figura en operaciones) | estado de flujos |
| arrendamientos_principal | repayment / principal portion of lease liabilities (financiación). Antes de IFRS 16 (2019) normalmente no existe: null y nota | estado de flujos |
| sbc | gasto por pagos basados en acciones (share-based payment). Busca «share-based», «stock option», «share plan». Si no aparece ninguna mención, null y nota «sin mención en el informe» | notas |
| id | gasto de investigación y desarrollo del año (Research and development costs / expenses) | notas o informe de gestión |
| acciones_diluidas | número medio ponderado de acciones diluido (o «number of shares» usado en el beneficio por acción diluido) | nota de beneficio por acción |
| patrimonio | Equity atribuible a los accionistas de la dominante, al cierre | balance |
| deuda | deudas financieras (liabilities to banks / financial liabilities), corto + largo, SIN arrendamientos | balance o notas |
| arrendamientos | pasivos por arrendamiento (lease liabilities), corto + largo | balance o notas |
| caja | Cash and cash equivalents | balance |
| otros_activos_financieros | activos financieros corrientes que no son caja (depósitos a plazo, valores) — aparte, no se suman a la caja | balance |
| pensiones | obligación neta por pensiones (provisions for pensions) | balance o notas |
| minoritarios | Non-controlling interests (si no hay línea: null y nota) | balance |

Además: `fecha_cierre` del ejercicio, `moneda` y `unidad` de los estados, y si el informe dice que reexpresa cifras del año anterior.

## Salida
Escribe `fase1_partes/AR_<AÑO>.json` con esta forma:
```
{"anio": <AÑO>, "fecha_cierre": "...", "moneda": "EUR", "unidad": "kEUR",
 "reexpresion": "<texto o null>",
 "partidas": {"ventas": {"actual": {"impreso": "...", "pagina": n, "linea": "..."},
                         "anterior": {"impreso": "...", "pagina": n, "linea": "..."},
                         "nota": null}, ...,
              "circulante_lineas": {"actual": [{"concepto": "...", "impreso": "...", "pagina": n, "linea": "..."}, ...],
                                    "anterior": [...], "nota": null}}}
```
Antes de terminar, comprueba con un script (python) que cada `impreso` aparece literalmente en la `linea` y que la `linea` aparece en su
página del .txt. Mensaje final (≤ 8 líneas): partidas `null` y por qué, ambigüedades (qué línea elegiste y por qué), reexpresiones.
No leas ni escribas nada fuera de esta carpeta. No leas el repositorio de GitHub.
