# CC3084 · Data Science

Código de los laboratorios y proyectos del curso de Ciencia de Datos (CC3084,
UVG). Cada entregable vive en su propia carpeta, autocontenida y reproducible.

## Estructura

```
.
├── 01_lipieza_datos/     # Pipeline de limpieza de datos (ver su README)
└── README.md
```

Cada proyecto sigue la misma convención:

```
NN_nombre/
├── src/                 # scripts / etapas
├── notebooks/           # Jupyter notebooks (exploracion, EDA)
├── data/raw/            # datos crudos (fuente de verdad, no se modifican)
├── data/processed/      # datos generados (reproducibles, no se versionan)
├── requirements.txt     # dependencias
└── README.md            # instrucciones especificas
```
