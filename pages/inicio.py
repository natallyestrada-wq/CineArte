### PREPARACIÓN DEL ENTORNO
# Librerías externas:
import streamlit as st

# Módulos propios
from src.data import inicializar_sesion

# Variables globales
from src.config import RUTA_FOTO

# Inicialización de variables de sesión
inicializar_sesion()

### ESTRUCTURA VISUAL DE LA PÁGINA
# TÍTULO Y DESCRIPCIÓN
st.title("🎬 CineArte")
st.write(
    "**Este es un espacio para explorar películas y descubrir tus nuevas"
    " historias favoritas a través del cine.**"
)
st.caption("Creado con Python, Streamlit e información de Kaggle por Cindy Estrada")


# SECCIONES
st.divider()

col1, col2, col3 = st.columns(3, vertical_alignment="bottom")

with col1:
    st.subheader("🔍 Explorar")
    st.write(
        "Descubre nuestro catálogo de películas "
        "y encuentra nuevas historias que te inspiren."
    )

    if st.button("Ir a Explorar", width="stretch"):
        st.switch_page("pages/explorar.py")

with col2:
    st.subheader("🎲 Jugar")
    st.write(
        "¿Tienes el catálogo pero no sabes qué película ver? ¡Descubre tu próxima historia jugando!"
    )

    if st.button("Jugar", width="stretch"):
        st.switch_page("pages/jugar.py")

with col3:
    st.subheader("🍿 Mi Cine")
    st.write(
        "Crea tu propia lista de películas favoritas"
        " con las que has visto y las que quieres ver."
    )
    if st.button("Ir a Mi Cine", width="stretch"):
        st.switch_page("pages/mi_cine.py")


# ESTADÍSTICAS DE USO
st.divider()
st.subheader("Tus estadísticas")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Películas vistas", len(st.session_state["pelis_vistas"]))
with col2:
    st.metric("Películas para ver", len(st.session_state["pelis_ver"]))
with col3:
    st.metric("Partidas jugadas", st.session_state["partidas_jugadas"])


# ACERCA DE
st.divider()
st.subheader("Acerca de la autora")

col_foto, col_bio = st.columns([1, 2])

with col_foto:
    st.image(RUTA_FOTO, width=220)

with col_bio:
    st.markdown("### Cindy Estrada")
    st.caption("Docente · Universidad de Antioquia")

    st.write("""
        Soy una profesional apasionada por la tecnología,
        la educación y la ciencia.

        Me gusta transformar ideas complejas en experiencias de
        aprendizaje claras y significativas. Disfruto aprender
        constantemente y combinar ciencia, tecnología y creatividad
        para resolver problemas.
        """)
