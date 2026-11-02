> **OBSOLETO** — sustituido por `MANUAL_POWERBI_COMPLETO.md` (versión de 7 páginas, narrativa completa). Se deja este archivo solo como referencia histórica de la primera versión (3 páginas); no lo sigas para montar el `.pbix`.

# Cómo montar el .pbix con estos fondos

Esto es la parte que tienes que hacer tú en Power BI Desktop (no tengo control de pantalla en esta sesión, así que no puedo hacerlo por ti). Son 3 páginas. Sigue el orden.

## 0. Datos a importar (Obtener datos → Carpeta / Texto-CSV)

- `data/powerbi/listings.parquet`, `reviews.parquet`, `calendar.parquet` — las tablas principales, ya curadas.
- `data/powerbi/resumen_kpis.csv` — tabla pequeña con los KPIs ya calculados en Python (brecha de negocio, R² del modelo, conteos de hallazgos). **No intentes recalcular estos números dentro de Power BI** — la lógica de `revenue_no_estimable` (0 reseñas último año Y estancia ≥28 noches) y la comparación de modelos sin fuga de datos ya están verificadas en los notebooks; replicarlas en DAX es trabajo innecesario y arriesga introducir un número distinto al de tu informe y tu Streamlit. Usa esta tabla tal cual.
- `data/powerbi/licencia_por_distrito.csv` — para el mapa/barras de la página 2.

## 1. Configurar el tamaño de página (hazlo una vez, en la primera página, y repítelo en las 3)

Panel Formato → **Página** → Tamaño personalizado → **Ancho 1280 px, Alto 720 px** (tipo "16:9", pero puesto a mano para que coincida exacto con las imágenes).

## 2. Poner el fondo en cada página

Panel Formato → **Fondo de página** → Agregar imagen → selecciona el PNG de esa página (están en `powerbi/fondos/`) → **Ajuste de imagen: Ajustar** (fit, no "Normal" ni "Mosaico") → Transparencia: **0%**.

- Página 1 → `pagina1_portada.png`
- Página 2 → `pagina2_auditoria.png`
- Página 3 → `pagina3_impacto.png`

## 3. Colocar los visuales reales encima

Para cada visual: después de crearlo, panel Formato → **General** → **Propiedades** → ahí están los campos **X, Y, Ancho, Alto** en píxeles — mete los números exactos de abajo, no los muevas a ojo. Y en **Efectos → Fondo del visual**, pon la transparencia al 100% (o quita el fondo) para que el visual se mezcle con la tarjeta blanca ya dibujada en la imagen de fondo.

### Página 1 — Portada
Nada que montar. Es la imagen completa. (Opcional, si quieres: un botón de navegación a la página 2, pero no es necesario para el entregable.)

### Página 2 — Auditoría: alcance y hallazgos

| Visual | Tipo | X | Y | Ancho | Alto | Campos |
|---|---|---|---|---|---|---|
| Anuncios auditados | Tarjeta (Card) | 40 | 104 | 380 | 92 | Medida nueva: `Anuncios Auditados = COUNTROWS(listings)` |
| Hallazgos encontrados | Tarjeta | 450 | 104 | 380 | 92 | Campo `resumen_kpis[valor]`, filtro de visual: `etiqueta = "hallazgos_totales"` |
| Tablas auditadas | Tarjeta | 860 | 104 | 380 | 92 | Campo `resumen_kpis[valor]`, filtro de visual: `etiqueta = "tablas_auditadas"` |
| % problema de licencia por distrito | Barras horizontales (o Mapa de formas si te animas) | 40 | 232 | 760 | 436 | Eje: `licencia_por_distrito[distrito]` (ordenado por `pct_problema` descendente) · Valor: `licencia_por_distrito[pct_problema]` |
| Hallazgos por dimensión | Columnas agrupadas | 820 | 232 | 420 | 436 | Eje: `resumen_kpis[etiqueta]` · Valor: `resumen_kpis[valor]` · filtro de visual: `etiqueta` en `{hallazgos_completitud, hallazgos_integridad, hallazgos_plausibilidad}` |

**Sobre el mapa por distrito**: un mapa coroplético real de Barcelona (Shape Map) exige importar un GeoJSON de barrios como visual personalizado — es más trabajo de montaje y más frágil el día de la defensa si algo no carga. Mi recomendación: usa barras horizontales ordenadas (mismo mensaje, mucho más fiable). Si quieres el mapa de verdad, dímelo y te preparo el GeoJSON recortado para importar como Shape Map.

### Página 3 — Impacto en negocio y en el modelo

| Visual | Tipo | X | Y | Ancho | Alto | Campos |
|---|---|---|---|---|---|---|
| Brecha de ingresos (barras agrupadas) | Columnas agrupadas | 40 | 128 | 580 | 330 | Necesita datos "largos": ver nota abajo |
| Brecha sin auditar | Tarjeta | 40 | 500 | 280 | 90 | `resumen_kpis[valor]` filtro `etiqueta = "gap_sin_auditar_pct"` |
| Brecha auditada | Tarjeta | 340 | 500 | 280 | 90 | `resumen_kpis[valor]` filtro `etiqueta = "gap_auditado_pct"` |
| R² por versión del modelo | Columnas | 660 | 128 | 580 | 490 | Eje: `etiqueta` · Valor: `valor` · filtro `etiqueta` en `{r2_a_crudo, r2_d_variables, r2_b_tratado}` |

**Nota sobre el gráfico de barras agrupadas de brecha**: `resumen_kpis.csv` tiene las 4 cifras (particular/profesional × sin auditar/auditado) como filas sueltas, no en formato "ancho" ideal para un gráfico agrupado con dos ejes (tipo de anfitrión y momento). Si Power BI te lo pone difícil con esas 4 filas sueltas, dime y te preparo una tabla aparte ya en el formato correcto (`anfitrion, momento, euros`) — es un cambio de 2 minutos de mi parte, mejor que pelear con DAX para pivotarlo.

## 4. Exportar a PDF (el entregable oficial)

Archivo → Exportar a → **Exportar a PDF**. Revisa que las 3 páginas salgan completas y sin recortes antes de guardarlo en `report/` junto al informe.

## 5. Si usaste alguna fórmula DAX más allá de las medidas simples de arriba

El enunciado pide un documento aparte explicando las fórmulas DAX si usaste alguna. Las de esta guía (`COUNTROWS`, filtros de visual) son tan simples que probablemente no haga falta, pero si añades algo más complejo, avísame y te preparo ese documento.
