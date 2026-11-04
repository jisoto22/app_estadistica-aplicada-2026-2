"""Funciones compartidas para leer los datos y presentar al estudiante."""

import json
from pathlib import Path

import pandas as pd
import streamlit as st


# Se calcula la carpeta de datos desde este módulo para que las rutas no dependan del directorio actual.
DIRECTORIO_DATOS = Path(__file__).resolve().parents[1] / "datos"


@st.cache_data
def cargar_csv(nombre: str) -> pd.DataFrame:
    """Carga un CSV de datos/ y convierte a fecha la columna fecha si está presente.

    Esta función permite reutilizar los archivos simulados en distintas páginas de
    la aplicación. La caché evita releer el archivo mientras no cambie su contenido.

    Args:
        nombre: Nombre de un archivo CSV ubicado directamente en datos/.

    Returns:
        Tabla de pandas con los registros del archivo.

    Raises:
        ValueError: Si el nombre intenta salir de la carpeta datos/.
        FileNotFoundError: Si el archivo solicitado no existe.
    """
    # Se restringe la ruta a datos/ para que las páginas solo lean los conjuntos del proyecto.
    ruta_csv = (DIRECTORIO_DATOS / nombre).resolve()
    if ruta_csv.parent != DIRECTORIO_DATOS:
        raise ValueError("El archivo debe estar directamente dentro de datos/.")
    if not ruta_csv.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de datos: {nombre}")

    # Se inspecciona el encabezado para solicitar el parseo de fechas solo cuando exista esa columna.
    columnas = pd.read_csv(ruta_csv, nrows=0).columns
    columnas_fecha = ["fecha"] if "fecha" in columnas else None
    return pd.read_csv(ruta_csv, parse_dates=columnas_fecha)


@st.cache_data
def cargar_metadatos() -> dict:
    """Lee datos/metadatos.json con la identificación del estudiante.

    Returns:
        Diccionario con código, nombre, cultivo, municipio, cantidad de parcelas y huella.
    """
    # Se abre el JSON en UTF-8 para conservar correctamente los nombres con tildes y eñes.
    ruta_metadatos = DIRECTORIO_DATOS / "metadatos.json"
    with ruta_metadatos.open("r", encoding="utf-8") as archivo_json:
        return json.load(archivo_json)


def tarjeta_estudiante() -> None:
    """Muestra los datos del estudiante en la barra lateral de Streamlit.

    La tarjeta identifica el conjunto de datos personalizado que se está usando
    durante las actividades de estadística aplicada.
    """
    # Se consulta el archivo compartido y se informa con claridad si aún no está disponible.
    with st.sidebar:
        st.subheader("Estudiante")
        try:
            metadatos = cargar_metadatos()
        except FileNotFoundError:
            st.warning("No se encontró datos/metadatos.json.")
            return

        # Cada campo se muestra con una etiqueta para facilitar la identificación del conjunto.
        st.markdown(f"**Nombre:** {metadatos['nombre']}")
        st.markdown(f"**Código:** {metadatos['codigo']}")
        st.markdown(f"**Cultivo:** {metadatos['cultivo']}")
        st.markdown(f"**Municipio:** {metadatos['municipio']}")
        st.markdown(f"**Huella:** `{metadatos['huella']}`")