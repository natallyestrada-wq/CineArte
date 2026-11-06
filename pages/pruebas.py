import streamlit as st
import plotly.express as px
import pandas as pd

from src.data import cargar_pelis
from src.traduccion import traducir_texto, traducir_genero, traducir_idioma
import src.figuras as fig

st.title("Página de pruebas 🚧")

pelis = cargar_pelis()
# Mostrar la gráfica
st.plotly_chart(fig.pelis_por_genero(pelis))
st.plotly_chart(fig.top_10_rating(pelis))
st.plotly_chart(fig.distribucion_de_anhos(pelis))
st.plotly_chart(fig.popularidad_por_rating(pelis, limite_popularidad=200))
st.plotly_chart(fig.pelis_por_idioma(pelis))


# #----------------------------------------------------------------------------------------
# ## 4. Botón para aumentar variable de estado
# if "contador" not in st.session_state:
#     st.session_state.contador = 0

# if st.button("Aumentar contador"):
#     st.session_state.contador += 1
#     st.write(f"Contador: {st.session_state.contador}")

# ## 3. verificar que se puede usar un botón
# if st.button("hola mundo"):
#     st.write("botón presionado")


### 2. verificar que cargan los datos correctamente
# from src.data import cargar_pelis
# pelis = cargar_pelis()

# st.subheader("Vista previa de Películas")
# st.dataframe(pelis)

### 1. verificar la ruta del archivo actual
# from pathlib import Path
# print(Path(__file__).parent)
