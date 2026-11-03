# Corrección puntual de la norma contable · V6.3

Aplicada a la plantilla y a los tres ejemplos. En `Control maestro`, una norma contable ausente en `L4` ya impide alcanzar «LISTO», aunque su evidencia figure como documentada. La fila de evidencia muestra «falta norma contable». También se detectan espacios, tabulaciones, espacios no separables y fórmulas que devuelven texto vacío.

Cuando se informa la norma, siguen siendo necesarias su clasificación y su fuente. No se ha supuesto ni rellenado una norma en la plantilla ni en los ejemplos que la tenían vacía. Las normas ya presentes en ABB y Hermès se conservan.

Cambios: tres fórmulas (`L206`, `D248`, `D250`) y una etiqueta (`A248`) de Control maestro. Todas las demás fórmulas y entradas se conservan. Se mantienen los estilos, validaciones, controles, deslizadores, gráficos y demás partes nativas. Los resultados guardados se han actualizado mediante recálculo en LibreOffice.

Validación realizada sobre esta corrección:
- 14 casos dirigidos: ausencia y cumplimentación en los motores A, B y C; espacios; fórmula vacía; texto invisible; fórmula con norma; fuente ausente; estimación sin norma y con norma; dato no verificable. Todos superados, sin cambios en los valores de referencia.
- Los cuatro entregables recalculados y conformes con la nueva referencia de integridad.
- El verificador rechaza la eliminación de la nueva protección y la alteración de la fórmula de valoración. Acepta editar legítimamente la norma contable.
- Comparación de todas las celdas: solo cambian las cuatro indicadas. Las partes nativas ajenas a las hojas conservan sus bytes.

La referencia `referencia/referencia_V6.3.json` y `IDENTIFICACION_V6_3.txt` corresponden a esta entrega. El constructor y los datos sintéticos de la batería general se han actualizado para que incorporen esta corrección. No se repitió la batería general de 251 casos ni la reconstrucción byte a byte: sus informes, capturas, fixtures y resultados anteriores se conservan como antecedentes, no como pruebas nuevas de estos archivos. Para esta corrección, la evidencia actual está en `pruebas/correccion_norma_contable/`.

Para repetir las pruebas dirigidas:
`python3 scripts/test_norma_contable.py entregables salida_pruebas_norma`

Excel real sigue sin probarse. No se han certificado apertura, interacción con deslizadores o guardado en Microsoft Excel.
