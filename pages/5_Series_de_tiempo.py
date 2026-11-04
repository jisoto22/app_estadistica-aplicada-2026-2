"""Página de temas para análisis y pronóstico de series de tiempo."""

import streamlit as st

from src.datos import tarjeta_estudiante


# Se identifica al estudiante en la barra lateral compartida.
tarjeta_estudiante()

# Se presentan los temas previstos para el análisis temporal y el pronóstico.
st.title("Series de tiempo")
st.info("En construcción")
st.markdown(
    """
### Temas
- Tendencia, estacionalidad y componente irregular.
- Promedios móviles e índices estacionales.
- Descomposición clásica aditiva y multiplicativa.
- Métodos de referencia y validación temporal.
- Métricas MAE, RMSE y SMAPE; pronósticos con AutoTS.
"""
)