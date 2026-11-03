> Antecedente de la entrega previa a la corrección de la norma contable. Para el cambio y las pruebas actuales, consultar `Correccion_norma_contable.md`. Los hashes y resultados que siguen describen aquella entrega.

# Informe · Plantilla V6.3 (30-oct-2026 · cobertura completa de evidencias)

**Estado: cerrada dentro del alcance declarado.** 251 pruebas superadas, 0 fallidas, 0 no ejecutadas
sobre los archivos finales ya empaquetados; los cuatro entregables son ÍNTEGROS frente a la
referencia aprobada; la reconstrucción desde los originales V6.1 da los mismos bytes. Lo que no se
ha podido comprobar está en el §7 sin disfrazar.

Esta revisión sustituye a la del 29-oct. Las correcciones anteriores (ausencias ≠ cero, moneda común,
conciliación de f con efecto en el estado, dominios económicos, verificador contra referencia) se
conservan; lo que cambia es el control de evidencias, que no cubría las hipótesis ni varias entradas
condicionales.

## 1. Archivos finales probados

| Archivo | SHA-256 |
|---|---|
| `entregables/Plantilla_V6.3.xlsx` | `128f4a0f12088c13de237ea82c03c18614745b351a173964a43d3cd8782e9087` |
| `entregables/Ejemplo_V6.3_EmpresaX.xlsx` | `d99bc648f70f2e562172fbfda0961a6b8261f1be3336d269c55d5af47fadce1a` |
| `entregables/Ejemplo_ABB_V6.3.xlsx` | `5b1c66aa855d2708aa05ee524ca61b7a8888f0a4e68a7b3f03df8b080e90cd09` |
| `entregables/Ejemplo_migracion_Hermes_V6.3.xlsx` | `9e944384f166a5407b6acbdc888e53fa22527926b9cd5f92f12806f5f94f2df4` |
| `referencia/referencia_V6.3.json` (generada desde la plantilla anterior, mismo SHA) | `03f40e9df6e386480a92bb10cd518f86b29ae790de3c7e3e547e41e5f2e8f0d4` |

## 2. El defecto de cobertura: reproducido y corregido

| Receta de la revisión externa (Empresa X) | V6.3 del 29-oct | V6.3 de hoy |
|---|---|---|
| Motor B · 13 filas de datos documentadas · F53 (r) y F146 (crecimiento NORMAL) «Pendiente de inversor» | `Motor!B266` = **LISTO**, «documentadas 13 de 13», cero hipótesis pendientes | «NO LISTO · evidencias incompletas (26 pendientes) · cálculo completo»; «datos 13 de 17 · hipótesis confirmadas 0 de 22 · 9 hipótesis pendientes…» |
| Motor A · 15 filas documentadas · `C46` = 0, `C43` Transitorio, `C44` = 200 · F167 «Dato no verificable», J167 vacío | `C83` = 53,9956252725 y **LISTO** | mismo valor (el motor usa el FCF normalizado, y así lo dice `Historia!C71`); libro «NO LISTO · evidencias incompletas (30 pendientes)», «1 no verificables» |
| `Análisis!C76` (exceso de caja) fuera del inventario | modificaba el valor sin control | con `C76` = 50 y sin confirmar: «NO LISTO · (1 pendientes)»; confirmado: LISTO |

**Causa:** el inventario del 29-oct lo construí a mano con los *datos* que usa cada motor (23 filas) y
dejé fuera todas las *hipótesis* que mueven el valor, los metadatos de interpretación y las entradas
condicionales. La relación de hoy no sale de mi cabeza: sale de las fórmulas.

### 2.1 Relación independiente de entradas materiales

`scripts/trazar_entradas_materiales.py` hace dos cosas sin leer el inventario: una traza estática del
grafo de fórmulas desde las salidas (`Análisis B78:D78, C83, C84, C85, C86`, `Motor B252, B253, B254,
B267`, `Diagnóstico C156`) hasta las celdas editables, y una **activación empírica**: para cada celda
candidata, por motor y por configuración (base, quiebra activa, FCF base ≤ 0 con normalizado, exceso
de caja, ADR, desviación de capitalización, I+D capitalizada), cambia su valor, recalcula y mira si
alguna salida cambia. 492 recálculos; resultado en `pruebas/relacion_independiente.json`: **55
entradas mueven alguna salida**; 77 no.

Sobre eso, `scripts/relacion_entradas_materiales.py` fija la relación curada: **58 entradas** con
tipo (dato / hipótesis), motores, condición de uso (texto, fórmula Excel y predicado Python) y
período. Tres se añaden por razonamiento sobre la traza estática porque la perturbación tiene un
punto ciego con ellas, y está escrito cuál: `Palancas C43` (sus opciones Transitorio y Extraordinario
producen la misma rama), `Palancas C8` (el fixture tiene márgenes constantes, así que «Media del
ciclo» = «Último año») y `Palancas C6` (la opción perturbada solo avisa; «Financiera» bloquea A y B).
Dos se añaden por el encargo: `Control maestro J4` (unidad) y `L4` (norma contable), con sus filas de
trazabilidad nuevas (174 y 175). Las entradas editables que **no** están y por qué (filtro Pabrai,
indicadores auxiliares, anclas informativas, pistas, interruptores, parámetros de diseño) están en la
matriz, con la comprobación empírica detrás de cada exclusión.

Frente al inventario del 29-oct: **35 omisiones**, ahora cubiertas (`docs/Matriz_cobertura_evidencias_V6_3.md`).

Por motor, en la configuración base: A 43 entradas (19 datos, 24 hipótesis) · B 39 (17 / 22) ·
C 28 (10 / 18). Las condicionales se activan solas: probabilidad y recuperación de quiebra cuando
`C22 > 0`; `C43` cuando el FCF base ≤ 0 y `C44` además cuando la naturaleza es Transitorio o
Extraordinario; `C76` cuando está informado y no es 0; el ratio ADR cuando se declara ADR; la causa
de la desviación cuando la desviación supera el umbral de `Diagnóstico C91` o hay causa declarada.

### 2.2 Cinco estados, y una regla sobre las hipótesis

| Clasificación en Control maestro (col. F) | Dato | Hipótesis o decisión |
|---|---|---|
| «Rellenado y verificado» + documento en J | **documentada** | **incoherente**: una hipótesis no es un hecho verificado → pendiente |
| «Hipótesis confirmada» + justificación en J, M o N | incoherente: un dato se documenta, no se confirma → pendiente | **razonada y confirmada** |
| «Estimación declarada» + justificación | **estimación justificada** → PROVISIONAL | **estimación justificada** → PROVISIONAL |
| «Dato no verificable» | no verificable → pendiente | no verificable → pendiente |
| «Pendiente de inversor» | pendiente | **hipótesis pendiente** |
| «No aplicable» en una entrada que el motor usa | indebido → pendiente | indebido → pendiente |
| vacío, o confirmación/estimación sin justificar | pendiente | pendiente |

`Motor!B266`: `LISTO` solo con todos los datos documentados y todas las hipótesis confirmadas;
`LISTO · PROVISIONAL (n estimaciones justificadas)` en ámbar; `NO LISTO · evidencias incompletas (n
pendientes) · cálculo completo` en ámbar. El resumen (`Control maestro D250`, `Motor B269`,
`Análisis E6`, `Panel B3`) separa datos de hipótesis: «documentadas 17 de 17 · hipótesis confirmadas
22 de 22». No he confirmado ninguna hipótesis ni rellenado ninguna fuente en los ejemplos: Empresa X
muestra su valor y dice «NO LISTO · evidencias incompletas (43 pendientes)»; ABB conserva sus huecos
reales y sigue sin valor por `C49`.

### 2.3 Cobertura demostrada

Familia «9 · cobertura» de la batería, **149 casos generados desde la relación** (no desde el
inventario): para cada entrada activa de cada motor y configuración, se completa todo lo demás
(datos documentados, hipótesis confirmadas) y se deja esa entrada pendiente → el libro debe decir
exactamente «NO LISTO · evidencias incompletas (1 pendientes)». Positivos: todo documentado y
confirmado → `LISTO` en las once combinaciones motor × configuración; estimación justificada →
`LISTO · PROVISIONAL`; «No aplicable» en una entrada que el motor no usa (D&A en B, S2C en C) →
`LISTO`; probabilidad de quiebra vacía → no exige confirmación (convención documentada). Negativos:
no verificable, «No aplicable» indebido, estimación sin justificar, hipótesis sin justificar,
hipótesis marcada como hecho verificado. Todos superados; matriz en `docs/Matriz_cobertura_evidencias_V6_3.md`.

## 3. Lo que ya estaba corregido y se conserva

- **Ausencias ≠ cero** en Historia (6 casos de la familia: amortizaciones, capex, circulante, deuda,
  arrendamientos, caja) y en `Análisis C48/C49`; medias históricas sin años incompletos.
- **Moneda común** antes de ponderar en el motor B; sin conversión automática.
- **Conciliación de f** (`Historia 73–81`) con efecto en el estado: `C58` alterada → DATOS INVÁLIDOS.
- **Dominios económicos**: deuda bruta, arrendamientos, caja, minoritarios, D&A, capex, intereses,
  SBC, I+D y acciones no admiten negativos; pensiones como posición neta (superávit = 0 con aviso).
- **Verificador contra referencia aprobada** (`verificar_v63.py`): las cuatro manipulaciones
  obligatorias rechazadas nombrando la celda, diez entradas legítimas sin falsos positivos, los
  cuatro entregables ÍNTEGROS. La referencia se regeneró de la plantilla final después de pasar la
  batería, nunca desde un archivo sospechoso.
- **Motor C**: los dos fixtures (referencia original de `test_fill.py` y palancas del ejemplo A) se
  reproducen exactamente. **Motor B**: ponderaciones conservadas y etiquetadas como tasa
  personalizada. **Convenciones** escritas en `Convenciones_financieras_V6_3.md`.

## 4. Cambios de resultados

Los cálculos no cambian: Empresa X 25,8903521530 (A), 30,7047681226 (B), 17,8908417409 (C con
palancas de A), 11,8997522712 (C original). Cambia el **estado** de Empresa X: de «(15 pendientes)»
a «(43 pendientes)», porque ahora cuentan también las 24 hipótesis y los 4 metadatos que no tiene
documentados. Es lo correcto: es una empresa inventada.

## 5. Decisiones de implementación tomadas (reversibles)

1. Una hipótesis clasificada como «Rellenado y verificado» cuenta como **incoherente** y bloquea
   `LISTO`, aunque lleve documento: el encargo pide que una hipótesis futura no se presente como
   hecho histórico verificado. Lo mismo al revés (un dato «confirmado»).
2. La justificación de una hipótesis vale en J, M o N (documento, ajuste/criterio u observaciones),
   para no obligar a inventar un «documento» donde lo que hay es un razonamiento.
3. `Palancas C6` (caso especial) y `Análisis C62` (motor) se tratan como decisiones que hay que
   confirmar en todos los motores: determinan la aplicabilidad del modelo.
4. `Palancas C22` vacía y `Análisis C76` vacío o 0 **no** exigen confirmación (convenciones
   deliberadas, con aviso visible en el primer caso); se exige cuando se informan.
5. El filtro Pabrai (`C11:C13`) queda fuera del control de evidencias: es un gate de dominio
   controlado por el estado de inversión.

## 6. Reproducibilidad

`scripts/construir_v63.py originales/V6.1 salida` reproduce los cuatro entregables **byte a byte**
(fechas del paquete fijadas). Comprobado en esta entrega. La batería se ejecuta en dos tandas por
tamaño (`--excluir-familia 9` y `--solo-familia 9`) y se une con `unir_resultados.py`.

## 7. Lo que NO se ha comprobado

1. **Excel real.** Todo el recálculo es LibreOffice 24.2.7.2 headless. Controles, gráficos y VML son
   los de la V6.1 (hash en la referencia), pero deslizadores, colores, avisos de reparación y
   guardado/reapertura en Excel quedan **sin probar**.
2. **Booleanos en Historia** (regla V37): LibreOffice los lee como números.
3. **R03 y R08 desde sus insumos de origen** (`Hermes_evaluada.xlsx`, `abb_fase1.json`): no están en
   el material; se verifica la regresión sobre los ejemplos ya rellenos.
4. Cobertura con **dos configuraciones condicionales a la vez** (p. ej. quiebra + FCF normalizado):
   cada condición se probó por separado.
5. Combinaciones de tres o más ausencias; barrido de `Sector`, `Riesgo país` y metadatos de Control
   maestro que no entran en el cálculo.

## 8. Fuera de alcance, no tocado

Kit del personaje, personajes, lotes y cartera. Ninguna celda de `Análisis` cambia de dirección; los
nombres de las hojas se conservan; las salidas que el kit consume siguen fijas
(`Contrato_de_relleno_V6.3.csv`).

## 9. Erratas de informes anteriores

- Informe V6.2 §5.2: afirmé que las referencias del motor C eran irreproducibles y que el agente de
  réplica se equivocaba; el agente tenía razón (fixture con palancas propias de `test_fill.py`).
- Informe V6.3 del 29-oct: declaré el control de evidencias «con inventario explícito» cuando cubría
  solo los datos y no las hipótesis ni las entradas condicionales. Corregido aquí con una relación
  derivada de las fórmulas y 149 pruebas de cobertura.
