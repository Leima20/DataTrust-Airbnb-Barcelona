"""DataTrust -- página de contexto: objetivos, fuentes y flujo del proyecto."""
import streamlit as st

from src.data_loader import cargar_calidad, cargar_contexto, cargar_geografia_distrito, cargar_geojson_barrios
from src.styles import (
    kicker, fmt_num, AZUL_OSCURO, AZUL_PIZARRA, AZUL_PETROLEO, GRIS_CLARO, TURQUESA_TEXTO,
)
from src.charts import mapa_anuncios_distrito


COLOR_TABLA = {
    "listings": AZUL_PIZARRA,
    "reviews": AZUL_PIZARRA,
    "calendar": AZUL_PIZARRA,
}


ICONO_LISTINGS = """<svg width="30" height="30" viewBox="0 0 24 24" fill="none">
    <path d="M3 11.5 12 4l9 7.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M5.5 10v9.5h13V10" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="10" y="13.5" width="4" height="6" stroke="currentColor" stroke-width="1.6"/>
</svg>"""
ICONO_REVIEWS = """<svg width="30" height="30" viewBox="0 0 24 24" fill="none">
    <path d="M4 5h16v11H9l-5 4V5Z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/>
    <path d="M8 10.3 10 9l1.6 1.3-.6 2L9 13l-1.6-.7-.6-2Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
</svg>"""
ICONO_CALENDAR = """<svg width="30" height="30" viewBox="0 0 24 24" fill="none">
    <rect x="3.5" y="5" width="17" height="15" rx="2" stroke="currentColor" stroke-width="1.8"/>
    <path d="M3.5 9.5h17M8 3v4M16 3v4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
    <rect x="7" y="12.5" width="3" height="3" fill="currentColor"/>
</svg>"""


def _tarjeta_tabla(icono, etiqueta, valor, descripcion_corta, color):
    st.markdown(
        f"""
        <div style="background-color:white; border-top:4px solid {color}; border-radius:10px;
                    padding:1rem 1.1rem; height:100%;">
        <div style="color:{color};">{icono}</div>
        <span style="font-size:0.8rem; color:#555; text-transform:uppercase; font-weight:600;">
        {etiqueta}</span><br>
        <span style="font-size:2rem; color:{color}; font-weight:800;">{valor}</span><br>
        <span style="font-size:0.85rem; color:#777;">{descripcion_corta}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

def _fila_ranking(d, max_n, total):
    pct = d["n_anuncios"] / total * 100
    ancho = d["n_anuncios"] / max_n * 100
    st.markdown(
        f'''<div style="margin-bottom:0.7rem;">
          <div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:0.25rem;">
            <span style="font-size:1.05rem; color:{AZUL_OSCURO}; font-weight:600;">{d["distrito"]}</span>
            <span style="font-size:1.05rem; color:{AZUL_OSCURO}; font-weight:800;">{pct:.0f}%</span>
          </div>
          <div style="background-color:{GRIS_CLARO}; border-radius:5px; height:12px; overflow:hidden;">
            <div style="width:{ancho:.1f}%; height:100%; background-color:{AZUL_PETROLEO}; border-radius:5px;"></div>
          </div>
        </div>''',
        unsafe_allow_html=True,
    )


def _ranking_distritos(distritos_data, total):
    filas = sorted(distritos_data, key=lambda d: -d["n_anuncios"])
    max_n = filas[0]["n_anuncios"]
    mitad = (len(filas) + 1) // 2
    col_izq, col_der = st.columns(2, gap="large")
    with col_izq:
        for d in filas[:mitad]:
            _fila_ranking(d, max_n, total)
    with col_der:
        for d in filas[mitad:]:
            _fila_ranking(d, max_n, total)


contexto = cargar_contexto()
calidad = cargar_calidad()

kicker("Página 2 de 9")
tablas = calidad.get("tablas", {})
st.title("¿Qué datos utilicé?")
fecha_snapshot = contexto.get("fuente_origen", "").split("snapshot")[-1].strip(" )")
icono_calendar_chico = """<svg width="16" height="16" viewBox="0 0 24 24" fill="none">
    <rect x="3.5" y="5" width="17" height="15" rx="2" stroke="currentColor" stroke-width="2"/>
    <path d="M3.5 9.5h17M8 3v4M16 3v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    <rect x="7" y="12.5" width="3" height="3" fill="currentColor"/>
</svg>"""
st.markdown(
    f"""
    <div style="background-color:white; border-top:4px solid {TURQUESA_TEXTO}; border-radius:10px;
                padding:1.1rem 1.3rem; margin-bottom:0.8rem;">
    <span style="font-size:1.3rem; font-weight:800; color:{AZUL_OSCURO};">Inside Airbnb</span><br>
    <span style="font-size:0.9rem; color:#666;">Proyecto independiente — no afiliado a Airbnb, la empresa</span>
    <div style="margin-top:0.7rem; padding-top:0.6rem; border-top:1px solid {GRIS_CLARO};
                display:flex; align-items:center; gap:0.4rem; color:#777;">
    <span style="display:flex;">{icono_calendar_chico}</span>
    <span style="font-size:0.85rem;">Snapshot: {fecha_snapshot}</span>
    </div>
    </div>
    """,
    unsafe_allow_html=True,
)
c1, c2, c3 = st.columns(3)
with c1:
    _tarjeta_tabla(
        ICONO_LISTINGS, "Anuncios (listings)", fmt_num(tablas.get("listings", {}).get("filas", 0)),
        f"{tablas.get('listings', {}).get('columnas_raw', '—')} columnas en crudo",
        COLOR_TABLA["listings"],
    )
with c2:
    _tarjeta_tabla(
        ICONO_REVIEWS, "Reseñas (reviews)", fmt_num(tablas.get("reviews", {}).get("filas", 0)),
        f"{tablas.get('reviews', {}).get('columnas_raw', '—')} columnas en crudo",
        COLOR_TABLA["reviews"],
    )
with c3:
    _tarjeta_tabla(
        ICONO_CALENDAR, "Calendario (calendar)", fmt_num(tablas.get("calendar", {}).get("filas", 0)),
        f"{tablas.get('calendar', {}).get('columnas_raw', '—')} columnas en crudo",
        COLOR_TABLA["calendar"],
    )

st.markdown("---")
geo = cargar_geografia_distrito()
geojson = cargar_geojson_barrios()
distritos_data = geo.get("distritos", [])
if distritos_data and geojson:
    mas = max(distritos_data, key=lambda d: d["n_anuncios"])
    menos = min(distritos_data, key=lambda d: d["n_anuncios"])
    ratio = mas["n_anuncios"] / menos["n_anuncios"]
    nombres = [d["distrito"] for d in distritos_data]
    ns = [d["n_anuncios"] for d in distritos_data]
    total_anuncios = sum(ns)
    st.markdown("### ¿Cómo se reparten esos anuncios?")
    st.plotly_chart(mapa_anuncios_distrito(geojson, nombres, ns), width="stretch")
    st.caption(
        f"Barcelona no es un mercado uniforme. Cada barrio hereda el número de anuncios de su distrito "
        f"(no hay dato propio a nivel de barrio) -- de {fmt_num(menos['n_anuncios'])} en `{menos['distrito']}` "
        f"a {fmt_num(mas['n_anuncios'])} en `{mas['distrito']}`."
    )
    st.markdown(f"**% del total ({fmt_num(total_anuncios)} anuncios)**")
    _ranking_distritos(distritos_data, total_anuncios)

st.markdown("---")
st.markdown("### El proyecto en detalle")
st.caption("Flujo del proyecto: de la auditoría al resultado final.")

dot_flujo = r"""
digraph Flujo {
  rankdir=LR;
  node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=14, margin=0.2,
        color="#14506B", fillcolor="#EAF2F8"];
  edge [fontname="Helvetica", fontsize=11, color="#888888"];

  aud [label="1. Auditoría\n\nDetección de hallazgos\nen listings, reviews, calendar"];
  gob [label="2. Gobernanza\n\nDecisión documentada por\ncada hallazgo"];
  tra [label="3. Tratamiento\n\nDecisiones ejecutadas\nsobre los datos"];
  neg [label="4. Comparación de negocio\n\nBrecha de ingresos:\ncrudo vs. auditado"];
  mod [label="5. Comparación de modelos\n\nRendimiento:\ncrudo vs. tratado"];
  sim [label="6. Simulación de decisión\n\n¿Qué cambiaría con una\nregla de descarte simple?"];

  aud -> gob -> tra;
  tra -> neg;
  tra -> mod;
  aud -> sim;
  {rank=same; neg; mod; sim}
}
"""
st.graphviz_chart(dot_flujo, width="stretch")
