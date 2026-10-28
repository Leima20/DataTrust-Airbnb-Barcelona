import pandas as pd
import streamlit as st

from src.data_loader import cargar_modelo
from src.styles import kicker, caja_alerta, fmt_num, COLOR_CRUDO, COLOR_TRATADO, COLOR_NEUTRO, AMBAR_PENDIENTE
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

st.markdown("**Selecciona que versiones comparar** (cada una se evalua sobre su PROPIA poblacion de test)")
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

caja_alerta(
    "**Estos R² NO son directamente comparables entre si** -- cada modelo parte de una poblacion base "
    "distinta (13.355 filas para A y D, 10.669 para B) y hace su propio `train_test_split` sobre ella, "
    "asi que ademas se evalua sobre un conjunto de test distinto (2.671 filas para A y D, 2.134 para B). "
    "La comparacion valida -- y si estas diferencias aguantan un analisis riguroso -- se investiga en "
    "la pagina 'Resultados y robustez'."
)

st.markdown("### Tabla de metricas (población propia de cada modelo)")
filas = []
for clave, v in versiones.items():
    filas.append({
        "Modelo": v["nombre_display"],
        "n (anuncios en el dataset)": fmt_num(v["n"]),
        "n (test, usado para MAE/RMSE/R²)": fmt_num(v.get("n_test_propio", 0)),
        "MAE (€)": fmt_num(v["mae"], 1),
        "RMSE (€)": fmt_num(v["rmse"], 1),
        "R²": fmt_num(v["r2"], 3),
        "Baseline MAE (predecir mediana)": fmt_num(v["baseline_mae"], 1),
    })
st.dataframe(pd.DataFrame(filas), width="stretch", hide_index=True)

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

st.markdown("---")
st.markdown("### Chequeo de sensibilidad: ¿importa el criterio de imputación?")
diff = versiones.get("TRATADO_criterio_B_barrio", {}).get("diferencia_vs_A", {})
if diff:
    st.markdown(
        f"Reimputar `bedrooms`/`bathrooms`/`beds` por mediana de **barrio** en vez de por **capacidad** "
        f"cambia el MAE en solo **{fmt_num(diff.get('mae_eur', 0), 1)} € "
        f"({fmt_num(diff.get('mae_pct', 0), 2)}% relativo)** y el R² en "
        f"**{fmt_num(diff.get('r2', 0), 3)}**. La conclusion del modelo no depende de cual de los dos "
        "criterios razonables se use."
    )
