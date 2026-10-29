# Preparación del entorno
import streamlit as st
from src.data import cargar_pelis

# CARGA DE DATOS
pelis = cargar_pelis()  # Cargar las películas desde el archivo CSV
pelis_filtradas = (
    pelis.copy()
)  # Crear una copia del DataFrame original para aplicar los filtros

# Inicializar variables de sesión para almacenar datos de uso de la aplicación
if "pelis_ver" not in st.session_state:
    st.session_state["pelis_ver"] = []

if "pelis_vistas" not in st.session_state:
    st.session_state["pelis_vistas"] = []


# ESTRUCTURA VISUAL DE LA PÁGINA
st.header("🔍 Explorar")

# Filtros de búsqueda
titulo_buscar = st.text_input(
    "Buscar por título:", placeholder="Ingrese el título de la película"
)

col1, col2, col3 = st.columns(3)
with col1:
    search_genre = st.text_input(
        "🎭 Género",
        placeholder="Ej. Drama",
    )

with col2:
    search_director = st.text_input(
        "🎬 Directores",
        placeholder="Ej. Christopher Nolan",
    )

with col3:
    search_cast = st.text_input(
        "👥 Reparto",
        placeholder="Ej. Tom Hanks",
    )


filtros = {  # filtros
    "title": titulo_buscar,
    "genres": search_genre,
    "directors": search_director,
    "cast": search_cast,
}

for column, value in filtros.items():
    if value.strip():
        pelis_filtradas = pelis_filtradas[
            pelis_filtradas[column]
            .fillna("")
            .str.contains(
                value.strip(),
                case=False,
                regex=False,
            )
        ]

# pelis_filtradas[column]: selecciona la columna que se quiere buscar, por ejemplo, title.
# .fillna(""): reemplaza los valores faltantes por texto vacío para evitar problemas.
# .str.contains(...): comprueba si cada texto contiene lo que escribió el usuario.
# value.strip(): busca el texto sin espacios sobrantes.
# case=False: ignora mayúsculas y minúsculas.
# regex=False: interpreta el texto como una búsqueda literal, no como una expresión regular.
# pelis_filtradas[...]: conserva las filas donde la condición es verdadera.

st.divider()
st.subheader(f"Resultados de la búsqueda: {len(pelis_filtradas)} películas encontradas")

st.dataframe(pelis_filtradas[["title", "genres", "directors", "cast"]])

max_results = st.selectbox(
    "Películas mostradas",
    options=[50, 100, 200],
    index=1,
)

# table_movies = pelis_filtradas.head(max_results)
