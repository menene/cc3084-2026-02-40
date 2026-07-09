# Practica: Limpieza de datos (pipeline)

Se parte de un dataset de
ventas capturado "a mano" (`data/raw/ventas.csv`), con errores tipicos de
captura: tipos de dato mezclados, formatos de fecha inconsistentes, valores
nulos escritos de formas distintas, categorias mal escritas y duplicados.

En lugar de un unico script que hace todo, la limpieza esta organizada como un
pipeline de 4 etapas. Cada etapa hace una sola cosa, lee la salida de
la etapa anterior, la valida, la transforma y escribe su propio dataset.

## El pipeline

```
data/raw/ventas.csv
        │
        ▼
┌─────────────────────┐
│ 01_ingesta.py       │  carga el crudo como texto y unifica los nulos
└─────────────────────┘
        │  data/processed/01_ingesta.csv
        ▼
┌─────────────────────┐
│ 02_deduplicacion.py │  quita duplicados y garantiza id_venta unico
└─────────────────────┘
        │  data/processed/02_deduplicado.csv
        ▼
┌─────────────────────┐
│ 03_tipado.py        │  convierte cada columna a su tipo y dominio valido
└─────────────────────┘
        │  data/processed/03_tipado.csv
        ▼
┌─────────────────────┐
│ 04_features.py      │  agrega columnas derivadas (total_venta) y ordena
└─────────────────────┘
        │
        ▼
data/processed/ventas_limpio.csv   ← dataset final (ver codebook.md)
```

| Etapa | Archivo | Responsabilidad | Entrada | Salida |
|-------|---------|--------------------------|---------|--------|
| 1 | `src/01_ingesta.py` | Traer el crudo a texto uniforme y unificar los marcadores de nulo (`""`, `NA`, `N/A`, `null`, `-`, `?`...) a `NaN` | `data/raw/ventas.csv` | `data/processed/01_ingesta.csv` |
| 2 | `src/02_deduplicacion.py` | Eliminar filas duplicadas y garantizar `id_venta` unico | `01_ingesta.csv` | `data/processed/02_deduplicado.csv` |
| 3 | `src/03_tipado.py` | Convertir cada columna a su tipo correcto y a su dominio de valores validos | `02_deduplicado.csv` | `data/processed/03_tipado.csv` |
| 4 | `src/04_features.py` | Agregar columnas derivadas (`total_venta`) y ordenar el dataset final | `03_tipado.csv` | `data/processed/ventas_limpio.csv` |

Archivos de apoyo:

- `src/00_init.py` — prepara el entorno: crea el venv e instala dependencias.
- `src/config.py` — rutas de cada etapa y el "contrato" de columnas.
- `src/utils.py` — funciones compartidas de carga, guardado y validacion.
- `src/run_pipeline.py` — corre las 4 etapas en orden.
- `requirements.txt` — dependencias del proyecto.

## Como correrlo

1. Preparar el entorno (una sola vez). Se corre con el python del sistema;
crea un entorno virtual en `.venv/` e instala las dependencias de
`requirements.txt`:

```
python src/00_init.py
```

2. Activar el venv (una vez por terminal). Asi el comando `python` apunta al
del entorno y ya no hay que escribir la ruta `.venv/bin/...`:

```
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

Sabras que esta activo porque el prompt muestra `(.venv)` al inicio. Para
salir del entorno mas tarde: `deactivate`.

3. Correr el pipeline completo:

```
python src/run_pipeline.py
```

O correr una etapa a la vez (cada script es independiente y se ejecuta solo):

```
python src/01_ingesta.py
python src/02_deduplicacion.py
python src/03_tipado.py
python src/04_features.py
```

Siempre desde la raiz del proyecto, con el venv activado.

## Por que un pipeline y no un solo script

Toda esta limpieza cabria en un solo archivo que cargara, limpiara, tipara y
guardara de corrido. Preferimos dividirla en etapas encadenadas porque, tanto
para aprender como para un proyecto real, aporta ventajas concretas:

- **Una responsabilidad por archivo.** Cada script hace una sola cosa y se
  puede leer, entender y explicar por separado. Si algo sale mal en la
  deduplicacion, sabes exactamente que archivo mirar.

- **Datasets intermedios auditables.** Cada etapa deja su resultado en
  `data/processed/` (`01_ingesta.csv`, `02_deduplicado.csv`, ...). Puedes abrir
  el dataset "a medio limpiar" y ver exactamente que cambio en cada paso, en
  lugar de que ese estado intermedio viva solo en memoria y desaparezca.

- **Validacion entre etapas.** Cada etapa empieza validando la
  salida de la anterior: la etapa 2 confirma que los nulos ya fueron
  normalizados, la etapa 3 confirma que `id_venta` es unico, la etapa 4
  confirma que las columnas numericas son numeros. Si un supuesto no se cumple,
  el pipeline falla ahi mismo (fail-fast) con un mensaje claro, en vez de
  arrastrar datos malos hasta el resultado final.

- **Reejecucion parcial.** Si cambias solo la logica de features, corres la
  etapa 4 sobre `03_tipado.csv` sin volver a procesar todo desde el crudo.

- **Reutilizable y extensible.** Agregar un paso nuevo (por ejemplo, un
  `05_analisis.py`) es solo encadenar otra etapa que lee el dataset anterior;
  no hay que tocar el codigo que ya funciona.

- **Datos crudos intactos.** `data/raw/ventas.csv` nunca se modifica: es la
  fuente de verdad. Todo lo generado vive en `data/processed/` y se puede
  regenerar corriendo el pipeline.

En resumen: dividir el trabajo en etapas hace que el proceso sea mas facil de
**entender, validar y mantener** — que es justo de lo que trata el curso.

Ver `codebook.md` para la definicion de cada variable en el dataset limpio.
