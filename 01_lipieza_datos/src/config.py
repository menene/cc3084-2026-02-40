"""
Configuracion compartida del pipeline de limpieza.

Aqui viven las rutas de cada etapa y el "contrato" del dataset (que columnas
deben existir). Tener esto en un solo lugar evita que cada script invente sus
propias rutas y que se desincronicen entre etapas.
"""
from pathlib import Path

# Raiz del proyecto (dos niveles arriba de este archivo: src/ -> raiz)
RAIZ = Path(__file__).resolve().parent.parent
DIR_RAW = RAIZ / "data" / "raw"
DIR_PROCESSED = RAIZ / "data" / "processed"

# ------------------------------------------------------------------
# Rutas de cada etapa del pipeline.
# Cada etapa LEE la salida de la anterior y ESCRIBE su propia salida,
# dejando un rastro auditable de como fueron cambiando los datos.
# ------------------------------------------------------------------
RUTA_CRUDA   = DIR_RAW / "ventas.csv"          # entrada, nunca se modifica
RUTA_INGESTA = DIR_PROCESSED / "01_ingesta.csv"     # <- 01_ingesta.py
RUTA_DEDUP   = DIR_PROCESSED / "02_deduplicado.csv"  # <- 02_deduplicacion.py
RUTA_TIPADO  = DIR_PROCESSED / "03_tipado.csv"       # <- 03_tipado.py
RUTA_FINAL   = DIR_PROCESSED / "ventas_limpio.csv"   # <- 04_features.py (dataset final)

# Columnas que deben venir en el crudo (contrato de entrada del pipeline).
COLUMNAS_CRUDAS = [
    "id_venta", "fecha", "producto", "categoria", "precio_unitario",
    "cantidad", "cliente_email", "metodo_pago", "en_oferta", "calificacion",
]
