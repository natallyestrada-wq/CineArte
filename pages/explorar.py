### PREPARACIÓN DEL ENTORNO
import streamlit as st
import plotly.express as px
import pandas as pd

from src.data import cargar_pelis
from src.traduccion import traducir_texto, traducir_genero, traducir_idioma
import src.figuras as fig

### CARGA DE DATOS
# st.cache_data.clear() # forzar recarga de datos para que actualice el dataframe si se cambia el archivo CSV
pelis = cargar_pelis()  # Cargar las películas desde el archivo CSV

### INICIALIZACIÓN DE VARIABLES DE SESIÓN
if (
    "pelis_ver" not in st.session_state
):  # para guardar las películas que el usuario quiere ver
    st.session_state["pelis_ver"] = []

if (
    "pelis_vistas" not in st.session_state
):  # para guardar las películas que el usuario ya vió
    st.session_state["pelis_vistas"] = []


### ESTRUCTURA VISUAL DE LA PÁGINA
st.header("🔍 Explorar")

## FILTROS DE BÚSQUEDA
# ------------------------------------------------------------------------------
titulo_buscar = st.text_input(
    "Buscar por título:", placeholder="Escribe el título de la película..."
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


filtros = {  # filtros necesarios para aplicar al dataframe
    "title": titulo_buscar,
    "genres": search_genre,
    "directors": search_director,
    "cast": search_cast,
}

pelis_filtradas = (
    pelis.copy()
)  # copia del DataFrame original para aplicarle los filtros

for column, value in filtros.items():  # filtrado
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

# PRESENTACIÓN DE RESULTADOS EN TABLA FILTRADA
# ------------------------------------------------------------------------------
st.divider()
st.subheader(f"{len(pelis_filtradas):,} películas encontradas")

opciones = {  # opciones de cantidad de resultados a mostrar
    "10 películas": 10,
    "50 películas": 50,
    "100 películas": 100,
    "200 películas": 200,
}

seleccion = st.selectbox(  # botón de selección de cantidad de resultados a mostrar
    "Mostrando las primeras...",  # Aquí va la etiqueta del selectbox
    options=list(opciones.keys()),  # aquí van las opciones del selectbox
    help="Selecciona la cantidad de resultados a mostrar",
    index=1,  # indica la opción que se muestra por defecto
)

# 1
# st.dataframe(pelis_filtradas)

# 2
# st.dataframe(
#     pelis_filtradas[
#         ["title", "release_date", "averageRating", "genres", "directors", "cast"]
#     ]
# )

# 3
# cant_pelis_mostrar = opciones[seleccion]  # se identifica el entero de pelis a mostrar
# st.dataframe(
#     pelis_filtradas[
#         ["title", "release_date", "averageRating", "genres", "directors", "cast"]
#     ].head(cant_pelis_mostrar)
# )

# 4
cant_pelis_mostrar = opciones[seleccion]  # se identifica el entero de pelis a mostrar
nombres_columnas = {
    "id": "id",
    "title": "🎬 Película",
    "release_date": "📅 Lanzamiento",
    "averageRating": "⭐ Rating",
    "genres": "🎭 Géneros",
    "directors": "👤 Directores",
    "cast": "👥 Reparto",
}

tabla_mostrar = (
    pelis_filtradas[nombres_columnas.keys()]
    .head(cant_pelis_mostrar)
    .rename(columns=nombres_columnas)
)

# 4444
# st.dataframe(
#     tabla_mostrar,
#     hide_index=True,
#     on_select="rerun",  # Controla qué sucede cuando el usuario selecciona una fila
#     selection_mode="single-row",  # Para seleccionar una sola fila a la vez)
# )

eventos_tabla = st.dataframe(
    tabla_mostrar,
    width="stretch",
    hide_index=True,
    on_select="rerun",  # Controla qué sucede cuando el usuario selecciona una fila
    selection_mode="single-row",  # Para seleccionar una sola fila a la vez)
    column_config={"id": None},  # Oculta la columna "id" de la tabla
)


## PRESENTACIÓN DE DETALLES DE LA PELÍCULA SELECCIONADA
# ------------------------------------------------------------------------------

if eventos_tabla.selection.rows:  # si el usuario selecciona una fila
    st.info("🍿 Ésta es la peli que escogiste:")

    # 1
    # st.write(eventos_tabla.selection.rows)

    # 2
    # st.write(tabla_mostrar.iloc[eventos_tabla.selection.rows[0]])

    # 3
    # peli = pelis_filtradas.iloc[eventos_tabla.selection.rows[0]]
    # st.write(peli)

    # 4
    peli = pelis_filtradas.iloc[eventos_tabla.selection.rows[0]]

    col_izq, col_der = st.columns([1, 2])
    with col_izq:
        poster_url = f"https://image.tmdb.org/t/p/w500{peli['poster_path']}"
        st.image(poster_url, use_container_width=True)

    with col_der:
        st.subheader(peli["title"])
        if not type(peli["tagline"]) == float:  # si no es vacío
            st.caption(traducir_texto(peli["tagline"]))
        st.write(traducir_texto(peli["overview"]))

        anho = f"📅 Lanzamiento: {peli['release_date'][0:4]}"
        duracion_idioma = f"⌛ {peli['runtime']} minutos 🗣️ {traducir_idioma(peli['original_language'])}"

        rating = f"⭐ Rating: {peli['averageRating']}"
        generos = f"🎭 Géneros: {traducir_genero(peli['genres'])}"
        directores = f"👤Directores: {peli['directors']}"
        guionistas = f"👥Guionistas: {peli['writers']}"

        st.markdown(
            f"""
            |||
            | :--- | :--- | 
            | {anho} | {duracion_idioma} |
            | {rating} | {generos} | 
            | {directores} | {guionistas} | 
            """,
        )

        st.caption(f"**Reparto:** {peli['cast']}")

        id_peli = peli["id"]

        # 1
        # if id_peli in st.session_state["pelis_ver"]:
        #     st.warning("Esta película ya está en tu lista de 'Películas para ver'.")
        # if id_peli in st.session_state["pelis_vistas"]:
        #     st.warning("Esta película ya está en tu lista de 'Películas vistas'.")

        # 2
        boton_1, boton_2 = st.columns(2)
        with boton_1:
            if id_peli in st.session_state["pelis_ver"]:
                st.success("💾 Guardada en tu lista para ver")
            elif st.button("💾 Guardar para ver", use_container_width=True):
                st.session_state["pelis_ver"].append(id_peli)
                st.rerun()

        with boton_2:
            if id_peli in st.session_state["pelis_vistas"]:
                st.success("✅ Marcada como vista")
            elif st.button("✅ Ya la vi", use_container_width=True):
                st.session_state["pelis_vistas"].append(id_peli)
                st.rerun()
else:
    st.info("👆 Selecciona una película para ver más detalles.")


## VISUALIZACIÓN DE GRÁFICOS DEL DATAFRAME
# Se presentan gráficos sólo si hay más de 10 películas en el DataFrame filtrado
# ------------------------------------------------------------------------------
if pelis_filtradas.shape[0] > 10:
    st.divider()
    st.subheader(f"Estadísticas")

    # -------- Resumen de los filtros aplicados --------
    filtros_activos = []

    if titulo_buscar.strip():
        filtros_activos.append(f"Título: {titulo_buscar.strip()}")

    if search_genre.strip():
        filtros_activos.append(f"Género: {search_genre.strip()}")

    if search_director.strip():
        filtros_activos.append(f"Director: {search_director.strip()}")

    if search_cast.strip():
        filtros_activos.append(f"Reparto: {search_cast.strip()}")

    if filtros_activos:
        st.info("**Filtros |** " + " | ".join(filtros_activos))
    else:
        st.info("No hay filtros aplicados. Mostrando todas las películas.")

    # -------- Gráficos --------
    st.plotly_chart(fig.top_10_rating(pelis_filtradas))

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        st.plotly_chart(fig.pelis_por_genero(pelis_filtradas))

    with col2:
        st.plotly_chart(fig.distribucion_de_anhos(pelis_filtradas))
    with col3:
        st.plotly_chart(
            fig.popularidad_por_rating(pelis_filtradas, limite_popularidad=200)
        )
    with col4:
        st.plotly_chart(fig.pelis_por_idioma(pelis_filtradas))
