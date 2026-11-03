# Réplica independiente de los tres motores · V6.2 · Empresa X

Réplica escrita en Python a partir de la **especificación** (`ESPEC_V6_1_rev4.md`, §0 y §5.2) y de los
**valores de entrada** del libro recalculado (`Ejemplo_V6.2_EmpresaX.xlsx`, hojas Historia / Palancas / Análisis,
`data_only=True`). No se leyó ninguna fórmula de la hoja `Motor`.

Entradas usadas: `V0 = 1000` (Historia C44) · `B0 = 600` (C59) · `ROE0 = 0,2375` (C60) · `m0 = 0,20` (C48, base
«Último año» de Palancas C8) · `τ = 0,25` (C52) · `f = 0,0139999999999999` (C58) · `r = 9 %` (Análisis C56) ·
`i = 0,0415384615384615` (C63) · `C64 = 250`, `C65 = 0`, `C66 = 100` · acciones = 100 (Análisis C55) ·
palancas B14:D18, g terminal B68:D68, probabilidades 0,2 / 0,6 / 0,2.

Réplica: `/tmp/claude-0/-home-claude/39782a3f-cde7-5f82-b097-9bbdcc06bca6/scratchpad/rep/final.py`

---

## 1 · Cifras: réplica frente al libro

Tolerancia exigida 1e-6. Las tres pasan.

### Motor A · `Análisis!C62 = "Sí"` (configuración entregada del libro)

| Escenario | Réplica | Libro `B78:D78` | Diferencia |
|---|---|---|---|
| MALO | 15,1023915686987 | 15,1023915686987 | −5,3e−15 |
| NORMAL | 25,0689493251303 | 25,0689493251303 | −1,4e−14 |
| BUENO | 39,1425212211033 | 39,1425212211033 | −2,1e−14 |
| Ponderado | 25,8903521530386 | `C83` = 25,8903521530386 | −3,2e−14 |

Redondeo a 3 decimales: 15,102 / 25,069 / 39,143 = referencia R01. **Coincide.**

### Motor B · `C62 = "No · financiación cambia mucho"` (copia recalculada con LibreOffice)

`r_op` replicada = 0,08399529042386185 vs `Diagnóstico V6!C15` = 0,0839952904238619 (dif −5,6e−17).

| Escenario | Réplica | Libro `B78:D78` | Diferencia |
|---|---|---|---|
| MALO | 17,3539528333579 | 17,3539528333579 | −3,6e−14 |
| NORMAL | 29,7144295704154 | 29,7144295704154 | +2,1e−14 |
| BUENO | 47,0265990683598 | 47,0265990683598 | +3,6e−14 |
| Ponderado | 30,7047681225928 | `C83` = 30,7047681225928 | −7,1e−15 |

Redondeo: 17,354 / 29,714 / 47,027 = referencia R01. **Coincide.**

### Motor C · `C62 = "No · banco o aseguradora"` (copia recalculada)

| Escenario | Réplica | Libro `B78:D78` | Diferencia | Referencia R01 |
|---|---|---|---|---|
| MALO | 10,9505167042730 | 10,9505167042730 | −2,5e−14 | 8,336 |
| NORMAL | 17,2492128342923 | 17,2492128342923 | −3,6e−14 | 11,978 |
| BUENO | 26,7560534971496 | 26,7560534971496 | −5,0e−14 | 15,229 |
| Ponderado | 17,8908417408599 | `C83` = 17,8908417408599 | −3,6e−14 | 11,900 |

**Réplica = libro a 5e−14, pero ninguna de las dos coincide con la referencia R01 de la especificación.**
Esto **no** es un fallo del motor C: la referencia R01 se calculó con **otro juego de palancas**. Reconstruido
el juego del arnés de pruebas (`scripts_V6.1.zip/test_fill.py`, bloque `if MOTOR == 'C'`):
g 0,03 / 0,06 / 0,08 · ROE objetivo 0,10 / 0,14 / 0,16 · ROE∞ 0,10 / 0,13 / 0,15.
Con esas palancas, mi réplica da **8,3362525831 / 11,9777149618 / 15,2293638877**, ponderado 11,8997522712
(dif máx. 4,2e−7 frente a las 6 cifras publicadas, limitada por el redondeo de la referencia).
**Las palancas de Empresa X en el libro entregado son 0,03/0,08/0,12 y 0,18/0,22/0,25 — las del motor A.**
La espec §5.2 enuncia los tres tríos de R01 como si salieran del mismo libro; no es así para el C.

---

## 2 · Convenciones que tuve que inferir (la espec NO las fija)

Declaro las cinco como **inferidas por reproducción**, no verificadas contra la especificación.

| # | Detalle que la espec deja sin determinar | Convención que reproduce el libro | Alternativas probadas y descartadas |
|---|---|---|---|
| I1 | Senda de crecimiento `V_t` entre los años 1–5 (palanca B14:D14) y el año 10 | `g_t = g₁₋₅` para t ≤ 5; de t = 6 a 10, **lineal** hasta `g₁₀ = g_terminal`: `g_t = g₁₅ + (g_T − g₁₅)·(t−5)/5` | lineal a 6 años (g₁₀ ≠ g_T), lineal a 4, plano a g₁₅, salto a g_T en t = 6 → error 0,20 a 2,13 por acción |
| I2 | Rampa del margen `m_t` hasta `m_obj` (Palancas B15:D15, «objetivo año 5») | **Lineal en 5 años desde `m₀`, inclusivo**: `m_t = m₀ + (m_obj − m₀)·min(t,5)/5`, luego plano. Con `m₀ = 0,20` = Historia C48 | rampa t−1 sobre 4 años (error 0,198), escalón a `m_obj` desde t = 1 (error 0,792) |
| I3 | Qué es `E` y qué es `D` en `r_op = r·E/(E+D) + i(1−τ)·D/(E+D)` | `E` = **capitalización de mercado** `Análisis!C41 = 2200`; `D` = **Historia C64 = 250** (deuda + arrendamientos), no C54 ni C64+C65−C66 | `E` = patrimonio contable 600 → 0,0727; `D` = 200 → 0,0851; `D` = 150 → 0,0862. Ninguna cuadra |
| I4 | En el motor C, cómo se proyecta `B_t` y cómo se rampa `ROE_t` | Mismas I1 e I2 trasladadas: `B_t` crece con la senda de ventas, `ROE_t` rampa lineal 5 años desde `ROE₀ = 0,2375` hasta `ROE_obj` = Palancas B15:D15. `τ` **no se aplica** (el ROE ya es neto) | Probadas 3 sendas × 4 rampas × 2 exponentes × 5 formas de terminal = 120 combinaciones; solo esta cuadra |
| I5 | Momento del `exceso de caja` (A) y del puente (B) | Se suman/restan **sin descontar**, en t = 0 | no verificable por valor: `C76 = 0` en este libro (ver §4) |

Confirmaciones cruzadas de I1 + I2 con celdas de salida independientes (NORMAL, motor A):
`C71` FCF año 10 = 248,947902639603 (réplica 248,94790263960346) · `C72` VP 1–10 = 986,960198437728
(réplica 986,9601984377282) · `C67` CAGR del FCF = 0,110677833087791 (réplica 0,11067783308779111) ·
`C74` % terminal = 0,606301729826246 (réplica 0,6063017298262463).

---

## 3 · Comprobaciones a mano

### a) El terminal del motor A está descontado 10 años, no 11 — **CORRECTO**

| Escenario | `V₁₀` | `FCF₁₁` | `TV = FCF₁₁/(r−g)` | `TV/1,09¹⁰` | Libro `B/C/D73` | `TV/1,09¹¹` |
|---|---|---|---|---|---|---|
| MALO | 1305,201678 | 125,142737 | 1787,753383 | **755,1663489935** | 755,1663489935 | 692,8131642 (−62,353) |
| NORMAL | 1847,619141 | 233,885488 | 3598,238277 | **1519,9347340753** | 1519,9347340753 | 1394,4355358 (−125,499) |
| BUENO | 2422,460488 | 362,730149 | 6045,502487 | **2553,6855836569** | 2553,6855836569 | 2342,8308107 (−210,855) |

Diferencia con 10 años: ≤ 2,3e−12. Con 11 años erraría 62 a 211 mm. El exponente es 10.

### b) Puente del motor B — **CORRECTO**, usa C64, C65 y C66

`Historia C64 = 250` (deuda + arrendamientos) · `C65 = 0` (pensiones + minoritarios) · `C66 = 100` (caja).
Pasivos netos = 250 + 0 − 100 = **150** = `Diagnóstico V6!C16`. ✓

| Escenario | Valor operativo (EV) | − 250 − 0 + 100 | Libro `B/C/D77` | Dif |
|---|---|---|---|---|
| MALO | 1885,39528334 | **1735,39528334** | 1735,39528334 | −3,6e−12 |
| NORMAL | 3121,44295704 | **2971,44295704** | 2971,44295704 | +2,3e−12 |
| BUENO | 4852,65990684 | **4702,65990684** | 4702,65990684 | +3,6e−12 |

Las cuatro partidas se restan y la caja se suma, tal como dice §0.

### c) Ajuste por quiebra — **CORRECTO**, y la recuperación NO se descuenta

Copia con `Palancas C22 = 0,30` y `C23 = 350`, recalculada. `C77` no cambia (1510,239 / 2506,895 / 3914,252):
el ajuste se aplica después y una sola vez, como dice Palancas A25.

| Escenario | Aritmética | Réplica | Libro `B78:D78` | Dif |
|---|---|---|---|---|
| MALO | 0,70 × 15,1023915687 + 0,30 × 3,50 | **11,6216740980890** | 11,6216740980890 | +2,0e−14 |
| NORMAL | 0,70 × 25,0689493251 + 0,30 × 3,50 | **18,5982645275911** | 18,5982645275911 | +4,3e−14 |
| BUENO | 0,70 × 39,1425212211 + 0,30 × 3,50 | **28,4497648547722** | 28,4497648547722 | +3,9e−14 |
| Ponderado | 0,2·11,6217 + 0,6·18,5983 + 0,2·28,4498 | **19,1732465071269** | `C83` = 19,1732465071269 | ~0 |

Si la recuperación se descontara 10 años al 9 %, el MALO daría 11,0152 (dif −0,606). **No se descuenta.** ✓

### d) Conciliación de `f` (Historia filas 73–81) — **CUADRA**

Ventana = `C57 = 3` últimos ejercicios (columnas J, K, L = 2023, 2024, 2025).

| Partida | Cálculo a mano | Celda del libro |
|---|---|---|
| Ventas medias | (857,338820 + 925,925926 + 1000) / 3 = **927,754915409236** | `C74` = 927,754915409236 |
| NOPAT medio | (128,600823 + 138,888889 + 150) / 3 = **139,163237311386** | `C75` = 139,163237311385 |
| Reinversión media | (42,866941 + 46,296296 + 50) / 3 = **46,387745770462** | `C76` = 46,3877457704618 |
| Flujo operativo implícito | 139,163237 − 46,387746 = **92,775491540924** | `C77` = 92,7754915409236 |
| FCF base que calibra | **79,786922725194** (= Análisis C52) | `C78` = 79,7869227251944 |
| Diferencia = fugas | 92,775492 − 79,786923 = **12,988568815729** | `C79` = 12,9885688157293 |
| f implícita | 12,988568815729 / 927,754915409236 = **0,014000000000000** | `C80` = 0,014 |

`Historia!C58` = 0,0139999999999999 → **dif = +5,4e−17**. `C81` = «✓ cuadra». Correcto.

---

## 4 · Incoherencias financieras encontradas

1. **R01 del motor C no es reproducible con el libro entregado** (ver §1). La espec §5.2 presenta los nueve
   números como «con la empresa de prueba», dando a entender un único juego de entradas. El motor C de R01
   usa palancas distintas (g 0,03/0,06/0,08 · ROE 0,10/0,14/0,16 · ROE∞ 0,10/0,13/0,15), tomadas del arnés
   `test_fill.py`. Con las palancas de Empresa X el motor C da 10,951 / 17,249 / 26,756. Un verificador que
   compare `B78:D78` del libro con las cifras de R01 concluiría, falsamente, que el motor C está roto.
2. **`r_op` del motor B usa la capitalización de mercado como peso del equity** (I3). El motor pondera con el
   precio (2200) el descuento que luego sirve para juzgar si ese precio es caro: hay realimentación del precio
   dentro del valor. La espec no dice qué es `E`, y la restricción §7.5 («sin coste medio ponderado del capital»)
   hace difícil defender pesos de mercado. Con `E` contable (600) el valor del NORMAL cambia de 29,71 a ~34.
3. **Salto de supuesto entre el año 10 y el 11 en los motores A y B.** `g₁₀ = g_T` ya (I1), pero `FCF₁₁` introduce
   de golpe el factor de reinversión `(1 − g/ROIC)`, que no está en ningún año 1–10. El FCF **cae** al pasar al
   terminal: −8,39 % (MALO), −6,05 % (NORMAL), −5,79 % (BUENO). Es defendible, pero es un escalón de hipótesis.
4. **`Análisis!E75` describe mal su propia celda.** La nota dice «(1 + g) ÷ (r − g)». Con r = 9 % y g = 2,5 % eso
   es 15,769231; el libro muestra 14,4537802449768, que es `TV / FCF₁₀` (el múltiplo efectivo, afectado por el
   escalón del punto 3). El número es el útil; el texto no corresponde.
5. **`Palancas B16:D16` (S2C) no se usa en el motor C** y la propia hoja lo marca «n/a» en el arnés, pero la
   regla de dominio de §2.2 («S2C > 0, motores A y B») y la celda `Diagnóstico V6!C16` siguen pobladas con el
   puente del motor B incluso cuando el motor activo es A o C (`C16 = 150` en la configuración de motor A).
   No afecta al valor; es ruido en el panel de diagnóstico.
6. **Discrepancia de etiqueta en el selector de motor C.** El libro entregado ofrece
   `"No · banco o aseguradora"`; el arnés de pruebas V6.1 escribe `"No · banco, aseguradora o regulada"`.
   Si el texto cambió sin actualizar el arnés, R01 del motor C no se habría ejecutado sobre el motor C.

---

## 5 · Lo que NO he podido comprobar

- **Momento del `exceso de caja` (I5, motor A).** `Análisis!B76:D76 = 0` en este libro, así que cualquier
  convención (sumar en t = 0 o descontada) da el mismo resultado. No verificado.
- **`Palancas C65` (pensiones + minoritarios) = 0** en todos los años. El puente del motor B sólo está
  comprobado para deuda + arrendamientos y caja; el signo del término de pensiones y minoritarios es
  conjetura leída de §0, no una comprobación numérica.
- **Las convenciones I1, I2 y I4 están inferidas, no verificadas.** Reproducen el libro a 5e−14 y son las únicas
  de 120 combinaciones que lo hacen, pero la especificación no las enuncia: otro implementador partiendo del
  mismo texto podría escribir legítimamente una rampa distinta y obtener un valor del NORMAL entre 24,9 y 27,2.
  Una réplica que cuadre no demuestra que la convención sea la pretendida.
- **No he verificado** la sensibilidad `B90:D92`, el DCF inverso `C86` (80 tramos), el Panel, las reglas de
  dominio §2.2 (T01–T18), ni ninguna de las otras pruebas de regresión R02–R06.
- **El origen del `0,0139999999999999` de `Historia!C58`** queda conciliado aritméticamente (§3d), pero no he
  comprobado que el perímetro contable de `C70` (Análisis C52, medias de 3 años de CFO, capex, intereses de
  financiación, arrendamientos y SBC) y el de `C75`–`C76` (EBIT, impuestos, capex − D&A + circulante de los
  mismos 3 años) sean el mismo perímetro. Si no lo fueran, `f` absorbería una diferencia de perímetro además
  de las fugas reales, y proyectarla como % constante de ventas no estaría justificado.
- **No he comprobado la ejecución de R01 tal como se registró.** `Resultados_pruebas_V6_1.md` declara T02c
  SUPERADA con 8,336253 / 11,977715 / 15,229364; esos valores son correctos **para su propio juego de
  palancas**, que no es el del ejemplo entregado. No puedo decir si la discrepancia es un defecto del registro
  de pruebas o una decisión deliberada no documentada.
