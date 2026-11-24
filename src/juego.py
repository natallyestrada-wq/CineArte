# MÓDULO JUEGO.PY
# Contiene funciones para administración del juego en JUGAR.PY

### PREPARACIÓN DEL ENTORNO
# Librerías externas:
import streamlit as st

# Módulos propios
from src import traduccion as tr

# Variables globales
from src.config import URL_POSTER, RONDAS_TOTALES

### DEFINICIÓN DE FUNCIONES
def marcar_ronda(i):
    """Marca la ronda actual en la sesión de Streamlit.
    
    Parámetros: i, int, ronda actual
            
    """
    st.session_state["ronda_actual"] = i

    if i == (RONDAS_TOTALES+1):
        # mostrar globos de éxito porque se completó una partida   
        st.balloons()
        # registrar que se ha jugado una partida completa
        st.session_state["partidas_jugadas"] += 1
        # guardar el historial de pelis jugadas
        ids_jugados = st.session_state["tabla_historial"]["id"].astype(int).tolist()         
        st.session_state["pelis_jugadas"] = list(set(
            ids_jugados + st.session_state["pelis_jugadas"]
        ))

def reiniciar_juego():
    """Finaliza la ronda actual y borra datos innecesarios."""
    conservar = ["pelis_ver", 
                 "pelis_vistas",
                 "pelis_jugadas",
                 "partidas_jugadas",
                 ]
    
    for key in list(st.session_state.keys()):
        if key not in conservar:
            del st.session_state[key]

    marcar_ronda(-1)

def seleccionar_peli_duelo(df_duelos):
    """Función que escoge una película para
    enfrentar en el duelo cinéfilo según las preferencias
    y el historial del usuario.

    Parámetros:
        df_duelos: DataFrame, datos filtrados
    Retorna:
        id_peli_duelo: int, id de la peli a presentar en el duelo. 
        Retorna None si no es posible formar el duelo.
        """

    if "pelis_excluidas" not in st.session_state:
        st.session_state["pelis_excluidas"] = (st.session_state["pelis_vistas"] +
                                                st.session_state["pelis_ver"])
    
    ids_excluir = st.session_state["pelis_excluidas"]


    # Excluir películas ya vistas o ya usadas en el duelo
    df_duelos = df_duelos[
        ~df_duelos["id"].isin(ids_excluir)
    ]

    # Comprobar que existan películas para el duelo
    if df_duelos.empty:
        return None

    # Seleccionar una película compatible con los filtros del usuario
    id_peli_duelo = int(df_duelos.sample(1).iloc[0]["id"])

    # Agregar esa película en la lista de pelis a descartar
    st.session_state["pelis_excluidas"].append(id_peli_duelo)


    return id_peli_duelo

def registrar_seleccion(id_peli_seleccionada):

    st.session_state["peli_ganadora"] = id_peli_seleccionada

    # Opción 1:
    # st.session_state["ronda_actual"] += 1

    # Opción 2:
    marcar_ronda(st.session_state["ronda_actual"] + 1)

def llenar_caja_duelo(caja1, info_peli, texto_boton):

    with caja1.container(horizontal_alignment="center", vertical_alignment="bottom"):
        url_poster = URL_POSTER + info_peli['poster_path']

        with st.expander("Sinopsis"):
            st.caption(tr.traducir_texto(info_peli["overview"]))

        st.image(url_poster, width="stretch")
        st.write(f"**{info_peli['title']}**") 

        st.button(texto_boton, type="primary",
                    on_click=registrar_seleccion, 
                    args=[info_peli["id"]],
                    width="stretch"
                )      
        
        st.write(f"{info_peli['release_date'][0:4]} | {info_peli['runtime']} min")
        st.write(f"{tr.traducir_idioma(info_peli['original_language'])} ⭐ {info_peli['averageRating']}")
