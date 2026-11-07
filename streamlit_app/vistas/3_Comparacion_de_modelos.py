import pandas as pd
import streamlit as st

from src.data_loader import cargar_modelo
from src.styles import kicker, fmt_num, COLOR_CRUDO, COLOR_D, COLOR_TRATADO, COLOR_NEUTRO, AMBAR_PENDIENTE, AZUL_PETROLEO, OCRE_DORADO_TEXTO
from src.charts import barras_r2_modelos

modelo = cargar_modelo()
versiones = modelo.get("versiones", {})

kicker("Página 6 de 9")
st.title("Comparación de modelos")
st.markdown(
    "Con las 4 versiones ya entrenadas (página anterior), la comparación más intuitiva es mirar el R² "
    "de cada una sobre su propia población de test. Es la forma más común de comparar modelos -- pero "
    "también la que puede engañar, como se investiga en la siguiente página."
)

st.markdown("### ¿Cómo evaluamos los modelos?")
col_r2, col_mae = st.columns(2)
with col_r2:
    st.markdown(
        f"""
        <div style="background-color: #ffffff; border-top: 4px solid {AZUL_PETROLEO}; border-radius: 8px; padding: 0.8rem 1rem; height: 100%;">
            <div style="color: {AZUL_PETROLEO}; font-weight: 700; font-size: 0.95rem;">R² -- capacidad explicativa</div>
            <div style="font-size: 0.85rem; color: #444; line-height: 1.4; margin: 0.3rem 0;">
                Qué proporción de la variabilidad del ingreso estimado explica el modelo, frente a predecir siempre el promedio.
            </div>
            <div style="font-size: 0.75rem; color: {AZUL_PETROLEO}; font-weight: 600;">Más alto = mejor (máximo 1)</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with col_mae:
    st.markdown(
        f"""
        <div style="background-color: #ffffff; border-top: 4px solid {OCRE_DORADO_TEXTO}; border-radius: 8px; padding: 0.8rem 1rem; height: 100%;">
            <div style="color: {OCRE_DORADO_TEXTO}; font-weight: 700; font-size: 0.95rem;">MAE -- error medio absoluto (€)</div>
            <div style="font-size: 0.85rem; color: #444; line-height: 1.4; margin: 0.3rem 0;">
                Cuánto se equivoca el modelo en promedio, en euros, al predecir sobre las filas de prueba.
            </div>
            <div style="font-size: 0.75rem; color: {OCRE_DORADO_TEXTO}; font-weight: 600;">Más bajo = mejor</div>
        </div>
        """,
        unsafe_allow_html=True
    )
st.caption(
    "Un R² de 0,469 no significa '46,9% de precisión' -- significa que el modelo explica "
    "aproximadamente ese porcentaje de la variabilidad observada en el conjunto de prueba. Y los "
    "valores usados como referencia son estimaciones de Inside Airbnb, no ingresos reales verificados."
)

st.markdown("---")

st.markdown("### Lógica metodológica de las comparaciones")

col_c1, col_c2, col_c3 = st.columns(3)

with col_c1:
    st.markdown(
        """
        <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8rem 0.9rem; height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                <span style="font-size: 0.7rem; color: #666; font-weight: 600; text-transform: uppercase;">Comparación 01</span>
                <span style="background-color: #E6E1EC; color: #5A4A75; font-size: 0.68rem; font-weight: 600; padding: 0.1rem 0.4rem; border-radius: 4px;">Misma población</span>
            </div>
            <div style="font-weight: 700; font-size: 0.95rem; color: #31333F; margin-bottom: 0.3rem;">A vs. D</div>
            <div style="font-size: 0.8rem; color: #444; margin-bottom: 0.35rem; line-height: 1.4;">
                <b style="color: #5A4A75;">Problema:</b> CRUDO y TRATADO-A cambian dos cosas a la vez (qué filas se evalúan y cómo se construyen las variables) — si solo los comparas, no sabes cuál de las dos causa la diferencia.
            </div>
            <div style="font-size: 0.8rem; color: #444; margin-bottom: 0.35rem; line-height: 1.4;">
                <b style="color: #5A4A75;">Solución:</b> el Modelo D usa las mismas filas que CRUDO, pero construye las variables como TRATADO — así aísla un solo factor.
            </div>
            <div style="font-size: 0.75rem; color: #5A4A75; font-weight: 600;">Resultado real: D≈A → la población manda, no las variables</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_c2:
    st.markdown(
        """
        <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8rem 0.9rem; height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                <span style="font-size: 0.7rem; color: #666; font-weight: 600; text-transform: uppercase;">Comparación 02</span>
                <span style="background-color: #dbe5f1; color: #1f3864; font-size: 0.68rem; font-weight: 600; padding: 0.1rem 0.4rem; border-radius: 4px;">Pob. distintas</span>
            </div>
            <div style="font-weight: 700; font-size: 0.95rem; color: #31333F; margin-bottom: 0.3rem;">A vs. B</div>
            <div style="font-size: 0.8rem; color: #444; margin-bottom: 0.35rem; line-height: 1.4;">
                <b style="color: #1f3864;">Problema:</b> A vs. B es la comparación más intuitiva -- "¿el modelo tratado es mejor?" -- pero cambia la población Y las variables a la vez, así que por sí sola no dice cuál de las dos causa el resultado.
            </div>
            <div style="font-size: 0.8rem; color: #444; margin-bottom: 0.35rem; line-height: 1.4;">
                <b style="color: #1f3864;">Solución:</b> se interpreta junto con A vs. D -- si ahí ya se vio que las variables casi no pesan (Δ=0,004), lo que quede en la diferencia A-B tiene que venir sobre todo de la población.
            </div>
            <div style="font-size: 0.75rem; color: #1f3864; font-weight: 600;">Resultado real: R² baja de 0,469 a 0,440 (Δ=0,029, 7× mayor) -- sobre todo por la población</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_c3:
    st.markdown(
        """
        <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8rem 0.9rem; height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                <span style="font-size: 0.7rem; color: #666; font-weight: 600; text-transform: uppercase;">Comparación 03</span>
                <span style="background-color: #fff2cc; color: #806000; font-size: 0.68rem; font-weight: 600; padding: 0.1rem 0.4rem; border-radius: 4px;">n = 426</span>
            </div>
            <div style="font-weight: 700; font-size: 0.95rem; color: #31333F; margin-bottom: 0.3rem;">Muestra común</div>
            <div style="font-size: 0.8rem; color: #444; margin-bottom: 0.35rem; line-height: 1.4;">
                <b style="color: #806000;">Problema:</b> A, D y B se evalúan cada uno sobre su propio test (filas distintas) -- comparar sus R² directamente no es justo. Un primer intento de comparación "controlada" resultó tener fuga de datos: el 80% de esas filas ya estaban en el entrenamiento de A/D.
            </div>
            <div style="font-size: 0.8rem; color: #444; margin-bottom: 0.35rem; line-height: 1.4;">
                <b style="color: #806000;">Solución:</b> construir una muestra de 426 filas que estén en el test de los tres modelos a la vez y fuera del entrenamiento de los tres -- garantizado sin fuga, los tres se evalúan sobre exactamente las mismas filas.
            </div>
            <div style="font-size: 0.75rem; color: #806000; font-weight: 600;">Resultado real: A 0,347 → D 0,389 → B 0,450 -- progresión clara, B gana limpio</div>
        </div>
        """,
        unsafe_allow_html=True
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
r2_b = versiones.get("B_tratado_criterio_A", {}).get("r2", 0)
st.markdown(
    f'<div style="background-color: #f8f9fa; border: 1px solid #e0e0e0; border-left: 4px solid #14506B; border-radius: 8px; padding: 1rem 1.2rem; margin: 1rem 0;">'
    f'<div style="font-size: 0.75rem; color: #666; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.2rem;">Hallazgo preliminar</div>'
    f'<div style="font-size: 1.05rem; font-weight: 700; color: #31333F; margin-bottom: 0.6rem;">Cambiar solo las variables apenas modifica el R² -- cambiar también la población, sí</div>'

    f'<div style="font-size: 0.78rem; color: #666; font-weight: 600; margin-bottom: 0.3rem;">Solo variables (misma población)</div>'
    f'<div style="display: flex; flex-wrap: wrap; gap: 1.5rem; align-items: center; margin-bottom: 0.8rem;">'
    f'<div><span style="font-size: 0.82rem; color: #555;">Modelo A:</span> '
    f'<strong style="font-size: 1.05rem; color: {COLOR_CRUDO};">{fmt_num(r2_a, 3)}</strong></div>'
    f'<div style="color: #888; font-weight: bold;">vs</div>'
    f'<div><span style="font-size: 0.82rem; color: #555;">Modelo D:</span> '
    f'<strong style="font-size: 1.05rem; color: {COLOR_D};">{fmt_num(r2_d, 3)}</strong></div>'
    f'<div style="background-color: #E9EDF1; color: {COLOR_NEUTRO}; padding: 0.15rem 0.6rem; border-radius: 4px; font-size: 0.82rem; font-weight: 600;">'
    f'Δ = {fmt_num(r2_a - r2_d, 3)}</div>'
    f'</div>'

    f'<div style="font-size: 0.78rem; color: #666; font-weight: 600; margin-bottom: 0.3rem;">Población + variables (A vs. B)</div>'
    f'<div style="display: flex; flex-wrap: wrap; gap: 1.5rem; align-items: center; margin-bottom: 0.6rem;">'
    f'<div><span style="font-size: 0.82rem; color: #555;">Modelo A:</span> '
    f'<strong style="font-size: 1.05rem; color: {COLOR_CRUDO};">{fmt_num(r2_a, 3)}</strong></div>'
    f'<div style="color: #888; font-weight: bold;">vs</div>'
    f'<div><span style="font-size: 0.82rem; color: #555;">Modelo B:</span> '
    f'<strong style="font-size: 1.05rem; color: {COLOR_TRATADO};">{fmt_num(r2_b, 3)}</strong></div>'
    f'<div style="background-color: #FBEED6; color: {AMBAR_PENDIENTE}; padding: 0.15rem 0.6rem; border-radius: 4px; font-size: 0.82rem; font-weight: 600;">'
    f'Δ = {fmt_num(r2_a - r2_b, 3)} ({fmt_num((r2_a - r2_b) / (r2_a - r2_d), 1)}× la diferencia de arriba)</div>'
    f'</div>'

    f'<div style="font-size: 0.83rem; color: #555; border-top: 1px solid #eaeaeb; padding-top: 0.5rem; margin-top: 0.4rem;">'
    f'<em>Las variables casi no pesan (Δ=0,004); la diferencia grande viene al cambiar también la población. '
    f'<b>Que A salga más alto aquí NO significa que sea el mejor modelo</b> -- son poblaciones distintas, no '
    f'es una comparación justa. En la comparación válida (muestra común de 426 filas, siguiente página), '
    f'el resultado se invierte: B gana claramente a A.</em></div>'
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
        "MAE modelo de referencia (predecir mediana)": fmt_num(v["baseline_mae"], 1),
    })
with st.expander("Ver tabla de métricas (MAE y R² por modelo)"):
    st.dataframe(pd.DataFrame(filas_cortas), width="stretch", hide_index=True)
with st.expander("Ver métricas y detalle técnico"):
    st.dataframe(pd.DataFrame(filas_completas), width="stretch", hide_index=True)

st.markdown("---")
st.markdown("### ¿Random Forest aporta algo más que una regla trivial?")
st.markdown(
    "En las tres versiones, el MAE de Random Forest está muy por debajo del MAE de un modelo de "
    "referencia que simplemente predice la mediana de ingresos del entrenamiento, sin mirar ninguna "
    "característica del alojamiento."
)
c1, c2, c3 = st.columns(3)
for col, clave in zip([c1, c2, c3], ["A_crudo", "D_variables_tratadas_poblacion_cruda", "B_tratado_criterio_A"]):
    v = versiones[clave]
    mejora_pct = (v["baseline_mae"] - v["mae"]) / v["baseline_mae"] * 100
    with col:
        st.markdown(
            f"""
            <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8rem 1rem;">
                <div style="font-size: 0.8rem; color: #666; font-weight: 600; margin-bottom: 0.3rem;">{v["nombre_display"]}</div>
                <div style="font-size: 1.3rem; font-weight: 700; color: #31333F;">{fmt_num(v["mae"], 0)} €</div>
                <div style="font-size: 0.75rem; color: #888; margin-bottom: 0.3rem;">error del modelo (MAE, más bajo = mejor)</div>
                <div style="background-color: {AZUL_PETROLEO}1A; color: {AZUL_PETROLEO}; display: inline-block; padding: 0.1rem 0.5rem; border-radius: 4px; font-size: 0.78rem; font-weight: 600;">
                    ↓ {fmt_num(mejora_pct, 1)}% menos error que el modelo de referencia
                </div>
                <div style="font-size: 0.72rem; color: #999; margin-top: 0.3rem;">
                    modelo de referencia (predecir siempre la mediana): {fmt_num(v["baseline_mae"], 0)} €
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.caption(
    "El chequeo de sensibilidad (criterio de imputación por barrio vs. capacidad) se investiga en la "
    "página 'Resultados y robustez', junto con el resto de comprobaciones de solidez."
)
