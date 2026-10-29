import streamlit as st

st.title("Página de pruebas 🚧")

### 1. verificar la ruta del archivo actual
# from pathlib import Path
# print(Path(__file__).parent)

### 2. verificar que cargan los datos correctamente
# from src.data import cargar_pelis
# pelis = cargar_pelis()

# st.subheader("Vista previa de Películas")
# st.dataframe(pelis)


### 3. verificar que se puede usar un botón
if st.button("hola mundo"):
    st.write("botón presionado")

### 4. Botón para aumentar variable de estado
if "contador" not in st.session_state:
    st.session_state.contador = 0

if st.button("Aumentar contador"):
    st.session_state.contador += 1
    st.write(f"Contador: {st.session_state.contador}")
