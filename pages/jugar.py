### PREPARACIÓN DEL ENTORNO
# Librerías externas:
import streamlit as st
import pandas as pd

# Módulos propios
from src import traduccion as tr
from src import juego as jg
from src.data import cargar_pelis, filtrar_peliculas, inicializar_sesion

# Variables globales
from src.config import URL_POSTER, RONDAS_TOTALES

# Carga de datos
pelis = cargar_pelis()

# Otras variables
COLUMNAS_DF = {
    "id": "id",
    "title": "🎬 Película",
    "genres": "🎭 Géneros",
    "directors": "👤 Directores",
    "averageRating": "⭐ Rating",
    'runtime': "⌛ Duración",
    "release_date": "📅 Año",
}

## INICIALIZACIÓN DE VARIABLES
# Variables generales:
inicializar_sesion()

# Si no se ha iniciado la partida, la ronda empieza en -1
if "ronda_actual" not in st.session_state:
    st.session_state["ronda_actual"] = -1

# Variable que activa o desactiva los botones de filtrado
if st.session_state["ronda_actual"] == -1:
    st.session_state["bloquear_filtros"] = False
else:
    st.session_state["bloquear_filtros"] = True

### ESTRUCTURA VISUAL DE LA PÁGINA
st.markdown("# 🎲 ¡Juguemos a Duelo cinéfilo!")
st.write("**Tendrás cuatro duelos para descubrir tu próxima película.**")
st.caption("Cuéntanos qué tipo de películas te gustaría descubrir:")
st.divider()

## PANTALLA DE PREFERENCIAS
# ------------------------------------------------------------------------------
opciones_experiencia = {         # Opciones de experiencia cinematográfica
    "💥 Acción y adrenalina": [
        "Action", "Adventure", "War", "Thriller"
    ],
    "🔍 Misterio y secretos": [
        "Mystery", "Crime", "Thriller"
    ],
    "👽 Mundos extraordinarios": [
        "Science Fiction", "Fantasy", "Adventure", "Animation"
    ],
    "😭 Emociones a flor de piel": [
        "Drama", "Romance", "History", "Music"
    ],
    "🗺️ Aventura y exploración": [
        "Adventure", "Western", "History", "War"
    ],
    "😂 Risas y diversión": [
        "Comedy", "Family", "Animation"
    ],
    "👻 Miedo y oscuridad": [
        "Horror", "Mystery", "Thriller"
    ],
    "🤯 Mentes sorprendidas": [
        "Science Fiction", "Mystery", "Thriller", "Drama"
    ],
    "🎬 Historias reales y del mundo": [
        "Documentary", "History", "War", "Music"
    ]
}

opciones_valoracion = [  # Opciones de valoración
    "⭐ Películas muy bien valoradas",
    "🧐 Películas poco populares",
    "🤯 Poco populares y bien valoradas",
    "🤷 Sin preferencia"
]

opciones_duracion = {   # Opciones de duración
    "🏃 Menos de 30 minutos":[0,30],
    "⏳ Hasta hora y media":[31,90],
    "⏰ Más de hora y media":[91,600],
    "🦦 Sin preferencia":[None, None]
}
# Presentación de botones de filtrado:
col1, col2, col3 = st.columns(3, vertical_alignment="center")
with col1:
    duracion_seleccionada = st.radio(
        "¿Qué duración prefieres?",
        list(opciones_duracion.keys()),
        index=len(opciones_duracion)-1, # Por defecto selecciona "Sin preferencia"
        disabled= st.session_state["bloquear_filtros"], # Para activar o desactivar los botones
    )

with col2:
    valoracion_seleccionada = st.radio(
        "¿Qué tipo de películas prefieres?",
        opciones_valoracion,
        index=len(opciones_valoracion)-1,
        disabled= st.session_state["bloquear_filtros"]
    )

with col3:
    excluir_adultos = st.checkbox("🔞 Excluir películas para adultos", wrap=True)


experiencias_seleccionadas = st.pills(
    "¿Qué tipo de experiencia buscas?",
    opciones_experiencia.keys(),
    selection_mode = "multi",
    width="stretch",
    wrap=True,   
    disabled= st.session_state["bloquear_filtros"]   
)

# Recálculo de variables según las selecciones del usuario
mejor_rating = False
desconocidas = False
if valoracion_seleccionada == "⭐ Películas muy bien valoradas":
    mejor_rating = True
elif valoracion_seleccionada == "🧐 Películas poco populares":
    desconocidas = True
elif valoracion_seleccionada == "🤯 Poco populares y bien valoradas":
    mejor_rating = True
    desconocidas = True


generos_seleccionados = []
for experiencia in experiencias_seleccionadas:
    generos = opciones_experiencia[experiencia]
    for genero in generos:
        if genero not in generos_seleccionados:
            generos_seleccionados.append(genero)
else:
    generos_seleccionados = [""]

duracion_seleccionada = opciones_duracion[duracion_seleccionada]

# with st.sidebar: # Para hacer debug de variables
# #     st.write(generos_seleccionados)    
#     st.write(duracion_seleccionada)    
#     st.write(duracion_seleccionada[0])    

## PANTALLA DE DUELOS
# ------------------------------------------------------------------------------
st.divider()
if st.session_state['ronda_actual'] == -1:
    st.button("¡Comenzar los duelos!",  # texto del botón
              type="primary",           # estilo del botón
              width="stretch",          # hace que el botón ocupe todo el ancho de la columna
              on_click=jg.marcar_ronda, # llama la función marcar_ronda() del módulo juego.py
              args=[0]                 # le manda el argumento a la función
    )

if st.session_state.ronda_actual == 0:
    df_duelos = filtrar_peliculas(
        pelis,

        generos=generos_seleccionados,

        duracion_min=duracion_seleccionada[0],
        duracion_max=duracion_seleccionada[1],
        mejor_rating = mejor_rating,
        desconocidas = desconocidas,
        excluir_adultos=excluir_adultos
    )

    id_primera_contrincante = jg.seleccionar_peli_duelo(df_duelos)

    if id_primera_contrincante and len(df_duelos)>= (RONDAS_TOTALES+1):
        jg.marcar_ronda(1) # indicar que se pasa a la ronda 1

        # Guardar vbles de sesión necesarias para las siguientes rondas
        st.session_state["df_duelos"] = df_duelos
        st.session_state["peli_ganadora"] = id_primera_contrincante

        tabla_historial = df_duelos.loc[
            df_duelos["id"] == id_primera_contrincante,
            COLUMNAS_DF.keys()
            ].rename(columns=COLUMNAS_DF)
        
        st.session_state["tabla_historial"] = tabla_historial
        
    else:
        st.warning("🥴 No hay suficientes películas para formar un duelo. "
            "Por favor, ajusta tus preferencias y vuelve a intentarlo.")
        jg.reiniciar_juego()


if st.session_state.ronda_actual >= 1 and st.session_state["ronda_actual"] <= RONDAS_TOTALES:
    st.info("⬇️ En cada duelo verás dos películas y deberás elegir la que más te llame la atención.")


    # dibuja el marco de los duelos en la interfaz de usuario
    col1, col2 = st.columns(2)

    with col1:
        col3, col4 = st.columns(2, border=True)
        with col3:
            caja1 = st.empty()
        with col4:
            caja2 = st.empty()  
    with col2:
        caja3 = st.empty()
    

    # extraer par de pelis para el duelo
    id_izquierda = st.session_state["peli_ganadora"]
    id_derecha = jg.seleccionar_peli_duelo(st.session_state["df_duelos"])

    # extraer df de historial
    tabla_historial = st.session_state["tabla_historial"] 


    # LLENAR CAJAS
    # caja 1
    info_peli = pelis[pelis['id'] == id_izquierda].iloc[0]  # extraer Serie de la peli
    jg.llenar_caja_duelo(caja1, info_peli, "☝️ Quiero esta")

    # caja 2
    info_peli = pelis[pelis['id'] == id_derecha].iloc[0]  # extraer Serie de la peli
    jg.llenar_caja_duelo(caja2, info_peli, "Prefiero esta ☝️")

    # Guardar info para el historial de la partida
    info_peli_der = info_peli.loc[
        COLUMNAS_DF.keys()
        ].rename(index=COLUMNAS_DF)

    tabla_historial = pd.concat(  # completar el historial con nueva peli
        [tabla_historial, info_peli_der.to_frame().T],
        ignore_index=True
    )

    st.session_state["tabla_historial"] = tabla_historial

    # caja 3
    with caja3.container():
        st.subheader(f"⚔️ Ronda {st.session_state['ronda_actual']} de {RONDAS_TOTALES}")
        st.progress(st.session_state["ronda_actual"] / (RONDAS_TOTALES+1))
        st.markdown("**Historial de duelos**",
                    help = "Desliza a la derecha 👉")

        st.dataframe(
            tabla_historial,
            width="stretch",
            hide_index=True,
            column_config={"id": None},  # Oculta la columna "id" de la tabla
        )

    

if st.session_state.ronda_actual == (RONDAS_TOTALES + 1):
    # dibuja el marco de los resultados
    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            id_ganadora = st.session_state["peli_ganadora"]
            info_peli = pelis[pelis['id'] == id_ganadora].iloc[0]

            st.subheader(f"🏆 Ganadora: {info_peli["title"]}")           
            if pd.notna(info_peli["tagline"]):                  # si no es vacío
                st.caption(tr.traducir_texto(info_peli["tagline"]))
            st.write(tr.traducir_texto(info_peli["overview"]))

            col_izq, col_der = st.columns([1, 2])
            with col_izq:
                url_poster = URL_POSTER + info_peli['poster_path']
                st.image(url_poster, width="stretch")

            with col_der:

                anho = f"📅 Lanzamiento: {info_peli['release_date'][0:4]}"
                duracion_idioma = f"⌛ {info_peli['runtime']} minutos 🗣️ {tr.traducir_idioma(info_peli['original_language'])}"

                rating = f"⭐ Rating: {info_peli['averageRating']}"
                generos = f"🎭 Géneros: {tr.traducir_genero(info_peli['genres'])}"
                directores = f"👤 Directores: {info_peli['directors']}"
                guionistas = f"👥 Guionistas: {info_peli['writers']}"

                st.markdown(
                    f"""
                    |||
                    | :--- | :--- | 
                    | {anho} | {duracion_idioma} |
                    | {rating} | {generos} | 
                    | {directores} | {guionistas} | 
                    """,
                )

            st.caption(f"**Reparto:** {info_peli['cast']}")

            boton_1, boton_2 = st.columns(2)
            with boton_1:
                if id_ganadora in st.session_state["pelis_ver"]:
                    st.success("💾 Guardada en tu lista para ver")
                elif st.button("💾 Guardar para ver", width="stretch"):
                    st.session_state["pelis_ver"].append(id_ganadora)
                    st.rerun()

            with boton_2:
                if id_ganadora in st.session_state["pelis_vistas"]:
                    st.success("✅ Marcada como vista")
                elif st.button("✅ Ya la vi", width="stretch"):
                    st.session_state["pelis_vistas"].append(id_ganadora)
                    st.rerun()

    with col2:
        
        tabla_historial = st.session_state["tabla_historial"] 

        st.subheader(f"⚔️ Partida finalizada")
        st.progress(st.session_state["ronda_actual"] / (RONDAS_TOTALES+1))
        st.markdown("**Historial de duelos**",
                    help = "Desliza a la derecha 👉")
        st.dataframe(
            tabla_historial,
            width="stretch",
            hide_index=True,
            column_config={"id": None},  # Oculta la columna "id" de la tabla
        )

        st.button("🎲 ¡Volver a jugar!",  
                type="primary",
                width="stretch",
                on_click=jg.reiniciar_juego,
                )

        st.markdown("**Tus estadísticas**")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Películas vistas", len(st.session_state["pelis_vistas"]))
        with col2:
            st.metric("Películas para ver", len(st.session_state["pelis_ver"]))
        with col3:
            st.metric("Partidas jugadas", st.session_state["partidas_jugadas"])

        if st.button("🍿 Ir a Mi Cine",
                    type="secondary",
                    width="stretch",
                    ):
            
            st.switch_page("pages/mi_cine.py")






        




        







