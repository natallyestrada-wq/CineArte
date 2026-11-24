import streamlit as st
import plotly.express as px
import pandas as pd

from src.data import cargar_pelis
from src.traduccion import traducir_texto, traducir_genero, traducir_idioma
import src.figuras as fig
from src.juego import marcar_ronda, registrar_seleccion, reiniciar_juego

#---------------------Para hacer debuging------------
from pprint import pprint
pprint(dict(st.session_state))
#----------------------------------------------------

st.title("Página de pruebas 🚧")
# 7. 


# 6. Comportamiento de botones y variables de sesión
#a
st.divider()
# if st.button("presioname"):
#     st.write("¡Botón presionado!")
# st.slider("Selecciona un valor", 0, 100, 50)

# #b
# st.divider()
# if 'clicked' not in st.session_state:
#     st.session_state.clicked = False

# def click_button():
#     st.session_state.clicked = True

# st.button('Click me', on_click=click_button)

# if st.session_state.clicked:
#     # The message and nested widget will remain on the page
#     st.write('Button clicked!')
#     st.slider('Select a value')

# # c.
# st.divider()
# if 'stage' not in st.session_state:
#     st.session_state.stage = 0

# def set_state(i):
#     st.session_state.stage = i

# if st.session_state.stage == 0:
#     st.button('Begin', on_click=set_state, args=[1])
# else:
#     st.button('Start Over', type='primary',on_click=set_state, args=[0])

# if st.session_state.stage >= 1:
#     name = st.text_input('Name', on_change=set_state, args=[2])

# if st.session_state.stage >= 2:
#     st.write(f'Hello {name}!')
#     color = st.selectbox(
#         'Pick a Color',
#         [None, 'red', 'orange', 'green', 'blue', 'violet'],
#         on_change=set_state, args=[3]
#     )
#     if color is None:
#         set_state(2)

# if st.session_state.stage >= 3:
#     st.write(f':{color}[Thank you!]')

#-------------------------------------------------------------------------------------
# d.
# if not "pelis_excluidas" in st.session_state:
#     st.session_state.pelis_excluidas=[]

# if ("pelis_ver" not in st.session_state):  # para guardar las películas que el usuario quiere ver
#     st.session_state["pelis_ver"] = []

# if ("pelis_vistas" not in st.session_state):  # para guardar las películas que el usuario ya vió
#     st.session_state["pelis_vistas"] = []

# if not "partidas_jugadas" in st.session_state:
#     st.session_state.partidas_jugadas = 0
    
# if 'ronda_actual' not in st.session_state:
#     st.session_state.ronda_actual = -1 

# #-------------------------
# if st.session_state.ronda_actual == -1:
#     st.button('No ha iniciado la partida, comenzar', on_click=marcar_ronda, args=[0])
# else:
#     st.button('Empezar de cero', on_click=reiniciar_juego)

# if st.session_state.ronda_actual == 0:
#     st.write("analizando juego, escoge si iniciar ronda 1")

#     # filtrar df
# # filtrar_pelis(preferencias)

#     # condicional:        
#     #si si:
#     st.button('si se puede Iniciar ronda 1', on_click=marcar_ronda, args=[1])
#     # guardar df en estado
#     # st.session_state["df_duelos"] = .....

#     #si no:
#     st.button('No se puede iniciar ronda 1', on_click=marcar_ronda, args=[-1])


# if st.session_state.ronda_actual == 1:

#     st.write('Éxito, entramos al juego')
#     st.write("mostrar aquí marco de duelos")
# # dibujar_marco_duelos()

#     # extraer par de pelis
# # peli_izq = seleccionar_peli_duelo()
# # peli_der = seleccionar_peli_duelo()
#     st.write(f"mostrar aquí el duelo {st.session_state.ronda_actual}")
# #? funcion? mostrar peli_izq y peli_der
# #? función? mostrar botones:

#     if st.button("escojo peli izquierda", 
#               on_click=registrar_seleccion, 
#               args=["id peli izq"]):
#         st.rerun()
#     if st.button("escojo peli derecha", 
#               on_click=registrar_seleccion, 
#               args=["id peli der"]):
#         st.rerun()
# # registrar_seleccion()

# if st.session_state.ronda_actual >= 2 and st.session_state.ronda_actual <=4:

#     # extraer par de pelis
# # peli_izq = st.session_state["peli_ganadora"]
# # peli_der = seleccionar_peli_duelo()
#     st.write(f"mostrar aquí el duelo {st.session_state.ronda_actual}")
# #? funcion? mostrar peli_izq y peli_der
# #? función? mostrar botones:

#     if st.button("escojo peli izquierda", 
#               on_click=registrar_seleccion, 
#               args=["id peli izq"]):
#         st.rerun()
#     if st.button("escojo peli derecha", 
#               on_click=registrar_seleccion, 
#               args=["id peli der"]):
#         st.rerun()
# # registrar_seleccion()




# if st.session_state.ronda_actual==5:
#     st.write('Terminamos')
#     st.session_state.partidas_jugadas += 1
#     st.write("Tu peli recomendada es -------")
# #? función ? mostrar ganadora
#     id_ganadora ="ññññññññññññ"

#     boton_1, boton_2 = st.columns(2)
#     with boton_1:
#         if id_ganadora in st.session_state["pelis_ver"]:
#             st.success("💾 Guardada en tu lista para ver")
#         elif st.button("💾 Guardar para ver", width="stretch"):
#             st.session_state["pelis_ver"].append(id_ganadora)
#             st.rerun()

#     with boton_2:
#         if id_ganadora in st.session_state["pelis_vistas"]:
#             st.success("✅ Marcada como vista")
#         elif st.button("✅ Ya la vi", width="stretch"):
#             st.session_state["pelis_vistas"].append(id_ganadora)
#             st.rerun()

    
    

# #----------------------------------------------------------------------------------------
# # 5.Mostrar la gráfica
# pelis = cargar_pelis()
# st.plotly_chart(fig.pelis_por_genero(pelis))
# st.plotly_chart(fig.top_10_rating(pelis))
# st.plotly_chart(fig.distribucion_de_anhos(pelis))
# st.plotly_chart(fig.popularidad_por_rating(pelis, limite_popularidad=200))
# st.plotly_chart(fig.pelis_por_idioma(pelis))

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
