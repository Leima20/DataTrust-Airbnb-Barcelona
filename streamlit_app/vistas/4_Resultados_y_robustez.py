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

st.markdown("---")
tab_resultados, tab_confianza = st.tabs(["📊 Resultados", "🔍 Confianza y conclusión"])

with tab_resultados:
    st.markdown("### ¿Qué se intentó comparar?")
    st.markdown(
        f"""
        <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem 1.1rem;">
          <svg width="100%" height="460" viewBox="0 0 1150 460" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <marker id="flecha_cm" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
                <path d="M0,0 L10,5 L0,10 z" fill="#aaa" />
              </marker>
            </defs>
            <text x="110" y="20" text-anchor="middle" fill="#888" font-size="11" font-weight="600" letter-spacing="0.5" font-family="Helvetica">1. PUNTO DE PARTIDA</text>
            <text x="560" y="20" text-anchor="middle" fill="#888" font-size="11" font-weight="600" letter-spacing="0.5" font-family="Helvetica">2. AÍSLA UN FACTOR A LA VEZ</text>
            <text x="990" y="20" text-anchor="middle" fill="#888" font-size="11" font-weight="600" letter-spacing="0.5" font-family="Helvetica">3. COMPARACIÓN CONTROLADA</text>
            <rect x="20" y="170" width="180" height="110" rx="10" fill="{COLOR_CRUDO}" />
            <text x="110" y="220" text-anchor="middle" fill="white" font-size="14" font-weight="700" font-family="Helvetica">A -- CRUDO</text>
            <text x="110" y="238" text-anchor="middle" fill="white" font-size="11" font-family="Helvetica" opacity="0.9">n = 13.355</text>
            <text x="110" y="256" text-anchor="middle" fill="white" font-size="10" font-family="Helvetica" opacity="0.8">punto de partida</text>
            <line x1="200" y1="195" x2="430" y2="85" stroke="#aaa" stroke-width="2" marker-end="url(#flecha_cm)" />
            <line x1="200" y1="225" x2="430" y2="225" stroke="#aaa" stroke-width="2" marker-end="url(#flecha_cm)" />
            <rect x="430" y="35" width="260" height="100" rx="10" fill="{COLOR_D}" />
            <text x="560" y="60" text-anchor="middle" fill="white" font-size="14" font-weight="700" font-family="Helvetica">D</text>
            <text x="560" y="78" text-anchor="middle" fill="white" font-size="11" font-family="Helvetica">¿Influye el tratamiento de variables?</text>
            <text x="560" y="96" text-anchor="middle" fill="white" font-size="10" font-family="Helvetica" opacity="0.85">misma población -- n = 13.355</text>
            <rect x="430" y="175" width="260" height="100" rx="10" fill="{COLOR_TRATADO}" />
            <text x="560" y="200" text-anchor="middle" fill="white" font-size="14" font-weight="700" font-family="Helvetica">B -- TRATADO-A</text>
            <text x="560" y="218" text-anchor="middle" fill="white" font-size="11" font-family="Helvetica">¿Qué ocurre al depurar los datos?</text>
            <text x="560" y="236" text-anchor="middle" fill="white" font-size="10" font-family="Helvetica" opacity="0.85">variables y población -- n = 10.669</text>
            <line x1="560" y1="275" x2="560" y2="315" stroke="#bbb" stroke-width="1.5" stroke-dasharray="3,3" />
            <text x="590" y="298" text-anchor="start" fill="#999" font-size="9" font-family="Helvetica">variante</text>
            <rect x="430" y="315" width="260" height="110" rx="10" fill="{COLOR_SENSIBILIDAD}" />
            <text x="560" y="340" text-anchor="middle" fill="white" font-size="14" font-weight="700" font-family="Helvetica">Chequeo de sensibilidad</text>
            <text x="560" y="358" text-anchor="middle" fill="white" font-size="11" font-family="Helvetica">¿Depende del criterio de imputación?</text>
            <text x="560" y="376" text-anchor="middle" fill="white" font-size="10" font-family="Helvetica" opacity="0.85">mismas filas que B, otro criterio</text>
            <text x="560" y="392" text-anchor="middle" fill="white" font-size="9" font-family="Helvetica" opacity="0.75">fuera de la muestra de 426</text>
            <line x1="690" y1="85" x2="870" y2="205" stroke="#ccc" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#flecha_cm)" />
            <line x1="690" y1="225" x2="870" y2="225" stroke="#ccc" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#flecha_cm)" />
            <rect x="870" y="170" width="240" height="110" rx="10" fill="#FBEED6" stroke="{AMBAR_PENDIENTE}" stroke-width="2" />
            <text x="990" y="220" text-anchor="middle" fill="{OCRE_DORADO_TEXTO}" font-size="14" font-weight="700" font-family="Helvetica">Muestra común</text>
            <text x="990" y="238" text-anchor="middle" fill="{OCRE_DORADO_TEXTO}" font-size="11" font-family="Helvetica">¿Qué ocurre en igualdad de condiciones?</text>
            <text x="990" y="256" text-anchor="middle" fill="#806000" font-size="10" font-family="Helvetica" opacity="0.85">n = 426 -- comparación controlada</text>
          </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("## 1. Se detectó un solapamiento que invalidaba la comparación inicial")
    st.markdown(
        "Para comparar A, D y B en igualdad de condiciones, se intentó evaluar a los tres sobre las mismas "
        "filas: las 2.134 del test de B."
    )
    fuga = modelo.get("fuga_de_datos_detectada_y_corregida", {})
    n_comun_426 = modelo.get("muestra_comun_426", {}).get("n", 0)
    n_contaminadas = fuga.get("n_contaminadas", 0)
    n_test_b_total = fuga.get("n_test_B_total", 0)
    pct_contam = fuga.get("pct_filas_contaminadas", 0)
    pct_seguro = 100 - pct_contam
    ancho_total = 760
    ancho_contam = ancho_total * (pct_contam / 100)
    ancho_seguro = ancho_total - ancho_contam
    cx_contam = 70 + ancho_contam / 2
    cx_seguro = 70 + ancho_contam + ancho_seguro / 2

    st.markdown(
        f"""
        <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.2rem 1.4rem;">
          <svg width="100%" height="340" viewBox="0 0 900 280" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <marker id="flecha_fuga" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
                <path d="M0,0 L10,5 L0,10 z" fill="#aaa" />
              </marker>
            </defs>
            <text x="450" y="25" text-anchor="middle" fill="#444" font-size="15" font-weight="700" font-family="Helvetica">Test del modelo B -- {fmt_num(n_test_b_total)} filas</text>
            <rect x="70" y="40" width="{ancho_contam:.0f}" height="70" fill="{AMBAR_ALERTA}" />
            <rect x="{70 + ancho_contam:.0f}" y="40" width="{ancho_seguro:.0f}" height="70" fill="{TURQUESA}" />
            <text x="{cx_contam:.0f}" y="85" text-anchor="middle" fill="white" font-size="24" font-weight="800" font-family="Helvetica">{fmt_num(pct_contam, 0)}%</text>
            <text x="{cx_seguro:.0f}" y="85" text-anchor="middle" fill="white" font-size="24" font-weight="800" font-family="Helvetica">{fmt_num(pct_seguro, 0)}%</text>
            <text x="{cx_contam:.0f}" y="130" text-anchor="middle" fill="#666" font-size="12" font-family="Helvetica">{fmt_num(n_contaminadas)} filas -- ya vistas por A/D en su entrenamiento</text>
            <text x="{cx_seguro:.0f}" y="130" text-anchor="middle" fill="#666" font-size="12" font-family="Helvetica">{fmt_num(n_comun_426)} filas</text>
            <line x1="{cx_seguro:.0f}" y1="150" x2="{cx_seguro:.0f}" y2="195" stroke="#aaa" stroke-width="2" marker-end="url(#flecha_fuga)" />
            <rect x="{cx_seguro - 170:.0f}" y="200" width="340" height="65" rx="10" fill="#FBEED6" stroke="{AMBAR_PENDIENTE}" stroke-width="2" />
            <text x="{cx_seguro:.0f}" y="228" text-anchor="middle" fill="{OCRE_DORADO_TEXTO}" font-size="16" font-weight="700" font-family="Helvetica">{fmt_num(n_comun_426)} -- Muestra común segura</text>
            <text x="{cx_seguro:.0f}" y="248" text-anchor="middle" fill="#806000" font-size="11" font-family="Helvetica">fuera del entrenamiento de los tres modelos</text>
          </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("Ver explicación completa"):
        st.markdown(
            "Una evaluación inicial pareció demasiado buena: comparar A y D directamente contra el test de B "
            "dio R² ≈ 0,82. Como A, D y B no son comparables cada uno en su propia población, se intentó dar "
            "a los tres el mismo examen: usar las 2.134 filas de test de B como terreno común, y evaluar ahí "
            "también a A y D. Pero A/D y B parten de poblaciones base distintas (13.355 vs. 10.669 filas), "
            "con particiones 80/20 hechas cada una por su cuenta -- nada garantizaba que esas filas de test "
            "de B no fueran ya filas de entrenamiento de A o D. Y lo eran: por eso salió un solapamiento. "
            "Evaluar con datos ya vistos infla el resultado artificialmente -- se corrigió antes de reportar "
            f"nada. {fuga.get('correccion', '')}"
        )

    st.markdown("---")
    st.markdown("## 2. Comparación sobre la muestra común segura (426 filas)")
    muestra = modelo.get("muestra_comun_426", {})
    resultados_426 = muestra.get("resultados", {})
    if resultados_426:
        st.plotly_chart(
            r2_muestra_comun(
                ["A · Crudo", "D · Variables tratadas", "B · Tratado"],
                [resultados_426["A_crudo"]["r2"], resultados_426["D_variables_tratadas_poblacion_cruda"]["r2"], resultados_426["B_tratado_criterio_A"]["r2"]],
                [COLOR_CRUDO, COLOR_NEUTRO, COLOR_TRATADO],
                height=360,
            ),
            width="stretch",
        )

        r2_a_426 = resultados_426["A_crudo"]["r2"]
        r2_d_426 = resultados_426["D_variables_tratadas_poblacion_cruda"]["r2"]
        r2_b_426 = resultados_426["B_tratado_criterio_A"]["r2"]
        diferencia_ab_426 = r2_b_426 - r2_a_426
        st.markdown(
            f"""
            <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.2rem 1.4rem; margin: 1rem 0;">
              <div style="display: flex; align-items: center; justify-content: center; gap: 1.2rem; flex-wrap: wrap;">
                <div style="text-align: center;">
                  <div style="width: 72px; height: 72px; border-radius: 50%; background-color: {COLOR_CRUDO}; color: white; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.3rem; margin: 0 auto;">A</div>
                  <div style="font-size: 1.15rem; font-weight: 800; margin-top: 0.4rem; color: #31333F;">{fmt_num(r2_a_426, 3)}</div>
                  <div style="font-size: 0.78rem; color: #666;">datos crudos</div>
                </div>
                <div style="font-size: 1.6rem; color: #aaa;">&rarr;</div>
                <div style="text-align: center;">
                  <div style="width: 72px; height: 72px; border-radius: 50%; background-color: {COLOR_D}; color: white; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.3rem; margin: 0 auto;">D</div>
                  <div style="font-size: 1.15rem; font-weight: 800; margin-top: 0.4rem; color: #31333F;">{fmt_num(r2_d_426, 3)}</div>
                  <div style="font-size: 0.78rem; color: #666;">variables tratadas</div>
                </div>
                <div style="font-size: 1.6rem; color: #aaa;">&rarr;</div>
                <div style="text-align: center;">
                  <div style="width: 72px; height: 72px; border-radius: 50%; background-color: {COLOR_TRATADO}; color: white; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.3rem; margin: 0 auto;">B</div>
                  <div style="font-size: 1.15rem; font-weight: 800; margin-top: 0.4rem; color: #31333F;">{fmt_num(r2_b_426, 3)}</div>
                  <div style="font-size: 0.78rem; color: #666;">variables tratadas y<br>población depurada</div>
                </div>
              </div>
              <div style="text-align: center; margin-top: 1rem;">
                <span style="background-color: {AMBAR_PENDIENTE}1A; color: {AMBAR_PENDIENTE}; padding: 0.35rem 0.9rem; border-radius: 6px; font-size: 0.95rem; font-weight: 700;">
                  +{fmt_num(diferencia_ab_426, 3)} -- diferencia de R² entre A y B en la muestra común
                </span>
              </div>
              <div style="font-size: 0.78rem; color: #888; border-top: 1px solid #eaeaeb; margin-top: 1rem; padding-top: 0.6rem; text-align: center;">
                Tres modelos entrenados con sus respectivas versiones de datos, evaluados sobre los mismos 426 casos --
                la secuencia no demuestra cuánto aporta cada decisión por separado.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander("Ver por qué esta es la comparación controlada, y métricas detalladas"):
            st.markdown(
                "Con la fuga ya corregida (sección 1), esta es la respuesta final y de fiar a la pregunta "
                "que abre toda la página -- ¿cuál de los tres modelos predice mejor de verdad? Aquí los "
                "tres se evalúan sobre exactamente las mismas 426 filas -- por eso hace falta reducir la "
                "muestra a ese tamaño: es lo único que cumple esa condición para los tres modelos a la vez, "
                "y ninguno la vio durante su entrenamiento. La sección 3 profundiza en *por qué* B gana, "
                "usando una muestra más grande."
            )
            st.markdown(muestra.get("representatividad", ""))
            st.caption(muestra.get("progresion", ""))
            df = pd.DataFrame([
                {"Modelo": "A (CRUDO)", "MAE (€)": fmt_num(resultados_426["A_crudo"]["mae"], 1), "R²": fmt_num(resultados_426["A_crudo"]["r2"], 3)},
                {"Modelo": "D (variables tratadas)", "MAE (€)": fmt_num(resultados_426["D_variables_tratadas_poblacion_cruda"]["mae"], 1), "R²": fmt_num(resultados_426["D_variables_tratadas_poblacion_cruda"]["r2"], 3)},
                {"Modelo": "B (TRATADO-A)", "MAE (€)": fmt_num(resultados_426["B_tratado_criterio_A"]["mae"], 1), "R²": fmt_num(resultados_426["B_tratado_criterio_A"]["r2"], 3)},
            ])
            st.dataframe(df, width="stretch", hide_index=True)

    st.markdown("---")
    st.markdown("## 3. ¿De dónde viene la diferencia entre A y B?")
    pob = modelo.get("poblacion_limpia_experimento", {})
    r2_d_toda_poblacion = modelo.get("versiones", {}).get("D_variables_tratadas_poblacion_cruda", {}).get("r2", 0)
    n_muestra_grande = pob.get("A_solo_poblacion_limpia", {}).get("n_test", 0)

    st.markdown(
        f"La sección 2 mostró que B gana a A (+{fmt_num(diferencia_ab_426, 3)} de R²). ¿Por qué? Aquí se "
        f"separa el efecto de las variables del de la población, con más margen: una muestra grande de "
        f"{fmt_num(n_muestra_grande)} filas para A y D (de la que las 426 de la sección 2 son un "
        f"subconjunto), y la propia población limpia de B."
    )

    aislar = modelo.get("aislar_variables_vs_poblacion", {})
    r2_var = aislar.get("A_vs_D_r2_diferencia", 0)
    rango_pob = aislar.get("cambio_poblacion_r2_diferencia_rango", [0, 0])
    d_toda_poblacion = modelo.get("versiones", {}).get("D_variables_tratadas_poblacion_cruda", {})

    def _fila_antes_despues(etiqueta, antes, despues, color):
        delta = despues - antes
        signo = "+" if delta >= 0 else ""
        st.markdown(
            f'<div style="display:flex; align-items:center; justify-content:space-between; flex-wrap: wrap; '
            f'background-color:#f8f9fa; border-radius:8px; padding:0.7rem 1rem; margin-bottom:0.6rem; gap:0.5rem;">'
            f'<span style="font-size:0.95rem; font-weight:700; color:#31333F;">{etiqueta}</span>'
            f'<div style="display:flex; align-items:center; gap:0.6rem;">'
            f'<span style="font-size:1rem; color:#666;">{fmt_num(antes, 3)}</span>'
            f'<span style="color:#aaa;">&rarr;</span>'
            f'<span style="font-size:1rem; font-weight:700; color:#31333F;">{fmt_num(despues, 3)}</span>'
            f'<span style="background-color:{color}1A; color:{color}; padding:0.25rem 0.6rem; border-radius:6px; '
            f'font-size:0.9rem; font-weight:800; margin-left:0.4rem;">{signo}{fmt_num(delta, 3)}</span>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.1rem 1.3rem; margin-bottom: 1rem;">',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div style="font-size:0.8rem; font-weight:800; color:{AZUL_PETROLEO}; letter-spacing:0.4px; margin-bottom:0.5rem;">'
        f'EFECTO DE LAS VARIABLES &nbsp;·&nbsp; misma población completa, n=13.355</div>',
        unsafe_allow_html=True,
    )
    _fila_antes_despues(
        "A (crudo) &rarr; D (variables tratadas)",
        pob["A_toda_poblacion"]["r2"], r2_d_toda_poblacion, AZUL_PETROLEO,
    )
    st.markdown(
        f'<div style="font-size:0.8rem; font-weight:800; color:{OCRE_DORADO_TEXTO}; letter-spacing:0.4px; margin:0.9rem 0 0.5rem;">'
        f'EFECTO DE LA POBLACIÓN &nbsp;·&nbsp; mismo modelo, quitando filas problemáticas</div>',
        unsafe_allow_html=True,
    )
    _fila_antes_despues(
        "A, toda su población &rarr; A, población limpia",
        pob["A_toda_poblacion"]["r2"], pob["A_solo_poblacion_limpia"]["r2"], OCRE_DORADO_TEXTO,
    )
    _fila_antes_despues(
        "D, toda su población &rarr; D, población limpia",
        r2_d_toda_poblacion, pob["D_solo_poblacion_limpia"]["r2"], OCRE_DORADO_TEXTO,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if pob:
        st.plotly_chart(
            r2_muestra_comun(
                ["A · muestra grande", "D · muestra grande", "B · su población"],
                [
                    pob["A_solo_poblacion_limpia"]["r2"], pob["D_solo_poblacion_limpia"]["r2"],
                    pob["B_propia_poblacion_limpia"]["r2"],
                ],
                [COLOR_CRUDO, COLOR_NEUTRO, COLOR_TRATADO],
                titulo=f"R² de A y D en la muestra grande (n={fmt_num(n_muestra_grande)}), y de B en su propia población limpia",
            ),
            width="stretch",
        )
        st.markdown(
            f"Al evaluarlos sobre la muestra grande, el R² de A y D baja a "
            f"**{fmt_num(pob['A_solo_poblacion_limpia']['r2'], 3)}** y **{fmt_num(pob['D_solo_poblacion_limpia']['r2'], 3)}** "
            f"-- muy cerca del R² de B (**{fmt_num(pob['B_propia_poblacion_limpia']['r2'], 3)}**). "
            f"**Conclusión: la diferencia entre A y B viene sobre todo de la población (-0,034 a -0,036), "
            f"no de las variables (-{fmt_num(r2_var, 3)}) -- 8-9 veces más.**"
        )
        with st.expander("Ver detalle del cálculo y MAE de cada evaluación"):
            st.markdown(
                "Esta comprobación no usa las 426 filas seguras de la sección 1 -- las 426 son un "
                "subconjunto de esta misma muestra grande, reducido todavía más para que quepa también B "
                "(sección 2). Aquí no hace falta esa restricción extra porque nunca se evalúa un modelo con "
                f"filas de otro (solo A y D, cada uno sobre un subconjunto de su propio test). {pob.get('nota', '')}"
            )
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
    sec5, sec6 = st.columns(2)
    with sec5:
        with st.container(border=True):
            st.markdown("**4 · ¿Cambia la conclusión si utilizamos otro criterio de imputación?**")
            versiones = modelo.get("versiones", {})
            b = versiones.get("B_tratado_criterio_A", {})
            sens = versiones.get("TRATADO_criterio_B_barrio", {})
            diff = sens.get("diferencia_vs_A", {})
            if diff:
                col_mae, col_r2 = st.columns(2)
                with col_mae:
                    st.markdown(
                        f"""
                        <div style="text-align: center; padding: 0.6rem 0;">
                          <div style="font-size: 0.78rem; color: #666;">Diferencia de MAE</div>
                          <div style="font-size: 1.6rem; font-weight: 800; color: {COLOR_SENSIBILIDAD};">+{fmt_num(diff.get('mae_eur', 0), 1)} €</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with col_r2:
                    st.markdown(
                        f"""
                        <div style="text-align: center; padding: 0.6rem 0;">
                          <div style="font-size: 0.78rem; color: #666;">Diferencia de R²</div>
                          <div style="font-size: 1.6rem; font-weight: 800; color: {COLOR_SENSIBILIDAD};">{fmt_num(diff.get('r2', 0), 3)}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                st.markdown(
                    "**La elección entre los dos criterios razonables de imputación apenas altera el resultado.**"
                )
                with st.expander("Ver detalle y comparación completa"):
                    st.caption("¿Cambia la conclusión si imputo por barrio en vez de por capacidad?")
                    if b and sens:
                        st.plotly_chart(
                            comparacion_sensibilidad(
                                b.get("mae", 0), sens.get("mae", 0), b.get("r2", 0), sens.get("r2", 0),
                                COLOR_TRATADO, COLOR_SENSIBILIDAD,
                                titulo="B vs. Chequeo de sensibilidad",
                            ),
                            width="stretch",
                        )
                    st.caption(
                        f"Diferencia: MAE {fmt_num(diff.get('mae_eur', 0), 1)} € "
                        f"({fmt_num(diff.get('mae_pct', 0), 2)}% relativo) · R² {fmt_num(diff.get('r2', 0), 3)}."
                    )

    with sec6:
        with st.container(border=True):
            st.markdown("**5 · ¿Qué características utiliza más el modelo?**")
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
            st.markdown(
                f'<div style="background-color: #fff3dc; border-left: 4px solid {AMBAR_PENDIENTE}; border-radius: 6px; padding: 0.5rem 0.8rem; font-size: 0.85rem; font-weight: 700; color: #806000;">'
                f'⚠️ Importancia predictiva ≠ causalidad</div>',
                unsafe_allow_html=True,
            )
            if valores_imp:
                with st.expander("Ver explicación completa y tabla por variable"):
                    st.caption("Cuánto ayuda cada variable a reducir el error de predicción cada vez que se usa para dividir los datos.")
                    st.caption(imp.get('caveat', ''))
                    st.dataframe(
                        df_imp.rename(columns={"crudo": "A (crudo)", "tratado_a": "B (tratado)", "tratado_b": "Sensibilidad"}),
                        width="stretch",
                    )

    st.markdown("---")
    st.markdown("### 6 · Un modelo puede ganar globalmente y no en cada predicción")
    ejemplo = modelo.get("ejemplo_prediccion_individual", {})
    if ejemplo:
        preds = ejemplo.get("predicciones", [])
        preds_adb = [p for p in preds if p["modelo"] in ("A", "D", "B")]
        COLOR_REAL = "#3A3A3A"

        st.markdown("**EVALUACIÓN GLOBAL**")
        st.markdown(
            f"B obtiene el mejor R² sobre la muestra común "
            f"(R² = {fmt_num(resultados_426.get('B_tratado_criterio_A', {}).get('r2', 0), 3)})."
        )
        st.markdown("<div style='text-align:center; color:#aaa; font-size:1.4rem; margin:0.3rem 0;'>&darr;</div>", unsafe_allow_html=True)

        st.markdown("**UN ANUNCIO CONCRETO**")
        datos_anuncio = ejemplo.get("datos_anuncio", {})
        if datos_anuncio:
            st.markdown(
                f"""
                <div style="background-color: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 10px; padding: 1.4rem 1.7rem; margin-bottom: 1rem;">
                  <div style="font-weight: 800; color: #31333F; margin-bottom: 0.4rem; font-size: 1.4rem;">🏠 Vivienda completa -- {datos_anuncio.get('neighbourhood_cleansed', '')}</div>
                  <div style="font-size: 0.95rem; color: #888; margin-bottom: 1.1rem;">room_type: {datos_anuncio.get('room_type', '')} -- property_type: {datos_anuncio.get('property_type', '')} -- id {ejemplo.get('id_anuncio', '')}</div>
                  <div style="display: flex; flex-wrap: wrap; gap: 2.4rem; font-size: 1.35rem; color: #333;">
                    <div>Precio/noche: <b>{fmt_num(datos_anuncio.get('precio_noche_eur', 0), 2)} €</b></div>
                    <div>Capacidad: <b>{fmt_num(datos_anuncio.get('accommodates', 0))}</b> personas</div>
                    <div>Habitaciones: <b>{fmt_num(datos_anuncio.get('bedrooms', 0))}</b></div>
                    <div>Baños: <b>{fmt_num(datos_anuncio.get('bathrooms', 0))}</b></div>
                    <div>Camas: <b>{fmt_num(datos_anuncio.get('beds', 0))}</b></div>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.caption(f"¿Cómo se eligió? De las {fmt_num(ejemplo.get('n_poblacion', 0))} filas seguras, se buscó el anuncio real más cercano a la mediana -- para no favorecer a ningún modelo.")
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: center; gap: 1rem; margin: 0.6rem 0 1rem 0; flex-wrap: wrap;">
              <div style="text-align: center;">
                <div style="font-size: 0.85rem; color: #666;">Mediana de las {fmt_num(ejemplo.get('n_poblacion', 0))} filas</div>
                <div style="font-size: 1.6rem; font-weight: 800; color: {AZUL_PETROLEO};">{fmt_num(ejemplo.get('mediana_poblacion_eur', 0), 1)} €</div>
              </div>
              <div style="font-size: 1.6rem; color: #aaa;">&rarr;</div>
              <div style="text-align: center;">
                <div style="font-size: 0.85rem; color: #666;">Este anuncio (ID {ejemplo.get('id_anuncio', '')})</div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #31333F;">{fmt_num(ejemplo.get('valor_real_eur', 0), 1)} €</div>
              </div>
              <div style="font-size: 1.6rem; color: #aaa;">&rarr;</div>
              <div style="text-align: center;">
                <div style="font-size: 0.85rem; color: #666;">Distancia</div>
                <div style="font-size: 1.6rem; font-weight: 800; color: {AMBAR_PENDIENTE};">{fmt_num(ejemplo.get('distancia_a_mediana_eur', 0), 1)} €</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        color_por_modelo = {"A": COLOR_CRUDO, "D": COLOR_D, "B": COLOR_TRATADO, "C": COLOR_SENSIBILIDAD}
        nombre_por_modelo = {"A": "A -- CRUDO", "D": "D", "B": "B -- TRATADO", "C": "Chequeo de sensibilidad"}
        preds_por_valor = sorted(preds_adb, key=lambda p: p["prediccion_eur"])
        valor_max = max([ejemplo.get("valor_real_eur", 0)] + [p["prediccion_eur"] for p in preds_por_valor])
        _barra_eur("Valor de referencia", ejemplo.get("valor_real_eur", 0), valor_max, COLOR_REAL, negrita=True)
        for p in preds_por_valor:
            etiqueta = f"{nombre_por_modelo.get(p['modelo'], p['nombre_display'])} -- error: {fmt_num(p['error_abs_eur'], 1)} €"
            _barra_eur(etiqueta, p["prediccion_eur"], valor_max, color_por_modelo.get(p["modelo"], AZUL_PETROLEO))
        st.markdown("<div style='text-align:center; color:#aaa; font-size:1.4rem; margin:0.3rem 0;'>&darr;</div>", unsafe_allow_html=True)

        st.markdown("**RESULTADO**")
        ganador = min(preds_adb, key=lambda p: p["error_abs_eur"])
        st.markdown(
            f"**D obtiene el menor error individual en este anuncio** -- "
            f"{fmt_num(ganador['error_abs_eur'], 1)} € de error absoluto."
        )

        st.markdown("---")
        st.markdown("**El mejor modelo global no tiene por qué ser el más preciso en cada predicción individual.**")
        st.caption(
            "Es un ejemplo ilustrativo de un único anuncio, no una demostración de que D sea mejor modelo que B."
        )
        with st.expander("Ver notas metodológicas (criterio de selección del anuncio)"):
            st.caption(
                f"Existe otro registro empatado en distancia a la mediana (ID {ejemplo.get('empate_id', '')}), "
                f"también a {fmt_num(ejemplo.get('distancia_a_mediana_eur', 0), 1)} € -- se conserva el primero "
                "según el criterio determinista del notebook."
            )
            st.caption(ejemplo.get("nota_metodologica", ""))

        pred_c = next((p for p in preds if p["modelo"] == "C"), None)
        if pred_c:
            with st.expander("Ficha técnica: predicción del Chequeo de sensibilidad para este anuncio"):
                st.markdown(
                    f"Predicción: **{fmt_num(pred_c['prediccion_eur'], 1)} €** -- "
                    f"error absoluto: **{fmt_num(pred_c['error_abs_eur'], 1)} €**."
                )
                st.caption(
                    "No es un cuarto modelo global -- el Chequeo responde una pregunta distinta a la de A, D "
                    "y B (ver bloque 4). Un solo caso tampoco demuestra nada sobre su rendimiento general."
                )

with tab_confianza:
    st.markdown("## ¿Cuánta confianza hay en estos resultados?")

    sim = modelo.get("simulacion_5000_submuestras", {})
    boot = modelo.get("bootstrap_intervalos_confianza", {})
    comparaciones = boot.get("comparaciones", [])
    pob_grande = modelo.get("poblacion_limpia_experimento", {})
    r2_a_grande = pob_grande.get("A_solo_poblacion_limpia", {}).get("r2", 0)
    r2_d_grande = pob_grande.get("D_solo_poblacion_limpia", {}).get("r2", 0)
    delta_grande = r2_a_grande - r2_d_grande
    muestra_426_r = modelo.get("muestra_comun_426", {}).get("resultados", {})
    r2_a_pequena = muestra_426_r.get("A_crudo", {}).get("r2", 0)
    r2_d_pequena = muestra_426_r.get("D_variables_tratadas_poblacion_cruda", {}).get("r2", 0)
    delta_pequena = abs(r2_a_pequena - r2_d_pequena)

    st.markdown(
        f"""
        <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 1rem;">
          <svg width="100%" height="380" viewBox="0 0 1040 320" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <marker id="flecha_rompecabezas" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
                <path d="M0,0 L10,5 L0,10 z" fill="#aaa" />
              </marker>
            </defs>
            <text x="200" y="20" text-anchor="middle" fill="#888" font-size="11" font-weight="600" letter-spacing="0.5" font-family="Helvetica">1. DOS MUESTRAS, DOS RESULTADOS</text>
            <text x="780" y="20" text-anchor="middle" fill="#888" font-size="11" font-weight="600" letter-spacing="0.5" font-family="Helvetica">2. LA PREGUNTA</text>
            <rect x="40" y="40" width="320" height="120" rx="10" fill="white" stroke="{COLOR_NEUTRO}" stroke-width="2" />
            <text x="200" y="65" text-anchor="middle" fill="#31333F" font-size="14" font-weight="700" font-family="Helvetica">Muestra grande -- 2.131 filas</text>
            <text x="200" y="88" text-anchor="middle" fill="#31333F" font-size="13" font-family="Helvetica">A: {fmt_num(r2_a_grande, 3)} -- D: {fmt_num(r2_d_grande, 3)}</text>
            <text x="200" y="108" text-anchor="middle" fill="#31333F" font-size="12" font-family="Helvetica">Δ R² (A-D) = {fmt_num(delta_grande, 3)}</text>
            <text x="200" y="128" text-anchor="middle" fill="#555" font-size="11" font-family="Helvetica">A ligeramente por delante</text>
            <rect x="40" y="180" width="320" height="120" rx="10" fill="white" stroke="{AMBAR_PENDIENTE}" stroke-width="2" />
            <text x="200" y="205" text-anchor="middle" fill="#31333F" font-size="14" font-weight="700" font-family="Helvetica">Muestra pequeña -- 426 filas</text>
            <text x="200" y="228" text-anchor="middle" fill="#31333F" font-size="13" font-family="Helvetica">A: {fmt_num(r2_a_pequena, 3)} -- D: {fmt_num(r2_d_pequena, 3)}</text>
            <text x="200" y="248" text-anchor="middle" fill="#31333F" font-size="12" font-family="Helvetica">Δ R² (A-D) = {fmt_num(delta_pequena, 3)}</text>
            <text x="200" y="268" text-anchor="middle" fill="#555" font-size="11" font-family="Helvetica">D claramente por delante (signo invertido)</text>
            <line x1="360" y1="100" x2="620" y2="160" stroke="#aaa" stroke-width="2" marker-end="url(#flecha_rompecabezas)" />
            <line x1="360" y1="240" x2="620" y2="205" stroke="#aaa" stroke-width="2" marker-end="url(#flecha_rompecabezas)" />
            <text x="490" y="172" text-anchor="middle" fill="#888" font-size="10" font-family="Helvetica">{fmt_num(delta_pequena, 3)} &divide; {fmt_num(delta_grande, 3)} &approx; {fmt_num(delta_pequena / delta_grande, 0)}&times;</text>
            <text x="490" y="186" text-anchor="middle" fill="#888" font-size="10" font-family="Helvetica">más grande que en la muestra grande</text>
            <rect x="620" y="125" width="320" height="110" rx="10" fill="#FBEED6" stroke="{AMBAR_PENDIENTE}" stroke-width="2" />
            <text x="780" y="175" text-anchor="middle" fill="{OCRE_DORADO_TEXTO}" font-size="15" font-weight="700" font-family="Helvetica">¿Por qué cambia tanto?</text>
            <text x="780" y="197" text-anchor="middle" fill="#806000" font-size="11" font-family="Helvetica">Investigado a fondo en los paneles de abajo</text>
          </svg>
        </div>
        """,
        unsafe_allow_html=True,
    )

    sub1, sub2 = st.columns(2)
    with sub1:
        st.markdown("**A · ¿Se repite el resultado?**")
        st.markdown(
            '<div style="background-color: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 8px; '
            'padding: 0.7rem 1rem; margin-bottom: 0.7rem; font-size: 0.85rem; color: #444;">'
            '<b>¿Cómo funciona?</b> De un universo de 2.131 filas, se sortean 426 filas distintas '
            '(sin repetir ninguna) en cada una de las 5.000 repeticiones -- simula elegir otros 426 '
            'anuncios reales distintos.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div style='text-align:center; color:#888; font-size:0.78rem; font-weight:600; letter-spacing:0.3px; margin-bottom:0.5rem;'>"
            "5.000 SUBMUESTRAS &rarr; REPETIR LA COMPARACIÓN A-D &rarr; OBSERVAR LA DISTRIBUCIÓN DE DIFERENCIAS</div>",
            unsafe_allow_html=True,
        )
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
            pct_real = sim.get('percentil_del_resultado_real', 0)
            st.markdown(
                f"""
                <div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-left: 4px solid {AMBAR_PENDIENTE}; border-radius: 8px; padding: 1rem 1.3rem; margin-top: 0.8rem;">
                  <div style="display: flex; align-items: baseline; gap: 0.8rem; margin-bottom: 0.6rem;">
                    <div style="font-size: 2.2rem; font-weight: 800; color: {AMBAR_PENDIENTE};">{fmt_num(pct_real, 1)}%</div>
                    <div style="font-size: 0.85rem; color: #666;">percentil del resultado real</div>
                  </div>
                  <div style="font-size: 0.95rem; color: #31333F; font-weight: 700; margin-bottom: 0.4rem;">La diferencia observada es poco habitual</div>
                  <div style="font-size: 0.85rem; color: #555;">Solo el {fmt_num(pct_real, 1)}% de las 5.000 submuestras dieron un resultado tan extremo como el real, o más.</div>
                  <div style="font-size: 0.78rem; color: #888; border-top: 1px solid #eee; margin-top: 0.6rem; padding-top: 0.5rem;">Esto no demuestra por sí solo significación estadística -- es una medida de sensibilidad a qué filas se evalúan, no una prueba formal.</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.expander("Ver detalle de la simulación y explicación completa"):
                st.metric("Media de 5.000 simulaciones", fmt_num(sim.get('r2_diferencia_media', 0), 4))
                st.metric("Desviación estándar", fmt_num(sim.get('r2_diferencia_std', 0), 4))
                rango = sim.get('rango_central_95', [0, 0])
                st.metric("Rango central (2.5%-97.5%)", f"[{fmt_num(rango[0], 4)}, {fmt_num(rango[1], 4)}]")
                st.metric("Resultado real observado (426 filas)", fmt_num(sim.get('diferencia_real_observada_426', 0), 4))
                st.markdown(
                    "Con solo 426 filas, no se puede afirmar con seguridad que si se hubieran elegido otros "
                    "426 anuncios distintos, el resultado se mantuviera igual -- de hecho, el histograma "
                    "muestra que la mayoría de esas otras elecciones posibles habrían dado un resultado muy "
                    "distinto (más cercano a cero, o incluso a favor de A). Por eso esta comparación "
                    "concreta, por sí sola, no es una base sólida para afirmar que D gana a A -- el hallazgo "
                    "fiable es el de la muestra grande (sección 3)."
                )

    with sub2:
        st.markdown("**B · ¿Cuánta incertidumbre tiene la muestra?**")
        st.markdown(
            '<div style="background-color: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 8px; '
            'padding: 0.7rem 1rem; margin-bottom: 0.7rem; font-size: 0.85rem; color: #444;">'
            '<b>¿Cómo funciona?</b> De las mismas 426 filas fijas, se sacan 426 "con reemplazo" (un mismo '
            'anuncio puede salir repetido) en cada una de las 5.000 repeticiones -- simula la variabilidad '
            'dentro de esta misma muestra, sin cambiar de anuncios.</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div style='font-size:0.82rem; color:#555; margin-bottom:0.6rem;'>"
            "Si el intervalo <b>cruza el cero</b> &rarr; no concluyente. "
            "Si <b>no lo cruza</b> &rarr; diferencia respaldada por este procedimiento.</div>",
            unsafe_allow_html=True,
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
            st.markdown(
                "**B predice mejor que A, y esa diferencia SÍ es estadísticamente real** -- el intervalo de "
                "confianza de A vs. B no incluye el cero."
            )
            with st.expander("Ver cómo se hizo el bootstrap, e intervalos por comparación"):
                st.markdown(
                    "Igual que en el panel A, se repite el cálculo 5.000 veces -- pero con un método "
                    "distinto. Aquí no se buscan otras filas del universo: se vuelve a muestrear de las "
                    "mismas 426 filas, con reemplazo (un mismo anuncio puede salir repetido varias veces en "
                    "una ronda, o ninguna). En cada una de las 5.000 repeticiones se remuestrea una sola vez "
                    "y se aplica igual a A, D y B -- los tres se evalúan sobre las mismas filas "
                    "remuestreadas en cada ronda, para que la comparación entre ellos sea consistente ronda "
                    "a ronda. Mide la fiabilidad de la muestra que ya tienes, no cambia de muestra."
                )
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
                    "Lo único que no se puede repartir con precisión es **cuánto** de esa mejora viene de "
                    "excluir los ceros artificiales (población) y cuánto de construir mejor las variables -- "
                    "esas dos piezas, vistas por separado (A-D y D-B), sí incluyen el cero en esta muestra de "
                    "426 filas. Que un intervalo incluya el 0 no demuestra que el efecto sea nulo, solo que "
                    "con esta muestra no se puede distinguir del azar."
                )

    st.markdown("---")
    st.markdown("## Conclusión de esta sección")
    concl = modelo.get("conclusion_final", {})

    def _tarjeta_conclusion(numero, color, titulo, texto):
        st.markdown(
            f'<div style="background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 10px; '
            f'padding: 1.2rem 1.3rem; height: 100%;">'
            f'<div style="display: flex; align-items: center; gap: 0.7rem; margin-bottom: 0.6rem;">'
            f'<div style="width: 38px; height: 38px; min-width: 38px; border-radius: 50%; background-color: {color}; '
            f'color: white; display: flex; align-items: center; justify-content: center; font-weight: 800; '
            f'font-size: 1.2rem;">{numero}</div>'
            f'<div style="font-size: 0.95rem; color: {color}; font-weight: 700; text-transform: uppercase; '
            f'letter-spacing: 0.5px; line-height: 1.3;">{titulo}</div>'
            f'</div>'
            f'<div style="font-size: 1.15rem; color: #31333F; line-height: 1.55;">{texto}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    col_ev, col_int, col_lim = st.columns(3)
    with col_ev:
        _tarjeta_conclusion(1, AZUL_PETROLEO, "Evidencia -- lo observado", concl.get('observado', ''))
    with col_int:
        _tarjeta_conclusion(2, COLOR_NEUTRO, "Interpretación -- la lectura razonable", concl.get('interpretacion_razonable', ''))
    with col_lim:
        _tarjeta_conclusion(3, AMBAR_PENDIENTE, "Limitación -- lo que sigue sin resolver", concl.get('sin_resolver', ''))
