import streamlit as st

from src.data_loader import cargar_impacto_negocio, cargar_modelo
from src.styles import (
    kicker, fmt_num, AZUL_NOCHE, TURQUESA, TURQUESA_TEXTO, AZUL_PETROLEO,
    OCRE_DORADO_TEXTO, AMBAR_PENDIENTE, VIOLETA, COLOR_SENSIBILIDAD_TEXTO,
)

impacto = cargar_impacto_negocio()
modelo = cargar_modelo()

kicker("Página 9 de 9")
st.title("Conclusiones y recomendaciones")

naive = impacto.get("gap_naive", {})
corregido = impacto.get("gap_corregido", {})
muestra_426 = modelo.get("muestra_comun_426", {}).get("resultados", {})
exp = impacto.get("experimento_decision", {})
auditada = exp.get("regla_auditada", {})

st.markdown("### Dos hipótesis, dos respuestas")


def _kpi_hipotesis(color, texto_kicker, antes, despues, contexto):
    st.markdown(
        f'<div style="padding:0.3rem 0 0.2rem 0;">'
        f'<div style="font-size:0.85rem; color:{color}; font-weight:700; text-transform:uppercase; '
        f'letter-spacing:0.6px; margin-bottom:0.5rem;">{texto_kicker}</div>'
        f'<div style="display:flex; align-items:baseline; gap:0.7rem; flex-wrap:wrap;">'
        f'<span style="font-size:2.4rem; font-weight:700; color:#31333F;">{antes}</span>'
        f'<span style="font-size:1.6rem; color:#aaa;">&rarr;</span>'
        f'<span style="font-size:2.4rem; font-weight:700; color:{color};">{despues}</span>'
        f'</div>'
        f'<div style="font-size:1rem; color:#555; margin-top:0.5rem; line-height:1.45;">{contexto}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


col_h1, col_h2 = st.columns(2)
with col_h1:
    _kpi_hipotesis(
        OCRE_DORADO_TEXTO, "Hipótesis 1 · Negocio",
        f"{fmt_num(naive.get('gap_pct', 0), 1)}%", f"{fmt_num(corregido.get('gap_pct', 0), 1)}%",
        "La brecha media particular-profesional cambia al investigar los 2.686 casos de ingreso "
        "estimado cero no estimables.",
    )
with col_h2:
    _kpi_hipotesis(
        TURQUESA, "Hipótesis 2 · Modelo (R²)",
        fmt_num(muestra_426.get("A_crudo", {}).get("r2", 0), 3),
        fmt_num(muestra_426.get("B_tratado_criterio_A", {}).get("r2", 0), 3),
        "El modelo tratado (B) mejora frente al crudo (A) en una comparación sobre 426 "
        "observaciones que ningún modelo vio durante el entrenamiento.",
    )

st.markdown("---")

tab1, tab4 = st.tabs(["Conclusiones demostradas", "Recomendaciones"])

with tab1:
    st.subheader("Qué cambió, y qué no, al investigar la calidad de los datos")

    def _fila_hallazgo(numero, color, texto):
        st.markdown(
            f'<div style="display:flex; gap:1rem; align-items:flex-start; padding:0.9rem 0; '
            f'border-bottom:1px solid #eee;">'
            f'<div style="min-width:2.2rem; height:2.2rem; border-radius:50%; background-color:{color}; '
            f'color:white; font-weight:700; font-size:1rem; display:flex; align-items:center; '
            f'justify-content:center; flex-shrink:0;">{numero}</div>'
            f'<div style="font-size:1.05rem; color:#333; line-height:1.55; padding-top:0.2rem;">{texto}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    _fila_hallazgo(
        "01", AZUL_PETROLEO,
        "Al investigar los 2.686 casos de ingreso estimado '0 €' no reales, la brecha de ingresos entre "
        f"particulares y profesionales cambia de <b>{fmt_num(naive.get('gap_pct', 0), 1)}%</b> a "
        f"<b>{fmt_num(corregido.get('gap_pct', 0), 1)}%</b> -- un cambio de conclusión de negocio, no solo "
        "un ajuste cosmético.",
    )
    _fila_hallazgo(
        "02", TURQUESA,
        "Sobre 426 observaciones que ningún modelo vio durante el entrenamiento, el modelo con variables y "
        "población tratadas (B) predice mejor que el modelo con los datos crudos (A): el R² sube de "
        f"<b>{fmt_num(muestra_426.get('A_crudo', {}).get('r2', 0), 3)}</b> a "
        f"<b>{fmt_num(muestra_426.get('B_tratado_criterio_A', {}).get('r2', 0), 3)}</b>.",
    )
    _fila_hallazgo(
        "03", COLOR_SENSIBILIDAD_TEXTO,
        "Esa conclusión no depende de qué criterio de imputación se use (por capacidad o por barrio): la "
        "diferencia es de <b>menos del 0,1%</b> en el error del modelo (MAE) -- es robusta al criterio elegido.",
    )
    _fila_hallazgo(
        "04", AMBAR_PENDIENTE,
        "Un inversor que descartara automáticamente cualquier anuncio con ingreso estimado = 0 (dato "
        f"crudo) se equivocaría en el <b>{fmt_num(exp.get('cambian_clasificacion_pct_de_descartados', 0), 1)}%</b> "
        f"de esos descartes ({fmt_num(auditada.get('revision_n', 0))} anuncios): merecían 'revisión', no "
        "ser descartados. Simulación sobre datos reales, no una decisión de inversión real.",
    )

with tab4:
    st.subheader("De las conclusiones a las acciones")

    def _pilar(color, icono, titulo, items):
        filas = "".join(
            f'<div style="display:flex; gap:0.7rem; align-items:flex-start; margin-bottom:0.8rem;">'
            f'<span style="min-width:1.5rem; height:1.5rem; border-radius:50%; background-color:{color}1A; '
            f'color:{color}; font-weight:700; font-size:0.85rem; display:flex; align-items:center; '
            f'justify-content:center; flex-shrink:0;">&check;</span>'
            f'<span style="font-size:1.05rem; color:#444; line-height:1.5;">{item}</span>'
            f'</div>'
            for item in items
        )
        st.markdown(
            f'<div style="border-radius:10px; overflow:hidden; border:1px solid #e3e6ea; height:100%;">'
            f'<div style="background-color:{color}; color:white; padding:0.8rem 1.1rem; font-weight:700; '
            f'font-size:1.15rem; display:flex; align-items:center; gap:0.6rem;">'
            f'<span style="font-size:1.35rem;">{icono}</span>{titulo}</div>'
            f'<div style="padding:1.1rem 1.1rem 0.3rem 1.1rem;">{filas}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        _pilar(
            AZUL_PETROLEO, "🔍", "Calidad de datos",
            [
                "Investigar la <b>semántica</b> de las variables antes de tratar sus valores (el caso de "
                "los 2.686 ceros 'no estimables' no se habría encontrado solo mirando el % de nulos).",
                "Separar explícitamente valores desconocidos de ceros reales en cualquier variable objetivo.",
            ],
        )
    with col_r2:
        _pilar(
            TURQUESA, "⚙️", "Modelado y validación",
            [
                "Evitar fugas entre entrenamiento y evaluación, especialmente al comparar modelos "
                "entrenados sobre poblaciones de origen distintas.",
                "Usar conjuntos de comparación equivalentes al evaluar dos versiones de un modelo.",
                "Revisar la calidad de los datos <b>antes</b> de interpretar las métricas, no después.",
            ],
        )
    with col_r3:
        _pilar(
            OCRE_DORADO_TEXTO, "📋", "Gobernanza y procesos",
            [
                "Documentar las reglas de limpieza con la misma trazabilidad que una decisión de negocio.",
                "Registrar las transformaciones para garantizar la reproducibilidad.",
            ],
        )

    st.markdown("---")

    st.markdown(
        f'<div style="display:flex; justify-content:center; align-items:center; gap:1.1rem; '
        f'margin:0.6rem 0 1.5rem 0; flex-wrap:wrap;">'
        f'<span style="background-color:{AZUL_PETROLEO}1A; color:{AZUL_PETROLEO}; font-weight:700; '
        f'font-size:1.2rem; padding:0.6rem 1.3rem; border-radius:999px;">Calidad de datos</span>'
        f'<span style="color:#aaa; font-size:1.6rem;">&rarr;</span>'
        f'<span style="background-color:{TURQUESA}1A; color:{TURQUESA_TEXTO}; font-weight:700; '
        f'font-size:1.2rem; padding:0.6rem 1.3rem; border-radius:999px;">Confianza en el análisis</span>'
        f'<span style="color:#aaa; font-size:1.6rem;">&rarr;</span>'
        f'<span style="background-color:{VIOLETA}1A; color:{VIOLETA}; font-weight:700; '
        f'font-size:1.2rem; padding:0.6rem 1.3rem; border-radius:999px;">Mejores decisiones</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div style="text-align:center; font-size:1.9rem; font-weight:700; color:{AZUL_NOCHE}; '
        f'line-height:1.5; margin:0.5rem auto 1rem auto; max-width:780px;">'
        f'"La calidad de los datos no es un detalle técnico: puede cambiar tanto las conclusiones de negocio '
        f'como el rendimiento de un modelo."'
        f'</div>',
        unsafe_allow_html=True,
    )
