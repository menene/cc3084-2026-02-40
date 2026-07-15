# CC3084 · Data Science

Código de los laboratorios y proyectos del curso de Ciencia de Datos (CC3084,
UVG). Cada entregable vive en su propia carpeta, autocontenida y reproducible.

## Sitio publicado

Los cuadernos se publican como un sitio web en GitHub Pages:

**https://menene.github.io/cc3084-2026-02-40/**

El sitio se regenera solo en cada push a `main` (ver
`.github/workflows/publish.yml`). Los cuadernos ya vienen renderizados, así que
la publicación no ejecuta código: solo arma el HTML.

## Descargar el código

Para tener los archivos localmente (código, datos crudos y cuadernos):

```
git clone https://github.com/menene/cc3084-2026-02-40.git
```

O desde GitHub: botón **Code → Download ZIP**. Cada carpeta `NN_*/` trae su
propio `README.md` con instrucciones para correrla.

## Estructura

```
.
├── 01_lipieza_datos/               # Pipeline de limpieza de datos (ver su README)
├── 02_AR_MA_ARMA_ARIMA_SARIMA/     # Series de tiempo (ver su README)
├── _quarto.yml                     # config del sitio Quarto (publica todos los cuadernos)
├── index.qmd                       # portada del sitio
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
