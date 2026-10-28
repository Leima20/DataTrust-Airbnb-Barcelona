import pandas as pd
import streamlit as st

from src.data_loader import cargar_contexto, cargar_impacto_negocio, cargar_modelo
from src.styles import kicker, fmt_num

impacto = cargar_impacto_negocio()
modelo = cargar_modelo()
contexto = cargar_contexto()

kicker("Pagina 8 de 9")
st.title("Conclusiones y recomendaciones")
st.markdown(
    "Despues de auditar, tratar y comparar (sin fuga de datos), esta pagina reune todo en 4 niveles de "
    "certeza distintos -- para no mezclar lo que se demostro con lo que es solo una interpretacion "
    "razonable."
)

tab1, tab2, tab3, tab4 = st.tabs(["Hallazgos demostrados", "Interpretaciones razonables", "Limitaciones", "Recomendaciones"])

with tab1:
    st.subheader("Resultados que se desprenden directamente de las auditorías y experimentos verificados")
    naive = impacto.get("gap_naive", {})
    corregido = impacto.get("gap_corregido", {})
    if naive and corregido:
        st.markdown(
            f"- Al investigar los 2.686 casos de ingreso estimado '0€' no reales, la brecha media "
            f"particular-profesional cambia de **{fmt_num(naive.get('gap_pct', 0), 1)}%** a "
            f"**{fmt_num(corregido.get('gap_pct', 0), 1)}%** "
            f"-- un cambio de conclusión medible, no cosmético (ver 'El hallazgo crítico')."
        )
    muestra = modelo.get("muestra_comun_426", {}).get("resultados", {})
    if muestra:
        st.markdown(
            f"- En una comparación sin fuga de datos, sobre 426 observaciones que no formaron parte del "
            f"entrenamiento de ninguno de los tres modelos y que se utilizaron para evaluarlos sobre una "
            f"base común: el modelo tratado obtiene un R² mejor que el crudo "
            f"(**{fmt_num(muestra['A_crudo']['r2'], 3)}** → **{fmt_num(muestra['B_tratado_criterio_A']['r2'], 3)}**), con "
            f"un intervalo de confianza que no incluye el cero -- aunque el diseño no permite repartir con "
            f"precisión cuánto de esa mejora viene de la población evaluada y cuánto de la construcción de "
            f"variables (ver pestaña 'Interpretaciones razonables')."
        )
    st.markdown(
        "- El tratamiento de curación (bedrooms/bathrooms/beds imputados) **no depende** de cuál de dos "
        "criterios razonables se use: la diferencia entre imputar por capacidad o por barrio es menor al "
        "0,1% en MAE."
    )
    st.markdown(
        "- Se detectó y corrigió una fuga de datos real en el propio diseño del experimento (el 80% de "
        "una muestra de validación ya había sido vista en entrenamiento) — documentada como parte del "
        "proceso, no ocultada."
    )

with tab2:
    st.subheader("Explicaciones compatibles con los resultados, pero no demostradas completamente")
    st.markdown(
        "- La mejora combinada del modelo tratado **probablemente** viene tanto de excluir población "
        "trivial (2.686 casos de ingreso '0€' no estimable) como de construir mejor las variables — ambos "
        "efectos van en la misma dirección, pero no se puede repartir la proporción exacta con los datos "
        "disponibles.\n"
        "- Que la discrepancia entre la muestra grande (0,006) y la muestra pequeña (0,04) se explique por "
        "tamaño de muestra es la explicación **más simple y mejor respaldada** (percentil ~1,2 en 5.000 "
        "simulaciones), pero no es una prueba definitiva de que no exista ningún efecto distinto.\n"
        "- Que los profesionales adopten el nuevo registro NRUA más rápido (65,7% vs. 18-25%) es "
        "compatible con una hipótesis de mayor capacidad administrativa, pero el proyecto no investigó la "
        "causa directamente."
    )

with tab3:
    st.subheader("Limitaciones")
    st.markdown(
        "En resumen: la validación sin fuga de datos usa solo **426 filas** (suficiente para el efecto "
        "combinado, no para separar población de variables), el target `estimated_revenue_l365d` es una "
        "**estimación** de Inside Airbnb y no un ingreso real observado, y el experimento cubre un solo "
        "dataset y un solo algoritmo."
    )
    st.caption("Detalle completo (6 puntos) en la página 'Metodología y limitaciones'.")

with tab4:
    st.subheader("Recomendaciones")
    st.markdown(
        "- Investigar la **semántica** de las variables antes de tratar sus valores (el caso de los "
        "2.686 ceros 'no estimables' no se habría encontrado solo mirando el porcentaje de nulos).\n"
        "- Documentar las reglas de limpieza con la misma trazabilidad que una decisión de negocio.\n"
        "- Separar explícitamente valores desconocidos de ceros reales en cualquier variable objetivo.\n"
        "- Evitar fugas entre entrenamiento y evaluación, especialmente al comparar modelos entrenados "
        "sobre poblaciones de origen distintas.\n"
        "- Usar conjuntos de comparación equivalentes al evaluar dos versiones de un modelo.\n"
        "- Registrar las transformaciones para garantizar la reproducibilidad.\n"
        "- Revisar la calidad de los datos **antes** de interpretar las métricas de un modelo, no después."
    )

st.markdown("---")
st.markdown("### Cierre: ¿se cumplieron los 5 objetivos del proyecto?")
muestra_426 = modelo.get("muestra_comun_426", {}).get("resultados", {})
evidencia_por_objetivo = {
    1: "14 hallazgos documentados en las 3 tablas (ver 'Auditoría de calidad').",
    2: "cada hallazgo clasificado por riesgo, con una de 3 decisiones de gobernanza documentada.",
    3: "L1/L2/L4 ejecutados con cambio de datos, L5/C2 marcados con bandera, el resto mantenido sin "
       "tratamiento — cada decisión con su justificación.",
    4: (f"la brecha media particular-profesional cambia de {fmt_num(naive.get('gap_pct', 0), 1)}% a "
        f"{fmt_num(corregido.get('gap_pct', 0), 1)}% al investigar los 2.686 casos de ingreso no estimable "
        "(ver 'El hallazgo crítico').") if naive and corregido else "ver 'Hallazgos demostrados' arriba.",
    5: (f"R² sube de {fmt_num(muestra_426.get('A_crudo', {}).get('r2', 0), 3)} a "
        f"{fmt_num(muestra_426.get('B_tratado_criterio_A', {}).get('r2', 0), 3)} en una comparación sin fuga "
        "de datos, sobre 426 observaciones que no formaron parte del entrenamiento de ningún modelo."
        ) if muestra_426 else "ver 'Resultados y robustez'.",
}
with st.expander("Ver detalle objetivo por objetivo"):
    for o in contexto.get("objetivos", []):
        st.markdown(f"**{o['n']}. {o['texto']}**")
        st.markdown(f"✓ Cumplido — {evidencia_por_objetivo.get(o['n'], '')}")

st.markdown("---")
st.markdown("### Qué decisión podría cambiar, y qué evidencia tenemos")
st.markdown(
    "La simulación de clasificación de anuncios es un caso práctico de la pregunta de investigación, pero "
    "**no se ha demostrado que Airbnb o un anfitrión haya tomado una decisión equivocada**, ni se observó "
    "una decisión real antes y después de la auditoría. Para no sobre-afirmar, se distinguen 4 niveles:"
)
exp = impacto.get("experimento_decision", {})
auditada = exp.get("regla_auditada", {})
niveles = pd.DataFrame([
    {"Nivel": "Hallazgo observado", "Qué se puede defender": "La interpretación de los ingresos estimados cambia al investigar los ceros (2.686 casos, gap de 39,7% a 23,1%)."},
    {"Nivel": "Resultado del experimento", "Qué se puede defender": "Las métricas del modelo varían según la población evaluada y el tratamiento (R² de 0,348 a 0,448 sin fuga de datos)."},
    {"Nivel": "Cambio de clasificación (simulado)", "Qué se puede defender": (
        f"Bajo una regla de decisión simple que descarta ingreso=0, {fmt_num(auditada.get('revision_n', 0))} "
        f"de los anuncios descartados ({fmt_num(exp.get('cambian_clasificacion_pct_de_descartados', 0), 1)}%) "
        "pasarían a 'revisión' en vez de descartarse -- medido con datos reales, ver 'El hallazgo crítico'."
    ) if exp else "ver 'El hallazgo crítico'."},
    {"Nivel": "Impacto económico real", "Qué se puede defender": "No observado -- no hay datos de ingresos/reservas reales ni un caso de inversión documentado que lo mida. No se ha encontrado evidencia de que inversores reales usen Inside Airbnb para decidir así."},
])
st.dataframe(niveles, width="stretch", hide_index=True)
st.warning(
    "**No se afirma que se haya probado una decisión empresarial equivocada.** La conclusión se formula "
    "en términos de **riesgo analítico**: tomar decisiones sobre datos sin auditar es arriesgado y "
    "medible en este caso — no que ya se haya demostrado un error concreto de Airbnb o de un anfitrión."
)
st.markdown(
    "> *La calidad de los datos no se reduce al porcentaje de valores nulos — y una diferencia en las "
    "métricas, por sí sola, nunca demuestra un impacto empresarial real sin investigar qué la produce.*"
)
