# Scripts V6.1 · reproducción completa (rutas configurables por argumento)

Requisitos: Python 3 con openpyxl 3.1, LibreOffice (soffice) en el PATH para recalcular, pdftoppm (poppler) y Pillow para las capturas.

1. Construir la plantilla (tema oscuro) a partir de la V5.3:
   `python3 build_v6.py plantilla_v53.xlsx Plantilla_V6.xlsx`   (añade `--claro` para el tema claro)
2. Añadir los seis deslizadores (siempre el último paso, sobre el archivo final):
   `python3 add_sliders.py Plantilla_V6.xlsx Plantilla_V6.1.xlsx`
3. Ejemplo Empresa X (y JSON con los valores esperados por la réplica en Python):
   `python3 test_fill.py Plantilla_V6.xlsx Ejemplo.xlsx A`   (A | B | C = motor)  → luego `add_sliders.py`
4. Pruebas automáticas (149; recálculo real con LibreOffice; escribe Resultados_pruebas_V6_1.md y resultados_pruebas.json):
   `python3 run_tests.py Plantilla_V6.xlsx Plantilla_V6.1.xlsx carpeta_salida`
   Necesita `plantilla_v53.xlsx` junto a los scripts (R02/R04) y, si existen, `../abb/abb_fase1.json` (R08) y la hoja de Hermès (R03, ruta en la constante HERMES).
5. Migración V5.3 → V6.1 por lista blanca con conciliación:
   `python3 migrate_values.py origen_v53.xlsx Plantilla_V6.xlsx salida.xlsx conciliacion.json`  → luego `add_sliders.py`
6. ABB con datos reales: `python3 fill_abb.py Plantilla_V6.xlsx abb_fase1.json Ejemplo_ABB.xlsx` → luego `add_sliders.py`
7. Capturas: `python3 render_panel.py archivo.xlsx salida.png` (Panel) · `python3 render_sheet.py archivo.xlsx "Hoja" A1:J60 salida.png`
8. Tema oscuro suelto: `python3 theme_dark.py entrada.xlsx salida.xlsx`

Identificación de versión: cada ejecución de run_tests.py registra el SHA-256 del archivo probado (prueba R00).
