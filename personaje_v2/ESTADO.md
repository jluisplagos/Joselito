# ESTADO · personaje v2 (se actualiza en cada entrega)

Encargo vigente: **versión 0.2.1** (2-nov-2026). **Dos empresas reales hechas: Rational AG y Vidrala, S.A.** (autorizadas por José Luis el 3-nov-2026): las dos `concluido`, auditoría APROBADO. El personaje **no está declarado terminado**: falta la prueba de variabilidad (ver «Pendientes»).

Última actualización: 2026-11-03 (Europe/Amsterdam) · sesión: Claude Code (claude.ai) · orquestación: Opus 5.5 · agentes: Sonnet (extracción, lectura del corpus), Opus alto (fases A, B, C), Opus medio contexto limpio (auditoría).

## Cómo retomar (para una sesión que no ha visto nada)
1. Lee `personaje_v2/ENCARGO_personaje_v2.md` entero y los anexos A–D.
2. Lee este archivo y `DECISIONES.md` (todas las decisiones de construcción están registradas allí, con fecha 2-nov-2026).
3. Siguiente paso exacto: **pieza 5 (primera empresa real), solo con la autorización de José Luis y sus tres insumos** (S-1: qué empresa; S-2: `fase1_v63.json` con fuente y página por dato; la V5.3 evaluada por el v1 y los textos). Mientras tanto: pedir los 7 PDF de Damodaran (pieza 3) y resolver S-4 (dónde vive `personaje_v2/` en el repositorio; el repositorio no se ha leído ni se ha escrito en él).
4. Para ejecutar una empresa: `python3 scripts/pipeline.py empresas_v2/<E>` desde la raíz `personaje_v2/`. Cuando el pipeline necesita un agente termina con código 10 y deja `ESPERANDO.md` + `prompts_generados/<paso>_<agente>.md` en la carpeta de la empresa: se lanza ese agente (modelo y esfuerzo en la cabecera del prompt), que escribe el archivo pedido, y se vuelve a lanzar el pipeline. El pipeline nunca aprueba por agotamiento: si se agotan las correcciones, termina en `no_entregable` con `diagnostico.md`.

## Piezas
| Pieza | Estado | Notas |
|---|---|---|
| 0 Inventario, entorno, lecturas | hecha | `scripts/comprobar_entorno.sh` (python3, lxml, openpyxl, jsonschema, LibreOffice con perfil de recálculo forzado). |
| 1 Escritura íntegra (`escribir_v63.py` + prueba) | hecha | Método: XML directo (lxml) sobre el paquete; lista blanca de 68 celdas de juicio + entradas; borra las cachés de fórmulas; `verificar_v63.py` = ÍNTEGRO tras cada escritura. `pruebas/test_pieza1.py` 17/17. |
| 2 Scripts del pipeline | hecha (sintético) | 26 scripts en `scripts/` (pasos 0–14, Anexo B §B.2/§B.3, Anexo C, comprobación conjunta, ficha, informe, diagnóstico, resumen, `verificar_todo.sh`, `validar_esquema.py`). `pruebas/test_pipeline_sintetico.py`: 9 escenarios (completa, favorable, sobrevive, abstención, bloqueo, límite, datos ausentes, sin base, auditoría REPETIR) con agentes simulados: **30/30 comprobaciones PASAN** (`pruebas/sintetico/log_pruebas11.txt`; los escenarios de escritura repetidos en `log_pruebas12.txt` tras el último cambio: 17/17). Tres revisiones independientes con contexto limpio el 2-nov (scripts: 24 + 19 hallazgos; prompts/personaje/esquemas: 22 hallazgos): todas corregidas y registradas en `DECISIONES.md`. |
| 3 Corpus Damodaran | **hecha** (3-nov) | `corpus/damodaran.md`: 203 citas literales verificadas por script; `corpus/trazabilidad_damodaran.md` con páginas y reclasificaciones (cuota implícita → convención; la fórmula «invertida» de CV no existe en el PDF). Antes: `scripts/construir_corpus_damodaran.py`, `corpus/README.md` y `corpus/trazabilidad_damodaran.md` (plantilla) listos; **faltan los 7 PDF** (no se pueden descargar desde este entorno: la red solo permite registros de paquetes). Sin `corpus/damodaran.md`, `verify_quotes_v2.py` cuenta toda cita a Damodaran con página como **no comprobable = fallo**; el personaje y los prompts no citan páginas de Damodaran (solo categorías del Anexo B), así que pasan. |
| 4 Personaje v2 + prompts + esquemas | hecha (sin probar con agentes) | `personaje_munger_v2.md` (v2.0, 13.434 palabras, `verify_quotes_v2 --paginas-estrictas` PASS), `prompts/` (extracción V6.3, fase A, fase B, fase C turno 1, fase C turno 2, verificación; PASS de citas; revisados contra encargo, anexos y lo que el pipeline exige), `esquema/` (fase_a, fase_b, fase_c, ficha; validados contra las salidas sintéticas y con pruebas de mutación). **Ningún prompt se ha ejecutado con un agente real**: su calidad solo se podrá juzgar en la pieza 5. |
| 5 Primera empresa extremo a extremo | **hecha: Rational** | `empresas_v2/Rational/`: concluido · Vigilar · esperar · precio de Sí 336,87 € (provisional, C18) · auditoría APROBADO 16/16. Cuatro fallos de implementación corregidos en su causa (DECISIONES 3-nov). |
| 6 Segunda empresa + README | **hecha: Vidrala** | concluido · Vigilar · esperar · precio de Sí 54,67 € (52,17 con la combinación adversa) · auditoría APROBADO. README y `PROMPT_CLAUDE_CODE.md` actualizados. Antes: `README_v2.md` («cómo se ejecuta una empresa», requisitos, pruebas). La segunda empresa, tras la primera. |
| 7 (opcional) Fase 1 V6.3 genérica | **hecha y probada con Vidrala** | `scripts/fase1_historia.py`, `prompts/historia_anio.md`, `prompts/metadatos_fase1.md`, `scripts/pdf_a_texto.py`; integrada en el paso 2 del pipeline. Antes: `empresas_v2/Rational/fase1_partes/` (instrucciones por año, `consolidar.py`, `construir_fase1.py`): falta convertirlo en script genérico. Antes: `rellenar_fase1_v63.py` fija el esquema de `fase1_v63.json` (`esquema/fase1_v63.ejemplo.json`, sintético). |

## Qué está construido y probado (solo con datos sintéticos)
- Pipeline completo pasos 0–14 con los cinco estados finales; integridad del libro conservada en todas las escrituras (XML directo), recálculo forzado comprobado en cada lectura; comprobación conjunta (D10) sobre copia de prueba, que **supera** la comprobación cuando corresponde (escenario `sobrevive`: concluido · comprar · Sí · comprobación conjunta superada · auditoría APROBADO sintética) y **no** la supera cuando la zona cambia (`favorable` → `pendiente_de_investigacion`).
- Gramática (Anexo B §B.3) con G1a–G19, L1–L3, A1–A6; desviaciones solo con hechos referenciados y palanca fundamentada/convención; errores nunca aprobados; modo copia de prueba.
- Escalera (Anexo C) con forma cerrada y autotest (tolerancia 1e-9); `coincide_C86` exigido en el paso 12 cuando la tabla del DCF inverso es utilizable.
- S-19: revisión de **cada** dato de `datos_ausentes.json` exigida; material → `pendiente_de_datos`. D16: C104 sin porcentaje (esquema + coherencia + verificador). D17: todos los límites terminan en `no_entregable`; la auditoría solo aprueba con una línea `Veredicto: APROBADO` sin FALLA en 1/4/11/12/16.
- Esquemas JSON validados al recibir cada salida de agente y la ficha en todos los estados (criterio 7 †); criterios † 1 y 3 ejecutados en todos los estados finales.

## Pendientes explícitos (nada de esto está hecho)
- **Pieza 5**: ninguna empresa real analizada; ningún agente de juicio (Opus) ni de extracción (Sonnet) ejecutado. Los prompts pueden necesitar ajustes al primer uso real (D17: se corrige la causa, no el criterio).
- **Pieza 3**: `corpus/damodaran.md` y `trazabilidad_damodaran.md` vacíos hasta recibir los PDF; las categorías del Anexo B §B.0 no tienen todavía página de respaldo.
- **Prueba de variabilidad (§10.2.9), prueba de herencia (§10.2.11) y mediciones (§10.3)**: pendientes de la empresa real.
- **Criterio 2 (§10.2)** en una empresa real: `Motor!B255 = COMPLETO Y VÁLIDO` y `Control maestro!D250` sin pendientes dependen de la fase 1 real (en el sintético hay 5 datos «no verificables» por construcción).
- **S-1, S-2, S-4** sin respuesta: empresa, `fase1_v63.json` real, ubicación en el repositorio (el repositorio no se ha leído ni modificado; no se ha hecho ningún commit ni push). El paquete está listo para subirse tal cual como carpeta `personaje_v2/`: `config_v2.json` lleva rutas relativas a esa carpeta (`scripts/config_v2.py` las resuelve) y `config_v2.ejemplo.json` supone `kit_pipeline_munger/` y `V6_3/` junto a ella; `bash scripts/comprobar_entorno.sh` dice qué ruta hay que ajustar.
- `Análisis!D4` como texto ISO produce el aviso V31 de la hoja (ver `DECISIONES.md`); si José Luis prefiere la fecha como serie, hay que decidir el estilo (S-4b).
- El estado del libro no puede expresar `estado_analisis`: vive en `ficha.json`, `informe.md`, `resumen_v2.csv` y `estado_pipeline.json`.

## Supuestos resueltos por José Luis
- S-18 (2-nov-2026): el personaje no escribe porcentajes de posición, tampoco «0 %». S-19 (2-nov-2026): materialidad de los datos ausentes. S-1, S-2, S-4: **sin respuesta**.

## Mediciones (§10.3 del encargo)
| Empresa | Fase | Modelo | Tiempo | Coste aprox. | Intentos | Fallos | Estado final |
|---|---|---|---|---|---|---|---|
| (ninguna real) | — | — | — | — | — | — | — |
| Empresa X (sintética, 9 escenarios) | pipeline completo con agentes simulados | sin modelo (archivos JSON fijos) | ≈ 1–3 min por escenario (LibreOffice) | 0 | B: 1 (corrección por G5 en la primera pasada: el agente sintético copia la referencia y la justifica en la corrección) | 0 | concluido / pendiente_de_investigacion / pendiente_de_datos / modelo_no_aplicable / no_entregable según el escenario |

## Prueba de variabilidad
| Empresa | Celdas distintas entre pasadas | Cubo | Estado | Zona | Precio de Sí (dif. %) | Conclusión |
|---|---|---|---|---|---|---|
| pendiente (empresa real) | | | | | | |

## Desviaciones respecto a la referencia mecánica, por palanca (¿Munger se desvía siempre en el mismo sentido?)
| Empresa | g 1–5 | margen | S2C | g ∞ | ROIC LP | probabilidades |
|---|---|---|---|---|---|---|
| pendiente (empresa real) | | | | | | |

## Estados finales por empresa y causa (D17)
| Empresa | Estado | Causa (tipo) | Paso | Qué sigue válido |
|---|---|---|---|---|
| EmpresaX (sintética) | concluido (esperar; zona caro) | — | 14 | todo |
| EmpresaX_sobrevive (sintética, precio 8) | concluido (comprar; comprobación conjunta superada) | — | 14 | todo |
| EmpresaX_favorable (sintética, precio 16) | pendiente_de_investigacion | incertidumbre_no_acotada (la combinación lleva la zona a vigilar) | 10 | 68 celdas, escalera, cubo Vigilar |
| EmpresaX_sin_precio (sintética) | pendiente_de_datos | falta_de_datos (C37) | 3 | libro de datos íntegro |
| EmpresaX_bloqueo (sintética, g ≥ tasa) | no_entregable | fallo_de_implementacion (G2 tras 2 correcciones) | 8 | fase A escrita |
| EmpresaX_limite (sintética, C62 otro método) | modelo_no_aplicable | limite_del_modelo (L3) | 6 | juicio cualitativo |
| EmpresaX_sin_C34 (sintética) | pendiente_de_datos | falta_de_datos (C34 material, S-19) | 10 | 68 celdas, revisión de datos ausentes |
| EmpresaX_sin_base (sintética) | pendiente_de_investigacion | incertidumbre_no_acotada (ROIC LP sin base) | 10 | 68 celdas, cubo Vigilar |
| EmpresaX_repetir (sintética, auditoría REPETIR) | no_entregable | fallo_de_implementacion (auditoría tras 2 correcciones) | 13 | 68 celdas sin aprobar |

## Problemas abiertos
- La calidad de las salidas de los agentes (fases A, B, C, verificación) no se ha observado: los esquemas, la gramática y las coherencias atan el formato y las reglas, no el juicio.
- El lector del veredicto de la auditoría es conservador a propósito: la palabra «FALLA» dentro de un punto 1/4/11/12/16 que PASA, o cualquier coletilla tras «Veredicto: APROBADO», cuenta como REPETIR (gasta una corrección). El prompt de verificación lo advierte.
- Los prompts de las fases llevan reglas de formato que el pipeline exige (claves exactas, tokens de las Observaciones, formato de páginas, Damodaran sin página): un agente que las ignore agota dos correcciones de formato y termina en `no_entregable`. Es intencionado (D17), pero será la primera fuente de ruido en la pieza 5.
- `verify_quotes_v2.py` da por aproximados 6 fragmentos del personaje (heredados del v1: comillas y erratas del corpus); no son fallos en modo normal ni con `--paginas-estrictas`.
- Sin corpus Damodaran, los prompts piden citar a Damodaran solo por categoría (E1…, I1…, N1…), nunca por página.

## Presupuesto consumido (aprox.)
- Sesión de construcción del 2-nov-2026 en Claude Code: redacción (encargo 0.2.1, personaje v2, prompts, esquemas), scripts y pruebas sintéticas; ninguna llamada a agentes de juicio. Sin cifra en dólares disponible desde esta sesión.


## Pendientes (3-nov-2026, tras Rational)
1. **Prueba de variabilidad**: repetir fases A–C de Rational con agentes nuevos y comparar cubo, palancas y precio de Sí (¿la conclusión depende del agente?).
2. ~~Segunda empresa~~ hecha (Vidrala). 3. ~~Generalizar la pieza 7~~ hecha.
4. Revisar en el personaje el patrón visto en la fase B: fijar una palanca justo bajo un umbral de la gramática (S2C del BUENO = 3,9 «para no pasar de 2 × C55»). Se declaró y la fase C lo marcó, pero conviene una regla explícita.
5. Revisión final de la trazabilidad de Damodaran por un agente independiente (no hecha).

6. Instalar en el repositorio con `PROMPT_CLAUDE_CODE.md` (José Luis sube el zip; Claude Code instala, pasa las pruebas y sigue con más empresas y la variabilidad).
