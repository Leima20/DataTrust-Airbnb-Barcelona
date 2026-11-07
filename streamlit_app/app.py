"""DataTrust -- punto de entrada y navegacion.

Ejecutar con: streamlit run app.py (desde la carpeta streamlit_app/)
"""
import streamlit as st

from src.styles import inyectar_css

st.set_page_config(page_title="DataTrust", page_icon="🔎", layout="wide", initial_sidebar_state="expanded")
inyectar_css()

inicio = st.Page("vistas/0_Inicio.py", title="Inicio", icon=":material/home:", default=True)
contexto_pagina = st.Page("vistas/0b_Contexto_proyecto.py", title="Contexto del proyecto", icon=":material/explore:")
auditoria = st.Page("vistas/1_Auditoria_de_calidad.py", title="Auditoría de calidad", icon=":material/search:")
hallazgo_critico = st.Page("vistas/1b_Hallazgo_critico_revenue.py", title="El hallazgo crítico", icon=":material/key:")
diseno = st.Page("vistas/2_Diseno_experimental.py", title="Diseño experimental", icon=":material/science:")
comparacion = st.Page("vistas/3_Comparacion_de_modelos.py", title="Comparación de modelos", icon=":material/bar_chart:")
resultados = st.Page("vistas/4_Resultados_y_robustez.py", title="Resultados y robustez", icon=":material/insights:")
conclusiones = st.Page("vistas/5_Conclusiones_y_recomendaciones.py", title="Conclusiones y recomendaciones", icon=":material/flag:")
metodologia = st.Page("vistas/6_Metodologia_y_limitaciones.py", title="Metodología y limitaciones", icon=":material/menu_book:")

navegacion = st.navigation({
    "DataTrust": [inicio, contexto_pagina],
    "La investigación": [auditoria, hallazgo_critico, diseno, comparacion, resultados],
    "Cierre": [conclusiones, metodologia],
})
navegacion.run()
