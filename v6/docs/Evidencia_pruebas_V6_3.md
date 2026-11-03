> Antecedente de la entrega previa a la corrección de la norma contable. Para el cambio y las pruebas actuales, consultar `Correccion_norma_contable.md`. Los hashes y resultados que siguen describen aquella entrega.

# Evidencia de pruebas · V6.3 (30-oct-2026)

Ejecución final sobre los entregables ya empaquetados (con deslizadores), con la referencia aprobada
`referencia_V6.3.json` generada de la misma plantilla (mismo SHA-256). Entorno: LibreOffice 24.2.7.2
headless, openpyxl 3.1.5, Python 3. Las carpetas de salida se vacían al empezar: no hay recálculos
reutilizados. Cada caso declara su esperado en `run_tests_v63.py` antes de ejecutarse; la familia 9 se
genera desde `relacion_entradas_materiales.py`, no desde el inventario que verifica. La batería se ejecutó
en dos tandas (familias 1–8 y familia 9) y se unió con `unir_resultados.py`.

## Archivos probados (SHA-256)

- `Ejemplo_ABB_V6.3.xlsx` · `5b1c66aa855d2708aa05ee524ca61b7a8888f0a4e68a7b3f03df8b080e90cd09`
- `Ejemplo_V6.3_EmpresaX.xlsx` · `d99bc648f70f2e562172fbfda0961a6b8261f1be3336d269c55d5af47fadce1a`
- `Ejemplo_migracion_Hermes_V6.3.xlsx` · `9e944384f166a5407b6acbdc888e53fa22527926b9cd5f92f12806f5f94f2df4`
- `Plantilla_V6.3.xlsx` · `128f4a0f12088c13de237ea82c03c18614745b351a173964a43d3cd8782e9087`
- `referencia_V6.3.json` · `03f40e9df6e386480a92bb10cd518f86b29ae790de3c7e3e547e41e5f2e8f0d4` (origen: `Plantilla_V6.3.xlsx` `128f4a0f12088c13…`)

**251 superadas · 0 fallidas · 0 no ejecutadas · total 251**

| Familia | Casos | Superadas |
|---|---|---|
| 1 · fallos nuevos | 26 | 26 |
| 2 · fallos anteriores | 14 | 14 |
| 3 · evidencias | 12 | 12 |
| 4 · vacía y combinaciones | 13 | 13 |
| 5 · referencias | 5 | 5 |
| 6 · invariantes | 21 | 21 |
| 7 · integridad | 9 | 9 |
| 8 · visualización | 2 | 2 |
| 9 · cobertura | 149 | 149 |

## Casos

| Caso | Familia | Base | Motor | Entradas modificadas | Celda | Esperado | Obtenido | Resultado |
|---|---|---|---|---|---|---|---|---|
| N1_evidencias_receta_motorB | 1 · fallos nuevos | EmpresaX | B | función: receta_evidencias | `Motor!B269` | empieza por «INCOMPLETAS» | `INCOMPLETAS · datos 8 de 17 · hipótesis confirmadas 0 de 22 · 0 estima…` | OK |
|  |  |  |  |  | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas» | `NO LISTO · evidencias incompletas (31 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Análisis!C83` | 30.7047681226 | `30.7047681226` | OK |
| N1_evidencias_receta_motorA | 1 · fallos nuevos | EmpresaX | A | función: receta_evidencias | `Motor!B269` | contiene «1 no verificables» | `INCOMPLETAS · datos 14 de 19 · hipótesis confirmadas 0 de 24 · 0 estim…` | OK |
|  |  |  |  |  | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas» | `NO LISTO · evidencias incompletas (29 pendientes) · cálculo completo` | OK |
| N1_solo_datos_documentados_B_no_basta | 1 · fallos nuevos | EmpresaX | B | función: <lambda> | `Motor!B269` | contiene «hipótesis confirmadas 0 de 22» | `INCOMPLETAS · datos 17 de 17 · hipótesis confirmadas 0 de 22 · 0 estim…` | OK |
|  |  |  |  |  | `Motor!B266` | empieza por «NO LISTO» | `NO LISTO · evidencias incompletas (22 pendientes) · cálculo completo` | OK |
| N1_datos_e_hipotesis_B_LISTO | 1 · fallos nuevos | EmpresaX | B | función: documentar_B | `Motor!B269` | empieza por «documentadas 17 de 17 · hipótesis confirmadas 22 de 22» | `documentadas 17 de 17 · hipótesis confirmadas 22 de 22 (declarado por …` | OK |
|  |  |  |  |  | `Motor!B266` | 'LISTO' | `LISTO` | OK |
| N1_datos_e_hipotesis_A_LISTO | 1 · fallos nuevos | EmpresaX | A | función: documentar_A | `Motor!B269` | empieza por «documentadas 19 de 19 · hipótesis confirmadas 24 de 24» | `documentadas 19 de 19 · hipótesis confirmadas 24 de 24 (declarado por …` | OK |
|  |  |  |  |  | `Motor!B266` | 'LISTO' | `LISTO` | OK |
| N1_datos_e_hipotesis_C_LISTO | 1 · fallos nuevos | EmpresaX | C | función: <lambda> | `Motor!B269` | empieza por «documentadas 10 de 10 · hipótesis confirmadas 18 de 18» | `documentadas 10 de 10 · hipótesis confirmadas 18 de 18 (declarado por …` | OK |
|  |  |  |  |  | `Motor!B266` | 'LISTO' | `LISTO` | OK |
|  |  |  |  |  | `Análisis!C83` | 17.8908417409 | `17.8908417409` | OK |
| N4_receta_B_r_y_crecimiento_pendientes | 1 · fallos nuevos | EmpresaX | B | función: receta_B_cobertura | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas» | `NO LISTO · evidencias incompletas (26 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B269` | empieza por «INCOMPLETAS» | `INCOMPLETAS · datos 13 de 17 · hipótesis confirmadas 0 de 22 · 0 estim…` | OK |
|  |  |  |  |  | `Análisis!C83` | 30.7047681226 | `30.7047681226` | OK |
| N4_receta_A_FCF_normalizado_no_verificable | 1 · fallos nuevos | EmpresaX | A | función: receta_A_cobertura | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas» | `NO LISTO · evidencias incompletas (30 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B269` | contiene «1 no verificables» | `INCOMPLETAS · datos 15 de 19 · hipótesis confirmadas 0 de 26 · 0 estim…` | OK |
|  |  |  |  |  | `Análisis!C83` | 53.9956252725 | `53.9956252725` | OK |
|  |  |  |  |  | `Historia!C71` | contiene «Palancas C44» | `Palancas C44 (FCF normalizado · Transitorio)` | OK |
| N4_receta_A_FCF_normalizado_estimacion_justificada | 1 · fallos nuevos | EmpresaX | A | función: receta_A_estimacion_justificada | `Motor!B266` | empieza por «LISTO · PROVISIONAL (1 estimaciones» | `LISTO · PROVISIONAL (1 estimaciones justificadas)` | OK |
|  |  |  |  |  | `Análisis!C83` | 53.9956252725 | `53.9956252725` | OK |
| N4_exceso_de_caja_sin_confirmar | 1 · fallos nuevos | EmpresaX | A | función: <lambda> | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Análisis!C83` | 26.3903521530 | `26.390352153` | OK |
| N4_hipotesis_marcada_como_hecho_es_incoherente | 1 · fallos nuevos | EmpresaX | B | función: <lambda> | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Control maestro!L208` | contiene «incoherente» | `incoherente: hipótesis marcada como hecho` | OK |
| N4_hipotesis_sin_justificar | 1 · fallos nuevos | EmpresaX | B | función: <lambda> | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
| N1_filas_121_124_restauradas | 1 · fallos nuevos | EmpresaX | — | — | `Control maestro!B122` | 'Historia!C20:L20' | `Historia!C20:L20` | OK |
|  |  |  |  |  | `Control maestro!B123` | 'Historia!C21:L21' | `Historia!C21:L21` | OK |
|  |  |  |  |  | `Control maestro!B124` | 'Historia!C22:L22' | `Historia!C22:L22` | OK |
|  |  |  |  |  | `Control maestro!A121` | 'Historia' | `Historia` | OK |
|  |  |  |  |  | `Control maestro!C122` | 'Acciones diluidas (mm)' | `Acciones diluidas (mm)` | OK |
| N2_C58_cero_bloquea | 1 · fallos nuevos | EmpresaX | A | función: <lambda> | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'DATOS INVÁLIDOS' | `DATOS INVÁLIDOS` | OK |
|  |  |  |  |  | `Motor!B256` | contiene «conciliación de f no cuadra» | `La conciliación de f no cuadra (Historia C81): la fórmula de Historia …` | OK |
|  |  |  |  |  | `Historia!C81` | contiene «no cuadra» | `⛔ TÉCNICO · la conciliación no cuadra` | OK |
| N2_C58_formula_falsa_bloquea | 1 · fallos nuevos | EmpresaX | A | función: <lambda> | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'DATOS INVÁLIDOS' | `DATOS INVÁLIDOS` | OK |
| N2_conciliacion_no_evaluable_no_bloquea | 1 · fallos nuevos | EmpresaX | A | `Historia!C8`=None; `Historia!D8`=None; `Historia!E8`=None… | `Historia!C81` | '—' | `—` | OK |
|  |  |  |  |  | `Motor!B255` | 'INCOMPLETO' | `INCOMPLETO` | OK |
|  |  |  |  |  | `Motor!B256` | no contiene «conciliación» | `Motor A: faltan amortizaciones D&A (fila 8) en algún año de la ventana…` | OK |
| N3_L22_deuda_negativa | 1 · fallos nuevos | EmpresaX | B | `Historia!L22`=-200 | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'DATOS INVÁLIDOS' | `DATOS INVÁLIDOS` | OK |
|  |  |  |  |  | `Motor!B256` | contiene «deuda BRUTA» | `Deuda financiera negativa en Historia fila 22: la plantilla pide deuda…` | OK |
| N3_L23_arrendamientos_negativos | 1 · fallos nuevos | EmpresaX | B | `Historia!L23`=-10 | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'DATOS INVÁLIDOS' | `DATOS INVÁLIDOS` | OK |
| N3_L24_caja_negativa | 1 · fallos nuevos | EmpresaX | B | `Historia!L24`=-5 | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B256` | contiene «Caja negativa» | `Caja negativa en Historia fila 24: la caja es un saldo ≥ 0; un descubi…` | OK |
| N3_E12_capex_negativo | 1 · fallos nuevos | EmpresaX | A | `Historia!E12`=-3 | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B256` | contiene «Capex negativo» | `Capex negativo en Historia fila 12: la plantilla pide el capex en posi…` | OK |
| N3_E8_DA_negativa_fuera_de_ventana | 1 · fallos nuevos | EmpresaX | A | `Historia!C8`=-1 | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'DATOS INVÁLIDOS' | `DATOS INVÁLIDOS` | OK |
| N3_circulante_negativo_permitido | 1 · fallos nuevos | EmpresaX | A | `Historia!E14`=-3 | `Análisis!C83` | un número | `25.890352153` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| N3_adquisiciones_negativas_permitidas | 1 · fallos nuevos | EmpresaX | A | `Historia!E13`=-30 | `Análisis!C83` | un número | `25.890352153` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| N3_CFO_negativo_permitido | 1 · fallos nuevos | EmpresaX | A | `Historia!C11`=-50 | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| N3_superavit_pensiones_es_cero_con_aviso | 1 · fallos nuevos | EmpresaX | B | `Historia!L25`=-40 | `Análisis!C83` | 30.7047681226 | `30.7047681226` | OK |
|  |  |  |  |  | `Historia!C65` | 0.0000000000 | `0` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
|  |  |  |  |  | `__libro__` | aviso de superávit de pensiones en las causas activas | `—` | OK |
| N3_deficit_pensiones_se_resta | 1 · fallos nuevos | EmpresaX | B | `Historia!L25`=40 | `Análisis!C83` | 30.3047681226 | `30.3047681226` | OK |
|  |  |  |  |  | `Historia!C65` | 40.0000000000 | `40` | OK |
| A1_amortizaciones_ausentes | 2 · fallos anteriores | EmpresaX | A | `Historia!C8`=None; `Historia!D8`=None; `Historia!E8`=None… | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'INCOMPLETO' | `INCOMPLETO` | OK |
|  |  |  |  |  | `Motor!B256` | contiene «amortizaciones» | `Motor A: faltan amortizaciones D&A (fila 8) en algún año de la ventana…` | OK |
| A2_amortizacion_parcial | 2 · fallos anteriores | EmpresaX | A | `Historia!L8`=None | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B256` | contiene «amortizaciones» | `Motor A: faltan amortizaciones D&A (fila 8) en algún año de la ventana…` | OK |
| B1_caja_ausente | 2 · fallos anteriores | EmpresaX | B | `Historia!L24`=None | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B256` | contiene «caja del último año» | `Motor B: falta la caja del último año (Historia L24); una caja descono…` | OK |
| C1_monedas_distintas_B | 2 · fallos anteriores | EmpresaX | B | `Palancas!C48`='USD'; `Control maestro!H4`='EUR' | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'DATOS INVÁLIDOS' | `DATOS INVÁLIDOS` | OK |
|  |  |  |  |  | `Motor!B256` | contiene «pesos de financiación» | `Motor B: la capitalización está en USD y la deuda en EUR: los pesos de…` | OK |
| C2_monedas_distintas_A_solo_lectura | 2 · fallos anteriores | EmpresaX | A | `Palancas!C48`='USD'; `Control maestro!H4`='EUR' | `Análisis!C83` | 25.8903521530 | `25.890352153` | OK |
|  |  |  |  |  | `Análisis!C84` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B253` | False | `False` | OK |
| A3_fila12_ausente | 2 · fallos anteriores | EmpresaX | A | `Historia!C12`=None; `Historia!D12`=None; `Historia!E12`=None… | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'INCOMPLETO' | `INCOMPLETO` | OK |
| A3_fila14_ausente | 2 · fallos anteriores | EmpresaX | A | `Historia!C14`=None; `Historia!D14`=None; `Historia!E14`=None… | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'INCOMPLETO' | `INCOMPLETO` | OK |
| B2_L22_ausente | 2 · fallos anteriores | EmpresaX | B | `Historia!L22`=None | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'INCOMPLETO' | `INCOMPLETO` | OK |
| B2_L23_ausente | 2 · fallos anteriores | EmpresaX | B | `Historia!L23`=None | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'INCOMPLETO' | `INCOMPLETO` | OK |
| B2_L25_ausente | 2 · fallos anteriores | EmpresaX | B | `Historia!L25`=None | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'INCOMPLETO' | `INCOMPLETO` | OK |
| B2_L26_ausente | 2 · fallos anteriores | EmpresaX | B | `Historia!L26`=None | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'INCOMPLETO' | `INCOMPLETO` | OK |
| B3_ceros_explicitos_valen | 2 · fallos anteriores | EmpresaX | B | `Historia!L23`=0; `Historia!L25`=0; `Historia!L26`=0 | `Análisis!C83` | un número | `30.3792524` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| A4_C48_vacio | 2 · fallos anteriores | EmpresaX | A | `Análisis!C48`=None | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B256` | contiene «intereses en financiación» | `Faltan intereses en financiación o principal de arrendamientos (Anális…` | OK |
| A5_C49_vacio | 2 · fallos anteriores | EmpresaX | A | `Análisis!C49`=None | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B256` | contiene «arrendamientos» | `Faltan intereses en financiación o principal de arrendamientos (Anális…` | OK |
| E1_estimacion_justificada_provisional | 3 · evidencias | EmpresaX | B | función: estimacion_justificada | `Motor!B266` | empieza por «LISTO · PROVISIONAL (1 estimaciones» | `LISTO · PROVISIONAL (1 estimaciones justificadas)` | OK |
|  |  |  |  |  | `Motor!B269` | empieza por «PROVISIONAL» | `PROVISIONAL · 1 estimación(es) justificada(s) · documentadas 16 de 17 …` | OK |
|  |  |  |  |  | `Análisis!C83` | 30.7047681226 | `30.7047681226` | OK |
| E2_estimacion_sin_justificar_pendiente | 3 · evidencias | EmpresaX | B | función: estimacion_sin_justificar | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
| E3_no_verificable_no_es_completa | 3 · evidencias | EmpresaX | B | función: no_verificable | `Motor!B269` | contiene «1 no verificables» | `INCOMPLETAS · datos 16 de 17 · hipótesis confirmadas 22 de 22 · 0 esti…` | OK |
|  |  |  |  |  | `Motor!B266` | empieza por «NO LISTO» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
| E4_no_aplicable_en_caja_indebido | 3 · evidencias | EmpresaX | B | función: no_aplicable_indebido | `Motor!B269` | contiene «1 «No aplicable» indebido» | `INCOMPLETAS · datos 16 de 17 · hipótesis confirmadas 22 de 22 · 0 esti…` | OK |
|  |  |  |  |  | `Motor!B266` | empieza por «NO LISTO» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
| E5_no_aplicable_en_entrada_no_usada_ok | 3 · evidencias | EmpresaX | B | función: no_aplicable_legitimo | `Motor!B266` | 'LISTO' | `LISTO` | OK |
| E6_fuente_pendiente_fila_124_cuenta | 3 · evidencias | EmpresaX | B | función: fuente_pendiente_fila_124 | `Motor!B269` | contiene «1 sin clasificar» | `INCOMPLETAS · datos 16 de 17 · hipótesis confirmadas 22 de 22 · 0 esti…` | OK |
|  |  |  |  |  | `Motor!B266` | empieza por «NO LISTO» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
| E7_hipotesis_pendiente_cuenta | 3 · evidencias | EmpresaX | B | función: hipotesis_pendiente | `Motor!B269` | contiene «1 hipótesis pendientes» | `INCOMPLETAS · datos 16 de 17 · hipótesis confirmadas 22 de 22 · 0 esti…` | OK |
| E8_rellenar_otras_celdas_no_confirma | 3 · evidencias | EmpresaX | B | función: rellenar_otras_no_convierte | `Motor!B269` | contiene «1 hipótesis pendientes» | `INCOMPLETAS · datos 16 de 17 · hipótesis confirmadas 22 de 22 · 0 esti…` | OK |
| E9_sin_motor_sin_entradas_aplicables | 3 · evidencias | Plantilla | — | — | `Motor!B269` | empieza por «sin entradas aplicables» | `sin entradas aplicables: elige el motor en Análisis C62` | OK |
| E10_ABB_conserva_pendientes | 3 · evidencias | ABB | — | — | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'INCOMPLETO' | `INCOMPLETO` | OK |
|  |  |  |  |  | `Motor!B256` | contiene «Análisis C48, C49» | `Faltan intereses en financiación o principal de arrendamientos (Anális…` | OK |
|  |  |  |  |  | `Análisis!C49` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B269` | empieza por «INCOMPLETAS» | `INCOMPLETAS · datos 0 de 19 · hipótesis confirmadas 0 de 24 · 0 estima…` | OK |
| E11_ABB_variante_prueba_C49_cero | 3 · evidencias | ABB | — | `Análisis!C49`=0 | `Análisis!C83` | 37.3528564268 | `37.3528564268` | OK |
|  |  |  |  |  | `Motor!B255` | 'INCOMPLETO' | `INCOMPLETO` | OK |
|  |  |  |  |  | `Motor!B256` | contiene «Filtro Pabrai» | `Filtro Pabrai sin completar (Análisis C11:C13)` | OK |
|  |  |  |  |  | `Historia!C65` | 559.0000000000 | `559` | OK |
| E12_EmpresaX_sigue_ficticia | 3 · evidencias | EmpresaX | A | — | `Análisis!B3` | contiene «inventada» | `Empresa X (inventada)` | OK |
|  |  |  |  |  | `Análisis!C83` | 25.8903521530 | `25.890352153` | OK |
|  |  |  |  |  | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas» | `NO LISTO · evidencias incompletas (43 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Panel!B3` | empieza por «Evidencias: INCOMPLETAS» | `Evidencias: INCOMPLETAS · datos 0 de 19 · hipótesis confirmadas 0 de 2…` | OK |
| V1_plantilla_vacia | 4 · vacía y combinaciones | Plantilla | — | — | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'INCOMPLETO' | `INCOMPLETO` | OK |
|  |  |  |  |  | `Motor!B256` | texto, no un error | `Falta elegir el motor en Análisis C62` | OK |
|  |  |  |  |  | `__libro__` | sin #VALUE!/#REF!/#DIV/0!/#NAME? (los #N/A de Motor!B141:E169 son los huecos de gráfico) | `—` | OK |
| V2_A_combinacion_D&A_y_capex | 4 · vacía y combinaciones | EmpresaX | A | `Historia!C8`=None; `Historia!D8`=None; `Historia!E8`=None… | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B256` | texto, no un error | `Motor A: faltan amortizaciones D&A (fila 8) en algún año de la ventana…` | OK |
|  |  |  |  |  | `__libro__` | sin #VALUE!/#REF!/#DIV/0!/#NAME? (los #N/A de Motor!B141:E169 son los huecos de gráfico) | `—` | OK |
| V3_A_combinacion_C50_y_B15 | 4 · vacía y combinaciones | EmpresaX | A | `Análisis!C50`=None; `Palancas!B15`=None | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B256` | texto, no un error | `Faltan datos del FCF base (Análisis C46, C47, C50 o C51)` | OK |
|  |  |  |  |  | `__libro__` | sin #VALUE!/#REF!/#DIV/0!/#NAME? (los #N/A de Motor!B141:E169 son los huecos de gráfico) | `—` | OK |
| V4_B_combinacion_caja_deuda_intereses | 4 · vacía y combinaciones | EmpresaX | B | `Historia!L24`=None; `Historia!L22`=None; `Historia!L15`=None | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B256` | texto, no un error | `Motor B: falta la deuda o los arrendamientos del último año (Historia …` | OK |
|  |  |  |  |  | `__libro__` | sin #VALUE!/#REF!/#DIV/0!/#NAME? (los #N/A de Motor!B141:E169 son los huecos de gráfico) | `—` | OK |
| V5_B_combinacion_moneda_y_caja | 4 · vacía y combinaciones | EmpresaX | B | `Palancas!C48`=None; `Historia!L24`=None | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B256` | texto, no un error | `Motor B: falta la caja del último año (Historia L24); una caja descono…` | OK |
|  |  |  |  |  | `__libro__` | sin #VALUE!/#REF!/#DIV/0!/#NAME? (los #N/A de Motor!B141:E169 son los huecos de gráfico) | `—` | OK |
| V6_C_combinacion_patrimonio_beneficio | 4 · vacía y combinaciones | EmpresaX | C | `Historia!L21`=None; `Historia!L9`=None | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B256` | texto, no un error | `Motor C: faltan patrimonio o beneficio del último año (Historia L9, L2…` | OK |
|  |  |  |  |  | `__libro__` | sin #VALUE!/#REF!/#DIV/0!/#NAME? (los #N/A de Motor!B141:E169 son los huecos de gráfico) | `—` | OK |
| V7_C_combinacion_ROE_y_g | 4 · vacía y combinaciones | EmpresaX | C | `Palancas!C15`=None; `Análisis!C68`=None | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B256` | texto, no un error | `Faltan márgenes objetivo (Palancas B15:D15)` | OK |
|  |  |  |  |  | `__libro__` | sin #VALUE!/#REF!/#DIV/0!/#NAME? (los #N/A de Motor!B141:E169 son los huecos de gráfico) | `—` | OK |
| V8_parcial_tipo_impositivo_un_año | 4 · vacía y combinaciones | EmpresaX | A | `Historia!K10`=None | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'INCOMPLETO' | `INCOMPLETO` | OK |
|  |  |  |  |  | `Historia!C52` | sin valor | `None` | OK |
| V9_texto_en_historia | 4 · vacía y combinaciones | EmpresaX | A | `Historia!L8`='n/d' | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'DATOS INVÁLIDOS' | `DATOS INVÁLIDOS` | OK |
|  |  |  |  |  | `__libro__` | sin #VALUE!/#REF!/#DIV/0!/#NAME? (los #N/A de Motor!B141:E169 son los huecos de gráfico) | `—` | OK |
| V10_C51_fuera_dominio | 4 · vacía y combinaciones | EmpresaX | A | `Análisis!C51`='Tal vez' | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'DATOS INVÁLIDOS' | `DATOS INVÁLIDOS` | OK |
| V11_causa_legible_B15 | 4 · vacía y combinaciones | EmpresaX | A | `Palancas!B15`=None | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B256` | texto, no un error | `Faltan márgenes objetivo (Palancas B15:D15)` | OK |
|  |  |  |  |  | `__libro__` | sin #VALUE!/#REF!/#DIV/0!/#NAME? (los #N/A de Motor!B141:E169 son los huecos de gráfico) | `—` | OK |
| V11_causa_legible_C16 | 4 · vacía y combinaciones | EmpresaX | A | `Palancas!C16`=None | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B256` | texto, no un error | `Faltan ventas por euro reinvertido (Palancas B16:D16)` | OK |
|  |  |  |  |  | `__libro__` | sin #VALUE!/#REF!/#DIV/0!/#NAME? (los #N/A de Motor!B141:E169 son los huecos de gráfico) | `—` | OK |
| V11_causa_legible_D18 | 4 · vacía y combinaciones | EmpresaX | A | `Palancas!D18`=None | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B256` | texto, no un error | `Faltan ROIC a largo plazo (Palancas B18:D18)` | OK |
|  |  |  |  |  | `__libro__` | sin #VALUE!/#REF!/#DIV/0!/#NAME? (los #N/A de Motor!B141:E169 son los huecos de gráfico) | `—` | OK |
| R1_motor_A | 5 · referencias | EmpresaX | A | — | `Análisis!C83` | 25.8903521530 | `25.890352153` | OK |
|  |  |  |  |  | `Análisis!B78` | 15.1023915687 | `15.1023915687` | OK |
|  |  |  |  |  | `Análisis!C78` | 25.0689493251 | `25.0689493251` | OK |
|  |  |  |  |  | `Análisis!D78` | 39.1425212211 | `39.1425212211` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| R2_motor_B | 5 · referencias | EmpresaX | B | — | `Análisis!C83` | 30.7047681226 | `30.7047681226` | OK |
|  |  |  |  |  | `Análisis!B78` | 17.3539528334 | `17.3539528334` | OK |
|  |  |  |  |  | `Análisis!C78` | 29.7144295704 | `29.7144295704` | OK |
|  |  |  |  |  | `Análisis!D78` | 47.0265990684 | `47.0265990684` | OK |
| R3_motor_C_con_palancas_del_ejemplo_A | 5 · referencias | EmpresaX | C | — | `Análisis!C83` | 17.8908417409 | `17.8908417409` | OK |
|  |  |  |  |  | `Análisis!B78` | 10.9505167043 | `10.9505167043` | OK |
|  |  |  |  |  | `Análisis!C78` | 17.2492128343 | `17.2492128343` | OK |
|  |  |  |  |  | `Análisis!D78` | 26.7560534971 | `26.7560534971` | OK |
| R4_motor_C_fixture_original_test_fill | 5 · referencias | EmpresaX | C_orig | función: palancas_C_orig | `Análisis!B78` | 8.3362525831 | `8.3362525831` | OK |
|  |  |  |  |  | `Análisis!C78` | 11.9777149618 | `11.9777149618` | OK |
|  |  |  |  |  | `Análisis!D78` | 15.2293638877 | `15.2293638877` | OK |
|  |  |  |  |  | `Análisis!C83` | 11.8997522712 | `11.8997522712` | OK |
| R5_f_conciliada | 5 · referencias | EmpresaX | A | — | `Historia!C58` | 0.0140000000 | `0.014` | OK |
|  |  |  |  |  | `Historia!C80` | 0.0140000000 | `0.014` | OK |
|  |  |  |  |  | `Historia!C81` | contiene «cuadra» | `✓ cuadra` | OK |
| S1_estudio_A_ON_0 | 6 · invariantes | EmpresaX | A | función: f | `Análisis!C83` | 25.8903521530 | `25.890352153` | OK |
|  |  |  |  |  | `Análisis!C56` | 0.0900000000 | `0.09` | OK |
| S1_estudio_A_ON_40 | 6 · invariantes | EmpresaX | A | función: f | `Análisis!C83` | 25.8903521530 | `25.890352153` | OK |
|  |  |  |  |  | `Análisis!C56` | 0.0900000000 | `0.09` | OK |
| S1_estudio_A_OFF_40 | 6 · invariantes | EmpresaX | A | función: f | `Análisis!C83` | 25.8903521530 | `25.890352153` | OK |
|  |  |  |  |  | `Análisis!C56` | 0.0900000000 | `0.09` | OK |
| S1_estudio_B_ON_0 | 6 · invariantes | EmpresaX | B | función: f | `Análisis!C83` | 30.7047681226 | `30.7047681226` | OK |
|  |  |  |  |  | `Análisis!C56` | 0.0900000000 | `0.09` | OK |
| S1_estudio_B_ON_40 | 6 · invariantes | EmpresaX | B | función: f | `Análisis!C83` | 30.7047681226 | `30.7047681226` | OK |
|  |  |  |  |  | `Análisis!C56` | 0.0900000000 | `0.09` | OK |
| S1_estudio_B_OFF_40 | 6 · invariantes | EmpresaX | B | función: f | `Análisis!C83` | 30.7047681226 | `30.7047681226` | OK |
|  |  |  |  |  | `Análisis!C56` | 0.0900000000 | `0.09` | OK |
| S1_estudio_C_ON_0 | 6 · invariantes | EmpresaX | C | función: f | `Análisis!C83` | 17.8908417409 | `17.8908417409` | OK |
|  |  |  |  |  | `Análisis!C56` | 0.0900000000 | `0.09` | OK |
| S1_estudio_C_ON_40 | 6 · invariantes | EmpresaX | C | función: f | `Análisis!C83` | 17.8908417409 | `17.8908417409` | OK |
|  |  |  |  |  | `Análisis!C56` | 0.0900000000 | `0.09` | OK |
| S1_estudio_C_OFF_40 | 6 · invariantes | EmpresaX | C | función: f | `Análisis!C83` | 17.8908417409 | `17.8908417409` | OK |
|  |  |  |  |  | `Análisis!C56` | 0.0900000000 | `0.09` | OK |
| S2_tasa_usuario_se_conserva_B | 6 · invariantes | EmpresaX | B | — | `Análisis!C56` | 0.0900000000 | `0.09` | OK |
|  |  |  |  |  | `Diagnóstico V6!C15` | 0.0839952904 | `0.0839952904` | OK |
| S3_C15_vacia_fuera_de_B | 6 · invariantes | EmpresaX | A | — | `Diagnóstico V6!C15` | '—' | `—` | OK |
|  |  |  |  |  | `Diagnóstico V6!C16` | '—' | `—` | OK |
| S4_probabilidades_fuera | 6 · invariantes | EmpresaX | A | `Análisis!B69`=-0.1; `Análisis!C69`=1.1; `Análisis!D69`=0.0 | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'DATOS INVÁLIDOS' | `DATOS INVÁLIDOS` | OK |
| S5_ponderado_equiprobable | 6 · invariantes | EmpresaX | A | `Análisis!B69`=0.3333333333333333; `Análisis!C69`=0.3333333333333333; `Análisis!D69`=0.3333333333333333 | `__libro__` | C83 = media de B78:D78 | `—` | OK |
| S6_quiebra_150 | 6 · invariantes | EmpresaX | A | `Palancas!C22`=1.5 | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'DATOS INVÁLIDOS' | `DATOS INVÁLIDOS` | OK |
| S7_quiebra_30_recuperacion_sin_descontar | 6 · invariantes | EmpresaX | A | `Palancas!C22`=0.3; `Palancas!C23`=350 | `Análisis!B78` | 11.6216740981 | `11.6216740981` | OK |
| S8_g_mayor_que_r | 6 · invariantes | EmpresaX | A | `Análisis!C68`=0.12; `Análisis!C56`=0.1 | `Análisis!C83` | sin valor | `None` | OK |
|  |  |  |  |  | `Motor!B255` | 'DATOS INVÁLIDOS' | `DATOS INVÁLIDOS` | OK |
| S9_precio_vacio_bloquea_lectura | 6 · invariantes | EmpresaX | A | `Análisis!C37`=None | `Análisis!C84` | sin valor | `None` | OK |
|  |  |  |  |  | `Diagnóstico V6!C156` | sin valor | `None` | OK |
|  |  |  |  |  | `Panel!M25` | sin valor | `None` | OK |
| S10_precio_referencia_k | 6 · invariantes | EmpresaX | A | `Diagnóstico V6!C158`=0.5 | `Diagnóstico V6!C156` | 12.9451760765 | `12.9451760765` | OK |
| S11_salidas_dependientes_con_valor_bloqueado | 6 · invariantes | EmpresaX | B | `Historia!L24`=None | `Análisis!C84` | sin valor | `None` | OK |
|  |  |  |  |  | `Análisis!C86` | sin valor | `None` | OK |
|  |  |  |  |  | `Diagnóstico V6!C156` | sin valor | `None` | OK |
|  |  |  |  |  | `Panel!K20` | sin valor | `None` | OK |
|  |  |  |  |  | `Análisis!B90` | sin valor | `None` | OK |
|  |  |  |  |  | `Análisis!D92` | sin valor | `None` | OK |
|  |  |  |  |  | `Análisis!A90` | texto, no un error | `r operativa -2 pts (6.4 %)` | OK |
| S12_ADR_ratio_1_comparable | 6 · invariantes | EmpresaX | A | `Palancas!C47`='ADR o ADS'; `Control maestro!D5`=1 | `Motor!B253` | True | `True` | OK |
| S13_ADR_sin_ratio_no_comparable | 6 · invariantes | EmpresaX | A | `Palancas!C47`='ADR o ADS' | `Motor!B253` | False | `False` | OK |
|  |  |  |  |  | `Análisis!C84` | sin valor | `None` | OK |
| VIS_Plantilla_V6.3.xlsx | 8 · visualización | Plantilla_V6.3.xlsx | — | — | `bloques nuevos` | visibles, con tema y reglas de color | `OK` | OK |
| VIS_Ejemplo_V6.3_EmpresaX.xlsx | 8 · visualización | Ejemplo_V6.3_EmpresaX.xlsx | — | — | `bloques nuevos` | visibles, con tema y reglas de color | `OK` | OK |
| INT_Ejemplo_ABB_V6.3.xlsx | 7 · integridad | Ejemplo_ABB_V6.3.xlsx | — | — | `libro completo` | ÍNTEGRO frente a V6.3 (30-oct-2026) | `ÍNTEGRO` | OK |
| INT_Ejemplo_V6.3_EmpresaX.xlsx | 7 · integridad | Ejemplo_V6.3_EmpresaX.xlsx | — | — | `libro completo` | ÍNTEGRO frente a V6.3 (30-oct-2026) | `ÍNTEGRO` | OK |
| INT_Ejemplo_migracion_Hermes_V6.3.xlsx | 7 · integridad | Ejemplo_migracion_Hermes_V6.3.xlsx | — | — | `libro completo` | ÍNTEGRO frente a V6.3 (30-oct-2026) | `ÍNTEGRO` | OK |
| INT_Plantilla_V6.3.xlsx | 7 · integridad | Plantilla_V6.3.xlsx | — | — | `libro completo` | ÍNTEGRO frente a V6.3 (30-oct-2026) | `ÍNTEGRO` | OK |
| MAN_C58_cero | 7 · integridad | Plantilla_V6.3.xlsx | — | `Historia!C58`='=0' | `Historia!C58` | ALTERADO y la celda nombrada | `['Historia!C58: fórmula alterada → =0']` | OK |
| MAN_C83_cero | 7 · integridad | Plantilla_V6.3.xlsx | — | `Análisis!C83`='=0' | `Análisis!C83` | ALTERADO y la celda nombrada | `['Análisis!C83: fórmula alterada → =0']` | OK |
| MAN_C83_valor | 7 · integridad | Plantilla_V6.3.xlsx | — | `Análisis!C83`=25.0 | `Análisis!C83` | ALTERADO y la celda nombrada | `['Análisis!C83: fórmula sustituida por el valor 25']` | OK |
| MAN_V23_anulada | 7 · integridad | Plantilla_V6.3.xlsx | — | `Motor!E223`='=""' | `Motor!E223` | ALTERADO y la celda nombrada | `['Motor!E223: fórmula alterada → =""']` | OK |
| INT_entradas_legitimas_sin_falsos_positivos | 7 · integridad | Plantilla_V6.3.xlsx | — | 10 entradas rellenadas | `libro completo` | ÍNTEGRO | `ÍNTEGRO` | OK |
| COB_base_A_precio | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_capitalizacion | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_acciones | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_cfo_media | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_capex_media | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_int_fin_media | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_leases_media | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_sbc_media | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_h_anios | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_h_ventas | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_h_ebit | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_h_da | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_h_tipo | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_h_capex | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_h_circulante | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_moneda_cotizacion | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_moneda_modelo | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_unidad | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_norma | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_motor | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_r | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_caso_especial | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_base_margen | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_anios_f | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_restar_sbc | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_crec_MALO | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_margen_MALO | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_s2c_MALO | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_roic_MALO | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_g_MALO | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_prob_MALO | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_crec_NORMAL | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_margen_NORMAL | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_s2c_NORMAL | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_roic_NORMAL | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_g_NORMAL | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_prob_NORMAL | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_crec_BUENO | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_margen_BUENO | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_s2c_BUENO | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_roic_BUENO | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_g_BUENO | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_prob_BUENO | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_A_todo_confirmado_LISTO | 9 · cobertura | EmpresaX | A | función: _pos | `Motor!B266` | 'LISTO' | `LISTO` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_precio | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_capitalizacion | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_acciones | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_h_anios | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_h_ventas | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_h_ebit | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_h_tipo | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_h_intereses | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_h_deuda | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_h_arrend | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_h_caja | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_h_pensiones | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_h_minoritarios | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_moneda_cotizacion | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_moneda_modelo | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_unidad | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_norma | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_motor | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_r | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_caso_especial | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_base_margen | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_crec_MALO | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_margen_MALO | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_s2c_MALO | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_roic_MALO | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_g_MALO | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_prob_MALO | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_crec_NORMAL | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_margen_NORMAL | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_s2c_NORMAL | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_roic_NORMAL | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_g_NORMAL | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_prob_NORMAL | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_crec_BUENO | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_margen_BUENO | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_s2c_BUENO | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_roic_BUENO | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_g_BUENO | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_prob_BUENO | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_B_todo_confirmado_LISTO | 9 · cobertura | EmpresaX | B | función: _pos | `Motor!B266` | 'LISTO' | `LISTO` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_precio | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_capitalizacion | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_acciones | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_h_anios | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_h_beneficio | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_h_patrimonio | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_moneda_cotizacion | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_moneda_modelo | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_unidad | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_norma | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_motor | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_r | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_caso_especial | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_crec_MALO | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_margen_MALO | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_roic_MALO | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_g_MALO | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_prob_MALO | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_crec_NORMAL | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_margen_NORMAL | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_roic_NORMAL | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_g_NORMAL | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_prob_NORMAL | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_crec_BUENO | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_margen_BUENO | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_roic_BUENO | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_g_BUENO | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_prob_BUENO | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_base_C_todo_confirmado_LISTO | 9 · cobertura | EmpresaX | C | función: _pos | `Motor!B266` | 'LISTO' | `LISTO` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_quiebra_A_p_quiebra | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_quiebra_A_recuperacion | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_quiebra_A_todo_confirmado_LISTO | 9 · cobertura | EmpresaX | A | función: _pos | `Motor!B266` | 'LISTO' | `LISTO` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_quiebra_B_p_quiebra | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_quiebra_B_recuperacion | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_quiebra_B_todo_confirmado_LISTO | 9 · cobertura | EmpresaX | B | función: _pos | `Motor!B266` | 'LISTO' | `LISTO` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_quiebra_C_p_quiebra | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_quiebra_C_recuperacion | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_quiebra_C_todo_confirmado_LISTO | 9 · cobertura | EmpresaX | C | función: _pos | `Motor!B266` | 'LISTO' | `LISTO` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_fcf_neg_A_naturaleza_fcf | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_fcf_neg_A_fcf_normalizado | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_fcf_neg_A_todo_confirmado_LISTO | 9 · cobertura | EmpresaX | A | función: _pos | `Motor!B266` | 'LISTO' | `LISTO` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_exceso_caja_A_exceso_caja | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_exceso_caja_A_todo_confirmado_LISTO | 9 · cobertura | EmpresaX | A | función: _pos | `Motor!B266` | 'LISTO' | `LISTO` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_adr_A_ratio_adr | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_adr_A_causa_desviacion | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_adr_A_todo_confirmado_LISTO | 9 · cobertura | EmpresaX | A | función: _pos | `Motor!B266` | 'LISTO' | `LISTO` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_adr_B_ratio_adr | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_adr_B_causa_desviacion | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_adr_B_todo_confirmado_LISTO | 9 · cobertura | EmpresaX | B | función: _pos | `Motor!B266` | 'LISTO' | `LISTO` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_adr_C_ratio_adr | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_adr_C_causa_desviacion | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_adr_C_todo_confirmado_LISTO | 9 · cobertura | EmpresaX | C | función: _pos | `Motor!B266` | 'LISTO' | `LISTO` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_desviacion_A_causa_desviacion | 9 · cobertura | EmpresaX | A | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_desviacion_A_todo_confirmado_LISTO | 9 · cobertura | EmpresaX | A | función: _pos | `Motor!B266` | 'LISTO' | `LISTO` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_desviacion_B_causa_desviacion | 9 · cobertura | EmpresaX | B | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_desviacion_B_todo_confirmado_LISTO | 9 · cobertura | EmpresaX | B | función: _pos | `Motor!B266` | 'LISTO' | `LISTO` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_desviacion_C_causa_desviacion | 9 · cobertura | EmpresaX | C | función: f | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_desviacion_C_todo_confirmado_LISTO | 9 · cobertura | EmpresaX | C | función: _pos | `Motor!B266` | 'LISTO' | `LISTO` | OK |
|  |  |  |  |  | `Motor!B255` | 'COMPLETO Y VÁLIDO' | `COMPLETO Y VÁLIDO` | OK |
| COB_no_aplicable_legitimo_DA_en_B | 9 · cobertura | EmpresaX | B | función: <lambda> | `Motor!B266` | 'LISTO' | `LISTO` | OK |
| COB_no_aplicable_legitimo_S2C_en_C | 9 · cobertura | EmpresaX | C | función: <lambda> | `Motor!B266` | 'LISTO' | `LISTO` | OK |
| COB_no_aplicable_indebido_r_en_C | 9 · cobertura | EmpresaX | C | función: <lambda> | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B269` | contiene «1 «No aplicable» indebido» | `INCOMPLETAS · datos 10 de 10 · hipótesis confirmadas 17 de 18 · 0 esti…` | OK |
| COB_no_verificable_crecimiento_en_A | 9 · cobertura | EmpresaX | A | función: <lambda> | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
|  |  |  |  |  | `Motor!B269` | contiene «1 no verificables» | `INCOMPLETAS · datos 19 de 19 · hipótesis confirmadas 23 de 24 · 0 esti…` | OK |
| COB_estimacion_sin_justificar_margen_en_B | 9 · cobertura | EmpresaX | B | función: <lambda> | `Motor!B266` | empieza por «NO LISTO · evidencias incompletas (1 pendientes)» | `NO LISTO · evidencias incompletas (1 pendientes) · cálculo completo` | OK |
| COB_estimacion_justificada_ROIC_en_C_provisional | 9 · cobertura | EmpresaX | C | función: <lambda> | `Motor!B266` | empieza por «LISTO · PROVISIONAL (1 estimaciones» | `LISTO · PROVISIONAL (1 estimaciones justificadas)` | OK |
| COB_quiebra_vacia_no_exige_confirmacion | 9 · cobertura | EmpresaX | A | función: <lambda> | `Motor!B266` | 'LISTO' | `LISTO` | OK |
|  |  |  |  |  | `Palancas!C22` | sin valor | `None` | OK |

## Regresión frente a la V6.1 (recálculo real)

| Libro | C83 V6.1 | C83 V6.3 | Estado V6.3 |
|---|---|---|---|
| Empresa X (motor A) | 25,8903521530 | 25,8903521530 | COMPLETO Y VÁLIDO · NO LISTO · evidencias incompletas (43 pendientes) · cálculo completo |
| Empresa X (motor B) | 30,7047681226 | 30,7047681226 | COMPLETO Y VÁLIDO · NO LISTO · evidencias incompletas (39 pendientes) |
| Empresa X (motor C, palancas del ejemplo A) | 17,8908417409 | 17,8908417409 | COMPLETO Y VÁLIDO |
| Empresa X (motor C, fixture original de test_fill.py) | 11,8997522712 | 11,8997522712 | COMPLETO Y VÁLIDO |
| ABB (entregado, C49 vacío) | 37,3528564268 | **sin valor** · INCOMPLETO · falta C48/C49 | no se ha rellenado el hueco |
| ABB (variante de prueba, C49 = 0; no es entregable) | — | 37,3528564268 | INCOMPLETO (juicios del inversor) |
| Hermès migrado | sin valor | sin valor | INCOMPLETO |
| Plantilla vacía | sin valor | sin valor | INCOMPLETO (22 pendientes) |

Ningún `#VALUE!`, `#REF!`, `#DIV/0!` ni `#NAME?` en ninguno de los libros recalculados; los `#N/A` de
`Motor!B141:E169` son los huecos de gráfico documentados en la V6.1.

## Reproducibilidad

`construir_v63.py originales/V6.1 → salida` produce los cuatro entregables con los mismos SHA-256 (fechas del
paquete fijadas). Comprobado en esta entrega.

## NO EJECUTADAS (no se declaran superadas)

- Excel real: deslizadores, colores, avisos de reparación y guardado/reapertura (solo LibreOffice 24.2 headless)
- V37 frente a booleanos en Historia (LibreOffice los lee como números)
- R03 migración desde Hermes_evaluada.xlsx y R08 ABB desde abb_fase1.json: insumos no entregados
- Combinaciones de tres o más ausencias simultáneas distintas de las probadas.
- Barrido de las tablas `Sector` y `Riesgo país` y de los metadatos de Control maestro que no entran en el cálculo.
- Cobertura de evidencias con dos configuraciones condicionales activas a la vez (p. ej. quiebra + FCF normalizado): cada condición se probó por separado.