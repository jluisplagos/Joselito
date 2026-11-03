# Convenciones financieras de la V6.3 · las que antes se inferían, ahora escritas

Cada convención va con cómo se ha verificado. «Verificada por equivalencia» significa que una réplica
en Python escrita con esa convención reproduce el libro recalculado a menos de 5·10⁻¹⁴ en los tres
motores (`pruebas/resultados_v63.json`, casos R1–R4; réplica: `scripts/test_fill.py` de la V6.1).

## Los tres motores

| | Motor A · accionista | Motor B · operativo | Motor C · patrimonio y ROE |
|---|---|---|---|
| Flujo anual t = 1…10 | `V_t·[m_t·(1−τ) − f] − (V_t − V_{t−1})/S2C` | igual con `f = 0` | `B_{t−1}·ROE_t − (B_t − B_{t−1})` |
| Terminal (año 11) | `V_10·(1+g)·[m_obj·(1−τ)·(1 − g/ROIC) − f]` ÷ `(r − g)` | igual con `f = 0` y `r_op` | `B_10·(ROE_∞ − g)/(r − g)` |
| Descuento | r del inversor (Análisis C56) | `r_op` (abajo) | r del inversor |
| Puente al accionista | + exceso de caja (Análisis C76) | − deuda − arrendamientos − déficit de pensiones − minoritarios + caja | — |

## Convenciones (antes implícitas)

1. **Crecimiento.** Años 1–5 al ritmo de la palanca `Palancas B14:D14`. Años 6–10: baja en línea recta
   hasta el g para siempre (`Análisis B68:D68`), que se alcanza exactamente en el año 10:
   `g_t = g_5 − (g_5 − g_∞)·(t − 5)/5`. Verificada por equivalencia.
2. **Margen (ROE en el motor C).** Sube en línea recta desde el margen del último ejercicio
   (`Historia C48`; ROE0 = `L9/L21` en el motor C) hasta el objetivo en 5 años, y se mantiene:
   `m_t = m_0 + (m_obj − m_0)·min(t,5)/5`. Verificada por equivalencia.
3. **Reinversión.** Años 1–10: `(V_t − V_{t−1})/S2C`. Terminal: `g/ROIC` del flujo (factor
   `1 − g/ROIC`). En el año 11 la rentabilidad del capital pasa de `S2C·m_obj·(1−τ)` a `ROIC`; el salto
   se muestra en `Diagnóstico V6`, bloque 10, y avisa si supera `C179` (5 puntos). Es una hipótesis
   del analista, no un resultado.
4. **`r_op` del motor B** = `r·E/(E+D) + i·(1−τ)·D/(E+D)` con **E = capitalización bursátil**
   (`Análisis C41`), **D = deuda + arrendamientos del último ejercicio** (`Historia C64`),
   **i = intereses pagados ÷ deuda media de los dos últimos ejercicios** (`Historia C63`),
   **τ = tipo impositivo medio de 5 años** (`Historia C52`). Es una tasa personalizada derivada de la
   rentabilidad exigida por el usuario, de una aproximación histórica del coste de la deuda y de unos
   pesos de financiación observados; **no** es una estimación íntegra del coste de capital de
   mercado. Exige moneda común entre capitalización y deuda (regla V23) y deuda bruta ≥ 0.
   Verificada por equivalencia (decisión del encargo V6.3: se conserva).
5. **Caja, deuda y ajustes.** Se suman o restan al valor presente **sin descontar**: son saldos de
   la fecha de valoración. En el motor B: `− Historia C64 − C65 + C66`; en el A: `+ Análisis C76`.
   Verificada por equivalencia y a mano (caso S7 y réplica independiente de la V6.2).
6. **Quiebra.** Los tres escenarios se valoran suponiendo supervivencia. Después, una sola vez por
   escenario: `valor = (1 − p)·valor + p·recuperación`, con `p` = `Palancas C22` (vacío = 0 por
   convención, con aviso: no es un riesgo medido) y `recuperación` = `Palancas C23` **tomada como
   valor presente, sin descontar**. Si tu r ya incluye una prima por riesgo de quiebra, contarías el
   riesgo dos veces. Las guías por rating de Damodaran son acumulados a 5 años; la celda pide 10:
   no se convierten automáticamente. Verificada a mano (S7: 0,7×15,1024 + 0,3×3,5 = 11,6217).
7. **Historia: vacío = desconocido.** Un hueco nunca vale cero. El motor exige las partidas que usa en
   los períodos que usa (A: ventas, EBIT, D&A, tipo, capex y circulante en la ventana de `C57`
   ejercicios; B: intereses, deuda, arrendamientos, caja, pensiones y minoritarios del último
   ejercicio; C: beneficio y patrimonio del último ejercicio) y las medias históricas no se calculan
   con años incompletos. Para un cero comprobado se escribe `0`.
8. **Dominios.** Deuda bruta, arrendamientos, caja, minoritarios, D&A, capex, intereses, SBC, I+D y
   acciones no admiten negativos (DATOS INVÁLIDOS con la fila nombrada). FCF, resultados, CFO,
   circulante y adquisiciones netas sí. **Pensiones (fila 25) es una posición neta**: el déficit
   (> 0) se resta; un superávit (< 0) se trata como 0 y se avisa, porque no es caja disponible para
   el accionista sin más análisis. Un descubierto bancario va en deuda, no como caja negativa.
9. **Capitalización y precio.** `Análisis C55` son las acciones vigentes en la fecha de valoración;
   `Historia fila 20` es la media diluida del ejercicio. Su diferencia no es un error por sí sola.
   La capitalización vive en la moneda de cotización (`Palancas C48`); el modelo, en `Control
   maestro H4`. Sin coincidencia no hay lectura de precio (A, C) ni valor (B). La hoja no convierte
   divisas: pide el importe normalizado y su conciliación.
10. **f («fugas al accionista»)** = (NOPAT medio − reinversión media − FCF base) ÷ ventas medias, sobre
    la ventana `Historia C57`; conciliación visible en `Historia 73–81`. Recoge lo que el FCF base
    declarado ya absorbe (intereses, financiación neta, arrendamientos, SBC, adquisiciones) en la
    medida en que lo recoja. Proyectarla como % constante de ventas supone que escala con el
    negocio; si la financiación cambia mucho, usa el motor B. Un f negativo no es un error. Si la
    conciliación no cuadra con `C58`, el libro pasa a DATOS INVÁLIDOS (V39).
11. **Precio de referencia** = mín(valor MALO; k × ponderado), k en `Diagnóstico V6 C158` (0,75).
    Es una convención configurable, no una garantía de margen de seguridad ni una orden.
12. **Estados.** Estado técnico (DATOS INVÁLIDOS › MODELO NO APLICABLE › INCOMPLETO › COMPLETO Y
    VÁLIDO) y estado de inversión (filtro Pabrai) se calculan siempre. **Estado de las evidencias**
    (`Control maestro 176+`, `Motor B269`): cada entrada material del motor activo es un DATO (se
    documenta: «Rellenado y verificado» + documento) o una HIPÓTESIS o decisión (se razona y se
    confirma: «Hipótesis confirmada» + justificación; nunca se presenta como hecho verificado). Cinco
    estados por entrada: documentada · estimación justificada (resultado provisional) · hipótesis
    razonada y confirmada · hipótesis pendiente · dato no verificable. **Estado del libro**
    (`Motor B266`): `LISTO` solo con todos los datos documentados y todas las hipótesis confirmadas;
    `LISTO · PROVISIONAL (n estimaciones justificadas)`; `NO LISTO · evidencias incompletas (n
    pendientes) · cálculo completo`. Las entradas condicionales (quiebra, FCF normalizado, exceso de
    caja, ADR, causa de la desviación) se exigen solo cuando se usan. Una fuente declarada acredita
    documentación declarada por el analista, no que Excel haya comprobado el dato.

## Motor C · dos fixtures distintos

| Fixture | Palancas B14:D14 | B15:D15 | B18:D18 | Análisis B68:D68 | B78:D78 |
|---|---|---|---|---|---|
| Original de `test_fill.py` (referencia R01) | 0,03 / 0,06 / 0,08 | 0,10 / 0,14 / 0,16 | 0,10 / 0,13 / 0,15 | 0,02 / 0,025 / 0,03 | 8,3362525831 / 11,9777149618 / 15,2293638877 |
| Motor C con las palancas del ejemplo A | 0,03 / 0,08 / 0,12 | 0,18 / 0,22 / 0,25 | 0,10 / 0,15 / 0,20 | 0,02 / 0,025 / 0,03 | 10,9505167043 / 17,2492128343 / 26,7560534971 |

Son dos juegos de entradas; las ecuaciones son las mismas. Ambos se conservan como pruebas (R3, R4).
