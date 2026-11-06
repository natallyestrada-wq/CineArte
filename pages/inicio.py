import streamlit as st
from pathlib import Path

# Rutas
RAIZ = Path(__file__).parent.parent
RUTA_FOTO = RAIZ / "assets" / "cindy_estrada.jpeg"

# TÍTULO Y DESCRIPCIÓN
st.title("🎬 Cine Arte")
st.write(
    "**Este es un espacio para explorar películas y descubrir tus nuevas"
    " historias favoritas a través del cine.**"
)
st.caption("Creado con Python, Streamlit e información de Kaggle por Cindy Estrada")


# SECCIONES
st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🔍 Explorar")
    st.write(
        "Descubre nuestro catálogo de películas."
        "y encuentra nuevas historias que te inspiren."
    )

    if st.button("Ir a Explorar", use_container_width=True):
        st.switch_page("pages/explorar.py")

with col2:
    st.subheader("🎲 Jugar")
    st.write(
        "¿Tienes el catálogo pero no sabes qué película ver? ¡Descubre tu próxima historia jugando!"
    )

    if st.button("Jugar", use_container_width=True):
        st.switch_page("pages/jugar.py")

with col3:
    st.subheader("🍿 Mi Cine")
    st.write(
        "Crea tu propia lista de películas favoritas."
        "Guarda las que has visto y las que quieres ver."
    )
    if st.button("Ir a Mi Cine", use_container_width=True):
        st.switch_page("pages/mi_cine.py")


# ESTADÍSTICAS DE USO
st.divider()
st.subheader("Tus estadísticas")

# Inicialización de variables de sesión
if "pelis_ver" not in st.session_state:
    st.session_state["pelis_ver"] = []
if "pelis_vistas" not in st.session_state:
    st.session_state["pelis_vistas"] = []
if "partidas_jugadas" not in st.session_state:
    st.session_state["partidas_jugadas"] = 0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Películas vistas", len(st.session_state["pelis_vistas"]))
with col2:
    st.metric("Películas para ver", len(st.session_state["pelis_ver"]))
with col3:
    st.metric("Partidas jugadas", st.session_state["partidas_jugadas"])
# st.write(f"Contador: {st.session_state.contador}")

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
