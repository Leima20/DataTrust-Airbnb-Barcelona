import streamlit as st

from src.data_loader import cargar_impacto_negocio, cargar_modelo
from src.styles import kicker, caja_alerta, fmt_num, COLOR_TRATADO, AMBAR_PENDIENTE, OCRE_DORADO_TEXTO
from src.charts import (
    reclasificacion_anuncios, ingreso_particular_profesional,
    perfil_tipo_habitacion, perfil_precio_mediana,
)

impacto = cargar_impacto_negocio()
modelo = cargar_modelo()

kicker("Página 4 de 9")
st.title("El hallazgo crítico: un cero no siempre es un cero real")

st.markdown("---")

# --- BLOQUE 1: los 4.181 casos con HTML Flexbox seguro ---
st.markdown("### 1. Los 4.181 casos")
no_est = impacto.get("no_estimable", {})
regla_original = impacto.get("experimento_decision", {}).get("regla_original", {})
cantidad_fmt = f"{regla_original.get('descartados_n', 0):,}".replace(",", ".")
pct_fmt = f"{fmt_num(regla_original.get('descartados_pct', 0), 1)}%"

html_punto_1 = f"""
<div style="background: #fafafa; border: 1px solid #e0e0e0; border-radius: 10px; padding: 1.2rem; margin-bottom: 0.8rem;">
    <div style="display: flex; gap: 2rem; width: 100%; align-items: center;">
        <div style="flex: 1; border-right: 1px solid #e0e0e0; padding-right: 1rem;">
            <div style="font-size: 0.85rem; color: #666; margin-bottom: 0.2rem;">Volumen total detectado</div>
            <div style="font-size: 2rem; font-weight: 600; color: #31333F; line-height: 1.2;">{cantidad_fmt} <span style="font-size: 1rem; font-weight: 400; color: #888;">→ <code>estimated_revenue_l365d</code></span></div>
            <div style="font-size: 0.8rem; color: #555; margin-top: 0.3rem;">Anuncios con ingreso cero</div>
        </div>
        <div style="flex: 2;">
            <div style="font-size: 1.3rem; font-weight: 600; color: #31333F;">{pct_fmt} de los anuncios con dato</div>
            <div style="font-size: 0.9rem; color: #555; margin-top: 0.3rem;">Representan el núcleo de la distorsión analítica detectada en la plataforma.</div>
        </div>
    </div>
</div>
"""
st.markdown(html_punto_1, unsafe_allow_html=True)

st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)

# --- BLOQUE 2: flujograma del calculo ---
st.markdown("### 2. Cómo calcula Inside Airbnb los ingresos, y qué se hace con los ceros")
t = modelo.get("target", {})
dot_revenue = r"""
digraph Flujo {
  rankdir=LR;
  node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=13, margin=0.18, color="#14506B"];
  edge [fontname="Helvetica", fontsize=11, color="#888888"];

  subgraph cluster_airbnb {
    label="Fórmula de Inside Airbnb";
    fontname="Helvetica";
    fontsize=12;
    fontcolor="#555555";
    style=filled;
    color="#F2F4F6";

    anuncio [label="Anuncio:\nreseñas recientes (number_of_reviews_ltm),\nestancia mínima (minimum_nights), price", fillcolor="#EAF2F8"];
    ocupacion [label="estimated_occupancy_l365d:\nreseñas recientes ÷ 50%\n× duración media", fillcolor="#EAF2F8"];
    ingreso [label="estimated_revenue_l365d\n= ocupación × price", fillcolor="#EAF2F8"];
    espacio_airbnb [label="", style=invis, width=0.01, height=0.01];
    anuncio -> ocupacion -> ingreso;
    ocupacion -> espacio_airbnb [style=invis];
  }

  subgraph cluster_proyecto {
    label="Decisión propia del proyecto";
    fontname="Helvetica";
    fontsize=12;
    fontcolor="#555555";
    style=filled;
    color="#F2F4F6";

    decision [label="¿0 reseñas recientes\nY estancia ≥ 28 noches?", shape=diamond, fillcolor="#FFF3DC", color="#C98A1B"];
    no_estimable [label="Se crea la variable\n'No estimable'\n(bandera -- dato intacto)", fillcolor="#FFF3DC", color="#C98A1B"];
    valido [label="Valor usable\n(cero real o ingreso > 0)", fillcolor="#FFF3DC", color="#C98A1B"];
    decision -> no_estimable [label="Sí"];
    decision -> valido [label="No"];
  }

  ingreso -> decision;
}
"""
st.graphviz_chart(dot_revenue, width="stretch")
with st.expander("Ver fórmula completa, columnas usadas y definición exacta"):
    st.markdown("**Columnas que forman la fórmula del target** (excluidas como predictoras del modelo, para no hacer trampa):")
    st.markdown("\n".join(f"- `{c}`" for c in t.get("excluidas_por_fuga", [])))
    st.caption(t.get("nota_fuga", ""))
    st.info(
        "📐 **Fórmula documentada (Inside Airbnb):**\n\n"
        "• **`estimated_occupancy_l365d`:** (Reseñas últimos 365 días ÷ tasa de conversión del 50%) × duración media de estancia (tope de ocupación del 70%).\n"
        "• **`estimated_revenue_l365d`:** Ocupación estimada × `price` (verificado empíricamente: `revenue / price` coincide exactamente con la ocupación, con error de redondeo < 0,0001).\n\n"
        "🔗 [insideairbnb.com/data-assumptions](https://insideairbnb.com/data-assumptions/)"
    )
    st.markdown(f"**Definición exacta de 'no estimable'**: {no_est.get('definicion', '')}")
    st.markdown(f"**Qué se hizo con ellos**: {no_est.get('tratamiento', '')}")

st.markdown("---")

# --- BLOQUE 3: Impacto en el mercado ---
st.markdown("### 3. Cómo cambia la interpretación: ceros auditados vs. sin auditar")
naive = impacto.get("gap_naive", {})
corregido = impacto.get("gap_corregido", {})
if naive and corregido:
    st.plotly_chart(
        ingreso_particular_profesional(
            naive.get("particular_media", 0), corregido.get("particular_media", 0),
            naive.get("profesional_media", 0), corregido.get("profesional_media", 0),
        ),
        width="stretch",
    )
    mediana_corregida_fmt = fmt_num(corregido.get('profesional_mediana', 0))
    gap_naive_fmt = fmt_num(naive.get('gap_eur', 0))
    gap_corregido_fmt = fmt_num(corregido.get('gap_eur', 0))
    caja_alerta(
        f"En la versión ingenua, el **ingreso mediano de los profesionales es 0€** — una señal de alerta "
        f"de que algo anda mal con el dato, no de que la mitad de los anfitriones profesionales no ganen "
        f"nada. Al excluir los 2.686 casos no estimables, la mediana profesional sube a "
        f"{mediana_corregida_fmt} € y la brecha particular-profesional baja de "
        f"{gap_naive_fmt} € ({fmt_num(naive.get('gap_pct', 0), 1)}%) a "
        f"{gap_corregido_fmt} € ({fmt_num(corregido.get('gap_pct', 0), 1)}%)."
    )

st.markdown("---")

# --- BLOQUE 4: Simulación de decisión en tarjeta unificada de 3 columnas ---
st.markdown("### 4. Simulación de decisión: ¿cuántos anuncios cambian de categoría?")
exp = impacto.get("experimento_decision", {})
if exp:
    st.markdown(
        f"""
        <div style="background-color:#FFF8EC; border:2px solid {AMBAR_PENDIENTE}; border-radius:10px;
                    padding:0.8rem 1.3rem; margin-bottom:0.4rem;">
        <span style="font-size:1.05rem; font-weight:700; color:{OCRE_DORADO_TEXTO};">
        🧪 Simulación: ¿cómo cambia una regla de decisión al auditar los datos crudos?</span><br>
        <span style="font-size:0.9rem; color:#555;">{exp.get('escenario', '')}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    original = exp.get("regla_original", {})
    auditada = exp.get("regla_auditada", {})

    val_desc_n = fmt_num(original.get("descartados_n", 0))
    val_desc_pct = fmt_num(original.get('descartados_pct', 0), 1)
    val_rev_n = fmt_num(auditada.get("revision_n", 0))
    val_rev_pct = fmt_num(exp.get('cambian_clasificacion_pct_de_descartados', 0), 1)
    val_sig_n = fmt_num(auditada.get("siguen_descartados_n", 0))
    val_sig_pct = fmt_num(auditada.get('siguen_descartados_pct', 0), 1)

    def _tarjeta_momento(etiqueta, valor, subtexto, sub_etiqueta):
        st.markdown(
            f'<div style="background-color:white; border-top:4px solid {AMBAR_PENDIENTE}; '
            'border-radius:10px; padding:1rem 1.1rem; height:100%;">'
            f'<div style="font-size:0.85rem; font-weight:700; color:{OCRE_DORADO_TEXTO}; margin-bottom:0.5rem;">{etiqueta}</div>'
            f'<div style="font-size:1.8rem; font-weight:800; color:#31333F; line-height:1.1;">{valor}</div>'
            f'<div style="font-size:0.8rem; color:#777; margin-top:0.2rem;">{sub_etiqueta}</div>'
            f'<div style="font-size:0.85rem; color:#555; margin-top:0.3rem;">{subtexto}</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    c1, c2, c3 = st.columns(3)
    with c1:
        _tarjeta_momento("Momento 1 — Regla simple", val_desc_n, f"{val_desc_pct}% del universo", "Anuncios descartados")
    with c2:
        _tarjeta_momento("Momento 2 — Pasan a revisión", val_rev_n, f"{val_rev_pct}% de descartados", "Reclasificados")
    with c3:
        _tarjeta_momento("Momento 2 — Siguen descartados", val_sig_n, f"{val_sig_pct}% del universo", "No aptos")

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

    st.plotly_chart(
        reclasificacion_anuncios(
            auditada.get("revision_n", 0), 
            auditada.get("siguen_descartados_n", 0),
            titulo=f"Qué pasa con los {fmt_num(original.get('descartados_n', 0))} anuncios descartados por la regla original",
        ),
        width="stretch",
    )

    carac = exp.get("caracteristicas", {})
    rev_c = carac.get("revision", {})
    desc_c = carac.get("siguen_descartados", {})
    if rev_c and desc_c:
        st.markdown("**¿Qué tipo de anuncio pasa a revisión, comparado con el que sigue descartado?**")
        g1, g2 = st.columns(2)
        with g1:
            st.plotly_chart(
                perfil_tipo_habitacion(
                    rev_c.get("room_type_entire_pct", 0),
                    rev_c.get("room_type_private_pct", 0),
                    desc_c.get("room_type_entire_pct", 0),
                    desc_c.get("room_type_private_pct", 0),
                ),
                width="stretch",
            )
        with g2:
            st.plotly_chart(
                perfil_precio_mediana(
                    rev_c.get("price_mediana_entera_eur", 0),
                    rev_c.get("price_mediana_privada_eur", 0),
                    desc_c.get("price_mediana_entera_eur", 0),
                    desc_c.get("price_mediana_privada_eur", 0),
                ),
                width="stretch",
            )


st.markdown("---")

# --- BLOQUE 5: Cierre de la parte de negocio ---
st.markdown("### 5. Conclusiones")
st.markdown(
    f"""
    <div style="background-color:#E7ECF0; border-top:4px solid {COLOR_TRATADO}; border-radius:8px;
                padding:1rem 1.2rem;">
    <b style="color:{COLOR_TRATADO};">✓ Demostrado con datos</b>
    <ul style="margin-top:0.6rem; padding-left:1.1rem; font-size:0.95rem;">
    <li>Existen {cantidad_fmt} anuncios ({pct_fmt}) con <code>estimated_revenue_l365d = 0</code>, y no todos son ceros reales -- 2.686 de ellos quedan marcados como "no estimables" (0 reseñas recientes + estancia ≥ 28 noches).</li>
    <li>Excluirlos cambia la brecha particular-profesional de <b>39,7% a 23,1%</b>.</li>
    <li>El 64,2% de los anuncios descartados por la regla simple cambiarían de categoría con la regla auditada.</li>
    <li>En una simulación, un filtro ingenuo descartaría por igual los 4.181 anuncios con ingreso 0€. Pero 2.686 de ellos (los que pasan a revisión al auditar) son sobre todo alojamientos pequeños y baratos -- el segmento más accesible del mercado.</li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True,
)