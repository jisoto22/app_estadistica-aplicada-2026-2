"""Página de temas para correlación y regresión lineal simple."""

import streamlit as st

from src.datos import tarjeta_estudiante


# Se identifica al estudiante en la barra lateral compartida.
tarjeta_estudiante()

# Se presentan los temas previstos para el análisis de regresión.
st.title("Regresión")
st.info("En construcción")
st.markdown(
    """
### Temas
- Correlaciones de Pearson y Spearman.
- Regresión lineal simple por mínimos cuadrados ordinarios (MCO).
- Bondad de ajuste e inferencia sobre la pendiente.
- Diagnóstico de residuos, supuestos y observaciones influyentes.
"""
)