# ANEXO D · Esquemas, formatos y salidas

Versión 0.2.1 (2-nov-2026). Todo JSON en UTF-8, números como números (0,07 → `0.07`), fechas `AAAA-MM-DD`, textos en español. Los esquemas definitivos (JSON Schema) se escriben en `esquema/` en la pieza 4 y los validan los scripts. Lo que sigue fija el contenido mínimo.

## D.1 `extracto_v63.md` (agente de extracción V6.3 · Sonnet · ≤ 10.000 palabras)

Complementa el `extracto.md` de la etapa 1 (no lo repite). Secciones, cada dato con `[archivo, PDF p. n]`; si no hay información: «No encontrado en los documentos».

1. **Mercado y cuota**: cifras de tamaño de mercado, crecimiento del mercado y cuota que la propia empresa publique (con la definición que use). Nada de memoria.
2. **Economía por segmento y geografía**: ventas y margen por segmento, reparto geográfico (% de ventas por país o región; es lo que va a `Palancas!A28:B33`), evolución a tipo constante.
3. **Capacidad, capex e inversión**: planes de capacidad, capex anunciado por destino, I+D (importe y % de ventas), adquisiciones con precio y múltiplo si lo dan.
4. **Precios y poder de fijación**: subidas de precio y su efecto en volumen; mezcla; evidencia de que el cliente absorbe o no la subida.
5. **Guía y objetivos de la dirección** (solo como dato, etiquetado «guía»): ventas, margen, capex, dividendo; y si cumplió la guía anterior.
6. **Financiación** (para el motor B y la quiebra): vencimientos, covenants, rating si lo publica, coste medio de la deuda, pasivos por arrendamientos, pensiones, minoritarios.
7. **Regulación y capital** (solo financieras y reguladas): ratios de capital exigidos y mantenidos, límites regulatorios a la distribución.
8. **Hechos medibles para predicciones**: métricas que la empresa publica con regularidad (unidades, tiendas, clientes, cartera de pedidos, márgenes por segmento) y su último valor, para que las predicciones de la fase C sean comprobables.
9. **Lo que no encontré.**

## D.2 `fase_a.json` (Munger cualitativo)

```json
{
  "empresa": "…", "ticker": "…", "fecha_analisis": "AAAA-MM-DD", "version_personaje": "v2.0",
  "cinco_frases": "…",
  "seis_preguntas": {"confio_en_la_gestion": "…", "puede_danar_reputacion": "…", "que_puede_salir_mal": "…", "lo_entiendo": "…", "necesita_capital": "…", "que_caja_espero": "…"},
  "descalificadores": [{"nombre": "deuda que mata", "aplica": false, "evidencia": "…"}],
  "foso": {"tipo": "…", "pruebas": {"sobrino_idiota": "…", "duracion": "…", "quien_me_mata": "…", "empresa_o_nicho": "…"}},
  "cubo_provisional": "Vigilar",
  "limite_del_modelo": {"aplica": false, "cual": null, "porque": null},
  "celdas": {"C11": "Sí", "C12": "Sí", "C13": "No", "C14": "Compounder", "C17": "Sí", "C18": "Sí", "C19": "Sí", "C20": "Incert. alta + riesgo bajo",
             "C25": "Sí", "C27": "Estable", "C51": "Sí", "C56": 0.09, "C61": "No está claro", "C62": "Sí", "C97": "Neutral", "C98": "Buena",
             "Palancas!C5": "Madura en crecimiento", "Palancas!C6": "Ninguno", "Palancas!C8": "Último año", "Palancas!C9": "No", "Palancas!C10": null,
             "Palancas!C43": "No aplica", "Palancas!C47": "Ninguna",
             "B65": "…", "C65": "…", "D65": "…", "B66": "…", "C66": "…", "D66": "…"},
  "herencia": {"C18": {"etapa1": "Sí", "decision": "mantiene", "motivo": "evidencia_nueva", "evidencia_y_razonamiento": "ROIC medio 5 años 22 % frente a r 9 % (Historia C55); margen EBIT 10 años entre 38 y 42 % (fila 29): la ventaja se ve en diez años, no solo en los tres de la etapa 1"}},
  "escenarios": {"MALO": {"historia": "…", "mecanismo": "…", "quien_se_queda_la_mejora": "…", "que_lo_pararia": "…", "hechos_en_que_se_apoya": ["…"]}, "NORMAL": {…}, "BUENO": {…}},
  "observaciones": {"C11": "[Clase: …] [Confianza: …] Hereda: … Apoyo: … Lo sustituiría: …"},
  "lo_que_no_se": ["…"], "que_no_sabria_munger": ["…"]
}
```

`herencia` tiene una entrada por cada una de las **22** celdas heredadas que decide la fase A (`C11:C14`, `C17:C20`, `C25`, `C27`, `C51`, `C56`, `C61`, `C62`, `C97`, `C98`, `B65:D66`). `decision` ∈ {`mantiene`, `cambia`}; `motivo` ∈ {`misma_evidencia`, `evidencia_nueva`, `razonamiento_corregido`, `definicion_o_medicion_distinta`} (D3); `evidencia_y_razonamiento` es obligatorio en todos los casos y tiene que **nombrar la evidencia** (celda de Historia, página del extracto, dato de la V6.3) y el razonamiento; no vale remitirse a la etapa 1 como autoridad. `mantiene` + `misma_evidencia` es una combinación legítima y frecuente. Las otras 12 heredadas llevan el mismo campo `herencia` en `fase_b.json` (`B68:D69`, `C76`: 7) y en `fase_c.json` (`C93`, `B101`, `B102`, `C103`, `C104`: 5); `ficha.py` junta las 34 en `cambios_vs_etapa1`. `limite_del_modelo.aplica = true` (L1 sin motor B posible, L2 o L3 del Anexo B) lleva el análisis a `modelo_no_aplicable` sin fase B; en ese camino `ficha.py` deriva `decision.accion` de `cubo_provisional` (`No` → `descartar`, `Demasiado difícil` → `demasiado_dificil`, otro → `null`), con `precio_objetivo` y `condicion` = `null`. Si el límite lo declara la fase C en su primer turno (paso 10), `ficha.py` deriva la acción igual, de `fase_c.json.cubo_provisional`.

## D.3 Formato de la Observación (columna N de Control maestro y campo `observaciones`)

Una Observación por celda, en una sola celda de texto, con este orden y estas etiquetas (para que los scripts la validen):

```
[Clase: fundamentada | convención | técnico | sin juicio propio] [Confianza: alta | media | baja]
Hereda: <valor etapa 1> → <mantiene | cambia> (<motivo>): <evidencia y razonamiento en una frase>.   (celdas heredadas)
Hereda: nueva en V6.3.                                                                              (celdas nuevas)
Referencia mecánica: <cifra y regla, o «no disponible: motivo»>. Decisión: <cifra o valor>. Desviación: <±x, «ninguna» o «sin referencia»> porque <motivo>.   (solo palancas, probabilidades, quiebra, C76, C44)
Apoyo: <hechos del extracto o de la Historia, con celda o página; citas «…» (PCA p.110; HIM) o (CV p. 7)>.
Lo sustituiría: <qué dato o hecho me haría cambiar esta celda, en qué sentido>.
```

Reglas: ≤ 900 caracteres; toda cita con libro/documento y página; `<motivo>` es uno de los cuatro de D3; la clase *sin juicio propio* solo con «Desviación: ninguna» y referencia disponible; la clase *técnico* solo donde no hay referencia disponible (o la celda no tiene referencia), con «Desviación: sin referencia» y siempre con un rango en «Apoyo»; una Observación de celda heredada siempre lleva la línea `Hereda: … → …`; una de celda nueva lleva exactamente `Hereda: nueva en V6.3.` Una Observación con clase *fundamentada* o *convención* cuya línea «Apoyo» no cite ningún hecho (celda o página) se cuenta como hipótesis insuficientemente fundamentada a efectos de D10.

## D.4 `fase_b.json` (palancas)

```json
{
  "motor": "A",
  "palancas": {
    "crecimiento_1_5": {"MALO": {"referencia_mecanica": 0.0, "referencia_no_disponible_motivo": null, "valor": 0.01, "desviacion": 0.01, "clase": "fundamentada", "confianza": "media", "porque": "…", "apoyo": "…", "lo_sustituiria": "…"}, "NORMAL": {…}, "BUENO": {…}},
    "margen_objetivo": {…}, "s2c": {…}, "g_perpetuo": {…}, "roic_lp": {…},
    "probabilidades": {"MALO": {…}, "NORMAL": {…}, "BUENO": {…}, "argumento": "…"}
  },
  "quiebra": {"C22": null, "C23": null, "disparadores": [], "clase": "convención", "porque": "…"},
  "mercado": {"C24": null, "fuente": null},
  "exceso_caja": {"C76": 0, "clase": "fundamentada", "porque": "…"},
  "fcf_normalizado": {"C44": null, "clase": null, "porque": "…"},
  "desviaciones_justificadas": [{"comprobacion": "G4", "escenario": "NORMAL", "justificacion": "…", "hechos": ["Historia C55", "extracto p. 12"], "clase": "fundamentada"}],
  "limite_del_modelo": {"aplica": false, "cual": null, "porque": null},
  "herencia": {"B68": {"etapa1": 0.015, "decision": "mantiene", "motivo": "misma_evidencia", "evidencia_y_razonamiento": "…"}, "C68": {…}, "D68": {…}, "B69": {…}, "C69": {…}, "D69": {…}, "C76": {…}},
  "dos_errores": {"mas_cerca_de": "regatear | pagar cualquier cosa", "porque": "…"},
  "celdas": {"Palancas!B14": 0.01, "Palancas!C14": 0.04, "Palancas!D14": 0.06, "Palancas!B15": …, "Palancas!B16": …, "Palancas!B18": …, "B68": 0.015, "C68": 0.025, "D68": 0.03, "B69": 0.2, "C69": 0.6, "D69": 0.2, "C76": 0, "Palancas!C22": null, "Palancas!C23": null, "Palancas!C24": null, "Palancas!C44": null},
  "observaciones": {"Palancas!B14": "…", "…": "…"}
}
```

Por palanca y escenario: `referencia_mecanica` (número, o `null` con `referencia_no_disponible_motivo`), `valor`, `desviacion` (`valor − referencia_mecanica`, o `null` si no hay referencia), `clase`, `confianza`, `porque`, `apoyo`, `lo_sustituiria`. Regla G14: `clase = "sin juicio propio"` exige referencia disponible y `desviacion = 0`; con referencia `null` la clase es *fundamentada*, *convención* o *técnico*. `comprobar_gramatica.py` exige que toda comprobación de categoría *desviación económica* disparada tenga su entrada en `desviaciones_justificadas` con `justificacion` no vacía, `hechos` no vacío y clase *fundamentada* o *convención*; un **error** no admite entrada ahí: se corrige. `limite_del_modelo.aplica = true` (L1 detectado al traducir) devuelve la pregunta a la fase A (código 3).

## D.5 `resultados.json` (lectura del libro recalculado)

Valores (`B78:D78`, `C83`, `C84`, `C85`, `C86`, `C39`, `C87`), estados (`Motor!B255`, `B256`, `B258`, `B266`, `B267`, `B268`, `B269`), causas activas (`Diagnóstico V6!A161:A172`), semáforos (`Diagnóstico V6!B40:D50` con sus textos), «cuánto pagas por crecer» (`C53:D57`), múltiplos (`B61:E65`), autocomprobaciones (`B69:B84`), salto del año 11 (`B176:D178`), tornado (`A215:C221`), precio de referencia (`C156`), evidencias (`Control maestro!D240:D250`), banderas y avisos (`Análisis!C7`, `D7`), tabla del DCF inverso (`Análisis!A108:B188`), `Diagnóstico V6!C5` (motor), `C15:C18` (r operativa y r mínima), `Historia!C43:C66` (anclas), y `recalculo_forzado_comprobado: true` (la prueba de §4.7: una celda dependiente de una celda escrita cambió).

## D.6 `fase_c.json` (revisión inversa, fundamento material y conclusión; se completa en dos turnos)

```json
{
  "una_sola_historia": {"coherente": true, "incoherencias": ["…"]},
  "lo_que_dice_la_hoja": {"semaforos_relevantes": ["…"], "peso_terminal_NORMAL": 0.68, "salto_anio_11": {"MALO": 0.01, "NORMAL": 0.07, "BUENO": 0.12, "explicacion": "…"}, "dcf_inverso": "…", "palanca_mas_influyente": "ROIC / ROE largo plazo (±5 pts)", "nota": "el tornado es información, no criterio"},
  "desviaciones_justificadas": [{"comprobacion": "G16", "escenario": "NORMAL", "justificacion": "…", "hechos": ["…"], "clase": "fundamentada"}],
  "autocomprobacion": [
    {"sesgo": "anclaje en la etapa 1", "hallazgo": "…", "cambio": "ninguno porque … | C18 → …"},
    {"sesgo": "anclaje en el precio o en la fuente externa", "hallazgo": "…", "cambio": "…"},
    {"sesgo": "consistencia y compromiso", "hallazgo": "…", "cambio": "…"},
    {"sesgo": "historia bonita / viento de cola atribuido a la empresa", "hallazgo": "…", "cambio": "…"},
    {"sesgo": "optimismo del BUENO frente a la tasa base", "hallazgo": "…", "cambio": "…"},
    {"sesgo": "doble castigo del mismo riesgo", "hallazgo": "…", "cambio": "…"},
    {"sesgo": "disponibilidad (lo vívido del extracto)", "hallazgo": "…", "cambio": "…"},
    {"sesgo": "autoridad (guía de la dirección como hecho)", "hallazgo": "…", "cambio": "…"},
    {"sesgo": "¿el MALO es de verdad malo?", "hallazgo": "…", "cambio": "…"},
    {"sesgo": "lo no numerable que pesa y no está en las palancas", "hallazgo": "…", "cambio": "…"}
  ],
  "revisar_palancas": false, "instrucciones_revision": null,
  "cubo_provisional": "Sí", "conclusion_provisional": "comprar",
  "revision_datos_ausentes": {
    "revisados": [
      {"dato": "Análisis!C88", "que_falta": "P/FCF histórico", "conclusion_afectada": "ninguna celda de juicio; solo contexto del precio", "material_para_conclusion_favorable": false, "porque": "la escalera no usa C88; el múltiplo histórico serviría de contraste, no de fundamento"},
      {"dato": "Palancas!A28:B33", "que_falta": "reparto geográfico de las ventas", "conclusion_afectada": "prima de riesgo país dentro de r (heredada, S-3) y lectura del mercado del BUENO", "material_para_conclusion_favorable": false, "porque": "el extracto (p. 14) dice que el 91 % de las ventas es de la eurozona: la prima país que falta no cambia r de forma apreciable; lo anoto en lo_que_no_se"}
    ],
    "alguno_material": false
  },
  "fundamento_material": {
    "hipotesis_sin_fundamento": [
      {"celda": "B69:D69", "hipotesis": "probabilidades 0,2/0,6/0,2", "clase": "sin juicio propio", "porque_sin_fundamento": "copiadas de la referencia sin argumento propio",
       "alternativas_defendibles": {"hay_base": true, "rango": {"MALO": [0.2, 0.4], "NORMAL": [0.4, 0.6], "BUENO": [0.1, 0.2]},
         "evidencia": "p(MALO), techo 0,4: en 10 ejercicios (Historia 2015–2024, filas 28–29), 4 tuvieron crecimiento negativo O margen por debajo del margen del MALO (2016, 2019, 2020, 2023) = 0,4. Suelo 0,2: con la definición estricta (las dos cosas a la vez) son 3 (2016, 2020, 2023) = 0,3, y de ellos 2020 fue el cierre por pandemia, que la dirección describe como no repetible y cuyas ventas se recuperaron en 2021 (extracto p. 22): sin ese año, 2 de 10 = 0,2. p(BUENO), suelo 0,1: 1 de 10 ejercicios (2021) cumplió a la vez el crecimiento y el margen del BUENO. Techo 0,2: 2 de 10 (2017, 2021) cumplieron al menos una de las dos condiciones. NORMAL: el resto."}},
      {"celda": "Palancas!D18", "hipotesis": "ROIC LP BUENO 0,18", "clase": "técnico", "porque_sin_fundamento": "sin referencia BUENO (C55 vacía: la empresa publica el desglose necesario solo desde 2022, tres ejercicios de 2015–2024) y sin hechos en los extractos sobre cuánto durará la ventaja",
       "alternativas_defendibles": {"hay_base": false, "rango": null,
         "evidencia": "no hay base para acotarlo: la media del ROIC del sector (Palancas!H18 = 0,14) es un dato de otras empresas, no un suelo de esta; Análisis!C56 + 0,10 = 0,19 es un umbral de aviso de la plantilla, no un techo económico; tres ejercicios propios no permiten decir qué ROIC sostendría esta empresa en el año 11. Lo que haría falta: ROIC por año de los informes 2015–2021 (notas de segmentos) y cualquier dato de la dirección sobre la duración de los contratos que sostienen el margen."}}
    ],
    "comprobacion_conjunta": {
      "procede": false,
      "combinacion": null,
      "coherencia_economica": null,
      "sobrevive": null
    },
    "resultado": "pendiente_de_investigacion",
    "hipotesis_que_mas_condiciona": "Palancas!D18",
    "que_lo_resolveria": "ROIC por año de los informes 2015–2021 (notas de segmentos) para completar Historia fila 33, y la duración media de los contratos que sostienen el margen (pregunta a Relación con Inversores)"
  },
  "estado_analisis": "pendiente_de_investigacion",
  "cubo_final": "Vigilar",
  "escalera": {"de": "precio.json"},
  "decision": {"accion": null, "precio_objetivo": null, "condicion": null, "condiciones_revision": {"al_alza": "…", "a_la_baja": "…"}},
  "insumos_decision_cartera": {"precio_actual": 494, "zona": "cumple_regla_k", "precio_de_si": 520, "precio_escenario_malo": 430, "ponderado": 610, "distancia_a_precio_si": -0.05, "distancia_a_malo": 0.13, "fundamento": "pendiente de investigación (ROIC LP BUENO sin base para acotar)", "datos_ausentes_materiales": [], "descalificadores_considerados": ["…"], "r": 0.09, "r_minima": 0.085, "palanca_mas_influyente": "ROIC / ROE largo plazo (±5 pts)"},
  "herencia": {"C93": {"etapa1": "Sí", "decision": "mantiene", "motivo": "misma_evidencia", "evidencia_y_razonamiento": "…"}, "B101": {…}, "B102": {…}, "C103": {…}, "C104": {…}},
  "comparacion_etapa_1": {"cubo_v1": "Vigilar", "precio_de_si_v1": 686, "cubo_v2": "Vigilar", "precio_de_si_v2": 520, "por_que_difieren": "…"},
  "celdas": {"C93": "Sí", "C103": "Sí", "C104": "Pendiente de decisión de cartera · conclusión del personaje: sin conclusión (pendiente de investigación) · zona cumple_regla_k · precio de Sí ≤ 520 · precio esc. MALO 430 · ponderado 610 · fundamento pendiente de investigación", "B101": "…", "B102": "…",
             "Palancas!A38": "…", "Palancas!B38": "2027-03-31", "Palancas!C38": 0.7, "Palancas!A39": "…", "Palancas!B39": "…", "Palancas!C39": 0.6, "Palancas!A40": "…", "Palancas!B40": "…", "Palancas!C40": 0.5,
             "Diagnóstico V6!B222": "…", "Diagnóstico V6!B223": "…"},
  "celdas_corregidas": {"C18": {"antes": "Sí", "despues": "Sí", "motivo": "…"}},
  "cambiaria_de_cubo": {"a_si": "…", "a_no": "…", "a_demasiado_dificil": "…"},
  "observaciones": {"C93": "…", "C103": "…", "C104": "…", "B101": "…", "B102": "…", "Palancas!A38": "…"}
}
```

Cuando la comprobación conjunta procede (todas las hipótesis con `hay_base = true` y conclusión provisional favorable), el primer turno rellena `comprobacion_conjunta.combinacion` (una sola combinación: celda → valor, cada uno dentro de su rango y en el extremo desfavorable a la tesis, o con la razón de no estarlo) y `coherencia_economica` (la historia única que hace compatibles esos valores); el script escribe `comprobacion_conjunta.json` (§D.6b) y el segundo turno copia `sobrevive` (booleano, el mismo de §D.6b) y rellena el resto. En el ejemplo, la conclusión provisional era `comprar` (precio 494 en zona `cumple_regla_k`); la primera hipótesis tiene rango con cada límite atado a hechos de la empresa, pero la segunda **no tiene base para acotarse** (y el ejemplo dice por qué no valen la media del sector ni el umbral de la plantilla): no procede la comprobación conjunta y el resultado es `pendiente_de_investigacion`, cubo `Vigilar`, acción `null`. `revision_datos_ausentes` (S-19) recorre cada dato de `datos_ausentes.json` con la conclusión afectada y el motivo; si alguno fuera material para la conclusión favorable, `alguno_material = true` y la fase C cerraría igual sin conclusión, con `C104` «… sin conclusión (pendiente de datos: <celdas>)», y el pipeline pondría `pendiente_de_datos`.

Vocabulario cerrado: `estado_analisis` ∈ {`concluido`, `pendiente_de_investigacion`, `modelo_no_aplicable`} desde la fase C (`concluido` es provisional: lo confirma el pipeline tras la auditoría APROBADO y hasta entonces no se escribe en la ficha; `pendiente_de_datos` y `no_entregable` los pone solo el pipeline; cuando la propia revisión de datos ausentes de la fase C declara `alguno_material = true` (S-19), la fase C escribe `estado_analisis = pendiente_de_datos` (único caso en que lo escribe ella; el pipeline lo confirma tras escribir las celdas de C) y cierra con `cubo_final = Vigilar` y `accion = null`, nunca con `Sí`/`comprar`); `cubo_final` ∈ {`Sí`, `Vigilar`, `No`, `Demasiado difícil`}, con `Sí` solo si `estado_analisis = concluido` y `accion = comprar`; `decision.accion` ∈ {`comprar`, `esperar`, `descartar`, `demasiado_dificil`, `null`}; `fundamento_material.resultado` ∈ {`sin_limitacion` (lista vacía), `comprobacion_conjunta_superada`, `pendiente_de_investigacion`, `no_procede` (conclusión provisional no favorable, o favorable bloqueada antes por un dato ausente material, S-19; si la comprobación se hizo igualmente, su escalera se informa como rango del precio de Sí y `resultado` sigue siendo `no_procede`)}. No existe ningún campo de tamaño de posición ni porcentaje alguno, tampoco «0 %» (D16). `revision_datos_ausentes.revisados` tiene una entrada por cada dato de `datos_ausentes.json` (el verificador lo comprueba). El mapa cubo ↔ acción ↔ estado está en el encargo, §8. `Palancas!C38:C40` es la probabilidad de que **cada predicción** se cumpla dado el escenario NORMAL.

## D.6b `comprobacion_conjunta.json` (lo escribe `comprobacion_conjunta.py`; D10, Anexo B §B.6)

Ejemplo construido sobre **la misma empresa y las mismas cifras de §D.6, suponiendo que la segunda hipótesis sí tuviera base** (cinco ejercicios de ROIC en `Historia` fila 33 en vez de tres): muestra qué habría hecho la comprobación conjunta. En el caso real de §D.6 no procede.

```json
{
  "libro_origen": "<E>_v63_evaluada.xlsx", "copia_de_prueba": "comprobacion_conjunta/<E>_conj.xlsx", "hash_copia": "…",
  "combinacion": {"B69": 0.4, "C69": 0.5, "D69": 0.1, "Palancas!D18": 0.14},
  "rangos_y_evidencia": {"B69:D69": {"rango": "MALO 0,2–0,4 · NORMAL 0,4–0,6 · BUENO 0,1–0,2", "evidencia": "p(MALO) techo 0,4: 4 de 10 ejercicios con crecimiento negativo O margen bajo el del MALO (Historia 2015–2024, filas 28–29: 2016, 2019, 2020, 2023); suelo 0,2: con las dos condiciones a la vez son 3 (2016, 2020, 2023), y 2020 fue el cierre por pandemia, no repetible según la dirección, con ventas recuperadas en 2021 (extracto p. 22): 2 de 10. p(BUENO) suelo 0,1: 1 de 10 (2021) cumplió a la vez crecimiento y margen del BUENO; techo 0,2: 2 de 10 (2017, 2021) cumplieron al menos una condición"}, "Palancas!D18": {"rango": "0,14–0,18", "evidencia": "techo 0,18 = el ROIC más alto de la propia serie de cinco ejercicios (Historia fila 33, 2021), que coincide con la tesis del BUENO: por encima de lo mejor que ya hizo, ningún hecho del extracto lo sostiene. Suelo 0,14 = el ROIC más bajo de la misma serie (2022, año de la subida de costes de materias primas, extracto p. 31), que la empresa sostuvo sin perder cuota ni precio: por debajo de lo que ya demostró en un mal año habría que suponer un deterioro que ningún hecho del extracto anuncia. La media del sector (H18) y el umbral C56 + 0,10 no se usan como límites."}},
  "coherencia_economica": "si el foso dura menos de lo que supone el BUENO, ese escenario es menos probable y su ROIC terminal cae al nivel del peor año propio; el MALO gana la probabilidad que pierde el BUENO; S2C y márgenes no mejoran a la vez que cae el ROIC",
  "recalculo_forzado_comprobado": true,
  "precio_actual": 494,
  "resultados_bajo_combinacion": {"B78": 430, "C78": 520, "D78": 900, "C83": 522, "Motor!B255": "COMPLETO Y VÁLIDO", "semaforos": ["…"], "errores_gramatica": []},
  "escalera_bajo_combinacion": {"P_estrella": 481.1, "precio_si": 481.1, "precio_escenario_malo": 430, "ponderado": 522, "zona_precio_actual": "vigilar"},
  "escalera_original": {"valores": [430, 520, 1060], "probabilidades": [0.2, 0.6, 0.2], "P_estrella": 540.8, "precio_si": 520, "precio_escenario_malo": 430, "ponderado": 610, "zona_precio_actual": "cumple_regla_k"},
  "sobrevive": false,
  "nota": "superar esta comprobación no es una garantía de seguridad; su fuerza depende de los rangos declarados"
}
```

`sobrevive` = la zona del precio actual bajo la combinación sigue siendo `cumple_regla_k` o `bajo_malo` y no aparece ningún error de gramática ni de mecánica. La copia de prueba no se entrega ni se verifica con `verificar_v63.py` (no hace falta: no sustituye al libro), pero se conserva para el estudio.

## D.7 `ficha.json` (para la capa entre empresas y el futuro Damodaran independiente)

Campos: `empresa`, `ticker`, `fecha`, `moneda`, `versiones` {`personaje`, `plantilla` = «V6.3», `gramatica`, `referencias_mecanicas`, `config`}, `hashes` {`libro_entrada`, `libro_evaluado`}, `estado_analisis` (§3.4), `causa_si_no_concluido` {`tipo`: falta_de_datos | incertidumbre_no_acotada | limite_del_modelo | fallo_de_implementacion, `detalle`}, `etapa1` {`cubo`, `precio_de_si`, `fecha`, `r`}, `cubo`, `cubo_cualitativo_fase_a`, `decision` (de D.6; en `modelo_no_aplicable` derivada de `fase_a.json` como dice §D.2; `accion` puede ser `null`), `insumos_decision_cartera` (de D.6), `motor`, `escenarios` {MALO / NORMAL / BUENO, cada uno: `historia`, `probabilidad`, `valor_accion`, `palancas` {`g15`, `m_obj`, `s2c`, `g_inf`, `roic_lp`, cada una {`referencia_mecanica`, `referencia_no_disponible_motivo`, `valor`, `desviacion`, `clase`, `confianza`}}}, `valor_ponderado`, `precio`, `escalera` (de `precio.json`, con `convencion`), `fundamento_material` (de D.6, con la lista completa) y `comprobacion_conjunta` (de D.6b si existe), `estado_libro`, `estado_evidencias`, `palanca_mas_influyente` {`nombre`, `clase`, `nota`: «información, no criterio»}, `semaforos` (lista), `salto_anio_11`, `peso_terminal`, `cambios_vs_etapa1` (las 34 celdas heredadas: {`celda`, `antes`, `despues`, `decision`, `motivo`, `evidencia_y_razonamiento`}), `predicciones` (3 × {`texto`, `fecha`, `prob`, `resultado`: null}), `incertidumbre_pendiente`, `que_lo_resolveria`, `cambiaria_de_cubo`, `autocomprobacion`, `recuento_clases` {`fundamentada`, `convencion`, `tecnico`, `sin_juicio`}, `desviaciones_justificadas` (número y lista), `avisos` (lista), `confianza_global`, `que_falta` (datos de etapa 1 o de fase 1 ausentes, con su nivel de §3.4), `revision_datos_ausentes` (de D.6: por dato, conclusión afectada, material o no, por qué), `citas` {`munger`: n, `damodaran`: n}. En los estados `pendiente_de_datos` y `modelo_no_aplicable` los campos que no existen van a `null`, nunca se inventan; en `pendiente_de_datos` tras la fase C (S-19), `decision.accion` = `null` y `causa_si_no_concluido.tipo` = `falta_de_datos` con `detalle` = los datos ausentes materiales, la conclusión que afectan y por qué.

## D.8 `informe.md` (trece secciones, en este orden; las que no aplican al estado se escriben con una línea «No aplica en estado …»)

1. Estado del análisis, cubo y conclusión en una línea (con precios si los hay). 2. Qué cambió respecto a la etapa 1 y por qué (con el motivo de D3). 3. Las seis preguntas. 4. Los tres escenarios contados. 5. Tabla de palancas: referencia mecánica → decisión → desviación → clase → por qué. 6. Lo que dice la hoja (semáforos, peso del terminal, salto del año 11, DCF inverso, tornado como información). 7. Escalera de precios (convención experimental), fundamento material (lista de hipótesis, alternativas, combinación y resultado de la comprobación conjunta, con la frase «no es una garantía de seguridad» si se superó) y los dos errores opuestos. 8. Tesis y tesis inversa. 9. Predicciones. 10. Qué me haría cambiar de cubo. 11. Autocomprobación. 12. Qué no sé y qué pediría (incluido qué no sabría Munger; la revisión de datos ausentes con qué afecta cada uno; en `pendiente_de_investigacion` o `pendiente_de_datos`, lo que haría falta para continuar). 13. Citas usadas (Munger y Damodaran, con página).

Sin preámbulos ni cierres. Frases cortas. Todo hecho con su fuente; todo juicio como juicio. Ningún tamaño de posición.

## D.9 `auditoria.md` (agente de verificación)

Lista numerada con PASA/FALLA y una línea cada una: (1) mecánica (todos los scripts PASS; `verificar_v63.py` íntegro; estado del libro el esperado según el encargo §7.3, con recálculo forzado comprobado); (2) literalidad de C11–C13; (3) herencia: cada celda heredada con «mantiene/cambia», motivo válido y evidencia nombrada (no «como ya se dijo»); (4) gramática: ningún error; toda desviación justificada con hechos y clase válida; límites del modelo tratados como tales; (5) coherencia de las 68 con las historias; (6) citas de Munger y Damodaran con página (grep); (7) tesis inversa con hechos; (8) nada de internet ni de memoria; (9) evidencia de fase 1 usada antes de decir «no consta»; (10) escalera coherente con `precio.json` y presentada como convención; (11) **fundamento material (D10)**: la lista `hipotesis_sin_fundamento` es completa (el verificador busca por su cuenta clases *sin juicio propio* / *técnico* y Observaciones sin hechos), cada límite de cada rango está atado a un hecho de esta empresa con la explicación de por qué acota (una media sectorial, un umbral de la plantilla o la variabilidad histórica por sí sola no valen), las limitaciones sin base están registradas con lo que haría falta, la combinación toma los extremos desfavorables o explica por qué no, es económicamente coherente, el resultado y el estado son los que corresponden, y ningún texto presenta la comprobación como garantía; (12) `C104` sin ningún porcentaje, tampoco «0 %», y ningún tamaño en ficha ni informe (D16); (13) predicciones falsables y sobre el negocio; (14) autocomprobación con contenido (no frases vacías); (15) comparación honesta con la etapa 1; (16) **revisión de datos ausentes (S-19)**: una entrada por cada dato de `datos_ausentes.json`, con conclusión afectada y motivo específico, y estado coherente con la materialidad declarada. Veredicto: APROBADO / REPETIR, y en una línea qué corregir. **Un FALLA en (1), (4), (11), (12) o (16) es REPETIR sin excepción.**

## D.10 `resumen_v2.csv`

`empresa, fecha, estado_analisis, causa_si_no_concluido, cubo_v1, cubo_v2, motor, precio, moneda, precio_escenario_malo, precio_si, ponderado, zona, accion, fundamento_material, estado_libro, palanca_mas_influyente, n_desviaciones, n_sin_juicio, n_tecnico, n_hipotesis_sin_fundamento, comprobacion_conjunta, n_datos_ausentes, n_datos_ausentes_materiales, intentos_B, intentos_C, verificacion, coste_estimado, tiempo_min`

## D.11 `diagnostico.md` y `diagnostico.json` (D18; siempre que `estado_analisis ≠ concluido`)

```json
{
  "empresa": "…", "fecha": "AAAA-MM-DD", "estado_analisis": "no_entregable",
  "causa": {"tipo": "fallo_de_implementacion", "detalle": "G2 (N2): ROIC largo plazo del MALO 0,02 ≤ g para siempre 0,025 tras 2 correcciones de la fase B; en las tres pasadas la fase B bajó el ROIC del MALO sin bajar su g", "comprobacion": "G2", "categoria": "error"},
  "paso_en_que_se_detuvo": 8,
  "intentos": {"fase_b": 3, "fase_c": 0, "auditoria": 0},
  "lo_que_sigue_valido": {"libro": "íntegro; celdas de la fase A escritas y verificadas", "cubo_cualitativo": "Vigilar", "descalificadores": "ninguno aplica", "gestion": "Buena", "seis_preguntas": true, "celdas_verificadas": ["C11", "…"]},
  "lo_que_no_es_valido": ["palancas de la fase B", "escalera"],
  "para_continuar": {"que_hace_falta": "revisar el prompt de la fase B en la regla N2 (si el ROIC a largo plazo de un escenario es ≤ g, ese escenario tiene que bajar g, no mantenerlo)", "desde_que_paso": 8, "quien": "Claude Code | José Luis (datos)"},
  "archivos": ["entrada_v63.md", "fase_a.json", "gramatica.md", "verificacion_*.txt"]
}
```

`causa.tipo` ∈ {`falta_de_datos`, `incertidumbre_no_acotada`, `limite_del_modelo`, `fallo_de_implementacion`}. `diagnostico.md` es la misma información en diez líneas legibles. Para `pendiente_de_investigacion` y `modelo_no_aplicable` el diagnóstico es breve y remite a la ficha y al informe, que existen; para `pendiente_de_datos` lista exactamente lo que falta (de `entrada_v63.md`) y, si viene de la revisión de la fase C (S-19), qué conclusión afecta cada dato y por qué, con `para_continuar` = de dónde debería salir el dato; para `no_entregable` dice qué falló, en qué paso y qué se conserva. Nunca «revisar el prompt» sin decir qué regla.
