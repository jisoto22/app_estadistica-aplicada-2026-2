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


def tipos_de_variables(df: pd.DataFrame) -> pd.DataFrame:
    """Resume el tipo de dato y la clasificación estadística de cada columna.

    Las columnas numéricas enteras se clasifican como discretas y las numéricas
    no enteras como continuas. Las fechas se consideran cuantitativas discretas
    porque se observan en instantes de calendario; las categorías ordenadas se
    clasifican como cualitativas ordinales.

    Args:
        df: Tabla cuyas columnas se van a describir.

    Returns:
        Tabla con nombre de variable, tipo de dato y clasificación estadística.
    """
    # Se determina la clasificación de cada variable a partir del dtype disponible.
    filas = []
    for nombre_variable in df.columns:
        serie = df[nombre_variable]
        tipo_dato = str(serie.dtype)

        # Las categorías ordenadas conservan su jerarquía; las demás son nominales.
        if isinstance(serie.dtype, pd.CategoricalDtype):
            clasificacion = (
                "cualitativa ordinal" if serie.dtype.ordered else "cualitativa nominal"
            )
        elif pd.api.types.is_bool_dtype(serie.dtype):
            clasificacion = "cualitativa nominal"
        elif pd.api.types.is_datetime64_any_dtype(serie.dtype):
            clasificacion = "cuantitativa discreta"
        elif pd.api.types.is_numeric_dtype(serie.dtype):
            if nombre_variable == "tiempo_min":
                clasificacion = "cuantitativa continua"
            elif pd.api.types.is_integer_dtype(serie.dtype):
                clasificacion = "cuantitativa discreta"
            else:
                clasificacion = "cuantitativa continua"
        else:
            clasificacion = "cualitativa nominal"

        filas.append(
            {
                "variable": nombre_variable,
                "tipo_dato": tipo_dato,
                "clasificacion_estadistica": clasificacion,
            }
        )

    # Se devuelve una tabla incluso cuando el DataFrame no tiene columnas.
    return pd.DataFrame(
        filas,
        columns=["variable", "tipo_dato", "clasificacion_estadistica"],
    )


def valores_faltantes(df: pd.DataFrame) -> pd.DataFrame:
    """Calcula la cantidad y el porcentaje de valores faltantes por columna.

    Args:
        df: Tabla en la que se van a contar valores faltantes.

    Returns:
        Tabla con variable, cantidad faltante y porcentaje respecto de las filas.
    """
    # Se cuentan valores nulos por columna y se evita dividir entre cero en tablas vacías.
    cantidades = df.isna().sum()
    porcentajes = cantidades / len(df) * 100 if len(df) else cantidades.astype(float)

    # Se conservan todas las variables para que también aparezcan las que no tienen faltantes.
    return pd.DataFrame(
        {
            "variable": df.columns,
            "cantidad_faltante": cantidades.to_numpy(),
            "porcentaje_faltante": porcentajes.to_numpy().round(2),
        }
    )