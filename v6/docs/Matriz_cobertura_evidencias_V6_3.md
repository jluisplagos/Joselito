> Antecedente de la entrega previa a la corrección de la norma contable. Para el cambio y las pruebas actuales, consultar `Correccion_norma_contable.md`. Los hashes y resultados que siguen describen aquella entrega.

# Matriz de cobertura del control de evidencias · V6.3 (30-oct-2026)

Origen de la relación: `scripts/trazar_entradas_materiales.py` → `pruebas/relacion_independiente.json` (traza
estática del grafo de fórmulas + activación empírica por motor y configuración, 492 recálculos) y
`scripts/relacion_entradas_materiales.py` (relación curada con tipo y condición de uso). El inventario de
Control maestro (bloque 176+) se construye DESDE esa relación; las pruebas de la familia «9 · cobertura» se
generan DESDE la relación, no desde el inventario.

Resultado: **149 pruebas de cobertura, todas superadas**; batería completa 251 superadas · 0 fallidas · 0 no ejecutadas.

Columnas: *Empírica* = la perturbación de la celda movió alguna salida vigilada (motor: configuraciones en que lo hizo);
*Inv. 29-oct* = estaba en el inventario anterior; *Prueba* = caso «pendiente → NO LISTO (1 pendientes)» por motor/configuración.

| Entrada | Celda | Tipo | Motores | Condición de uso | Evidencia o confirmación exigida | Empírica | Inv. 29-oct | Prueba |
|---|---|---|---|---|---|---|---|---|
| precio | `Análisis!C37` | dato | A · B · C | siempre (lectura del precio) | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,adr,desviacion_capitalizacion · B: base,adr,desviacion_capitalizacion · C: base,adr,desviacion_capitalizacion | sí | A/base OK; B/base OK; C/base OK |
| capitalizacion | `Análisis!C41` | dato | A · B · C | siempre (bloquea el valor si falta; peso de financiación en B) | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | B: base,adr,desviacion_capitalizacion | sí | A/base OK; B/base OK; C/base OK |
| acciones | `Análisis!C55` | dato | A · B · C | siempre | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,desviacion_capitalizacion · B: base,desviacion_capitalizacion · C: base,desviacion_capitalizacion | sí | A/base OK; B/base OK; C/base OK |
| cfo_media | `Análisis!C46` | dato | A | siempre en A (FCF base) | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | A: base | sí | A/base OK |
| capex_media | `Análisis!C47` | dato | A | siempre en A | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | A: base | sí | A/base OK |
| int_fin_media | `Análisis!C48` | dato | A | siempre en A (0 explícito si no hay) | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | A: base | sí | A/base OK |
| leases_media | `Análisis!C49` | dato | A | siempre en A (0 explícito si no hay) | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | A: base | sí | A/base OK |
| sbc_media | `Análisis!C50` | dato | A | siempre en A (0 explícito si no hay) | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | A: base | sí | A/base OK |
| h_anios | `Historia!C5:L5` | dato | A · B · C | siempre (años consecutivos, el último en L) | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | A: base · B: base · C: base | sí | A/base OK; B/base OK; C/base OK |
| h_ventas | `Historia!C6:L6` | dato | A · B | A y B | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,fcf_negativo_normalizado · B: base | sí | A/base OK; B/base OK |
| h_ebit | `Historia!C7:L7` | dato | A · B | A y B | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,fcf_negativo_normalizado · B: base | sí | A/base OK; B/base OK |
| h_da | `Historia!C8:L8` | dato | A | A | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,fcf_negativo_normalizado | sí | A/base OK |
| h_beneficio | `Historia!C9:L9` | dato | C | C | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | C: base | sí | C/base OK |
| h_tipo | `Historia!C10:L10` | dato | A · B | A y B | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,fcf_negativo_normalizado · B: base | sí | A/base OK; B/base OK |
| h_capex | `Historia!C12:L12` | dato | A | A | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,fcf_negativo_normalizado | sí | A/base OK |
| h_circulante | `Historia!C14:L14` | dato | A | A | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,fcf_negativo_normalizado | sí | A/base OK |
| h_intereses | `Historia!C15:L15` | dato | B | B | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | B: base | sí | B/base OK |
| h_patrimonio | `Historia!C21:L21` | dato | C | C | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | C: base | sí | C/base OK |
| h_deuda | `Historia!C22:L22` | dato | B | B | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | B: base | sí | B/base OK |
| h_arrend | `Historia!C23:L23` | dato | B | B | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | B: base | sí | B/base OK |
| h_caja | `Historia!C24:L24` | dato | B | B | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | B: base | sí | B/base OK |
| h_pensiones | `Historia!C25:L25` | dato | B | B | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | B: base | sí | B/base OK |
| h_minoritarios | `Historia!C26:L26` | dato | B | B | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | B: base | sí | B/base OK |
| moneda_cotizacion | `Palancas!C48` | dato | A · B · C | siempre (comparabilidad; en B también el valor) | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,adr · B: base,adr · C: base,adr | **no** | A/base OK; B/base OK; C/base OK |
| moneda_modelo | `'Control maestro'!H4` | dato | A · B · C | siempre | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | — (traza estática + razonamiento) | **no** | A/base OK; B/base OK; C/base OK |
| ratio_adr | `'Control maestro'!D5` | dato | A · B · C | si Palancas C47 = «ADR o ADS» o D5 informado | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | A: adr · B: adr · C: adr | **no** | A/adr OK; B/adr OK; C/adr OK |
| unidad | `'Control maestro'!J4` | dato | A · B · C | siempre (metadato: sin él ninguna cifra se interpreta) | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | — (traza estática + razonamiento) | **no** | A/base OK; B/base OK; C/base OK |
| norma | `'Control maestro'!L4` | dato | A · B · C | siempre (metadato: IFRS / US GAAP cambia intereses y arrendamientos) | «Rellenado y verificado» + documento en J; o «Estimación declarada» + justificación (PROVISIONAL) | — (traza estática + razonamiento) | **no** | A/base OK; B/base OK; C/base OK |
| motor | `Análisis!C62` | hipótesis | A · B · C | siempre (elección del motor) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base · B: base · C: base | **no** | A/base OK; B/base OK; C/base OK |
| r | `Análisis!C56` | hipótesis | A · B · C | siempre (r exigida; en B entra en la r operativa) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,quiebra · B: base,quiebra · C: base,quiebra | **no** | A/base OK; B/base OK; C/base OK |
| caso_especial | `Palancas!C6` | hipótesis | A · B · C | siempre (aplicabilidad del motor: «Financiera» bloquea A y B) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | — (traza estática + razonamiento) | **no** | A/base OK; B/base OK; C/base OK |
| base_margen | `Palancas!C8` | hipótesis | A · B | A y B (margen de partida: último año o media del ciclo) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | — (traza estática + razonamiento) | **no** | A/base OK; B/base OK |
| anios_f | `Historia!C57` | hipótesis | A | A (ventana que calibra f) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,fcf_negativo_normalizado | **no** | A/base OK |
| restar_sbc | `Análisis!C51` | hipótesis | A | A, si la SBC (C50) no es 0 | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base | **no** | A/base OK |
| crec_MALO | `Palancas!B14` | hipótesis | A · B · C | siempre | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base · B: base · C: base | **no** | A/base OK; B/base OK; C/base OK |
| margen_MALO | `Palancas!B15` | hipótesis | A · B · C | siempre (margen objetivo; ROE objetivo en C) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base · B: base · C: base | **no** | A/base OK; B/base OK; C/base OK |
| s2c_MALO | `Palancas!B16` | hipótesis | A · B | A y B (reinversión) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base · B: base | **no** | A/base OK; B/base OK |
| roic_MALO | `Palancas!B18` | hipótesis | A · B · C | siempre (rentabilidad terminal) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,id_capitalizada · B: base,id_capitalizada · C: base,id_capitalizada | **no** | A/base OK; B/base OK; C/base OK |
| g_MALO | `Análisis!B68` | hipótesis | A · B · C | siempre (crecimiento terminal) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base · B: base · C: base | **no** | A/base OK; B/base OK; C/base OK |
| prob_MALO | `Análisis!B69` | hipótesis | A · B · C | siempre (ponderación) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,quiebra · B: base,quiebra · C: base,quiebra | **no** | A/base OK; B/base OK; C/base OK |
| crec_NORMAL | `Palancas!C14` | hipótesis | A · B · C | siempre | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base · B: base · C: base | **no** | A/base OK; B/base OK; C/base OK |
| margen_NORMAL | `Palancas!C15` | hipótesis | A · B · C | siempre (margen objetivo; ROE objetivo en C) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base · B: base · C: base | **no** | A/base OK; B/base OK; C/base OK |
| s2c_NORMAL | `Palancas!C16` | hipótesis | A · B | A y B (reinversión) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base · B: base | **no** | A/base OK; B/base OK |
| roic_NORMAL | `Palancas!C18` | hipótesis | A · B · C | siempre (rentabilidad terminal) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,id_capitalizada · B: base,id_capitalizada · C: base,id_capitalizada | **no** | A/base OK; B/base OK; C/base OK |
| g_NORMAL | `Análisis!C68` | hipótesis | A · B · C | siempre (crecimiento terminal) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base · B: base · C: base | **no** | A/base OK; B/base OK; C/base OK |
| prob_NORMAL | `Análisis!C69` | hipótesis | A · B · C | siempre (ponderación) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,quiebra · B: base,quiebra · C: base,quiebra | **no** | A/base OK; B/base OK; C/base OK |
| crec_BUENO | `Palancas!D14` | hipótesis | A · B · C | siempre | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base · B: base · C: base | **no** | A/base OK; B/base OK; C/base OK |
| margen_BUENO | `Palancas!D15` | hipótesis | A · B · C | siempre (margen objetivo; ROE objetivo en C) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base · B: base · C: base | **no** | A/base OK; B/base OK; C/base OK |
| s2c_BUENO | `Palancas!D16` | hipótesis | A · B | A y B (reinversión) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base · B: base | **no** | A/base OK; B/base OK |
| roic_BUENO | `Palancas!D18` | hipótesis | A · B · C | siempre (rentabilidad terminal) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,id_capitalizada · B: base,id_capitalizada · C: base,id_capitalizada | **no** | A/base OK; B/base OK; C/base OK |
| g_BUENO | `Análisis!D68` | hipótesis | A · B · C | siempre (crecimiento terminal) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base · B: base · C: base | **no** | A/base OK; B/base OK; C/base OK |
| prob_BUENO | `Análisis!D69` | hipótesis | A · B · C | siempre (ponderación) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,quiebra · B: base,quiebra · C: base,quiebra | **no** | A/base OK; B/base OK; C/base OK |
| p_quiebra | `Palancas!C22` | hipótesis | A · B · C | si está informada y es > 0 (vacía = 0 por convención, con aviso) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,quiebra · B: base,quiebra · C: base,quiebra | **no** | A/quiebra OK; B/quiebra OK; C/quiebra OK |
| recuperacion | `Palancas!C23` | hipótesis | A · B · C | si la probabilidad de quiebra es > 0 | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: quiebra · B: quiebra · C: quiebra | **no** | A/quiebra OK; B/quiebra OK; C/quiebra OK |
| exceso_caja | `Análisis!C76` | hipótesis | A | A, si está informado y no es 0 | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: base,exceso_caja | **no** | A/exceso_caja OK |
| naturaleza_fcf | `Palancas!C43` | hipótesis | A | A, si el FCF base (Análisis C52) ≤ 0 | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | — (traza estática + razonamiento) | **no** | A/fcf_neg OK |
| fcf_normalizado | `Palancas!C44` | hipótesis | A | A, si C52 ≤ 0 y la naturaleza es Transitorio o Extraordinario (calibra f) | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: fcf_negativo_normalizado | **no** | A/fcf_neg OK |
| causa_desviacion | `Palancas!C47` | hipótesis | A · B · C | si la desviación capitalización ÷ (precio × acciones) supera el umbral (Diagnóstico C91) o hay causa declarada | «Hipótesis confirmada» + justificación en J, M o N; o «Estimación declarada» + justificación (PROVISIONAL) | A: desviacion_capitalizacion · B: desviacion_capitalizacion · C: desviacion_capitalizacion | **no** | A/adr OK; A/desviacion OK; B/adr OK; B/desviacion OK; C/adr OK; C/desviacion OK |

## Casos positivos y de clasificación

| Caso | Comprobaciones | Resultado |
|---|---|---|
| N1_solo_datos_documentados_B_no_basta | `Motor!B269` contiene «hipótesis confirmadas 0 de 22»; `Motor!B266` empieza por «NO LISTO» | SUPERADA |
| N1_datos_e_hipotesis_B_LISTO | `Motor!B269` empieza por «documentadas 17 de 17 · hipótesis confirmadas 22 de 22»; `Motor!B266` 'LISTO' | SUPERADA |
| N1_datos_e_hipotesis_A_LISTO | `Motor!B269` empieza por «documentadas 19 de 19 · hipótesis confirmadas 24 de 24»; `Motor!B266` 'LISTO' | SUPERADA |
| N1_datos_e_hipotesis_C_LISTO | `Motor!B269` empieza por «documentadas 10 de 10 · hipótesis confirmadas 18 de 18»; `Motor!B266` 'LISTO'; `Análisis!C83` 17.8908417409 | SUPERADA |
| N4_receta_B_r_y_crecimiento_pendientes | `Motor!B266` empieza por «NO LISTO · evidencias incompletas»; `Motor!B269` empieza por «INCOMPLETAS»; `Análisis!C83` 30.7047681226 | SUPERADA |
| N4_receta_A_FCF_normalizado_no_verificable | `Motor!B266` empieza por «NO LISTO · evidencias incompletas»; `Motor!B269` contiene «1 no verificables»; `Análisis!C83` 53.9956252725; `Historia!C71` contiene «Palancas C | SUPERADA |
| N4_receta_A_FCF_normalizado_estimacion_justificada | `Motor!B266` empieza por «LISTO · PROVISIONAL (1 estimaciones»; `Análisis!C83` 53.9956252725 | SUPERADA |
| N4_exceso_de_caja_sin_confirmar | `Motor!B266` empieza por «NO LISTO · evidencias incompletas (1 pendientes)»; `Análisis!C83` 26.3903521530 | SUPERADA |
| N4_hipotesis_marcada_como_hecho_es_incoherente | `Motor!B266` empieza por «NO LISTO · evidencias incompletas (1 pendientes)»; `Control maestro!L208` contiene «incoherente» | SUPERADA |
| N4_hipotesis_sin_justificar | `Motor!B266` empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | SUPERADA |
| COB_base_A_todo_confirmado_LISTO | `Motor!B266` 'LISTO'; `Motor!B255` 'COMPLETO Y VÁLIDO' | SUPERADA |
| COB_base_B_todo_confirmado_LISTO | `Motor!B266` 'LISTO'; `Motor!B255` 'COMPLETO Y VÁLIDO' | SUPERADA |
| COB_base_C_todo_confirmado_LISTO | `Motor!B266` 'LISTO'; `Motor!B255` 'COMPLETO Y VÁLIDO' | SUPERADA |
| COB_quiebra_A_todo_confirmado_LISTO | `Motor!B266` 'LISTO'; `Motor!B255` 'COMPLETO Y VÁLIDO' | SUPERADA |
| COB_quiebra_B_todo_confirmado_LISTO | `Motor!B266` 'LISTO'; `Motor!B255` 'COMPLETO Y VÁLIDO' | SUPERADA |
| COB_quiebra_C_todo_confirmado_LISTO | `Motor!B266` 'LISTO'; `Motor!B255` 'COMPLETO Y VÁLIDO' | SUPERADA |
| COB_fcf_neg_A_todo_confirmado_LISTO | `Motor!B266` 'LISTO'; `Motor!B255` 'COMPLETO Y VÁLIDO' | SUPERADA |
| COB_exceso_caja_A_todo_confirmado_LISTO | `Motor!B266` 'LISTO'; `Motor!B255` 'COMPLETO Y VÁLIDO' | SUPERADA |
| COB_adr_A_todo_confirmado_LISTO | `Motor!B266` 'LISTO'; `Motor!B255` 'COMPLETO Y VÁLIDO' | SUPERADA |
| COB_adr_B_todo_confirmado_LISTO | `Motor!B266` 'LISTO'; `Motor!B255` 'COMPLETO Y VÁLIDO' | SUPERADA |
| COB_adr_C_todo_confirmado_LISTO | `Motor!B266` 'LISTO'; `Motor!B255` 'COMPLETO Y VÁLIDO' | SUPERADA |
| COB_desviacion_A_todo_confirmado_LISTO | `Motor!B266` 'LISTO'; `Motor!B255` 'COMPLETO Y VÁLIDO' | SUPERADA |
| COB_desviacion_B_todo_confirmado_LISTO | `Motor!B266` 'LISTO'; `Motor!B255` 'COMPLETO Y VÁLIDO' | SUPERADA |
| COB_desviacion_C_todo_confirmado_LISTO | `Motor!B266` 'LISTO'; `Motor!B255` 'COMPLETO Y VÁLIDO' | SUPERADA |
| COB_no_aplicable_legitimo_DA_en_B | `Motor!B266` 'LISTO' | SUPERADA |
| COB_no_aplicable_legitimo_S2C_en_C | `Motor!B266` 'LISTO' | SUPERADA |
| COB_no_aplicable_indebido_r_en_C | `Motor!B266` empieza por «NO LISTO · evidencias incompletas (1 pendientes)»; `Motor!B269` contiene «1 «No aplicable» indebido» | SUPERADA |
| COB_no_verificable_crecimiento_en_A | `Motor!B266` empieza por «NO LISTO · evidencias incompletas (1 pendientes)»; `Motor!B269` contiene «1 no verificables» | SUPERADA |
| COB_estimacion_sin_justificar_margen_en_B | `Motor!B266` empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | SUPERADA |
| COB_estimacion_justificada_ROIC_en_C_provisional | `Motor!B266` empieza por «LISTO · PROVISIONAL (1 estimaciones» | SUPERADA |
| COB_quiebra_vacia_no_exige_confirmacion | `Motor!B266` 'LISTO'; `Palancas!C22` sin valor | SUPERADA |

## Exclusiones: entradas editables fuera del control, y por qué

| Entradas | Motivo |
|---|---|
| Análisis C11:C13 (filtro Pabrai) | gate de dominio (solo «Sí»/«No» exactos); lo controla el estado de inversión, no la evidencia |
| Análisis B65:D66, B101, B102, C14, C17:C20, C24:C28, C31:C34, C93, C96:C98, C103, C104 | juicios cualitativos y completitud (nivel 3): no mueven el valor ni la lectura del precio |
| Análisis C38, C40, C42, C53, C54, C57, C60, C88 | indicadores auxiliares (fuente externa, FCF yield, múltiplos, tasa sin riesgo): no mueven las salidas vigiladas |
| Historia filas 11, 13, 16, 17, 18, 19, 20 | anclas informativas (S2C marginal, FCF histórico, ROIC con I+D): sin efecto en las salidas |
| Palancas C5, C7, C9, C10, C24, C45, C46, A28:B33, A38:C40 | pistas, sector, I+D en anclas, cuota implícita, fechas (solo aviso), países (r mínima), predicciones: sin efecto en las salidas |
| Panel C6, F6, E20:E25 | visualización y modo estudio: no tocan la hipótesis base (R05) |
| Diagnóstico V6 C91:C94, C158, C179, B222:C223 | parámetros de diseño visibles (el verificador informa sus cambios) y líneas de juicio libre |
| Control maestro E:N de la trazabilidad | es la documentación misma |
| Palancas C22 vacía | convención deliberada: probabilidad de quiebra 0 con aviso visible; se exige confirmación solo cuando se informa > 0 |
| Análisis C76 vacío o 0 | convención deliberada: sin exceso de caja; se exige confirmación solo cuando se informa ≠ 0 |

## Entradas que la activación empírica movió y no están en la relación

- `Análisis!C11`: gate de dominio del filtro Pabrai (solo «Sí»/«No» exactos): al perturbar el texto el libro pasa a DATOS INVÁLIDOS; lo controla el estado de inversión (tres «Sí» explícitos), no la evidencia.
- `Análisis!C12`: gate de dominio del filtro Pabrai (solo «Sí»/«No» exactos): al perturbar el texto el libro pasa a DATOS INVÁLIDOS; lo controla el estado de inversión (tres «Sí» explícitos), no la evidencia.
- `Análisis!C13`: gate de dominio del filtro Pabrai (solo «Sí»/«No» exactos): al perturbar el texto el libro pasa a DATOS INVÁLIDOS; lo controla el estado de inversión (tres «Sí» explícitos), no la evidencia.

## Omisiones del inventario anterior (29-oct) respecto a la relación

35 entradas, todas ahora cubiertas: `Palancas!C48`, `'Control maestro'!H4`, `'Control maestro'!D5`, `'Control maestro'!J4`, `'Control maestro'!L4`, `Análisis!C62`, `Análisis!C56`, `Palancas!C6`, `Palancas!C8`, `Historia!C57`, `Análisis!C51`, `Palancas!B14`, `Palancas!B15`, `Palancas!B16`, `Palancas!B18`, `Análisis!B68`, `Análisis!B69`, `Palancas!C14`, `Palancas!C15`, `Palancas!C16`, `Palancas!C18`, `Análisis!C68`, `Análisis!C69`, `Palancas!D14`, `Palancas!D15`, `Palancas!D16`, `Palancas!D18`, `Análisis!D68`, `Análisis!D69`, `Palancas!C22`, `Palancas!C23`, `Análisis!C76`, `Palancas!C43`, `Palancas!C44`, `Palancas!C47`.

La relación y el inventario coinciden entrada por entrada (el inventario se genera desde la relación);
lo que la familia 9 comprueba es que las fórmulas de Excel aplican de verdad cada condición de uso.