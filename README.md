# DataTrust

Un estudio del impacto de la calidad y la gobernanza de datos en las
conclusiones analíticas — de negocio y de un modelo predictivo — usando el
mercado de alquiler turístico de Barcelona como caso de estudio real.

**App interactiva en vivo (presentación del proyecto)**:
[datatrust-bcn.streamlit.app](https://datatrust-bcn.streamlit.app/)

## Pregunta central

¿Cómo afectan los problemas de calidad, consistencia e integridad de los datos a
las conclusiones de negocio y al rendimiento de un modelo predictivo, en un caso
real de alquiler turístico en Barcelona?

## Dos hipótesis de trabajo

1. **Negocio**: ¿la calidad de los datos puede cambiar las conclusiones de negocio?
2. **Modelo**: ¿el tratamiento de los datos puede cambiar el rendimiento de un
   modelo predictivo?

El proyecto sigue un flujo de 6 pasos para responder a ambas hipótesis con
evidencia: 1. Auditoría (detección de hallazgos en `listings`, `reviews`,
`calendar`) → 2. Gobernanza (decisión documentada por cada hallazgo) →
3. Tratamiento (decisiones ejecutadas sobre los datos) → 4. Comparación de
negocio → 5. Comparación de modelos → 6. Simulación de decisión.

## El caso de estudio

[Airbnb Barcelona](https://insideairbnb.com/barcelona/) (Inside Airbnb, snapshot
2026-06-24): 15.293 alojamientos, 1.033.523 reseñas y 5.623.190 registros de
disponibilidad. Datos reales, no sintéticos, con problemas de calidad genuinos
(columnas vacías, licencias turísticas mal formadas, registros huérfanos entre
tablas) que se auditan, documentan y tratan a lo largo del proyecto.

## Cómo navegar este repositorio

```
Proyecto_Final/
├── README.md                    ← estás aquí
├── 00_ficha_maestra.md          ← documento de trabajo interno (plan, decisiones)
├── data/airbnb_bcn/             ← datos originales de Inside Airbnb (NO en el repo, ver abajo)
├── data/airbnb_bcn_curado/      ← datos curados en CSV (NO en el repo, ver abajo)
├── database/construir_base_datos.py  ← script para regenerar la base SQLite
├── notebooks/
│   ├── 01_auditoria_listings.ipynb       ← auditoría de alojamientos (completado)
│   ├── 02_auditoria_reviews.ipynb        ← auditoría de reseñas (completado)
│   ├── 03_auditoria_calendar.ipynb       ← auditoría de calendario (completado)
│   ├── 04_recomendaciones_gobernanza.ipynb  ← 14 hallazgos priorizados (completado)
│   ├── 05_tratamiento_curacion.ipynb     ← curación ejecutada en código (completado)
│   └── 06_modelo_ml.ipynb                ← modelo original vs. tratado (completado)
├── report/                      ← informe final en PDF (completado)
└── streamlit_app/                ← app de presentación interactiva (ver enlace arriba)
```

Se recomienda abrir los notebooks en orden numérico, cada uno documenta sus
hallazgos con el código que los produce, no solo en texto.

## Cómo reproducir los datos

Los CSV originales y curados (1,3 GB en total) y la base de datos SQLite
(1,1 GB) no están en este repositorio por su tamaño. Para regenerarlos:

1. Descargar `listings.csv`, `reviews.csv`, `calendar.csv` y
   `neighbourhoods.geojson` desde
   [insideairbnb.com/barcelona](https://insideairbnb.com/barcelona/)
   (snapshot 2026-06-24) en `data/airbnb_bcn/`.
2. Ejecutar `database/construir_base_datos.py` para construir
   `database/airbnb.db`.
3. Ejecutar los notebooks 01-05 en orden; el notebook 05 genera
   `data/airbnb_bcn_curado/` y las tablas `*_curado` en la base de datos.

## Hallazgo de apertura

**El 51,4% de los alojamientos presenta al menos una incidencia de calidad**
dentro de las dimensiones auditadas (licencia no verificable, precio ausente,
datos estructurales incompletos, o sin ninguna valoración). No es un problema
marginal, afecta a más de la mitad del inventario analizado.

## Resultado del modelo

Comparando el mismo algoritmo (RandomForest) entrenado con datos crudos vs.
tratados, sobre una muestra común de 426 filas que ningún modelo vio durante
su entrenamiento (sin fuga de datos), el modelo tratado predice **mejor**
que el crudo: R² sube de 0,347 a 0,450, y el MAE baja de 15.168 € a
14.343 €. Un chequeo de sensibilidad (probando un criterio de imputación
alternativo) confirma que la conclusión es estable y no depende de esa
decisión concreta de curación (diferencia menor al 0,1% en MAE). Detalle
completo en `notebooks/06_modelo_ml.ipynb` y en la app interactiva.

## Corrección metodológica aplicada

Tras una revisión a fondo del proyecto, se corrigieron dos variables usadas
en el caso de negocio y en el modelo, verificadas contra el diccionario de
datos oficial de Inside Airbnb:

- **"Anfitrión profesional" se mide con `calculated_host_listings_count`**
  (escala del anfitrión específicamente en Barcelona), no con
  `host_listings_count` (conteo global de toda la plataforma).
- **"Ingreso no estimable" se mide con `number_of_reviews_ltm`** (reseñas del
  último año, la misma ventana temporal que el target), no con
  `number_of_reviews` (histórico completo).

Ninguna corrección debilitó el hallazgo central del proyecto: comparando
anfitriones profesionales y particulares (dos grupos que ya existen hoy,
escalado solo como ayuda de intuición a un grupo ilustrativo de 50 anuncios),
el impacto de auditar pasó de 124.605 €/año a **149.958 €/año**. Detalle
completo en
`notebooks/05_tratamiento_curacion.ipynb` (sección 1.2 y 1.6) y en la ficha
maestra.

## Autora

Leidy Pimentel · IT Academy, Barcelona Activa / Cibernarium
