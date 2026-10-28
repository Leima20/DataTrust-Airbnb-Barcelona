# DataTrust — app de presentación (Streamlit)

Presentación interactiva del proyecto final "DataTrust" (auditoría de calidad de datos sobre
Inside Airbnb Barcelona), pensada para apoyar una defensa oral de 20-30 minutos ante un
tribunal académico.

**Estado del proyecto**: esta app es una construcción exploratoria, pedida para ver cómo
quedaría una alternativa a la herramienta de presentación ya decidida. El plan por defecto
documentado en `00_ficha_maestra.md` sigue siendo presentar en vivo con Power BI; esta app
Streamlit no sustituye esa decisión, es un "extra opcional" a evaluar.

## Instalación y ejecución local

```bash
cd streamlit_app
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
streamlit run app.py
```

Abre `http://localhost:8501` en el navegador. La navegación entre las 7 páginas aparece
automáticamente en la barra lateral (Streamlit detecta `pages/` por convención).

## Estructura

```text
streamlit_app/
├── app.py                              # Página 1: Inicio
├── pages/
│   ├── 1_Auditoria_de_calidad.py
│   ├── 2_Diseno_experimental.py
│   ├── 3_Comparacion_de_modelos.py
│   ├── 4_Resultados_y_robustez.py
│   ├── 5_Conclusiones_y_recomendaciones.py
│   └── 6_Metodologia_y_limitaciones.py
├── src/
│   ├── data_loader.py    # Carga y cachea los JSON de data/
│   ├── styles.py          # Paleta de colores y CSS compartido
│   ├── charts.py          # Constructores de gráficos Plotly
│   └── methodology.py     # "Notas para la exposición" + FAQ del tribunal
├── data/
│   ├── README.md
│   ├── calidad_resumen.json
│   ├── impacto_negocio.json
│   └── modelo_resultados.json
└── requirements.txt
```

No se carga ningún CSV grande en tiempo de ejecución — todos los números vienen de los tres
JSON en `data/`, precalculados a partir de resultados reales ya guardados (ver
`data/README.md` para el detalle de cada fuente).

## Qué se verificó y qué no

Ver el resumen completo en la respuesta que acompañó la construcción de esta app. En corto:
casi todas las cifras del prompt original (incluidas las de R² sobre la muestra de 426 filas:
0,348 / 0,388 / 0,448) se confirmaron exactas contra las salidas guardadas del notebook 06.
La única cifra de licencia que se ajustó fue el desglose "Otro" (7,6% en el prompt original):
el dato real tiene 5 categorías, no 4 — se usó el desglose completo y verificado (HUTB 47,0%,
Exento 25,7%, Sin dato 19,9%, NRUA 6,2%, No clasificable 1,2%) en vez de agrupar las dos
últimas en una sola etiqueta "Otro".

## Pruebas realizadas

Cada página se ejecutó con `streamlit.testing.v1.AppTest` (ejecución headless real del script,
no solo revisión de sintaxis) y no produjo ninguna excepción. También se lanzó
`streamlit run app.py` en segundo plano y se confirmó una respuesta HTTP 200 del servidor.
No se hizo una revisión visual en navegador real — eso queda pendiente para quien lo ejecute
localmente.
