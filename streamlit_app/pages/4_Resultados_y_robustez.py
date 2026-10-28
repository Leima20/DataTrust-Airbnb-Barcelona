import pandas as pd
import streamlit as st

from src.data_loader import cargar_modelo, cargar_simulacion_valores
from src.styles import kicker, caja_alerta, fmt_num
from src.charts import dispersion_muestra_simulada, intervalo_confianza

modelo = cargar_modelo()
simulacion_real = cargar_simulacion_valores()

kicker("Pagina 7 de 9")
st.title("Resultados, robustez e interpretación")
st.markdown(
    "Esta es la pagina central del proyecto. Los R² de la pagina anterior invitan a sacar una "
    "conclusion rapida -- pero **se evaluan sobre poblaciones distintas**, y comparar asi puede "
    "engañar. Antes de confiar en cualquier diferencia entre modelos, se investigo si la comparacion "
    "en si misma era confiable. No lo era: se encontro un problema real."
)

st.markdown("---")
st.markdown("## 1. La fuga de datos detectada y corregida")
fuga = modelo.get("fuga_de_datos_detectada_y_corregida", {})
caja_alerta(
    f"Un primer intento de comparar A y D contra el test de B dio un resultado sospechoso "
    f"(R² ≈ 0,82). Se investigo y se encontro: **{fmt_num(fuga.get('n_contaminadas', 0))} de "
    f"{fmt_num(fuga.get('n_test_B_total', 0))} filas ({fmt_num(fuga.get('pct_filas_contaminadas', 0), 0)}%)** del test de B "
    "ya formaban parte del entrenamiento de A y D -- evaluar con datos ya vistos infla el resultado "
    "artificialmente. Se corrigio antes de reportar nada."
)
st.markdown(fuga.get("correccion", ""))

st.markdown("---")
st.markdown("## 2. ¿De dónde viene realmente la diferencia entre A y B?")
pob = modelo.get("poblacion_limpia_experimento", {})
st.markdown(pob.get("nota", ""))
if pob:
    df_pob = pd.DataFrame([
        {"Evaluación": "A, sobre toda su población", "MAE (€)": fmt_num(pob["A_toda_poblacion"]["mae"], 1), "R²": fmt_num(pob["A_toda_poblacion"]["r2"], 3)},
        {"Evaluación": "A, solo sobre población limpia", "MAE (€)": fmt_num(pob["A_solo_poblacion_limpia"]["mae"], 1), "R²": fmt_num(pob["A_solo_poblacion_limpia"]["r2"], 3)},
        {"Evaluación": "D, solo sobre población limpia", "MAE (€)": fmt_num(pob["D_solo_poblacion_limpia"]["mae"], 1), "R²": fmt_num(pob["D_solo_poblacion_limpia"]["r2"], 3)},
        {"Evaluación": "B, su propia población limpia", "MAE (€)": fmt_num(pob["B_propia_poblacion_limpia"]["mae"], 1), "R²": fmt_num(pob["B_propia_poblacion_limpia"]["r2"], 3)},
    ])
    st.dataframe(df_pob, width="stretch", hide_index=True)
    st.info(pob.get("conclusion", ""))
aislar = modelo.get("aislar_variables_vs_poblacion", {})
if aislar:
    st.caption(aislar.get("conclusion", ""))

st.markdown("---")
st.markdown("## 3. Comparación sobre la muestra común segura (426 filas)")
muestra = modelo.get("muestra_comun_426", {})
st.markdown(muestra.get("representatividad", ""))
resultados_426 = muestra.get("resultados", {})
if resultados_426:
    df = pd.DataFrame([
        {"Modelo": "A (CRUDO)", "MAE (€)": fmt_num(resultados_426["A_crudo"]["mae"], 1), "R²": fmt_num(resultados_426["A_crudo"]["r2"], 3)},
        {"Modelo": "D (variables tratadas)", "MAE (€)": fmt_num(resultados_426["D_variables_tratadas_poblacion_cruda"]["mae"], 1), "R²": fmt_num(resultados_426["D_variables_tratadas_poblacion_cruda"]["r2"], 3)},
        {"Modelo": "B (TRATADO-A)", "MAE (€)": fmt_num(resultados_426["B_tratado_criterio_A"]["mae"], 1), "R²": fmt_num(resultados_426["B_tratado_criterio_A"]["r2"], 3)},
    ])
    st.dataframe(df, width="stretch", hide_index=True)
    st.caption(muestra.get("progresion", ""))

st.markdown("---")
st.markdown("## 4. ¿Por qué la diferencia A-D es distinta aquí que en la muestra grande?")
disc = modelo.get("discrepancia_426_vs_2131", {})
st.markdown(disc.get("descripcion", ""))

sim = modelo.get("simulacion_5000_submuestras", {})
if sim:
    diffs_reales = simulacion_real.get("diffs_sim_426")
    col1, col2 = st.columns([3, 2])
    with col1:
        if diffs_reales:
            st.plotly_chart(
                dispersion_muestra_simulada(diffs_reales, sim.get("diferencia_real_observada_426", 0)),
                width="stretch",
            )
            st.caption(
                "Histograma con los 5.000 valores reales de la simulacion (semilla fija 42, "
                "reproducible) -- no es una aproximacion."
            )
        else:
            caja_alerta(
                "No se encontraron los 5.000 valores reales de la simulacion -- falta "
                "`simulacion_5000_valores.json`. No se muestra un histograma aproximado en su lugar."
            )
    with col2:
        st.metric("Media de 5.000 simulaciones", fmt_num(sim.get('r2_diferencia_media', 0), 4))
        st.metric("Desviación estándar", fmt_num(sim.get('r2_diferencia_std', 0), 4))
        rango = sim.get('rango_central_95', [0, 0])
        st.metric("Rango central (2.5%-97.5%)", f"[{fmt_num(rango[0], 4)}, {fmt_num(rango[1], 4)}]")
        st.metric("Resultado real observado (426 filas)", fmt_num(sim.get('diferencia_real_observada_426', 0), 4))
        st.metric("Percentil del resultado real", fmt_num(sim.get('percentil_del_resultado_real', 0), 1))
    st.info(sim.get("conclusion", ""))

st.markdown("---")
st.markdown("## 5. Intervalos de confianza (bootstrap emparejado, 5.000 repeticiones)")
boot = modelo.get("bootstrap_intervalos_confianza", {})
comparaciones = boot.get("comparaciones", [])
if comparaciones:
    st.plotly_chart(
        intervalo_confianza(
            [c["nombre"] for c in comparaciones],
            [c["diferencia_media"] for c in comparaciones],
            [c["ic_95"][0] for c in comparaciones],
            [c["ic_95"][1] for c in comparaciones],
        ),
        width="stretch",
    )
    st.caption("Gris = el intervalo incluye el cero (no concluyente). Verde = el intervalo NO incluye el "
               "cero (diferencia estadisticamente distinguible de cero).")
    for c in comparaciones:
        incluye = "incluye el 0 (no concluyente)" if c["incluye_cero"] else "NO incluye el 0 (distinguible de cero)"
        st.markdown(f"- **{c['nombre']}**: diferencia media {fmt_num(c['diferencia_media'], 4)}, IC95% "
                    f"[{fmt_num(c['ic_95'][0], 4)}, {fmt_num(c['ic_95'][1], 4)}] — {incluye}")
st.markdown(boot.get("conclusion", ""))

caja_alerta(
    "**Que un intervalo incluya el 0 NO demuestra que el efecto sea nulo** -- solo indica que, con esta "
    "muestra y este metodo, no hay evidencia suficientemente precisa para distinguirlo de cero. No se "
    "concluye 'A y D son iguales', se concluye 'no se puede afirmar cual es mejor con esta muestra'."
)
caja_alerta(
    "**El intervalo de A-B tampoco es una certeza absoluta**: su limite superior (-0,0043) esta muy "
    "cerca de cero -- es evidencia de una diferencia en esta evaluacion concreta, con incertidumbre "
    "considerable, no una prueba de que el tratamiento mejora el modelo en cualquier contexto o muestra."
)

st.markdown("---")
st.markdown("## 6. Importancia de variables")
imp = modelo.get("importancia_variables", {})
st.markdown(imp.get("nota", ""))
caja_alerta(imp.get("caveat", ""))

st.markdown("---")
st.markdown("## Conclusión de esta sección")
concl = modelo.get("conclusion_final", {})
st.success(f"**Lo observado:** {concl.get('observado', '')}")
st.warning(f"**Interpretación razonable:** {concl.get('interpretacion_razonable', '')}")
st.info(f"**Lo que sigue sin resolver:** {concl.get('sin_resolver', '')}")
