# DataTrust

Auditoría de calidad y gobernanza de datos aplicada a un caso real de alquiler
turístico en Barcelona.

## Pregunta central

¿Cómo afectan los problemas de calidad, consistencia e integridad de los datos a
las conclusiones de negocio y al rendimiento de un modelo predictivo, en un caso
real de alquiler turístico en Barcelona?

## Objetivos

1. Auditar la calidad de los datos (`listings`, `reviews`, `calendar`).
2. Identificar y priorizar los problemas encontrados según su impacto.
3. Aplicar un proceso de curación documentado y justificado.
4. Comparar las conclusiones de negocio antes y después del tratamiento.
5. Comparar el rendimiento de un modelo predictivo antes y después del tratamiento.

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
├── data/airbnb_bcn/             ← datos originales (CSV) de Inside Airbnb
├── data/airbnb_bcn_curado/      ← datos curados (CSV), generados por el notebook 05
├── database/airbnb.db           ← tablas raw + tablas _curado en SQLite
├── notebooks/
│   ├── 01_auditoria_listings.ipynb       ← auditoría de alojamientos (completado)
│   ├── 02_auditoria_reviews.ipynb        ← auditoría de reseñas (completado)
│   ├── 03_auditoria_calendar.ipynb       ← auditoría de calendario (completado)
│   ├── 04_recomendaciones_gobernanza.ipynb  ← 14 hallazgos priorizados (completado)
│   ├── 05_tratamiento_curacion.ipynb     ← curación ejecutada en código (completado)
│   └── 06_modelo_ml.ipynb                ← modelo original vs. tratado (pendiente)
├── report/                      ← informe final en PDF (pendiente)
└── slides/                      ← presentación de 30 minutos (pendiente)
```

Se recomienda abrir los notebooks en orden numérico, cada uno documenta sus
hallazgos con el código que los produce, no solo en texto.

## Hallazgo de apertura

**El 53,4% de los alojamientos presenta al menos una incidencia de calidad**
dentro de las dimensiones auditadas (licencia no verificable, precio ausente,
datos estructurales incompletos, o sin ninguna valoración). No es un problema
marginal, afecta a más de la mitad del inventario analizado.

## Autora

Leidy Pimentel · IT Academy, Barcelona Activa / Cibernarium
