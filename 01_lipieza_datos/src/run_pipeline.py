"""
Orquestador del pipeline de limpieza.
------------------------------------------------------------
Corre las 4 etapas en orden. Cada etapa es un script independiente que se
puede correr solo; este archivo solo las encadena para reproducir todo el
proceso de una vez.

Si una etapa falla su validacion, se detiene con codigo de error y NO sigue
con las siguientes (fail-fast): asi nunca se genera un dataset final a partir
de datos que no pasaron los controles.

Ejecutar:  python src/run_pipeline.py
"""
import subprocess
import sys
from pathlib import Path

DIR_SRC = Path(__file__).resolve().parent

ETAPAS = [
    "01_ingesta.py",
    "02_deduplicacion.py",
    "03_tipado.py",
    "04_features.py",
]

for etapa in ETAPAS:
    print("\n" + "#" * 60, flush=True)
    print(f"# EJECUTANDO {etapa}", flush=True)
    print("#" * 60, flush=True)
    resultado = subprocess.run([sys.executable, str(DIR_SRC / etapa)])
    if resultado.returncode != 0:
        print(f"\n>>> El pipeline se detuvo en {etapa} (fallo una validacion).")
        sys.exit(resultado.returncode)

print("\n" + "#" * 60)
print("# PIPELINE COMPLETO: dataset final en data/processed/ventas_limpio.csv")
print("#" * 60)
