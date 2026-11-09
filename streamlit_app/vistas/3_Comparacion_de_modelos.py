import pandas as pd
import streamlit as st

from src.data_loader import cargar_modelo
from src.styles import (
    kicker, fmt_num, COLOR_CRUDO, COLOR_TRATADO, COLOR_NEUTRO, AMBAR_PENDIENTE,
    AZUL_PETROLEO, OCRE_DORADO_TEXTO,
)
from src.charts import barras_r2_modelos

modelo = cargar_modelo()
versiones = modelo.get("versiones", {})

kicker("Página 6 de 9")
st.title("Evaluación de los modelos")

st.markdown("### ¿Cómo evaluamos los modelos?")
col_r2, col_mae = st.columns(2)
with col_r2:
    st.markdown(
        f"""
        <div style="background-color: #ffffff; border-left: 4px solid {AZUL_PETROLEO}; border-radius: 8px; padding: 0.7rem 1rem; display: flex; align-items: center; gap: 0.9rem;">
            <div style="font-size: 1.7rem; font-weight: 800; color: {AZUL_PETROLEO};">R²</div>
            <div style="font-size: 0.85rem; color: #444; line-height: 1.35;">
                Capacidad explicativa.<br><span style="color: {AZUL_PETROLEO}; font-weight: 700;">Más alto = mejor</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.caption(
        "Número entre 0 y 1 que mide cuánto explica el modelo de la variación del ingreso estimado (la "
        "variable a predecir), a partir de las variables usadas para predecirlo -- no es un porcentaje "
        "de aciertos."
    )
with col_mae:
    st.markdown(
        f"""
        <div style="background-color: #ffffff; border-left: 4px solid {OCRE_DORADO_TEXTO}; border-radius: 8px; padding: 0.7rem 1rem; display: flex; align-items: center; gap: 0.9rem;">
            <div style="font-size: 1.7rem; font-weight: 800; color: {OCRE_DORADO_TEXTO};">MAE</div>
            <div style="font-size: 0.85rem; color: #444; line-height: 1.35;">
                Error medio absoluto, en €.<br><span style="color: {OCRE_DORADO_TEXTO}; font-weight: 700;">Más bajo = mejor</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.caption(
        "Diferencia media, en valor absoluto, entre lo que predice el modelo y el ingreso estimado real, "
        "sobre el conjunto de prueba."
    )
st.markdown("---")

opciones = {
    "A — CRUDO": "A_crudo",
    "D — Variables tratadas, población cruda": "D_variables_tratadas_poblacion_cruda",
    "B — TRATADO (criterio A)": "B_tratado_criterio_A",
    "Chequeo de sensibilidad (criterio B)": "TRATADO_criterio_B_barrio",
}
puntos_color = {
    "A — CRUDO": "🔵",
    "D — Variables tratadas, población cruda": "🟣",
    "B — TRATADO (criterio A)": "🔷",
    "Chequeo de sensibilidad (criterio B)": "🟡",
}
color_por_clave = {
    "A_crudo": COLOR_CRUDO,
    "D_variables_tratadas_poblacion_cruda": COLOR_NEUTRO,
    "B_tratado_criterio_A": COLOR_TRATADO,
    "TRATADO_criterio_B_barrio": AMBAR_PENDIENTE,
}

st.markdown(
    '<div style="font-size:1.15rem; font-weight:700; color:#31333F; margin-bottom:0.5rem;">'
    'Vista preliminar: cada modelo sobre su propio conjunto de prueba.</div>',
    unsafe_allow_html=True,
)
seleccion = []
cols_check = st.columns(len(opciones))
for col, (nombre, clave) in zip(cols_check, opciones.items()):
    marcado = col.checkbox(f"{puntos_color[nombre]} {nombre}", value=(clave != "TRATADO_criterio_B_barrio"))
    if marcado:
        seleccion.append(nombre)

etiquetas_extra = {
    "B_tratado_criterio_A": "<br>(variables y población tratadas)",
}

if seleccion:
    claves = [opciones[s] for s in seleccion]
    nombres = [versiones[c]["nombre_display"] + etiquetas_extra.get(c, "") for c in claves]
    r2s = [versiones[c]["r2"] for c in claves]
    colores = [color_por_clave[c] for c in claves]
    st.plotly_chart(
        barras_r2_modelos(nombres, r2s, colores, titulo="R² en el conjunto de prueba de cada modelo"),
        width="stretch",
    )

st.markdown("### Tabla de métricas (población propia de cada modelo)")
filas_completas = []
for clave, v in versiones.items():
    filas_completas.append({
        "Modelo": v["nombre_display"],
        "n (anuncios en el dataset)": fmt_num(v["n"]),
        "n (test, usado para MAE/RMSE/R²)": fmt_num(v.get("n_test_propio", 0)),
        "MAE (€)": fmt_num(v["mae"], 1),
        "RMSE (€)": fmt_num(v["rmse"], 1),
        "R²": fmt_num(v["r2"], 3),
        "MAE modelo de referencia (predecir mediana)": fmt_num(v["referencia_mae"], 1),
    })
with st.expander("Ver métricas y detalle técnico"):
    st.dataframe(pd.DataFrame(filas_completas), width="stretch", hide_index=True)

st.markdown("---")
st.markdown("### ¿Random Forest aporta algo más que una regla trivial?")
st.markdown(
    "El MAE de Random Forest está muy por debajo del MAE de un modelo de referencia que simplemente "
    "predice la mediana de ingresos del entrenamiento, sin mirar ninguna característica del alojamiento."
)
filas_referencia = []
for clave in ["A_crudo", "D_variables_tratadas_poblacion_cruda", "B_tratado_criterio_A", "TRATADO_criterio_B_barrio"]:
    v = versiones[clave]
    mejora_pct = (v["referencia_mae"] - v["mae"]) / v["referencia_mae"] * 100
    filas_referencia.append({
        "Versión": v["nombre_display"],
        "MAE Random Forest (€)": fmt_num(v["mae"], 0),
        "MAE referencia (€)": fmt_num(v["referencia_mae"], 0),
        "Reducción del error": f"↓ {fmt_num(mejora_pct, 1)}%",
    })
st.dataframe(pd.DataFrame(filas_referencia), width="stretch", hide_index=True)
