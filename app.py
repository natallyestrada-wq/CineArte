import streamlit as st
from pathlib import Path

RAIZ = Path(__file__).parent
RUTA_LOGO = RAIZ / "assets" / "logo_color_frio.png"

st.set_page_config(
    page_title="CineArte",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# st.sidebar.title("CineArte---")
st.sidebar.image(RUTA_LOGO)

pag = st.navigation(
    [
        st.Page("pages/inicio.py", title="Inicio", icon="🏠"),
        st.Page("pages/explorar.py", title="Explorar", icon="🔍"),
        st.Page("pages/jugar.py", title="Jugar", icon="🎲"),
        st.Page("pages/mi_cine.py", title="Mi Cine", icon="🍿"),
        st.Page("pages/pruebas.py", title="Pruebas", icon="🚧"),
    ],
)

pag.run()


# COPYRIGHT
st.divider()

izquierda, centro, derecha = st.columns([1, 2, 1])
with centro:
    st.caption(
        "© 2026 Cindy Estrada · CineArte · "
        "[Creative Commons BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)"
    )
