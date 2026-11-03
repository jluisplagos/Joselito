# Scripts V6.3 · reproducción completa

Dependencias explícitas: Python 3, `openpyxl >= 3.1`, LibreOffice (`soffice`) en el PATH para
recalcular. Capturas opcionales: `pdftoppm` (poppler) y Pillow. Sin rutas personales: todo por argumento.

| Script | Para qué |
|---|---|
| `construir_v63.py carpeta_V6.1 carpeta_salida` | Construye los cuatro entregables V6.3 desde los originales V6.1 (patch + deslizadores + gráficos canónicos) |
| `patch_v63.py entrada.xlsx salida.xlsx [--graficos-de Plantilla_V6.1.xlsx]` | Capa V6.3 sobre un libro de la familia V6.1 (importa `patch_v62_base.py`) |
| `add_sliders.py entrada.xlsx salida.xlsx` | Reinyecta los seis deslizadores · SIEMPRE el último paso (openpyxl los pierde) |
| `run_tests_v63.py carpeta_entregables carpeta_salida --referencia referencia_V6.3.json` | Batería de 94 pruebas con recálculo real; escribe `resultados_v63.json`; código 1 si alguna falla |
| `generar_referencia.py Plantilla_V6.3.xlsx referencia_V6.3.json --version V6.3` | Referencia aprobada: se genera UNA vez, de la plantilla final, después de las pruebas |
| `verificar_v63.py archivo.xlsx referencia_V6.3.json [--json salida.json]` | Verifica un libro contra la referencia; 0 íntegro · 1 alterado (nombra celdas) |
| `inventario_entradas.py` | Celdas que el usuario puede escribir; todo lo demás es fijo |
| `trazar_entradas_materiales.py Ejemplo_V6.3_EmpresaX.xlsx carpeta salida.json [--fase construir¦recalcular¦evaluar] [--max N]` | Relación INDEPENDIENTE de entradas materiales: traza estática + activación empírica (≈ 490 recálculos; por fases para no pasar de 10 min) |
| `relacion_entradas_materiales.py` | Relación curada (58 entradas: tipo, motores, condición de uso en Excel y en Python). De aquí sale el inventario de Control maestro y la familia 9 de pruebas |
| `unir_resultados.py parte1.json parte2.json salida.json` | Une tandas de `run_tests_v63.py` (`--solo-familia 9` / `--excluir-familia 9`) |
| `contrato_relleno.py Plantilla_V6.3.xlsx salida.csv` | Contrato de relleno para quien (persona o agente) rellene la hoja |

## Orden para reconstruir y verificar

```
python3 construir_v63.py ../originales/V6.1 salida
python3 run_tests_v63.py salida pruebas_a --referencia ../referencia/referencia_V6.3.json --excluir-familia 9
python3 run_tests_v63.py salida pruebas_b --referencia ../referencia/referencia_V6.3.json --solo-familia 9
python3 unir_resultados.py pruebas_a/resultados_v63.json pruebas_b/resultados_v63.json resultados_v63.json
python3 verificar_v63.py salida/Plantilla_V6.3.xlsx ../referencia/referencia_V6.3.json
```
Si cambia alguna fórmula del motor, vuelve a generar la relación independiente
(`trazar_entradas_materiales.py`, fases construir → recalcular → evaluar) y compárala con
`relacion_entradas_materiales.py` antes de reconstruir.
La reconstrucción debe dar los mismos SHA-256 que `referencia/SHA256_entregables_V6.3.txt`.

## Reglas

- La referencia no se regenera desde un archivo que se quiera verificar: eso anula la verificación.
  Solo se regenera al cerrar una versión nueva, desde su plantilla final, después de que pase la batería.
- Los libros recalculados por LibreOffice (`pruebas/.../rct`) no son entregables: pierden los
  controles de formulario. El verificador los rechazará por ese motivo, y es correcto.
- Scripts de la V6.1 que siguen siendo válidos sin cambios: `add_sliders.py` (incluido),
  `theme_dark.py`, `render_panel.py`, `render_sheet.py`, `migrate_values.py`, `fill_abb.py`,
  `test_fill.py` (réplica en Python de los tres motores; los fixtures del motor C salen de él).
- `verificar_integridad.py` de la V6.2 (comparador de desarrollo por lista blanca) no se incluye:
  aceptaba cualquier fórmula en una celda autorizada.
