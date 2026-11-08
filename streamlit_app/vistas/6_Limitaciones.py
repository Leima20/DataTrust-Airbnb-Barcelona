import streamlit as st

from src.data_loader import cargar_modelo
from src.styles import kicker, TURQUESA

modelo = cargar_modelo()

kicker("Página 8 de 9")
st.title("Limitaciones")
st.markdown("Las 6 limitaciones conocidas del proyecto, sin excepción.")

universo_n = modelo.get("poblacion_limpia_experimento", {}).get("A_solo_poblacion_limpia", {}).get("n_test", 2131)
muestra_n = modelo.get("muestra_comun_426", {}).get("n", 426)

LIMITACIONES = [
    ("01", "Tamaño de la muestra común", f"{muestra_n} de {universo_n} filas -- alcanza para el efecto combinado A-B, no para separar A-D y D-B con precisión."),
    ("02", "Incertidumbre de las estimaciones", "Los intervalos de confianza de A-D y D-B incluyen el cero."),
    ("03", "Fuga leve en la imputación del Modelo D", "La mediana de `bedrooms`/`bathrooms`/`beds` se calculó sobre todo el dataframe antes del split -- la misma práctica ya presente en el tratamiento original."),
    ("04", "El target no es un ingreso real observado", "`estimated_revenue_l365d` es una estimación de Inside Airbnb, no datos de reservas reales."),
    ("05", "Alcance del experimento", "Un solo dataset, un solo algoritmo, una sola variable objetivo -- no se generaliza automáticamente a otros contextos."),
    ("06", "La imputación no distingue `room_type`", "Afecta al 5,9% de los `bedrooms` imputados (151 de 2.562), con un sesgo promedio de +1,07 habitaciones -- marginal en `bathrooms`/`beds` (&lt;1%)."),
]

tab_limitaciones, tab_pasos = st.tabs(["Limitaciones", "Próximos pasos"])

with tab_limitaciones:
    for numero, titulo, implicacion in LIMITACIONES:
        st.markdown(
            f'<div style="display:flex; gap:0.9rem; padding:0.8rem 0; border-bottom:1px solid #eee;">'
            f'<div style="font-size:1rem; color:#999; font-weight:700; min-width:2rem;">{numero}</div>'
            f'<div style="flex:1;">'
            f'<span style="font-weight:700; font-size:1.1rem; color:#31333F;">{titulo}</span>'
            f'<div style="font-size:1.05rem; color:#555; line-height:1.5; margin-top:0.3rem;">{implicacion}</div>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with st.expander("Ver detalle completo de la limitación 06 (imputación y room_type)"):
        st.markdown(
            "`bedrooms`/`bathrooms`/`beds` se agrupan solo por `accommodates`, mezclando pisos enteros con "
            "habitaciones privadas/compartidas de la misma capacidad. Ver detalle en 'Auditoría de calidad' → "
            "Gobernanza y tratamiento → criterio de imputación."
        )

with tab_pasos:
    st.markdown("Lo que investigaría a continuación, directamente a partir de estas limitaciones.")

    st.markdown(
        f'<div style="border-left:4px solid {TURQUESA}; padding:0.3rem 0 0.3rem 1rem; margin-bottom:1.1rem;">'
        f'<div style="font-size:1.2rem; color:#31333F; font-weight:700; line-height:1.55;">Más allá de este '
        f'proyecto puntual: convertir este proceso manual en un sistema que prepare los datos automáticamente '
        f'-- detectando problemas de calidad y aplicando las reglas de gobernanza -- antes de cualquier '
        f'análisis o modelo predictivo, no solo para este dataset.</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown("**Pasos más concretos, a partir de las limitaciones de arriba:**")

    PROXIMOS_PASOS = [
        "Repetir el análisis con una muestra mayor (más snapshots de Inside Airbnb): el efecto de A-D y D-B "
        "por separado ya se calcula, pero con 426 filas sus intervalos de confianza incluyen el cero -- una "
        "muestra mayor permitiría confirmarlos con precisión estadística.",
        "Calcular la mediana de imputación del Modelo D solo con los datos de entrenamiento, no con todo el "
        "dataframe antes del split, para eliminar la fuga leve de la limitación 03.",
        "Imputar `bedrooms`/`bathrooms`/`beds` agrupando también por `room_type`, no solo por `accommodates`.",
        "Explorar otras variables predictoras no incluidas en este modelo.",
        "Validar las estimaciones contra datos reales de reservas, si se consiguiera acceso a esa información.",
    ]

    for paso in PROXIMOS_PASOS:
        st.markdown(
            f'<div style="display:flex; gap:0.7rem; align-items:flex-start; padding:0.45rem 0;">'
            f'<span style="color:{TURQUESA}; font-size:1.2rem; flex-shrink:0;">&rarr;</span>'
            f'<span style="font-size:1.05rem; color:#444; line-height:1.55;">{paso}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
