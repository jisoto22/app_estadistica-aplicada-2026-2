"""Página de temas para distribuciones y modelos de secado."""

import streamlit as st

from src.datos import tarjeta_estudiante


# Se identifica al estudiante en la barra lateral compartida.
tarjeta_estudiante()

# Se presentan los temas previstos para los modelos probabilísticos y de secado.
st.title("Distribuciones")
st.info("En construcción")
st.markdown(
    """
### Temas
- Normal, Lognormal, Gamma, Weibull, Gumbel y GEV para precipitación máxima anual.
- Estimación de parámetros y pruebas de Kolmogorov-Smirnov y Anderson-Darling.
- Comparación mediante AIC, BIC y AICc.
- Períodos de retorno, riesgo e incertidumbre de las estimaciones.
- Modelos de secado en capa delgada y comparación con AICc.
"""
)