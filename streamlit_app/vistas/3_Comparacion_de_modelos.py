import pandas as pd
import streamlit as st

from src.data_loader import cargar_modelo
from src.styles import kicker, fmt_num, COLOR_CRUDO, COLOR_D, COLOR_TRATADO, COLOR_NEUTRO, AMBAR_PENDIENTE, AZUL_PETROLEO, OCRE_DORADO_TEXTO, COLOR_SENSIBILIDAD
from src.charts import barras_r2_modelos

modelo = cargar_modelo()
versiones = modelo.get("versiones", {})

kicker("Página 6 de 9")
st.title("Comparación de modelos")

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

st.markdown("### Lógica metodológica de las comparaciones")

st.markdown(
    f"""
    <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem 1.1rem;">
      <svg width="100%" height="460" viewBox="0 0 1150 460" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="flecha_cm" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" fill="#aaa" />
          </marker>
        </defs>
        <text x="110" y="20" text-anchor="middle" fill="#888" font-size="11" font-weight="600" letter-spacing="0.5" font-family="Helvetica">1. PUNTO DE PARTIDA</text>
        <text x="560" y="20" text-anchor="middle" fill="#888" font-size="11" font-weight="600" letter-spacing="0.5" font-family="Helvetica">2. AÍSLA UN FACTOR A LA VEZ</text>
        <text x="990" y="20" text-anchor="middle" fill="#888" font-size="11" font-weight="600" letter-spacing="0.5" font-family="Helvetica">3. COMPARACIÓN CONTROLADA</text>
        <rect x="20" y="170" width="180" height="110" rx="10" fill="{COLOR_CRUDO}" />
        <text x="110" y="220" text-anchor="middle" fill="white" font-size="14" font-weight="700" font-family="Helvetica">A -- CRUDO</text>
        <text x="110" y="238" text-anchor="middle" fill="white" font-size="11" font-family="Helvetica" opacity="0.9">n = 13.355</text>
        <text x="110" y="256" text-anchor="middle" fill="white" font-size="10" font-family="Helvetica" opacity="0.8">punto de partida</text>
        <line x1="200" y1="195" x2="430" y2="85" stroke="#aaa" stroke-width="2" marker-end="url(#flecha_cm)" />
        <line x1="200" y1="225" x2="430" y2="225" stroke="#aaa" stroke-width="2" marker-end="url(#flecha_cm)" />
        <rect x="430" y="35" width="260" height="100" rx="10" fill="{COLOR_D}" />
        <text x="560" y="60" text-anchor="middle" fill="white" font-size="14" font-weight="700" font-family="Helvetica">D</text>
        <text x="560" y="78" text-anchor="middle" fill="white" font-size="11" font-family="Helvetica">¿Influye el tratamiento de variables?</text>
        <text x="560" y="96" text-anchor="middle" fill="white" font-size="10" font-family="Helvetica" opacity="0.85">misma población -- n = 13.355</text>
        <rect x="430" y="175" width="260" height="100" rx="10" fill="{COLOR_TRATADO}" />
        <text x="560" y="200" text-anchor="middle" fill="white" font-size="14" font-weight="700" font-family="Helvetica">B -- TRATADO-A</text>
        <text x="560" y="218" text-anchor="middle" fill="white" font-size="11" font-family="Helvetica">¿Qué ocurre al depurar los datos?</text>
        <text x="560" y="236" text-anchor="middle" fill="white" font-size="10" font-family="Helvetica" opacity="0.85">variables y población -- n = 10.669</text>
        <line x1="560" y1="275" x2="560" y2="315" stroke="#bbb" stroke-width="1.5" stroke-dasharray="3,3" />
        <text x="590" y="298" text-anchor="start" fill="#999" font-size="9" font-family="Helvetica">variante</text>
        <rect x="430" y="315" width="260" height="110" rx="10" fill="{COLOR_SENSIBILIDAD}" />
        <text x="560" y="340" text-anchor="middle" fill="white" font-size="14" font-weight="700" font-family="Helvetica">Chequeo de sensibilidad</text>
        <text x="560" y="358" text-anchor="middle" fill="white" font-size="11" font-family="Helvetica">¿Depende del criterio de imputación?</text>
        <text x="560" y="376" text-anchor="middle" fill="white" font-size="10" font-family="Helvetica" opacity="0.85">mismas filas que B, otro criterio</text>
        <text x="560" y="392" text-anchor="middle" fill="white" font-size="9" font-family="Helvetica" opacity="0.75">fuera de la muestra de 426</text>
        <line x1="690" y1="85" x2="870" y2="205" stroke="#ccc" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#flecha_cm)" />
        <line x1="690" y1="225" x2="870" y2="225" stroke="#ccc" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#flecha_cm)" />
        <rect x="870" y="170" width="240" height="110" rx="10" fill="#FBEED6" stroke="{AMBAR_PENDIENTE}" stroke-width="2" />
        <text x="990" y="220" text-anchor="middle" fill="{OCRE_DORADO_TEXTO}" font-size="14" font-weight="700" font-family="Helvetica">Muestra común</text>
        <text x="990" y="238" text-anchor="middle" fill="{OCRE_DORADO_TEXTO}" font-size="11" font-family="Helvetica">¿Qué ocurre en igualdad de condiciones?</text>
        <text x="990" y="256" text-anchor="middle" fill="#806000" font-size="10" font-family="Helvetica" opacity="0.85">n = 426 -- comparación controlada</text>
      </svg>
    </div>
    """,
    unsafe_allow_html=True,
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

st.caption("Selecciona qué versiones mostrar")
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

r2_a = versiones.get("A_crudo", {}).get("r2", 0)
r2_d = versiones.get("D_variables_tratadas_poblacion_cruda", {}).get("r2", 0)
r2_b = versiones.get("B_tratado_criterio_A", {}).get("r2", 0)
delta_ad = r2_a - r2_d
delta_ab = r2_a - r2_b
n_ad = versiones.get("A_crudo", {}).get("n", 0)
n_b = versiones.get("B_tratado_criterio_A", {}).get("n", 0)
st.markdown(
    f'<div style="background-color: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.4rem 1.6rem; margin: 1rem 0;">'
    f'<div style="font-size: 0.78rem; color: #666; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.9rem;">Hallazgo preliminar</div>'
    f'<div style="display: flex; flex-wrap: wrap; gap: 2.5rem;">'
    f'<div style="flex: 1; min-width: 260px;">'
    f'<div style="font-size: 1.15rem; font-weight: 700; color: #31333F;">Efecto de las variables '
    f'(Δ = <span style="color: {COLOR_NEUTRO};">{fmt_num(delta_ad, 3)}</span>)</div>'
    f'<div style="font-size: 0.95rem; color: #555; margin-top: 0.5rem; line-height: 1.4;">Cambiar solo variables (A vs. D, misma población) casi no afecta el R².</div>'
    f'</div>'
    f'<div style="flex: 1; min-width: 260px; border-left: 2px solid #d8dce0; padding-left: 2.5rem;">'
    f'<div style="font-size: 1.15rem; font-weight: 700; color: #31333F;">Efecto de la población '
    f'(Δ = <span style="color: {AMBAR_PENDIENTE};">{fmt_num(delta_ab, 3)}</span>)</div>'
    f'<div style="font-size: 0.95rem; color: #555; margin-top: 0.5rem; line-height: 1.4;">La diferencia (A vs. B) viene sobre todo de usar poblaciones distintas ({fmt_num(n_ad)} vs. {fmt_num(n_b)} filas).</div>'
    f'</div>'
    f'</div>'
    f'<div style="font-size: 0.8rem; color: #888; border-top: 1px solid #eaeaeb; padding-top: 0.7rem; margin-top: 1rem;">'
    f'Resultado preliminar, no estadísticamente probado.</div>'
    f'</div>',
    unsafe_allow_html=True
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

st.caption(
    "El resto de comprobaciones del Chequeo de sensibilidad (criterio de imputación por barrio vs. "
    "capacidad) se investiga en la página 'Resultados y robustez'."
)
