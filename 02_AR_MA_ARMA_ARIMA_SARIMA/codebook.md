# Codebook: serie Air Passengers

Conjunto de datos usado en `notebooks/series-de-tiempo.ipynb`. Es un clasico de
dominio publico, ideal para series de tiempo porque tiene **tendencia** y
**estacionalidad multiplicativa** muy marcadas. Los 144 valores estan
incrustados directamente en el cuaderno, por lo que no hay archivo en `data/`.

## Descripcion

Total mensual de pasajeros de aerolineas internacionales, de enero de 1949 a
diciembre de 1960 (12 anios x 12 meses = 144 observaciones).

| Variable   | Tipo (Python/pandas) | Descripcion                                   | Valores / notas                                  |
|------------|-----------------------|-----------------------------------------------|--------------------------------------------------|
| fecha      | datetime64 (indice)   | Mes de la observacion                          | Frecuencia mensual `MS` (inicio de mes), 1949-01 a 1960-12 |
| pasajeros  | int                   | Total de pasajeros en el mes, en miles         | Entero positivo, rango aprox. 104-622            |

## Caracteristicas relevantes para el modelado

- **Tendencia** creciente sostenida a lo largo de los 12 anios.
- **Estacionalidad** anual (periodo = 12) cuya amplitud crece con el nivel de la
  serie: estacionalidad *multiplicativa*.
- Por eso el cuaderno trabaja con el **logaritmo** de la serie (convierte la
  estacionalidad multiplicativa en aditiva y estabiliza la varianza) y aplica
  diferenciacion regular (`d=1`) y estacional (`D=1`, `s=12`) para alcanzar
  estacionariedad, confirmada con las pruebas ADF y KPSS.

## Particion

Se reservan los **ultimos 24 meses** (1959-01 a 1960-12) como conjunto de
prueba. La prueba es siempre posterior en el tiempo: los datos nunca se barajan.

## Fuente

Box & Jenkins (1976), *Time Series Analysis: Forecasting and Control*. Serie
"AirPassengers", de dominio publico, incluida en multiples librerias
(statsmodels, R datasets) y usada aqui con fines didacticos.
