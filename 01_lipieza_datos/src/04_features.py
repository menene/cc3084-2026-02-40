"""
Etapa 4 del pipeline: FEATURES + DATASET FINAL
------------------------------------------------------------
Una sola responsabilidad: enriquecer el dataset ya limpio con columnas
derivadas y dejarlo listo para analisis.

  Lee : data/processed/03_tipado.csv
  Hace: - calcula total_venta = precio_unitario * cantidad
        - ordena por id_venta
  Escribe: data/processed/ventas_limpio.csv   (dataset final, ver codebook.md)

Empieza VALIDANDO que la etapa 3 dejo las columnas numericas con tipos
usables (si precio o cantidad fueran texto, el calculo saldria mal).

Ejecutar:  python src/04_features.py
"""
import pandas as pd

import config
from utils import banner, cargar, guardar, afirmar


banner("ETAPA 4 | FEATURES + DATASET FINAL")

# parse_dates: recuperamos fecha como datetime (el CSV la guardo como texto).
df = cargar(config.RUTA_TIPADO, parse_dates=["fecha"])

# --- Validar el contrato de la etapa anterior (03_tipado) ---
afirmar(pd.api.types.is_numeric_dtype(df["precio_unitario"]),
        "precio_unitario llega como numero")
afirmar(pd.api.types.is_numeric_dtype(df["cantidad"]),
        "cantidad llega como numero")

# --- Unica transformacion de esta etapa: feature engineering ---
df["total_venta"] = (df["precio_unitario"] * df["cantidad"]).round(2)
df = df.sort_values("id_venta").reset_index(drop=True)

print(f"\nDataset final: {df.shape[0]} filas, {df.shape[1]} columnas")
print("\nTipos de dato finales:")
print(df.dtypes)

# --- Validar la salida final ---
calculables = df["precio_unitario"].notna() & df["cantidad"].notna()
esperado = (df.loc[calculables, "precio_unitario"] * df.loc[calculables, "cantidad"]).round(2)
afirmar((df.loc[calculables, "total_venta"] == esperado).all(),
        "total_venta = precio_unitario * cantidad en todas las filas calculables")

guardar(df, config.RUTA_FINAL)
print(f"\nDataset limpio final: {config.RUTA_FINAL}")
