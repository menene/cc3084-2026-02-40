# Demo — Deep Learning para Series de Tiempo (pronóstico con LSTM)

Instrucciones para construir un notebook de demostración en Jupyter, alineado con la
lección **Deep Learning** de cc3084. El objetivo es que un estudiante vea, de principio a fin,
cómo se pronostica una serie de tiempo con una red neuronal, tocando cada concepto de la clase:
ventanas deslizantes, escalado, división temporal, LSTM, métricas, overfitting y early stopping.

> Cómo usar este archivo: cada sección de abajo es una celda (o par de celdas markdown + código)
> del notebook. Sigue el orden. El código está listo para copiar; comenta todo en español.


## Objetivos del demo

- Convertir una serie de tiempo en un problema supervisado con ventanas deslizantes.
- Preparar los datos correctamente (escalado y división temporal, sin barajar).
- Entrenar una LSTM y compararla contra una línea base simple.
- Evaluar con MAE / RMSE / MAPE y visualizar predicciones vs valores reales.
- Discutir overfitting, la curva de pérdida y cómo elegir las épocas (early stopping).


## Dependencias

```bash
pip install numpy pandas matplotlib scikit-learn tensorflow
```

Versiones sugeridas: Python 3.10+, TensorFlow 2.15+. Si no hay GPU, funciona igual (la serie es pequeña).


## Dataset

Usa una serie clásica con **tendencia y estacionalidad** para que el patrón sea visible.
Opción A (recomendada, sin descargar nada): serie sintética reproducible. Opción B: pasajeros de aerolínea.

**Opción A — serie sintética (tendencia + estacionalidad + ruido):**

```python
import numpy as np
import pandas as pd

np.random.seed(42)
n = 300
t = np.arange(n)
tendencia = 0.05 * t
estacionalidad = 10 * np.sin(2 * np.pi * t / 12)   # ciclo de 12 pasos
ruido = np.random.normal(0, 1.5, n)
serie = 50 + tendencia + estacionalidad + ruido
serie = pd.Series(serie, name="valor")
```

**Opción B — AirPassengers (mensual, tendencia + estacionalidad anual):**

```python
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/airline-passengers.csv"
df = pd.read_csv(url)
serie = df["Passengers"].astype(float)
```

Explica en una celda markdown: qué representa la serie, por qué el orden importa y que el objetivo es
pronosticar el siguiente valor a partir de los pasados.


## Estructura del notebook (sección por sección)

### 1. Título y objetivos (markdown)
Portada del notebook con el título, el nombre del curso y una lista corta de lo que se va a hacer.

### 2. Imports (código)

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.callbacks import EarlyStopping
```

### 3. Cargar y explorar la serie (código + markdown)
Grafica la serie completa. Señala a simple vista la tendencia y la estacionalidad.

```python
plt.figure(figsize=(10, 4))
plt.plot(serie.values)
plt.title("Serie de tiempo")
plt.xlabel("Tiempo"); plt.ylabel("Valor")
plt.show()
```

### 4. Escalado (código + markdown)
Las redes son sensibles a la escala. Normaliza a [0, 1]. Importante: el scaler se ajusta **solo con
el tramo de entrenamiento** para no filtrar información del futuro (aquí, por simplicidad del demo,
puedes ajustarlo con toda la serie y mencionar la advertencia; la versión rigurosa se muestra abajo).

```python
scaler = MinMaxScaler()
serie_esc = scaler.fit_transform(serie.values.reshape(-1, 1)).flatten()
```

### 5. Ventanas deslizantes (código + markdown)
Este es el concepto central de la clase: convertir la serie en pares (X, y).

```python
def crear_ventanas(serie, k):
    X, y = [], []
    for i in range(len(serie) - k):
        X.append(serie[i:i+k])   # ventana de k valores pasados
        y.append(serie[i+k])     # el valor siguiente
    return np.array(X), np.array(y)

k = 12                    # tamaño de la ventana (un ciclo estacional)
X, y = crear_ventanas(serie_esc, k)
X = X.reshape((X.shape[0], k, 1))   # (muestras, pasos, variables) para la LSTM
```

Muestra en markdown un ejemplo concreto con k pequeño (p. ej. `[10,12,13] -> 15`) igual que en la clase.

### 6. División temporal (código + markdown)
Nunca uses datos del futuro para entrenar. El conjunto de prueba es el **tramo final** de la serie,
no una muestra aleatoria.

```python
corte = int(len(X) * 0.8)
X_train, X_test = X[:corte], X[corte:]
y_train, y_test = y[:corte], y[corte:]
```

### 7. Línea base (naive) (código + markdown)
Antes de deep learning, una línea base: predecir que el siguiente valor es igual al último conocido.
Sirve para saber si la red realmente aporta.

```python
# la predicción ingenua = último valor de cada ventana
y_pred_naive = X_test[:, -1, 0]
```

### 8. Modelo LSTM (código + markdown)
Construye, compila y entrena. Usa un conjunto de validación y **early stopping** para elegir las épocas.

```python
model = Sequential([
    LSTM(50, activation='tanh', input_shape=(k, 1)),
    Dense(1)
])
model.compile(optimizer='adam', loss='mse')

es = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
hist = model.fit(
    X_train, y_train,
    validation_split=0.2,
    epochs=200,
    batch_size=16,
    callbacks=[es],
    verbose=0
)
```

### 9. Curva de pérdida (código + markdown)
Grafica train vs validation loss. Aquí se **ve** el overfitting y por qué early stopping detiene el
entrenamiento en el punto justo.

```python
plt.figure(figsize=(8, 4))
plt.plot(hist.history['loss'], label='train')
plt.plot(hist.history['val_loss'], label='validation')
plt.title("Pérdida por época"); plt.xlabel("Época"); plt.ylabel("MSE")
plt.legend(); plt.show()
```

### 10. Predicción y des-escalado (código)

```python
y_pred = model.predict(X_test).flatten()

# volver a la escala original para interpretar y graficar
def desescalar(v):
    return scaler.inverse_transform(np.array(v).reshape(-1, 1)).flatten()

y_test_real  = desescalar(y_test)
y_pred_real  = desescalar(y_pred)
y_naive_real = desescalar(y_pred_naive)
```

### 11. Métricas (código + markdown)
Compara la LSTM contra la línea base con MAE, RMSE y MAPE.

```python
def mae(a, b):  return np.mean(np.abs(a - b))
def rmse(a, b): return np.sqrt(np.mean((a - b) ** 2))
def mape(a, b): return np.mean(np.abs((a - b) / a)) * 100

for nombre, pred in [("Naive", y_naive_real), ("LSTM", y_pred_real)]:
    print(f"{nombre:6}  MAE={mae(y_test_real, pred):6.2f}  "
          f"RMSE={rmse(y_test_real, pred):6.2f}  MAPE={mape(y_test_real, pred):5.2f}%")
```

Punto de discusión: ¿la LSTM le gana a la línea base? Si no, quizá la serie es demasiado simple o
faltan datos: exactamente la conversación de "¿cuándo vale la pena deep learning?".

### 12. Visualización: predicción vs real (código + markdown)

```python
plt.figure(figsize=(10, 4))
plt.plot(y_test_real, label='real', marker='.')
plt.plot(y_pred_real, label='LSTM', marker='.')
plt.plot(y_naive_real, label='naive', linestyle='--', alpha=0.6)
plt.title("Pronóstico en el conjunto de prueba")
plt.legend(); plt.show()
```

### 13. Pronóstico multi-paso (opcional, código + markdown)
Predice varios pasos hacia adelante de forma iterativa (usando cada predicción como entrada) y muestra
cómo se **acumula el error**. Refuerza la idea de horizonte de la clase.

```python
def pronostico_iterativo(model, ventana_inicial, pasos):
    ventana = list(ventana_inicial)
    preds = []
    for _ in range(pasos):
        x = np.array(ventana[-k:]).reshape((1, k, 1))
        p = model.predict(x, verbose=0).flatten()[0]
        preds.append(p)
        ventana.append(p)
    return desescalar(preds)

futuro = pronostico_iterativo(model, X_test[0, :, 0], pasos=24)
```

### 14. Cierre y discusión (markdown)
- Escalado + división temporal fueron clave; sin ellos el modelo falla o "hace trampa".
- Early stopping eligió las épocas mirando la validación, no un número fijo.
- Comparar contra una línea base evita venderse humo: DL solo vale si supera lo simple.
- Métodos clásicos (ARIMA, suavizado exponencial) siguen siendo fuertes en series cortas y univariadas.


## Retos para el estudiante (dejar como ejercicios)

1. Cambia el tamaño de ventana `k` (6, 12, 24) y observa el efecto en las métricas.
2. Sustituye la LSTM por una GRU y por un MLP (aplanando la ventana). ¿Cuál gana?
3. Agrega una segunda variable (p. ej. un indicador de mes o feriado) y conviértelo en multivariado.
4. Quita el escalado y vuelve a entrenar: observa cómo se degrada el aprendizaje.
5. Aumenta las épocas y quita el early stopping: identifica el punto donde empieza el overfitting.


## Notas de buenas prácticas para el demo (para el docente)

- Corre el notebook completo antes de clase (fija `np.random.seed` y `tf.random.set_seed`).
- Ten a la mano la versión rigurosa del escalado (ajustar el scaler solo con el train) por si preguntan.
- El objetivo pedagógico no es ganarle a ARIMA, sino **ver el flujo completo** de un modelo de DL para series.
