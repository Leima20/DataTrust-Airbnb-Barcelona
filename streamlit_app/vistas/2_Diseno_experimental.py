import streamlit as st

from src.styles import (
    kicker, AZUL_PETROLEO, OCRE_DORADO_TEXTO, AZUL_OSCURO, COLOR_CRUDO, COLOR_D, COLOR_TRATADO,
    COLOR_SENSIBILIDAD, AMBAR_PENDIENTE, TURQUESA_TEXTO, COLOR_SENSIBILIDAD_TEXTO,
)

kicker("Página 5 de 9")
st.title("Diseño experimental")

st.markdown(
    "Para comprobar si las decisiones de curación alteran el rendimiento predictivo, "
    "entrenamos el **mismo algoritmo** bajo distintas versiones de los datos, "
    "separando el efecto de la **población** y el de la **calidad de las variables**."
)

st.markdown("---")

st.markdown("### ¿Qué variables entran en los modelos?")

def _etiqueta(nombre, color):
    return (
        f'<span style="display:inline-block; background-color:{color}1A; color:{color}; '
        f'border:1px solid {color}55; border-radius:12px; padding:0.15rem 0.5rem; '
        f'font-size:0.72rem; font-family:monospace; margin:0.12rem;">{nombre}</span>'
    )


def _bloque_etiquetas(nombres, color):
    return (
        '<div style="display:flex; flex-wrap:wrap; gap:0.05rem;">'
        + "".join(_etiqueta(n, color) for n in nombres)
        + "</div>"
    )


predictoras_num = ["accommodates", "bedrooms", "bathrooms", "beds", "host_listings_count",
                   "calculated_host_listings_count", "amenities_count"]
predictoras_cat = ["room_type", "property_type", "neighbourhood_cleansed", "host_is_superhost"]
excluidas = ["price", "estimated_occupancy_l365d", "number_of_reviews (y variantes)", "minimum_nights"]

def _tarjeta_variables(titulo, subtitulo, color, contenido_html):
    st.markdown(
        f"""
        <div style="background-color:white; border-top:4px solid {color}; border-radius:10px;
                    padding:1rem 1.1rem; height:100%;">
            <div style="color:{color}; font-weight:700; font-size:0.95rem;">{titulo}</div>
            <div style="font-size:0.78rem; color:#888; text-transform:uppercase; margin-bottom:0.6rem;">
            {subtitulo}</div>
            {contenido_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


col_obj, col_pred, col_exc = st.columns([1, 1.6, 1.3])
with col_obj:
    _tarjeta_variables(
        "Variable objetivo", "A predecir", AZUL_OSCURO,
        '<code style="font-size:0.78rem;">estimated_revenue_l365d</code>',
    )
with col_pred:
    _tarjeta_variables(
        "Predictoras", "11 variables", AZUL_PETROLEO,
        _bloque_etiquetas(predictoras_num + predictoras_cat, AZUL_PETROLEO),
    )
with col_exc:
    _tarjeta_variables(
        "Excluidas", "4 variables, causan fuga", OCRE_DORADO_TEXTO,
        _bloque_etiquetas(excluidas, OCRE_DORADO_TEXTO),
    )
st.caption(
    "De las 11 predictoras, solo **bedrooms/bathrooms/beds** (nulos a rellenar) y **amenities_count** "
    "(proxy vs. cálculo real) cambian de tratamiento entre las 4 versiones."
)

st.markdown("---")

st.markdown("### Las cuatro versiones de los modelos")

st.markdown(
    f"""
    <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem 1.1rem;">
      <svg width="100%" height="350" viewBox="0 0 900 350" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="flecha_v" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" fill="#aaa" />
          </marker>
        </defs>
        <rect x="20" y="20" width="415" height="68" rx="10" fill="#f4f4f4" stroke="{COLOR_CRUDO}" stroke-width="1.5" />
        <text x="227" y="42" text-anchor="middle" fill="#444" font-size="13" font-weight="700" font-family="Helvetica">listings_raw</text>
        <text x="227" y="59" text-anchor="middle" fill="#777" font-size="10" font-family="Helvetica">sin tratamiento</text>
        <text x="227" y="74" text-anchor="middle" fill="#999" font-size="9" font-family="Helvetica">15.293 filas, 90 cols</text>
        <rect x="470" y="20" width="415" height="68" rx="10" fill="#f4f4f4" stroke="{COLOR_TRATADO}" stroke-width="1.5" />
        <text x="677" y="42" text-anchor="middle" fill="#444" font-size="13" font-weight="700" font-family="Helvetica">listings_curado</text>
        <text x="677" y="59" text-anchor="middle" fill="#777" font-size="10" font-family="Helvetica">tratado: L1, L2, L4, target</text>
        <text x="677" y="74" text-anchor="middle" fill="#999" font-size="9" font-family="Helvetica">15.293 filas, 91 cols</text>
        <line x1="115" y1="88" x2="115" y2="158" stroke="#aaa" stroke-width="2" marker-end="url(#flecha_v)" />
        <line x1="340" y1="88" x2="340" y2="158" stroke="#aaa" stroke-width="2" marker-end="url(#flecha_v)" />
        <line x1="565" y1="88" x2="565" y2="158" stroke="#aaa" stroke-width="2" marker-end="url(#flecha_v)" />
        <line x1="790" y1="88" x2="790" y2="158" stroke="#aaa" stroke-width="2" marker-end="url(#flecha_v)" />
        <rect x="20" y="165" width="190" height="170" rx="10" fill="{COLOR_CRUDO}" />
        <text x="115" y="190" text-anchor="middle" fill="white" font-size="12" font-weight="700" font-family="Helvetica">Modelo A -- CRUDO</text>
        <text x="115" y="210" text-anchor="middle" fill="white" font-size="11" font-family="Helvetica">n = 13.355</text>
        <text x="115" y="228" text-anchor="middle" fill="white" font-size="9" font-family="Helvetica" opacity="0.85">variables sin tratar</text>
        <text x="115" y="246" text-anchor="middle" fill="white" font-size="8.5" font-family="Helvetica" opacity="0.85">bedrooms/bathrooms/beds: -1</text>
        <text x="115" y="262" text-anchor="middle" fill="white" font-size="8.5" font-family="Helvetica" opacity="0.85">amenities_count: proxy (texto)</text>
        <rect x="245" y="165" width="190" height="170" rx="10" fill="{COLOR_D}" />
        <text x="340" y="190" text-anchor="middle" fill="white" font-size="12" font-weight="700" font-family="Helvetica">Modelo D</text>
        <text x="340" y="210" text-anchor="middle" fill="white" font-size="11" font-family="Helvetica">n = 13.355</text>
        <text x="340" y="228" text-anchor="middle" fill="white" font-size="9" font-family="Helvetica" opacity="0.85">variables tratadas</text>
        <text x="340" y="246" text-anchor="middle" fill="white" font-size="8.5" font-family="Helvetica" opacity="0.85">bedrooms/bathrooms/beds:</text>
        <text x="340" y="261" text-anchor="middle" fill="white" font-size="8.5" font-family="Helvetica" opacity="0.85">mediana agrupada</text>
        <text x="340" y="276" text-anchor="middle" fill="white" font-size="8.5" font-family="Helvetica" opacity="0.85">por accommodates</text>
        <text x="340" y="294" text-anchor="middle" fill="white" font-size="8.5" font-family="Helvetica" opacity="0.85">amenities_count: extracción real</text>
        <rect x="470" y="165" width="190" height="170" rx="10" fill="{COLOR_TRATADO}" />
        <text x="565" y="190" text-anchor="middle" fill="white" font-size="12" font-weight="700" font-family="Helvetica">Modelo B -- TRATADO-A</text>
        <text x="565" y="210" text-anchor="middle" fill="white" font-size="11" font-family="Helvetica">n = 10.669</text>
        <text x="565" y="228" text-anchor="middle" fill="white" font-size="8.5" font-family="Helvetica" opacity="0.85">población y variables tratadas</text>
        <text x="565" y="246" text-anchor="middle" fill="white" font-size="8.5" font-family="Helvetica" opacity="0.85">bedrooms/bathrooms/beds:</text>
        <text x="565" y="261" text-anchor="middle" fill="white" font-size="8.5" font-family="Helvetica" opacity="0.85">mediana agrupada</text>
        <text x="565" y="276" text-anchor="middle" fill="white" font-size="8.5" font-family="Helvetica" opacity="0.85">por accommodates</text>
        <text x="565" y="294" text-anchor="middle" fill="white" font-size="8.5" font-family="Helvetica" opacity="0.85">amenities_count: extracción real</text>
        <rect x="695" y="165" width="190" height="170" rx="10" fill="{COLOR_SENSIBILIDAD}" />
        <text x="790" y="190" text-anchor="middle" fill="white" font-size="12" font-weight="700" font-family="Helvetica">Chequeo de sensibilidad</text>
        <text x="790" y="210" text-anchor="middle" fill="white" font-size="11" font-family="Helvetica">n = 10.669</text>
        <text x="790" y="228" text-anchor="middle" fill="white" font-size="8.5" font-family="Helvetica" opacity="0.85">otro criterio de imputación</text>
        <text x="790" y="246" text-anchor="middle" fill="white" font-size="8.5" font-family="Helvetica" opacity="0.85">bedrooms/bathrooms/beds:</text>
        <text x="790" y="261" text-anchor="middle" fill="white" font-size="8.5" font-family="Helvetica" opacity="0.85">mediana agrupada</text>
        <text x="790" y="276" text-anchor="middle" fill="white" font-size="8.5" font-family="Helvetica" opacity="0.85">por barrio</text>
        <text x="790" y="294" text-anchor="middle" fill="white" font-size="8.5" font-family="Helvetica" opacity="0.85">amenities_count: extracción real</text>
      </svg>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("📋 Ficha técnica: variables e imputación por modelo"):
    st.markdown(
        f"""
        <div style="color: {COLOR_CRUDO}; font-weight: 700; font-size: 0.9rem; margin-bottom: 0.2rem;">Modelo A — CRUDO</div>
        <ul style="font-size: 0.85rem; color: #444; line-height: 1.6; margin: 0 0 0.8rem 1.1rem; padding: 0;">
            <li><code>bedrooms</code>/<code>bathrooms</code>/<code>beds</code>: centinela <code>-1</code> (valor imposible, no una estimación real)</li>
            <li><code>host_listings_count</code>: relleno técnico = <code>1</code></li>
            <li><code>host_is_superhost</code>: relleno técnico = <code>f</code></li>
            <li><code>amenities_count</code>: proxy — longitud de texto</li>
            <li>2.686 casos 'no estimable' contabilizados como ceros reales</li>
        </ul>

        <div style="color: {COLOR_D}; font-weight: 700; font-size: 0.9rem; margin-bottom: 0.2rem;">Modelo D</div>
        <ul style="font-size: 0.85rem; color: #444; line-height: 1.6; margin: 0 0 0.8rem 1.1rem; padding: 0;">
            <li><code>bedrooms</code>/<code>bathrooms</code>/<code>beds</code>: mediana por <code>accommodates</code></li>
            <li><code>host_listings_count</code>: relleno técnico = <code>1</code></li>
            <li><code>host_is_superhost</code>: relleno técnico = <code>f</code></li>
            <li><code>amenities_count</code>: extracción real (lista JSON), igual que en el Modelo B</li>
        </ul>

        <div style="color: {TURQUESA_TEXTO}; font-weight: 700; font-size: 0.9rem; margin-bottom: 0.2rem;">Modelo B — TRATADO-A</div>
        <ul style="font-size: 0.85rem; color: #444; line-height: 1.6; margin: 0 0 0.8rem 1.1rem; padding: 0;">
            <li>Excluye los 2.686 casos <code>revenue_no_estimable</code></li>
            <li><code>bedrooms</code>/<code>bathrooms</code>/<code>beds</code>: mediana por <code>accommodates</code></li>
            <li><code>host_listings_count</code>: relleno técnico = <code>1</code></li>
            <li><code>host_is_superhost</code>: relleno técnico = <code>f</code></li>
            <li><code>amenities_count</code>: extracción real (lista JSON)</li>
        </ul>

        <div style="color: {COLOR_SENSIBILIDAD_TEXTO}; font-weight: 700; font-size: 0.9rem; margin-bottom: 0.2rem;">Chequeo de sensibilidad</div>
        <ul style="font-size: 0.85rem; color: #444; line-height: 1.6; margin: 0 0 0 1.1rem; padding: 0;">
            <li><code>bedrooms</code>/<code>bathrooms</code>/<code>beds</code>: mediana por barrio (<code>neighbourhood_cleansed</code>), en vez de por capacidad</li>
            <li><code>host_listings_count</code> / <code>host_is_superhost</code> / <code>amenities_count</code>: igual que el Modelo B</li>
        </ul>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

st.markdown("### Cómo se entrena y evalúa cada versión")

st.markdown(
    f"""
    <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem 1.1rem;">
      <svg width="100%" height="460" viewBox="0 0 1500 380" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="flecha_ev" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" fill="#aaa" />
          </marker>
        </defs>
        <text x="100" y="20" text-anchor="middle" fill="#888" font-size="11" font-weight="600" letter-spacing="0.5" font-family="Helvetica">1. DIVISIÓN</text>
        <rect x="10" y="150" width="180" height="80" rx="10" fill="#f4f4f4" stroke="#ccc" stroke-width="1.5" />
        <text x="100" y="185" text-anchor="middle" fill="#444" font-size="13" font-weight="700" font-family="Helvetica">Todos los datos</text>
        <text x="100" y="205" text-anchor="middle" fill="#888" font-size="11" font-family="Helvetica">por versión</text>
        <line x1="190" y1="190" x2="255" y2="65" stroke="#aaa" stroke-width="2" marker-end="url(#flecha_ev)" />
        <line x1="190" y1="190" x2="255" y2="305" stroke="#aaa" stroke-width="2" marker-end="url(#flecha_ev)" />
        <rect x="260" y="30" width="230" height="70" rx="10" fill="{AZUL_PETROLEO}" />
        <text x="375" y="60" text-anchor="middle" fill="white" font-size="15" font-weight="700" font-family="Helvetica">Entrenamiento</text>
        <text x="375" y="82" text-anchor="middle" fill="white" font-size="13" font-family="Helvetica">80% de las filas</text>
        <rect x="260" y="270" width="230" height="70" rx="10" fill="{OCRE_DORADO_TEXTO}" />
        <text x="375" y="300" text-anchor="middle" fill="white" font-size="15" font-weight="700" font-family="Helvetica">Prueba</text>
        <text x="375" y="322" text-anchor="middle" fill="white" font-size="13" font-family="Helvetica">20% de las filas</text>
        <text x="100" y="250" text-anchor="middle" fill="#999" font-size="10" font-family="Helvetica">(misma semilla en las 4 versiones)</text>
        <rect x="35" y="258" width="130" height="22" rx="11" fill="#eee" />
        <text x="100" y="273" text-anchor="middle" fill="#666" font-size="10" font-family="monospace">random_state=42</text>
        <text x="730" y="20" text-anchor="middle" fill="#888" font-size="11" font-weight="600" letter-spacing="0.5" font-family="Helvetica">2. PREPARACIÓN Y ENTRENAMIENTO</text>
        <line x1="490" y1="65" x2="555" y2="80" stroke="#aaa" stroke-width="2" marker-end="url(#flecha_ev)" />
        <rect x="560" y="30" width="340" height="125" rx="10" fill="white" stroke="{AZUL_PETROLEO}" stroke-width="2" />
        <text x="730" y="55" text-anchor="middle" fill="{AZUL_PETROLEO}" font-size="13" font-weight="700" font-family="Helvetica">Pipeline (ajustado solo con el 80%)</text>
        <text x="730" y="75" text-anchor="middle" fill="#444" font-size="12" font-family="Helvetica">StandardScaler + OneHotEncoder</text>
        <text x="730" y="88" text-anchor="middle" fill="#999" font-size="9" font-family="Helvetica">(escalado de números, codificación de categorías)</text>
        <line x1="600" y1="98" x2="860" y2="98" stroke="#eee" stroke-width="1" />
        <text x="730" y="117" text-anchor="middle" fill="#444" font-size="12" font-weight="600" font-family="Helvetica">Random Forest aprende patrones</text>
        <text x="730" y="135" text-anchor="middle" fill="#999" font-size="10" font-family="Helvetica">200 árboles, random_state=42</text>
        <text x="1100" y="115" text-anchor="middle" fill="#888" font-size="11" font-weight="600" letter-spacing="0.5" font-family="Helvetica">3. PREDICCIÓN</text>
        <line x1="900" y1="90" x2="985" y2="175" stroke="#aaa" stroke-width="2" marker-end="url(#flecha_ev)" />
        <line x1="490" y1="305" x2="985" y2="205" stroke="#aaa" stroke-width="2" marker-end="url(#flecha_ev)" />
        <rect x="980" y="150" width="240" height="80" rx="10" fill="white" stroke="{AZUL_OSCURO}" stroke-width="2" />
        <text x="1100" y="180" text-anchor="middle" fill="{AZUL_OSCURO}" font-size="13" font-weight="700" font-family="Helvetica">Transformaciones aprendidas</text>
        <text x="1100" y="200" text-anchor="middle" fill="#444" font-size="12" font-family="Helvetica">aplicadas al 20% de prueba</text>
        <text x="1385" y="115" text-anchor="middle" fill="#888" font-size="11" font-weight="600" letter-spacing="0.5" font-family="Helvetica">4. EVALUACIÓN</text>
        <line x1="1220" y1="190" x2="1285" y2="190" stroke="#aaa" stroke-width="2" marker-end="url(#flecha_ev)" />
        <rect x="1290" y="150" width="200" height="80" rx="10" fill="{OCRE_DORADO_TEXTO}" />
        <text x="1390" y="178" text-anchor="middle" fill="white" font-size="13" font-weight="700" font-family="Helvetica">MAE · R²</text>
        <text x="1390" y="198" text-anchor="middle" fill="white" font-size="11" font-family="Helvetica">sobre el 20% de prueba</text>
        <text x="1390" y="216" text-anchor="middle" fill="white" font-size="10" font-family="Helvetica" opacity="0.85">mismo criterio en las 4 versiones</text>
      </svg>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

st.markdown(
    "<div style='text-align:center; color:#666; font-size:1.15rem; font-style:italic; margin-bottom:0.5rem;'>"
    "¿Cómo consigue el modelo generar esa predicción?</div>",
    unsafe_allow_html=True,
)
st.markdown("### ¿Qué ocurre dentro de Random Forest?")

def _icono_arbol(cx, color):
    return (
        f'<circle cx="{cx}" cy="34" r="14" fill="{color}" />'
        f'<line x1="{cx}" y1="34" x2="{cx-34}" y2="78" stroke="{color}" stroke-width="4" />'
        f'<line x1="{cx}" y1="34" x2="{cx+34}" y2="78" stroke="{color}" stroke-width="4" />'
        f'<circle cx="{cx-34}" cy="78" r="10" fill="{color}" />'
        f'<circle cx="{cx+34}" cy="78" r="10" fill="{color}" />'
    )

arboles_x = [430, 590, 750, 910, 1070]
arboles_label = ["Árbol 1", "Árbol 2", "Árbol 3", "...", "Árbol 200"]
iconos = "".join(_icono_arbol(cx, AZUL_PETROLEO) for cx in arboles_x)
etiquetas = "".join(
    f'<text x="{cx}" y="108" text-anchor="middle" fill="#444" font-size="15" font-weight="600" font-family="Helvetica">{lbl}</text>'
    for cx, lbl in zip(arboles_x, arboles_label)
)
flechas = "".join(
    f'<line x1="{cx}" y1="118" x2="750" y2="128" stroke="#aaa" stroke-width="2" marker-end="url(#flecha_rf)" />'
    for cx in arboles_x
)

st.markdown(
    f"""
    <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem 1.1rem; margin-top: 0.8rem;">
      <svg width="100%" height="390" viewBox="0 0 1250 340" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <marker id="flecha_rf" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" fill="#aaa" />
          </marker>
        </defs>
        <text x="130" y="20" text-anchor="middle" fill="#888" font-size="12" font-weight="600" letter-spacing="0.5" font-family="Helvetica">¿POR QUÉ RANDOM FOREST?</text>
        <rect x="10" y="32" width="240" height="80" rx="8" fill="white" stroke="{AZUL_PETROLEO}" stroke-width="1.5" />
        <text x="130" y="66" text-anchor="middle" fill="#444" font-size="13" font-weight="600" font-family="Helvetica">Maneja bien variables</text>
        <text x="130" y="86" text-anchor="middle" fill="#444" font-size="13" font-weight="600" font-family="Helvetica">categóricas codificadas</text>
        <rect x="10" y="122" width="240" height="80" rx="8" fill="white" stroke="{AZUL_PETROLEO}" stroke-width="1.5" />
        <text x="130" y="156" text-anchor="middle" fill="#444" font-size="13" font-weight="600" font-family="Helvetica">Relaciones</text>
        <text x="130" y="176" text-anchor="middle" fill="#444" font-size="13" font-weight="600" font-family="Helvetica">no lineales</text>
        <rect x="10" y="212" width="240" height="80" rx="8" fill="white" stroke="{AZUL_PETROLEO}" stroke-width="1.5" />
        <text x="130" y="246" text-anchor="middle" fill="#444" font-size="13" font-weight="600" font-family="Helvetica">Calcula de forma directa</text>
        <text x="130" y="266" text-anchor="middle" fill="#444" font-size="13" font-weight="600" font-family="Helvetica">la importancia de variables</text>
        <text x="130" y="306" text-anchor="middle" fill="#999" font-size="10" font-family="Helvetica">sin exigir variables escaladas</text>
        <text x="130" y="320" text-anchor="middle" fill="#999" font-size="10" font-family="Helvetica">(se aplica igual, por criterio uniforme)</text>
        <line x1="255" y1="150" x2="405" y2="60" stroke="#ccc" stroke-width="1.5" stroke-dasharray="3,3" marker-end="url(#flecha_rf)" />
        <text x="340" y="20" text-anchor="middle" fill="#888" font-size="11" font-weight="600" letter-spacing="0.5" font-family="Helvetica">1. LA DIVERSIDAD</text>
        {iconos}
        {etiquetas}
        {flechas}
        <text x="750" y="152" text-anchor="middle" fill="#888" font-size="11" font-weight="600" letter-spacing="0.5" font-family="Helvetica">2. LA AGREGACIÓN</text>
        <rect x="450" y="160" width="600" height="60" rx="10" fill="{AZUL_PETROLEO}" />
        <text x="750" y="196" text-anchor="middle" fill="white" font-size="17" font-weight="700" font-family="Helvetica">Promedio de las 200 predicciones</text>
        <line x1="750" y1="220" x2="750" y2="246" stroke="#aaa" stroke-width="2.5" marker-end="url(#flecha_rf)" />
        <text x="750" y="260" text-anchor="middle" fill="#888" font-size="11" font-weight="600" letter-spacing="0.5" font-family="Helvetica">3. LA PREDICCIÓN</text>
        <rect x="550" y="268" width="400" height="46" rx="10" fill="{OCRE_DORADO_TEXTO}" />
        <text x="750" y="296" text-anchor="middle" fill="white" font-size="16" font-weight="700" font-family="Helvetica">Predicción final (ingreso estimado)</text>
      </svg>
      <div style="font-size: 0.85rem; color: #666; text-align: center; margin-top: 0.3rem;">
      200 árboles independientes predicen cada uno su propio número, y se promedian para llegar a un
      resultado más robusto que un único árbol: cada uno se entrena con una muestra aleatoria distinta
      de filas y variables. <code>RandomForestRegressor</code> -- 200 árboles, <code>random_state=42</code>.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
