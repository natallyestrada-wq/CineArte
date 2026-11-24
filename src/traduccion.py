# MÓDULO TRADUCCION.PY
# Contiene funciones para la traducción al español

### PREPARACIÓN DEL ENTORNO
# Librerías externas:
import argostranslate.translate
import streamlit as st

# Variables globales
from src.config import DICCIONARIO_GENEROS, DICCIONARIO_IDIOMAS

### FUNCIONES
# Función para traducir texto
@st.cache_data
def traducir_texto(texto, idioma_origen="en", idioma_destino="es"):

    if not isinstance(texto, str) or not texto.strip():
        return texto

    try:
        traduccion = argostranslate.translate.translate(
            texto, idioma_origen, idioma_destino
        )

    except Exception as e:
        return texto

    return traduccion


def traducir_genero(genero):

    if isinstance(genero, list):
        generos_traducidos = []

        for nombre in genero:
            traduccion = DICCIONARIO_GENEROS.get(nombre, nombre)
            generos_traducidos.append(traduccion)

        return generos_traducidos

    return DICCIONARIO_GENEROS.get(genero, genero)


def traducir_idioma(idioma):
    
    return DICCIONARIO_IDIOMAS.get(idioma, "Desconocido")
