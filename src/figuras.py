### PREPARACIÓN DEL ENTORNO
import streamlit as st
import plotly.express as px
import pandas as pd

from src.data import cargar_pelis
from src.traduccion import traducir_texto, traducir_genero, traducir_idioma


# -------- Gráfico de barras -------- Cantidad de películas por género
def pelis_por_genero(df, titulo="🎭 Análisis por género"):

    # Separar los géneros que están unidos por comas
    generos = df["genres"].str.split(",").explode().str.strip()

    # Contar la cantidad de cada género
    cantidad_por_genero = generos.value_counts().reset_index()
    # st.write(cantidad_por_genero)  # Mostrar la tabla de cantidad de películas por género

    # Traducir columna de género
    cantidad_por_genero["genres"] = cantidad_por_genero["genres"].apply(traducir_genero)

    # Crear la gráfica
    fig = px.bar(
        cantidad_por_genero,
        y="genres",
        x="count",
        color="count",
        color_continuous_scale="turbo",
        title=titulo,
        labels={"count": "Cantidad de películas", "genres": ""},
    )
    fig.update_layout(coloraxis_showscale=False)

    return fig


# -------- Gráfico de barras -------- Top de peliculas con mejor rating
def top_10_rating(df, titulo="🏆 Top 10 películas mejor calificadas"):
    # Las 10 películas con mayor calificación
    top_10_rating = df.nlargest(10, "averageRating")

    # Ordenar
    top_10_rating.sort_values("averageRating", inplace=True)

    # Crear la gráfica
    fig = px.bar(
        top_10_rating,
        x="averageRating",
        y="title",
        color="averageRating",
        color_continuous_scale="pinkyl_r",
        orientation="h",
        title=titulo,
        labels={
            "averageRating": "Calificación",
            "title": "",
        },
        text="title",
    )
    fig.update_layout(coloraxis_showscale=False)
    fig.update_yaxes(showticklabels=False)

    return fig


# -------- Histograma -------- Distribución de años de lanzamiento
def distribucion_de_anhos(df, titulo="📆 Distribución de años"):
    fig = px.histogram(
        df,
        x="release_date",
        title=titulo,
        labels={"release_date": "Año de lanzamiento"},
        color_discrete_sequence=["cornsilk"],
    )
    fig.update_yaxes(title_text="Cantidad de películas")
    # figura_rating.update_xaxes(title_text="Año de lanzamiento")
    fig.update_layout(hovermode="x unified")

    return fig


# -------- Gráfico de dispersión -------- Popularidad vs. Rating
def popularidad_por_rating(
    df, titulo="🎊 Popularidad vs. calificación", limite_popularidad=150
):
    df = df[df["popularity"] < limite_popularidad]

    fig = px.scatter(
        df,
        x="popularity",
        y="averageRating",
        hover_name="title",
        title=titulo,
        labels={"popularity": "Popularidad", "averageRating": "Calificación"},
        color="averageRating",
        color_continuous_scale="Inferno",
    )
    fig.update_layout(coloraxis_showscale=False)
    return fig


# -------- Gráfico de barras -------- Cantidad de películas por idioma
def pelis_por_idioma(df, titulo="🌎 Idiomas más comunes", max_peliculas=20):

    # Contar la cantidad de cada idioma
    cantidad_por_idioma = df["original_language"].value_counts().reset_index()

    # Los idiomas más comunes
    cantidad_por_idioma = cantidad_por_idioma.head(max_peliculas)

    # Traducir columna de idioma
    cantidad_por_idioma["original_language"] = cantidad_por_idioma[
        "original_language"
    ].apply(traducir_idioma)

    # Crear la gráfica
    fig = px.bar(
        cantidad_por_idioma,
        x="original_language",
        y="count",
        color="count",
        color_continuous_scale="ylorrd",
        title=titulo,
        orientation="v",
        labels={
            "count": "Cantidad de películas",
            "original_language": "Idioma original",
        },
    )
    fig.update_layout(coloraxis_showscale=False)

    return fig
