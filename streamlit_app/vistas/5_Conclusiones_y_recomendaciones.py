import streamlit as st

from src.data_loader import cargar_contexto, cargar_impacto_negocio, cargar_modelo
from src.styles import kicker, fmt_num, caja_alerta, AZUL_ACERO, TURQUESA, AMBAR_PENDIENTE, AZUL_PETROLEO

impacto = cargar_impacto_negocio()
modelo = cargar_modelo()
contexto = cargar_contexto()

kicker("Página 8 de 9")
st.title("Conclusiones y recomendaciones")
st.markdown(
    "Después de auditar, tratar y comparar (sin fuga de datos), esta página reúne todo en 4 niveles de "
    "certeza distintos -- para no mezclar lo que se demostró con lo que es solo una interpretación "
    "razonable."
)

tab1, tab2, tab3, tab4 = st.tabs(["Hallazgos demostrados", "Interpretaciones razonables", "Limitaciones", "Recomendaciones"])

with tab1:
    st.subheader("Resultados que se desprenden directamente de las auditorías y experimentos verificados")

    def _tarjeta_hallazgo(icono, titulo, texto, chip_html=""):
        st.markdown(
            f'<div style="background-color:#fff; border:1px solid #e3e6ea; border-top:4px solid {AZUL_PETROLEO}; '
            f'border-radius:10px; padding:1rem 1.1rem; height:100%; margin-bottom:0.9rem;">'
            f'<div style="font-size:1.3rem; margin-bottom:0.3rem;">{icono}</div>'
            f'<div style="font-weight:700; font-size:0.98rem; color:#31333F; margin-bottom:0.4rem; line-height:1.3;">{titulo}</div>'
            f'<div style="font-size:0.88rem; color:#555; line-height:1.45; margin-bottom:0.7rem;">{texto}</div>'
            f'{chip_html}'
            f'</div>',
            unsafe_allow_html=True,
        )

    def _chip_antes_despues(antes, despues, etiqueta=""):
        return (
            f'<div style="display:flex; align-items:center; gap:0.5rem; flex-wrap:wrap;">'
            f'<span style="background-color:#E9EDF1; color:{AZUL_ACERO}; padding:0.15rem 0.55rem; '
            f'border-radius:4px; font-size:0.82rem; font-weight:700;">{antes}</span>'
            f'<span style="color:#999; font-weight:700;">&rarr;</span>'
            f'<span style="background-color:#DCEEEC; color:{TURQUESA}; padding:0.15rem 0.55rem; '
            f'border-radius:4px; font-size:0.82rem; font-weight:700;">{despues}</span>'
            f'<span style="font-size:0.78rem; color:#888;">{etiqueta}</span>'
            f'</div>'
        )

    naive = impacto.get("gap_naive", {})
    corregido = impacto.get("gap_corregido", {})
    muestra = modelo.get("muestra_comun_426", {}).get("resultados", {})

    col_a, col_b = st.columns(2)
    with col_a:
        if naive and corregido:
            _tarjeta_hallazgo(
                "💶",
                "La brecha de ingresos cambia al investigar los ceros",
                "Al investigar los 2.686 casos de ingreso estimado '0€' no reales, la brecha media "
                "particular-profesional cambia de forma medible -- un cambio de conclusión, no cosmético "
                "(ver 'El hallazgo crítico').",
                _chip_antes_despues(
                    f"{fmt_num(naive.get('gap_pct', 0), 1)}%", f"{fmt_num(corregido.get('gap_pct', 0), 1)}%",
                    "brecha particular-profesional",
                ),
            )
        _tarjeta_hallazgo(
            "🧭",
            "La curación no depende del criterio de imputación elegido",
            "El tratamiento de curación (bedrooms/bathrooms/beds imputados) no depende de cuál de dos "
            "criterios razonables se use: imputar por capacidad o por barrio.",
            f'<span style="background-color:#DCEEEC; color:{TURQUESA}; padding:0.15rem 0.55rem; '
            f'border-radius:4px; font-size:0.82rem; font-weight:700;">Δ &lt; 0,1% en MAE</span>',
        )
    with col_b:
        if muestra:
            _tarjeta_hallazgo(
                "📊",
                "El modelo tratado predice mejor, sin fuga de datos",
                "Sobre 426 observaciones que no formaron parte del entrenamiento de ninguno de los tres "
                "modelos, el tratado obtiene mejor R² que el crudo, con un intervalo de confianza que no "
                "incluye el cero -- el diseño no permite repartir con precisión cuánto viene de la "
                "población y cuánto de las variables (ver 'Interpretaciones razonables').",
                _chip_antes_despues(
                    fmt_num(muestra['A_crudo']['r2'], 3), fmt_num(muestra['B_tratado_criterio_A']['r2'], 3),
                    "R² (A → B, sin fuga)",
                ),
            )
        _tarjeta_hallazgo(
            "🔍",
            "Se detectó y corrigió una fuga de datos real",
            "En el propio diseño del experimento: una muestra de validación ya había sido vista en "
            "entrenamiento. Documentada como parte del proceso, no ocultada.",
            _chip_antes_despues("80% contaminación", "426 filas seguras", "muestra de validación"),
        )

with tab2:
    st.subheader("Explicaciones compatibles con los resultados, pero no demostradas completamente")
    st.markdown(
        "- La mejora combinada del modelo tratado **probablemente** viene tanto de excluir población "
        "trivial (2.686 casos de ingreso '0€' no estimable) como de construir mejor las variables — ambos "
        "efectos van en la misma dirección, pero no se puede repartir la proporción exacta con los datos "
        "disponibles.\n"
        "- Que la discrepancia entre la muestra grande (0,006) y la muestra pequeña (0,04) se explique por "
        "tamaño de muestra es la explicación **más simple y mejor respaldada** (percentil ~0,7 en 5.000 "
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

def _fila_certeza(color, bg, numero, titulo, texto):
    st.markdown(
        f'<div style="background-color:{bg}; border-left:5px solid {color}; border-radius:8px; '
        f'padding:0.8rem 1.1rem 0.8rem 1rem; margin-bottom:0.7rem;">'
        f'<div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:0.3rem;">'
        f'<span style="background-color:{color}; color:white; border-radius:50%; width:1.6rem; height:1.6rem; '
        f'min-width:1.6rem; display:inline-flex; align-items:center; justify-content:center; font-size:0.8rem; '
        f'font-weight:700;">{numero}</span>'
        f'<span style="font-weight:700; font-size:0.95rem; color:#31333F;">{titulo}</span>'
        f'</div>'
        f'<div style="font-size:0.88rem; color:#555; line-height:1.45; padding-left:2.2rem;">{texto}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

_fila_certeza(
    TURQUESA, "#DCEEEC", "1", "Hallazgo observado",
    "La interpretación de los ingresos estimados cambia al investigar los ceros (2.686 casos, gap de 39,7% a 23,1%).",
)
_fila_certeza(
    AZUL_PETROLEO, "#EAF2F8", "2", "Resultado del experimento",
    "Las métricas del modelo varían según la población evaluada y el tratamiento (R² de 0,347 a 0,450 sin fuga de datos).",
)
_fila_certeza(
    AMBAR_PENDIENTE, "#FFF8EC", "3", "Cambio de clasificación (simulado)",
    (
        f"Bajo una regla de decisión simple que descarta ingreso=0, {fmt_num(auditada.get('revision_n', 0))} "
        f"de los anuncios descartados ({fmt_num(exp.get('cambian_clasificacion_pct_de_descartados', 0), 1)}%) "
        "pasarían a 'revisión' en vez de descartarse -- medido con datos reales, ver 'El hallazgo crítico'."
    ) if exp else "ver 'El hallazgo crítico'.",
)
_fila_certeza(
    "#999999", "#ffffff", "4", "Impacto económico real",
    "No observado -- no hay datos de ingresos/reservas reales ni un caso de inversión documentado que lo "
    "mida. No se ha encontrado evidencia de que inversores reales usen Inside Airbnb para decidir así.",
)

caja_alerta(
    "**No se afirma que se haya probado una decisión empresarial equivocada.** La conclusión se formula "
    "en términos de **riesgo analítico**: tomar decisiones sobre datos sin auditar es arriesgado y "
    "medible en este caso -- no que ya se haya demostrado un error concreto de Airbnb o de un anfitrión."
)
st.markdown(
    "> *La calidad de los datos no se reduce al porcentaje de valores nulos — y una diferencia en las "
    "métricas, por sí sola, nunca demuestra un impacto empresarial real sin investigar qué la produce.*"
)
