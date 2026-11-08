# DataTrust — app de presentación (Streamlit)

Presentación interactiva del proyecto final "DataTrust" (auditoría de calidad de datos sobre
Inside Airbnb Barcelona), pensada para apoyar una defensa oral de 20-30 minutos ante un
tribunal académico.

## Instalación y ejecución local

```bash
cd streamlit_app
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
streamlit run app.py
```

Abre `http://localhost:8501` en el navegador. La navegación entre las 9 páginas (agrupadas en
3 secciones en la barra lateral) la define `app.py` explícitamente con `st.Page()` y
`st.navigation()` — no es la convención automática de una carpeta `pages/`, las páginas viven
en `vistas/`.

## Estructura

```text
streamlit_app/
├── app.py                                    # Define la navegación (st.Page / st.navigation)
├── vistas/
│   ├── 0_Inicio.py
│   ├── 0b_Contexto_proyecto.py
│   ├── 1_Auditoria_de_calidad.py
│   ├── 1b_Hallazgo_critico_revenue.py
│   ├── 2_Diseno_experimental.py
│   ├── 3_Comparacion_de_modelos.py
│   ├── 4_Resultados_y_robustez.py
│   ├── 5_Conclusiones_y_recomendaciones.py
│   └── 6_Limitaciones.py
├── src/
│   ├── data_loader.py    # Carga y cachea los JSON de data/
│   ├── styles.py         # Paleta de colores y CSS compartido
│   ├── charts.py         # Constructores de gráficos Plotly
│   └── methodology.py    # Reservado; sin contenido (las notas de exposición no van en pantalla)
├── data/
│   ├── README.md
│   ├── calidad_resumen.json
│   ├── contexto_proyecto.json
│   ├── geografia_distrito.json
│   ├── impacto_negocio.json
│   ├── modelo_resultados.json
│   ├── neighbourhoods.geojson
│   └── simulacion_5000_valores.json
└── requirements.txt
```

No se carga ningún CSV grande en tiempo de ejecución — todos los números vienen de los JSON
en `data/`, precalculados a partir de resultados reales ya guardados (ver `data/README.md`
para el detalle de cada fuente).

## Qué se verificó

Las cifras clave (R² sobre la muestra común de 426 filas: 0,347 / 0,389 / 0,450; la brecha de
negocio 39,7% → 23,1%; el desglose de `license_categoria` en 5 categorías) se verificaron
contra las salidas guardadas del notebook 06 y contra `calidad_resumen.json` /
`impacto_negocio.json`, no se tomaron de memoria. Cada vez que una página cita un número, ese
número existe literalmente en uno de los JSON de `data/`.

## Pruebas realizadas

Cada página se ejecutó con `streamlit.testing.v1.AppTest` (ejecución headless real del script,
no solo revisión de sintaxis) y no produjo ninguna excepción. También se lanzó
`streamlit run app.py` en segundo plano, se confirmó una respuesta HTTP 200 del servidor y se
revisó visualmente cada cambio en el navegador antes de darlo por cerrado.
