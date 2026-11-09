"""DataTrust -- página de Inicio."""
import streamlit as st

from src.data_loader import cargar_contexto
from src.styles import fmt_num, AZUL_OSCURO, TURQUESA, TURQUESA_CLARO, OCRE_DORADO, OCRE_DORADO_TEXTO

contexto = cargar_contexto()

autoria = contexto.get("autoria", {})
partes_autoria = " · ".join(
    p for p in [autoria.get("nombre", ""), autoria.get("programa", ""), autoria.get("institucion", "")] if p
)

st.markdown(
    f"""
    <div style="background-color:{AZUL_OSCURO}; margin:-3.5rem -5rem 2rem -5rem;
                padding:3.5rem 5rem 2.8rem 5rem; position:relative; overflow:hidden;">
    <svg width="460" height="345" viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg"
         style="position:absolute; right:-10px; top:50%; transform:translateY(-50%); opacity:0.5; z-index:0;">
      <rect x="20" y="220" width="40" height="60" rx="3" fill="{TURQUESA_CLARO}" opacity="0.55"/>
      <rect x="75" y="140" width="40" height="140" rx="3" fill="{TURQUESA_CLARO}" opacity="0.55"/>
      <rect x="130" y="180" width="40" height="100" rx="3" fill="{TURQUESA_CLARO}" opacity="0.55"/>
      <rect x="185" y="110" width="40" height="170" rx="3" fill="{TURQUESA_CLARO}" opacity="0.55"/>
      <rect x="240" y="200" width="40" height="80" rx="3" fill="{TURQUESA_CLARO}" opacity="0.55"/>
      <rect x="295" y="130" width="40" height="150" rx="3" fill="{TURQUESA_CLARO}" opacity="0.55"/>
      <polyline points="40,190 95,110 150,150 205,70 260,160 315,90" fill="none"
                stroke="{OCRE_DORADO}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>
      <circle cx="40" cy="190" r="9" fill="{OCRE_DORADO}"/>
      <circle cx="95" cy="110" r="9" fill="{OCRE_DORADO}"/>
      <circle cx="150" cy="150" r="9" fill="{OCRE_DORADO}"/>
      <circle cx="205" cy="70" r="9" fill="{OCRE_DORADO}"/>
      <circle cx="260" cy="160" r="9" fill="{OCRE_DORADO}"/>
      <circle cx="315" cy="90" r="9" fill="{OCRE_DORADO}"/>
    </svg>
    <div style="position:relative; z-index:1;">
    <span style="color:{TURQUESA_CLARO}; font-weight:700; letter-spacing:0.08em; text-transform:uppercase;
                 font-size:0.85rem;">DataTrust · Auditoría de calidad de datos</span>
    <h1 style="color:white; font-size:2.7rem; font-weight:800; margin:0.7rem 0 1.1rem 0; line-height:1.18;">
    ¿Podemos confiar en los datos para tomar decisiones?</h1>
    <p style="color:#C7CDD3; font-size:1.15rem; max-width:760px; margin:0 0 1rem 0;">
    Un estudio sobre cómo la calidad y gobernanza de los datos afecta las conclusiones de negocio y
    el rendimiento de un modelo predictivo, usando Inside Airbnb Barcelona como caso de estudio.</p>
    <span style="color:#8B99A8; font-size:0.9rem;">{partes_autoria}</span>
    </div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab_zillow, tab_pregunta = st.tabs(["El caso Zillow", "La pregunta de investigación"])

with tab_zillow:
    zillow = contexto.get("caso_zillow", {})
    if zillow:
        st.markdown(
            f'## El colapso de <span style="color:{OCRE_DORADO_TEXTO};">Zillow</span> Offers',
            unsafe_allow_html=True,
        )
        col_cifra, col_texto = st.columns([1, 1.3], gap="large")
        with col_cifra:
            perdida_fmt = fmt_num(zillow.get('perdida_anual_usd', 0) / 1_000_000)

            # Accion ZG (Zillow Class A), cierre mensual 2021 -- fuente: Digrin.com (digrin.com/stocks/detail/ZG/price)
            precios_zg_2021 = [138.72, 169.82, 131.38, 133.35, 118.29, 122.53, 107.13, 95.60, 88.58, 105.72, 54.11, 62.22]
            _vmin, _vmax = min(precios_zg_2021), max(precios_zg_2021)
            _W, _H, _pad_top, _pad_bottom = 300, 84, 6, 14

            def _xy(i, v):
                x = round(i * (_W / (len(precios_zg_2021) - 1)), 1)
                frac = (v - _vmin) / (_vmax - _vmin)
                y = round(_pad_top + (1 - frac) * (_H - _pad_top - _pad_bottom), 1)
                return x, y

            _puntos = [_xy(i, v) for i, v in enumerate(precios_zg_2021)]
            _polyline_pts = " ".join(f"{x},{y}" for x, y in _puntos)
            _oct_x, _oct_y = _puntos[9]
            _nov_x, _nov_y = _puntos[10]
            _oct_frac = _oct_x / _W * 100
            _nov_frac = _nov_x / _W * 100
            _mid_frac = (_oct_x + _nov_x) / 2 / _W * 100
            _caida_pct = (precios_zg_2021[10] - precios_zg_2021[9]) / precios_zg_2021[9] * 100
            _precio_oct = fmt_num(precios_zg_2021[9], 2)
            _precio_nov = fmt_num(precios_zg_2021[10], 2)

            st.markdown(
                f"""
                <div style="background-color:#1A2733; border-radius:14px; box-shadow:0 8px 20px rgba(11,57,84,0.25);
                            padding:2rem 1.4rem; text-align:center;">
                <span style="font-size:0.85rem; color:{OCRE_DORADO}; font-weight:700; text-transform:uppercase;
                             letter-spacing:0.08em;">Pérdida en 2021</span><br>
                <span style="font-size:3.5rem; color:#FFFFFF; font-weight:800; white-space:nowrap;">${perdida_fmt}M</span><br>
                <span style="font-size:0.85rem; color:#C7CDD3;">Zillow Offers, división cerrada</span>
                <div style="margin-top:1.4rem; border-top:1px solid #2C3A47; padding-top:0.7rem;">
                <span style="font-size:0.72rem; color:#8A95A1; font-weight:700; text-transform:uppercase;
                             letter-spacing:0.06em;">Cotización de la acción (Zillow Group, cierre mensual)</span>
                </div>
                <div style="margin-top:0.6rem; position:relative;">
                <span style="position:absolute; left:{_mid_frac:.1f}%; top:{_oct_y - 28:.0f}px; transform:translateX(-50%);
                             font-size:1.15rem; font-weight:800; color:{OCRE_DORADO}; white-space:nowrap;">{_caida_pct:.0f}%</span>
                <svg viewBox="0 0 {_W} {_H}" width="100%" height="84" preserveAspectRatio="none">
                    <polyline points="{_polyline_pts}" fill="none" stroke="#C7CDD3" stroke-width="2"
                              stroke-linejoin="round" stroke-linecap="round" opacity="0.55"/>
                    <polyline points="{_oct_x},{_oct_y} {_nov_x},{_nov_y}" fill="none" stroke="{OCRE_DORADO}"
                              stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>
                    <circle cx="{_oct_x}" cy="{_oct_y}" r="3.5" fill="{OCRE_DORADO}"/>
                    <circle cx="{_nov_x}" cy="{_nov_y}" r="3.5" fill="{OCRE_DORADO}"/>
                </svg>
                <div style="position:relative; height:16px; font-size:0.72rem; color:{OCRE_DORADO}; margin-top:0.1rem;">
                <span style="position:absolute; left:{_oct_frac:.1f}%; transform:translateX(-50%); white-space:nowrap;">${_precio_oct}</span>
                <span style="position:absolute; left:{_nov_frac:.1f}%; transform:translateX(-50%); white-space:nowrap;">${_precio_nov}</span>
                </div>
                <div style="position:relative; height:20px; font-size:0.9rem; color:#A9B4BF; margin-top:0.2rem;">
                <span style="position:absolute; left:0;">Ene</span>
                <span style="position:absolute; left:{_mid_frac:.1f}%; transform:translateX(-50%); color:{OCRE_DORADO};
                             font-weight:700; white-space:nowrap;">Oct → Nov: anuncio de cierre</span>
                <span style="position:absolute; right:0;">Dic</span>
                </div>
                </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<div style='margin-top:1.2rem;'></div>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div style="background-color:#EAF2F8; border-left:4px solid #0B3954; border-radius:8px;
                            padding:0.9rem 1.1rem; font-size:0.92rem; color:#333; height:100%;
                            box-sizing:border-box; display:flex; align-items:center;">
                {zillow.get('cita_ceo', '')}
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_texto:
            st.markdown(
                f'### ¿Qué falló en <span style="color:{OCRE_DORADO_TEXTO};">Zillow</span>?'
                f'<div style="width:56px; height:4px; background-color:{OCRE_DORADO}; border-radius:2px; '
                f'margin:0.3rem 0 0.2rem 0;"></div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f"""
                <div style="display:flex; justify-content:center; margin:1rem 0 1.4rem 0;">
                <svg width="100" height="100" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
                  <path d="M15,58 L60,16 L105,58" fill="none" stroke="#0B3954" stroke-width="7"
                        stroke-linecap="round" stroke-linejoin="round"/>
                  <rect x="27" y="56" width="66" height="48" rx="3" fill="white" stroke="#0B3954" stroke-width="6"/>
                  <circle cx="94" cy="88" r="21" fill="{OCRE_DORADO}" stroke="white" stroke-width="3"/>
                  <rect x="91" y="76" width="6" height="16" rx="3" fill="white"/>
                  <circle cx="94" cy="98" r="3.3" fill="white"/>
                </svg>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                <div style="background-color:#EAF2F8; border-left:4px solid #0B3954; border-radius:8px;
                            padding:0.9rem 1.1rem; font-size:0.92rem; color:#333;">
                💡 ¿Puede un modelo con buenas métricas técnicas garantizar buenas decisiones si nadie
                audita los datos y los supuestos que lo alimentan?
                </div>
                """,
                unsafe_allow_html=True,
            )

        fuentes_zillow = zillow.get("fuentes", [])
        enlace = lambda nombre, url: f'<a href="{url}" target="_blank" style="color:#0B3954;">{nombre}</a>'
        fuentes_txt = " · ".join(enlace(f["nombre"], f["url"]) for f in fuentes_zillow) if fuentes_zillow else ""
        fuente_accion = enlace("Digrin — ZG, cierre mensual 2021", "https://www.digrin.com/stocks/detail/ZG/price")
        texto_fuentes = f"Fuentes: {fuentes_txt} · {fuente_accion}" if fuentes_txt else f"Fuentes: {fuente_accion}"
        st.markdown(
            f'<div style="text-align:center; font-size:0.8rem; color:#888; margin:1rem 0 0.3rem 0;">{texto_fuentes}</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div style="background-color:#EAF2F8; border-left:6px solid #0B3954; border-radius:8px;
                        padding:1rem 1.2rem; margin-top:0.5rem; display:flex; align-items:center;
                        gap:1rem;">
            <svg width="46" height="54" viewBox="0 0 120 140" xmlns="http://www.w3.org/2000/svg"
                 style="flex-shrink:0;">
              <path d="M60,8 L108,24 V64 C108,100 84,122 60,132 C36,122 12,100 12,64 V24 Z"
                    fill="white" stroke="#0B3954" stroke-width="5"/>
              <rect x="33" y="60" width="13" height="32" rx="2" fill="{TURQUESA}"/>
              <rect x="53" y="45" width="13" height="47" rx="2" fill="{TURQUESA}"/>
              <rect x="73" y="66" width="13" height="26" rx="2" fill="{TURQUESA}"/>
              <circle cx="90" cy="98" r="17" fill="{AZUL_OSCURO}"/>
              <path d="M82,98 L88,104 L99,91" stroke="white" stroke-width="4" fill="none"
                    stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <div>
            <div style="font-size:0.8rem; font-weight:700; color:#14506B; text-transform:uppercase;
                        letter-spacing:0.04em;">DataTrust nace de la misma pregunta</div>
            <div style="font-size:1.5rem; font-weight:800; color:#0B3954; margin:0.3rem 0; line-height:1.3;">
            "¿Qué pasa cuando se confía en datos o modelos predictivos sin auditar su calidad?"</div>
            <div style="font-size:0.92rem; color:#333;">Para responderlo, analizamos nuestro caso de
            estudio: <b>Inside Airbnb Barcelona</b>.</div>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with tab_pregunta:
    st.markdown(
        """
        <div style="background-color:#EAF2F8; padding:1.3rem 1.5rem; border-radius:10px;
                    border-left:6px solid #0B3954; margin-bottom:1rem;">
        <span style="font-size:0.8rem; color:#14506B; font-weight:600; text-transform:uppercase;
                     letter-spacing:0.05em;">La pregunta de investigación</span>
        <h3 style="margin:0.4rem 0 0 0; color:#0B3954;">¿Puede la <b>calidad de los datos</b> influir en la
        toma de decisiones y en las conclusiones de un análisis, incluso cuando los datos <b>parecen
        suficientemente completos</b> y el <b>modelo predictivo ofrece buenos resultados</b>?</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <h3 style="color:{AZUL_OSCURO}; margin-bottom:0.2rem;">Estructura del análisis</h3>
        <p style="color:#777; font-size:0.9rem; margin-top:0; margin-bottom:1.3rem;">
        Para responder a la pregunta, se plantean 2 hipótesis de trabajo.</p>
        """,
        unsafe_allow_html=True,
    )
    dot_arbol = r"""
    digraph Arbol {
        rankdir=LR;
        bgcolor="transparent";
        size="12,4!";
        ratio=fill;
        node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=18,
              margin=0.22, color="#B7C2CC"];
        edge [color="#B7C2CC", arrowsize=0.9, penwidth=1.6];

        main [label="¿Importa la calidad\nde los datos?", fillcolor="%(azul)s",
              fontcolor=white, fontsize=20];
        negocio [label="Impacto en\nel negocio", fillcolor="%(ocre)s", fontcolor=white];
        modelo [label="Impacto en\nel modelo", fillcolor="%(turquesa)s", fontcolor=white];
        pregunta_negocio [label="¿Cambian las\nconclusiones de negocio?", fillcolor=white, fontcolor="%(azul)s"];
        pregunta_modelo [label="¿Cambia el\nrendimiento del modelo?", fillcolor=white, fontcolor="%(azul)s"];

        main -> negocio;
        main -> modelo;
        negocio -> pregunta_negocio;
        modelo -> pregunta_modelo;
    }
    """ % {"azul": AZUL_OSCURO, "ocre": OCRE_DORADO_TEXTO, "turquesa": TURQUESA}
    st.graphviz_chart(dot_arbol, width="stretch")
