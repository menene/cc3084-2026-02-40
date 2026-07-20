# Demo: Deep Learning para Series de Tiempo (LSTM)

**Curso:** CC3084 · **Semestre 02, 2026**

Demostración de principio a fin de cómo se **pronostica una serie de tiempo con
una red neuronal recurrente (LSTM)**, alineada con la lección de Deep Learning
del curso. El cuaderno toca cada concepto de la clase: ventanas deslizantes,
escalado, división temporal, LSTM, métricas, overfitting y early stopping.

Todo el trabajo vive en un único cuaderno autocontenido:

```
notebooks/deep-learning-series-tiempo.ipynb
```

Usa la serie **Air Passengers** (144 valores mensuales, 1949-1960), incluida en
`data/raw/airline-passengers.csv`. Ver `codebook.md` para la descripción del
conjunto de datos.

## Contenido del cuaderno

1. Imports y reproducibilidad (semillas de NumPy y TensorFlow).
2. Carga y exploración de la serie (tendencia y estacionalidad).
3. Escalado a [0, 1] + versión rigurosa sin fuga de información.
4. **Ventanas deslizantes**: convertir la serie en un problema supervisado.
5. División temporal (el tramo final es la prueba; nunca se baraja).
6. Línea base (naive) como referencia.
7. Modelo **LSTM** con validación y **early stopping**.
8. Curva de pérdida: ver el overfitting y por qué early stopping ayuda.
9. Predicción y des-escalado a valores reales.
10. Métricas MAE / RMSE / MAPE (LSTM vs línea base).
11. Visualización de predicción vs real.
12. Pronóstico multi-paso iterativo (cómo se acumula el error).
13. Cierre, discusión y retos para el estudiante.

## Cómo correrlo

1. Crear el entorno e instalar dependencias:

```
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

2. Abrir el cuaderno y ejecutarlo de arriba hacia abajo:

```
jupyter notebook notebooks/deep-learning-series-tiempo.ipynb
```

> El cuaderno ya viene **renderizado** (con salidas incrustadas), así que el
> sitio Quarto no necesita ejecutar TensorFlow para publicarlo.

### Regenerar el cuaderno

El cuaderno se genera con un script y luego se ejecuta para incrustar salidas:

```
python build_nb.py
jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=600 \
  notebooks/deep-learning-series-tiempo.ipynb
```

## Estructura del proyecto

```
notebooks/  cuaderno con la demo completa (único entregable)
data/raw/         serie Air Passengers (airline-passengers.csv)
data/processed/   datos derivados (vacío: reservado para futuras salidas)
src/              scripts de apoyo (vacío: reservado)
build_nb.py       generador del cuaderno (nbformat)
codebook.md       descripción del conjunto de datos
requirements.txt  dependencias del proyecto
```

Las carpetas `data/processed/` y `src/` se dejan listas por convención, para
poder extender el proyecto sin reorganizar nada.
