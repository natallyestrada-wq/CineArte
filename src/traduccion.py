# MÓDULO TRADUCCION.PY
# Contiene funciones para la traducción al español

### PREPARACIÓN DEL ENTORNO
# Librerías externas:
import argostranslate.translate
import streamlit as st
import argostranslate.package

# Variables globales
from src.config import DICCIONARIO_GENEROS, DICCIONARIO_IDIOMAS

### FUNCIONES
# Función para instalar el paquete de traducción

# Instalar modelo de traducción si no existe
@st.cache_resource
def instalar_modelo():

    paquetes = argostranslate.package.get_installed_packages()

    instalado = any(
        p.from_code == "en" and p.to_code == "es"
        for p in paquetes
    )

    if instalado:
        return

    argostranslate.package.update_package_index()

    paquetes_disponibles = argostranslate.package.get_available_packages()

    modelo = next(
        (
            p for p in paquetes_disponibles
            if p.from_code == "en" and p.to_code == "es"
        ),
        None
    )

    if modelo is None:
        raise RuntimeError("No se encontró el modelo inglés-español.")

    ruta = modelo.download()
    argostranslate.package.install_from_path(ruta)

# Función para traducir texto
@st.cache_data
def traducir_texto(texto, idioma_origen="en", idioma_destino="es"):

    if not isinstance(texto, str) or not texto.strip():
        return texto

    try:
        instalar_modelo()
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
