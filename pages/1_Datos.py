"""Página para explorar los datos del proyecto o cargar un archivo propio."""

from pathlib import Path

import pandas as pd
import streamlit as st

from src.datos import (
    cargar_csv,
    tarjeta_estudiante,
    tipos_de_variables,
    valores_faltantes,
)


# Se describen el contenido, las unidades y el uso académico de cada conjunto incluido.
DESCRIPCIONES_ARCHIVOS = {
    "parcelas.csv": {
        "representa": "Parcelas agrícolas simuladas para el cultivo personalizado del estudiante.",
        "unidades": "dosis_N: kg/ha; lamina_riego: mm; materia_organica: %; pH: sin unidad; rendimiento: t/ha.",
        "pagina": "EDA y Regresión.",
    },
    "precip_max_anual.csv": {
        "representa": "Máximo anual simulado de precipitación acumulada en 24 horas.",
        "unidades": "anio: año calendario; pmax24h_mm: mm en 24 horas.",
        "pagina": "Distribuciones.",
    },
    "clima_mensual.csv": {
        "representa": "Serie climática mensual simulada entre enero de 2015 y diciembre de 2025.",
        "unidades": "fecha: inicio de mes; precipitacion_mm: mm/mes; temperatura_c: °C.",
        "pagina": "Series de tiempo y EDA.",
    },
    "secado.csv": {
        "representa": "Razón de humedad simulada durante un ensayo de secado en capa delgada.",
        "unidades": "tiempo_min: minutos; MR: razón de humedad adimensional.",
        "pagina": "Distribuciones, comparación de modelos de secado.",
    },
}


# La tarjeta del estudiante se mantiene visible en la barra lateral.
tarjeta_estudiante()

# Se elige un conjunto del proyecto y se permite reemplazarlo temporalmente por un archivo propio.
st.title("Datos")
st.write("Explora un conjunto simulado o carga un CSV o un libro de Excel (.xlsx).")
archivo_seleccionado = st.selectbox(
    "Conjunto de datos del proyecto",
    options=list(DESCRIPCIONES_ARCHIVOS),
    format_func=lambda nombre: nombre.removesuffix(".csv"),
)
archivo_usuario = st.file_uploader(
    "Cargar datos propios (opcional)",
    type=["csv", "xlsx"],
    help="Si cargas un archivo, se usará en esta vista en lugar del conjunto seleccionado.",
)

# Se carga el archivo elegido; las fechas se convierten para mantener un tipo temporal utilizable.
try:
    if archivo_usuario is None:
        datos = cargar_csv(archivo_seleccionado)
        nombre_mostrado = archivo_seleccionado
        descripcion = DESCRIPCIONES_ARCHIVOS[archivo_seleccionado]
    else:
        extension = Path(archivo_usuario.name).suffix.lower()
        if extension == ".csv":
            datos = pd.read_csv(archivo_usuario)
        elif extension == ".xlsx":
            datos = pd.read_excel(archivo_usuario)
        else:
            st.error("Formato no compatible. Carga un archivo CSV o Excel .xlsx.")
            st.stop()

        if "fecha" in datos.columns:
            datos["fecha"] = pd.to_datetime(datos["fecha"], errors="coerce")
        nombre_mostrado = archivo_usuario.name
        descripcion = {
            "representa": "Archivo proporcionado por el usuario; su contenido depende de la tabla cargada.",
            "unidades": "Las unidades no se pueden inferir automáticamente; consúltalas en la fuente de los datos.",
            "pagina": "Datos. Puede utilizarse en EDA, Distribuciones, Regresión o Series de tiempo según sus variables.",
        }
except Exception as error:
    st.error(f"No fue posible leer el archivo seleccionado: {error}")
    st.stop()

# Se muestran dimensiones y registros para reconocer de inmediato el tamaño del conjunto.
st.subheader(f"Vista de datos: {nombre_mostrado}")
columna_filas, columna_variables = st.columns(2)
columna_filas.metric("Filas", len(datos))
columna_variables.metric("Columnas", len(datos.columns))
st.dataframe(datos, width="stretch", hide_index=True)

# Se presentan los tipos de almacenamiento y la clasificación estadística de cada variable.
st.subheader("Tipo y clasificación de las variables")
st.dataframe(tipos_de_variables(datos), width="stretch", hide_index=True)
st.caption(
    "Las fechas se clasifican como cuantitativas discretas por sus instantes de calendario; "
    "las categorías de texto se consideran nominales salvo que se indiquen como ordenadas."
)

# Se resumen faltantes con su número y porcentaje calculado sobre las filas del archivo.
st.subheader("Valores faltantes")
st.dataframe(valores_faltantes(datos), width="stretch", hide_index=True)

# Se documentan el significado, las unidades y las páginas de análisis recomendadas.
st.subheader("Descripción del archivo")
st.markdown(f"**Qué representa:** {descripcion['representa']}")
st.markdown(f"**Unidades:** {descripcion['unidades']}")
st.markdown(f"**Se usa en:** {descripcion['pagina']}")

# El archivo descargado corresponde a la tabla que está visible, incluso si se cargó un Excel.
nombre_descarga = f"{Path(nombre_mostrado).stem}.csv"
contenido_csv = datos.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "Descargar tabla como CSV",
    data=contenido_csv,
    file_name=nombre_descarga,
    mime="text/csv",
)