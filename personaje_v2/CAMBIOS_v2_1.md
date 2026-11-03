# Cambios del personaje v2.0 → v2.1 (3-nov-2026) · NO INSTALAR hasta terminar la prueba de variabilidad con la v2.0

Origen: lo visto en Rational y Vidrala (primeras empresas reales) y la revisión independiente de la trazabilidad de Damodaran (`corpus/revision_trazabilidad.md`, agente Opus con contexto limpio: las 203 citas literales están bien; los resúmenes del Anexo B y del personaje decían a veces más de lo que el texto sostiene).

## Reglas nuevas (comportamiento de los agentes)
1. **Nada de calibrar a un umbral** (personaje §11 «Desviación económica» y prompt de la fase B): la cifra sale de los hechos; si los hechos la llevan al otro lado del umbral, se cruza y se justifica. Visto en Rational: S2C del BUENO = 3,9 «para no pasar de 2 × C55».
2. **La fase C devuelve las palancas mal derivadas** (prompt fase C turno 1, punto 3): aritmética, perímetro o dato equivocado → `revisar_palancas`, salvo que calcule y escriba que corregirla no cambia cubo ni zona y mueve el precio de Sí menos de un 5 %. Visto en Vidrala: S2C del NORMAL anotado como «error prudente».

## Citas: comprobación en cada fase (tras la prueba de variabilidad de Rational, 3-nov-2026)
La repetición de Rational llegó a la misma conclusión (Vigilar, esperar; precio de Sí 320,83 € frente a 336,87 €, −4,8 %), pero terminó en `no_entregable`: tres referencias a Damodaran con una página que existe pero no trata el principio citado («(CV p. 10, E1)»: E1 está en CV pp. 4–5). `verify_quotes_v2.py` solo comprobaba que la página existiera, y cada auditor encontró errores distintos cuando ya no quedaba vuelta a la fase B.
3. **`corpus/paginas_principios.json`**: para cada principio (I1–I3, E1–E9), las páginas de cada documento donde el texto lo sostiene (de la trazabilidad revisada).
4. **`verify_quotes_v2.py`**: una referencia que nombra un principio y una página de Damodaran tiene que caer en esas páginas (±1); cada principio nombrado en el paréntesis tiene que quedar cubierto. Prueba: detecta los tres casos de la repetición; el original de Rational y Vidrala pasan.
5. **`pipeline.py`**: las citas se comprueban en cuanto llega la salida de cada fase (A, B, C turno 1 y turno 2), con su .md y todos los textos del JSON; un fallo vuelve al mismo agente como corrección de formato. Límite: la comprobación es por principio, no por cada afirmación (p. ej. «doble cuenta» con PA p. 4 pasa porque E6 está en PA p. 4).
6. **Prompts A, B y C**: citar a Damodaran solo con páginas de la lista, o solo documento y principio sin página; pasar el verificador antes de entregar.
7. **`PROMPT_CLAUDE_CODE.md` §3**: la copia para la variabilidad lleva solo las entradas (etapa 1, PDF, texto, fase 1).

## Atribuciones a Damodaran corregidas (no cambia ningún umbral ni ningún script)
- **E2**: añadido MR pp. 62–63 (exceso a perpetuidad de 2–3 puntos sobre el coste «at best», suelo en el coste) y la preferencia de CV pp. 10–11, 17 por la media del sector. Declarado que el umbral de G4 (tasa + 10 puntos) es de la plantilla y mucho más laxo; el personaje dice que por encima de tasa + 3 puntos lo declara y lo sostiene.
- **NORMAL_ref de ROIC LP (= tasa)**: convención prudente, ya no «recuerda E2/E3» (CV p. 10 la atribuye a «algunos»; MR p. 62).
- **G16 (peso del terminal)**: ya no se apoya en E7; CV p. 23 dice que un peso alto es lo esperable. Umbral de la plantilla.
- **G17 y el techo de mercado**: convención del ejercicio, no NN.
- **E6**: acotado a las dos dobles cuentas de PA (pp. 20–21, 37–38) y a PA p. 40; lo demás es convención.
- **I1**: retorno **marginal**, no medio (GV p. 30; MR p. 51); «reinversión = Δventas ÷ S2C» es identidad del motor, no de GV.
- **E9**: «el motor C no valida la solvencia» pasa a [C]; FS prefiere dividendos al FCFE (p. 1).
- **Quiebra**: retirada la frase sobre tablas por rating a 5 años (no está en los textos).
- **E1, E4, E5, E8**: matices recuperados con página.
- Personaje y Anexo: retirado «cuando exista el corpus / hasta entonces»; ahora se cita documento y página.
- `trazabilidad_damodaran.md`: quitada la fila contradictoria de I2; páginas en lugar de «ver …»; el peso del terminal marcado como contrario a G16. `damodaran.md`: cuatro rótulos de principio ajustados a su cita (entradas 13, 36, 135, 179 de la revisión).

## Criterio cambiado con autorización de José Luis (3-nov-2026, 12:56)
- **G4 salta con ROIC LP > tasa + 0,03** (antes + 0,10), alineado con MR pp. 62–63. Parámetro `config_v2.json → convenciones.umbral_g4_roic_lp_sobre_tasa`; la referencia mecánica del BUENO pasa a mín(ROIC medio 5 años; tasa + 0,03) (`referencias_mecanicas.roic_lp_bueno_tope_sobre_c56`). El semáforo de la propia plantilla (`Diagnóstico V6!C43`) sigue en + 0,10: la plantilla no se toca.
- Efecto en las dos empresas hechas con la v2.0 (r = 0,09, umbral 0,12): **Rational** NORMAL 0,18 y BUENO 0,22 quedarían señalados (hoy solo el BUENO, con umbral 0,19); MALO 0,12 en el límite. **Vidrala** solo el BUENO (0,14). Señalado no es prohibido: exige decir cuánto dura la ventaja y qué la sostiene, con C18 = Sí.

Comprobado: `verify_quotes_v2.py --paginas-estrictas` PASS sobre el personaje v2.1 y sobre `damodaran.md`. Scripts cambiados respecto a la v2.0: umbral de G4 (`comprobar_gramatica.py`), nota de la referencia mecánica (`referencias_mecanicas.py`), comprobación principio↔página (`verify_quotes_v2.py`) y comprobación de citas por fase (`pipeline.py`); pruebas de regresión repetidas con la v2.1.
