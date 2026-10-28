"""DataTrust -- pagina de contexto: objetivos, fuentes, flujo y herramientas."""
import streamlit as st

from src.data_loader import cargar_calidad, cargar_contexto, cargar_geografia_distrito, cargar_geojson_barrios
from src.styles import kicker, fmt_num
from src.charts import mapa_anuncios_distrito

COLOR_TABLA = {
    "listings": "#0B3954",
    "reviews": "#1B998B",
    "calendar": "#5C7A99",
}


def _tarjeta_tabla(etiqueta, valor, columnas_txt, descripcion, color):
    st.markdown(
        f"""
        <div style="background-color:white; border-top:4px solid {color}; border-radius:10px;
                    padding:1rem 1.1rem; height:100%;">
        <span style="font-size:0.8rem; color:#555; text-transform:uppercase; font-weight:600;">
        {etiqueta}</span><br>
        <span style="font-size:2rem; color:{color}; font-weight:800;">{valor}</span><br>
        <span style="font-size:0.78rem; color:#888;">{columnas_txt}</span><br>
        <span style="font-size:0.85rem; color:#555;">{descripcion}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

contexto = cargar_contexto()
calidad = cargar_calidad()

kicker("Pagina 2 de 9")
st.title("Contexto del proyecto")
st.markdown(
    "Antes de entrar a los hallazgos: qué se propuso el proyecto, de donde vienen los datos, y cómo "
    "se conectan las piezas."
)

st.markdown("### La escala de los datos")
st.markdown(
    "Los datos provienen de **Inside Airbnb**, un proyecto independiente (no pertenece a Airbnb la "
    "empresa) que recopila datos públicos de la plataforma mediante web scraping, con fines de "
    "investigación y transparencia sobre el impacto de los alquileres turísticos."
)
st.caption(f"Origen: {contexto.get('fuente_origen', '—')}")
tablas = calidad.get("tablas", {})
fuentes_desc = {f["nombre"].replace(".csv", ""): f["descripcion"] for f in contexto.get("fuentes", [])}
c1, c2, c3 = st.columns(3)
with c1:
    _tarjeta_tabla(
        "Anuncios (listings)", fmt_num(tablas.get("listings", {}).get("filas", 0)),
        f"{tablas.get('listings', {}).get('columnas_raw', '—')} columnas en crudo",
        fuentes_desc.get("listings", ""), COLOR_TABLA["listings"],
    )
with c2:
    _tarjeta_tabla(
        "Reseñas (reviews)", fmt_num(tablas.get("reviews", {}).get("filas", 0)),
        f"{tablas.get('reviews', {}).get('columnas_raw', '—')} columnas en crudo",
        fuentes_desc.get("reviews", ""), COLOR_TABLA["reviews"],
    )
with c3:
    _tarjeta_tabla(
        "Calendario (calendar)", fmt_num(tablas.get("calendar", {}).get("filas", 0)),
        f"{tablas.get('calendar', {}).get('columnas_raw', '—')} columnas en crudo",
        fuentes_desc.get("calendar", ""), COLOR_TABLA["calendar"],
    )

st.markdown("---")
st.markdown("El análisis se centra específicamente en **Barcelona**, donde los anuncios se concentran de forma muy desigual por distrito:")
geo = cargar_geografia_distrito()
geojson = cargar_geojson_barrios()
distritos_data = geo.get("distritos", [])
if distritos_data and geojson:
    nombres = [d["distrito"] for d in distritos_data]
    ns = [d["n_anuncios"] for d in distritos_data]
    st.plotly_chart(mapa_anuncios_distrito(geojson, nombres, ns), width="stretch")
    mas = max(distritos_data, key=lambda d: d["n_anuncios"])
    menos = min(distritos_data, key=lambda d: d["n_anuncios"])
    st.caption(
        f"Cada barrio hereda el número de anuncios de su distrito (no hay dato propio a nivel de barrio). "
        f"Rango: {fmt_num(menos['n_anuncios'])} anuncios (`{menos['distrito']}`) a "
        f"{fmt_num(mas['n_anuncios'])} (`{mas['distrito']}`)."
    )

st.markdown("---")
st.markdown("### El proyecto en detalle")

tab_obj, tab_herr, tab_flujo = st.tabs(["Objetivos", "Herramientas", "Flujo del proyecto"])

with tab_obj:
    # Mismo icono que la pagina del menu a la que apunta cada objetivo (coherencia real, no al azar)
    gancho_objetivos = {
        1: "🔍 Auditoría",
        2: "🔍 Priorización",
        3: "🧩 Curación",
        4: "🎯 Negocio",
        5: "📊 Modelo",
    }
    objetivos = contexto.get("objetivos", [])
    fila1 = st.columns(3)
    for col, o in zip(fila1, objetivos[:3]):
        with col:
            with st.container(border=True):
                st.markdown(f"**{gancho_objetivos.get(o['n'], '')}**")
                st.markdown(f"{o['n']}. {o['texto']}")
    fila2 = st.columns(2)
    for col, o in zip(fila2, objetivos[3:5]):
        with col:
            with st.container(border=True):
                st.markdown(f"**{gancho_objetivos.get(o['n'], '')}**")
                st.markdown(f"{o['n']}. {o['texto']}")

with tab_herr:
    iconos_herramientas = {
        "Python": "python",
        "pandas": "pandas",
        "SQLite": "sqlite",
        "scikit-learn": "scikitlearn",
        "Plotly": "plotly",
        "Streamlit": "streamlit",
    }
    usos_cortos = {
        "Python": "Carga y exploración",
        "pandas": "Limpieza y curación",
        "SQLite": "Integridad referencial",
        "scikit-learn": "Modelo predictivo",
        "Plotly": "Visualización",
        "Streamlit": "Esta app",
    }
    cols_herr = st.columns(len(iconos_herramientas))
    for col, (nombre, slug) in zip(cols_herr, iconos_herramientas.items()):
        with col:
            st.image(f"assets/icons/{slug}.svg", width=36)
            st.caption(f"**{nombre}**")
            st.caption(usos_cortos.get(nombre, ""))

    with st.expander("Ver detalle técnico de cada herramienta"):
        st.markdown(
            "- **Python + pandas**: lectura de los 3 CSV, duplicados, nulos, clasificación de licencias.\n"
            "- **SQLite**: `JOIN` para filas huérfanas en `reviews` (6.592) y `calendar` (41.245) -- antes "
            "y después del tratamiento; `calendar` (5,6M filas) se consulta solo con SQL, por velocidad.\n"
            "- **scikit-learn**: `RandomForestRegressor`, 4 versiones comparadas.\n"
            "- **Plotly + Streamlit**: todos los gráficos y esta misma app."
        )

with tab_flujo:
    dot_flujo = r"""
    digraph Flujo {
      rankdir=LR;
      node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=14, margin=0.2, color="#14506B"];
      edge [fontname="Helvetica", fontsize=11, color="#888888"];

      aud [label="1. Auditoría\n\n14 hallazgos detectados\nen listings, reviews, calendar", fillcolor="#FDECEC"];
      gob [label="2. Gobernanza\n\nDecisión documentada por\ncada hallazgo", fillcolor="#FFF3DC"];
      tra [label="3. Tratamiento\n\nDecisiones ejecutadas\nsobre los datos", fillcolor="#EAF2F8"];
      neg [label="4a. Comparación negocio\n\nBrecha de ingresos:\ncrudo vs. tratado", fillcolor="#E7F6E7"];
      mod [label="4b. Comparación modelo\n\nR2 del modelo:\ncrudo vs. tratado", fillcolor="#E7F6E7"];
      sim [label="1b. Simulación de decisión\n\n2.686 de 4.181 anuncios\npasan a revisión", fillcolor="#FDECEC"];

      aud -> gob -> tra;
      tra -> neg;
      tra -> mod;
      aud -> sim;
      {rank=same; neg; mod; sim}
    }
    """
    st.graphviz_chart(dot_flujo, width="stretch")
    st.caption(
        "Las dos comparaciones finales se hacen en paralelo, no una después de la otra: el efecto en "
        "una métrica de negocio, y el efecto en el rendimiento del modelo predictivo. Además, directamente "
        "desde la auditoría -- sin pasar por el tratamiento -- se investiga una simulación de decisión "
        "basada en el patrón de los 2.686 ceros (se explica en detalle en 'El hallazgo crítico')."
    )
    st.caption(
        "¿Cómo se ve esto aplicado a filas reales? Ver los ejemplos de 'dato original a dato curado' en "
        "la página 'Auditoría de calidad'."
    )
