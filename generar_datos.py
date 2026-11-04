"""Genera datos agrícolas simulados, reproducibles y personalizados."""

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


# Estos datos identifican al estudiante y determinan toda la simulación.
CODIGO = "1104417335"
NOMBRE = "Jose Ignacio Soto Viloria"


def main():
    """Crea los datos del proyecto y muestra las muestras para los ejercicios."""
    # La semilla personaliza los resultados y permite repetir exactamente la simulación.
    semilla = int(CODIGO) % (2**32)
    rng = np.random.default_rng(semilla)

    # Cada cultivo tiene un rendimiento base expresado en toneladas por hectárea.
    rendimientos_base = {
        "Maíz": 5.2,
        "Arroz": 5.8,
        "Yuca": 18.0,
        "Ñame": 12.0,
        "Ajonjolí": 0.9,
        "Plátano": 14.0,
        "Frijol": 1.5,
        "Sorgo": 3.2,
    }
    cultivo = str(rng.choice(list(rendimientos_base)))
    municipios = [
        "Sincelejo",
        "Corozal",
        "Sampués",
        "Los Palmitos",
        "San Marcos",
        "Majagual",
        "Tolú",
        "Ovejas",
    ]
    municipio = str(rng.choice(municipios))
    rendimiento_base = rendimientos_base[cultivo]

    # Se generan parcelas con tratamientos y condiciones de suelo variados.
    n_parcelas = int(rng.integers(80, 121))
    suelos = np.array(["Franco", "Arcilloso", "Arenoso"])
    suelo = rng.choice(suelos, size=n_parcelas, p=[0.45, 0.35, 0.20])
    riego = rng.choice(np.array(["Sí", "No"]), size=n_parcelas, p=[0.55, 0.45])
    dosis_n = rng.uniform(0, 180, size=n_parcelas)
    lamina_riego = np.where(
        riego == "Sí",
        rng.uniform(80, 240, size=n_parcelas),
        rng.uniform(0, 30, size=n_parcelas),
    )
    materia_organica_real = rng.uniform(0.5, 5.0, size=n_parcelas)
    ph = rng.uniform(4.8, 7.8, size=n_parcelas)

    # El rendimiento responde a nitrógeno, agua, materia orgánica, pH y suelo.
    efecto_suelo = {"Franco": 0.08, "Arcilloso": 0.02, "Arenoso": -0.09}
    factor_rendimiento = (
        1
        + 0.20 * dosis_n / 180
        + 0.12 * lamina_riego / 240
        + 0.12 * (materia_organica_real - 2.5) / 2.5
        - 0.08 * (ph - 6.3) ** 2
        + np.array([efecto_suelo[tipo_suelo] for tipo_suelo in suelo])
    )
    rendimiento = rendimiento_base * factor_rendimiento
    rendimiento += rng.normal(0, max(0.05, rendimiento_base * 0.06), size=n_parcelas)
    rendimiento = np.maximum(rendimiento, rendimiento_base * 0.15)

    # Dos parcelas se separan deliberadamente del patrón para practicar detección de atípicos.
    indices_atipicos = rng.choice(n_parcelas, size=2, replace=False)
    indice_atipico_alto, indice_atipico_bajo = map(int, indices_atipicos)
    rendimiento[indice_atipico_alto] = max(
        rendimiento_base * 3.0,
        float(np.max(rendimiento) + rendimiento_base * 1.5),
    )
    rendimiento[indice_atipico_bajo] = rendimiento_base * 0.05

    # Se dejan entre tres y seis mediciones de materia orgánica como valores faltantes.
    materia_organica = materia_organica_real.copy()
    n_faltantes = int(rng.integers(3, 7))
    indices_faltantes = rng.choice(n_parcelas, size=n_faltantes, replace=False)
    materia_organica[indices_faltantes] = np.nan
    parcelas = pd.DataFrame(
        {
            "parcela": [f"P{numero:03d}" for numero in range(1, n_parcelas + 1)],
            "suelo": suelo,
            "riego": riego,
            "dosis_N": np.round(dosis_n, 2),
            "lamina_riego": np.round(lamina_riego, 2),
            "materia_organica": np.round(materia_organica, 2),
            "ph": np.round(ph, 2),
            "rendimiento": np.round(rendimiento, 2),
        }
    )

    # La precipitación máxima anual se simula con una Gumbel cuyos parámetros dependen del código.
    mu_gumbel = 70 + (semilla % 3001) / 100
    beta_gumbel = 12 + ((semilla // 3001) % 801) / 100
    anios = np.arange(1986, 2026)
    precip_max_anual = pd.DataFrame(
        {
            "anio": anios,
            "pmax24h_mm": np.round(
                rng.gumbel(loc=mu_gumbel, scale=beta_gumbel, size=len(anios)), 2
            ),
        }
    )

    # La lluvia tiene dos temporadas húmedas y ruido lognormal; la temperatura combina ciclo y tendencia.
    fechas = pd.date_range("2015-01-01", "2025-12-01", freq="MS")
    mes = fechas.month.to_numpy()
    anio = fechas.year.to_numpy()
    lluvia_media_mensual = np.array([25, 20, 25, 110, 145, 85, 70, 80, 125, 150, 135, 40])
    sigma_lluvia = 0.45
    ruido_lognormal = rng.lognormal(
        mean=-(sigma_lluvia**2) / 2,
        sigma=sigma_lluvia,
        size=len(fechas),
    )
    precipitacion_mensual = lluvia_media_mensual[mes - 1] * ruido_lognormal
    temperatura = 27.0 + 0.025 * (anio - 2015)
    temperatura += 1.1 * np.cos(2 * np.pi * (mes - 4) / 12)
    temperatura += rng.normal(0, 0.35, size=len(fechas))
    clima_mensual = pd.DataFrame(
        {
            "fecha": fechas,
            "precipitacion_mm": np.round(precipitacion_mensual, 2),
            "temperatura_c": np.round(temperatura, 2),
        }
    )

    # La razón de humedad sigue el modelo de Page, con ruido pequeño y límites físicos.
    tiempo_min = np.arange(0, 301, 15)
    k_page = 0.0007 + (semilla % 8001) / 10_000_000
    n_page = 1.1 + ((semilla // 8001) % 600) / 1000
    mr_ideal = np.exp(-k_page * tiempo_min**n_page)
    mr_observado = mr_ideal + rng.normal(0, 0.012, size=len(tiempo_min))
    mr_observado = np.clip(mr_observado, 0, 1)
    mr_observado[0] = 1.0
    secado = pd.DataFrame(
        {"tiempo_min": tiempo_min, "MR": np.round(mr_observado, 4)}
    )

    # Se forman las cuatro muestras pequeñas con reglas reproducibles para ejercicios manuales.
    indices_regulares = np.setdiff1d(np.arange(n_parcelas), indices_atipicos)
    indice_un_atipico = int(rng.choice(indices_atipicos))
    indices_eda = np.concatenate(
        [
            rng.choice(indices_regulares, size=9, replace=False),
            np.array([indice_un_atipico]),
        ]
    )
    rng.shuffle(indices_eda)
    muestra_eda10 = parcelas.iloc[indices_eda][
        ["parcela", "suelo", "riego", "rendimiento"]
    ].reset_index(drop=True)

    indices_dist = rng.choice(len(precip_max_anual), size=10, replace=False)
    muestra_dist10 = precip_max_anual.iloc[indices_dist].sort_values("anio").reset_index(drop=True)

    # qcut crea ocho estratos de lámina; se toma una parcela regular al azar en cada estrato.
    parcelas_regulares = parcelas.iloc[indices_regulares].copy()
    parcelas_regulares["grupo_lamina"] = pd.qcut(
        parcelas_regulares["lamina_riego"], q=8, labels=False, duplicates="drop"
    )
    indices_reg = []
    for _, grupo_lamina in parcelas_regulares.groupby(
        "grupo_lamina", sort=True, observed=True
    ):
        indices_reg.append(int(rng.choice(grupo_lamina.index.to_numpy())))
    if len(indices_reg) != 8:
        raise RuntimeError("No fue posible formar ocho grupos de lámina de riego.")
    muestra_reg8 = parcelas.loc[indices_reg, ["parcela", "lamina_riego", "rendimiento"]]
    muestra_reg8 = muestra_reg8.sort_values("lamina_riego").reset_index(drop=True)

    muestra_series24 = clima_mensual.tail(24).copy().reset_index(drop=True)
    muestra_series24["periodo"] = np.arange(1, 25)
    muestra_series24["anio"] = muestra_series24["fecha"].dt.year
    muestra_series24["mes"] = muestra_series24["fecha"].dt.month
    muestra_series24["conjunto"] = np.where(
        muestra_series24["periodo"] <= 18, "entrenamiento", "validacion"
    )
    muestra_series24 = muestra_series24[
        ["periodo", "fecha", "anio", "mes", "precipitacion_mm", "conjunto"]
    ]

    # Se guardan todos los archivos en datos/ con texto Unicode legible.
    directorio_datos = Path(__file__).resolve().parent / "datos"
    directorio_datos.mkdir(parents=True, exist_ok=True)
    archivos_csv = {
        "parcelas.csv": parcelas,
        "precip_max_anual.csv": precip_max_anual,
        "clima_mensual.csv": clima_mensual,
        "secado.csv": secado,
        "muestra_eda10.csv": muestra_eda10,
        "muestra_dist10.csv": muestra_dist10,
        "muestra_reg8.csv": muestra_reg8,
        "muestra_series24.csv": muestra_series24,
    }
    for nombre_archivo, datos in archivos_csv.items():
        datos.to_csv(directorio_datos / nombre_archivo, index=False, encoding="utf-8-sig")

    # La huella permite identificar de forma breve este conjunto personalizado.
    suma_rendimiento = parcelas["rendimiento"].sum()
    contenido_huella = f"{CODIGO}|{n_parcelas}|{suma_rendimiento:.2f}"
    huella = hashlib.md5(contenido_huella.encode("utf-8")).hexdigest()[:8].upper()
    metadatos = {
        "codigo": CODIGO,
        "nombre": NOMBRE,
        "cultivo": cultivo,
        "municipio": municipio,
        "n_parcelas": n_parcelas,
        "huella": huella,
    }
    with (directorio_datos / "metadatos.json").open("w", encoding="utf-8") as archivo_json:
        json.dump(metadatos, archivo_json, ensure_ascii=False, indent=2)
        archivo_json.write("\n")

    # Se imprimen la identificación y las cuatro muestras para revisar el resultado.
    print(f"Nombre: {NOMBRE}")
    print(f"Código: {CODIGO}")
    print(f"Cultivo: {cultivo}")
    print(f"Municipio: {municipio}")
    print(f"Huella: {huella}")
    for titulo, muestra in [
        ("Muestra EDA (10 parcelas)", muestra_eda10),
        ("Muestra de distribuciones (10 años)", muestra_dist10),
        ("Muestra de regresión (8 parcelas)", muestra_reg8),
        ("Muestra de series (24 meses)", muestra_series24),
    ]:
        print(f"\n{titulo}:")
        print(muestra.to_string(index=False))


if __name__ == "__main__":
    main()