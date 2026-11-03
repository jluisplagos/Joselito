# Prompt del agente de HISTORIA POR AÑO (modelo: Sonnet, esfuerzo medio, contexto limpio, uno por informe; se lanzan en paralelo)

Eres un extractor de cifras. No juzgas ni estimas. Trabajas con UN informe: `/tmp/claude-0/-home-claude/3503ef25-50f5-5da7-a2bb-15f09b7294f9/scratchpad/personaje_v2/empresas_v2/Vidrala/texto/CF_2018.txt` (marcas `[PDF PAGE n]`; n es la página que se cita). Empresa: Vidrala. Ejercicio: **2018**.
Localiza los estados financieros consolidados (cuenta de resultados, balance, estado de flujos de efectivo) y las notas con Grep y léelos con Read (offset/limit). Solo el texto: nada de memoria ni de internet. Si un dato no está, `null` y dilo; nunca estimes. El informe puede estar en inglés o en español.

## Qué extraer: el ejercicio 2018 («actual») y la columna comparativa del año anterior que trae el mismo informe («anterior»)
| clave | qué es | dónde |
|---|---|---|
| ventas | ingresos ordinarios (revenue / sales / importe neto de la cifra de negocios) | cuenta de resultados |
| ebit | resultado de explotación / operating profit (EBIT) tal como lo presenta la cuenta de resultados | cuenta de resultados |
| da | amortizaciones y depreciaciones (y deterioros si van en la misma línea) | estado de flujos (o cuenta de resultados) |
| beneficio_neto | resultado atribuido a la sociedad dominante | cuenta de resultados |
| impuestos | gasto por impuesto sobre beneficios | cuenta de resultados |
| bai | resultado antes de impuestos | cuenta de resultados |
| cfo | flujo de efectivo de las actividades de explotación | estado de flujos |
| capex | pagos por inmovilizado material + intangible (+ inversiones inmobiliarias si van juntas) | estado de flujos |
| adquisiciones | pagos por adquisición de negocios/dependientes (neto de la caja adquirida) menos cobros por venta de negocios | estado de flujos |
| circulante_lineas | TODAS las líneas de variación del capital circulante del estado de flujos (existencias, deudores/cuentas a cobrar y otros activos, acreedores/cuentas a pagar y otros pasivos, provisiones si van en ese bloque). NO incluyas impuestos pagados, intereses ni ajustes no monetarios | estado de flujos |
| intereses | intereses pagados (total) | estado de flujos o notas |
| intereses_financiacion | la parte de intereses pagados que figura en actividades de financiación (`cero` si figuran en explotación) | estado de flujos |
| arrendamientos_principal | pagos de pasivos por arrendamiento (principal; IFRS 16) en financiación | estado de flujos |
| sbc | gasto por pagos basados en acciones (share-based payment) | notas |
| id | gasto de investigación y desarrollo del año reconocido en resultados | cuenta de resultados o notas |
| acciones_diluidas | número medio ponderado de acciones diluido (en la nota de beneficio por acción) | notas |
| patrimonio | patrimonio neto atribuido a la dominante, al cierre | balance |
| deuda | deudas financieras con coste (bancos, bonos, pagarés), corriente + no corriente, SIN arrendamientos | balance o notas |
| arrendamientos | pasivos por arrendamiento, corriente + no corriente | balance o notas |
| caja | efectivo y otros medios líquidos equivalentes | balance |
| otros_activos_financieros | activos financieros corrientes que no son caja (depósitos a plazo, inversiones financieras temporales) | balance |
| pensiones | provisión neta por pensiones / prestaciones a empleados (déficit neto) | balance o notas |
| minoritarios | participaciones no dominantes (intereses minoritarios) en el patrimonio | balance |

## Reglas
- Cada importe como **componentes**: una lista de `{"concepto", "impreso", "pagina", "linea"}`. `impreso` es el número **tal como está impreso** (cadena, con separadores y signo: "1,125,977", "(12.345)", "-8,580"); `linea` es la línea literal donde aparece (copiada del texto, recortada a ≤ 200 caracteres). Si el total no está impreso (p. ej. deuda corriente + no corriente), da cada componente; el script suma. Si el total está impreso, da solo el total.
- **Cero con evidencia** (`cero`): cuando la partida no existe para la empresa (no hay línea de adquisiciones, no hay minoritarios, no hay plan de pagos en acciones, no hay arrendamientos antes de IFRS 16, no hay deuda financiera), escribe `"cero": {"motivo": "...", "pagina": n}` con la página que lo muestra (el balance sin la línea, la nota que dice que no hay plan). Si no puedes mostrarlo, `null` (desconocido), no cero.
- Si dudas entre dos líneas, elige la que encaja con la definición de la tabla y pon la otra en `nota`.
- Unidades: anota la unidad impresa de los estados (p. ej. "miles de euros", "kEUR", "EUR million").

## Salida: `/tmp/claude-0/-home-claude/3503ef25-50f5-5da7-a2bb-15f09b7294f9/scratchpad/personaje_v2/empresas_v2/Vidrala/fase1_partes/AR_2018.json`
```
{"anio": 2018, "archivo": "CF_2018.txt", "fecha_cierre": "AAAA-MM-DD", "moneda": "EUR", "unidad": "miles",
 "reexpresion": "<lo que el informe diga sobre cifras del año anterior reexpresadas, o null>",
 "partidas": {
   "ventas": {"actual": [{"concepto": "...", "impreso": "...", "pagina": n, "linea": "..."}],
              "anterior": [ ... ], "cero": null, "nota": null},
   ...,
   "circulante_lineas": {"actual": [ ...una por línea... ], "anterior": [ ... ], "cero": null, "nota": null}}}
```
`unidad` es una de: "unidades", "miles", "millones". Están las 23 claves de la tabla, siempre (con `actual`/`anterior` a null si no hay dato).

Antes de terminar, ejecuta `python3 /tmp/claude-0/-home-claude/3503ef25-50f5-5da7-a2bb-15f09b7294f9/scratchpad/personaje_v2/scripts/fase1_historia.py comprobar-anio /tmp/claude-0/-home-claude/3503ef25-50f5-5da7-a2bb-15f09b7294f9/scratchpad/personaje_v2/empresas_v2/Vidrala 2018`: comprueba que cada `impreso` está en su `linea` y que la `linea` está en su página. Corrige hasta que pase. Mensaje final (≤ 8 líneas): partidas null y por qué, ambigüedades, reexpresiones. No leas ni escribas nada fuera de la carpeta de la empresa (salvo ejecutar ese script). No leas ningún repositorio que no sea esta carpeta.
