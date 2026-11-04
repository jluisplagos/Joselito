# Prompt para una ventana nueva de Claude · analizar una empresa con el personaje Munger v2

Cómo usarlo: abre una conversación nueva en Claude (una por empresa), adjunta `munger_v2_paquete.zip` y pega todo lo que hay debajo de la línea, cambiando `<EMPRESA>`. Modelo de la conversación: **Sonnet, esfuerzo medio** (solo orquesta; los agentes de juicio se lanzan con Opus).

---

Vas a analizar la empresa **<EMPRESA>** con el personaje Munger v2 (etapa 2 de mi embudo: Plantilla V6.3). Trabaja en español. Antes de cada paso dime qué información necesitas de mí y con qué modelo y esfuerzo lo vas a hacer.

Reglas que no se negocian:
- No rebajes ningún criterio para que algo pase: no cambies pruebas, umbrales, esquemas, la gramática ni los prompts para obtener un aprobado, y no conviertas un bloqueo en aviso. Si algo falla y es un fallo de un script, corrige la causa, anótalo con fecha en `personaje_v2/DECISIONES.md` y dímelo; si faltan datos, pídemelos.
- Nada de memoria: los datos de la empresa salen de sus informes; precio y tipos, de fuentes web con nombre y fecha.
- Nunca declares terminado lo que no lo está: el estado final es el que da `pipeline.py`.
- El personaje no escribe tamaños de posición: eso lo decido yo.

## 1. Instalar (al empezar cada conversación)
1. Descomprime `munger_v2_paquete.zip` en tu carpeta de trabajo. Debe quedar `personaje_v2/`, `kit_pipeline_munger/` y `v6/` al mismo nivel. Las rutas de `personaje_v2/config_v2.json` ya apuntan a `../kit_pipeline_munger` y `../v6`; si no fuera así, ajústalas (relativas a `personaje_v2/`) y no toques nada más del config.
2. Instala lo que falte: `pip install --break-system-packages openpyxl lxml pypdf jsonschema`; comprueba que existen `soffice` (LibreOffice) y `pdftotext`.
3. Desde `personaje_v2/`: `bash scripts/comprobar_entorno.sh`, `python3 scripts/precio_de_si.py --autotest` y `python3 pruebas/test_pieza1.py` (17/17). La prueba larga `python3 pruebas/test_pipeline_sintetico.py` (30/30, ~15 min) solo si te lo pido o si has tenido que tocar un script. Si algo no pasa, para y dime qué.
4. Lee `personaje_v2/README_v2.md`, `personaje_v2/ESTADO.md`, `personaje_v2/RESUMEN_EMPRESAS.md` y los últimos `CAMBIOS_v2_*.md`.

## 2. Recibir mis archivos
Necesitas de la empresa: su etapa 1 (`<EMPRESA>_evaluada.xlsx` y `<EMPRESA>_respuesta.md`, de mi carpeta de lotes) y sus informes anuales de 10 años en PDF (cuentas consolidadas).
- Lo normal es que yo conecte una carpeta de mi escritorio con esos archivos: usa las herramientas de mi ordenador (listar la carpeta y traer los archivos) y no leas nada fuera de ella. Si no la he conectado, pídemelo o pídeme que los adjunte.
- Crea `personaje_v2/empresas_v2/<EMPRESA>/etapa1/` (los dos archivos de la etapa 1) y `personaje_v2/empresas_v2/<EMPRESA>/pdf/` (los PDF). Identifica por su contenido el ejercicio de cada PDF y llámalos `AR_<año>.pdf` (si el ejercicio no acaba en diciembre, el año es el del cierre). Dime si falta o se repite algún año.
- `python3 scripts/pdf_a_texto.py empresas_v2/<EMPRESA>`.

## 3. Ejecutar
Bucle: `python3 scripts/pipeline.py empresas_v2/<EMPRESA>`.
- **Código 10** = espera a uno o varios agentes: lee `empresas_v2/<EMPRESA>/ESPERANDO.md`. Por cada agente que liste, lanza un subagente con la herramienta de agentes, con el modelo y el esfuerzo que dice la cabecera de su prompt o `ESPERANDO.md` (`config_v2.json → modelos`: Sonnet medio para historia por año, metadatos y extracción; Opus alto para las fases A, B y C; Opus medio con contexto limpio para la verificación). La instrucción del subagente es: «Tu instrucción completa está en `<ruta del prompt generado>`. Léela entera y cúmplela al pie de la letra.» Si `ESPERANDO.md` lista varios (fase 1: uno por año más metadatos), lánzalos **en paralelo**.
- **Fase C turno 2**: la hace **el mismo agente** del turno 1 (continúalo con un mensaje; no lances uno nuevo).
- **Verificación (auditoría)**: siempre un agente **nuevo**, sin contexto; no le digas qué esperas.
- Cuando los agentes hayan escrito sus salidas, vuelve a lanzar `pipeline.py`. Repite hasta **código 0**.
- Si termina en `pendiente_de_datos` o `no_entregable`, lee `diagnostico.md`: fallo de un script → corrige la causa, anótalo y reanuda con `--desde <paso>`; faltan datos → dime cuáles.

## 4. Entregar
1. Dame un resumen de una página: estado final, cubo y acción, precio de Sí frente al precio actual, los tres escenarios con su valor y lo que tiene que pasar en cada uno, qué cambió respecto a la etapa 1 y por qué, y qué quedó dudoso.
2. Deja en mi carpeta conectada una subcarpeta `resultado_personaje_v2/` con `<EMPRESA>_v63_evaluada.xlsx`, `informe.md`, `ficha.json`, `auditoria.md` e `historia_revision.md`, y un zip de `empresas_v2/<EMPRESA>/` sin `pdf/`, `texto/` ni `recalc/` (para subirlo a mi repositorio si quiero).
3. Si has corregido algún script, dame también un zip con los archivos de `personaje_v2/` que cambiaste y `DECISIONES.md`, para actualizar mi paquete.
