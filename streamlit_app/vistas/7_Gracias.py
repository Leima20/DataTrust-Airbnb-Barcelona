import streamlit as st

from src.styles import AZUL_OSCURO, TURQUESA_CLARO

st.markdown(
    f'<div style="background-color:{AZUL_OSCURO}; margin:-3.5rem -5rem -3.5rem -5rem; '
    f'padding:7rem 5rem; text-align:center; min-height:70vh; display:flex; '
    f'flex-direction:column; align-items:center; justify-content:center;">'
    f'<div style="font-size:8.5rem; font-weight:800; color:white; letter-spacing:0.08em; '
    f'margin-bottom:2.5rem;">GRACIAS</div>'
    f'<div style="font-size:2.1rem; font-style:italic; color:{TURQUESA_CLARO}; '
    f'line-height:1.5; max-width:800px; margin-bottom:1.2rem;">'
    f'"In God we trust; all others must bring data."'
    f'</div>'
    f'<div style="font-size:1.3rem; color:#C7CDD3; font-weight:600;">-- W. Edwards Deming</div>'
    f'</div>',
    unsafe_allow_html=True,
)
