"""DataTrust -- punto de entrada y navegacion.

Ejecutar con: streamlit run app.py (desde la carpeta streamlit_app/)
"""
import streamlit as st

from src.styles import inyectar_css

st.set_page_config(page_title="DataTrust", page_icon="🔎", layout="wide", initial_sidebar_state="expanded")
inyectar_css()

inicio = st.Page("pages/0_Inicio.py", title="Inicio", icon="🏠", default=True)
contexto_pagina = st.Page("pages/0b_Contexto_proyecto.py", title="Contexto del proyecto", icon="🧭")
auditoria = st.Page("pages/1_Auditoria_de_calidad.py", title="Auditoría de calidad", icon="🔍")
hallazgo_critico = st.Page("pages/1b_Hallazgo_critico_revenue.py", title="El hallazgo crítico", icon="🎯")
diseno = st.Page("pages/2_Diseno_experimental.py", title="Diseño experimental", icon="🧩")
comparacion = st.Page("pages/3_Comparacion_de_modelos.py", title="Comparación de modelos", icon="📊")
resultados = st.Page("pages/4_Resultados_y_robustez.py", title="Resultados y robustez", icon="📈")
conclusiones = st.Page("pages/5_Conclusiones_y_recomendaciones.py", title="Conclusiones y recomendaciones", icon="✅")
metodologia = st.Page("pages/6_Metodologia_y_limitaciones.py", title="Metodología y limitaciones", icon="📚")

navegacion = st.navigation({
    "DataTrust": [inicio, contexto_pagina],
    "La investigación": [auditoria, hallazgo_critico, diseno, comparacion, resultados],
    "Cierre": [conclusiones, metodologia],
})
navegacion.run()
