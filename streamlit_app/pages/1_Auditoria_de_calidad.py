import html

import pandas as pd
import streamlit as st

from src.data_loader import cargar_calidad, cargar_contexto, cargar_geografia_distrito, cargar_geojson_barrios
from src.styles import kicker, fmt_num, AZUL_OSCURO, AZUL_PETROLEO, TURQUESA, AZUL_PIZARRA, ROJO_ALERTA, AMBAR_PENDIENTE, VERDE_OK, GRIS_TEXTO
from src.charts import completitud_por_columna, licencia_categorias, mapa_licencia_distrito, hallazgos_por_tabla, huerfanas_por_tabla

calidad = cargar_calidad()
contexto = cargar_contexto()
hallazgos = calidad.get("hallazgos_14", {})
decisiones = calidad.get("decisiones_tratamiento", {})

kicker("Pagina 3 de 9")
st.title("Auditoría de calidad")
st.markdown(
    "Se revisaron las 3 tablas del dataset (`listings`, `reviews`, `calendar`), cruzando cada columna "
    "contra 3 preguntas."
)

# ---------- 1. Alcance de la auditoria ----------
st.markdown("## 1. Alcance de la auditoría")
tablas = calidad.get("tablas", {})
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<span style='color:{AZUL_OSCURO}; font-weight:700;'>listings</span>", unsafe_allow_html=True)
    st.metric("Filas", f'{tablas.get("listings",{}).get("filas",0):,}'.replace(",", "."),
              f'{tablas.get("listings",{}).get("columnas_raw","—")} columnas', delta_color="off")
with c2:
    st.markdown(f"<span style='color:{TURQUESA}; font-weight:700;'>reviews</span>", unsafe_allow_html=True)
    st.metric("Filas", f'{tablas.get("reviews",{}).get("filas",0):,}'.replace(",", "."),
              f'{tablas.get("reviews",{}).get("columnas_raw","—")} columnas', delta_color="off")
with c3:
    st.markdown(f"<span style='color:{AZUL_PIZARRA}; font-weight:700;'>calendar</span>", unsafe_allow_html=True)
    st.metric("Filas", f'{tablas.get("calendar",{}).get("filas",0):,}'.replace(",", "."),
              f'{tablas.get("calendar",{}).get("columnas_raw","—")} columnas', delta_color="off")

st.markdown("---")

tab2, tab3, tab4, tab5 = st.tabs([
    "2. Dimensiones", "3. Resultados",
    "4. Gobernanza y tratamiento", "5. Conclusión",
])

# ---------- 2. Dimensiones de calidad ----------
with tab2:
    st.markdown("#### Dimensiones de calidad")
    dim_cols = st.columns(3)
    dimensiones = [
        ("🧩", "Completitud", "¿Falta información?"),
        ("🔗", "Integridad referencial", "¿Las filas conectan bien entre tablas?"),
        ("🔎", "Plausibilidad semántica", "¿Un valor 'válido' tiene sentido real?"),
    ]
    for col, (icono, titulo, pregunta) in zip(dim_cols, dimensiones):
        with col:
            with st.container(border=True):
                st.markdown(f"**{icono} {titulo}**")
                st.caption(pregunta)

    st.markdown("###### Cómo leer un hallazgo")
    st.caption(
        "No todo nulo es un error, y no todo cero es un error -- cada hallazgo cae en una de estas 4 "
        "categorías:"
    )

    def _chip_categoria(icono, titulo, bg, borde, color_texto):
        st.markdown(
            f"""
            <div style="background-color:{bg}; border:1px solid {borde}; border-radius:8px;
                        padding:0.5rem 0.7rem; text-align:center;">
            <span style="font-size:1.1rem;">{icono}</span><br>
            <span style="font-size:0.82rem; font-weight:700; color:{color_texto};">{titulo}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    cat_cols = st.columns(4)
    categorias_hallazgo = [
        ("⚠️", "Problema detectado", "#FDECEC", "#F0C9C9", "#D03B3B"),
        ("🔧", "Decisión de tratamiento", "#EAF2F8", "#C6DBEA", "#14506B"),
        ("📄", "Limitación de la fuente", "#ECEDEF", "#CBCFD4", "#555555"),
        ("❓", "Hipótesis pendiente de validar", "#FFF8EC", "#F0DDB3", "#C98A1B"),
    ]
    for col, (icono, titulo, bg, borde, color_texto) in zip(cat_cols, categorias_hallazgo):
        with col:
            _chip_categoria(icono, titulo, bg, borde, color_texto)

    st.markdown(
        f"**Nomenclatura de los IDs:** "
        f"<span style='color:{AZUL_OSCURO}; font-weight:700;'>L</span> = listings &nbsp;·&nbsp; "
        f"<span style='color:{TURQUESA}; font-weight:700;'>R</span> = reviews &nbsp;·&nbsp; "
        f"<span style='color:{AZUL_PIZARRA}; font-weight:700;'>C</span> = calendar "
        f"-- el número es el orden dentro de esa tabla, no correlativo entre tablas.",
        unsafe_allow_html=True,
    )

# ---------- 3. Resultados principales ----------
with tab3:
    st.markdown("#### Resultados principales")
    n_listings, n_reviews, n_calendar = len(hallazgos.get("listings", [])), len(hallazgos.get("reviews", [])), len(hallazgos.get("calendar", []))
    n_total = n_listings + n_reviews + n_calendar
    st.markdown(
        f"""
        <div style="text-align:center; padding:0.4rem 0 0.2rem 0;">
        <span style="font-size:3rem; font-weight:800; color:#0B3954;">{n_total}</span>
        <span style="font-size:1.15rem; color:#333; font-weight:600;"> Hallazgos encontrados en la auditoría</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col_chart = st.columns([1.5, 1, 1.5])[1]
    with col_chart:
        st.plotly_chart(hallazgos_por_tabla(n_listings, n_reviews, n_calendar), width="stretch")

    sub_completitud, sub_integridad, sub_plausibilidad = st.tabs([
        "📊 Completitud", "🔗 Integridad referencial", "📍 Plausibilidad",
    ])

    with sub_completitud:
        st.markdown(f"<span style='color:{AZUL_OSCURO}; font-weight:700;'>L1 · L2 · listings</span>", unsafe_allow_html=True)
        st.caption(
            "Se comprobó en las 3 tablas -- `reviews` y `calendar` salieron limpias (100% completas), el "
            "único hallazgo de esta dimensión está en `listings`."
        )
        st.markdown(
            f"**{calidad.get('columnas_100_nulas', {}).get('cantidad', '—')} columnas** de `listings` están "
            "100% vacías (`L1`) -- 0% de dato útil en toda la tabla."
        )
        nulos = calidad.get("nulos_parciales_L2", [])
        if nulos:
            cols_n = [n["columna"] for n in nulos]
            pcts_n = [n["pct_nulo"] for n in nulos]
            st.plotly_chart(completitud_por_columna(cols_n, pcts_n, "L2 — Nulos parciales en columnas predictoras"),
                             width="stretch")
            st.caption("Rojo = 20% o más de nulos. Estas 6 columnas son las que se usan como predictoras del "
                       "modelo (ver página 'Diseño experimental').")
        with st.expander("📝 Notas técnicas"):
            st.caption(
                "Las 12 columnas 100% vacías (`L1`): "
                + ", ".join(f"`{c}`" for c in calidad.get("columnas_100_nulas", {}).get("nombres", []))
                + "."
            )

    with sub_plausibilidad:
        st.markdown(f"<span style='color:{AZUL_OSCURO}; font-weight:700;'>L3 · L4 · listings</span>", unsafe_allow_html=True)
        st.markdown(
            "**El problema** -- el campo `license` debería contener un número de licencia turística "
            "legible, pero en la práctica mezcla formatos:\n\n"
            "- **21,1% no verificable** (`L3`: sin dato o texto no clasificable).\n"
            "- **5.470 registros con formato roto** (HTML sin limpiar o dos números de licencia "
            "concatenados en el mismo campo, `L4`)."
        )
        st.markdown(
            "**¿Por qué importa?**\n\n"
            "- Compliance o segmentación por licencia pierde fiabilidad para **1 de cada 5 anuncios** (`L3`).\n"
            "- Extraer patrones automáticamente del texto puede fallar o contar de más por el formato "
            "roto (`L4`)."
        )
        st.markdown("##### Marco legal de las licencias en el dataset")
        col_hutb, col_nrua = st.columns(2)
        with col_hutb:
            st.info(
                "**`HUTB` -- Registro catalán**\n\nCódigo del registro turístico de Cataluña "
                "('Habitatge d'Ús Turístic'). El formato histórico, el más frecuente en el dataset."
            )
        with col_nrua:
            st.info(
                "**`NRUA` -- Registro estatal**\n\nEl nuevo registro único a nivel nacional, creado por "
                "el Real Decreto 1312/2024 y obligatorio desde julio de 2025. Convive con el `HUTB`, "
                "no lo sustituye."
            )
        lic = calidad.get("licencia", {})
        cats = lic.get("categorias", [])
        if cats:
            st.plotly_chart(
                licencia_categorias([c["nombre"] for c in cats], [c["pct"] for c in cats]),
                width="stretch",
            )
            st.caption(f"Rojo = categorías no verificables (`L3`: {fmt_num(lic.get('no_verificable_L3_pct', 0), 1)}% "
                       "del campo `license`) -- no se asume incumplimiento legal, solo que no se puede confirmar.")
        geo = cargar_geografia_distrito()
        geojson = cargar_geojson_barrios()
        distritos_data = geo.get("distritos", [])
        if distritos_data and geojson:
            nombres_d = [d["distrito"] for d in distritos_data]
            pcts_d = [d["pct_problema"] for d in distritos_data]
            ns_d = [d["n_anuncios"] for d in distritos_data]
            st.plotly_chart(mapa_licencia_distrito(geojson, nombres_d, pcts_d, ns_d), width="stretch")
            peor, mejor = distritos_data[-1], distritos_data[0]
            st.caption(
                f"Rango: {fmt_num(mejor['pct_problema'], 1)}% (`{mejor['distrito']}`) a "
                f"{fmt_num(peor['pct_problema'], 1)}% (`{peor['distrito']}`)."
            )
        with st.expander("📝 Notas técnicas y hallazgos secundarios de Plausibilidad"):
            st.markdown(
                "**Contexto metodológico** -- esta dimensión abarca también `minimum_nights` en "
                "`listings` (`L5`), patrones en `reviews` (`R1`, `R3`, `R4`) y coherencia de fechas en "
                "`calendar` (`C2`); la licencia es el ejemplo más ilustrativo, no el único."
            )
            st.markdown("---")
            st.markdown(
                "**Patrón de negocio derivado** (no es un defecto de dato) -- `L6` y `L7` son el mismo "
                "dato de licencia (`L3`) mirado desde otro ángulo: `L6` lo cruza por tipo de anfitrión, "
                "`L7` por distrito."
            )
            st.caption(
                "**'Profesional'** -- anfitrión con más de 50 anuncios en Barcelona "
                "(`calculated_host_listings_count > 50`). **'Particular'** -- el resto, 50 anuncios o "
                "menos en Barcelona. Es una distinción propia del proyecto, no de Airbnb, que mide "
                "gestión en la plataforma, no propiedad."
            )
            col_l6, col_l7 = st.columns(2)
            l6 = next((h for h in hallazgos.get("listings", []) if h["id"] == "L6"), None)
            with col_l6:
                if l6:
                    st.info(f"**`L6`** -- {l6['resumen']}: {l6['detalle']}")
            with col_l7:
                st.info("**`L7`** -- Variación del problema de licencia por distrito. Ya se ve en el mapa de arriba, no se repite aquí.")

    with sub_integridad:
        r2 = next((h for h in hallazgos.get("reviews", []) if h["id"] == "R2"), None)
        c1_ = next((h for h in hallazgos.get("calendar", []) if h["id"] == "C1"), None)
        col_a, col_b = st.columns(2)
        if r2:
            with col_a:
                st.markdown(f"<span style='color:{TURQUESA}; font-weight:700;'>R2 · reviews</span>", unsafe_allow_html=True)
                st.metric("Filas huérfanas", "6.592", "0,64% de 1.033.523 filas", delta_color="off")
                st.caption(r2["detalle"])
        if c1_:
            with col_b:
                st.markdown(f"<span style='color:{AZUL_PIZARRA}; font-weight:700;'>C1 · calendar</span>", unsafe_allow_html=True)
                st.metric("Filas huérfanas", "41.245", "0,73% de 5.623.190 filas", delta_color="off")
                st.caption(c1_["detalle"])
        st.plotly_chart(huerfanas_por_tabla(0.64, 0.73), width="stretch")
        st.caption("Ambos se detectaron con SQL (`LEFT JOIN` contra `listings`), no pandas.")

        st.success(
            "**Verificaciones con resultado satisfactorio**:\n\n"
            "- `listings` -- `id` únicos, sin duplicados.\n"
            "- `reviews` -- 100% completos en sus 4 campos estructurales.\n"
            "- `calendar` -- 100% completo, sin duplicados, estructura perfecta (365 filas/alojamiento)."
        )
        with st.expander("📝 Notas técnicas"):
            st.caption(
                "113 listings × 365 filas/año = 41.245, la cifra exacta observada -- confirma que no es un "
                "problema de carga parcial de datos. La distribución de `price` en `listings` no tiene un "
                "límite de negocio objetivo que marque valores como sospechosos, y los nombres de barrio no "
                "tienen caracteres mal codificados."
            )

    with st.expander("Ver los 14 hallazgos completos, con su trazabilidad"):
        for grupo, titulo in [("listings", "Listings"), ("reviews", "Reviews"), ("calendar", "Calendar")]:
            filas_grupo = hallazgos.get(grupo, [])
            st.markdown(f"**{titulo}** ({len(filas_grupo)} hallazgos)")
            df = pd.DataFrame(filas_grupo)
            if not df.empty:
                df = df.rename(columns={"id": "ID", "resumen": "Hallazgo", "detalle": "Detalle"})
                st.dataframe(df, width="stretch", hide_index=True)


# ---------- 4. Decisiones de gobernanza ----------
with tab4:
    st.markdown("#### Gobernanza: la decisión")
    st.caption(
        "Cada uno de los 14 hallazgos cae en exactamente una de estas 3 categorías -- la decisión y su "
        "justificación quedan documentadas, no se improvisan caso por caso."
    )

    def _caja_gobernanza(titulo, descripcion, codigos, bg, borde, color_texto):
        st.markdown(
            f"""
            <div style="background-color:{bg}; border:1px solid {borde}; border-radius:10px;
                        padding:0.9rem 1.1rem; height:100%;">
            <b style="color:{color_texto};">{titulo}</b><br>
            <span style="font-size:0.82rem; color:#555;">{descripcion}</span><br><br>
            <span style="font-family:monospace; font-size:0.85rem; color:{color_texto};">
            {", ".join(codigos)}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    d1, d2, d3 = st.columns(3)
    with d1:
        _caja_gobernanza(
            "Cambio de datos",
            "Se modificó el valor original: imputación, eliminación de filas/columnas, o reformateo.",
            decisiones.get("ejecutadas_con_cambio", []), "#EAF2F8", "#14506B", "#14506B",
        )
    with d2:
        _caja_gobernanza(
            "Bandera, sin cambiar el valor",
            "Se marca el caso para revisión manual, pero el dato original queda intacto.",
            decisiones.get("ejecutadas_como_bandera", []), "#FFF8EC", "#C98A1B", "#C98A1B",
        )
    with d3:
        _caja_gobernanza(
            "Mantener sin tratamiento",
            "Decisión consciente de no tocar el dato -- no hay evidencia de que sea un error.",
            decisiones.get("mantener_sin_tratamiento", []), "#F7F8FA", "#999999", "#555555",
        )

    st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
    st.markdown("##### Prioridad de tratamiento")
    st.caption("Distinta de la decisión de arriba -- mide urgencia, no relevancia narrativa.")
    prioridad = calidad.get("prioridad_gobernanza", {})
    conteo = prioridad.get("conteo", {})
    por_id = prioridad.get("por_id", {})

    def _stat_prioridad(etiqueta, valor, color, codigos):
        st.markdown(
            f"""
            <div style="text-align:center; padding-bottom:1rem;">
            <span style="font-size:2.2rem; font-weight:800; color:{color};">{valor}</span><br>
            <span style="font-size:0.85rem; color:#555;">{etiqueta}</span><br>
            <span style="font-family:monospace; font-size:0.75rem; color:{color};">{", ".join(codigos)}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    cod_alta = [k for k, v in por_id.items() if v == "Alta"]
    cod_media = [k for k, v in por_id.items() if v == "Media"]
    cod_baja = [k for k, v in por_id.items() if v == "Baja"]

    p1, p2, p3 = st.columns(3)
    with p1:
        _stat_prioridad("Alta", conteo.get("Alta", 0), ROJO_ALERTA, cod_alta)
    with p2:
        _stat_prioridad("Media", conteo.get("Media", 0), AMBAR_PENDIENTE, cod_media)
    with p3:
        _stat_prioridad("Baja", conteo.get("Baja", 0), GRIS_TEXTO, cod_baja)
    st.markdown("<div style='margin-top:0.3rem;'></div>", unsafe_allow_html=True)
    st.markdown(prioridad.get("patron", ""))

    st.markdown("---")
    st.markdown("#### Tratamiento: la ejecución")
    st.caption(
        "La gobernanza decide, el tratamiento ejecuta — esto es lo que pasó de verdad con los datos "
        "clasificados como 'cambio de datos'."
    )

    # --- Ejemplo 1 en Desplegable ---
    ej1 = contexto.get("ejemplo_valores_ausentes", {})
    if ej1:
        titulo_ej1 = ej1.get("titulo", "Tratamiento de valores ausentes (L2)")
        with st.expander(titulo_ej1, expanded=False):
            st.caption(ej1.get("intro", ""))

            def _regla_corta(fila):
                if fila["campo"] == "price":
                    if fila["original"] == "Nulo":
                        return "Mediana del grupo (barrio, tipo de habitación); si falta dato, mediana global."
                    return "No aplica -- el dato original ya estaba completo."
                return "Mediana por capacidad (`accommodates`), con mediana global de respaldo."

            filas_ej1 = ej1.get("filas", [])
            for fila in filas_ej1:
                fila["Regla aplicada"] = _regla_corta(fila)
            df_ej1 = pd.DataFrame(filas_ej1)
            df_ej1 = df_ej1.rename(columns={
                "id": "id", "campo": "Campo", "original": "Original",
                "curado": "Curado", "interpretacion": "Interpretación",
            })
            df_ej1 = df_ej1[["id", "Campo", "Original", "Curado", "Regla aplicada", "Interpretación"]]
            st.dataframe(df_ej1, width="stretch", hide_index=True)
            st.info(ej1.get("nota_imputacion", ""))
            
            with st.expander("Ver criterio completo de imputación y limitaciones metodológicas"):
                st.markdown(f"**`price`**: {ej1.get('regla_price', '')}")
                st.markdown(f"**`bedrooms`/`bathrooms`/`beds`**: {ej1.get('regla_bedrooms', '')}")
                st.markdown("---")
                st.caption(ej1.get("justificacion", ""))
                st.caption(ej1.get("limitacion_room_type", ""))
    # --- Ejemplo 2 en Desplegable (Sin estrellitas, con diseño limpio) ---
    ej2 = contexto.get("ejemplo_licencia", {})
    if ej2:
        with st.expander(ej2.get("titulo", "Ejemplo 2"), expanded=False):
            st.caption(ej2.get("intro", ""))
            col_x, col_y = st.columns(2)
            
            caja_antes = (
                "<div style='background-color:#FDF8F2; border:1px solid #E6D5C3; border-left:5px solid #D9822B; border-radius:6px; "
                "padding:0.9rem 1rem; font-family:monospace; font-size:0.82rem; height:100%; color:#333;'>{valor}</div>"
            )
            caja_despues = (
                "<div style='background-color:#F0F7F4; border:1px solid #C2E0D1; border-left:5px solid #2ECC71; border-radius:6px; "
                "padding:0.9rem 1rem; font-family:monospace; font-size:0.82rem; height:100%; color:#333;'>{valor}</div>"
            )

            with col_x:
                st.markdown(f"**Antes** — `license` cruda (id {ej2.get('id', '')}):")
                st.markdown(
                    caja_antes.format(valor=html.escape(ej2.get("license_crudo", ""))),
                    unsafe_allow_html=True,
                )
            with col_y:
                st.markdown("**Después** — texto limpio (`license_limpio`):")
                st.markdown(
                    caja_despues.format(valor=ej2.get("license_limpio", "")),
                    unsafe_allow_html=True,
                )
            
            st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
            st.markdown("De ese texto limpio se extraen dos campos nuevos (`L4`):")
            col_a, col_b = st.columns(2)
            campo_extraido = (
                "<div style='background-color:white; border:1px solid #E0E0E0; border-top:4px solid {color}; border-radius:8px; "
                "padding:0.8rem 1rem; height:100%;'>"
                "<span style='font-size:0.78rem; color:#555; text-transform:uppercase; font-weight:600;'>{etiqueta}</span><br>"
                "<span style='font-family:monospace; font-size:0.88rem; color:{gris};'>{valor}</span>"
                "</div>"
            )
            with col_a:
                st.markdown(
                    campo_extraido.format(
                        color=AZUL_PETROLEO, gris=GRIS_TEXTO, etiqueta="license_hutb_codigos",
                        valor=ej2.get("license_hutb_codigos", ""),
                    ),
                    unsafe_allow_html=True,
                )
            with col_b:
                st.markdown(
                    campo_extraido.format(
                        color=AZUL_PETROLEO, gris=GRIS_TEXTO, etiqueta="license_categoria",
                        valor=ej2.get("license_categoria", ""),
                    ),
                    unsafe_allow_html=True,
                )
            
            st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
            st.markdown("**Regla** (aplicada a los 15.293 anuncios):")
            st.markdown(ej2.get("regla", ""))
            
            st.markdown("**Nota sobre los códigos HUTB detectados:**")
            st.caption(
                "`license_hutb_codigos` lista los códigos HUTB detectados en el texto original -- no implica "
                "que ambos sean licencias vigentes o válidas, solo que el campo `license` contenía dos códigos "
                "distintos. Confirmar la validez de cada código exigiría consultar el registro oficial, fuera "
                "del alcance de este dataset."
            )
            st.caption(ej2.get("justificacion", ""))

# ---------- 5. Conclusion y transicion ----------
with tab5:
    st.markdown("#### Conclusión")
    st.success(
        "- **14 hallazgos** documentados en las 3 tablas, cada uno con una decisión de gobernanza justificada.\n"
        "- **Verificaciones limpias**: completitud 100% en `reviews` y `calendar`, unicidad de `id` en "
        "`listings` -- no todo resultó ser un problema.\n"
        "- **El hallazgo de mayor impacto no está aquí**: surge de investigar los ceros en "
        "`estimated_revenue_l365d`, en la página 'El hallazgo crítico' (siguiente en el menú)."
    )
