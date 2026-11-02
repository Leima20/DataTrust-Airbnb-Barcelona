import pandas as pd
import streamlit as st

from src.data_loader import cargar_modelo
from src.styles import kicker, fmt_num, COLOR_CRUDO, COLOR_TRATADO, COLOR_NEUTRO, AMBAR_PENDIENTE
from src.charts import barras_r2_modelos

modelo = cargar_modelo()
versiones = modelo.get("versiones", {})

kicker("Pagina 6 de 9")
st.title("Comparación de modelos")
st.markdown(
    "Con las 4 versiones ya entrenadas (página anterior), la comparación más intuitiva es mirar el R² "
    "de cada una sobre su propia población de test. Es la forma más común de comparar modelos -- pero "
    "también la que puede engañar, como se investiga en la siguiente página."
)

opciones = {
    "A — CRUDO": "A_crudo",
    "D — Variables tratadas, población cruda": "D_variables_tratadas_poblacion_cruda",
    "B — TRATADO (criterio A)": "B_tratado_criterio_A",
    "Chequeo de sensibilidad (criterio B)": "TRATADO_criterio_B_barrio",
}
puntos_color = {
    "A — CRUDO": "🔴",
    "D — Variables tratadas, población cruda": "🔵",
    "B — TRATADO (criterio A)": "🟢",
    "Chequeo de sensibilidad (criterio B)": "🟡",
}
color_por_clave = {
    "A_crudo": COLOR_CRUDO,
    "D_variables_tratadas_poblacion_cruda": COLOR_NEUTRO,
    "B_tratado_criterio_A": COLOR_TRATADO,
    "TRATADO_criterio_B_barrio": AMBAR_PENDIENTE,
}

st.markdown("**Selecciona qué versiones mostrar**")
seleccion = []
cols_check = st.columns(len(opciones))
for col, (nombre, clave) in zip(cols_check, opciones.items()):
    marcado = col.checkbox(f"{puntos_color[nombre]} {nombre}", value=(clave != "TRATADO_criterio_B_barrio"))
    if marcado:
        seleccion.append(nombre)

if seleccion:
    claves = [opciones[s] for s in seleccion]
    nombres = [versiones[c]["nombre_display"] for c in claves]
    r2s = [versiones[c]["r2"] for c in claves]
    colores = [color_por_clave[c] for c in claves]
    st.plotly_chart(barras_r2_modelos(nombres, r2s, colores), width="stretch")

r2_a = versiones.get("A_crudo", {}).get("r2", 0)
r2_d = versiones.get("D_variables_tratadas_poblacion_cruda", {}).get("r2", 0)
st.markdown(
    f'<div style="background-color: #f8f9fa; border: 1px solid #e0e0e0; border-left: 4px solid #14506B; border-radius: 8px; padding: 1rem 1.2rem; margin: 1rem 0;">'
    f'<div style="font-size: 0.75rem; color: #666; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.2rem;">Hallazgo preliminar</div>'
    f'<div style="font-size: 1.05rem; font-weight: 700; color: #31333F; margin-bottom: 0.6rem;">Cambiar las variables apenas modifica el R²</div>'
    f'<div style="display: flex; flex-wrap: wrap; gap: 1.5rem; align-items: center; margin-bottom: 0.6rem;">'
    f'<div><span style="font-size: 0.82rem; color: #555;">Modelo A:</span> '
    f'<strong style="font-size: 1.05rem; color: #DC3545;">{fmt_num(r2_a, 3)}</strong></div>'
    f'<div style="color: #888; font-weight: bold;">vs</div>'
    f'<div><span style="font-size: 0.82rem; color: #555;">Modelo D:</span> '
    f'<strong style="font-size: 1.05rem; color: #D4A017;">{fmt_num(r2_d, 3)}</strong></div>'
    f'<div style="background-color: #e2f0d9; color: #385723; padding: 0.15rem 0.6rem; border-radius: 4px; font-size: 0.82rem; font-weight: 600;">'
    f'Δ = {fmt_num(r2_a - r2_d, 3)} (misma población)</div>'
    f'</div>'
    f'<div style="font-size: 0.83rem; color: #555; border-top: 1px solid #eaeaeb; padding-top: 0.5rem; margin-top: 0.4rem;">'
    f'<em>El efecto real (si aguanta un análisis riguroso) se investiga en la siguiente página.</em></div>'
    f'</div>',
    unsafe_allow_html=True
)

n_ad = versiones.get("A_crudo", {}).get("n", 0)
n_test_ad = versiones.get("A_crudo", {}).get("n_test_propio", 0)
n_b = versiones.get("B_tratado_criterio_A", {}).get("n", 0)
n_test_b = versiones.get("B_tratado_criterio_A", {}).get("n_test_propio", 0)
st.markdown(
    f'<div style="background-color: #fcf8e3; border: 1px solid #faebcc; border-left: 4px solid #8a6d3b; border-radius: 6px; padding: 0.9rem 1.1rem; margin: 1rem 0; color: #8a6d3b;">'
    f'<div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 0.4rem; color: #8a6d3b;">⚠️ Advertencia metodológica: Estos R² NO son directamente comparables</div>'
    f'<div style="font-size: 0.88rem; line-height: 1.4; margin-bottom: 0.5rem; color: #555;">Cada modelo opera sobre una población base y un conjunto de prueba distintos, por lo que una comparativa directa no es rigurosa:</div>'
    f'<ul style="margin: 0 0 0.5rem 1.2rem; padding: 0; font-size: 0.85rem; line-height: 1.4; color: #555;">'
    f'<li><b>Modelos A y D:</b> {fmt_num(n_ad)} filas base ➔ Test de {fmt_num(n_test_ad)} filas.</li>'
    f'<li><b>Modelo B:</b> {fmt_num(n_b)} filas base ➔ Test de {fmt_num(n_test_b)} filas.</li>'
    f'</ul>'
    f'<div style="font-size: 0.85rem; font-style: italic; border-top: 1px solid #faebcc; padding-top: 0.4rem; margin-top: 0.4rem; color: #666;">'
    f"La comparación válida y el análisis de robustez se desarrollan en la página <b>'Resultados y robustez'</b>.</div>"
    f'</div>',
    unsafe_allow_html=True
)

st.markdown("### Tabla de métricas (población propia de cada modelo)")
filas_cortas = []
filas_completas = []
for clave, v in versiones.items():
    filas_cortas.append({
        "Modelo": v["nombre_display"],
        "MAE (€)": fmt_num(v["mae"], 1),
        "R²": fmt_num(v["r2"], 3),
    })
    filas_completas.append({
        "Modelo": v["nombre_display"],
        "n (anuncios en el dataset)": fmt_num(v["n"]),
        "n (test, usado para MAE/RMSE/R²)": fmt_num(v.get("n_test_propio", 0)),
        "MAE (€)": fmt_num(v["mae"], 1),
        "RMSE (€)": fmt_num(v["rmse"], 1),
        "R²": fmt_num(v["r2"], 3),
        "Baseline MAE (predecir mediana)": fmt_num(v["baseline_mae"], 1),
    })
st.dataframe(pd.DataFrame(filas_cortas), width="stretch", hide_index=True)
with st.expander("Ver métricas y detalle técnico"):
    st.dataframe(pd.DataFrame(filas_completas), width="stretch", hide_index=True)

st.markdown("---")
st.markdown("### ¿Random Forest aporta algo más que una regla trivial?")
st.markdown(
    "En las tres versiones, el MAE de Random Forest esta muy por debajo del MAE de un modelo de "
    "referencia que simplemente predice la mediana de ingresos del entrenamiento, sin mirar ninguna "
    "caracteristica del alojamiento."
)
c1, c2, c3 = st.columns(3)
for col, clave in zip([c1, c2, c3], ["A_crudo", "D_variables_tratadas_poblacion_cruda", "B_tratado_criterio_A"]):
    v = versiones[clave]
    col.metric(v["nombre_display"], f'{v["mae"]:,.0f} € (RF)'.replace(",", "."),
               f'vs. {v["baseline_mae"]:,.0f} € (mediana)'.replace(",", "."), delta_color="inverse")

st.caption(
    "El chequeo de sensibilidad (criterio de imputación por barrio vs. capacidad) se investiga en la "
    "página 'Resultados y robustez', junto con el resto de comprobaciones de solidez."
)
