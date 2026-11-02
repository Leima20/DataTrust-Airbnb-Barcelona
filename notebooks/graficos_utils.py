# -*- coding: utf-8 -*-
"""Funciones de generación automática de gráficos (una por columna, según su
tipo). Módulo compartido entre 00_exploracion_automatica.ipynb y
00b_exploracion_interpretada.ipynb, para no duplicar la lógica en los dos."""
import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

COLOR_GRAFICO = "steelblue"


def tipo_de_columna(serie: pd.Series, umbral_categorias: int = 10) -> str:
    """
    Clasifica una columna en 'fecha', 'categorica' o 'numerica'.

    Args:
        serie (pd.Series): Columna a clasificar.
        umbral_categorias (int): Maximo de valores distintos para tratar una
            columna numerica como categorica.

    Returns:
        str: Uno de 'fecha', 'categorica', 'numerica'.
    """
    if pd.api.types.is_datetime64_any_dtype(serie):
        return "fecha"
    if pd.api.types.is_numeric_dtype(serie) and serie.nunique() > umbral_categorias:
        return "numerica"
    return "categorica"


def graficar_numerica(serie: pd.Series, nombre: str, carpeta: str) -> str:
    """
    Genera y exporta un histograma con boxplot marginal.

    Args:
        serie (pd.Series): Columna numerica a graficar.
        nombre (str): Nombre de la columna.
        carpeta (str): Carpeta donde guardar la imagen.

    Returns:
        str: Ruta del archivo exportado.
    """
    fig, (ax_box, ax_hist) = plt.subplots(
        2, 1, figsize=(6, 4), sharex=True, gridspec_kw={"height_ratios": [1, 4]}
    )
    sns.boxplot(x=serie.dropna(), ax=ax_box, color=COLOR_GRAFICO)
    sns.histplot(serie.dropna(), ax=ax_hist, color=COLOR_GRAFICO)
    ax_box.set(xlabel="")
    ax_hist.set_xlabel(nombre)
    fig.suptitle(f"Distribución de {nombre}")
    fig.tight_layout()

    ruta = os.path.join(carpeta, f"{nombre}_numerica.png")
    fig.savefig(ruta)
    plt.close(fig)
    return ruta


def graficar_categorica(serie: pd.Series, nombre: str, carpeta: str, top_n: int = 10) -> str:
    """
    Genera y exporta un grafico de barras con las categorias mas frecuentes.

    Args:
        serie (pd.Series): Columna categorica a graficar.
        nombre (str): Nombre de la columna.
        carpeta (str): Carpeta donde guardar la imagen.
        top_n (int): Categorias maximas a mostrar.

    Returns:
        str: Ruta del archivo exportado.
    """
    conteo = serie.value_counts(dropna=False).head(top_n)
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=conteo.values, y=conteo.index.astype(str), ax=ax, color=COLOR_GRAFICO)
    ax.set_xlabel("Frecuencia")
    ax.set_ylabel(nombre)
    ax.set_title(f"Categorías más frecuentes de {nombre}")
    fig.tight_layout()

    ruta = os.path.join(carpeta, f"{nombre}_categorica.png")
    fig.savefig(ruta)
    plt.close(fig)
    return ruta


def graficar_fecha(serie: pd.Series, nombre: str, carpeta: str) -> str:
    """
    Genera y exporta un grafico de barras con los anios mas frecuentes.

    Args:
        serie (pd.Series): Columna de tipo fecha a graficar.
        nombre (str): Nombre de la columna.
        carpeta (str): Carpeta donde guardar la imagen.

    Returns:
        str: Ruta del archivo exportado.
    """
    anios = serie.dt.year.value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=anios.index.astype(str), y=anios.values, ax=ax, color=COLOR_GRAFICO)
    ax.set_xlabel("Año")
    ax.set_ylabel("Frecuencia")
    ax.set_title(f"Años más frecuentes de {nombre}")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()

    ruta = os.path.join(carpeta, f"{nombre}_fecha.png")
    fig.savefig(ruta)
    plt.close(fig)
    return ruta


def explorar_dataset(df: pd.DataFrame, carpeta_salida: str = "graficos_exploracion") -> dict:
    """
    Genera y exporta un grafico por columna, eligiendo el tipo automaticamente.

    Args:
        df (pd.DataFrame): Dataset a explorar.
        carpeta_salida (str): Carpeta donde se guardan los graficos.

    Returns:
        dict: Diccionario {nombre_columna: ruta_del_grafico}.
    """
    os.makedirs(carpeta_salida, exist_ok=True)
    rutas = {}
    for columna in df.columns:
        tipo = tipo_de_columna(df[columna])
        if tipo == "numerica":
            rutas[columna] = graficar_numerica(df[columna], columna, carpeta_salida)
        elif tipo == "fecha":
            rutas[columna] = graficar_fecha(df[columna], columna, carpeta_salida)
        else:
            rutas[columna] = graficar_categorica(df[columna], columna, carpeta_salida)
    return rutas
