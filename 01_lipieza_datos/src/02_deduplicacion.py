"""
Etapa 2 del pipeline: DEDUPLICACION
------------------------------------------------------------
Una sola responsabilidad: garantizar que cada venta aparezca una sola vez.

  Lee : data/processed/01_ingesta.csv
  Hace: - elimina filas duplicadas exactas
        - garantiza que id_venta sea unico (conserva la primera ocurrencia)
  Escribe: data/processed/02_deduplicado.csv

Empieza VALIDANDO el trabajo de la etapa anterior: si los nulos no fueron
normalizados, no seguimos. Asi cada etapa confia en un contrato claro.

Ejecutar:  python src/02_deduplicacion.py
"""
import config
from utils import banner, cargar, guardar, afirmar

MARCADORES_NULOS = {"NA", "N/A", "null", "NULL", "-", "?", "n/a"}


banner("ETAPA 2 | DEDUPLICACION")

df = cargar(config.RUTA_INGESTA, dtype=str)

# --- Validar el contrato de la etapa anterior (01_ingesta) ---
afirmar(list(df.columns) == config.COLUMNAS_CRUDAS,
        "el dataset trae las columnas esperadas")
afirmar(not df.isin(MARCADORES_NULOS).any().any(),
        "los nulos ya vienen normalizados desde la etapa 1")
afirmar(df["id_venta"].notna().all(),
        "ninguna fila viene sin id_venta")

# --- Unica transformacion de esta etapa ---
filas_antes = len(df)
df = df.drop_duplicates()
print(f"\nFilas duplicadas exactas eliminadas: {filas_antes - len(df)}")

duplicados_id = df[df.duplicated(subset="id_venta", keep=False)]
if not duplicados_id.empty:
    print(f"Advertencia: {duplicados_id['id_venta'].nunique()} id_venta con "
          f"registros distintos. Se conserva el primero.")
    print(duplicados_id.sort_values("id_venta")[["id_venta", "fecha", "producto"]])
df = df.drop_duplicates(subset="id_venta", keep="first")

# --- Validar la salida de esta etapa ---
afirmar(not df.duplicated(subset="id_venta").any(),
        "id_venta es unico despues de deduplicar")

guardar(df, config.RUTA_DEDUP)
