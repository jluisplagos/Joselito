# ANEXO C · Precio de Sí y escalera de precios (`precio_de_si.py`)

Versión 0.2 (1-nov-2026). Decisión D11. **La escalera es una convención experimental del ejercicio**: su definición matemática y su parámetro k están fijados para poder estudiarla empresa a empresa, y **su suficiencia inversora no está demostrada**. Se calcula **fuera de la hoja**, a partir de la copia recalculada por LibreOffice con **recálculo forzado** (encargo §1.4: sin él la copia conserva valores viejos). No toca ninguna celda. El script **no decide nada**: produce una lectura aritmética de los valores y probabilidades que Munger introdujo; la conclusión depende además del fundamento material (D10) y de los bloqueos (D17), que mandan sobre cualquier zona.

## C.1 Entradas (leídas de `recalc/<Empresa>_v63_evaluada.xlsx` con `data_only=True`; en modo `--copia` de `comprobacion_conjunta/recalc/<Empresa>_conj.xlsx`)

| Dato | Celda | Nota |
|---|---|---|
| Valor por acción MALO / NORMAL / BUENO | `Análisis!B78` / `C78` / `D78` | Ya incluyen el recorte por quiebra si `Palancas!C22` > 0. Si alguno no es numérico, no hay escalera. |
| Probabilidades | `Análisis!B69:D69` | Deben sumar 1 (si no, la hoja no da ponderado y no hay escalera). |
| Valor ponderado | `Análisis!C83` | |
| Precio actual y moneda | `Análisis!C37`, `Palancas!C48` | La moneda debe coincidir con `Control maestro!H4` (`Motor!B253` = VERDADERO); si no, «sin lectura de precio». |
| Estado técnico | `Motor!B255` = `COMPLETO Y VÁLIDO` y `Motor!B252` = FALSO | Si no, no hay escalera. |
| Tabla del DCF inverso | `Análisis!A108:B188` (crecimiento años 1–5 → valor por acción) y `Motor!B193` | Para el crecimiento implícito en cada precio. |
| Crecimiento NORMAL años 1–5 | `Palancas!C14` | |
| Precio de referencia de la hoja (regla antigua) | `Diagnóstico V6!C156` | Se informa; no decide. |
| k | `config_v2.json` → `k_asimetria` (3) | Convención del ejercicio. |

## C.2 Definición

Para un precio P, con escenarios i de valor V_i y probabilidad p_i:

- Ganancia esperada: **G(P) = Σ p_i · máx(V_i − P, 0)**
- Pérdida esperada: **L(P) = Σ p_i · máx(P − V_i, 0)**
- **P\*** = el precio más alto que cumple **G(P) ≥ k · L(P)**.

Propiedades (las comprueba el script): F(P) = G(P) − k·L(P) es continua, lineal a trozos y decreciente; para P ≤ mín V_i se cumple siempre (L = 0); por tanto P\* existe, es único y **P\* ≥ mín V_i**. En P = ponderado, G = L, así que con k > 1 se tiene **P\* < ponderado** siempre que algún escenario esté por debajo del ponderado (el tope «nunca por encima del ponderado» de la conversación queda garantizado por construcción y el script solo lo verifica).

Lo que estas propiedades **no** dicen: G y L son esperanzas sobre tres valores elegidos por Munger con tres probabilidades elegidas por Munger. Que P\* ≥ V_MALO es aritmética, no una afirmación de que el MALO acote la pérdida. Ni G/L ni el margen frente al ponderado miden riesgo (identidad I4 del Anexo B).

## C.3 Forma cerrada (sin iterar)

Ordenar los escenarios por valor: V₍₁₎ ≤ V₍₂₎ ≤ V₍₃₎. P\* está siempre en [V₍₁₎, V₍₃₎] (por encima de V₍₃₎, G = 0 y L > 0; P\* = V₍₃₎ solo si los tres valores coinciden). En el tramo [V₍ⱼ₎, V₍ⱼ₊₁₎], donde los escenarios de índice ≤ j quedan por debajo de P y los de índice > j por encima:

**P = ( Σ_{i>j} p_i·V_i + k · Σ_{i≤j} p_i·V_i ) ÷ ( Σ_{i>j} p_i + k · Σ_{i≤j} p_i )**

Se prueba j = 1 y después j = 2, y se acepta el primer P que cae dentro de su tramo (el caso degenerado de valores iguales resuelve ya en j = 1; j = 3 nunca hace falta). Con tres escenarios son como mucho dos divisiones.

## C.4 Escalera y comprobaciones encima

0. **Orden de los valores:** el script exige `B78` ≤ `C78` ≤ `D78`. Si no se cumple (G1a ordena las palancas, no los valores), devuelve «sin escalera · valores desordenados»: es el **error** G19 del Anexo B (condición N6), que vuelve a la fase B una vez y, si persiste, termina en `no_entregable`.
1. **Precio del escenario MALO** = V_MALO (`B78`). Es el valor por acción que producen las palancas del escenario MALO, con sus probabilidades de quiebra ya aplicadas. **No es un suelo de valor ni la pérdida máxima posible**: el MALO es una historia elegida; la realidad puede ser peor, y la quiebra está modelada como un recorte único. Si V_MALO ≤ 0, «sin precio del escenario MALO» (la hoja además avisa: V36).
2. **Precio de Sí** = mín(P\*, V_NORMAL). El tope V_NORMAL es la comprobación del DCF inverso de D11 en forma exacta **cuando la tabla es estrictamente creciente** (`Motor!B193` = «✓ PASA») y `Palancas!C14` está en [−10 %, +30 %]: con las palancas del NORMAL, el crecimiento implícito en un precio P es ≤ el crecimiento NORMAL si y solo si P ≤ V_NORMAL (el valor del NORMAL es, por construcción, el de la tabla del DCF inverso en el crecimiento `C14`). El script lo verifica: interpola la tabla `A108:B188` en `C14` y compara con `C78` (tolerancia 1 %). Si no cuadran o `B193` ≠ «✓ PASA», el tope sigue siendo V_NORMAL (es la condición económica: no pagar más que el escenario central), el crecimiento implícito se marca «no utilizable» y se anota en `precio.json` y en la ficha.
3. **Ponderado** = `C83`.
4. **Zona del precio actual:** `bajo_malo` si precio ≤ precio del escenario MALO · `cumple_regla_k` si precio ≤ precio de Sí · `vigilar` si precio ≤ ponderado · `caro` si precio > ponderado. La zona dice si el precio **cumple la regla matemática** (k) con los valores introducidos. **No** dice que haya fundamento suficiente para una conclusión favorable (D10) ni anula ningún bloqueo (D17): la fase C y el pipeline deciden eso antes de mirar la zona (encargo §8).
5. **Crecimiento implícito** (interpolación lineal en la tabla): al precio actual y al precio de Sí. Al precio actual debe coincidir con `Análisis!C86` cuando `C86` es numérico (tolerancia 0,5 pt); si `C86` es texto («FCF ≤ 0», «< -10%», «> 30%»), el script reproduce ese mismo texto y no compara números.
6. **Tasa de descuento como palanca más influyente** (`Diagnóstico V6!C221` = «Tasa de descuento (±1 pt)»): el script lo anota (aviso A5 del Anexo B) para que la ficha diga que el valor depende sobre todo de la r exigida. El tornado se informa; **no es criterio** de nada (D10). Condición previa para leerlo: `B215:B220` numéricos y alguno > 0; si todos son 0 o vacíos, se anota «sin tornado».
7. **Descalificadores y fundamento:** la fase C puede imponer No / Demasiado difícil por encima de cualquier zona, y la falta de fundamento material (D10) deja el análisis en `pendiente_de_investigacion` por encima de cualquier zona. El script no decide el cubo ni el estado; solo la escalera.
8. **Distancias:** (precio − precio de Sí) ÷ precio y (precio − precio del escenario MALO) ÷ precio, como insumos para la decisión de cartera (D16) y la lista de vigilancia futura.
9. **Modo `--copia`** (comprobación conjunta, Anexo B §B.6): mismas lecturas sobre la copia de prueba recalculada; escribe `escalera_bajo_combinacion` en `comprobacion_conjunta.json` (valores, P\*, precio de Sí, zona del precio actual). La fase C compara las dos escaleras; el script no concluye.

## C.5 Casos de prueba (k = 3)

| Caso | V (MALO, NORMAL, BUENO) | p | P\* | G(P\*) | L(P\*) | Ponderado | Precio de Sí = mín(P\*, V_N) | Precio esc. MALO |
|---|---|---|---|---|---|---|---|---|
| 1 · tramo [MALO, NORMAL] | 60, 100, 150 | 0,25 / 0,50 / 0,25 | **88,3333** | 21,25 | 7,0833 | 102,5 | 88,33 | 60 |
| 2 · tramo [NORMAL, BUENO] | 90, 100, 160 | 0,2 / 0,6 / 0,2 | **102,3077** | 11,5385 | 3,8462 | 110 | **100** (tope NORMAL) | 90 |
| 3 · degenerado | 100, 100, 100 | 0,2 / 0,6 / 0,2 | 100 | 0 | 0 | 100 | 100 | 100 |
| 4 · MALO negativo | −20, 80, 200 | 0,2 / 0,6 / 0,2 | 54,2857 | 44,5714 | 14,8571 | 84 | 54,29 | sin precio del escenario MALO |
| 5 · BUENO muy gordo | 40, 70, 300 | 0,3 / 0,5 / 0,2 | 77,3077 | 44,5385 | 14,8462 | 107 | **70** (tope NORMAL) | 40 |

Comprobación del caso 1 a mano: con P = 88,33: G = 0,5·(100 − 88,33) + 0,25·(150 − 88,33) = 5,83 + 15,42 = 21,25; L = 0,25·(88,33 − 60) = 7,08; G ÷ L = 3,00. Caso 2: en el tramo [90, 100] la fórmula da 104,29 > 100, fuera del tramo; en [100, 160] da (0,2·160 + 3·(0,2·90 + 0,6·100)) ÷ (0,2 + 3·0,8) = 266 ÷ 2,6 = 102,31, dentro.

Propiedades que el script prueba además de los cinco casos: G(P\*) − k·L(P\*) = 0 (|·| < 1e-9); P\* ≥ mín V; P\* ≤ ponderado; P\* decrece al subir k; el resultado no depende del orden en que lleguen los escenarios; con probabilidades que no suman 1 el script se niega.

## C.6 Pseudocódigo

```
leer V = [B78, C78, D78], p = [B69, C69, D69], precio = C37, pond = C83, k
si no COMPLETO_Y_VALIDO o Motor!B252 o no comparable(moneda) o algún V no numérico o |Σp − 1| > 1e-3: devolver {sin_lectura: motivo}
si no (B78 ≤ C78 ≤ D78): devolver {sin_escalera: "valores desordenados", error: "G19"}
s = ordenar(zip(V, p)) por V            # s[1], s[2], s[3] (índices 1..3, como en §C.3)
para j en 1..2:
    bajo = s[1..j]; alto = s[j+1..3]
    P = (Σ_alto p·V + k·Σ_bajo p·V) / (Σ_alto p + k·Σ_bajo p)
    si s[j].V − 1e-12 ≤ P ≤ s[j+1].V + 1e-12: P* = P; salir
afirmar que P* existe, G(P*) − k·L(P*) ≈ 0, P* ≥ s[1].V, P* ≤ pond
V_normal = C78
tabla_ok = (Motor!B193 == "✓ PASA") y (−0,10 ≤ C14 ≤ 0,30) y |interpolacion(tabla, C14) − V_normal| ≤ 1 % · V_normal
precio_si = min(P*, V_normal) ; precio_escenario_malo = B78 si B78 > 0 si no null
zona = clasificar(precio, precio_escenario_malo, precio_si, pond)     # bajo_malo | cumple_regla_k | vigilar | caro
si tabla_ok: g_impl_actual = interpolar_inversa(tabla, precio) ; g_impl_si = interpolar_inversa(tabla, precio_si)
si no:      g_impl_actual = g_impl_si = "no utilizable" ; anotar
si tabla_ok y C86 es numérico: afirmar |g_impl_actual − C86| ≤ 0,005 ; si C86 es texto: g_impl_actual = C86
aviso_tasa = (C221 == "Tasa de descuento (±1 pt)") si hay tornado si no "sin tornado"
escribir precio.json {V, p, k, P_estrella, precio_si, precio_escenario_malo, ponderado, zona, g_impl_actual, g_impl_si,
                      C156, distancias, aviso_tasa, convencion: "escalera experimental, k = 3; la zona no es la conclusión", notas}
```

En modo `--copia` el mismo bloque se ejecuta sobre la copia de prueba y el resultado va a `comprobacion_conjunta.json` → `escalera_bajo_combinacion`.

## C.7 Qué dice la ficha y el informe

«Precio actual X (moneda). Escalera (convención experimental, k = 3): precio del escenario MALO A (no es un suelo de valor) · precio de Sí B · ponderado C. Zona: <zona>. La zona dice si el precio cumple la regla de precio con mis valores; la conclusión depende además del fundamento material (D10) y de los bloqueos (D17). El precio actual descuenta un crecimiento de ventas del g % a cinco años (NORMAL: n %). Regla antigua de la hoja (mín(MALO, 0,75 × ponderado)): D.»

Si hubo comprobación conjunta: «Bajo la combinación adversa documentada (…), el precio de Sí sería B′ y la zona <zona′>. Comprobación conjunta <superada | no superada>; superarla no es una garantía de seguridad.» Si el estado es `pendiente_de_investigacion`: «Sin conclusión de compra: <hipótesis> no puede acotarse con la evidencia disponible; lo resolvería <dato>.» Si la palanca más influyente es la tasa de descuento: «El valor depende sobre todo de tu rentabilidad exigida (r = …).»
