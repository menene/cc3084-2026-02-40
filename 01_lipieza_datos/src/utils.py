"""
Utilidades compartidas por todas las etapas del pipeline.

La idea es que cada etapa (01, 02, 03, 04) se lea igual: carga -> valida ->
transforma -> valida -> guarda. Estas funciones evitan repetir el mismo
codigo de I/O y de validacion en cada archivo.
"""
import sys
import pandas as pd


def banner(titulo):
    """Imprime un titulo destacado para separar visualmente cada etapa."""
    print("=" * 60)
    print(titulo)
    print("=" * 60)


def cargar(ruta, **kwargs):
    """Carga un CSV informando de donde viene."""
    df = pd.read_csv(ruta, **kwargs)
    print(f"[cargado]  {ruta.name:24s} -> {df.shape[0]} filas, {df.shape[1]} columnas")
    return df


def guardar(df, ruta):
    """Guarda un CSV informando a donde va."""
    ruta.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(ruta, index=False)
    print(f"[guardado] {ruta.name:24s} <- {df.shape[0]} filas, {df.shape[1]} columnas")


def afirmar(condicion, mensaje):
    """
    Validacion tipo 'assert' pero que detiene el pipeline con codigo de error.

    Si una etapa recibe datos que no cumplen el contrato de la etapa anterior,
    preferimos FALLAR AQUI (con un mensaje claro) antes que arrastrar datos
    malos hasta el dataset final.
    """
    if condicion:
        print(f"[ok]       {mensaje}")
    else:
        print(f"[FALLO]    {mensaje}")
        sys.exit(1)
