import streamlit as st

from src.styles import kicker, caja_alerta, fmt_num, VERDE_OK, AMBAR_PENDIENTE, AZUL_PETROLEO

kicker("Página 5 de 9")
st.title("Diseño experimental")

st.markdown(
    "Para comprobar si las decisiones de curación alteran el rendimiento predictivo, "
    "entrenamos el **mismo algoritmo** bajo distintas versiones de los datos, "
    "separando el efecto de la **población** y el de la **calidad de las variables**."
)

st.markdown("---")

# --- BLOQUE 1: Las cuatro versiones en tarjetas compactas (2x2) ---
st.markdown("### Las cuatro versiones")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 1rem;">
            <div style="color: #DC3545; font-weight: 700; font-size: 0.95rem; margin-bottom: 0.3rem;">■ Modelo A — Datos Crudos (Línea Base)</div>
            <div style="font-size: 0.88rem; color: #444; margin-bottom: 0.5rem; line-height: 1.4;">
                Escenario sin auditar. Mantiene los nulos con centinela (<code>-1</code>) y los 2.686 casos 'no estimable' contabilizados como ceros reales. Sirve como referencia base.
            </div>
            <div style="font-size: 0.75rem; color: #666; text-transform: uppercase; letter-spacing: 0.5px;">n filas</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #31333F;">13.355</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 1rem;">
            <div style="color: #198754; font-weight: 700; font-size: 0.95rem; margin-bottom: 0.3rem;">■ Modelo B — Datos Tratados (Criterio Principal)</div>
            <div style="font-size: 0.88rem; color: #444; margin-bottom: 0.5rem; line-height: 1.4;">
                Escenario depurado final. Excluye los 2.686 casos <code>revenue_no_estimable</code> e imputa los nulos por capacidad (<code>accommodates</code>). Representa la muestra limpia.
            </div>
            <div style="font-size: 0.75rem; color: #666; text-transform: uppercase; letter-spacing: 0.5px;">n filas</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #31333F;">10.669</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 1rem;">
            <div style="color: #D4A017; font-weight: 700; font-size: 0.95rem; margin-bottom: 0.3rem;">■ Modelo D — Variables Tratadas / Población Cruda</div>
            <div style="font-size: 0.88rem; color: #444; margin-bottom: 0.5rem; line-height: 1.4;">
                Aísla el efecto de las variables. Mantiene la población completa (13.355 filas) y los ceros originales, pero corrige el cálculo de amenities y nulos.
            </div>
            <div style="font-size: 0.75rem; color: #666; text-transform: uppercase; letter-spacing: 0.5px;">n filas</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #31333F;">13.355</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8rem 1rem; margin-bottom: 1rem;">
            <div style="color: #6C757D; font-weight: 700; font-size: 0.95rem; margin-bottom: 0.3rem;">■ Chequeo de Sensibilidad (Criterio Alternativo)</div>
            <div style="font-size: 0.88rem; color: #444; margin-bottom: 0.5rem; line-height: 1.4;">
                Prueba de robustez. Parte de las 10.669 filas limpias del Modelo B pero imputando los nulos por barrio (<code>neighbourhood_cleansed</code>).
            </div>
            <div style="font-size: 0.75rem; color: #666; text-transform: uppercase; letter-spacing: 0.5px;">n filas</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #31333F;">10.669</div>
        </div>
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
    f'<div style="width:20%; background-color:{AMBAR_PENDIENTE}; color:white; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:0.95rem;">20%</div>'
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

# --- BLOQUE 2: Diagrama de arquitectura experimental ---
st.markdown("### Diagrama: población, tratamiento y comparaciones")
dot_experimento = r"""
digraph Experimento {
  rankdir=LR;
  node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=12, margin=0.15, color="#14506B"];
  edge [fontname="Helvetica", fontsize=10, color="#888888"];

  raw [label="listings_raw\n(15.293 filas, 90 cols)\nsin tratamiento", fillcolor="#F8D7DA", color="#DC3545"];
  curado [label="listings_curado\n(15.293 filas, 91 cols)\ntratado: L1, L2, L4, target", fillcolor="#D1E7DD", color="#198754"];
  
  mod_a [label="Modelo A — CRUDO\nnulos predictoras: -1\namenities: proxy texto\nincluye 2.686 filas con target=0\nn=13.355", fillcolor="#F8D7DA", color="#DC3545"];
  mod_d [label="Modelo D\npoblación = A (13.355)\nvariables tratadas\n(amenities real, mediana)", fillcolor="#FFF3CD", color="#FFC107"];
  mod_b [label="Modelo B — TRATADO-A\npoblación sin 2.686 'no estimable'\nvariables tratadas\nn=10.669", fillcolor="#D1E7DD", color="#198754"];
  
  chequeo [label="Chequeo sensibilidad\nmismo B, imputa por\nbarrio en vez de capacidad", fillcolor="#E2E3E5", color="#6C757D"];
  comun [label="Muestra común segura\nn=426\n(sin fuga de datos)", shape=ellipse, fillcolor="#FFE69C", color="#FFC107"];

  raw -> mod_a [label="mismas filas,\notras variables"];
  raw -> mod_d;
  curado -> mod_b [label="misma población,\notro criterio imputación"];
  curado -> chequeo;
  
  mod_a -> comun [style=dashed];
  mod_d -> comun [style=dashed];
  mod_b -> comun [style=dashed];
}
"""
st.graphviz_chart(dot_experimento, width="stretch")

st.markdown("---")

# --- BLOQUE 3: Lógica metodológica de las comparaciones (3 columnas horizontales) ---
st.markdown("### Lógica metodológica de las comparaciones")

col_c1, col_c2, col_c3 = st.columns(3)

with col_c1:
    st.markdown(
        """
        <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8rem 0.9rem; height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                <span style="font-size: 0.7rem; color: #666; font-weight: 600; text-transform: uppercase;">Comparación 01</span>
                <span style="background-color: #e2f0d9; color: #385723; font-size: 0.68rem; font-weight: 600; padding: 0.1rem 0.4rem; border-radius: 4px;">Misma población</span>
            </div>
            <div style="font-weight: 700; font-size: 0.95rem; color: #31333F; margin-bottom: 0.3rem;">A vs. D</div>
            <div style="font-size: 0.82rem; color: #444; margin-bottom: 0.4rem; line-height: 1.4;">
                Aísla el efecto exclusivo de la <b>construcción de variables</b> (crudo vs. amenities reales e imputación correcta).
            </div>
            <div style="font-size: 0.75rem; color: #2e7d32; font-weight: 600;">Variables → efecto aislado</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_c2:
    st.markdown(
        """
        <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8rem 0.9rem; height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                <span style="font-size: 0.7rem; color: #666; font-weight: 600; text-transform: uppercase;">Comparación 02</span>
                <span style="background-color: #dbe5f1; color: #1f3864; font-size: 0.68rem; font-weight: 600; padding: 0.1rem 0.4rem; border-radius: 4px;">Pob. distintas</span>
            </div>
            <div style="font-weight: 700; font-size: 0.95rem; color: #31333F; margin-bottom: 0.3rem;">A vs. B</div>
            <div style="font-size: 0.82rem; color: #444; margin-bottom: 0.4rem; line-height: 1.4;">
                Combina cambios de población y variables al excluir los 2.686 casos 'no estimable' y aplicar mejoras.
            </div>
            <div style="font-size: 0.75rem; color: #1f3864; font-weight: 600;">Pob. + variables → combinado</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_c3:
    st.markdown(
        """
        <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 0.8rem 0.9rem; height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                <span style="font-size: 0.7rem; color: #666; font-weight: 600; text-transform: uppercase;">Comparación 03</span>
                <span style="background-color: #fff2cc; color: #806000; font-size: 0.68rem; font-weight: 600; padding: 0.1rem 0.4rem; border-radius: 4px;">n = 426</span>
            </div>
            <div style="font-weight: 700; font-size: 0.95rem; color: #31333F; margin-bottom: 0.3rem;">Muestra común</div>
            <div style="font-size: 0.82rem; color: #444; margin-bottom: 0.4rem; line-height: 1.4;">
                Evaluación limpia sobre un subconjunto seguro no visto en entrenamiento, evitando la fuga de datos.
            </div>
            <div style="font-size: 0.75rem; color: #806000; font-weight: 600;">Mismos casos → comparable</div>
        </div>
        """,
        unsafe_allow_html=True
    )