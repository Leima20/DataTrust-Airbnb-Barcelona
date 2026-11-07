import streamlit as st

from src.data_loader import cargar_calidad, cargar_impacto_negocio, cargar_modelo
from src.styles import kicker, caja_pendiente, fmt_num, AMBAR_PENDIENTE

calidad = cargar_calidad()
modelo = cargar_modelo()
impacto = cargar_impacto_negocio()

kicker("Página 9 de 9")
st.title("Metodología y limitaciones")
st.markdown("Detalle técnico completo: fuente de datos, definición de variables, parámetros del modelo, diseño de la validación y limitaciones.")

tab_datos, tab_modelo, tab_robustez = st.tabs([
    "📋 Datos y gobernanza", "🧮 Modelo y validación", "🔁 Robustez y simulación",
])

# ---------- Grupo 1: Datos y gobernanza ----------
with tab_datos:
    with st.expander("Fuente y estructura de los datos", expanded=True):
        tablas = calidad.get("tablas", {})
        st.markdown(
            f"- `listings.csv`: {tablas.get('listings', {}).get('filas', '—')} filas, "
            f"{tablas.get('listings', {}).get('columnas_raw', '—')} columnas en crudo, "
            f"{tablas.get('listings', {}).get('columnas_curado', '—')} en curado.\n"
            f"- `reviews.csv`: {tablas.get('reviews', {}).get('filas', 0):,} filas, "
            f"{tablas.get('reviews', {}).get('columnas_raw', '—')} columnas (igual en crudo y curado).\n"
            f"- `calendar.csv`: {tablas.get('calendar', {}).get('filas', 0):,} filas, "
            f"{tablas.get('calendar', {}).get('columnas_raw', '—')} columnas en crudo, "
            f"{tablas.get('calendar', {}).get('columnas_curado', '—')} en curado (+1 por la bandera `rango_noches_incoherente`, C2).\n"
            f"- Fuente: Inside Airbnb Barcelona."
        )

    with st.expander("Definición de la variable objetivo"):
        t = modelo.get("target", {})
        st.markdown(f"**Target**: `{t.get('nombre', '—')}` (estimación de Inside Airbnb, no ingreso real observado).")
        st.markdown("**Predictoras excluidas por fuga de información**: " + ", ".join(f"`{c}`" for c in t.get("excluidas_por_fuga", [])))
        st.markdown(t.get("nota_fuga", ""))
        st.markdown("**Predictoras usadas**: " + ", ".join(f"`{c}`" for c in modelo.get("predictoras", [])))
        st.markdown(modelo.get("nota_amenities", ""))

    with st.expander("Reglas de exclusión e imputación"):
        st.markdown(
            "Cada uno de los 14 hallazgos recibió una de 3 decisiones: **cambio de datos** (se modificó el "
            "valor), **bandera sin cambiar el valor** (se marcó para revisión manual, dato intacto), o "
            "**mantener sin tratamiento** (decisión consciente de no tocarlo)."
        )
        st.caption("Lista completa de qué hallazgo recibió cada decisión, con su justificación, en la página "
                   "'Auditoría de calidad'.")

# ---------- Grupo 2: Modelo y validación ----------
with tab_modelo:
    with st.expander("Tratamiento de las versiones A, D, B y el chequeo de sensibilidad", expanded=True):
        for clave, v in modelo.get("versiones", {}).items():
            st.markdown(f"**{v['nombre_display']}** (n={v['n']:,})".replace(",", "."))
            st.markdown(v.get("descripcion", ""))
            st.markdown("")

    with st.expander("Parámetros del algoritmo"):
        algoritmo = modelo.get("algoritmo", {})
        st.code(
            f"RandomForestRegressor(\n"
            f"    n_estimators={algoritmo.get('n_estimators')},\n"
            f"    random_state={algoritmo.get('random_state')},\n"
            f"    n_jobs={algoritmo.get('n_jobs')},\n"
            f")\n{algoritmo.get('split')}\nMétricas: {', '.join(algoritmo.get('metricas', []))}\n"
            f"Modelo de referencia: {algoritmo.get('baseline')}",
            language="text",
        )

    with st.expander("Diseño de la validación y la muestra común de 426 filas"):
        fuga = modelo.get("fuga_de_datos_detectada_y_corregida", {})
        st.markdown(fuga.get("descripcion", ""))
        st.markdown(fuga.get("correccion", ""))
        muestra = modelo.get("muestra_comun_426", {})
        st.markdown(f"**Representatividad**: {muestra.get('representatividad', '')}")

    with st.expander("Definición e interpretación de R²"):
        st.markdown(
            "Proporción de la varianza del target que el modelo explica sobre el conjunto de test. No es un "
            "porcentaje de aciertos, y un valor alto en poblaciones distintas no es comparable sin controlar "
            "qué población se evaluó — ver página 'Comparación de modelos'."
        )

# ---------- Grupo 3: Robustez y simulación ----------
with tab_robustez:
    with st.expander("Método de submuestreo y bootstrap", expanded=True):
        sim = modelo.get("simulacion_5000_submuestras", {})
        st.markdown(f"**Simulación de 5.000 submuestras**: {sim.get('metodo', '')}")
        boot = modelo.get("bootstrap_intervalos_confianza", {})
        st.markdown(f"**Bootstrap de intervalos de confianza**: {boot.get('metodo', '')}")
        st.caption(
            "Ambos métodos reutilizan predicciones ya calculadas por modelos entrenados una sola vez -- miden "
            "la sensibilidad del resultado a qué filas se evalúan, no la incertidumbre de reentrenar el "
            "modelo con otro reparto de datos (una fuente de variabilidad distinta, no cuantificada aquí)."
        )

    with st.expander("Simulación de decisión: regla original vs. regla auditada"):
        exp = impacto.get("experimento_decision", {})
        st.markdown(f"**Escenario simulado**: {exp.get('escenario', '')}")
        st.markdown(f"**Universo**: {fmt_num(exp.get('universo_n', 0))} anuncios -- {exp.get('universo_nota', '')}")
        st.markdown(
            "**Regla original**: descarta cualquier anuncio con `estimated_revenue_l365d == 0` "
            f"({fmt_num(exp.get('regla_original', {}).get('descartados_n', 0))} anuncios, "
            f"{fmt_num(exp.get('regla_original', {}).get('descartados_pct', 0), 1)}% del universo)."
        )
        st.markdown(
            "**Regla auditada**: de esos, los que cumplen el patrón (0 reseñas recientes Y estancia mínima "
            f"≥28 noches) pasan a 'requiere revisión' en vez de descartarse -- "
            f"{fmt_num(exp.get('regla_auditada', {}).get('revision_n', 0))} anuncios "
            f"({fmt_num(exp.get('cambian_clasificacion_pct_de_descartados', 0), 1)}% de los descartados "
            "originalmente)."
        )
        st.caption(f"Fuente: `{exp.get('fuente', '—')}` (script permanente en la raíz del proyecto, ejecutado "
                   "en vivo contra el CSV crudo).")
        st.info(exp.get("limites", ""))

st.markdown("<div style='margin-top:1.4rem;'></div>", unsafe_allow_html=True)
st.markdown("### Limitaciones y cuestiones pendientes")
st.caption("Transparencia metodológica completa -- las 6 limitaciones conocidas del proyecto, sin excepción.")


def _tarjeta_limitacion(icono, titulo, texto):
    st.markdown(
        f'<div style="background-color:#fff; border:1px solid #e3e6ea; border-left:4px solid {AMBAR_PENDIENTE}; '
        f'border-radius:8px; padding:0.85rem 1.05rem; height:100%; margin-bottom:0.9rem;">'
        f'<div style="display:flex; align-items:baseline; gap:0.5rem; margin-bottom:0.3rem;">'
        f'<span style="font-size:1.05rem;">{icono}</span>'
        f'<span style="font-weight:700; font-size:0.92rem; color:#31333F;">{titulo}</span>'
        f'</div>'
        f'<div style="font-size:0.85rem; color:#555; line-height:1.45;">{texto}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


col_lim1, col_lim2 = st.columns(2)
with col_lim1:
    _tarjeta_limitacion(
        "📏", "Tamaño de la muestra común",
        "Solo 426 filas pasaron el filtro sin fuga de datos — suficiente para el efecto combinado (A-B), "
        "insuficiente para repartir con precisión cuánto corresponde a población y cuánto a variables por "
        "separado (A-D y D-B individualmente). <b>Próximo paso</b>: repetir este análisis con una muestra "
        "mayor (más snapshots de Inside Airbnb) para comprobar si el resultado se mantiene o cambia.",
    )
    _tarjeta_limitacion(
        "📐", "Incertidumbre de las estimaciones",
        "Los intervalos de confianza de A-D y D-B incluyen el cero — no se puede afirmar su signo ni su "
        "magnitud con precisión.",
    )
    _tarjeta_limitacion(
        "⚙️", "Fuga leve en la imputación del Modelo D",
        "La mediana de `bedrooms`/`bathrooms`/`beds` se calculó sobre todo el dataframe antes del split — "
        "la misma práctica que ya existía en el tratamiento original de los datos, documentada aquí "
        "como limitación conocida del método.",
    )
with col_lim2:
    _tarjeta_limitacion(
        "🎯", "El target no es un ingreso real observado",
        "`estimated_revenue_l365d` es una estimación de Inside Airbnb basada en reseñas y disponibilidad, "
        "no datos de reservas reales.",
    )
    _tarjeta_limitacion(
        "🔭", "Alcance del experimento",
        "Un solo dataset (Airbnb Barcelona), un solo algoritmo (Random Forest), una sola variable objetivo "
        "— no se generaliza automáticamente a otros contextos. <b>Próximo paso</b>: explorar otras "
        "variables predictoras no incluidas en este modelo, por si influyen en el resultado.",
    )
    _tarjeta_limitacion(
        "🏠", "La imputación no distingue `room_type`",
        "`bedrooms`/`bathrooms`/`beds` se agrupan solo por `accommodates`, mezclando pisos enteros con "
        "habitaciones privadas/compartidas de la misma capacidad. Afecta al 5,9% de los `bedrooms` "
        "imputados (151 de 2.562), con un sesgo promedio de +1,07 habitaciones -- marginal en `bathrooms` "
        "y `beds` (&lt;1%). Ver detalle en 'Auditoría de calidad' → Gobernanza y tratamiento → criterio de "
        "imputación.",
    )
