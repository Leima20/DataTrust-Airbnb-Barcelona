import streamlit as st

from src.styles import kicker, caja_alerta, fmt_num, AMBAR_PENDIENTE, AZUL_PETROLEO, COLOR_CRUDO, COLOR_D, COLOR_TRATADO, COLOR_SENSIBILIDAD, TURQUESA_TEXTO, COLOR_SENSIBILIDAD_TEXTO, OCRE_DORADO_TEXTO, AZUL_OSCURO, GRIS_CLARO

kicker("Página 5 de 9")
st.title("Diseño experimental")

st.markdown(
    "Para comprobar si las decisiones de curación alteran el rendimiento predictivo, "
    "entrenamos el **mismo algoritmo** bajo distintas versiones de los datos, "
    "separando el efecto de la **población** y el de la **calidad de las variables**."
)

st.markdown("---")

# --- BLOQUE 0a: Algoritmo elegido, lo primero (la intro ya lo menciona) ---
st.markdown("### El algoritmo: Random Forest")
st.markdown(
    f"""
    <div style="background-color: #ffffff; border-top: 4px solid {AZUL_PETROLEO}; border-radius: 8px;
                padding: 0.9rem 1.1rem;">
        <div style="font-weight: 700; font-size: 1rem; color: #31333F; margin-bottom: 0.4rem;">
        <code>RandomForestRegressor</code> — 200 árboles, <code>random_state=42</code></div>
        <div style="font-size: 0.85rem; color: #444; line-height: 1.5;">
        <b>Por qué este algoritmo:</b> maneja bien las variables categóricas codificadas y relaciones no
        lineales, sin exigir que las variables estén escaladas para funcionar (el escalado se aplica
        igualmente, por buena práctica y para que el criterio sea idéntico en las 4 versiones) -- y da
        la importancia de cada variable de forma directa.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# --- BLOQUE 0b: Que variables entran en el modelo ---
st.markdown("### Qué variables entran en el modelo")

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

st.markdown(
    f"""
    <div style="position:relative; width:100%; aspect-ratio:2/1;">
      <svg width="100%" height="100%" viewBox="0 0 1400 700" xmlns="http://www.w3.org/2000/svg"
           style="position:absolute; top:0; left:0;">
        <polygon points="700,20 600,250 800,250" fill="{AZUL_OSCURO}" />
        <polygon points="600,250 500,480 700,480" fill="{AZUL_PETROLEO}" />
        <polygon points="800,250 700,480 900,480" fill="{OCRE_DORADO_TEXTO}" />
        <polygon points="600,250 700,480 800,250" fill="{GRIS_CLARO}" />
        <text x="700" y="128" text-anchor="middle" fill="white" font-size="17" font-weight="700" font-family="Helvetica">Variable</text>
        <text x="700" y="152" text-anchor="middle" fill="white" font-size="17" font-weight="700" font-family="Helvetica">objetivo</text>
        <text x="700" y="225" text-anchor="middle" fill="white" font-size="11" font-family="monospace">estimated_revenue_l365d</text>
        <text x="600" y="400" text-anchor="middle" fill="white" font-size="15" font-weight="700" font-family="Helvetica">Predictoras</text>
        <text x="600" y="422" text-anchor="middle" fill="white" font-size="13" font-family="Helvetica">(11)</text>
        <text x="800" y="400" text-anchor="middle" fill="white" font-size="15" font-weight="700" font-family="Helvetica">Excluidas</text>
        <text x="800" y="422" text-anchor="middle" fill="white" font-size="13" font-family="Helvetica">(4, causan fuga)</text>
        <defs>
          <marker id="flecha" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
            <path d="M0,0 L10,5 L0,10 z" fill="#999" />
          </marker>
        </defs>
        <line x1="595" y1="403" x2="410" y2="403" stroke="#999" stroke-width="2" marker-end="url(#flecha)" />
        <line x1="805" y1="403" x2="990" y2="403" stroke="#999" stroke-width="2" marker-end="url(#flecha)" />
      </svg>
      <div style="position:absolute; left:0%; top:40%; width:28%;">
        {_bloque_etiquetas(predictoras_num + predictoras_cat, AZUL_PETROLEO)}
      </div>
      <div style="position:absolute; left:72%; top:44%; width:26%;">
        {_bloque_etiquetas(excluidas, OCRE_DORADO_TEXTO)}
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption(
    "De las 11 predictoras, solo **bedrooms/bathrooms/beds** (nulos a rellenar) y **amenities_count** "
    "(proxy vs. cálculo real) cambian de tratamiento entre las 4 versiones -- las otras 7 llegan completas "
    "y se usan igual en todas. Las 4 excluidas forman parte de la fórmula con la que Inside Airbnb calcula "
    "el propio target -- usarlas sería hacer trampa al modelo."
)

st.markdown("---")

# --- BLOQUE 1: Las cuatro versiones en tarjetas compactas (2x2) ---
st.markdown("### Las cuatro versiones")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 1rem;">
            <div style="color: {COLOR_CRUDO}; font-weight: 700; font-size: 0.95rem; margin-bottom: 0.3rem;">■ Modelo A — Datos Crudos (Línea Base)</div>
            <div style="font-size: 0.88rem; color: #444; margin-bottom: 0.5rem; line-height: 1.4;">
                Escenario sin auditar: población completa, variables sin tratar. Sirve como referencia base.
            </div>
            <div style="font-size: 0.75rem; color: #666; text-transform: uppercase; letter-spacing: 0.5px;">n filas</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #31333F;">13.355</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 1rem;">
            <div style="color: {TURQUESA_TEXTO}; font-weight: 700; font-size: 0.95rem; margin-bottom: 0.3rem;">■ Modelo B — Datos Tratados (Criterio Principal)</div>
            <div style="font-size: 0.88rem; color: #444; margin-bottom: 0.5rem; line-height: 1.4;">
                Escenario depurado final: variables tratadas y población limpia. Representa la muestra final del proyecto.
            </div>
            <div style="font-size: 0.75rem; color: #666; text-transform: uppercase; letter-spacing: 0.5px;">n filas</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #31333F;">10.669</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 1rem;">
            <div style="color: {COLOR_D}; font-weight: 700; font-size: 0.95rem; margin-bottom: 0.3rem;">■ Modelo D — Variables Tratadas / Población Cruda</div>
            <div style="font-size: 0.88rem; color: #444; margin-bottom: 0.5rem; line-height: 1.4;">
                Solo variables tratadas: misma población que el Modelo A, para aislar el efecto de cómo se construyen las variables.
            </div>
            <div style="font-size: 0.75rem; color: #666; text-transform: uppercase; letter-spacing: 0.5px;">n filas</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #31333F;">13.355</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 1rem;">
            <div style="color: {COLOR_SENSIBILIDAD_TEXTO}; font-weight: 700; font-size: 0.95rem; margin-bottom: 0.3rem;">■ Chequeo de Sensibilidad (Criterio Alternativo)</div>
            <div style="font-size: 0.88rem; color: #444; margin-bottom: 0.5rem; line-height: 1.4;">
                Prueba de robustez: misma población que el Modelo B, con otro criterio de imputación.
            </div>
            <div style="font-size: 0.75rem; color: #666; text-transform: uppercase; letter-spacing: 0.5px;">n filas</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #31333F;">10.669</div>
        </div>
        """,
        unsafe_allow_html=True
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
            <li><code>amenities_count</code>: parseo real (lista JSON), igual que en el Modelo B</li>
        </ul>

        <div style="color: {TURQUESA_TEXTO}; font-weight: 700; font-size: 0.9rem; margin-bottom: 0.2rem;">Modelo B — TRATADO-A</div>
        <ul style="font-size: 0.85rem; color: #444; line-height: 1.6; margin: 0 0 0.8rem 1.1rem; padding: 0;">
            <li>Excluye los 2.686 casos <code>revenue_no_estimable</code></li>
            <li><code>bedrooms</code>/<code>bathrooms</code>/<code>beds</code>: mediana por <code>accommodates</code></li>
            <li><code>host_listings_count</code>: relleno técnico = <code>1</code></li>
            <li><code>host_is_superhost</code>: relleno técnico = <code>f</code></li>
            <li><code>amenities_count</code>: parseo real (lista JSON)</li>
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

# --- BLOQUE 1b: Cómo se evalúa cada versión (80/20) ---
st.markdown("### Cómo se evalúa cada versión")
st.markdown(
    "Para cada una de las 4 versiones, los datos se dividieron en dos conjuntos: **80% para "
    "entrenamiento** (el algoritmo aprende patrones entre las variables predictoras y el target) y "
    "**20% para prueba** (filas que el modelo no vio al entrenar, usadas solo para medir MAE, RMSE y "
    "R²). Misma proporción y misma semilla (`random_state=42`) en las 4 versiones, para que cualquier "
    "diferencia en las métricas venga del tratamiento de los datos, no de una partición distinta."
)
st.markdown(
    f'<div style="border-radius:8px; overflow:hidden; display:flex; height:2.4rem; margin:0.6rem 0 0.3rem 0;">'
    f'<div style="width:80%; background-color:{AZUL_PETROLEO}; color:white; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:0.95rem;">80%</div>'
    f'<div style="width:20%; background-color:{OCRE_DORADO_TEXTO}; color:white; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:0.95rem;">20%</div>'
    f'</div>'
    f'<div style="display:flex; justify-content:space-between; font-size:0.8rem; color:#666;">'
    f'<span>Entrenamiento — aprender patrones</span><span>Prueba — evaluar</span>'
    f'</div>',
    unsafe_allow_html=True,
)
st.caption(
    "Esto es la división **dentro de cada versión por separado** -- no confundir con la 'muestra común "
    "de 426 filas' del diagrama de abajo, que es un subconjunto adicional construido después, para "
    "comparar las versiones entre sí sin fuga de datos (ver 'Resultados y robustez')."
)

st.markdown("---")

# --- BLOQUE 1c: Estandarizacion y codificacion, identicas en las 4 versiones ---
st.markdown("### Antes de entrenar: mismo criterio en las 4 versiones")
col_std, col_ohe = st.columns(2)
with col_std:
    st.markdown(
        f"""
        <div style="background-color: #ffffff; border-top: 4px solid {AZUL_PETROLEO}; border-radius: 8px;
                    padding: 0.9rem 1rem; height: 100%;">
            <div style="color: {AZUL_PETROLEO}; font-weight: 700; font-size: 0.95rem;">StandardScaler</div>
            <div style="font-size: 0.78rem; color: #888; text-transform: uppercase; margin-bottom: 0.4rem;">
            Variables numéricas</div>
            <div style="font-size: 0.85rem; color: #444; line-height: 1.4;">
            Cada variable se reescala a media 0 y desviación 1, ajustado solo con el 80% de entrenamiento.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_ohe:
    st.markdown(
        f"""
        <div style="background-color: #ffffff; border-top: 4px solid {TURQUESA_TEXTO}; border-radius: 8px;
                    padding: 0.9rem 1rem; height: 100%;">
            <div style="color: {TURQUESA_TEXTO}; font-weight: 700; font-size: 0.95rem;">OneHotEncoder</div>
            <div style="font-size: 0.78rem; color: #888; text-transform: uppercase; margin-bottom: 0.4rem;">
            Variables categóricas</div>
            <div style="font-size: 0.85rem; color: #444; line-height: 1.4;">
            Cada categoría se convierte en una columna binaria, también ajustado solo con el 80% de entrenamiento.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.caption(
    "Mismo criterio de escalado y codificación en las 4 versiones (dentro de un `Pipeline`, para no "
    "filtrar información del test) -- lo único que cambia entre versiones es la población y la "
    "construcción de las variables, que es justo lo que se quiere comparar."
)

st.markdown("---")

# --- BLOQUE 2: Diagrama de arquitectura experimental ---
st.markdown("### Diagrama: población, tratamiento y comparaciones")
dot_experimento = f"""
digraph Experimento {{
  rankdir=LR;
  node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=12, margin=0.15, color="{AZUL_PETROLEO}"];
  edge [fontname="Helvetica", fontsize=10, color="#888888"];

  raw [label="listings_raw\\n(15.293 filas, 90 cols)\\nsin tratamiento", fillcolor="#E3E9EF", color="{COLOR_CRUDO}"];
  curado [label="listings_curado\\n(15.293 filas, 91 cols)\\ntratado: L1, L2, L4, target", fillcolor="#DCEEEC", color="{COLOR_TRATADO}"];

  mod_a [label="Modelo A — CRUDO\\nn=13.355\\n(variables sin tratar)", fillcolor="#E3E9EF", color="{COLOR_CRUDO}"];
  mod_d [label="Modelo D\\nn=13.355\\n(población de A, variables tratadas)", fillcolor="#EAE4F0", color="{COLOR_D}"];
  mod_b [label="Modelo B — TRATADO-A\\nn=10.669\\n(población y variables tratadas)", fillcolor="#DCEEEC", color="{COLOR_TRATADO}"];

  chequeo [label="Chequeo sensibilidad\\nn=10.669\\n(otro criterio de imputación)", fillcolor="#E2E3E5", color="{COLOR_SENSIBILIDAD}"];
  comun [label="Muestra común segura\\nn=426\\n(sin fuga de datos)", shape=ellipse, fillcolor="#FBEED6", color="{AMBAR_PENDIENTE}"];

  raw -> mod_a [label="mismas filas,\\notras variables"];
  raw -> mod_d;
  curado -> mod_b [label="misma población,\\notro criterio imputación"];
  curado -> chequeo;

  mod_a -> comun [style=dashed];
  mod_d -> comun [style=dashed];
  mod_b -> comun [style=dashed];
}}
"""
st.graphviz_chart(dot_experimento, width="stretch")
