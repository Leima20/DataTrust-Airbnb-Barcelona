# Datos de esta app

Esta app **no** lee `data/airbnb_bcn/` ni `data/airbnb_bcn_curado/` en tiempo de ejecución
(serían varios cientos de MB y hasta 5,6 millones de filas en `calendar.csv`). En su lugar usa
archivos JSON pequeños, precalculados a partir de resultados ya guardados:

- `calidad_resumen.json` — los 14 hallazgos de calidad (L1-L8, R1-R4, C1-C2), tamaños de las
  3 tablas, columnas 100% vacías, nulos parciales, distribución de `license_categoria`.
  Fuente: `00_ficha_maestra.md` + verificación en vivo contra los CSV curados.
- `impacto_negocio.json` — el caso de negocio (brecha profesional/particular, antes y después
  de corregir los ceros falsos). Fuente: `check_impacto_negocio_profesional.py`, reejecutado
  en vivo antes de construir esta app.
- `modelo_resultados.json` — todas las métricas de los modelos A/D/B y el chequeo de
  sensibilidad, la fuga de datos detectada y corregida, la muestra común de 426 filas y el
  bootstrap de intervalos de confianza. Fuente: salidas de celda guardadas en
  `notebooks/06_modelo_ml.ipynb`, leídas directamente con `nbformat`, sin reejecutar el
  notebook.
- `simulacion_5000_valores.json` — los 5.000 valores de diferencia de R² (A vs. D) de la
  simulación por submuestreo, usados en la página "Resultados y robustez" para ubicar el
  resultado observado dentro de la distribución completa. Misma fuente que
  `modelo_resultados.json` (notebook 06).
- `contexto_proyecto.json` — el caso Zillow Offers y el resto del contexto narrativo usado en
  "Inicio", "Contexto del proyecto" y "Auditoría de calidad".
- `geografia_distrito.json` — % de `license_problema` por distrito (el hallazgo L7), recalculado
  en vivo contra `data/airbnb_bcn_curado/listings.csv` y verificado contra el rango ya documentado
  en `00_ficha_maestra.md` (16,1% Eixample a 33,1% Nou Barris — coincide exacto).
- `neighbourhoods.geojson` — copia de `data/airbnb_bcn/neighbourhoods.geojson` (75 barrios, con su
  distrito como propiedad `neighbourhood_group`), usada para el mapa coroplético de la página
  "Auditoria de calidad". Cada barrio se colorea con el valor agregado de su distrito (no hay un
  valor de licencia propio por barrio en el dataset).

Cada archivo JSON incluye un campo `"fuente"` indicando de dónde viene. Si alguno de estos
archivos falta, las páginas que lo usan muestran "—" en vez de fallar o inventar un valor.
