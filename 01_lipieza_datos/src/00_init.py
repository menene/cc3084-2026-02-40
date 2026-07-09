"""
Etapa 0 del pipeline: SETUP DEL ENTORNO
------------------------------------------------------------
Una sola responsabilidad: dejar listo el entorno para correr el pipeline.

  Hace: - crea un entorno virtual en .venv (si no existe)
        - instala las dependencias de requirements.txt dentro de ese venv

Se corre con el python del sistema (no necesita nada instalado todavia):

    python src/00_init.py

Al terminar, activa el venv y ya puedes correr los scripts con `python`:
    source .venv/bin/activate    (macOS / Linux)   ->  python src/run_pipeline.py
    .venv\\Scripts\\activate       (Windows)          ->  python src\\run_pipeline.py
"""
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR_VENV = RAIZ / ".venv"
REQUIREMENTS = RAIZ / "requirements.txt"

# El ejecutable de python dentro del venv cambia segun el sistema operativo.
if sys.platform == "win32":
    PYTHON_VENV = DIR_VENV / "Scripts" / "python.exe"
else:
    PYTHON_VENV = DIR_VENV / "bin" / "python"

print("=" * 60)
print("ETAPA 0 | SETUP DEL ENTORNO")
print("=" * 60)

# --- Crear el venv (si no existe) ---
if PYTHON_VENV.exists():
    print(f"[ok]       ya existe un venv en {DIR_VENV}")
else:
    print(f"[creando]  entorno virtual en {DIR_VENV} ...")
    subprocess.run([sys.executable, "-m", "venv", str(DIR_VENV)], check=True)
    print("[ok]       venv creado")

# --- Instalar dependencias dentro del venv ---
print(f"[instalando] dependencias de {REQUIREMENTS.name} ...")
subprocess.run([str(PYTHON_VENV), "-m", "pip", "install", "--upgrade", "pip"], check=True)
subprocess.run([str(PYTHON_VENV), "-m", "pip", "install", "-r", str(REQUIREMENTS)], check=True)
print("[ok]       dependencias instaladas")

print("\nListo. Activa el venv y corre el pipeline:")
if sys.platform == "win32":
    print("    .venv\\Scripts\\activate")
else:
    print("    source .venv/bin/activate")
print("    python src/run_pipeline.py")
