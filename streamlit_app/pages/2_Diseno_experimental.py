import streamlit as st

from src.data_loader import cargar_modelo
from src.styles import kicker

modelo = cargar_modelo()

kicker("Pagina 5 de 9")
st.title("Diseño experimental")
st.markdown(
    "Ya se sabe que problemas de calidad existen y que se decidio hacer con cada uno (pagina anterior). "
    "La pregunta que sigue es: ¿esas decisiones de curacion cambian algo cuando los datos se usan para "
    "una tarea real, como predecir ingresos? Para responder con rigor -- no solo comparar antes/despues "
    "a ojo -- se diseña un experimento controlado."
)
st.markdown(
    "Se entrena el **mismo algoritmo y configuración general** (mismo `random_state`, mismos "
    "hiperparámetros) sobre distintas versiones de los datos -- con particiones de train/test "
    "específicas para cada población evaluada, ya que A/D (13.355 filas) y B (10.669 filas) parten "
    "de un número distinto de filas -- para aislar que efecto viene de la **poblacion** evaluada y "
    "cual viene de la **construccion de variables**."
)

st.markdown("### Las cuatro versiones")
versiones = modelo.get("versiones", {})
cols = st.columns(4)
etiquetas = [
    ("A_crudo", "A — CRUDO"),
    ("D_variables_tratadas_poblacion_cruda", "D — Variables tratadas, poblacion cruda"),
    ("B_tratado_criterio_A", "B — TRATADO (criterio A)"),
    ("TRATADO_criterio_B_barrio", "Chequeo sensibilidad (criterio B)"),
]
for col, (clave, titulo) in zip(cols, etiquetas):
    v = versiones.get(clave, {})
    with col:
        st.markdown(f"**{titulo}**")
        st.caption(v.get("descripcion", ""))
        st.metric("n filas", f'{v.get("n", "—"):,}'.replace(",", "."))

st.markdown("---")
st.markdown("### Diagrama: poblacion, tratamiento y comparaciones")

dot = r"""
digraph DataTrust {
  rankdir=LR;
  node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=11, margin=0.15];
  edge [fontname="Helvetica", fontsize=9, color="#888888"];

  raw [label="listings_raw\n(15.293 filas, 90 cols)\nsin tratamiento", fillcolor="#FDECEC", color="#D03B3B"];
  curado [label="listings_curado\n(15.293 filas, 91 cols)\ntratado: L1,L2,L4,target", fillcolor="#E7F6E7", color="#0CA30C"];

  A [label="Modelo A — CRUDO\nnulos predictoras: -1\namenities: proxy texto\nincluye 2.686 filas con target=0\nn=13.355", fillcolor="#FDECEC", color="#D03B3B"];
  D [label="Modelo D\npoblacion = A (13.355)\nvariables = tratadas\n(amenities real, mediana)", fillcolor="#FFF3DC", color="#C98A1B"];
  B [label="Modelo B — TRATADO-A\npoblacion sin 2.686 'no estimable'\nvariables tratadas\nn=10.669", fillcolor="#E7F6E7", color="#0CA30C"];
  Bsens [label="Chequeo sensibilidad\nmismo B, imputa por\nbarrio en vez de capacidad", fillcolor="#EAF2F8", color="#14506B"];

  raw -> A;
  raw -> D [label="  mismas filas,\n  otras variables"];
  curado -> B;
  curado -> Bsens [label="  misma poblacion,\n  otro criterio imputacion"];

  comun [label="Muestra comun segura\nn=426\n(sin fuga de datos)", shape=ellipse, fillcolor="#FFF3DC", color="#C98A1B"];
  A -> comun [style=dashed];
  D -> comun [style=dashed];
  B -> comun [style=dashed];

  {rank=same; A; D}
}
"""
st.graphviz_chart(dot, width="stretch")
st.caption(
    "Linea solida = de donde viene cada modelo. Linea punteada = las tres versiones se re-evaluan, sin "
    "reentrenar, sobre la misma muestra pequena y segura de 426 filas (ver 'Resultados y robustez')."
)

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.markdown("### ¿Qué separa cada comparación?")
    st.markdown(
        "- **A vs. D** (misma poblacion, 13.355 filas): aisla el efecto de **como se construyen las "
        "variables** (amenities real vs. proxy, imputacion por mediana vs. centinela `-1`).\n"
        "- **A vs. B** (poblaciones distintas): combina el efecto de poblacion y de variables a la vez -- "
        "no se puede repartir sin la muestra comun.\n"
        "- **A, D y B sobre la muestra comun de 426 filas**: la unica comparacion de los tres sin fuga de "
        "datos, sobre casos que ningun modelo vio al entrenar."
    )
with col2:
    st.markdown("### ¿Por qué Random Forest?")
    st.markdown(
        "Maneja variables categoricas codificadas y relaciones no lineales sin necesitar escalar las "
        "variables, y da una medida de importancia de variables de forma directa. **No se presenta como "
        "la unica opcion posible**, ni la importancia de variables se interpreta como causalidad -- "
        "ver pagina 'Metodología y limitaciones'."
    )
    algoritmo = modelo.get("algoritmo", {})
    st.code(
        f"RandomForestRegressor(\n"
        f"    n_estimators={algoritmo.get('n_estimators', '—')},\n"
        f"    random_state={algoritmo.get('random_state', '—')},\n"
        f"    n_jobs={algoritmo.get('n_jobs', '—')},\n"
        f")\n# {algoritmo.get('split', '—')}",
        language="python",
    )
