"""Página de inicio de la aplicación de Estadística Aplicada."""

import streamlit as st

from src.datos import tarjeta_estudiante


# La configuración de página se declara antes de mostrar elementos en la interfaz.
st.set_page_config(page_title="Estadística Aplicada con Python y R", layout="wide")

# La barra lateral mantiene visible la identificación del conjunto personalizado.
tarjeta_estudiante()

# La portada presenta el propósito académico y la navegación multipágina.
st.title("App de Estadística Aplicada — Ingeniería Agrícola, Unisucre")
st.markdown(
    "Esta aplicación reúne herramientas para explorar datos agrícolas y aplicar "
    "métodos estadísticos con criterios claros, resultados reproducibles y atención "
    "a las unidades y los supuestos de cada análisis."
)

# Se describen brevemente las tareas disponibles en cada página del proyecto.
st.subheader("Páginas de la aplicación")
st.markdown(
    """
- **Datos:** consulta los conjuntos simulados y revisa sus variables y observaciones.
- **EDA:** resume variables, distribuciones, relaciones y patrones iniciales.
- **Distribuciones:** analiza precipitación máxima anual y modelos de secado.
- **Regresión:** estudia correlaciones, regresión lineal e inferencia sobre la pendiente.
- **Series de tiempo:** explora componentes, métodos de referencia y pronósticos.
"""
)

# Se enfatiza el aprendizaje manual y la comprobación computacional como etapas complementarias.
st.subheader("Lápiz y Algoritmo")
st.markdown(
    "Primero se resuelve cada ejercicio a mano para comprender el procedimiento; "
    "luego se verifican los cálculos con la app, Python y R. La comparación ayuda "
    "a detectar errores y a entender qué hace cada método."
)

# La advertencia recuerda que las herramientas no reemplazan el criterio académico.
st.warning(
    "La app apoya el aprendizaje, pero la interpretación de los resultados y sus "
    "conclusiones es responsabilidad del estudiante."
)