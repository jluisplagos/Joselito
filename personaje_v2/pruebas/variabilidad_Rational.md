# Prueba de variabilidad · Rational AG (3-nov-2026)

Original: `empresas_v2/Rational/` (concluido, auditoría APROBADO). Repetición: `empresas_v2/Rational_rep/` (fases A, B, C y auditoría con agentes nuevos, mismos insumos de fase 1).

**Resultado de la repetición según `pipeline.py`: `no_entregable`** (paso 13). Causa registrada: «auditoría en REPETIR tras agotar las correcciones (nunca se aprueba por agotamiento)». Intentos: fase C 1, auditoría 3, vueltas C→B 1. No se ha corregido nada a mano ni se ha reanudado.

## 1. Cómo se hizo
- Copia de `Rational/` a `Rational_rep/` sin `fase_a.*`, `fase_b.*`, `fase_c.*`, `auditoria.md`, `estado_pipeline.json`, `ESPERANDO.md`, `prompts_generados/` ni los `*_v63_*.xlsx`. Se hizo con Python (no hay `rsync`).
- **Salvedad de método:** la lista de exclusión de la orden no cubre las salidas derivadas (`celdas_A/B/C.json`, `ficha.json`, `informe.md`, `gramatica.*`, `resultados.json`, `precio.json`, `verificacion_*`), que se copiaron y el pipeline sobrescribió al regenerarlas. Comprobé que el prompt de la fase A solo lee `datos_v63.md`, `extracto_v63.md` y el personaje, así que no vio la fase A original. No he comprobado de forma exhaustiva que ningún agente leyera una salida antigua antes de que se sobrescribiera.
- Agentes: fase A, B y C = Opus alto; auditoría = Opus medio, **uno nuevo por cada auditoría (tres)**. Las correcciones de B y C las hicieron los mismos agentes de B y C de la repetición (con contexto).
- Las probabilidades 0,2/0,6/0,2 (B69:D69) las hereda la etapa 1 en las dos pasadas: **no cuentan como evidencia de estabilidad**.

## 2. Comparación (original → repetición)
| Concepto | Original | Repetición | Dif. |
|---|---|---|---|
| Motor | A | A | igual |
| Cubo provisional (fase A) | Vigilar | Vigilar | igual |
| Cubo final / acción (fase C) | Vigilar · esperar | Vigilar · esperar (pero estado final `no_entregable`: `ficha.json` deja cubo y decisión en `null`) | igual en el juicio, no en el estado |
| Zona de la escalera | caro | caro | igual |
| g 1–5 (MALO/NORMAL/BUENO) | 1 % / 6,0 % / 10 % | 1 % / 5,5 % / 9 % | −0,5 / −1 pt |
| Margen objetivo | 22,5 / 26 / 27 % | 22 / 26 / 26,5 % | −0,5 / 0 / −0,5 pt |
| S2C | 2,0 / 3,5 / 3,9 | 2,5 / 3,5 / 4,0 | +0,5 / 0 / +0,1 |
| g perpetuo | 1,5 / 2,5 / 3 % | 1,5 / 2,5 / 3 % | igual |
| ROIC a largo plazo | 12 / 18 / 22 % | 9 / 15 / 19 % | −3 pt en los tres |
| Probabilidades | 0,2 / 0,6 / 0,2 | 0,2 / 0,6 / 0,2 | igual (heredadas) |
| Valor MALO / NORMAL / BUENO | 241,38 / 376,21 / 505,29 € | 232,72 / 360,81 / 465,26 € | −3,6 % / −4,1 % / −7,9 % |
| Ponderado | 375,06 € | 356,08 € | −5,1 % |
| **Precio de Sí** | **336,87 €** | **320,83 €** | **−4,8 %** |
| Precio actual | 630 € | 630 € | — |
| Celdas de juicio (fundamentadas / convención) | 49 / 17 | 45 / 21 | — |
| Desviaciones justificadas | 5 | 4 | — |
| Citas (Munger / Damodaran) | 35 / 2 | 39 / 21 | Damodaran ×10 |
| Auditoría | APROBADO (16/16) | REPETIR ×3 (falla la 6 «citas»; 15/16 pasan) | — |

Lectura: en lo sustantivo la repetición llega a la misma conclusión (Vigilar, esperar, zona caro, el precio es ~2× el de Sí). Las palancas se mueven pocos puntos y **todas las que difieren van en el mismo sentido (más prudentes)**, sobre todo el ROIC a largo plazo (−3 pt). El precio de Sí queda un 4,8 % por debajo. La dispersión es pequeña frente a la distancia al precio (630 € frente a 321–337 €). Con una sola repetición no puedo decir si ese sesgo a la baja es sistemático o azar.

## 3. Por qué termina `no_entregable`
La conclusión no cambia; lo que falla es la comprobación 6 (citas) de la auditoría. El script `verificacion_citas.txt` da PASS (solo comprueba que la página exista); la auditoría, hecha por un agente con `grep` sobre el corpus, comprueba además que la página trate lo citado.
1. **Auditoría 1:** «(CV p. 10, E1)» debería ser «CV p. 5». La fase C pidió la única vuelta a la fase B y se corrigió (sin mover valores).
2. **Auditoría 2** (agente nuevo): dos citas más, en fase B: Observación de Palancas!C22 «(PA p. 4, E6)» → p. 9, y Palancas!B18 «(CV p. 10, E2–E3)» → E3 está en CV p. 13. La vuelta C→B ya estaba gastada: la fase C solo pudo anotarlas en `incoherencias`.
3. **Auditoría 3** (agente nuevo): las mismas dos, sin corregir → REPETIR → `no_entregable`.

También quedó anotada, sin vuelta posible, una incoherencia de la fase A: el texto atribuye a C55 un ROIC medio de cinco años del 54 % cuando C55 = 0,41 (la auditoría dice que no cambia la conclusión).

## 4. Qué enseña la prueba (hechos y lectura)
- **Hecho:** el original citó a Damodaran con página 2 veces; la repetición, 21. Más citas con página = más superficie para errores de página que el script no detecta. Esa es la diferencia visible entre una pasada aprobada y otra no.
- **Hecho:** cada auditoría nueva encontró errores de cita distintos de los de la anterior. Lo que se aprueba o no depende también de qué cita revisa cada auditor: la auditoría es otra fuente de variabilidad.
- **Lectura (no probada):** el cuello de botella no es la tesis, sino que (a) la fase B corrige solo las citas que se le señalan, no revisa todas las suyas, y (b) la regla «una sola vuelta C→B» deja sin remedio los fallos de la segunda auditoría.
- Ningún criterio, umbral, prompt ni script se ha tocado.

## 5. Decisión pendiente (de José Luis)
No es un fallo de un script concreto, sino de diseño del proceso, así que no lo he corregido sin preguntar. Opciones: (1) dejar la prueba como está (resultado válido: el análisis es estable, el entregable no lo es); (2) cambiar el prompt de la fase B para que compruebe **todas** sus citas a Damodaran contra `corpus/damodaran.md` antes de escribir, y/o hacer que `verify_quotes_v2.py` compruebe que el principio citado está en la página, y repetir; (3) otra que prefieras.

## 6. Nota
El `diagnostico.md` de `Rational_rep` trae en «lo que sigue válido» «estado técnico INCOMPLETO», mientras que `ficha.json` y los agentes dicen «LISTO · PROVISIONAL». No lo he investigado.
