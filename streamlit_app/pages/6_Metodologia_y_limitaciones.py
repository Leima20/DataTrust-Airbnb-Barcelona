import pandas as pd
import streamlit as st

from src.data_loader import cargar_calidad, cargar_impacto_negocio, cargar_modelo
from src.styles import kicker, caja_pendiente, fmt_num

calidad = cargar_calidad()
modelo = cargar_modelo()
impacto = cargar_impacto_negocio()

kicker("Pagina 9 de 9")
st.title("Metodología y limitaciones")
st.markdown("Detalle técnico completo: fuente de datos, definición de variables, parámetros del modelo, diseño de la validación y limitaciones.")

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

with st.expander("Tratamiento de las versiones A, D, B y el chequeo de sensibilidad"):
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
        f"Baseline: {algoritmo.get('baseline')}",
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

with st.expander("Método de submuestreo y bootstrap"):
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

with st.expander("Reglas de exclusión e imputación"):
    st.markdown(
        "Cada uno de los 14 hallazgos recibió una de 3 decisiones: **cambio de datos** (se modificó el "
        "valor), **bandera sin cambiar el valor** (se marcó para revisión manual, dato intacto), o "
        "**mantener sin tratamiento** (decisión consciente de no tocarlo)."
    )
    st.caption("Lista completa de qué hallazgo recibió cada decisión, con su justificación, en la página "
               "'Auditoría de calidad'.")

with st.expander("Limitaciones y cuestiones pendientes", expanded=True):
    st.markdown(
        "- **Tamaño de la muestra común**: solo 426 filas pasaron el filtro sin fuga de datos — "
        "suficiente para el efecto combinado (A-B), insuficiente para repartir con precisión cuánto "
        "corresponde a población y cuánto a variables por separado (A-D y D-B individualmente).\n"
        "- **El target no es un ingreso real observado**: `estimated_revenue_l365d` es una estimación de "
        "Inside Airbnb basada en reseñas y disponibilidad, no datos de reservas reales.\n"
        "- **Incertidumbre de las estimaciones**: los intervalos de confianza de A-D y D-B incluyen el "
        "cero — no se puede afirmar su signo ni su magnitud con precisión.\n"
        "- **Alcance del experimento**: un solo dataset (Airbnb Barcelona), un solo algoritmo (Random "
        "Forest), una sola variable objetivo — no se generaliza automáticamente a otros contextos.\n"
        "- **Fuga leve en la imputación del Modelo D**: la mediana de `bedrooms`/`bathrooms`/`beds` se "
        "calculó sobre todo el dataframe antes del split — la misma práctica que ya existía en el "
        "tratamiento original del notebook 05, documentada aquí como limitación conocida del método.\n"
        "- **Alcance de esta app**: no reejecuta los modelos ni carga `calendar.csv` completo (5,6 "
        "millones de filas) -- usa exclusivamente resultados precalculados y guardados en "
        "`notebooks/06_modelo_ml.ipynb`."
    )
