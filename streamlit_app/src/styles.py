"""Paleta y CSS compartidos por todas las paginas de DataTrust."""
import re

import streamlit as st


def _markdown_bold_a_html(texto: str) -> str:
    """Convierte **negrita** de markdown a <b> real, para usar dentro de divs con unsafe_allow_html."""
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", texto)


def fmt_num(valor, decimales: int = 0) -> str:
    """Formatea un numero en notacion española: '.' para miles, ',' para decimales.
    f'{valor:,.Nf}'.replace(',', '.') se rompe cuando el numero tiene miles Y decimales a la vez
    (ej. 13309.7 -> '13.309.7'), por eso se hace un intercambio de simbolos en dos pasos."""
    texto = f"{valor:,.{decimales}f}"
    return texto.replace(",", "@").replace(".", ",").replace("@", ".")

AZUL_OSCURO = "#0B3954"
AZUL_PETROLEO = "#14506B"
TURQUESA = "#1B998B"
GRIS_FONDO = "#F7F8FA"
GRIS_TEXTO = "#333333"
ROJO_ALERTA = "#D03B3B"
VERDE_OK = "#0CA30C"
AMBAR_PENDIENTE = "#C98A1B"
AZUL_PIZARRA = "#5C7A99"  # identidad de 'calendar' en el codigo de color por tabla -- distinto de AZUL_OSCURO (listings) sin salirse de la paleta sobria de la app

COLOR_CRUDO = ROJO_ALERTA
COLOR_TRATADO = VERDE_OK
COLOR_NEUTRO = AZUL_PETROLEO


def inyectar_css():
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: {GRIS_FONDO}; }}
        h1, h2, h3 {{ color: {AZUL_OSCURO}; }}
        .dt-kicker {{
            color: {TURQUESA}; font-weight: 600; letter-spacing: 0.08em;
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
            background-color: #FDECEC; border: 1px solid {ROJO_ALERTA}; border-radius: 10px;
            padding: 0.8rem 1.1rem; margin-bottom: 0.8rem; font-size: 0.92rem;
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
    st.markdown(f'<div class="dt-caja-pendiente">⏳ <b>Cifra pendiente de validacion:</b> {texto}</div>', unsafe_allow_html=True)


def caja_alerta(texto: str):
    texto = _markdown_bold_a_html(texto)
    st.markdown(f'<div class="dt-caja-alerta">⚠️ {texto}</div>', unsafe_allow_html=True)
