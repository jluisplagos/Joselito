# DATOS V6.3 · Empresa X (inventada) (EMPX) · fecha de análisis 2026-10-20

Volcado automático (volcar_datos_v63.py). Todo lo de aquí es DATO de fase 1 o cálculo de la hoja, salvo el bloque HEREDADO, que son decisiones de la etapa 1 (hipótesis, no hechos: D3).

## 1. Estado técnico del libro

- Motor (Diagnóstico V6!C5): **A** · coherencia tipo/motor: ✓ PASA · tipo y motor coherentes
- Motor!B255 estado técnico: **INCOMPLETO** · causa principal: Faltan palancas de crecimiento (Palancas B14:D14)
- Motor!B266 estado del libro: NO LISTO · incompleto (6 pendientes) · B253 comparable precio↔valor: True · B252 bloqueo del valor: True
- Moneda del modelo (Control maestro!H4): EUR · moneda de cotización (Palancas!C48): EUR · unidad: mm · norma contable: IFRS · ratio ADR (D5): None
- Causas activas: 1. INCOMPLETO · Faltan palancas de crecimiento (Palancas B14:D14); 2. INCOMPLETO · Faltan márgenes objetivo (Palancas B15:D15); 3. INCOMPLETO · Faltan ventas por euro reinvertido (Palancas B16:D16); 4. INCOMPLETO · Faltan ROIC a largo plazo (Palancas B18:D18); 5. AVISO · Probabilidad de quiebra vacía (Palancas C22): se asume 0 por convención, no es un riesgo medido; 6. AVISO · Fecha de análisis escrita como texto (Análisis D4): escríbela como fecha; 7. INCOMPLETO · Faltan 3 predicciones (Palancas A38:A40); 8. INCOMPLETO · Faltan 1 respuestas de las etapas 1 y 2
- Reglas del motor que no están en OK/N/A: V12 INCOMPLETO (Faltan palancas de crecimiento (Palancas B14:D14)); V13 INCOMPLETO (Faltan márgenes objetivo (Palancas B15:D15)); V14 INCOMPLETO (Faltan ventas por euro reinvertido (Palancas B16:D16)); V16 INCOMPLETO (Faltan ROIC a largo plazo (Palancas B18:D18)); V19 AVISO (Probabilidad de quiebra vacía (Palancas C22): se asume 0 por convención, no es un riesgo medido); V31 AVISO (Fecha de análisis escrita como texto (Análisis D4): escríbela como fecha); C07 INCOMPLETO (Faltan 3 predicciones (Palancas A38:A40)); C08 INCOMPLETO (Faltan 1 respuestas de las etapas 1 y 2)

## 2. Datos de Análisis con su evidencia (Control maestro)

| Celda | Concepto | Valor | Clasificación (F) | Documento (J) | Página (L) | Observación (N) |
|---|---|---|---|---|---|---|
| B3 | Empresa | Empresa X (inventada) | Rellenado y verificado | fase1_v63.json (identificación) | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!B3 |
| D3 | Ticker | EMPX | Rellenado y verificado | fase1_v63.json (identificación) | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!D3 |
| B4 | Sector (texto libre) | — | — | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!B4 |
| D4 | Fecha de análisis | 2026-10-20 | Rellenado y verificado | fase1_v63.json (fecha de análisis) | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!D4 |
| C24 | ROIC / ROCE (%) | 0.18 | Dato no verificable | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C24 |
| C26 | CFO ÷ beneficio neto | 1.1 | Dato no verificable | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C26 |
| C28 | Dilución (Recompra/Estable/Emite) | Estable | — | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C28 |
| C31 | ¿Cobros o inventario crecen más rápido que ingresos? | No | Dato no verificable | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C31 |
| C32 | Goodwill ÷ activo total | 0.12 | Dato no verificable | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C32 |
| C33 | Deuda neta ÷ EBITDA (x) | 0.8 | Dato no verificable | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C33 |
| C34 | ¿La caja cubre la deuda a corto? | — | — | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C34 |
| C37 | Precio actual | 16 | Rellenado y verificado | cotización de cierre (sintética) | — | fecha 2026-10-20 · moneda de cotización EUR |
| C38 | Valor intrínseco de fuente externa | — | — | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C38 |
| C40 | FCF (mm) para FCF yield | — | — | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C40 |
| C41 | Capitalización (mm) | 1600 | Rellenado y verificado | precio × acciones (sintético) | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C41 |
| C42 | EV/EBITDA (x) | — | — | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C42 |
| C46 | CFO medio (mm) | 169.78 | Dato no verificable | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C46 |
| C47 | Capex medio (mm) | 74.22 | Dato no verificable | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C47 |
| C48 | Intereses en financiación (mm, IFRS) | 7.42 | Dato no verificable | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C48 |
| C49 | Principal de arrendamientos (mm, IFRS 16) | 3.71 | Dato no verificable | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C49 |
| C50 | SBC (mm) | 4.64 | Dato no verificable | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C50 |
| C52 | FCF base (fórmula) | 79.79 | — | — | — | — |
| C53 | Caja y equivalentes (mm) | 100 | Dato no verificable | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C53 |
| C54 | Deuda total (mm) | 60 | Dato no verificable | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C54 |
| C55 | Acciones diluidas (mm) | 100 | Rellenado y verificado | informe anual sintético, nota de capital | 12 | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C55 |
| C57 | Tasa sin riesgo | 0.03 | Rellenado y verificado | bono a 10 años (sintético) | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C57 |
| C60 | CAGR acciones diluidas | — | — | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C60 |
| C88 | P/FCF histórico | — | — | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C88 |
| C96 | Fecha de la evidencia de gestión | — | — | — | — | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C96 |

FCF base (C52, fórmula): 79.79 · Peso de la SBC (C59): 0.0549568 · Precio (C37): 16 EUR con fecha 2026-10-20 · Acciones (C55): 100 con fecha 2026-09-30 · Capitalización (C41): 1600 · Causa de diferencia de capitalización (Palancas!C47): Ninguna

## 3. Historia (10 años; una celda vacía es DESCONOCIDO, nunca cero)

| Partida | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | Fuente (M) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ventas | 500.249 | 540.269 | 583.49 | 630.17 | 680.583 | 735.03 | 793.832 | 857.339 | 925.926 | 1000 | Empresa X (inventada): informe anual sintético |
| ebit | 100.05 | 108.054 | 116.698 | 126.034 | 136.117 | 147.006 | 158.766 | 171.468 | 185.185 | 200 | Empresa X (inventada): informe anual sintético |
| da | 20.01 | 21.6108 | 23.3396 | 25.2068 | 27.2233 | 29.4012 | 31.7533 | 34.2936 | 37.037 | 40 | Empresa X (inventada): informe anual sintético |
| beneficio_neto | 71.2855 | 76.9883 | 83.1474 | 89.7992 | 96.9831 | 104.742 | 113.121 | 122.171 | 131.944 | 142.5 | Empresa X (inventada): informe anual sintético |
| tipo_impositivo | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | Empresa X (inventada): informe anual sintético |
| cfo | 91.5456 | 98.8692 | 106.779 | 115.321 | 124.547 | 134.51 | 145.271 | 156.893 | 169.444 | 183 | Empresa X (inventada): informe anual sintético |
| capex | 40.0199 | 43.2215 | 46.6792 | 50.4136 | 54.4467 | 58.8024 | 63.5066 | 68.5871 | 74.0741 | 80 | Empresa X (inventada): informe anual sintético |
| adquisiciones | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Empresa X (inventada): informe anual sintético |
| circulante | 5.00249 | 5.40269 | 5.8349 | 6.3017 | 6.80583 | 7.3503 | 7.93832 | 8.57339 | 9.25926 | 10 | Empresa X (inventada): informe anual sintético |
| intereses | 5.00249 | 5.40269 | 5.8349 | 6.3017 | 6.80583 | 7.3503 | 7.93832 | 8.57339 | 9.25926 | 10 | Empresa X (inventada): informe anual sintético |
| intereses_financiacion | 4.00199 | 4.32215 | 4.66792 | 5.04136 | 5.44467 | 5.88024 | 6.35066 | 6.85871 | 7.40741 | 8 | Empresa X (inventada): informe anual sintético |
| arrendamientos_principal | 2.001 | 2.16108 | 2.33396 | 2.52068 | 2.72233 | 2.94012 | 3.17533 | 3.42936 | 3.7037 | 4 | Empresa X (inventada): informe anual sintético |
| sbc | 2.50124 | 2.70134 | 2.91745 | 3.15085 | 3.40292 | 3.67515 | 3.96916 | 4.28669 | 4.62963 | 5 | Empresa X (inventada): informe anual sintético |
| id | 15.0075 | 16.2081 | 17.5047 | 18.9051 | 20.4175 | 22.0509 | 23.815 | 25.7202 | 27.7778 | 30 | Empresa X (inventada): informe anual sintético |
| acciones_diluidas | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | 100 | Empresa X (inventada): informe anual sintético |
| patrimonio | 300.149 | 324.161 | 350.094 | 378.102 | 408.35 | 441.018 | 476.299 | 514.403 | 555.556 | 600 | Empresa X (inventada): informe anual sintético |
| deuda | 100.05 | 108.054 | 116.698 | 126.034 | 136.117 | 147.006 | 158.766 | 171.468 | 185.185 | 200 | Empresa X (inventada): informe anual sintético |
| arrendamientos | 25.0124 | 27.0134 | 29.1745 | 31.5085 | 34.0292 | 36.7515 | 39.6916 | 42.8669 | 46.2963 | 50 | Empresa X (inventada): informe anual sintético |
| caja | 50.0249 | 54.0269 | 58.349 | 63.017 | 68.0583 | 73.503 | 79.3832 | 85.7339 | 92.5926 | 100 | Empresa X (inventada): informe anual sintético |
| pensiones | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Empresa X (inventada): informe anual sintético |
| minoritarios | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | Empresa X (inventada): informe anual sintético |

### Series calculadas por la hoja

| Serie | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|
| crecimiento_ventas | — | 0.08 | 0.08 | 0.08 | 0.08 | 0.08 | 0.08 | 0.08 | 0.08 | 0.08 |
| margen_ebit | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 |
| reinversion_neta_organica | 25.0124 | 27.0134 | 29.1745 | 31.5085 | 34.0292 | 36.7515 | 39.6916 | 42.8669 | 46.2963 | 50 |
| reinversion_neta_total | 25.0124 | 27.0134 | 29.1745 | 31.5085 | 34.0292 | 36.7515 | 39.6916 | 42.8669 | 46.2963 | 50 |
| capital_invertido | 375.187 | 405.202 | 437.618 | 472.627 | 510.437 | 551.272 | 595.374 | 643.004 | 694.444 | 750 |
| roic | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 |
| roe | 0.2375 | 0.2375 | 0.2375 | 0.2375 | 0.2375 | 0.2375 | 0.2375 | 0.2375 | 0.2375 | 0.2375 |
| fcf_accionista | 43.0214 | 46.4631 | 50.1802 | 54.1946 | 58.5302 | 63.2126 | 68.2696 | 73.7311 | 79.6296 | 86 |
| roic_con_id | — | — | — | — | — | — | — | — | — | — |

### Anclas (Historia C43:C66)

| Ancla | Celda | Valor |
|---|---|---|
| anios_con_ventas | C43 | 10 |
| ventas_ultimo | C44 | 1000 |
| cagr_3 | C45 | 0.08 |
| cagr_5 | C46 | 0.08 |
| cagr_serie | C47 | 0.08 |
| margen_ultimo | C48 | 0.2 |
| margen_medio | C49 | 0.2 |
| margen_min | C50 | 0.2 |
| margen_max | C51 | 0.2 |
| tipo_impositivo_5 | C52 | 0.25 |
| s2c_marginal | C53 | 1.48148 |
| s2c_medio | C54 | 1.33333 |
| roic_medio_5 | C55 | 0.2 |
| roe_medio_5 | C56 | 0.2375 |
| anios_fcf_base | C57 | 3 |
| f | C58 | 0.0139967 |
| patrimonio_ultimo | C59 | 600 |
| roe_ultimo | C60 | 0.2375 |
| beneficio_ultimo | C61 | 142.5 |
| ebitda_ultimo | C62 | 240 |
| coste_deuda | C63 | 0.0415385 |
| deuda_mas_arr | C64 | 250 |
| pensiones_mas_minor | C65 | 0 |
| caja_ultimo | C66 | 100 |

## 4. Sector y riesgo país que usa la hoja

- Sector de Damodaran (Palancas!C7): **Machinery** · etapa (C5): Madura en crecimiento · caso especial (C6): Ninguno · base del margen (C8): Último año · I+D capitalizada (C9/C10): No / None
- Crecimiento de ventas del sector (3 años) Q1 / mediana / Q3: 0.0311 / 0.0797 / 0.161 · media propia (F14): 0.08
- Margen operativo del sector Q1 / mediana / Q3: -0.000145349 / 0.0645941 / 0.125493 · media propia (F15): 0.2
- ROIC medio del sector (H18): 0.118351 · ROIC propio 5 años (F18): 0.2
- S2C MEDIO del sector (ventas ÷ capital; medida distinta de la palanca) Q1 / mediana / Q3: 0.718226 / 1.17726 / 1.78242 · propio (F19): 1.33333 · S2C MARGINAL propio (F16, la palanca): 1.48148
- Tasa sin riesgo (Análisis!C57): 0.03 · r del inversor (C56, heredada): 0.09 · r mínima (Diagnóstico!C17): 0.0815138 · ✓ PASA · r ≥ r mínima · r operativa del motor B (C15): —
- Reparto geográfico (Palancas A28:B33): Germany 0.6 (prima 0); Brazil 0.3 (prima 0.0309839); United States 0.1 (prima 0.00218635)

## 5. Conciliación precio × acciones ≈ capitalización y f

- Parámetros de la hoja: tolerancia 0.05, corte 0.25, separación máxima de fechas 90 días
- Reglas V22, V26, V27, V28: V22 OK; V26 OK; V27 OK; V28 OK
- f (fugas al accionista, Diagnóstico!C12 = Historia!C58): 0.0139967 · V0: 1000 · m0: 0.2 · t: 0.25

## 6. HEREDADO de la etapa 1 (V5.3 decidida por el personaje v1) — hipótesis, no hechos (D3)

Libro: EmpresaX_sin_C34_evaluada.xlsx. Cada celda con su Observación v1. El crecimiento del FCF (B67:D67) ya no se escribe en la V6.3 (fórmula): se muestra solo como contexto.

| Celda | Valor etapa 1 | Observación v1 (Control maestro N) |
|---|---|---|
| C11 | Sí | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C11 |
| C12 | Sí | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C12 |
| C13 | No | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C13 |
| C14 | Compounder | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C14 |
| C17 | Sí | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C17 |
| C18 | Sí | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C18 |
| C19 | Sí | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C19 |
| C20 | Incert. alta + riesgo bajo | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C20 |
| C25 | Sí | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C25 |
| C27 | Estable | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C27 |
| C51 | Sí | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C51 |
| C56 | 0.09 | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C56 |
| C61 | No está claro | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C61 |
| C62 | Sí | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C62 |
| B65 | El viento de cola se frena | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!B65 |
| C65 | Crece al ritmo de su mercado | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C65 |
| D65 | Gana cuota: el moat se ensancha | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!D65 |
| B66 | malo v1 | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!B66 |
| C66 | normal v1 | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C66 |
| D66 | bueno v1 | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!D66 |
| B67 | 0.02 | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!B67 |
| C67 | 0.07 | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C67 |
| D67 | 0.12 | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!D67 |
| B68 | 0.015 | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!B68 |
| C68 | 0.025 | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C68 |
| D68 | 0.03 | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!D68 |
| B69 | 0.2 | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!B69 |
| C69 | 0.6 | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C69 |
| D69 | 0.2 | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!D69 |
| C76 | 0 | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C76 |
| C93 | Sí | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C93 |
| C97 | Neutral | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C97 |
| C98 | Buena | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C98 |
| B101 | Tesis v1. | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!B101 |
| B102 | Tesis inversa v1. | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!B102 |
| C103 | Sí | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C103 |
| C104 | 0% · Vigilar · precio de Sí ≈ 15 | [Clase: fundamentada] [Confianza: media] obs v1 de Análisis!C104 |

### juicio.json de la etapa 1
```json
{"empresa": "Empresa X (inventada)", "cubo": "VIGILAR", "precio_de_si": 15}
```

### respuesta.md de la etapa 1 (cubo, precio de Sí v1, seis preguntas, qué le haría cambiar de cubo)

# respuesta v1 (sintética)

Cubo: VIGILAR. Precio de Sí v1: 15.

## 7. REFERENCIAS MECÁNICAS por palanca (convención del ejercicio, Anexo B §B.2; NO son estimaciones de Damodaran)

Versión de las reglas: 0.2.1 · motor A · tasa del motor 0.09 · rf 0.03. La fase B parte de aquí y se desvía con motivo; la clase «sin juicio propio» solo puede copiar una referencia disponible.

| Palanca | MALO_ref | NORMAL_ref | BUENO_ref | Regla / motivo de no disponibilidad | Anclas usadas | Criterio relacionado (no respalda la cifra) |
|---|---|---|---|---|---|---|
| crecimiento_1_5 | 0.03 | 0.08 | 0.08 | NORMAL = CAGR 5a acotado a [Q1, Q3]; MALO = mín(NORMAL, máx(mín(Q1, NORMAL − σ), −0,10)); BUENO = máx(NORMAL, mín(NORMAL + σ, Q3, 1,5 × CAGR)) | {"cagr_5": 0.0800000000000001, "fuente": "Historia!C46 (CAGR 5 años de ventas)", "sector_q1": 0.0311, "sector_mediana": 0.0797, "sector_q3": 0.161, "sigma": 6.01023760172117e-16, "sigma_nota": "σ muestral de 9 tasas anuales = 0.0000"} | E4 (el pasado predice mal); I1 (el crecimiento se paga con reinversión) |
| margen_objetivo | 0.2 | 0.2 | 0.2 | NORMAL = m0 (último año o media del ciclo según C8); MALO = máx(mín(m0, media), mínimo); BUENO = máx(m0, mín(máximo histórico, Q3 sector)); si m0 ya es el máximo, BUENO = m0 | {"m0": 0.2, "base": "Último año", "media": 0.2, "min": 0.2, "max": 0.200000000000001, "sector_q3": 0.125493291239148, "fuente": "Historia!C48 / C49 (según Palancas!C8), C50, C51 y Sector Q3"} | E2 (la competencia muerde los márgenes); E5 (cíclicas); E7 (comprobar contra la historia) |
| s2c | 1.1 | 1.5 | 1.9 | NORMAL = Historia!C53 con tope (rentabilidad marginal ≤ 2× ROIC histórico); MALO = 0,75 × NORMAL; BUENO = 1,25 × NORMAL con el mismo tope | {"s2c_marginal_C53": 1.48148148148148, "roic_medio_5_C55": 0.2, "tipo_impositivo_C52": 0.25} | I1 (reinversión = Δventas ÷ S2C); la banda ±25 % es convención del ejercicio |
| g_perpetuo | 0.015 | 0.025 | 0.03 | NORMAL = mín(0,025; rf) ajustado a la lista; MALO = NORMAL − 0,01 (suelo 0); BUENO = mín(NORMAL + 0,005; rf; 0,03); siempre < tasa del motor | {"rf_C57": 0.03, "tasa_del_motor": 0.09, "etapa_C5": "Madura en crecimiento"} | E1 (g estable ≤ rf, orientación); N1 (g < tasa del motor) |
| roic_lp | 0.09 | 0.09 | 0.19 | NORMAL = MALO = tasa del motor (convención: sin retornos en exceso a perpetuidad como caso neutro; no una ley); BUENO = mín(ROIC medio 5a, Análisis!C56 + 0,10), y la tasa si el histórico es menor | {"tasa_del_motor": 0.09, "roic_hist": 0.2, "C56": 0.09, "sector_roic_media_H18_solo_contexto": 0.118351200008183} | E2, E3; I2 (reinversión terminal g ÷ ROIC); el +0,10 es umbral de la plantilla |
| probabilidades | 0.2 | 0.6 | 0.2 | 0,2 / 0,6 / 0,2 (convención del ejercicio, S-6) | {} | E6 (suman 1 si cubren el rango) |

- Quiebra (C22/C23): referencia 0.05 / 0 · disparadores: deuda + arrendamientos (Historia!C64 = 250) > 3 × FCF base (79.79) · vacío (= 0) salvo disparador; con disparador 0,05 como convención y obligación de argumentar; C23 = 0
- Exceso de caja (C76): 0 · Tamaño de mercado (C24): solo con cifra de fuente primaria en los extractos
- Rentabilidad marginal implícita (S2C × margen × (1 − t)) y salto del año 11 con las referencias: {"MALO": {"rentabilidad_marginal": 0.16500000000000004, "roic_lp_ref": 0.09, "salto_anio_11": 0.07500000000000004}, "NORMAL": {"rentabilidad_marginal": 0.22500000000000003, "roic_lp_ref": 0.09, "salto_anio_11": 0.13500000000000004}, "BUENO": {"rentabilidad_marginal": 0.28500000000000003, "roic_lp_ref": 0.19, "salto_anio_11": 0.09500000000000003}}

## 8. DATOS AUSENTES no bloqueantes (entrada de la revisión de la fase C, S-19)

| Dato | Nivel | De dónde debería venir | Nota |
|---|---|---|---|
| Análisis!C34 | necesario para LISTO·PROVISIONAL | fase1_v63.json o derivado de Historia (rellenar_fase1_v63.py) |  |
| evidencia Análisis!C46 | necesario para LISTO·PROVISIONAL | fase1_v63.json (fuente y página del dato) o etapa 1 | el dato está pero su clasificación/documento no permite LISTO·PROVISIONAL; la fase C juzga si es material |
| evidencia Análisis!C47 | necesario para LISTO·PROVISIONAL | fase1_v63.json (fuente y página del dato) o etapa 1 | el dato está pero su clasificación/documento no permite LISTO·PROVISIONAL; la fase C juzga si es material |
| evidencia Análisis!C48 | necesario para LISTO·PROVISIONAL | fase1_v63.json (fuente y página del dato) o etapa 1 | el dato está pero su clasificación/documento no permite LISTO·PROVISIONAL; la fase C juzga si es material |
| evidencia Análisis!C49 | necesario para LISTO·PROVISIONAL | fase1_v63.json (fuente y página del dato) o etapa 1 | el dato está pero su clasificación/documento no permite LISTO·PROVISIONAL; la fase C juzga si es material |
| evidencia Análisis!C50 | necesario para LISTO·PROVISIONAL | fase1_v63.json (fuente y página del dato) o etapa 1 | el dato está pero su clasificación/documento no permite LISTO·PROVISIONAL; la fase C juzga si es material |
| Palancas!C24 | no bloqueante | extractos (solo con cifra de fuente primaria) |  |
| Análisis!C88 | no bloqueante | fase1_v63.json |  |
| Análisis!C38 | no bloqueante | fase1_v63.json (opcional) |  |
| extracto_v63: Tamaño del mercado (no publicado) | no bloqueante | informes de la empresa (fase 1 / extracción) | declarado «no encontrado» por el agente de extracción; la fase C decide si afecta a una celda de juicio |
| extracto_v63: Cuota de mercado | no bloqueante | informes de la empresa (fase 1 / extracción) | declarado «no encontrado» por el agente de extracción; la fase C decide si afecta a una celda de juicio |
