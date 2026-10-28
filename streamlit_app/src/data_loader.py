"""Carga de los datos precalculados que alimentan la app.

Todos los numeros vienen de notebooks/06_modelo_ml.ipynb, de
00_ficha_maestra.md, o de una comprobacion en vivo contra los CSV de
data/airbnb_bcn(_curado)/ -- ver el campo "fuente" en cada JSON.
No se recalculan modelos ni se leen los CSV de millones de filas en
tiempo de ejecucion de la app.
"""
from pathlib import Path
import json

import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


@st.cache_data
def cargar_json(nombre: str) -> dict:
    ruta = DATA_DIR / nombre
    if not ruta.exists():
        return {}
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def cargar_calidad() -> dict:
    return cargar_json("calidad_resumen.json")


def cargar_impacto_negocio() -> dict:
    return cargar_json("impacto_negocio.json")


def cargar_modelo() -> dict:
    return cargar_json("modelo_resultados.json")


def cargar_geografia_distrito() -> dict:
    return cargar_json("geografia_distrito.json")


def cargar_contexto() -> dict:
    return cargar_json("contexto_proyecto.json")


def cargar_simulacion_valores() -> dict:
    return cargar_json("simulacion_5000_valores.json")


@st.cache_data
def cargar_geojson_barrios() -> dict:
    ruta = DATA_DIR / "neighbourhoods.geojson"
    if not ruta.exists():
        return {}
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)
