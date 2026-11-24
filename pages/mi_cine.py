### PREPARACIÓN DEL ENTORNO
import streamlit as st
import pandas as pd

from src.data import cargar_pelis, inicializar_sesion
from src.traduccion import traducir_texto, traducir_genero, traducir_idioma
from src.config import URL_POSTER

### CARGA DE DATOS
pelis = cargar_pelis()

### INICIALIZACIÓN DE VARIABLES DE SESIÓN
inicializar_sesion()

if "peli_seleccionada" not in st.session_state:
    st.session_state["peli_seleccionada"] = None

if "version_tabla" not in st.session_state:
    st.session_state["version_tabla"] = 0


### CONFIGURACIÓN DE CATEGORÍAS
CATEGORIAS = {
    "Vista": "pelis_vistas",
    "Por ver": "pelis_ver",
    "Jugada": "pelis_jugadas",
}


### FUNCIONES AUXILIARES
def mostrar_valor(valor):
    """Controla los valores vacíos del DataFrame."""
    if pd.isna(valor) or valor is None or str(valor).strip() == "":
        return "No disponible"
    return str(valor)


def obtener_pelis_usuario():
    """Obtiene las películas pertenecientes a las listas del usuario."""
    ids_usuario = set()
    for lista in CATEGORIAS.values():
        ids_usuario.update(str(id_peli) for id_peli in st.session_state[lista])

    if not ids_usuario:
        return pelis.iloc[0:0].copy()

    resultado = pelis[pelis["id"].astype(str).isin(ids_usuario)].copy()
    resultado = resultado.drop_duplicates(subset="id")

    for categoria, lista in CATEGORIAS.items():
        ids_lista = {str(id_peli) for id_peli in st.session_state[lista]}
        resultado[categoria] = resultado["id"].astype(str).isin(ids_lista)

    return resultado.reset_index(drop=True)


def agregar_pelicula(id_peli, lista):
    """Agrega una película evitando duplicados."""
    ids_existentes = {str(x) for x in st.session_state[lista]}
    if str(id_peli) not in ids_existentes:
        st.session_state[lista].append(int(id_peli))


def eliminar_pelicula(id_peli, lista):
    """Elimina una película de una categoría específica."""
    st.session_state[lista] = [
        x for x in st.session_state[lista] if str(x) != str(id_peli)
    ]


# --- Callbacks de los botones ---
def accion_quitar(id_peli, lista):
    eliminar_pelicula(id_peli, lista)
    # Reinicia la selección visual de la tabla para que no arrastre el índice anterior
    st.session_state["version_tabla"] += 1


def accion_cambiar_estado(id_peli, nuevo_estado):
    """Cambia entre Vista y Por ver (mutuamente excluyentes) manteniendo la selección."""
    if nuevo_estado == "vista":
        eliminar_pelicula(id_peli, "pelis_ver")
        agregar_pelicula(id_peli, "pelis_vistas")
    elif nuevo_estado == "por_ver":
        eliminar_pelicula(id_peli, "pelis_vistas")
        agregar_pelicula(id_peli, "pelis_ver")

    st.session_state["peli_seleccionada"] = str(id_peli)
    st.session_state["version_tabla"] += 1


### ESTRUCTURA VISUAL DE LA PÁGINA
st.title("🍿 Mi Cine")
st.write("**Esta es tu propia lista de películas favoritas.**")
st.caption("Selecciona una de la tabla para administrarla")
st.divider()

## TABLA DE PELÍCULAS
# ------------------------------------------------------------------------------
pelis_usuario = obtener_pelis_usuario()

if pelis_usuario.empty:
    st.session_state["peli_seleccionada"] = None
    st.info("Todavía no tienes películas en Mi Cine.")

else:
    st.subheader(f"{len(pelis_usuario):,} películas en tu colección")

    nombres_columnas = {
        "id": "id",
        "title": "🎬 Película",
        "Vista": "👁️ Vista",
        "Por ver": "📌 Por ver",
        "Jugada": "🎲 Jugada",
        "release_date": "📅 Lanzamiento",
        "directors": "👤 Directores",
        "averageRating": "⭐ Rating",
        "genres": "🎭 Géneros",
    }

    tabla_mostrar = pelis_usuario[list(nombres_columnas.keys())].rename(
        columns=nombres_columnas
    )

    eventos_tabla = st.dataframe(
        tabla_mostrar,
        key=f"tabla_mi_cine_{st.session_state['version_tabla']}",
        width="stretch",
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
        column_config={
            "id": None,
            "👁️ Vista": st.column_config.CheckboxColumn("👁️ Vista", disabled=True),
            "📌 Por ver": st.column_config.CheckboxColumn("📌 Por ver", disabled=True),
            "🎲 Jugada": st.column_config.CheckboxColumn("🎲 Jugada", disabled=True),
        },
    )

    # Actualizar selección solo cuando el usuario hace clic en una fila de la tabla
    if eventos_tabla.selection.rows:
        indice = eventos_tabla.selection.rows[0]
        st.session_state["peli_seleccionada"] = str(tabla_mostrar.iloc[indice]["id"])


## DETALLES DE LA PELÍCULA SELECCIONADA
# ------------------------------------------------------------------------------
id_seleccionado = st.session_state.get("peli_seleccionada")

peli_seleccionada = (
    pelis_usuario[pelis_usuario["id"].astype(str) == str(id_seleccionado)]
    if id_seleccionado
    else pelis_usuario.iloc[0:0]
)

if not peli_seleccionada.empty:
    peli = peli_seleccionada.iloc[0]

    st.divider()

    listas_pelicula = [
        categoria for categoria in CATEGORIAS if peli[categoria]
    ]

    st.info("🍿 **Esta película pertenece a:** " + " | ".join(listas_pelicula))

    col_izq, col_der = st.columns([1, 2])

    with col_izq:
        if pd.notna(peli['poster_path']):
            url_poster = URL_POSTER + peli['poster_path']
            st.image(url_poster, width='stretch')

    with col_der:
        st.subheader(peli["title"])
        if pd.notna(peli["tagline"]):  # si no es vacío
            st.caption(traducir_texto(peli["tagline"]))
        st.write(traducir_texto(peli["overview"]))

        anho = f"📅 Lanzamiento: {str(peli['release_date'])[0:4]}"
        duracion_idioma = f"⌛ {peli['runtime']} minutos 🗣️ {traducir_idioma(peli['original_language'])}"

        rating = f"⭐ Rating: {peli['averageRating']}"
        generos = f"🎭 Géneros: {traducir_genero(peli['genres'])}"
        directores = f"👤 Directores: {peli['directors']}"
        guionistas = f"👥 Guionistas: {peli['writers']}"

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

        id_peli = int(peli["id"])

    ## ADMINISTRACIÓN DE LA PELÍCULA
    # ----------------------------------------------------------------------
    st.divider()
    st.write("**Administrar película:**")

    id_peli = peli["id"]
    botones = st.columns(3)

    # 1. Vista
    with botones[0]:
        if peli["Vista"]:
            st.button(
                "🗑️ Quitar de Vista",
                key=f"quitar_vista_{id_peli}",
                on_click=accion_quitar,
                args=(id_peli, "pelis_vistas"),
                width="stretch",
            )
        else:
            st.button(
                "✅ Marcar como vista",
                key=f"marcar_vista_{id_peli}",
                on_click=accion_cambiar_estado,
                args=(id_peli, "vista"),
                width="stretch",
            )

    # 2. Por ver
    with botones[1]:
        if peli["Por ver"]:
            st.button(
                "🗑️ Quitar de Por ver",
                key=f"quitar_por_ver_{id_peli}",
                on_click=accion_quitar,
                args=(id_peli, "pelis_ver"),
                width="stretch",
            )
        else:
            st.button(
                "💾 Guardar para ver",
                key=f"guardar_por_ver_{id_peli}",
                on_click=accion_cambiar_estado,
                args=(id_peli, "por_ver"),
                width="stretch",
            )

    # 3. Jugada
    with botones[2]:
        if peli["Jugada"]:
            st.button(
                "🗑️ Quitar de Jugada",
                key=f"quitar_jugada_{id_peli}",
                on_click=accion_quitar,
                args=(id_peli, "pelis_jugadas"),
                width="stretch",
            )
        else:
            if st.button(
                "🎲 Ir a jugar",
                key=f"ir_jugar_{id_peli}",
                width="stretch",
            ):
                st.switch_page("pages/jugar.py")

else:
    st.session_state["peli_seleccionada"] = None
    if not pelis_usuario.empty:
        st.info("👆 Selecciona una película de la tabla para ver sus detalles.")