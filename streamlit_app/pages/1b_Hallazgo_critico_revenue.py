import streamlit as st

from src.data_loader import cargar_impacto_negocio, cargar_modelo
from src.styles import kicker, caja_alerta, fmt_num, VERDE_OK, AMBAR_PENDIENTE
from src.charts import (
    reclasificacion_anuncios, ingreso_particular_profesional,
    perfil_tipo_habitacion, perfil_precio_mediana,
)

impacto = cargar_impacto_negocio()
modelo = cargar_modelo()

kicker("Página 4 de 9")
st.title("El hallazgo crítico: cuando cero no significa cero")
st.markdown(
    "Durante la auditoría surgió algo que merece su propio espacio, aparte de la lista de 14 hallazgos: "
    "**2.686 anuncios** (20,1% de los que tienen dato) con `estimated_revenue_l365d = 0`. ¿Son ingresos "
    "reales de cero, o algo distinto? La interpretación de las diferencias entre grupos cambia al "
    "investigar los valores cero."
)

st.markdown("---")

# --- BLOQUE 1: los 2.686 casos con HTML Flexbox seguro ---
st.markdown("### 1. Los 2.686 casos")
no_est = impacto.get("no_estimable", {})
cantidad_fmt = f"{no_est.get('cantidad', 0):,}".replace(",", ".")
pct_fmt = f"{fmt_num(no_est.get('pct_de_los_que_tienen_dato', 0), 1)}%"

html_punto_1 = f"""
<div style="background: #fafafa; border: 1px solid #e0e0e0; border-radius: 10px; padding: 1.2rem; margin-bottom: 0.8rem;">
    <div style="display: flex; gap: 2rem; width: 100%; align-items: center;">
        <div style="flex: 1; border-right: 1px solid #e0e0e0; padding-right: 1rem;">
            <div style="font-size: 0.85rem; color: #666; margin-bottom: 0.2rem;">Volumen total detectado</div>
            <div style="font-size: 2rem; font-weight: 600; color: #31333F; line-height: 1.2;">{cantidad_fmt}</div>
            <div style="font-size: 0.8rem; color: #555; margin-top: 0.3rem;">Anuncios con ingreso cero</div>
        </div>
        <div style="flex: 2;">
            <div style="font-size: 1.3rem; font-weight: 600; color: #31333F;">{pct_fmt} de los anuncios con dato</div>
            <div style="font-size: 0.9rem; color: #555; margin-top: 0.3rem;">Representan el núcleo de la distorsión analítica detectada en la plataforma.</div>
        </div>
    </div>
    <div style="margin-top: 0.9rem; background-color: #f8f9fa; border: 1px solid #e0e0e0; border-left: 4px solid {AMBAR_PENDIENTE}; border-radius: 6px; padding: 0.6rem 0.9rem; font-size: 0.85rem; color: #555;">
        💡 <b>Nota:</b> <i>'No estimable'</i> no es un dato oficial de Inside Airbnb — es una variable propia (<code>revenue_no_estimable</code>) para marcar este patrón. Cómo se calcula, en el punto 2.
    </div>
</div>
"""
st.markdown(html_punto_1, unsafe_allow_html=True)

st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)

# --- BLOQUE 2: flujograma del calculo ---
st.markdown("### 2. De dónde sale el ingreso estimado, y por qué a veces es 'no estimable'")
t = modelo.get("target", {})
dot_revenue = r"""
digraph Flujo {
  rankdir=LR;
  node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=13, margin=0.18, color="#14506B"];
  edge [fontname="Helvetica", fontsize=11, color="#888888"];

  anuncio [label="Anuncio\n(reseñas, estancia, price)", fillcolor="#EAF2F8"];
  ocupacion [label="Ocupación estimada\nreseñas recientes ÷ 50%\n× duración media", fillcolor="#EAF2F8"];
  ingreso [label="estimated_revenue_l365d\n= ocupación × price", fillcolor="#EAF2F8"];
  decision [label="¿0 reseñas recientes\nY estancia ≥ 28 noches?", shape=diamond, fillcolor="#FFF8EC"];
  no_estimable [label="No estimable\n(bandera -- dato intacto)", fillcolor="#FFF3DC", color="#C98A1B"];
  valido [label="Valor usable\n(cero real o ingreso > 0)", fillcolor="#E7F6E7", color="#0CA30C"];

  anuncio -> ocupacion -> ingreso -> decision;
  decision -> no_estimable [label="Sí"];
  decision -> valido [label="No"];
}
"""
st.graphviz_chart(dot_revenue, width="stretch")
st.caption(
    "No es evidencia de que esos 2.686 anuncios generen 0€ reales — es que la fórmula no tiene con qué "
    "estimar ahí (sin reseñas recientes, sin insumo para el cálculo). Se marcan con una bandera; el dato "
    "original no se borra ni se inventa."
)
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
st.markdown("### 3. Cómo cambia la interpretación: particular vs. profesional")
st.caption(
    "**'Profesional'** — anfitrión con más de 50 anuncios en Barcelona "
    "(`calculated_host_listings_count > 50`). **'Particular'** — el resto, 50 anuncios o menos en "
    "Barcelona. Es una distinción propia del proyecto, no de Airbnb, que mide gestión en la "
    "plataforma, no propiedad."
)
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
    caja_alerta(
        f"En la versión ingenua, el **ingreso mediano de los profesionales es 0€** — una señal de alerta "
        f"de que algo anda mal con el dato, no de que la mitad de los anfitriones profesionales no ganen "
        f"nada. Al excluir los 2.686 casos no estimables, la mediana profesional sube a "
        f"{mediana_corregida_fmt} € y la brecha particular-profesional baja de "
        f"{fmt_num(naive.get('gap_pct', 0), 1)}% al {fmt_num(corregido.get('gap_pct', 0), 1)}%."
    )

st.markdown("---")

# --- BLOQUE 4: Simulación de decisión en tarjeta unificada de 3 columnas ---
st.markdown("### 4. Simulación de decisión: ¿cuántos anuncios cambian de categoría?")
exp = impacto.get("experimento_decision", {})
if exp:
    st.markdown(
        f"""
        <div style="background-color:#FFF8EC; border:2px solid {AMBAR_PENDIENTE}; border-radius:10px;
                    padding:1rem 1.3rem; margin-bottom:1rem;">
        <span style="font-size:1.05rem; font-weight:700; color:{AMBAR_PENDIENTE};">
        🧪 Simulación: ¿cómo cambia una regla de decisión al auditar los datos crudos?</span><br>
        <span style="font-size:0.9rem; color:#555;">{exp.get('escenario', '')}</span><br>
        <span style="font-size:0.88rem; color:#555;">⚠️ {exp.get('aviso_evidencia', '')}</span>
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

    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown("**Momento 1 — Regla simple**")
            st.metric(
                "Anuncios descartados", 
                val_desc_n,
                f"{val_desc_pct}% del universo", 
                delta_color="off"
            )
            
        with c2:
            st.markdown("**Momento 2 — Pasan a revisión**")
            st.metric(
                "Reclasificados", 
                val_rev_n,
                f"{val_rev_pct}% de descartados"
            )
            
        with c3:
            st.markdown("**Momento 2 — Siguen descartados**")
            st.metric(
                "No aptos", 
                val_sig_n,
                f"{val_sig_pct}% del universo", 
                delta_color="off"
            )

    # --- NOTA METODOLÓGICA ABAJO A TODO EL ANCHO ---
    st.markdown(
        f"""
        <div style="background-color:#f8f9fa; border:1px solid #e0e0e0; border-left:4px solid {AMBAR_PENDIENTE}; border-radius:6px; padding:0.7rem 1rem; font-size:0.85rem; color:#555; margin-top:0.8rem; margin-bottom:1.2rem;">
        💡 <b>Nota metodológica:</b> <i>'No estimable'</i> no es un dato de Inside Airbnb — es una variable propia (<code>revenue_no_estimable</code>) para aislar el mismo patrón (0 reseñas recientes + estancia ≥ 28 noches). Recálculo directo sobre el CSV crudo: verifica exactamente los <b>2.686 IDs</b> del punto 1 (no introduce un grupo nuevo de datos).
        </div>
        """,
        unsafe_allow_html=True,
    )

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
            st.caption(
                f"Más peso de habitación privada entre los que pasan a revisión "
                f"({fmt_num(rev_c.get('room_type_private_pct', 0), 1)}% vs. "
                f"{fmt_num(desc_c.get('room_type_private_pct', 0), 1)}%)."
            )
        with g2:
            st.plotly_chart(
                perfil_precio_mediana(
                    rev_c.get("price_mediana_eur", 0), 
                    desc_c.get("price_mediana_eur", 0)
                ),
                width="stretch",
            )
            st.caption(
                f"También más baratos de mediana ({fmt_num(rev_c.get('price_mediana_eur', 0), 1)} € vs. "
                f"{fmt_num(desc_c.get('price_mediana_eur', 0), 1)} €)."
            )
        
        st.caption(
            "Los anuncios que pasan a revisión tienden a ser más pequeños, más baratos y con más peso de habitación privada "
            "que los que siguen descartados — un patrón descriptivo compatible con alojamientos de estancia larga, "
            "no una prueba de que estén ocupados o generen ingresos reales."
        )

    caja_alerta(
        "No se afirma que los anuncios en revisión sean rentables ni que generen ingresos reales — no hay datos de reservas/"
        "ingresos reales en este dataset. Esto es un cambio de clasificación cuantificado, no una decisión de inversión real "
        "observada ni una pérdida/ganancia económica medida. La 'regla auditada' es una alternativa más prudente para este patrón "
        "observado, no una regla universalmente correcta ni validada de forma definitiva — identifica casos potencialmente no estimables, "
        "no casos confirmados de ingresos reales no registrados."
    )

st.markdown("---")

# --- BLOQUE 5: Demostrado vs. hipotesis ---
st.markdown("### 5. Qué se ha demostrado y qué sigue siendo una hipótesis")
cd, ch = st.columns(2)
with cd:
    st.markdown(
        f"""
        <div style="background-color:#E7F6E7; border-top:4px solid {VERDE_OK}; border-radius:8px;
                    padding:1rem 1.2rem; height:100%;">
        <b style="color:{VERDE_OK};">✓ Demostrado con datos</b>
        <ul style="margin-top:0.6rem; padding-left:1.1rem; font-size:0.95rem;">
        <li>Los 2.686 casos existen y comparten el mismo patrón (0 reseñas recientes + estancia ≥ 28 noches).</li>
        <li>Excluirlos cambia la brecha particular-profesional de <b>39,7% a 23,1%</b>.</li>
        <li>El 64,2% de los anuncios descartados por la regla simple cambiarían de categoría con la regla auditada.</li>
        </ul>
        <span style="font-size:0.82rem; color:#555;">Es un cambio de clasificación medido con datos reales, no una decisión de inversión ni una pérdida/ganancia observada.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with ch:
    st.markdown(
        f"""
        <div style="background-color:#FFF8EC; border-top:4px solid {AMBAR_PENDIENTE}; border-radius:8px;
                    padding:1rem 1.2rem; height:100%;">
        <b style="color:{AMBAR_PENDIENTE};">? Hipótesis abierta, no demostrada</b>
        <ul style="margin-top:0.6rem; padding-left:1.1rem; font-size:0.95rem;">
        <li>Una estancia tan larga no cabe dentro de la ventana de reseñas recientes de la fórmula — es la explicación más simple y coherente con la documentación de Inside Airbnb.</li>
        <li>No se investigó la causa raíz dentro de la propia plataforma de Inside Airbnb.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )