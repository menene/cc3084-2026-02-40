# Practica: Series de Tiempo (AR, MA, ARMA, ARIMA, SARIMA)

**Curso:** CC3084 · **Semestre 02, 2026**

Flujo completo de analisis y modelado de una serie de tiempo, desde el analisis
exploratorio hasta el pronostico final. El objetivo es **mostrar todas las
familias de modelos** (AR, MA, ARMA, ARIMA y SARIMA), validarlas y seleccionar
la mejor para el caso.

Todo el trabajo vive en un unico cuaderno autocontenido:

```
notebooks/series-de-tiempo.ipynb
```

El cuaderno **incrusta sus propios datos** (serie *Air Passengers*, 144 valores
mensuales, 1949-1960), por lo que corre sin conexion y sin archivos externos.
Ver `codebook.md` para la descripcion del conjunto de datos.

## Contenido del cuaderno

1. Carga y analisis exploratorio (EDA) con graficas.
2. Verificacion de supuestos: estacionariedad con ADF y KPSS.
3. Transformaciones para lograr estacionariedad (logaritmo y diferenciacion).
4. Lectura de ACF y PACF para proponer los ordenes p y q.
5. Construccion de **todos** los modelos: AR, MA, ARMA, ARIMA y SARIMA.
6. Validacion de residuos (diagnostico y Ljung-Box) y error fuera de muestra.
7. Comparacion (AIC, MAE, RMSE, MAPE) y **seleccion del mejor modelo**.
8. Validacion walk-forward y pronostico final con intervalos de confianza.

## Como correrlo

1. Crear el entorno e instalar dependencias:

```
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
pip install -r requirements.txt
```

2. Abrir el cuaderno y ejecutarlo de arriba hacia abajo:

```
jupyter notebook notebooks/series-de-tiempo.ipynb
```

## Estructura del proyecto

```
notebooks/  cuaderno con todo el analisis y modelado (unico entregable)
data/raw/         datos crudos (vacio: la serie va incrustada en el cuaderno)
data/processed/   datos derivados (vacio: reservado para futuras salidas)
src/              scripts de apoyo (vacio: reservado)
codebook.md       descripcion del conjunto de datos
requirements.txt  dependencias del proyecto
```

Las carpetas `data/` y `src/` se dejan listas por convencion, para poder
extender el proyecto (por ejemplo, exportar la serie o mover utilidades a
modulos) sin reorganizar nada.
