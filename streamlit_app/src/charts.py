"""Constructores de graficos Plotly reutilizados entre paginas."""
import plotly.graph_objects as go
import plotly.express as px

from src.styles import AZUL_OSCURO, AZUL_PETROLEO, TURQUESA, ROJO_ALERTA, VERDE_OK, GRIS_TEXTO, AMBAR_PENDIENTE, AZUL_PIZARRA, fmt_num

# Tamanos de fuente pensados para leerse desde el fondo de una sala en una presentacion en vivo.
FONT_BASE = dict(size=14)
FONT_TITULO = dict(size=20)


def barras_r2_modelos(nombres, valores, colores=None, titulo="Comparacion de R²"):
    colores = colores or [AZUL_PETROLEO] * len(nombres)
    fig = go.Figure(
        go.Bar(
            x=nombres, y=valores, marker_color=colores,
            text=[fmt_num(v, 3) for v in valores], textposition="outside",
            hovertemplate="%{x}<br>R² = %{y:.3f}<extra></extra>",
        )
    )
    fig.update_layout(
        title=titulo, yaxis_title="R² (sobre su propia poblacion de test)",
        template="plotly_white", showlegend=False, height=420,
        margin=dict(t=60, b=40), font=FONT_BASE, title_font=FONT_TITULO,
    )
    fig.update_yaxes(range=[0, max(valores) * 1.25])
    return fig


def completitud_por_columna(columnas, pct_nulo, titulo="% de valores nulos por columna"):
    orden = sorted(zip(columnas, pct_nulo), key=lambda x: x[1])
    cols = [c for c, _ in orden]
    vals = [v for _, v in orden]
    colores = [ROJO_ALERTA if v >= 20 else AZUL_PETROLEO for v in vals]
    fig = go.Figure(
        go.Bar(
            x=vals, y=cols, orientation="h", marker_color=colores,
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


def licencia_categorias(nombres, pcts, titulo="Distribucion del campo license"):
    colores = [ROJO_ALERTA if "sin dato" in n.lower() or "no clasificable" in n.lower() else AZUL_PETROLEO for n in nombres]
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
    return fig


def dispersion_muestra_simulada(diffs, diferencia_real, titulo="Distribucion de 5.000 submuestras (A - D)"):
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=diffs, nbinsx=60, marker_color=AZUL_PETROLEO, name="Submuestras simuladas", opacity=0.85))
    fig.add_vline(x=diferencia_real, line_color=ROJO_ALERTA, line_width=2, line_dash="dash",
                  annotation_text="Resultado real (426 filas)", annotation_position="top right")
    fig.add_vline(x=0, line_color=GRIS_TEXTO, line_width=1, line_dash="dot")
    fig.update_layout(
        title=titulo, xaxis_title="Diferencia de R² (A - D)", yaxis_title="Frecuencia",
        template="plotly_white", height=420, margin=dict(t=60, b=40),
        font=FONT_BASE, title_font=FONT_TITULO,
    )
    return fig


def intervalo_confianza(nombres, medias, los, his, titulo="Intervalos de confianza (bootstrap, 95%)"):
    fig = go.Figure()
    for nombre, media, lo, hi in zip(nombres, medias, los, his):
        incluye_cero = lo <= 0 <= hi
        color = GRIS_TEXTO if incluye_cero else VERDE_OK
        fig.add_trace(go.Scatter(
            x=[lo, hi], y=[nombre, nombre], mode="lines",
            line=dict(color=color, width=6), showlegend=False,
            hovertemplate=f"{nombre}<br>IC95%% [{lo:.3f}, {hi:.3f}]<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=[media], y=[nombre], mode="markers",
            marker=dict(color=color, size=11, symbol="diamond"), showlegend=False,
            hovertemplate=f"{nombre}<br>media = {media:.3f}<extra></extra>",
        ))
    fig.add_vline(x=0, line_color="#999999", line_width=1, line_dash="dot")
    fig.update_layout(
        title=titulo, xaxis_title="Diferencia de R²", template="plotly_white",
        height=300, margin=dict(t=60, b=40, l=10),
        font=FONT_BASE, title_font=FONT_TITULO,
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
                              line=dict(color="#333333", dash="dash"), name="Prediccion perfecta"))
    fig.update_layout(
        title=f"{nombre} (R² = {r2:.3f})", xaxis_title="Ingreso real (€)", yaxis_title="Ingreso predicho (€)",
        template="plotly_white", height=420, margin=dict(t=60, b=40),
        font=FONT_BASE, title_font=FONT_TITULO,
    )
    return fig


def importancia_variables(df_importancia, columna, titulo="Importancia de variables"):
    datos = df_importancia.sort_values(columna, ascending=True)
    fig = go.Figure(
        go.Bar(
            x=datos[columna], y=datos.index, orientation="h", marker_color=AZUL_PETROLEO,
            hovertemplate="%{y}: %{x:.4f}<extra></extra>",
        )
    )
    fig.update_layout(
        title=titulo, xaxis_title="Importancia (Gini, Random Forest)", template="plotly_white",
        height=380, margin=dict(t=60, b=40, l=10),
        font=FONT_BASE, title_font=FONT_TITULO,
    )
    return fig


def mapa_licencia_distrito(geojson, distritos, pcts, n_anuncios, titulo="Problema de licencia (%) por distrito"):
    """Mapa coropletico a nivel de barrio, coloreado por el % de licencia-problema de SU distrito
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
        color_continuous_scale=["#F7F8FA", TURQUESA, ROJO_ALERTA],
        hover_name="distrito",
        hover_data={"barrio": True, "pct_problema": ":.1f", "distrito": False},
        map_style="carto-positron",
        center={"lat": 41.3874, "lon": 2.1686},
        zoom=10.6,
        opacity=0.85,
    )
    fig.update_layout(
        title=titulo, template="plotly_white", height=480,
        margin=dict(t=60, b=10, l=0, r=0),
        coloraxis_colorbar=dict(title="% problema"),
        font=FONT_BASE, title_font=FONT_TITULO,
    )
    return fig


def mapa_anuncios_distrito(geojson, distritos, n_anuncios, titulo="Anuncios de Airbnb por distrito"):
    """Mapa coropletico a nivel de barrio, coloreado por el numero de anuncios de SU distrito
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
        hover_name="distrito",
        hover_data={"barrio": True, "n_anuncios": True, "distrito": False},
        map_style="carto-positron",
        center={"lat": 41.3874, "lon": 2.1686},
        zoom=11.3,
        opacity=0.85,
    )
    fig.update_layout(
        title=titulo, template="plotly_white", height=460,
        margin=dict(t=60, b=10, l=0, r=0),
        coloraxis_colorbar=dict(title="Anuncios"),
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
        marker_color=ROJO_ALERTA, showlegend=False,
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
    valores = [n_listings, n_reviews, n_calendar]
    colores = [AZUL_OSCURO, TURQUESA, AZUL_PIZARRA]
    fig = go.Figure(
        go.Bar(
            x=tablas, y=valores, marker_color=colores,
            text=[str(v) for v in valores], textposition="outside",
            hovertemplate="%{x}: %{y} hallazgos<extra></extra>",
        )
    )
    fig.update_layout(
        template="plotly_white", showlegend=False, height=130,
        margin=dict(t=10, b=20, l=10, r=10),
        yaxis=dict(visible=False, range=[0, max(valores) * 1.3]),
        font=dict(size=12),
    )
    return fig


def huerfanas_por_tabla(pct_reviews, pct_calendar):
    tablas = ["reviews (R2)", "calendar (C1)"]
    valores = [pct_reviews, pct_calendar]
    fig = go.Figure(
        go.Bar(
            x=valores, y=tablas, orientation="h", marker_color=ROJO_ALERTA,
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
    colores = [ROJO_ALERTA, VERDE_OK] if len(valores) == 2 else [AZUL_PETROLEO] * len(valores)
    fig = go.Figure(
        go.Bar(
            x=nombres, y=valores, marker_color=colores,
            text=[f"{v:,.0f} €".replace(",", ".") for v in valores], textposition="outside",
        )
    )
    fig.update_layout(title=titulo, yaxis_title="EUR/anio", template="plotly_white",
                       showlegend=False, height=380, margin=dict(t=60, b=40))
    return fig
