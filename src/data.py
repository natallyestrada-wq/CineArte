import pandas as pd
import streamlit as st
from pathlib import Path

RAIZ = Path(__file__).parent.parent
RUTA_MOVIES = RAIZ / "data" / "movies.csv"


@st.cache_data  # decorador para almacenar en caché los resultados de la función
def cargar_pelis():
    """Función para cargar las películas desde un archivo CSV."""

    if not RUTA_MOVIES.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {RUTA_MOVIES}")

    return pd.read_csv(RUTA_MOVIES)
