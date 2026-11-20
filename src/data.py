import pandas as pd
import streamlit as st
from pathlib import Path

RAIZ = Path(__file__).parent.parent
RUTA_MOVIES = RAIZ / "data" / "movies.csv"
URL_POSTER = "https://image.tmdb.org/t/p/w500"

## FUCIÓN PARA LEER LA BASE DE DATOS Y CARGARLA A UN DATAFRAME
@st.cache_data  # decorador para almacenar en caché los resultados de la función
def cargar_pelis():
    """Función para cargar las películas desde un archivo CSV."""

    if not RUTA_MOVIES.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {RUTA_MOVIES}")

    return pd.read_csv(RUTA_MOVIES)

## FUNCIÓN PARA FILTRAR EL DATAFRAME
def filtrar_peliculas(
    df,
    titulo=None,

    generos=None,
    directores=None,
    actores=None,

    duracion_min=None,
    duracion_max=None,
    mejor_rating = False,
    desconocidas = False,
    excluir_adultos=False
):
    """
    Filtra películas según criterios de búsqueda y preferencias del usuario.

    Parámetros:
        df: DataFrame de películas.
        titulo: str, título de la película.
        generos: list, géneros a buscar.
        directores: str, directores a buscar.
        actores: str, actores a buscar.

        duracion_min: int, float, duración mínima en minutos.
        duracion_max: int, float, duración máxima en minutos.

        mejor_rating: bool, quitar o no las películas con bajo rating.
        desconocidas: bool, quitar o no las películas populares.
        excluir_adultos: bool, Excluir películas para adultos.
    """
    resultado = df.copy()

    # Filtros de textos
    filtros_texto = {
        "title": titulo,
        "directors": directores,
        "cast": actores
    }

    for columna, valor in filtros_texto.items():

        if valor is not None and valor.strip():
            resultado = resultado[
                resultado[columna].str.contains(
                    valor.strip(),
                    case=False,
                    regex=False
                )
            ]
        # .str.contains(...): comprueba si cada texto contiene lo que escribió el usuario.
        # value.strip(): busca el texto sin espacios sobrantes.
        # case=False: ignora mayúsculas y minúsculas.
        # regex=False: interpreta el texto como una búsqueda literal, no como una expresión regular.

    # Filtro de géneros (lista)
    if generos:

        mascara_generos = pd.Series( # Crear serie con todas las columnas en falso y 
            False,                   # el mismo índice que el df de entrada
            index=resultado.index
        )

        for genero in generos:

            coincidencias = resultado["genres"].str.contains(
                genero,
                case=False,
                regex=False
            )
            # Crea una serie con el mismo índice del df de entrada y con un una columna 
            # booleana que indica verdadero donde encuentre una coincidencia de texto

            # .str.contains(...): comprueba si cada texto contiene lo que escribió el usuario.
            # case=False: ignora mayúsculas y minúsculas.
            # regex=False: interpreta el texto como una búsqueda literal, no como una expresión regular.

            mascara_generos = mascara_generos | coincidencias # Realiza una intersección entre los
                            # valores de ambas series, conservando los positivos (true)
                            # el símbolo | corresponde a la ó inclusiva
            

        resultado = resultado[mascara_generos]

    # Filtros de duración
    if duracion_min is not None:
        resultado = resultado[
            resultado["runtime"] >= duracion_min
        ]

    if duracion_max is not None:
        resultado = resultado[
            resultado["runtime"] <= duracion_max
        ]
    
    # Quitar las películas con bajo rating
    if mejor_rating is not None:
            resultado = resultado[
                resultado["averageRating"] >= 8.0
            ]
    
    # Quitar las películas populares
    if desconocidas:
            resultado = resultado[
                resultado["popularity"] < 40.0
            ]
    
    # Excluir películas para adultos
    if excluir_adultos:
        resultado = resultado[
            ~resultado["adult"] # el símbolo ~ corresponde a la negación
        ]

    return resultado
