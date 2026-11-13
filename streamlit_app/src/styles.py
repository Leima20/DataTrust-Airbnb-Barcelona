"""Paleta y CSS compartidos por todas las páginas de DataTrust."""
import re

import streamlit as st


def _markdown_bold_a_html(texto: str) -> str:
    """Convierte **negrita** de markdown a <b> real, para usar dentro de divs con unsafe_allow_html."""
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", texto)


def fmt_num(valor, decimales: int = 0) -> str:
    """Formatea un número en notación española: '.' para miles, ',' para decimales.
    f'{valor:,.Nf}'.replace(',', '.') se rompe cuando el número tiene miles Y decimales a la vez
    (ej. 13309.7 -> '13.309.7'), por eso se hace un intercambio de símbolos en dos pasos."""
    texto = f"{valor:,.{decimales}f}"
    return texto.replace(",", "@").replace(".", ",").replace("@", ".")

AZUL_NOCHE = "#172B3A"
AZUL_ACERO = "#426A8C"
VIOLETA = "#8064A2"
OCRE_DORADO = "#D5A64A"
TURQUESA = "#268C87"
TURQUESA_TEXTO = "#1E6E69"
TURQUESA_CLARO = "#4FADA8"
OCRE_DORADO_TEXTO = "#8A6219"
COLOR_SENSIBILIDAD_TEXTO = "#636C75"
GRIS_CLARO = "#E9EDF1"
GRIS_HIELO = "#F4F6F8"
BLANCO = "#FFFFFF"
GRIS_OSCURO = "#263746"
GRIS_TEXTO = "#333333"
AZUL_PIZARRA = "#5C7A99"
AZUL_PIZARRA_CLARO = "#A4B8CC"

AZUL_OSCURO = AZUL_NOCHE
AZUL_PETROLEO = AZUL_ACERO
GRIS_FONDO = GRIS_HIELO
AMBAR_PENDIENTE = OCRE_DORADO
AMBAR_ALERTA = OCRE_DORADO

COLOR_CRUDO = AZUL_ACERO
COLOR_D = VIOLETA
COLOR_TRATADO = TURQUESA
COLOR_SENSIBILIDAD = "#8A95A1"
COLOR_NEUTRO = AZUL_NOCHE


def inyectar_css():
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: {GRIS_FONDO}; }}
        h1, h2, h3 {{ color: {AZUL_OSCURO}; }}
        .stApp p, .stApp li, .stMarkdown {{ font-size: 1.05rem; line-height: 1.55; }}
        .dt-kicker {{
            color: {TURQUESA_TEXTO}; font-weight: 600; letter-spacing: 0.08em;
            text-transform: uppercase; font-size: 0.8rem; margin-bottom: 0.2rem;
        }}
        .dt-caja {{
            background-color: white; border: 1px solid #E3E6EA; border-radius: 10px;
            padding: 1rem 1.2rem; margin-bottom: 0.8rem;
        }}
        .dt-caja-pendiente {{
            background-color: #FFF8EC; border: 1px solid {AMBAR_PENDIENTE}; border-radius: 10px;
            padding: 0.8rem 1.1rem; margin-bottom: 0.8rem; font-size: 0.92rem;
        }}
        .dt-caja-alerta {{
            background-color: #2A3F52; border: 1px solid {OCRE_DORADO}; border-radius: 10px;
            padding: 0.8rem 1.1rem; margin-bottom: 0.8rem; font-size: 0.92rem; color: {GRIS_CLARO};
        }}
        .dt-nota-exposicion {{
            background-color: #EFF7F6; border-left: 4px solid {TURQUESA};
            padding: 0.8rem 1.1rem; margin-top: 0.6rem; font-size: 0.9rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def kicker(texto: str):
    st.markdown(f'<div class="dt-kicker">{texto}</div>', unsafe_allow_html=True)


def caja_pendiente(texto: str):
    texto = _markdown_bold_a_html(texto)
    st.markdown(f'<div class="dt-caja-pendiente">⏳ <b>Cifra pendiente de validación:</b> {texto}</div>', unsafe_allow_html=True)


def caja_alerta(texto: str):
    texto = _markdown_bold_a_html(texto)
    st.markdown(f'<div class="dt-caja-alerta">⚠️ {texto}</div>', unsafe_allow_html=True)
