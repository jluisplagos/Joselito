# personaje_v2 · personaje Munger v2 para la Plantilla V6.3

Estado real: **construido, probado con datos sintéticos y con dos empresas reales (Rational y Vidrala, 3-nov-2026: `concluido`, auditoría APROBADO)**. No declarado terminado: falta la prueba de variabilidad (ver `ESTADO.md`).

## Qué hay en esta carpeta
| Carpeta / archivo | Qué es |
|---|---|
| `ENCARGO_personaje_v2.md`, `ANEXO_A…D`, `CAMBIOS_v0_2.md` | La especificación (celdas de juicio, gramática de Damodaran, escalera de precios, formatos de salida). |
| `personaje_munger_v2.md` | El personaje (v2.0): lo que lee cada agente de juicio antes de trabajar. |
| `prompts/` | Los seis prompts: extracción V6.3, fase A, fase B, fase C (dos turnos), verificación. `pipeline.py` los copia a `prompts_generados/` con las rutas y el motivo de cada corrección. |
| `esquema/` | Esquemas JSON de `fase_a.json`, `fase_b.json`, `fase_c.json` y `ficha.json` (Anexo D) y el ejemplo de `fase1_v63.json`. |
| `scripts/` | El pipeline (`pipeline.py`, pasos 0–14) y sus piezas: escritura íntegra del libro (`escribir_v63.py`, `v63_xml.py`), recálculo forzado (`recalc.sh`), lectura (`leer_resultados.py`), referencias mecánicas y gramática (`referencias_mecanicas.py`, `comprobar_gramatica.py`), escalera (`precio_de_si.py`), comprobación conjunta (`comprobacion_conjunta.py`), ficha/informe/diagnóstico, verificación (`verificar_todo.sh`, `validar_esquema.py`, `verify_quotes_v2.py`). |
| `corpus/` | Dónde irá `damodaran.md` (constructor: `scripts/construir_corpus_damodaran.py`; faltan los PDF). |
| `pruebas/` | `test_pieza1.py` (escritura íntegra) y `test_pipeline_sintetico.py` (9 escenarios con agentes simulados); `sintetico/` guarda la última ejecución. |
| `config_v2.json` | Rutas (relativas a esta carpeta), convenciones, límites de correcciones y modelos previstos por agente. `config_v2.ejemplo.json` es la misma configuración con las rutas supuestas del repositorio. |
| `empresas_v2/` | Una carpeta por empresa real (vacía hasta la pieza 5). |

## Requisitos
Python 3 con `openpyxl`, `lxml`, `pypdf`, `jsonschema`; LibreOffice (`soffice`) y `pdftotext`. Además, en el mismo repositorio o en una ruta conocida: el paquete V6.3 (`entregables/Plantilla_V6.3.xlsx`, `referencia/referencia_V6.3.json`, `scripts/verificar_v63.py`, `scripts/inventario_entradas.py`, `scripts/add_sliders.py`, `scripts/patch_v62_base.py`) y el kit v1.3 (`kit_pipeline_munger/`: `munger.md` y `scripts/add_cached_values.py`). Ajusta `plantilla.*` y `kit_v1.*` en `config_v2.json` (rutas relativas a `personaje_v2/`) y comprueba:

```
bash scripts/comprobar_entorno.sh
```

## Cómo se ejecuta una empresa
(El procedimiento completo para Claude Code, con instalación y reglas, está en `PROMPT_CLAUDE_CODE.md`.)
1. Crea `empresas_v2/<E>/etapa1/` con `<E>_evaluada.xlsx` (la V5.3 decidida por el personaje v1) y `<E>_respuesta.md`, y `empresas_v2/<E>/pdf/` con los informes anuales de 10 años (cuentas consolidadas, con el año en el nombre). `python3 scripts/pdf_a_texto.py empresas_v2/<E>` los convierte a `texto/` con marcas `[PDF PAGE n]`.
2. Lanza `python3 scripts/pipeline.py empresas_v2/<E>`. Cuando necesita agentes termina con código 10 y deja `ESPERANDO.md` y los prompts en `prompts_generados/`. Primero, la **fase 1** (si no hay `fase1_v63.json`): un agente por año (`01_historia_<año>.md`) y uno de metadatos (`01_metadatos.md`, con web), en paralelo; `scripts/fase1_historia.py` comprueba cada cifra en su página, consolida (cifra más reciente publicada) y escribe `fase1_v63.json` y `historia_revision.md`. Después: extracción, fase A, fase B, fase C (dos turnos del mismo agente) y verificación.
3. Lanza cada agente con el modelo y esfuerzo que dice la cabecera de su prompt (`config_v2.json → modelos`: Sonnet medio para historia, metadatos y extracción; Opus alto para las fases A, B y C; Opus medio con contexto limpio para la verificación), con el prompt generado como instrucción.
4. Vuelve a lanzar `pipeline.py`: continúa donde estaba. Repite hasta código 0.
5. Resultado: `<E>_v63_evaluada.xlsx` (libro íntegro: `verificar_v63.py` = ÍNTEGRO), `ficha.json`, `informe.md`, `precio.json`, `resultados.json`, `gramatica.md`, `auditoria.md`, `historia_revision.md`, los `verificacion_*.txt` y, si el estado no es `concluido`, `diagnostico.md` con qué falta y desde qué paso se reanuda (`--desde N`). `estado_pipeline.json` lleva el historial completo.

Estados finales: `concluido` · `pendiente_de_datos` · `pendiente_de_investigacion` · `modelo_no_aplicable` · `no_entregable`. Agotar un límite de correcciones nunca aprueba: termina en `no_entregable` con diagnóstico (D17). El personaje no escribe tamaños de posición (D16): `Análisis!C104` empieza siempre por «Pendiente de decisión de cartera».

## Pruebas
```
python3 pruebas/test_pieza1.py              # escritura íntegra y recálculo forzado (17 comprobaciones)
python3 pruebas/test_pipeline_sintetico.py  # 9 escenarios con agentes simulados (≈ 15 min, LibreOffice)
python3 scripts/precio_de_si.py --autotest  # escalera (Anexo C)
```

## Lo que no está hecho
Prueba de variabilidad (repetir Rational con agentes nuevos) y más empresas. Hechos el 3-nov-2026: corpus Damodaran, Rational y Vidrala (las dos `concluido` con auditoría APROBADO) y la fase 1 automática (pieza 7). Detalle y «cómo retomar» en `ESTADO.md`.
