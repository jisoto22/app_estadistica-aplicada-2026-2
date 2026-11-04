"""Página para consultar y reconocer los conjuntos de datos disponibles."""

import streamlit as st

from src.datos import tarjeta_estudiante


# Se identifica al estudiante en la barra lateral compartida.
tarjeta_estudiante()

# Se presentan los temas previstos para la página de datos.
st.title("Datos")
st.info("En construcción")
st.markdown(
    """
### Temas
- Archivos simulados del proyecto y metadatos del estudiante.
- Vista previa, dimensiones, nombres y tipos de variables.
- Valores faltantes, duplicados y selección de variables.
- Unidades, períodos de observación y procedencia de los datos.
"""
)