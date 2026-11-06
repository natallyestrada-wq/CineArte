import argostranslate.package
import argostranslate.translate
import streamlit as st

# Actualizar el índice de idiomas disponibles
argostranslate.package.update_package_index()

# Consultar los modelos disponibles
available_packages = argostranslate.package.get_available_packages()

# Buscar el modelo inglés -> español
package = next(
    filter(lambda x: x.from_code == "en" and x.to_code == "es", available_packages)
)

# Descargar e instalar el modelo
download_path = package.download()
argostranslate.package.install_from_path(download_path)

print("Modelo inglés-español instalado correctamente")
