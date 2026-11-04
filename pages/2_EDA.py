"""Página de temas para el análisis exploratorio de datos."""

import streamlit as st

from src.datos import tarjeta_estudiante


# Se identifica al estudiante en la barra lateral compartida.
tarjeta_estudiante()

# Se presentan los temas previstos para el análisis exploratorio.
st.title("EDA: Análisis Exploratorio de Datos")
st.info("En construcción")
st.markdown(
    """
### Temas
- Estadísticos descriptivos, cuantiles y frecuencias.
- Histogramas, densidades y diagramas de caja.
- Gráficos de dispersión y asociaciones iniciales.
- Detección exploratoria de valores atípicos y patrones temporales.
"""
)