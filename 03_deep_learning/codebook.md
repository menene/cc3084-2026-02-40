# Codebook: serie Air Passengers

Conjunto de datos usado en `notebooks/deep-learning-series-tiempo.ipynb`. Es un
clasico de dominio publico, ideal para pronostico porque tiene **tendencia** y
**estacionalidad** anual muy marcadas. Los 144 valores estan en
`data/raw/airline-passengers.csv` y tambien se cargan desde una URL de respaldo
si el archivo no esta presente.

## Descripcion

Total mensual de pasajeros de aerolineas internacionales, de enero de 1949 a
diciembre de 1960 (12 anios x 12 meses = 144 observaciones).

| Variable   | Tipo (Python/pandas) | Descripcion                              | Valores / notas                                            |
|------------|----------------------|------------------------------------------|------------------------------------------------------------|
| Month      | str / datetime64     | Mes de la observacion                     | Formato `YYYY-MM`, frecuencia mensual, 1949-01 a 1960-12   |
| Passengers | int                  | Total de pasajeros en el mes, en miles    | Entero positivo, rango aprox. 104-622                      |

## Caracteristicas relevantes para el modelado

- **Tendencia** creciente sostenida a lo largo de los 12 anios.
- **Estacionalidad** anual (periodo = 12): picos en verano, valles en invierno.
- La amplitud estacional crece con el nivel de la serie. Para una LSTM esto no
  requiere log-transformar: basta con **escalar a [0, 1]** para que la red
  aprenda con estabilidad numerica.

## Preparacion para deep learning

- **Ventanas deslizantes**: la serie se convierte en pares (X, y) donde X son los
  `k` valores pasados y `y` es el valor siguiente. En el cuaderno `k = 12` (un
  ciclo estacional completo).
- **Escalado**: `MinMaxScaler` a [0, 1]. El cuaderno muestra la version rigurosa
  (ajustar el scaler **solo con el tramo de entrenamiento**) para no filtrar
  informacion del futuro.
- **Particion temporal**: el conjunto de prueba es el **tramo final** de la
  serie (ultimo 20%). Los datos nunca se barajan.

## Fuente

Box & Jenkins (1976), *Time Series Analysis: Forecasting and Control*. Serie
"AirPassengers", de dominio publico. Archivo CSV tomado del repositorio publico
`jbrownlee/Datasets` y usado aqui con fines didacticos.
