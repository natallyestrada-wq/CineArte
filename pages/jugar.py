### PREPARACIÓN DEL ENTORNO
import streamlit as st
from src.data import cargar_pelis, filtrar_peliculas
from src import traduccion as tr
from src import juego as jg


### CARGA DE DATOS
pelis = cargar_pelis()

### CONFIGURACIÓN
RONDAS = 4

URL_POSTER = "https://image.tmdb.org/t/p/w500"

### INICIALIZACIÓN DE VARIABLES DE SESIÓN
# 1. Definir diccionario con el estado inicial 
estado_inicial = {
    "pelis_excluidas": [], 
    "pelis_ver": [],  # Películas que el usuario quiere ver
    "pelis_vistas": [],  # Películas que el usuario ya vio
    "partidas_jugadas": 0,  # Contador de partidas totales
    "ronda_actual": -1,  # Índice de la ronda en curso
}

# 2. Inicializar todas las variables
for clave, valor_defecto in estado_inicial.items():
  if clave not in st.session_state:
    st.session_state[clave] = valor_defecto


### ESTRUCTURA VISUAL DE LA PÁGINA
st.markdown("# 🎲 ¡Juguemos a Duelo cinéfilo!")
st.write("**Tendrás cuatro duelos para descubrir tu próxima película.**")
st.caption("Cuéntanos qué tipo de películas te gustaría descubrir:")


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
    )

with col2:
    valoracion_seleccionada = st.radio(
        "¿Qué tipo de películas prefieres?",
        opciones_valoracion,
        index=len(opciones_valoracion)-1
    )

with col3:
    excluir_adultos = st.checkbox("🔞 Excluir películas para adultos", wrap=True)


experiencias_seleccionadas = st.pills(
    "¿Qué tipo de experiencia buscas?",
    opciones_experiencia.keys(),
    selection_mode = "multi",
    width="stretch",
    wrap=True,       
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

duracion_seleccionada = opciones_duracion[duracion_seleccionada]

# with st.sidebar: # Para hacer debug de variables
# #     st.write(generos_seleccionados)    
#     st.write(duracion_seleccionada)    
#     st.write(duracion_seleccionada[0])    

## PANTALLA DE DUELOS
# ------------------------------------------------------------------------------
if st.session_state['ronda_actual'] == -1:
    st.button("¡Comenzar los duelos!",  # texto del botón
              type="primary",           # estilo del botón
              width="stretch",          # hace que el botón ocupe todo el ancho de la columna
              on_click=jg.marcar_ronda, # llama la función marcar_ronda() del módulo juego.py
              args=[0]                 # le manda el argumento a la función
    )
else:
    st.button("Empezar de cero",  
              type="primary",
              width="stretch",
              on_click=jg.reiniciar_juego,
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

    id_primera_contrincante = jg.seleccionar_peli__duelo(df_duelos)

    if id_primera_contrincante:
        jg.marcar_ronda(1) # indicar que se pasa a la ronda 1

        st.session_state["df_duelos"] = df_duelos
        st.session_state["peli_ganadora"] = id_primera_contrincante
    else:
        st.warning("🥴 No hay suficientes películas para formar un duelo. "
            "Por favor, ajusta tus preferencias y vuelve a intentarlo.")
        jg.reiniciar_juego()


if st.session_state.ronda_actual >= 1 and st.session_state["ronda_actual"] <= 4:
    st.caption(" En cada duelo verás dos películas y deberás elegir la que más te llame la atención.")
    st.subheader(f"⚔️ Ronda {st.session_state["ronda_actual"]} de {RONDAS}")
    st.progress(st.session_state["ronda_actual"] / RONDAS+1)
    
    caja1, caja2, resultado = jg.dibujar_marco_duelos()  # dibuja el marco de los duelos en la interfaz de usuario

    # extraer par de pelis para el duelo
    id_izquierda = st.session_state["peli_ganadora"]
    id_derecha = jg.seleccionar_peli__duelo(st.session_state["df_duelos"])

    # llenar cajones con datos
    with caja1.container(horizontal_alignment="center", vertical_alignment="bottom"):
        info_peli = pelis[pelis['id'] == id_izquierda].iloc[0]
        url_poster = URL_POSTER + info_peli['poster_path']

        if st.button("👈 Quiero esta", type="primary",
                        on_click=jg.registrar_seleccion, 
                        args=[id_izquierda],
                        width="stretch"):
            st.rerun()

        with st.expander("Sinopsis"):
            st.caption(tr.traducir_texto(info_peli["overview"]))

        st.image(url_poster, width="stretch")
        st.write(f"**{info_peli['title']}**") 
        st.write(f"{info_peli['release_date'][0:4]} | {info_peli['runtime']} min")
        st.write(f"{tr.traducir_idioma(info_peli['original_language'])} ⭐ {info_peli['averageRating']}")



    with caja2.container(horizontal_alignment="center", vertical_alignment="bottom"):
        info_peli = pelis[pelis['id'] == id_derecha].iloc[0]
        url_poster = URL_POSTER + info_peli['poster_path']

        if st.button("Prefiero esta 👉", type="primary",
                        on_click=jg.registrar_seleccion, 
                        args=[id_derecha],
                        width="stretch"):
            st.rerun()

        with st.expander("Sinopsis"):
            st.caption(tr.traducir_texto(info_peli["overview"]))

        st.image(url_poster, width="stretch")
        st.write(f"**{info_peli['title']}**") 
        st.write(f"{info_peli['release_date'][0:4]} | {info_peli['runtime']} min")
        st.write(f"{tr.traducir_idioma(info_peli['original_language'])} ⭐ {info_peli['averageRating']}")

        # Guardar info para el momento en que se acaben las rondas
        st.session_state["id_izquierda"] = id_izquierda
        st.session_state["id_derecha"] = id_derecha

if st.session_state.ronda_actual==5:

    # recuperar variables
    id_izquierda = st.session_state["id_izquierda"]
    id_derecha = st.session_state["id_derecha"] 
 
    st.caption("Duelo terminado")
    st.subheader(f"⚔️ ¡Hemos encontrado una ganadora!")
    st.progress(100)

    caja1, caja2, resultado = jg.dibujar_marco_duelos()  # dibuja el marco de los duelos en la interfaz de usuario

    # extraer par de pelis para el duelo
    # llenar cajones con datos
    with caja1.container(horizontal_alignment="center", vertical_alignment="bottom"):
        info_peli = pelis[pelis['id'] == id_izquierda].iloc[0]
        url_poster = URL_POSTER + info_peli['poster_path']

        with st.expander("Sinopsis"):
            st.caption(tr.traducir_texto(info_peli["overview"]))

        st.image(url_poster, width="stretch")
        st.write(f"**{info_peli['title']}**") 
        st.write(f"{info_peli['release_date'][0:4]} | {info_peli['runtime']} min")
        st.write(f"{tr.traducir_idioma(info_peli['original_language'])} ⭐ {info_peli['averageRating']}")



    with caja2.container(horizontal_alignment="center", vertical_alignment="bottom"):
        info_peli = pelis[pelis['id'] == id_derecha].iloc[0]
        url_poster = URL_POSTER + info_peli['poster_path']

        with st.expander("Sinopsis"):
            st.caption(tr.traducir_texto(info_peli["overview"]))

        st.image(url_poster, width="stretch")
        st.write(f"**{info_peli['title']}**") 
        st.write(f"{info_peli['release_date'][0:4]} | {info_peli['runtime']} min")
        st.write(f"{tr.traducir_idioma(info_peli['original_language'])} ⭐ {info_peli['averageRating']}")


    with resultado:
        id_ganadora = st.session_state["peli_ganadora"]
        info_peli = pelis[pelis['id'] == id_ganadora].iloc[0]

        col1, col2 = st.columns(2)

        with col1:   
            url_poster = URL_POSTER + info_peli['poster_path']
            st.image(url_poster, width="stretch")
        with col2:
            st.write(f"**{info_peli['title']}**") 
            st.write(f"{info_peli['release_date'][0:4]} | {info_peli['runtime']} min")
            st.write(f"{tr.traducir_idioma(info_peli['original_language'])} ⭐ {info_peli['averageRating']}")


    


if st.session_state.ronda_actual>5645:
    st.write('Terminamos')
    st.session_state.partidas_jugadas += 1
    st.write("Tu peli recomendada es -------")
#? función ? mostrar ganadora
    id_ganadora ="ññññññññññññ"

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






        




        







