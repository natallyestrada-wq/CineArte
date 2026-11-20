### PREPARACIÓN DEL ENTORNO
import streamlit as st
import pandas as pd

from src.data import cargar_pelis, URL_POSTER
from src.traduccion import traducir_texto, traducir_genero, traducir_idioma


### CARGA DE DATOS
pelis = cargar_pelis()


### INICIALIZACIÓN DE VARIABLES DE SESIÓN
for lista in ["pelis_ver", "pelis_vistas", "pelis_jugadas"]:
    if lista not in st.session_state:
        st.session_state[lista] = []

# ids_mi_cine = set(
#     st.session_state["pelis_vistas"]
#     + st.session_state["pelis_ver"]
#     + st.session_state["pelis_jugadas"]
# )

### CONFIGURACIÓN DE CATEGORÍAS
CATEGORIAS = {
    "Vista": "pelis_vistas",
    "Por ver": "pelis_ver",
    "Jugada": "pelis_jugadas"
}


### FUNCIONES AUXILIARES

def mostrar_valor(valor):
    """Controla los valores vacíos del DataFrame."""

    if pd.isna(valor):
        return "No disponible"

    return str(valor)


def obtener_pelis_usuario():
    """Obtiene las películas pertenecientes a las listas del usuario."""

    ids_usuario = set()

    for lista in CATEGORIAS.values():
        ids_usuario.update(
            str(id_peli) for id_peli in st.session_state[lista]
        )

    if not ids_usuario:
        return pelis.iloc[0:0].copy()

    resultado = pelis[
        pelis["id"].astype(str).isin(ids_usuario)
    ].copy()

    # Evitar películas duplicadas
    resultado = resultado.drop_duplicates(subset="id")

    # Crear columnas booleanas
    for categoria, lista in CATEGORIAS.items():

        ids_lista = {
            str(id_peli)
            for id_peli in st.session_state[lista]
        }

        resultado[categoria] = (
            resultado["id"].astype(str).isin(ids_lista)
        )

    return resultado.reset_index(drop=True)


def eliminar_pelicula(id_peli, lista):
    """Elimina una película de una categoría específica."""

    st.session_state[lista] = [
        id_actual
        for id_actual in st.session_state[lista]
        if str(id_actual) != str(id_peli)
    ]

    st.rerun()


### ESTRUCTURA VISUAL DE LA PÁGINA

st.title("🍿 Mi Cine")

## TABLA DE PELÍCULAS
# ------------------------------------------------------------------------------

pelis_usuario = obtener_pelis_usuario()

if pelis_usuario.empty:

    st.info("Todavía no tienes películas en Mi Cine.")

else:

    st.subheader(f"{len(pelis_usuario):,} películas en tu colección")

    nombres_columnas = {
        "id": "id",
        "title": "🎬 Película",
        "release_date": "📅 Lanzamiento",
        "runtime": "⌛ Duración",
        "averageRating": "⭐ Rating",
        "genres": "🎭 Géneros",
        "Vista": "👁️ Vista",
        "Por ver": "📌 Por ver",
        "Jugada": "🎲 Jugada"
    }

    tabla_mostrar = (
        pelis_usuario[list(nombres_columnas.keys())]
        .rename(columns=nombres_columnas)
    )

    eventos_tabla = st.dataframe(
        tabla_mostrar,
        width="stretch",
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            "id": None
        }
    )


    ## DETALLES DE LA PELÍCULA SELECCIONADA
    # --------------------------------------------------------------------------

    if eventos_tabla.selection.rows:

        indice = eventos_tabla.selection.rows[0]
        peli = pelis_usuario.iloc[indice]

        st.divider()
        st.info("🍿 Esta es la película seleccionada:")

        col_izq, col_der = st.columns([1, 2])

        with col_izq:

            poster = peli["poster_path"]

            if pd.notna(poster) and str(poster).strip():

                st.image(
                    URL_POSTER + str(poster),
                    width="stretch"
                )

            else:
                st.info("Póster no disponible.")

        with col_der:

            st.subheader(mostrar_valor(peli["title"]))

            tagline = peli["tagline"]

            if pd.notna(tagline) and str(tagline).strip():
                st.caption(traducir_texto(tagline))

            st.write(traducir_texto(mostrar_valor(peli["overview"])))

            # Información general
            fecha = peli["release_date"]

            anho = (
                str(fecha)[:4]
                if pd.notna(fecha)
                else "No disponible"
            )

            duracion = mostrar_valor(peli["runtime"])

            rating = mostrar_valor(peli["averageRating"])

            idioma = traducir_idioma(
                mostrar_valor(peli["original_language"])
            )

            generos = traducir_genero(
                mostrar_valor(peli["genres"])
            )

            directores = mostrar_valor(peli["directors"])
            guionistas = mostrar_valor(peli["writers"])

            st.markdown(
                f"""
                |||
                | :--- | :--- |
                | 📅 Lanzamiento: {anho} | ⌛ {duracion} minutos |
                | ⭐ Rating: {rating} | 🗣️ {idioma} |
                | 🎭 Géneros: {generos} | |
                | 👤 Directores: {directores} | |
                | ✍️ Guionistas: {guionistas} | |
                """
            )

            st.caption(
                f"**Reparto:** {mostrar_valor(peli['cast'])}"
            )

            st.caption(
                f"**Palabras clave:** {mostrar_valor(peli['keywords'])}"
            )


        ## BOTONES PARA ELIMINAR DE CADA CATEGORÍA
        # ----------------------------------------------------------------------

        st.write("**Administrar película:**")

        id_peli = peli["id"]

        botones = st.columns(3)

        for col, (categoria, lista) in zip(
            botones,
            CATEGORIAS.items()
        ):

            if id_peli in st.session_state[lista]:

                with col:

                    if st.button(
                        f"🗑️ Quitar de {categoria}",
                        key=f"quitar_{lista}_{id_peli}",
                        width="stretch"
                    ):

                        eliminar_pelicula(id_peli, lista)

    else:

        st.info("👆 Selecciona una película de la tabla para ver sus detalles.")



