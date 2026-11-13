import streamlit as st

def marcar_ronda(i):
    """Marca la ronda actual en la sesión de Streamlit."""
    st.session_state["ronda_actual"] = i

def reiniciar_juego():
    """Finaliza la ronda actual y borra datos innecesarios."""
    conservar = ["pelis_ver", 
                 "pelis_vistas",
                 "partidas_jugadas"
                 ]
    
    for key in list(st.session_state.keys()):
        if key not in conservar:
            del st.session_state[key]

    marcar_ronda(-1)

def seleccionar_peli__duelo(df_duelos):
    """Función que escoge una película para
    enfrentar en el duelo cinéfilo según las preferencias
    y el historial del usuario.

    Parámetros:
        df_duelos: DataFrame, datos filtrados
    Retorna:
        id_peli_duelo: int, id de la peli a presentar en el duelo. 
        Retorna None si no es posible formar el duelo.
        """

    if not "pelis_excluidas" in st.session_state:
        st.session_state["pelis_excluidas"] = st.session_state["pelis_vistas"]  
    
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

def dibujar_marco_duelos():
    """Dibuja el marco de los duelos cinéfilos en la interfaz de usuario.
    Crea un contenedores para mostrar las películas en duelo
    y el resultado de la elección del usuario.
    """

    col1, col2, resultado = st.columns([1,1,2], border=True)

    with col1:
        caja1 = st.empty()

    with col2:
        caja2 = st.empty()

    with resultado:
        st.write("🏆 **GANADORA**")

    return caja1, caja2, resultado

def registrar_seleccion(id_peli_seleccionada):

    st.session_state["peli_ganadora"] = id_peli_seleccionada

    # Opción 1:
    # st.session_state["ronda_actual"] += 1

    # Opción 2:
    marcar_ronda(st.session_state["ronda_actual"] + 1)

