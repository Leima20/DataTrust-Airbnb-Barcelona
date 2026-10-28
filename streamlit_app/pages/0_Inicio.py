"""DataTrust -- pagina de Inicio."""
import streamlit as st

from src.data_loader import cargar_contexto, cargar_impacto_negocio, cargar_modelo
from src.styles import kicker, fmt_num

impacto = cargar_impacto_negocio()
modelo = cargar_modelo()
contexto = cargar_contexto()

kicker("DataTrust · Auditoria de calidad de datos")
st.title("¿Podemos confiar en los datos para tomar decisiones?")
st.markdown(
    "##### Un estudio sobre cómo la calidad y gobernanza de los datos afecta las conclusiones de "
    "negocio y el rendimiento de un modelo predictivo, usando Inside Airbnb Barcelona como caso "
    "de estudio."
)
autoria = contexto.get("autoria", {})
if autoria:
    partes = [p for p in [autoria.get("nombre", ""), autoria.get("programa", ""), autoria.get("institucion", "")] if p]
    st.caption(" · ".join(partes))

st.markdown("---")

tab_zillow, tab_pregunta = st.tabs(["El caso Zillow", "La pregunta de investigación"])

with tab_zillow:
    zillow = contexto.get("caso_zillow", {})
    if zillow:
        st.markdown("## Esto ya le pasó a otros: el colapso de Zillow Offers")
        col_cifra, col_texto = st.columns([1, 1.5], gap="large")
        with col_cifra:
            perdida_fmt = fmt_num(zillow.get('perdida_anual_usd', 0) / 1_000_000)
            st.markdown(
                f"""
                <div style="background-color:#1A2733; border-radius:14px;
                            padding:1.6rem 1.2rem; text-align:center;">
                <span style="font-size:0.85rem; color:#FF8080; font-weight:700; text-transform:uppercase;
                             letter-spacing:0.08em;">Pérdida en 2021</span><br>
                <span style="font-size:3.2rem; color:#FFFFFF; font-weight:800;">${perdida_fmt}M</span><br>
                <span style="font-size:0.85rem; color:#C7CDD3;">Zillow Offers, división cerrada</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(f"> {zillow.get('cita_ceo', '')}")
            fuentes_zillow = zillow.get("fuentes", [])
            if fuentes_zillow:
                enlaces = " · ".join(f"[{f['nombre']}]({f['url']})" for f in fuentes_zillow)
                st.caption(f"Fuentes: {enlaces}")

        with col_texto:
            st.markdown("### ¿Qué falló en Zillow?")
            st.caption(zillow.get("quien_es_zillow", ""))
            writedown_fmt = fmt_num(zillow.get('writedown_usd', 0) / 1_000_000)
            st.error(
                f"**Causa raíz** -- la cadena que llevó al cierre:\n\n"
                f"1. El algoritmo sobreestimó el valor de reventa de las viviendas compradas.\n"
                f"2. Esto forzó un ajuste contable de inventario de **${writedown_fmt}M** en el Q3 2021.\n"
                f"3. La pérdida total atribuida a la división en el año fue de **${perdida_fmt}M** "
                f"-- dos magnitudes distintas, no una pérdida sumada a otra.\n"
                f"4. Zillow cerró Zillow Offers en noviembre de 2021 y recortó cerca del 25% de su plantilla."
            )
            st.info(
                "💡 Un modelo predictivo con buenas métricas técnicas no garantiza buenas decisiones si "
                "no se auditan los límites de los datos que lo alimentan."
            )

        st.markdown(
            """
            <div style="background-color:#EAF2F8; border-left:6px solid #0B3954; border-radius:8px;
                        padding:1rem 1.2rem; margin-top:0.5rem; display:flex; align-items:center;
                        gap:1rem;">
            <svg width="46" height="54" viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg"
                 style="flex-shrink:0;">
              <path d="M60,8 L108,24 V64 C108,100 84,122 60,132 C36,122 12,100 12,64 V24 Z"
                    fill="white" stroke="#0B3954" stroke-width="5"/>
              <rect x="33" y="60" width="13" height="32" rx="2" fill="#1B998B"/>
              <rect x="53" y="45" width="13" height="47" rx="2" fill="#1B998B"/>
              <rect x="73" y="66" width="13" height="26" rx="2" fill="#1B998B"/>
              <circle cx="90" cy="98" r="17" fill="#0CA30C"/>
              <path d="M82,98 L88,104 L99,91" stroke="white" stroke-width="4" fill="none"
                    stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div>
            <div style="font-size:0.8rem; font-weight:700; color:#14506B; text-transform:uppercase;
                        letter-spacing:0.04em;">DataTrust nace de la misma pregunta</div>
            <div style="font-size:1.25rem; font-weight:700; color:#0B3954; margin:0.25rem 0;">
            "¿Qué pasa cuando se confía en datos o modelos predictivos sin auditar su calidad?"</div>
            <div style="font-size:0.92rem; color:#333;">Para responderlo, analizamos nuestro caso de
            estudio: <b>Inside Airbnb Barcelona</b>.</div>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab_pregunta:
    st.caption("El título resume la idea -- esta es la formulación exacta que guía el proyecto:")
    st.markdown(
        """
        <div style="background-color:#EAF2F8; padding:1.3rem 1.5rem; border-radius:10px;
                    border-left:6px solid #0B3954; margin-bottom:1rem;">
        <span style="font-size:0.8rem; color:#14506B; font-weight:600; text-transform:uppercase;
                     letter-spacing:0.05em;">La pregunta de investigación</span>
        <h3 style="margin:0.4rem 0 0 0; color:#0B3954;">¿Puede la calidad de los datos influir en la
        toma de decisiones y en las conclusiones de un análisis, incluso cuando los datos parecen
        suficientemente completos y el modelo predictivo ofrece buenos resultados?</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        "El objetivo de DataTrust no es demostrar de antemano que los datos son malos, ni que Airbnb o "
        "algun anfitrion tomo una decision equivocada -- es **auditar la calidad, investigar un problema "
        "concreto, y evaluar experimentalmente** como las decisiones de preparacion de datos cambian (o "
        "no) los resultados."
    )

    st.markdown("### La evidencia en cifras")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div style="border:1px solid #D7DEE5; border-radius:10px; padding:1rem; height:100%;">
            <span style="font-size:0.78rem; color:#555; text-transform:uppercase; font-weight:600;">
            El dataset crudo</span>
            <h4 style="margin:0.4rem 0; color:#14506B;">Parece listo</h4>
            <span style="font-size:0.85rem; color:#666;">Miles de observaciones, columnas razonables y un
            modelo que se entrena sin errores. ¿Es suficiente para confiar en los resultados?</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        no_est = impacto.get("no_estimable", {})
        if no_est:
            cantidad_fmt = f"{no_est.get('cantidad', 0):,}".replace(",", ".")
            st.markdown(
                f"""
                <div style="background-color:#FDECEC; border:1px solid #F0C9C9; border-radius:10px;
                            padding:1rem; height:100%;">
                <span style="font-size:0.78rem; color:#D03B3B; text-transform:uppercase; font-weight:600;">
                Una señal de alerta</span>
                <h4 style="margin:0.4rem 0; color:#D03B3B;">{cantidad_fmt} anuncios
                ({fmt_num(no_est.get('pct_de_los_que_tienen_dato', 0), 1)}%)</h4>
                <span style="font-size:0.85rem; color:#777;">Presentan ingresos estimados de 0 €. ¿Qué
                significa realmente ese cero, y qué ocurre si lo interpretamos de forma incorrecta?</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
    with col3:
        muestra = modelo.get("muestra_comun_426", {}).get("resultados", {})
        if muestra:
            r2_a = muestra.get("A_crudo", {}).get("r2")
            r2_b = muestra.get("B_tratado_criterio_A", {}).get("r2")
            if r2_a is not None and r2_b is not None:
                st.markdown(
                    f"""
                    <div style="background-color:#E7F6E7; border:1px solid #BEE6BE; border-radius:10px;
                                padding:1rem; height:100%;">
                    <span style="font-size:0.78rem; color:#0CA30C; text-transform:uppercase; font-weight:600;">
                    Una diferencia en el modelo</span>
                    <h4 style="margin:0.4rem 0; color:#0CA30C;">R²: {fmt_num(r2_a, 3)} → {fmt_num(r2_b, 3)}</h4>
                    <span style="font-size:0.85rem; color:#777;">Modelo con datos crudos frente a modelo con
                    datos tratados, evaluados sobre los mismos 426 casos que ninguno usó al entrenar.
                    ¿A qué se debe, y qué podemos concluir?</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown("")
    st.markdown(
        "> *La calidad de los datos no se reduce al porcentaje de valores nulos -- y una diferencia en las "
        "métricas, por sí sola, nunca demuestra un impacto real sin investigar qué la produce.*"
    )
