# Prompt para Claude Code · instalar el personaje Munger v2 y analizar empresas

Copia todo lo que hay debajo de la línea en Claude Code, abierto sobre el repositorio. Modelo de la sesión principal: **Sonnet, esfuerzo medio** (solo orquesta: lanza scripts y agentes). Los agentes de juicio los lanza él con el modelo que dice cada prompt.

---

Vas a instalar y usar el paquete `personaje_v2` (personaje Munger v2 para la Plantilla V6.3) que he subido a este repositorio como `personaje_v2_para_repositorio_<fecha>.zip`. Trabaja en español. Reglas que no se negocian:

- **No leas el resto del repositorio.** Solo puedes localizar, por nombre, dos carpetas que ya existen: `kit_pipeline_munger/` (debe contener `munger.md` y `scripts/add_cached_values.py`) y la carpeta del paquete V6.3 que contiene `entregables/Plantilla_V6.3.xlsx`, `referencia/referencia_V6.3.json` y `scripts/verificar_v63.py` (suele llamarse `v6/`). Usa `find . -maxdepth 4 -type d -name kit_pipeline_munger` y `find . -maxdepth 5 -path '*entregables/Plantilla_V6.3.xlsx'`. No abras otros archivos del repositorio.
- **No rebajes ningún criterio para que algo pase**: no cambies pruebas, umbrales, esquemas, la gramática ni los prompts para obtener un aprobado; no conviertas un bloqueo en aviso. Si algo falla, dime qué falla y por qué, corrige la causa si es un fallo de implementación (y anótalo en `personaje_v2/DECISIONES.md` con fecha), o para y pregúntame.
- **Nada de memoria**: los datos de las empresas salen de sus informes y, para precio y tipos, de fuentes web con nombre y fecha.
- Nunca declares terminado lo que no lo está. El estado final de cada empresa es el que da `pipeline.py`.

## 1. Instalar
1. Descomprime el zip en la raíz del repositorio (crea `personaje_v2/`). No muevas `kit_pipeline_munger/` ni `v6/`.
2. Comprueba la huella de la plantilla: `sha256sum <v6>/entregables/Plantilla_V6.3.xlsx` frente a `<v6>/referencia/SHA256_entregables_V6.3.txt`. Si no coincide, para y avísame.
3. En `personaje_v2/config_v2.json` ajusta las rutas de `plantilla.*` y `kit_v1.*` a las carpetas encontradas, **relativas a `personaje_v2/`** (mira `config_v2.ejemplo.json`: supone `../kit_pipeline_munger` y `../v6`). No toques nada más del config.
4. Instala lo que falte: Python 3 con `openpyxl lxml pypdf jsonschema` (`pip install …`), LibreOffice (`soffice`) y `pdftotext` (poppler-utils).
5. Desde `personaje_v2/`: `bash scripts/comprobar_entorno.sh`, `python3 scripts/precio_de_si.py --autotest`, `python3 pruebas/test_pieza1.py` (debe dar 17/17) y `python3 pruebas/test_pipeline_sintetico.py` (30/30; tarda ~15 min). Si algo no pasa, para y dime exactamente qué.
6. Lee `personaje_v2/README_v2.md` y `personaje_v2/ESTADO.md` (estado real y pendientes).

## 2. Analizar una empresa (repite por cada una que te pida)
Para la empresa `<E>` necesito de mí: la carpeta de la etapa 1 (`<E>_evaluada.xlsx` y `<E>_respuesta.md`) y los informes anuales de 10 años en PDF (cuentas consolidadas; con el año en el nombre del archivo).
1. Crea `personaje_v2/empresas_v2/<E>/etapa1/` con los dos archivos de la etapa 1 y `personaje_v2/empresas_v2/<E>/pdf/` con los PDF. Ejecuta `python3 scripts/pdf_a_texto.py empresas_v2/<E>`.
2. Bucle: `python3 scripts/pipeline.py empresas_v2/<E>`.
   - **Código 10** = espera a uno o varios agentes. Lee `empresas_v2/<E>/ESPERANDO.md`. Por cada agente que liste, lanza un subagente (herramienta Agent/Task) con el modelo y esfuerzo que dice la cabecera del prompt o `ESPERANDO.md` (`config_v2.json → modelos`: Sonnet medio para historia por año, metadatos y extracción; Opus alto para las fases A, B y C; Opus medio con contexto limpio para la verificación). Su instrucción es: «Tu instrucción completa está en `<ruta del prompt generado>`. Léela entera y cúmplela al pie de la letra.» Si `ESPERANDO.md` lista varios agentes (fase 1: uno por año + metadatos), lánzalos **en paralelo**.
   - **Fase C turno 2**: la debe hacer **el mismo agente** que hizo el turno 1 (continúalo con su id; no lances uno nuevo).
   - **Verificación (auditoría)**: siempre un agente **nuevo**, sin contexto del trabajo; no le digas qué esperas que encuentre.
   - Cuando los agentes hayan escrito sus salidas, vuelve a lanzar `pipeline.py`. Repite hasta que termine con **código 0**.
   - Si termina en `pendiente_de_datos` o `no_entregable`, lee `diagnostico.md`: si es un fallo de implementación (un script), corrige la causa, anótalo en `DECISIONES.md` y reanuda con `--desde <paso>`; si faltan datos, dime cuáles.
3. Resultado en `empresas_v2/<E>/`: `<E>_v63_evaluada.xlsx`, `informe.md`, `ficha.json`, `auditoria.md`, `historia_revision.md`. Dame en cuatro líneas: estado, cubo, acción, precio de Sí, precio, y lo que la auditoría o las fases marcaron como dudoso.

## 3. Prueba de variabilidad (cuando te la pida)
Crea `empresas_v2/<E>_rep/` copiando de `empresas_v2/<E>/` **solo las entradas**: `etapa1/`, `pdf/`, `texto/`, `fase1_partes/`, `fase1_v63.json`, `fase1_metadatos.json`, `fase1_fuentes.json`, `fase1_decisiones.json` (si existe) e `historia_revision.md`. Nada más (ni salidas de fases, ni libros, ni `ficha`, `celdas_*`, `gramatica.*`, `resultados.json`, `precio.json`, `verificacion_*`). Ejecuta el bucle del punto 2 con agentes nuevos. Compara con el original: motor, cubo, acción, palancas por escenario, probabilidades, precio de Sí y estado final. Escribe la comparación en `personaje_v2/pruebas/variabilidad_<E>.md`.

## 4. Commit
Cuando te lo pida: `git add personaje_v2/` **sin** `empresas_v2/*/pdf/`, `empresas_v2/*/texto/`, `empresas_v2/*/recalc/`, `corpus/pdf/` (están en `.gitignore`), commit con un mensaje que diga qué empresas se analizaron y su estado final, y push a una rama nueva (no a la principal).
