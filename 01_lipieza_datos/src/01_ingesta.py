"""
Etapa 1 del pipeline: INGESTA + NORMALIZACION DE NULOS
------------------------------------------------------------
Una sola responsabilidad: traer el crudo a un estado textual uniforme.

  Lee : data/raw/ventas.csv           (crudo, nunca se modifica)
  Hace: - carga todo como texto (no inferir tipos todavia)
        - unifica los muchos "no hay dato" a un unico NaN
  Escribe: data/processed/01_ingesta.csv

Todavia NO convierte tipos ni quita duplicados: eso es trabajo de las
etapas siguientes. Aqui solo dejamos los datos "parejos" para poder trabajarlos.

Ejecutar:  python src/01_ingesta.py
"""
import numpy as np
import pandas as pd

import config
from utils import banner, cargar, guardar, afirmar

MARCADORES_NULOS = {"", "NA", "N/A", "null", "NULL", "-", "?", "n/a"}

def normalizar_texto(valor):
    """Quita espacios y convierte cualquier marcador de nulo en NaN."""
    if pd.isna(valor):
        return np.nan
    valor = valor.strip()
    if valor in MARCADORES_NULOS:
        return np.nan
    return valor


banner("ETAPA 1 | INGESTA + NORMALIZACION DE NULOS")

# dtype=str: no dejamos que pandas infiera tipos todavia, para no perder
# el "antes" (ej. "dos", "Q151.27", "01/05/2023" deben llegar tal cual).
df = cargar(config.RUTA_CRUDA, dtype=str)

# --- Validar el contrato de entrada del pipeline ---
afirmar(
    list(df.columns) == config.COLUMNAS_CRUDAS,
    "el crudo trae exactamente las columnas esperadas",
)

nulos_antes = df.isna().sum().sum()

# --- Unica transformacion de esta etapa ---
for col in df.columns:
    df[col] = df[col].map(normalizar_texto)

nulos_despues = df.isna().sum().sum()
print(f"\nNulos reconocidos por pandas: {nulos_antes} -> {nulos_despues} "
      f"(+{nulos_despues - nulos_antes} marcadores de texto convertidos a NaN)")

# --- Validar la salida de esta etapa ---
# Ningun marcador de nulo debe sobrevivir como texto.
quedan_marcadores = df.isin(MARCADORES_NULOS - {""}).any().any()
afirmar(not quedan_marcadores, "no quedan marcadores de nulo escritos como texto")

guardar(df, config.RUTA_INGESTA)
