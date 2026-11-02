import pandas as pd
import streamlit as st

from src.data_loader import cargar_modelo, cargar_simulacion_valores
from src.styles import kicker, caja_alerta, fmt_num, ROJO_ALERTA, VERDE_OK, COLOR_CRUDO, COLOR_TRATADO, COLOR_NEUTRO, AMBAR_PENDIENTE
from src.charts import dispersion_muestra_simulada, intervalo_confianza, r2_muestra_comun, importancia_variables

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
tab_resultados, tab_confianza = st.tabs(["📊 Resultados", "🔍 Confianza y conclusión"])

with tab_resultados:
    st.markdown("## 1. La fuga de datos detectada y corregida")
    fuga = modelo.get("fuga_de_datos_detectada_y_corregida", {})
    n_comun_426 = modelo.get("muestra_comun_426", {}).get("n", 0)
    st.markdown(
        f'<div style="background-color: #fff; border: 1px solid #e0e0e0; border-left: 4px solid {ROJO_ALERTA}; border-radius: 8px; padding: 1rem 1.2rem; margin: 1rem 0;">'
        f'<div style="font-size: 0.95rem; font-weight: 700; color: #31333F; margin-bottom: 0.9rem;">Una evaluación inicial pareció demasiado buena: R² ≈ 0,82</div>'
        f'<div style="display: flex; flex-wrap: wrap; gap: 2rem; margin-bottom: 0.8rem;">'
        f'<div><div style="font-size:2rem; font-weight:800; color:{ROJO_ALERTA};">{fmt_num(fuga.get("pct_filas_contaminadas", 0), 0)}%</div>'
        f'<div style="font-size:0.78rem; color:#666; max-width:220px;">Solapamiento -- filas del test de B que ya estaban en el entrenamiento de A/D '
        f'({fmt_num(fuga.get("n_contaminadas", 0))} de {fmt_num(fuga.get("n_test_B_total", 0))})</div></div>'
        f'<div><div style="font-size:2rem; font-weight:800; color:{VERDE_OK};">{fmt_num(n_comun_426)}</div>'
        f'<div style="font-size:0.78rem; color:#666; max-width:220px;">Casos seguros -- la base de la comparación corregida (sección 3)</div></div>'
        f'</div>'
        f'<div style="font-size:0.85rem; color:#555; border-top:1px solid #eee; padding-top:0.6rem;">'
        f'Evaluar con datos ya vistos infla el resultado artificialmente -- se corrigió antes de reportar nada. '
        f'{fuga.get("correccion", "")}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("## 2. ¿De dónde viene realmente la diferencia entre A y B?")
    pob = modelo.get("poblacion_limpia_experimento", {})
    st.caption(pob.get("nota", ""))
    if pob:
        st.plotly_chart(
            r2_muestra_comun(
                ["A · toda su población", "D · población limpia", "A · población limpia", "B · población limpia"],
                [pob["A_toda_poblacion"]["r2"], pob["D_solo_poblacion_limpia"]["r2"], pob["A_solo_poblacion_limpia"]["r2"], pob["B_propia_poblacion_limpia"]["r2"]],
                [AMBAR_PENDIENTE, COLOR_NEUTRO, COLOR_CRUDO, COLOR_TRATADO],
                titulo="R² de A al cambiar solo la población evaluada",
            ),
            width="stretch",
        )
        aislar = modelo.get("aislar_variables_vs_poblacion", {})
        r2_var = aislar.get("A_vs_D_r2_diferencia", 0)
        rango_pob = aislar.get("cambio_poblacion_r2_diferencia_rango", [0, 0])
        st.markdown(
            f'<div style="background-color: #f8f9fa; border: 1px solid #e0e0e0; border-left: 4px solid {COLOR_NEUTRO}; border-radius: 8px; padding: 0.9rem 1.1rem; margin: 0.8rem 0;">'
            f'<div style="font-size: 0.95rem; font-weight: 700; color: #31333F; margin-bottom: 0.5rem;">El factor dominante es la población evaluada, no la construcción de variables</div>'
            f'<div style="font-size: 0.85rem; color: #555;">Cambiar solo las variables (A vs. D): <b>{fmt_num(r2_var, 3)}</b> de diferencia en R². '
            f'Cambiar solo la población evaluada: <b>{fmt_num(rango_pob[0], 3)}-{fmt_num(rango_pob[1], 3)}</b> -- un efecto 6-7 veces mayor.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        with st.expander("Ver MAE y n de cada evaluación"):
            df_pob = pd.DataFrame([
                {"Evaluación": "A, sobre toda su población", "n test": fmt_num(pob["A_toda_poblacion"]["n_test"]), "MAE (€)": fmt_num(pob["A_toda_poblacion"]["mae"], 1), "R²": fmt_num(pob["A_toda_poblacion"]["r2"], 3)},
                {"Evaluación": "A, solo sobre población limpia", "n test": fmt_num(pob["A_solo_poblacion_limpia"]["n_test"]), "MAE (€)": fmt_num(pob["A_solo_poblacion_limpia"]["mae"], 1), "R²": fmt_num(pob["A_solo_poblacion_limpia"]["r2"], 3)},
                {"Evaluación": "D, solo sobre población limpia", "n test": fmt_num(pob["D_solo_poblacion_limpia"]["n_test"]), "MAE (€)": fmt_num(pob["D_solo_poblacion_limpia"]["mae"], 1), "R²": fmt_num(pob["D_solo_poblacion_limpia"]["r2"], 3)},
                {"Evaluación": "B, su propia población limpia", "n test": fmt_num(pob["B_propia_poblacion_limpia"]["n_test"]), "MAE (€)": fmt_num(pob["B_propia_poblacion_limpia"]["mae"], 1), "R²": fmt_num(pob["B_propia_poblacion_limpia"]["r2"], 3)},
            ])
            st.dataframe(df_pob, width="stretch", hide_index=True)
        st.caption(pob.get("conclusion", ""))

    st.markdown("---")
    st.markdown("## 3. Comparación sobre la muestra común segura (426 filas)")
    muestra = modelo.get("muestra_comun_426", {})
    st.markdown(muestra.get("representatividad", ""))
    resultados_426 = muestra.get("resultados", {})
    if resultados_426:
        st.plotly_chart(
            r2_muestra_comun(
                ["A · Crudo", "D · Variables tratadas", "B · Tratado"],
                [resultados_426["A_crudo"]["r2"], resultados_426["D_variables_tratadas_poblacion_cruda"]["r2"], resultados_426["B_tratado_criterio_A"]["r2"]],
                [COLOR_CRUDO, COLOR_NEUTRO, COLOR_TRATADO],
            ),
            width="stretch",
        )
        st.caption(muestra.get("progresion", ""))
        with st.expander("Ver métricas detalladas (MAE)"):
            df = pd.DataFrame([
                {"Modelo": "A (CRUDO)", "MAE (€)": fmt_num(resultados_426["A_crudo"]["mae"], 1), "R²": fmt_num(resultados_426["A_crudo"]["r2"], 3)},
                {"Modelo": "D (variables tratadas)", "MAE (€)": fmt_num(resultados_426["D_variables_tratadas_poblacion_cruda"]["mae"], 1), "R²": fmt_num(resultados_426["D_variables_tratadas_poblacion_cruda"]["r2"], 3)},
                {"Modelo": "B (TRATADO-A)", "MAE (€)": fmt_num(resultados_426["B_tratado_criterio_A"]["mae"], 1), "R²": fmt_num(resultados_426["B_tratado_criterio_A"]["r2"], 3)},
            ])
            st.dataframe(df, width="stretch", hide_index=True)

    st.markdown("---")
    sec5, sec6 = st.columns(2)
    with sec5:
        with st.container(border=True):
            st.markdown("**5 · Chequeo de sensibilidad**")
            st.caption("¿Importa el criterio de imputación (barrio vs. capacidad)?")
            sens = modelo.get("versiones", {}).get("TRATADO_criterio_B_barrio", {})
            diff = sens.get("diferencia_vs_A", {})
            if diff:
                st.markdown(f"MAE: **{fmt_num(diff.get('mae_eur', 0), 1)} €** ({fmt_num(diff.get('mae_pct', 0), 2)}% relativo) · R²: **{fmt_num(diff.get('r2', 0), 3)}**")
                st.caption("La conclusión del modelo no depende de cuál de los dos criterios razonables se use.")

    with sec6:
        with st.container(border=True):
            st.markdown("**6 · Importancia de variables**")
            imp = modelo.get("importancia_variables", {})
            valores_imp = imp.get("valores", [])
            if valores_imp:
                df_imp = pd.DataFrame(valores_imp).set_index("variable")
                st.plotly_chart(
                    importancia_variables(df_imp, "tratado_a", titulo="Importancia (Modelo B, tratado)"),
                    width="stretch",
                )
            st.caption("Las mismas 8 variables dominan en las tres versiones -- ninguna variable geográfica específica entra en el top 8.")
            st.caption(f"⚠️ {imp.get('caveat', '')}")
            if valores_imp:
                with st.expander("Ver comparación entre las 3 versiones (A, B, sensibilidad)"):
                    st.dataframe(
                        df_imp.rename(columns={"crudo": "A (crudo)", "tratado_a": "B (tratado)", "tratado_b": "Sensibilidad"}),
                        width="stretch",
                    )

with tab_confianza:
    st.markdown("## 4. ¿Cuánta confianza hay en estos resultados?")
    disc = modelo.get("discrepancia_426_vs_2131", {})
    st.caption(disc.get("descripcion", ""))

    sim = modelo.get("simulacion_5000_submuestras", {})
    boot = modelo.get("bootstrap_intervalos_confianza", {})
    comparaciones = boot.get("comparaciones", [])

    sub1, sub2 = st.columns(2)
    with sub1:
        st.markdown("**A · Variación entre subconjuntos del universo**")
        st.caption("¿Qué pasaría si eligiéramos otros 426 casos?")
        if sim:
            diffs_reales = simulacion_real.get("diffs_sim_426")
            if diffs_reales:
                st.plotly_chart(
                    dispersion_muestra_simulada(diffs_reales, sim.get("diferencia_real_observada_426", 0)),
                    width="stretch",
                )
            else:
                caja_alerta(
                    "No se encontraron los 5.000 valores reales de la simulacion -- falta "
                    "`simulacion_5000_valores.json`. No se muestra un histograma aproximado en su lugar."
                )
            st.metric("Percentil del resultado real", fmt_num(sim.get('percentil_del_resultado_real', 0), 1))
            with st.expander("Ver detalle de la simulación"):
                st.metric("Media de 5.000 simulaciones", fmt_num(sim.get('r2_diferencia_media', 0), 4))
                st.metric("Desviación estándar", fmt_num(sim.get('r2_diferencia_std', 0), 4))
                rango = sim.get('rango_central_95', [0, 0])
                st.metric("Rango central (2.5%-97.5%)", f"[{fmt_num(rango[0], 4)}, {fmt_num(rango[1], 4)}]")
                st.metric("Resultado real observado (426 filas)", fmt_num(sim.get('diferencia_real_observada_426', 0), 4))
            st.markdown("**La diferencia observada es poco habitual.**")
            st.caption(
                f"La muestra original cae en el percentil {fmt_num(sim.get('percentil_del_resultado_real', 0), 1)} "
                "de las 5.000 submuestras. La variabilidad de los casos seleccionados podría explicar parte del "
                "resultado, aunque no demuestra su causa."
            )

    with sub2:
        st.markdown("**B · Incertidumbre de la muestra fija (bootstrap)**")
        st.caption("¿Cuánta incertidumbre tiene la diferencia de nuestra muestra?")
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
            with st.expander("Ver intervalos por comparación"):
                for c in comparaciones:
                    incluye = "incluye el 0 (no concluyente)" if c["incluye_cero"] else "NO incluye el 0 (distinguible de cero)"
                    st.markdown(f"- **{c['nombre']}**: diferencia media {fmt_num(c['diferencia_media'], 4)}, IC95% "
                                f"[{fmt_num(c['ic_95'][0], 4)}, {fmt_num(c['ic_95'][1], 4)}] — {incluye}")
            st.markdown("**La mejora conjunta se distingue de cero; sus causas parciales, no concluyentes.**")
            st.caption(
                "B supera a A, pero no podemos determinar con precisión cuánto aporta excluir los ceros y "
                "cuánto la construcción de variables. Que un intervalo incluya el 0 no demuestra que el efecto "
                "sea nulo -- solo que, con esta muestra, no se puede distinguir de cero. El límite superior del "
                "intervalo A-B (-0,0043) está cerca de cero: evidencia real, no una certeza absoluta."
            )

    st.markdown("---")
    st.markdown("## Conclusión de esta sección")
    concl = modelo.get("conclusion_final", {})
    st.success(f"**Lo observado:** {concl.get('observado', '')}")
    st.warning(f"**Interpretación razonable:** {concl.get('interpretacion_razonable', '')}")
    st.info(f"**Lo que sigue sin resolver:** {concl.get('sin_resolver', '')}")
