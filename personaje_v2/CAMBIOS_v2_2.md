# Cambios del personaje v2.1 → v2.2 (3-nov-2026) · lo que enseñó Nike (primera empresa en US GAAP y dólares)

Nike terminó `concluido` con auditoría APROBADA (Vigilar, esperar; precio de Sí 18,69 $ frente a 39,12 $), pero dejó dos fallos de la fase 1, que es mía (pieza 7):

1. **EBIT con definiciones distintas según el año.** Los lectores por año incluían o no «Other (income) expense» (2024: 7.089 en la Historia frente a 6.311 del 10-K). Ahora cada lector entrega además `ebit_derivado` = resultado antes de impuestos − resultado financiero (solo intereses y partidas que la empresa agrupa en el bloque financiero; «Other (income) expense», participadas y extraordinarias quedan dentro). Si `ebit_derivado` está los diez años, `fase1_historia.py` lo usa para todos (misma definición) y anota en `historia_revision.md` cada año en que difiere del subtotal impreso; si no, usa el impreso y lo avisa. (`prompts/historia_anio.md`, `scripts/fase1_historia.py`.)
2. **Datos base del DCF vacíos (`Análisis!C46–C50`) cuando la etapa 1 no los trae.** En Nike el pipeline se paró en `pendiente_de_datos` (C48/C49) y Claude Code los escribió a mano. Ahora `fase1_historia.py` pone en `fase1_v63.json → analisis` la media de los últimos `anios_fcf_base` años de CFO, capex, intereses en financiación, principal de arrendamientos y SBC, con fuente; `rellenar_fase1_v63.py` solo los escribe en celdas vacías (la etapa 1 manda si los trae).

Probado: Vidrala reconstruida con la v2.2 da la misma Historia que con la v2.1 (sus ficheros no traen `ebit_derivado`) y los C46–C49 coinciden con la etapa 1 donde esta los tenía; una prueba con `ebit_derivado` elige el derivado y lo anota. Pruebas de regresión: ver DECISIONES.

No cambia ningún criterio, umbral ni prompt de juicio (fases A, B y C). Nike no necesita repetirse para la conclusión; solo para tener una Historia limpia en su Excel.
