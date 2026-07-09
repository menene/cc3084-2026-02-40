"""
Etapa 3 del pipeline: TIPADO + LIMPIEZA POR COLUMNA
------------------------------------------------------------
Una sola responsabilidad: convertir cada columna de texto a su tipo correcto
y a su dominio de valores validos.

  Lee : data/processed/02_deduplicado.csv
  Hace: convierte id/fecha/precio/cantidad/calificacion a sus tipos, y
        normaliza los dominios de categoria/metodo_pago/en_oferta/email.
  Escribe: data/processed/03_tipado.csv

Empieza VALIDANDO que la etapa 2 dejo id_venta unico (si no, el resto no
tiene sentido).

Ejecutar:  python src/03_tipado.py
"""
import re

import numpy as np
import pandas as pd

import config
from utils import banner, cargar, guardar, afirmar

# --- Tablas de referencia (dominios validos) ---
FORMATOS_FECHA = ["%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%b %d, %Y"]
CATEGORIAS_VALIDAS = {"Electronica", "Ropa", "Hogar", "Deportes"}
PALABRAS_A_NUMERO = {"uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5}
PATRON_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
# Dominios conocidos: sirven para reparar correos a los que se les cayo la "@"
# (ej. "cliente131gmail.com" -> "cliente131@gmail.com"). El dato SI existe,
# solo esta mal formateado; reponer la "@" es corregir, no inventar.
DOMINIOS_CONOCIDOS = ["gmail.com", "hotmail.com", "uvg.edu.gt"]
MAPA_METODO_PAGO = {
    "tarjeta": "tarjeta", "credit card": "tarjeta",
    "efectivo": "efectivo", "cash": "efectivo",
    "transferencia": "transferencia",
}
MAPA_BOOLEANO = {
    "si": True, "sí": True, "1": True, "true": True,
    "no": False, "0": False, "false": False,
}


def parsear_fecha(valor):
    if pd.isna(valor):
        return pd.NaT
    for formato in FORMATOS_FECHA:
        try:
            return pd.to_datetime(valor, format=formato)
        except ValueError:
            continue
    return pd.NaT


def limpiar_precio(valor):
    if pd.isna(valor):
        return np.nan
    texto = valor.replace("Q", "").replace("$", "").replace(",", "").strip()
    try:
        return abs(float(texto))  # un precio negativo es error de captura
    except ValueError:
        return np.nan


def limpiar_cantidad(valor):
    if pd.isna(valor):
        return np.nan
    valor = valor.lower().strip()
    if valor in PALABRAS_A_NUMERO:
        return PALABRAS_A_NUMERO[valor]
    try:
        return abs(int(float(valor)))
    except ValueError:
        return np.nan


def limpiar_email(valor):
    if pd.isna(valor):
        return np.nan
    valor = valor.strip()
    # Reparacion de formato: si no trae "@" pero termina en un dominio conocido,
    # reponemos la "@" antes del dominio.
    if "@" not in valor:
        for dominio in DOMINIOS_CONOCIDOS:
            if valor.endswith(dominio) and len(valor) > len(dominio):
                valor = valor[:-len(dominio)] + "@" + dominio
                break
    return valor if PATRON_EMAIL.match(valor) else np.nan


def limpiar_calificacion(valor):
    if pd.isna(valor):
        return np.nan
    try:
        num = int(float(valor))
    except ValueError:
        return np.nan
    return num if 1 <= num <= 5 else np.nan


banner("ETAPA 3 | TIPADO + LIMPIEZA POR COLUMNA")

df = cargar(config.RUTA_DEDUP, dtype=str)

# --- Validar el contrato de la etapa anterior (02_deduplicacion) ---
afirmar(not df.duplicated(subset="id_venta").any(),
        "id_venta llega unico desde la etapa 2")

# --- Conversion de tipos y limpieza por columna ---
df["id_venta"] = df["id_venta"].astype(int)
df["fecha"] = df["fecha"].map(parsear_fecha)
df["categoria"] = df["categoria"].str.strip().str.lower().str.capitalize()
df.loc[~df["categoria"].isin(CATEGORIAS_VALIDAS), "categoria"] = np.nan
df["precio_unitario"] = df["precio_unitario"].map(limpiar_precio)
df["cantidad"] = df["cantidad"].map(limpiar_cantidad)
df["cliente_email"] = df["cliente_email"].map(limpiar_email)
df["metodo_pago"] = df["metodo_pago"].str.lower().str.strip().map(MAPA_METODO_PAGO)
df["en_oferta"] = df["en_oferta"].str.lower().str.strip().map(MAPA_BOOLEANO)
df["calificacion"] = df["calificacion"].map(limpiar_calificacion)

print("\nTipos de dato finales:")
print(df.dtypes)
print("\nValores nulos por columna:")
print(df.isna().sum())

# --- Validar la salida de esta etapa (los dominios quedaron limpios) ---
afirmar(pd.api.types.is_integer_dtype(df["id_venta"]),
        "id_venta quedo como entero")
afirmar((df["precio_unitario"].dropna() >= 0).all(),
        "precio_unitario no tiene negativos")
afirmar((df["cantidad"].dropna() >= 0).all(),
        "cantidad no tiene negativos")
afirmar(df["categoria"].dropna().isin(CATEGORIAS_VALIDAS).all(),
        "categoria solo tiene valores del dominio valido")
cal = df["calificacion"].dropna()
afirmar(cal.between(1, 5).all(), "calificacion esta dentro del rango 1-5")

guardar(df, config.RUTA_TIPADO)
