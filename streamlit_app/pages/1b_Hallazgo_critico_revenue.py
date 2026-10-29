import pandas as pd
import streamlit as st

from src.data_loader import cargar_impacto_negocio, cargar_modelo
from src.styles import kicker, caja_alerta, fmt_num
from src.charts import reclasificacion_anuncios

impacto = cargar_impacto_negocio()
modelo = cargar_modelo()

kicker("Pagina 4 de 9")
st.title("El hallazgo crítico: cuando cero no significa cero")
st.markdown(
    "Durante la auditoría surgió algo que merece su propio espacio, aparte de la lista de 14 hallazgos: "
    "**2.686 anuncios** (20,1% de los que tienen dato) con `estimated_revenue_l365d = 0`. ¿Son ingresos "
    "reales de cero, o algo distinto? La interpretación de las diferencias entre grupos cambia al "
    "investigar los valores cero."
)

st.markdown("---")

# --- BLOQUE 1: ¿Qué es y cómo se identificó? (Con fórmulas visibles y limpias) ---
col_A, col_B = st.columns(2)

with col_A:
    with st.container(border=True):
        st.markdown("### 1. ¿Qué es `estimated_revenue_l365d`?")
        t = modelo.get("target", {})
        st.markdown(
            f"Es una **estimación** que calcula Inside Airbnb a partir de otras columnas del anuncio -- "
            f"no es un ingreso real observado (no hay datos de reservas reales). Se construye combinando "
            + ", ".join(f"`{c}`" for c in t.get("excluidas_por_fuga", []))
            + f". {t.get('nota_fuga', '')}"
        )
        # Fórmula visible directamente aquí, donde se origina el problema
        st.info(
            "📐 **Fórmula documentada (Inside Airbnb):**\n\n"
            "• **`estimated_occupancy_l365d`:** (Reseñas últimos 365 días ÷ tasa de conversión del 50%) × duración media de estancia (tope de ocupación del 70%).\n"
            "• **`estimated_revenue_l365d`:** Ocupación estimada × `price` (verificado empíricamente: `revenue / price` coincide exactamente con la ocupación, con error de redondeo < 0,0001).\n\n"
            "🔗 [insideairbnb.com/data-assumptions](https://insideairbnb.com/data-assumptions/)"
        )

with col_B:
    with st.container(border=True):
        st.markdown("### 2. ¿Cómo se identificaron los 2.686 casos?")
        no_est = impacto.get("no_estimable", {})
        m1, m2 = st.columns(2)
        m1.metric("Anuncios no estimables", f"{no_est.get('cantidad', 0):,}".replace(",", "."))
        m2.metric("% de los que tienen dato", f"{fmt_num(no_est.get('pct_de_los_que_tienen_dato', 0), 1)}%")
        st.markdown(f"**Definición exacta**: {no_est.get('definicion', '')}")

# --- BLOQUE 2: ¿Por qué 'no estimable'? (Oculto en un desplegable para no saturar) ---
with st.expander("3. ¿Por qué 'no estimable' y no 'ingreso real cero'?"):
    st.markdown(
        "Dado que la fórmula documentada se basa en contar reseñas de los últimos 365 días, el patrón "
        "observado (0 reseñas recientes **y** estancia mínima de 28+ noches) **es compatible con** que la "
        "fórmula no tenga con qué estimar ingresos ahí -- un huésped de estancia muy larga deja como mucho "
        "una reseña al año, así que con 0 reseñas recientes no hay insumo para el cálculo, aunque el "
        "alojamiento esté ocupado. Esto no es evidencia de que el anuncio no genere ingresos reales. Tratar "
        "estos casos como si fueran 0€ reales mezclaría 'no se puede saber' con 'se sabe que es cero', dos "
        "cosas distintas."
    )

st.markdown("---")

# --- BLOQUE 3: Impacto en el mercado (Particular vs Profesional) ---
st.markdown("### 4. Cómo cambia la interpretación: particular vs. profesional")
st.caption(
    "**'Profesional'** -- anfitrión con más de 50 anuncios en Barcelona "
    "(`calculated_host_listings_count > 50`): una distinción propia del proyecto, no de Airbnb, que "
    "mide gestión en la plataforma, no propiedad."
)
naive = impacto.get("gap_naive", {})
corregido = impacto.get("gap_corregido", {})
if naive and corregido:
    df_comp = pd.DataFrame([
        {
            "Versión": "Conclusión ingenua (sin investigar los ceros)",
            "Particular (media)": f"{fmt_num(naive.get('particular_media', 0))} €",
            "Profesional (media)": f"{fmt_num(naive.get('profesional_media', 0))} €",
            "Brecha (entre medias)": f"{fmt_num(naive.get('gap_eur', 0))} € ({fmt_num(naive.get('gap_pct', 0), 1)}%)",
        },
        {
            "Versión": "Conclusión corregida (excluyendo los 2.686 no estimables)",
            "Particular (media)": f"{fmt_num(corregido.get('particular_media', 0))} €",
            "Profesional (media)": f"{fmt_num(corregido.get('profesional_media', 0))} €",
            "Brecha (entre medias)": f"{fmt_num(corregido.get('gap_eur', 0))} € ({fmt_num(corregido.get('gap_pct', 0), 1)}%)",
        },
    ])
    st.dataframe(df_comp, width="stretch", hide_index=True)
    mediana_corregida_fmt = fmt_num(corregido.get('profesional_mediana', 0))
    caja_alerta(
        f"En la version ingenua, el **ingreso mediano de los profesionales es 0€** -- una señal de alerta "
        f"de que algo anda mal con el dato, no de que la mitad de los anfitriones profesionales no ganen "
        f"nada. Al excluir los 2.686 casos no estimables, la mediana profesional sube a "
        f"{mediana_corregida_fmt} € y la brecha particular-profesional baja de "
        f"{fmt_num(naive.get('gap_pct', 0), 1)}% al {fmt_num(corregido.get('gap_pct', 0), 1)}%."
    )

st.markdown("---")

# --- BLOQUE 4: Simulación de decisión y Conclusiones (En desplegables limpios) ---
with st.expander("5. Simulación de decisión: ¿cuántos anuncios cambian de categoría?"):
    exp = impacto.get("experimento_decision", {})
    if exp:
        st.markdown(exp.get("escenario", ""))
        st.warning(f"⚠️ {exp.get('aviso_evidencia', '')}")

        universo = exp.get("universo_n", 0)
        original = exp.get("regla_original", {})
        auditada = exp.get("regla_auditada", {})
        st.caption(
            f"Universo: {fmt_num(universo)} anuncios con dato en `estimated_revenue_l365d` "
            f"({exp.get('universo_nota', '')})"
        )
        c1, c2 = st.columns(2)
        c1.metric("Regla original -- descartados", f"{fmt_num(original.get('descartados_n', 0))}",
                  f"{fmt_num(original.get('descartados_pct', 0), 1)}% del universo")
        c2.metric("De esos, pasan a 'revisión' con la regla auditada",
                  f"{fmt_num(auditada.get('revision_n', 0))}",
                  f"{fmt_num(exp.get('cambian_clasificacion_pct_de_descartados', 0), 1)}% de los descartados")

        st.plotly_chart(
            reclasificacion_anuncios(
                auditada.get("revision_n", 0), auditada.get("siguen_descartados_n", 0),
                titulo=f"Qué pasa con los {fmt_num(original.get('descartados_n', 0))} anuncios descartados por la regla original",
            ),
            width="stretch",
        )
        desglose = exp.get("desglose_siguen_descartados", {})
        st.caption(
            f"Los {fmt_num(auditada.get('siguen_descartados_n', 0))} que siguen descartados "
            f"({fmt_num(auditada.get('siguen_descartados_pct', 0), 1)}% del universo) no entran en el patrón: "
            f"{desglose.get('nota', '')}"
        )

        carac = exp.get("caracteristicas", {})
        rev_c = carac.get("revision", {})
        desc_c = carac.get("siguen_descartados", {})
        if rev_c and desc_c:
            st.markdown("**¿Qué tipo de anuncio pasa a revisión, comparado con el que sigue descartado?**")
            df_carac = pd.DataFrame([
                {"Grupo": "Pasan a revisión", "Habitación entera": f"{fmt_num(rev_c.get('room_type_entire_pct', 0), 1)}%",
                 "Habitación privada": f"{fmt_num(rev_c.get('room_type_private_pct', 0), 1)}%",
                 "Precio mediana": f"{fmt_num(rev_c.get('price_mediana_eur', 0), 1)} €",
                 "Capacidad mediana": fmt_num(rev_c.get('accommodates_mediana', 0), 1)},
                {"Grupo": "Siguen descartados", "Habitación entera": f"{fmt_num(desc_c.get('room_type_entire_pct', 0), 1)}%",
                 "Habitación privada": f"{fmt_num(desc_c.get('room_type_private_pct', 0), 1)}%",
                 "Precio mediana": f"{fmt_num(desc_c.get('price_mediana_eur', 0), 1)} €",
                 "Capacidad mediana": fmt_num(desc_c.get('accommodates_mediana', 0), 1)},
            ])
            st.dataframe(df_carac, width="stretch", hide_index=True)
            st.caption(carac.get("nota", ""))

        caja_alerta(exp.get("limites", ""))

with st.expander("6. Qué se ha demostrado y qué sigue siendo una hipótesis"):
    st.success(
        "**Demostrado**: los 2.686 casos existen, comparten ese patrón doble (0 reseñas recientes + estancia "
        "mínima 28+ noches), excluirlos cambia la brecha particular-profesional de 39,7% a 23,1%, y bajo una "
        "regla de decisión simple que descarta todo ingreso=0, el 64,2% de los anuncios descartados cambiarían "
        "de categoría si se aplica la interpretación auditada -- un cambio de clasificación medido con datos "
        "reales, no una decisión de inversión real ni una pérdida económica observada."
    )
    st.warning(
        "**Hipótesis razonable, no demostrada causalmente**: que el mecanismo exacto sea 'una estancia tan "
        "larga no puede completarse dentro de la ventana de reseñas recientes' es la explicación más simple "
        "y coherente con como Inside Airbnb documenta el calculo, pero no se investigó la causa raíz dentro "
        "de la propia plataforma de Inside Airbnb."
    )