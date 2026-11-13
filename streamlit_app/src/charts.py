"""Constructores de gráficos Plotly reutilizados entre páginas."""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from src.styles import (
    AZUL_OSCURO, AZUL_PETROLEO, TURQUESA, AMBAR_ALERTA, GRIS_TEXTO, AMBAR_PENDIENTE,
    AZUL_PIZARRA, AZUL_PIZARRA_CLARO, AZUL_ACERO, VIOLETA, GRIS_HIELO, fmt_num,
)

FONT_BASE = dict(size=14)
FONT_TITULO = dict(size=20)


def barras_r2_modelos(nombres, valores, colores=None, titulo="Comparación de R²"):
    colores = colores or [AZUL_PETROLEO] * len(nombres)
    fig = go.Figure(
        go.Bar(
            x=nombres, y=valores, marker_color=colores,
            text=[fmt_num(v, 3) for v in valores], textposition="outside",
            hovertemplate="%{x}<br>R² = %{y:.3f}<extra></extra>",
        )
    )
    fig.update_layout(
        title=titulo, yaxis_title="R² (sobre su propia población de test)",
        template="plotly_white", showlegend=False, height=420,
        margin=dict(t=60, b=40), font=FONT_BASE, title_font=FONT_TITULO,
    )
    fig.update_yaxes(range=[0, max(valores) * 1.25])
    return fig


def completitud_por_columna(columnas, pct_nulo, titulo="% de valores nulos por columna", color=AZUL_PETROLEO):
    orden = sorted(zip(columnas, pct_nulo), key=lambda x: x[1])
    cols = [c for c, _ in orden]
    vals = [v for _, v in orden]
    fig = go.Figure(
        go.Bar(
            x=vals, y=cols, orientation="h", marker_color=color,
            text=[f"{fmt_num(v, 1)}%" for v in vals], textposition="outside",
            hovertemplate="%{y}: %{x:.1f}%% nulo<extra></extra>",
        )
    )
    fig.update_layout(
        title=titulo, xaxis_title="% de filas con valor nulo",
        template="plotly_white", height=360, margin=dict(t=60, b=40, l=10),
        font=FONT_BASE, title_font=FONT_TITULO,
    )
    return fig


def licencia_categorias(nombres, pcts, titulo="Distribución del campo license"):
    colores = [AMBAR_ALERTA if "sin dato" in n.lower() or "no clasificable" in n.lower() else AZUL_PETROLEO for n in nombres]
    fig = go.Figure(
        go.Bar(
            x=pcts, y=nombres, orientation="h", marker_color=colores,
            text=[f"{fmt_num(v, 1)}%" for v in pcts], textposition="outside",
            hovertemplate="%{y}: %{x:.1f}%%<extra></extra>",
        )
    )
    fig.update_layout(
        title=titulo, xaxis_title="% de anuncios", template="plotly_white",
        height=320, margin=dict(t=60, b=40, l=10),
        font=FONT_BASE, title_font=FONT_TITULO,
    )
    fig.update_yaxes(automargin=True)
    return fig


def dispersion_muestra_simulada(diffs, diferencia_real, titulo="Distribución de 5.000 submuestras (A - D)"):
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=diffs, nbinsx=60, marker_color=AZUL_PETROLEO, name="Submuestras simuladas", opacity=0.85))
    fig.add_vline(x=diferencia_real, line_color=VIOLETA, line_width=2, line_dash="dash",
                  annotation_text=f"Resultado real (426 filas): {diferencia_real:.3f}".replace(".", ","),
                  annotation_position="top right")
    fig.add_vline(x=0, line_color=GRIS_TEXTO, line_width=1, line_dash="dot")
    fig.update_layout(
        title=titulo, xaxis_title="Diferencia de R² (A - D)", yaxis_title="Frecuencia",
        template="plotly_white", height=420, margin=dict(t=60, b=40),
        font=FONT_BASE, title_font=FONT_TITULO,
    )
    return fig


def intervalo_confianza(nombres, medias, los, his, titulo="Intervalos de confianza (bootstrap, 95%)"):
    fig = go.Figure()
    hubo_real = False
    hubo_no_concluyente = False
    for nombre, media, lo, hi in zip(nombres, medias, los, his):
        incluye_cero = lo <= 0 <= hi
        color = GRIS_TEXTO if incluye_cero else TURQUESA
        hubo_no_concluyente = hubo_no_concluyente or incluye_cero
        hubo_real = hubo_real or not incluye_cero
        fig.add_trace(go.Scatter(
            x=[lo, hi], y=[nombre, nombre], mode="lines",
            line=dict(color=color, width=6), showlegend=False,
            hovertemplate=f"{nombre}<br>IC95%% [{lo:.3f}, {hi:.3f}]<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=[media], y=[nombre], mode="markers+text",
            marker=dict(color=color, size=11, symbol="diamond"), showlegend=False,
            text=[f"media: {media:.3f}"], textposition="top center",
            textfont=dict(color=color, size=12), hoverinfo="skip",
        ))
        fig.add_trace(go.Scatter(
            x=[lo, hi], y=[nombre, nombre], mode="text",
            text=[f"{lo:.3f}", f"{hi:.3f}"], textposition=["middle left", "middle right"],
            textfont=dict(color=color, size=12), showlegend=False, hoverinfo="skip",
        ))
    if hubo_real:
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode="lines", line=dict(color=TURQUESA, width=6),
            name="Diferencia real (no toca el cero)",
        ))
    if hubo_no_concluyente:
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode="lines", line=dict(color=GRIS_TEXTO, width=6),
            name="No concluyente (toca el cero)",
        ))
    fig.add_vline(
        x=0, line_color="#999999", line_width=1.5, line_dash="dot", layer="below",
        annotation_text="cero = sin diferencia", annotation_position="top",
        annotation_font=dict(size=12, color="#777777"),
    )
    margen_x = (max(his) - min(los)) * 0.12
    fig.update_layout(
        title=titulo, xaxis_title="Diferencia de R² (si la barra toca esta línea, no es concluyente)",
        xaxis_range=[min(los) - margen_x, max(his) + margen_x],
        template="plotly_white", height=410, margin=dict(t=90, b=90, l=10),
        font=FONT_BASE, title_font=FONT_TITULO,
        legend=dict(orientation="h", yanchor="top", y=-0.35, xanchor="left", x=0, font=dict(size=12)),
    )
    return fig


def dispersion_real_vs_predicho(real, predicho, r2, nombre, color):
    fig = go.Figure()
    fig.add_trace(go.Scattergl(
        x=real, y=predicho, mode="markers",
        marker=dict(color=color, size=5, opacity=0.35), name=nombre,
        hovertemplate="Real: %{x:.0f} €<br>Predicho: %{y:.0f} €<extra></extra>",
    ))
    lim = max(max(real, default=0), max(predicho, default=0))
    fig.add_trace(go.Scatter(x=[0, lim], y=[0, lim], mode="lines",
                              line=dict(color="#333333", dash="dash"), name="Predicción perfecta"))
    fig.update_layout(
        title=f"{nombre} (R² = {r2:.3f})", xaxis_title="Ingreso real (€)", yaxis_title="Ingreso predicho (€)",
        template="plotly_white", height=420, margin=dict(t=60, b=40),
        font=FONT_BASE, title_font=FONT_TITULO,
    )
    return fig


def importancia_variables(df_importancia, series, titulo="Importancia de variables"):
    """series: lista de (columna, nombre_legible, color) -- una barra por modelo, agrupadas por variable."""
    orden = df_importancia[series[0][0]].sort_values(ascending=True).index
    datos = df_importancia.loc[orden]
    fig = go.Figure()
    for columna, nombre, color in series:
        fig.add_trace(go.Bar(
            x=datos[columna], y=datos.index, orientation="h", name=nombre, marker_color=color,
            hovertemplate=f"{nombre} -- %{{y}}: %{{x:.4f}}<extra></extra>",
        ))
    fig.update_layout(
        title=titulo, xaxis_title="Importancia (Gini, Random Forest)", template="plotly_white",
        barmode="group", height=420, margin=dict(t=60, b=40, l=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        font=FONT_BASE, title_font=FONT_TITULO,
    )
    return fig


def comparacion_sensibilidad(mae_b, mae_sens, r2_b, r2_sens, color_b, color_sens,
                              titulo="B vs. Chequeo de sensibilidad"):
    """Dos mini-barras (MAE y R2) comparando el modelo B contra el chequeo con criterio de imputación alternativo."""
    fig = make_subplots(rows=1, cols=2, subplot_titles=("MAE (€, menor = mejor)", "R² (mayor = mejor)"))
    nombres = ["B (criterio A)", "Chequeo (criterio B)"]
    colores = [color_b, color_sens]

    fig.add_trace(go.Bar(
        x=nombres, y=[mae_b, mae_sens], marker_color=colores,
        text=[fmt_num(mae_b, 1), fmt_num(mae_sens, 1)], textposition="outside",
        showlegend=False,
    ), row=1, col=1)
    fig.add_trace(go.Bar(
        x=nombres, y=[r2_b, r2_sens], marker_color=colores,
        text=[fmt_num(r2_b, 3), fmt_num(r2_sens, 3)], textposition="outside",
        showlegend=False,
    ), row=1, col=2)

    fig.update_yaxes(range=[0, max(mae_b, mae_sens) * 1.25], row=1, col=1)
    fig.update_yaxes(range=[0, max(r2_b, r2_sens) * 1.25], row=1, col=2)
    fig.update_layout(
        title=titulo, template="plotly_white", height=380,
        margin=dict(t=70, b=40), font=FONT_BASE, title_font=FONT_TITULO,
    )
    return fig


def mapa_licencia_distrito(geojson, distritos, pcts, n_anuncios, titulo="Problema de licencia (%) por distrito"):
    """Mapa coroplético a nivel de barrio, coloreado por el % de licencia-problema de SU distrito
    (cada barrio hereda el valor agregado de su distrito, no hay dato propio a nivel de barrio)."""
    nombre_por_barrio = []
    valor_por_barrio = []
    distrito_por_barrio = []
    mapa_valores = dict(zip(distritos, pcts))
    mapa_n = dict(zip(distritos, n_anuncios))
    for feat in geojson["features"]:
        barrio = feat["properties"]["neighbourhood"]
        distrito = feat["properties"]["neighbourhood_group"]
        nombre_por_barrio.append(barrio)
        valor_por_barrio.append(mapa_valores.get(distrito))
        distrito_por_barrio.append(distrito)

    valor_max = max(pcts)

    fig = px.choropleth_map(
        {
            "barrio": nombre_por_barrio,
            "distrito": distrito_por_barrio,
            "pct_problema": valor_por_barrio,
        },
        geojson=geojson,
        locations="barrio",
        featureidkey="properties.neighbourhood",
        color="pct_problema",
        color_continuous_scale=[GRIS_HIELO, AZUL_ACERO, AZUL_OSCURO],
        range_color=[0, valor_max],
        hover_name="distrito",
        hover_data={"barrio": True, "pct_problema": ":.1f", "distrito": False},
        map_style="carto-positron",
        center={"lat": 41.3874, "lon": 2.1686},
        zoom=11.3,
        opacity=0.85,
    )
    fig.update_layout(
        title=titulo, template="plotly_white", height=480,
        margin=dict(t=60, b=10, l=0, r=60),
        coloraxis_colorbar=dict(
            title="% problema",
            tickvals=[0, 10, 20, 30, valor_max],
            ticktext=["0%", "10%", "20%", "30%", f"{valor_max:.1f}%"],
        ),
        font=FONT_BASE, title_font=FONT_TITULO,
    )
    return fig


def mapa_anuncios_distrito(geojson, distritos, n_anuncios, titulo="Anuncios de Airbnb por distrito"):
    """Mapa coroplético a nivel de barrio, coloreado por el número de anuncios de SU distrito
    (cada barrio hereda el valor agregado de su distrito, no hay dato propio a nivel de barrio)."""
    nombre_por_barrio = []
    valor_por_barrio = []
    distrito_por_barrio = []
    mapa_n = dict(zip(distritos, n_anuncios))
    for feat in geojson["features"]:
        barrio = feat["properties"]["neighbourhood"]
        distrito = feat["properties"]["neighbourhood_group"]
        nombre_por_barrio.append(barrio)
        valor_por_barrio.append(mapa_n.get(distrito))
        distrito_por_barrio.append(distrito)

    valor_max = max(n_anuncios)

    fig = px.choropleth_map(
        {
            "barrio": nombre_por_barrio,
            "distrito": distrito_por_barrio,
            "n_anuncios": valor_por_barrio,
        },
        geojson=geojson,
        locations="barrio",
        featureidkey="properties.neighbourhood",
        color="n_anuncios",
        color_continuous_scale=["#F7F8FA", TURQUESA, AZUL_PETROLEO],
        range_color=[0, valor_max],
        hover_name="distrito",
        hover_data={"barrio": True, "n_anuncios": True, "distrito": False},
        map_style="carto-positron",
        center={"lat": 41.3874, "lon": 2.1686},
        zoom=11.3,
        opacity=0.85,
    )
    fig.update_traces(marker_line_color=AZUL_PIZARRA, marker_line_width=1.1)
    fig.update_layout(
        title=titulo, template="plotly_white", height=460,
        margin=dict(t=60, b=10, l=0, r=0),
        coloraxis_colorbar=dict(
            title="Anuncios",
            tickvals=[0, 2000, 4000, valor_max],
            ticktext=["0", "2.000", "4.000", f"{valor_max:,}".replace(",", ".")],
        ),
        font=FONT_BASE, title_font=FONT_TITULO,
    )
    return fig


def reclasificacion_anuncios(n_revision, n_siguen_descartados, titulo="¿Qué pasa con los anuncios descartados por la regla original?"):
    total = n_revision + n_siguen_descartados
    pct_revision = n_revision / total * 100
    pct_descartados = n_siguen_descartados / total * 100
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=["Regla auditada"], x=[n_revision], orientation="h", name="Pasan a revisión",
        marker_color=AMBAR_PENDIENTE, showlegend=False,
        text=[f"Pasan a revisión<br>{fmt_num(n_revision)} ({fmt_num(pct_revision, 1)}%)"], textposition="inside",
        hovertemplate=f"Pasan a revisión: {fmt_num(n_revision)} ({fmt_num(pct_revision, 1)}%)<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        y=["Regla auditada"], x=[n_siguen_descartados], orientation="h", name="Siguen descartados",
        marker_color=AZUL_OSCURO, showlegend=False,
        text=[f"Siguen descartados<br>{fmt_num(n_siguen_descartados)} ({fmt_num(pct_descartados, 1)}%)"], textposition="inside",
        hovertemplate=f"Siguen descartados: {fmt_num(n_siguen_descartados)} ({fmt_num(pct_descartados, 1)}%)<extra></extra>",
    ))
    fig.update_layout(
        title=titulo, barmode="stack", template="plotly_white", height=220, showlegend=False,
        xaxis_title=f"Anuncios descartados por la regla original (n={fmt_num(total)})",
        margin=dict(t=60, b=50, l=10),
        font=FONT_BASE, title_font=FONT_TITULO,
    )
    return fig


def hallazgos_por_tabla(n_listings, n_reviews, n_calendar):
    tablas = ["listings", "reviews", "calendar"]
    letras = ["L", "R", "C"]
    valores = [n_listings, n_reviews, n_calendar]
    colores = AZUL_PIZARRA
    fig = go.Figure(
        go.Bar(
            x=tablas, y=valores, marker_color=colores,
            text=[str(v) for v in valores], textposition="outside",
            hovertemplate="%{x}: %{y} hallazgos<extra></extra>",
        )
    )
    fig.update_layout(
        template="plotly_white", showlegend=False, height=140,
        margin=dict(t=10, b=30, l=10, r=10),
        yaxis=dict(visible=False, range=[0, max(valores) * 1.3]),
        xaxis=dict(
            tickvals=tablas,
            ticktext=[f"{t}<br><b>{l}</b>" for t, l in zip(tablas, letras)],
        ),
        font=dict(size=12),
    )
    return fig


def huerfanas_por_tabla(pct_reviews, pct_calendar):
    tablas = ["reviews (R2)", "calendar (C1)"]
    valores = [pct_reviews, pct_calendar]
    fig = go.Figure(
        go.Bar(
            x=valores, y=tablas, orientation="h", marker_color=AMBAR_ALERTA,
            text=[f"{fmt_num(v, 2)}%" for v in valores], textposition="outside",
            hovertemplate="%{y}: %{x:.2f}%% huérfanas<extra></extra>",
        )
    )
    fig.update_layout(
        template="plotly_white", showlegend=False, height=180,
        margin=dict(t=10, b=30, l=10, r=40),
        xaxis=dict(title="% de filas huérfanas (sin listing_id válido)", range=[0, 5]),
        font=FONT_BASE,
    )
    return fig


def kpi_comparativo_eur(nombres, valores, titulo):
    colores = [AZUL_ACERO, TURQUESA] if len(valores) == 2 else [AZUL_PETROLEO] * len(valores)
    fig = go.Figure(
        go.Bar(
            x=nombres, y=valores, marker_color=colores,
            text=[f"{v:,.0f} €".replace(",", ".") for v in valores], textposition="outside",
        )
    )
    fig.update_layout(title=titulo, yaxis_title="EUR/año", template="plotly_white",
                       showlegend=False, height=380, margin=dict(t=60, b=40))
    return fig


def ingreso_particular_profesional(particular_antes, particular_despues, profesional_antes, profesional_despues,
                                    titulo="Ingreso medio por anuncio: antes vs. después de auditar los ceros"):
    categorias = ["Particular", "Profesional"]
    gap_antes_pct = (particular_antes - profesional_antes) / particular_antes * 100 if particular_antes else 0
    gap_despues_pct = (particular_despues - profesional_despues) / particular_despues * 100 if particular_despues else 0
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=categorias, y=[particular_antes, profesional_antes], name="Antes (sin investigar los ceros)",
        marker_color=GRIS_TEXTO,
        text=[f"{fmt_num(particular_antes)} €", f"{fmt_num(profesional_antes)} € (brecha: {fmt_num(gap_antes_pct, 1)}%)"],
        textposition="outside",
    ))
    fig.add_trace(go.Bar(
        x=categorias, y=[particular_despues, profesional_despues], name="Después (auditado)",
        marker_color=AZUL_PIZARRA,
        text=[f"{fmt_num(particular_despues)} €", f"{fmt_num(profesional_despues)} € (brecha: {fmt_num(gap_despues_pct, 1)}%)"],
        textposition="outside",
    ))
    fig.update_layout(
        title=titulo, barmode="group", template="plotly_white", height=420,
        yaxis_title="Ingreso medio por anuncio (EUR/año)", margin=dict(t=60, b=40),
        font=FONT_BASE, title_font=FONT_TITULO,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def perfil_tipo_habitacion(rev_entera, rev_privada, desc_entera, desc_privada,
                            titulo="Tipo de alojamiento"):
    grupos = ["Pasan a revisión", "Siguen descartados"]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grupos, y=[rev_entera, desc_entera], name="Alojamiento entero", marker_color=AZUL_PIZARRA,
        text=[f"{fmt_num(v, 1)}%" for v in [rev_entera, desc_entera]], textposition="inside",
    ))
    fig.add_trace(go.Bar(
        x=grupos, y=[rev_privada, desc_privada], name="Habitación privada", marker_color=AZUL_PIZARRA_CLARO,
        text=[f"{fmt_num(v, 1)}%" for v in [rev_privada, desc_privada]], textposition="inside",
    ))
    fig.update_layout(
        title=titulo, barmode="stack", template="plotly_white", height=320,
        yaxis_title="% de anuncios del grupo", margin=dict(t=60, b=40),
        font=FONT_BASE, title_font=FONT_TITULO,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def perfil_precio_mediana(rev_entera, rev_privada, desc_entera, desc_privada,
                           titulo="Precio mediana (€/noche)"):
    grupos = ["Pasan a revisión", "Siguen descartados"]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=grupos, y=[rev_entera, desc_entera], name="Alojamiento entero", marker_color=AZUL_PIZARRA,
        text=[f"{fmt_num(v, 1)} €" for v in [rev_entera, desc_entera]], textposition="outside",
    ))
    fig.add_trace(go.Bar(
        x=grupos, y=[rev_privada, desc_privada], name="Habitación privada", marker_color=AZUL_PIZARRA_CLARO,
        text=[f"{fmt_num(v, 1)} €" for v in [rev_privada, desc_privada]], textposition="outside",
    ))
    fig.update_layout(
        title=titulo, barmode="group", template="plotly_white", height=320,
        yaxis_title="Precio mediana (€/noche)", margin=dict(t=60, b=40),
        font=FONT_BASE, title_font=FONT_TITULO,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def r2_muestra_comun(nombres, valores, colores, titulo="R² sobre los mismos 426 casos", height=280):
    orden = sorted(zip(nombres, valores, colores), key=lambda x: x[1])
    nombres_o = [n for n, _, _ in orden]
    valores_o = [v for _, v, _ in orden]
    colores_o = [c for _, _, c in orden]
    fig = go.Figure(
        go.Bar(
            x=valores_o, y=nombres_o, orientation="h", marker_color=colores_o,
            text=[fmt_num(v, 3) for v in valores_o], textposition="outside",
            hovertemplate="%{y}<br>R² = %{x:.3f}<extra></extra>",
        )
    )
    fig.update_layout(
        title=titulo, xaxis_title="R² (mayor = más capacidad explicativa en esta evaluación)",
        template="plotly_white", showlegend=False, height=height,
        margin=dict(t=60, b=40, l=10), font=FONT_BASE, title_font=FONT_TITULO,
    )
    fig.update_xaxes(range=[0, max(valores_o) * 1.3])
    return fig
