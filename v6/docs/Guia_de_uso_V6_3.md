# Guía corta de uso · V6.3

1. **Copia** `entregables/Plantilla_V6.3.xlsx` para cada empresa. No escribas en las celdas de salida
   (`Análisis C52, B78:D78, C83:C86`; `Historia C44, C48, C52, C58, C70`; `Diagnóstico V6 C5, C12,
   C32`; `Panel K20, K25`): la regla V39 y el verificador las vigilan.
2. **Historia:** una celda vacía es un dato DESCONOCIDO. Escribe `0` cuando el cero esté comprobado.
   Deuda, arrendamientos, caja, minoritarios, D&A, capex, intereses, SBC, I+D y acciones nunca
   negativos. Pensiones: posición neta (déficit > 0; superávit < 0 se trata como 0). Las notas de
   fuente por fila van en la columna M.
3. **Motor** en `Análisis C62`. La hoja exige solo las partidas que ese motor usa, en los períodos que
   usa (`Contrato_de_relleno_V6.3.csv`, tabla por fila).
4. **Moneda:** `Palancas C48` (cotización) y `Control maestro H4` (modelo). Si difieren, no hay
   lectura de precio; con el motor B tampoco hay valor. La hoja no convierte: normaliza tú y anótalo.
5. **Evidencias:** en `Control maestro`, para cada entrada que el motor usa (el inventario, con su
   condición de uso, está en las filas 176–236 y el resumen en 238–250 y en `Panel B3`):
   - un **dato** (histórico, de mercado, metadato): columna F «Rellenado y verificado» + documento en J;
   - una **hipótesis o decisión** (motor, r, crecimiento, márgenes o ROE, S2C, ROIC/ROE terminal, g,
     probabilidades, quiebra, exceso de caja, FCF normalizado, base del margen, caso especial…):
     columna F «Hipótesis confirmada» + tu razonamiento en J, M o N. No la marques como «Rellenado y
     verificado»: una hipótesis no es un hecho, y la hoja lo cuenta como incoherente;
   - una **estimación** (dato o hipótesis): «Estimación declarada» + justificación → el libro queda
     `LISTO · PROVISIONAL`.
   `LISTO` solo cuando todo está documentado y confirmado. Lo que el motor no usa no bloquea nada.
6. **Lee el resultado** en `Análisis A6` (veredicto), `E6` (estados), `C83` (ponderado) y
   `E83` (la palanca que más lo mueve); en `Diagnóstico V6` bloque 10 (salto del año 11) y bloque 11
   (qué sostiene el valor; escribe tú la incertidumbre pendiente en B222:C223).
7. **Antes de fiarte de un archivo que no has construido tú:**
   `python3 scripts/verificar_v63.py archivo.xlsx referencia/referencia_V6.3.json`
   Código 0 = íntegro. Código 1 = alterado, con las celdas nombradas.
8. **Para reconstruir todo desde los originales:** `scripts/README_scripts_V6.3.md`.
