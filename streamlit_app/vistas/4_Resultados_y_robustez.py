import pandas as pd
import streamlit as st

from src.data_loader import cargar_modelo, cargar_simulacion_valores
from src.styles import kicker, caja_alerta, fmt_num, AMBAR_ALERTA, OCRE_DORADO_TEXTO, TURQUESA, AZUL_PETROLEO, COLOR_CRUDO, COLOR_D, COLOR_TRATADO, COLOR_SENSIBILIDAD, COLOR_NEUTRO, AMBAR_PENDIENTE
from src.charts import dispersion_muestra_simulada, intervalo_confianza, r2_muestra_comun, importancia_variables, comparacion_sensibilidad

modelo = cargar_modelo()
simulacion_real = cargar_simulacion_valores()


def _barra_eur(etiqueta, valor, valor_max, color, negrita=False):
    pct = min(100, (valor / valor_max) * 100) if valor_max else 0
    peso = "700" if negrita else "600"
    st.markdown(
        f'<div style="margin-bottom:0.65rem;">'
        f'<div style="display:flex; justify-content:space-between; align-items:baseline; margin-bottom:0.2rem;">'
        f'<span style="font-size:0.95rem; font-weight:{peso}; color:#31333F;">{etiqueta}</span>'
        f'<span style="font-size:0.95rem; font-weight:700; color:#31333F;">{fmt_num(valor, 1)} €</span>'
        f'</div>'
        f'<div style="background-color:#eceff1; border-radius:6px; height:10px; width:100%;">'
        f'<div style="background-color:{color}; border-radius:6px; height:10px; width:{pct:.1f}%;"></div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

kicker("Página 7 de 9")
st.title("Resultados, robustez e interpretación")
st.markdown(
    "Esta es la página central del proyecto. Los R² de la página anterior invitan a sacar una "
    "conclusión rápida -- pero **se evalúan sobre poblaciones distintas**, y comparar así puede "
    "engañar. Antes de confiar en cualquier diferencia entre modelos, se investigó si la comparación "
    "en sí misma era confiable. No lo era: se encontró un problema real."
)

st.markdown("---")
tab_resultados, tab_confianza = st.tabs(["📊 Resultados", "🔍 Confianza y conclusión"])

with tab_resultados:
    st.markdown("## 1. La fuga de datos detectada y corregida")
    fuga = modelo.get("fuga_de_datos_detectada_y_corregida", {})
    n_comun_426 = modelo.get("muestra_comun_426", {}).get("n", 0)
    st.markdown(
        f'<div style="background-color: #fff; border: 1px solid #e0e0e0; border-left: 4px solid {AMBAR_ALERTA}; border-radius: 8px; padding: 1rem 1.2rem; margin: 1rem 0;">'
        f'<div style="font-size: 0.95rem; font-weight: 700; color: #31333F; margin-bottom: 0.5rem;">Una evaluación inicial pareció demasiado buena: comparar A y D contra el test de B dio R² ≈ 0,82</div>'
        f'<div style="font-size: 0.85rem; color: #555; margin-bottom: 0.9rem; line-height: 1.4;">'
        f'Como A, D y B no son comparables cada uno en su propia población, se intentó dar a los tres el mismo '
        f'examen: usar las 2.134 filas de test de B como terreno común, y evaluar ahí también a A y D. '
        f'Pero A/D y B parten de poblaciones base distintas (13.355 vs. 10.669 filas), con particiones 80/20 '
        f'hechas cada una por su cuenta -- nada garantizaba que esas filas de test de B no fueran ya filas de '
        f'entrenamiento de A o D. Y lo eran: por eso salió una fuga.</div>'
        f'<div style="display: flex; flex-wrap: wrap; gap: 2rem; margin-bottom: 0.8rem;">'
        f'<div><div style="font-size:2rem; font-weight:800; color:{OCRE_DORADO_TEXTO};">{fmt_num(fuga.get("pct_filas_contaminadas", 0), 0)}%</div>'
        f'<div style="font-size:0.78rem; color:#666; max-width:220px;">Solapamiento -- filas del test de B que ya estaban en el entrenamiento de A/D '
        f'({fmt_num(fuga.get("n_contaminadas", 0))} de {fmt_num(fuga.get("n_test_B_total", 0))})</div></div>'
        f'<div><div style="font-size:2rem; font-weight:800; color:{TURQUESA};">{fmt_num(n_comun_426)}</div>'
        f'<div style="font-size:0.78rem; color:#666; max-width:260px;">Filas limpias -- las 2.134 de B, menos las 1.708 contaminadas: la única base sin fuga para comparar (sección 3)</div></div>'
        f'</div>'
        f'<div style="font-size:0.85rem; color:#555; border-top:1px solid #eee; padding-top:0.6rem;">'
        f'Evaluar con datos ya vistos infla el resultado artificialmente -- se corrigió antes de reportar nada. '
        f'{fuga.get("correccion", "")}</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("## 2. ¿De dónde viene realmente la diferencia entre A y B?")
    st.caption(
        "Esta comprobación es independiente de la sección 1 -- no usa las 426 filas seguras, porque aquí "
        "nunca se evalúa un modelo con filas de otro (solo A y D, cada uno sobre un subconjunto de su "
        "propio test). Es otra forma, en paralelo, de investigar el mismo origen de la diferencia A-B."
    )
    pob = modelo.get("poblacion_limpia_experimento", {})
    st.caption(pob.get("nota", ""))
    r2_d_toda_poblacion = modelo.get("versiones", {}).get("D_variables_tratadas_poblacion_cruda", {}).get("r2", 0)
    if pob:
        st.plotly_chart(
            r2_muestra_comun(
                ["A · toda su población", "D · toda su población", "A · población limpia", "D · población limpia", "B · población limpia"],
                [pob["A_toda_poblacion"]["r2"], r2_d_toda_poblacion, pob["A_solo_poblacion_limpia"]["r2"], pob["D_solo_poblacion_limpia"]["r2"], pob["B_propia_poblacion_limpia"]["r2"]],
                [AMBAR_PENDIENTE, COLOR_D, COLOR_CRUDO, COLOR_NEUTRO, COLOR_TRATADO],
                titulo="R² de A y D al cambiar solo la población evaluada",
            ),
            width="stretch",
        )
        aislar = modelo.get("aislar_variables_vs_poblacion", {})
        r2_var = aislar.get("A_vs_D_r2_diferencia", 0)
        rango_pob = aislar.get("cambio_poblacion_r2_diferencia_rango", [0, 0])
        st.markdown(
            f'<div style="background-color: #f8f9fa; border: 1px solid #e0e0e0; border-left: 4px solid {COLOR_NEUTRO}; border-radius: 8px; padding: 0.9rem 1.1rem; margin: 0.8rem 0;">'
            f'<div style="font-size: 0.95rem; font-weight: 700; color: #31333F; margin-bottom: 0.5rem;">Mismo modelo, mismas variables -- solo cambia la población evaluada</div>'
            f'<div style="font-size: 0.85rem; color: #555; margin-bottom: 0.4rem;">'
            f'A: {fmt_num(pob["A_toda_poblacion"]["r2"], 3)} (toda su población) − {fmt_num(pob["A_solo_poblacion_limpia"]["r2"], 3)} (población limpia) = <b>{fmt_num(rango_pob[0], 3)}</b><br>'
            f'D: {fmt_num(r2_d_toda_poblacion, 3)} (toda su población) − {fmt_num(pob["D_solo_poblacion_limpia"]["r2"], 3)} (población limpia) = <b>{fmt_num(rango_pob[1], 3)}</b>'
            f'</div>'
            f'<div style="font-size: 0.85rem; color: #555;">Son los mismos modelos, sin reentrenar -- cambia únicamente qué filas se usan para evaluarlos. '
            f'No hace falta tocar ni una variable para mover el resultado tanto.</div>'
            f'<div style="font-size: 0.78rem; color: #888; border-top: 1px solid #eee; margin-top: 0.5rem; padding-top: 0.4rem;">'
            f'Confirma lo visto en "Comparación de modelos": cambiar solo las variables (A vs. D, cada uno en su propia '
            f'población) apenas movía el R² (<b>{fmt_num(r2_var, 3)}</b>) -- 6-7 veces menos que el efecto de la población.</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        with st.expander("Ver MAE y n de cada evaluación"):
            d_toda_poblacion = modelo.get("versiones", {}).get("D_variables_tratadas_poblacion_cruda", {})
            df_pob = pd.DataFrame([
                {"Evaluación": "A, sobre toda su población", "n test": fmt_num(pob["A_toda_poblacion"]["n_test"]), "MAE (€)": fmt_num(pob["A_toda_poblacion"]["mae"], 1), "R²": fmt_num(pob["A_toda_poblacion"]["r2"], 3)},
                {"Evaluación": "A, solo sobre población limpia", "n test": fmt_num(pob["A_solo_poblacion_limpia"]["n_test"]), "MAE (€)": fmt_num(pob["A_solo_poblacion_limpia"]["mae"], 1), "R²": fmt_num(pob["A_solo_poblacion_limpia"]["r2"], 3)},
                {"Evaluación": "D, sobre toda su población", "n test": fmt_num(d_toda_poblacion.get("n_test_propio", 0)), "MAE (€)": fmt_num(d_toda_poblacion.get("mae", 0), 1), "R²": fmt_num(d_toda_poblacion.get("r2", 0), 3)},
                {"Evaluación": "D, solo sobre población limpia", "n test": fmt_num(pob["D_solo_poblacion_limpia"]["n_test"]), "MAE (€)": fmt_num(pob["D_solo_poblacion_limpia"]["mae"], 1), "R²": fmt_num(pob["D_solo_poblacion_limpia"]["r2"], 3)},
                {"Evaluación": "B, su propia población limpia", "n test": fmt_num(pob["B_propia_poblacion_limpia"]["n_test"]), "MAE (€)": fmt_num(pob["B_propia_poblacion_limpia"]["mae"], 1), "R²": fmt_num(pob["B_propia_poblacion_limpia"]["r2"], 3)},
            ])
            st.dataframe(df_pob, width="stretch", hide_index=True)
        st.caption(pob.get("conclusion", ""))

    st.markdown("---")
    st.markdown("## 3. Comparación sobre la muestra común segura (426 filas)")
    st.markdown(
        "**Por qué se hace esta comparación:** con la fuga ya corregida (sección 1), esta es la "
        "respuesta final y de fiar a la pregunta que abre toda la página -- ¿cuál de los tres modelos "
        "predice mejor de verdad? A diferencia del punto 2, donde cada modelo se evaluaba sobre **su "
        "propia población** (filtrada de forma parecida, pero no las mismas filas), aquí los tres se "
        "evalúan sobre **exactamente las mismas 426 filas** -- por eso hace falta reducir la muestra a "
        "ese tamaño: es lo único que cumple esa condición para los tres modelos a la vez, y ninguno la "
        "vio durante su entrenamiento."
    )
    st.caption(
        "Solo aparecen A, D y B -- el Chequeo de sensibilidad responde una pregunta distinta (si el "
        "criterio de imputación importa), nunca se diseñó una comparación sin fuga para él."
    )
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
            st.markdown("**4 · Chequeo de sensibilidad**")
            st.caption("¿Cambia la conclusión si imputo por barrio en vez de por capacidad?")
            versiones = modelo.get("versiones", {})
            b = versiones.get("B_tratado_criterio_A", {})
            sens = versiones.get("TRATADO_criterio_B_barrio", {})
            diff = sens.get("diferencia_vs_A", {})
            if b and sens:
                st.plotly_chart(
                    comparacion_sensibilidad(
                        b.get("mae", 0), sens.get("mae", 0), b.get("r2", 0), sens.get("r2", 0),
                        COLOR_TRATADO, COLOR_SENSIBILIDAD,
                        titulo="B vs. Chequeo de sensibilidad",
                    ),
                    width="stretch",
                )
            if diff:
                st.caption(f"Diferencia: MAE {fmt_num(diff.get('mae_eur', 0), 1)} € ({fmt_num(diff.get('mae_pct', 0), 2)}% relativo) · R² {fmt_num(diff.get('r2', 0), 3)} -- la conclusión del modelo no depende de cuál de los dos criterios razonables se use.")

    with sec6:
        with st.container(border=True):
            st.markdown("**5 · Importancia de variables**")
            st.caption("Cuánto ayuda cada variable a reducir el error de predicción cada vez que se usa para dividir los datos.")
            imp = modelo.get("importancia_variables", {})
            valores_imp = imp.get("valores", [])
            if valores_imp:
                df_imp = pd.DataFrame(valores_imp).set_index("variable")
                st.plotly_chart(
                    importancia_variables(
                        df_imp,
                        [("crudo", "A (crudo)", COLOR_CRUDO), ("tratado_a", "B (tratado)", COLOR_TRATADO)],
                        titulo="Importancia de variables -- A vs. B",
                    ),
                    width="stretch",
                )
            st.caption("Las mismas 8 variables dominan en las tres versiones -- ninguna variable geográfica específica entra en el top 8 (ni `room_type`, ni `property_type`, ni `neighbourhood_cleansed`).")
            st.caption(f"⚠️ {imp.get('caveat', '')}")
            if valores_imp:
                with st.expander("Ver tabla: importancia de cada variable en A, B y el Chequeo de sensibilidad"):
                    st.dataframe(
                        df_imp.rename(columns={"crudo": "A (crudo)", "tratado_a": "B (tratado)", "tratado_b": "Sensibilidad"}),
                        width="stretch",
                    )

    st.markdown("---")
    st.markdown("### 6 · Un modelo puede ganar globalmente y no en cada predicción")
    ejemplo = modelo.get("ejemplo_prediccion_individual", {})
    if ejemplo:
        st.caption("B es el mejor modelo en la evaluación global. ¿Ocurre lo mismo cuando examinamos un anuncio concreto?")
        preds = ejemplo.get("predicciones", [])
        COLOR_REAL = "#3A3A3A"

        with st.container(border=True):
            st.markdown("**01 — Selección del anuncio**")
            col_med, col_ref = st.columns(2)
            with col_med:
                st.caption(f"Mediana de las {fmt_num(ejemplo.get('n_poblacion', 0))} filas")
                st.markdown(f"<span style='font-size:1.6rem; font-weight:700; color:{AZUL_PETROLEO};'>{fmt_num(ejemplo.get('mediana_poblacion_eur', 0), 1)} €</span>", unsafe_allow_html=True)
            with col_ref:
                st.caption("Valor de referencia")
                st.markdown(f"<span style='font-size:1.6rem; font-weight:700; color:#31333F;'>{fmt_num(ejemplo.get('valor_real_eur', 0), 1)} €</span>", unsafe_allow_html=True)
                st.caption(f"ID {ejemplo.get('id_anuncio', '')}")
            st.markdown("---")
            st.markdown(f"Distancia a la mediana &nbsp;&nbsp; **{fmt_num(ejemplo.get('distancia_a_mediana_eur', 0), 1)} €**")
            st.caption(
                f"Se seleccionó el anuncio más próximo a la mediana. Existe otro registro empatado "
                f"(ID {ejemplo.get('empate_id', '')}), también a {fmt_num(ejemplo.get('distancia_a_mediana_eur', 0), 1)} €. "
                f"Se conserva el primero según el criterio determinista del notebook."
            )

        st.markdown("")
        with st.container(border=True):
            st.markdown("**02 — ¿Qué predice cada modelo?**")
            st.caption(f"Importes en euros · valor de referencia: {fmt_num(ejemplo.get('valor_real_eur', 0), 1)} €")
            preds_por_valor = sorted(preds, key=lambda p: p["prediccion_eur"])
            valor_max = max([ejemplo.get("valor_real_eur", 0)] + [p["prediccion_eur"] for p in preds_por_valor])
            _barra_eur("Valor de referencia", ejemplo.get("valor_real_eur", 0), valor_max, COLOR_REAL, negrita=True)
            for p in preds_por_valor:
                _barra_eur(p["nombre_display"], p["prediccion_eur"], valor_max, AZUL_PETROLEO)
            st.caption("Representación ilustrativa de las predicciones y del valor de referencia. Escala común desde cero.")

        st.markdown("")
        with st.container(border=True):
            st.markdown("**03 — ¿Cuál se equivoca menos?**")
            preds_por_error = sorted(preds, key=lambda p: p["error_abs_eur"])
            df_errores = pd.DataFrame([
                {"Modelo": p["nombre_display"], "Error absoluto": f"{fmt_num(p['error_abs_eur'], 1)} €"}
                for p in preds_por_error
            ])
            st.dataframe(df_errores, width="stretch", hide_index=True)
            ganador = preds_por_error[0]
            st.markdown("**Menor error individual**")
            st.markdown(f"<span style='font-size:1.6rem; font-weight:700; color:{AZUL_PETROLEO};'>{fmt_num(ganador['error_abs_eur'], 1)} €</span>", unsafe_allow_html=True)
            st.caption(f"Error absoluto en el anuncio {ejemplo.get('id_anuncio', '')} (modelo {ganador['nombre_display']})")

        st.markdown("")
        with st.container(border=True):
            st.markdown("**El mensaje final que debe quedar en pantalla**")
            col_g, col_i = st.columns(2)
            with col_g:
                st.caption(f"Evaluación global · {fmt_num(ejemplo.get('n_poblacion', 0))} filas")
                st.markdown(f"<span style='font-size:1.8rem; font-weight:800; color:{COLOR_TRATADO};'>B</span>", unsafe_allow_html=True)
                st.caption(f"R² = {fmt_num(resultados_426.get('B_tratado_criterio_A', {}).get('r2', 0), 3)}")
                st.caption("Mejor rendimiento global")
            with col_i:
                st.caption("Ejemplo individual · 1 anuncio")
                st.markdown(f"<span style='font-size:1.8rem; font-weight:800; color:{COLOR_D};'>D</span>", unsafe_allow_html=True)
                st.caption(f"Error = {fmt_num(ganador['error_abs_eur'], 1)} €")
                st.caption("Menor error en este caso")
            st.markdown("---")
            st.markdown("**El mejor modelo global no tiene por qué ser el más preciso en cada predicción individual.**")
            st.caption(ejemplo.get("nota_metodologica", ""))
        st.caption(f"ℹ️ {ejemplo.get('nota_c', '')}")

with tab_confianza:
    st.markdown("## ¿Cuánta confianza hay en estos resultados?")
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
                f"Solo el {fmt_num(sim.get('percentil_del_resultado_real', 0), 1)}% de las 5.000 submuestras "
                "simuladas (cada una, otros 426 anuncios elegidos al azar del mismo universo) dieron un "
                "resultado tan extremo como el real, o más. Con solo 426 filas, no se puede afirmar con "
                "seguridad que si se hubieran elegido otros 426 anuncios distintos, el resultado se "
                "mantuviera igual -- de hecho, el histograma muestra que la mayoría de esas otras "
                "elecciones posibles habrían dado un resultado muy distinto (más cercano a cero, o incluso "
                "a favor de A). Por eso esta comparación concreta, por sí sola, no es una base sólida para "
                "afirmar que D gana a A -- el hallazgo fiable es el de la muestra grande (sección 2)."
            )

    with sub2:
        st.markdown("**B · Incertidumbre de la muestra fija (bootstrap)**")
        st.caption("¿Cuánta incertidumbre tiene la diferencia de nuestra muestra?")
        st.markdown(
            f"**Qué se hizo**: igual que en el panel A, se repite el cálculo **5.000 veces** -- pero con un "
            f"método distinto. Aquí no se buscan otras filas del universo: se vuelve a muestrear **de "
            f"las mismas 426 filas, con reemplazo** (un mismo anuncio puede salir repetido varias veces "
            f"en una ronda, o ninguna). En cada una de las 5.000 repeticiones se remuestrea una sola vez "
            f"y se aplica igual a A, D y B -- los tres se evalúan sobre las mismas filas remuestreadas en "
            f"cada ronda, para que la comparación entre ellos sea consistente ronda a ronda."
        )
        st.caption(
            "**Para qué sirve**: mide cuánto se movería el resultado si tuvieras mala suerte (o buena) con "
            "qué filas concretas te tocaron dentro de esta muestra fija de 426 -- no cambia de muestra, "
            "mide la fiabilidad de la que ya tienes."
        )
        if comparaciones:
            etiquetas_cortas = {
                "A - B (efecto combinado, hallazgo principal)": "A vs. B -- población + variables juntas",
                "A - D (solo variables, 426 filas)": "A vs. D -- solo cambian las variables",
                "D - B (solo población, variables ya igualadas)": "D vs. B -- solo cambia la población",
            }
            st.plotly_chart(
                intervalo_confianza(
                    [etiquetas_cortas.get(c["nombre"], c["nombre"]) for c in comparaciones],
                    [c["diferencia_media"] for c in comparaciones],
                    [c["ic_95"][0] for c in comparaciones],
                    [c["ic_95"][1] for c in comparaciones],
                ),
                width="stretch",
            )
            st.caption(
                "**Cómo leerlo**: si la barra toca o cruza la línea de puntos (el cero), esa diferencia "
                "no se puede distinguir del azar con esta muestra. Solo la barra de abajo (A vs. B) no la toca."
            )
            st.success(
                "**B predice mejor que A, y esa diferencia SÍ es estadísticamente real** (el intervalo de "
                "confianza de A-B no incluye el cero)."
            )
            with st.expander("Ver intervalos por comparación"):
                veredictos = {
                    "A - B (efecto combinado, hallazgo principal)": "**Resultado: B predice mejor que A** -- diferencia real, confirmada.",
                    "A - D (solo variables, 426 filas)": "**Resultado: no concluyente** -- con esta muestra, no se puede afirmar si D es mejor o peor que A.",
                    "D - B (solo población, variables ya igualadas)": "**Resultado: no concluyente** -- con esta muestra, no se puede afirmar si B es mejor o peor que D.",
                }
                for c in comparaciones:
                    incluye = "incluye el 0 (no concluyente)" if c["incluye_cero"] else "NO incluye el 0 (distinguible de cero)"
                    st.markdown(f"- **{c['nombre']}**: diferencia media {fmt_num(c['diferencia_media'], 4)}, IC95% "
                                f"[{fmt_num(c['ic_95'][0], 4)}, {fmt_num(c['ic_95'][1], 4)}] — {incluye}. "
                                f"{veredictos.get(c['nombre'], '')}")
            st.caption(
                "Lo único que no se puede repartir con precisión es **cuánto** de esa mejora viene de excluir "
                "los ceros artificiales (población) y cuánto de construir mejor las variables -- esas dos "
                "piezas, vistas por separado (A-D y D-B), sí incluyen el cero en esta muestra de 426 filas. "
                "Que un intervalo incluya el 0 no demuestra que el efecto sea nulo, solo que con esta muestra "
                "no se puede distinguir del azar."
            )

    st.markdown("---")
    st.markdown("## Conclusión de esta sección")
    concl = modelo.get("conclusion_final", {})
    st.success(f"**Lo observado:** {concl.get('observado', '')}")
    st.warning(f"**Interpretación razonable:** {concl.get('interpretacion_razonable', '')}")
    st.info(f"**Lo que sigue sin resolver:** {concl.get('sin_resolver', '')}")
