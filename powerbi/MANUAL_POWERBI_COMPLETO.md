# DataTrust en Power BI — manual completo de construcción

Este documento sustituye a `INSTRUCCIONES_POWER_BI.md` (la versión de 3 páginas): ahora son **7 páginas**, con narrativa completa problema → evidencia → investigación → comparación → robustez → conclusiones. Los fondos ya están generados en `powerbi/fondos/`. Los datos ya están exportados en `data/powerbi/`. Lo que queda es exclusivamente trabajo tuyo en Power BI Desktop (no tengo control de pantalla en esta sesión).

---

## A. Auditoría previa — qué se verificó y 3 correcciones importantes

Revisé el Streamlit completo, los 9 notebooks, los JSON de datos, `00_ficha_maestra.md` y los scripts Python de la raíz antes de escribir este manual. Tres cosas de tu encargo original **no coinciden** con lo ya verificado en este proyecto — las corrijo aquí para que no se cuele un número o una definición inconsistente con tu informe PDF, tu Streamlit o tus guiones:

1. **Anfitrión "profesional" NO es `host_listings_count > 50`.** Es `calculated_host_listings_count > 50` — confirmado contra los 3 notebooks (`host_listings_count` es un conteo global de toda la plataforma, no específico de Barcelona; usar esa columna cambiaría 478 anuncios de categoría y te daría una brecha de negocio distinta a la ya publicada en tu informe de 39,7%→23,1%). Usa `calculated_host_listings_count` en todo lo que construyas.
2. **Las categorías de licencia no son "46,9% HUTB / 25,7% Exempt / 19,9% Sin dato / 7,6% Otro".** Son: **47,04% HUTB · 25,66% Exento · 19,90% Sin dato · 6,20% NRUA (registro estatal nuevo) · 1,20% Otro/no clasificable**. Tu encargo fusionó NRUA dentro de "Otro" — y el hallazgo de que los profesionales adoptan el NRUA más rápido (65,7% vs. 18-25%) es uno de los más interesantes del proyecto, no lo pierdas.
3. **No existe un "Modelo C".** Busqué el origen de esa idea: hay una variable interna llamada `tabla_modelo_c` en el notebook 06, pero es solo el nombre de una tabla auxiliar para un cálculo (evaluar el modelo A sobre su propia población completa vs. solo sobre la población limpia) — no es un cuarto modelo entrenado. Los escenarios reales son: **A (crudo) · D (variables tratadas, misma población que A) · B (tratado) · chequeo de sensibilidad**. No construyas una página ni un visual para un "Modelo C".

Resultados que sí están suficientemente respaldados para presentar tal cual (ya usados en tu informe PDF y tu Streamlit, verificados contra JSON/notebooks): los 14 hallazgos de calidad, la brecha de negocio 39,7%→23,1% (149.958€/año en el caso ilustrativo de 50 anuncios), la fuga de datos del 80%, los R² de la muestra de 426 (0,348/0,388/0,448), la simulación de 5.000 submuestras (percentil 1,2) y el bootstrap (IC 95% de A-B no incluye el cero).

Lo que confirmé que SÍ existe y es correcto en tu encargo: `database/airbnb.db` (SQLite, 1,1GB) y `database/construir_base_datos.py` existen de verdad. No los uses para importar a Power BI — son demasiado pesados y los datos ya curados están en `data/powerbi/` en Parquet, mucho más ligero.

Lo que falta y no debe inventarse: no hay datos de reservas/ingresos reales (todo `estimated_revenue_l365d` es una estimación de Inside Airbnb), y no hay evidencia de que un inversor real haya usado estos datos para decidir — esto ya está bien manejado en tu Streamlit y debe mantenerse igual de cauto en Power BI (ver página 7).

---

## B. Guion completo — 7 páginas

| # | Página | Objetivo narrativo | Mensaje principal |
|---|---|---|---|
| 1 | Portada | Situar el tema y la pregunta de investigación | DataTrust audita si la calidad de los datos cambia decisiones reales |
| 2 | Contexto y auditoría de calidad | Mostrar la escala de los datos y qué se encontró | 14 hallazgos en 3 tablas, con prioridad y decisión documentadas |
| 3 | El hallazgo crítico | Explicar por qué "0€" no siempre es cero | 2.686 casos cambian la brecha de negocio de 39,7% a 23,1% |
| 4 | Diseño experimental | Explicar cómo se aísla población de variables | 4 versiones, 3 comparaciones, para no confundir causas |
| 5 | La fuga de datos y los resultados | Mostrar el rigor metodológico y la comparación válida | Una comparación ingenua engaña (R²≈0,82); la correcta usa 426 filas seguras |
| 6 | Robustez | Cuantificar cuánta confianza hay en el resultado | El efecto combinado A-B se distingue de cero; los parciales no |
| 7 | Conclusiones | Cerrar con honestidad sobre qué se demostró y qué no | Riesgo analítico medible, no una decisión empresarial ya demostrada como errónea |

Transición entre páginas (para tu guion oral, ver bloque E): cada página termina con una frase puente hacia la siguiente — ya están integradas en el guion oral de abajo, no hace falta que las inventes en el momento.

---

## C. Manual de construcción — paso a paso por página

### Preparación común (hazlo una sola vez)

1. **Importar datos — solo esto, nada más** (corregido: una versión anterior de este manual se contradecía a sí misma sobre si cargar `reviews`/`calendar`; la respuesta es no, ninguno de los visuales del manual los usa):
   - **1 Parquet**: Obtener datos → Parquet → pega la ruta completa (el conector pide URL/ruta en un campo de texto, no un explorador de archivos): `...\data\powerbi\listings.parquet` — es el único Parquet que necesitas, solo para la medida `Anuncios Auditados` de la página 2.
   - **7 CSV**: Obtener datos → Texto o CSV (aquí sí explorador de Windows — pega la ruta en el campo "Nombre de archivo") para cada uno:
     - `...\data\powerbi\resumen_kpis.csv`
     - `...\data\powerbi\licencia_por_distrito.csv`
     - `...\data\powerbi\hallazgos_14.csv`
     - `...\data\powerbi\impacto_particular_profesional.csv`
     - `...\data\powerbi\modelo_r2_comparaciones.csv`
     - `...\data\powerbi\simulacion_5000_diffs.csv`
     - `...\data\powerbi\bootstrap_intervalos.csv`
   - **No importes** `reviews.parquet`, `calendar.parquet` ni `database/airbnb.db` — ningún visual de este manual los necesita, y solo añaden peso y tiempo de carga al `.pbix`.

2. **No hace falta ninguna transformación de Power Query** más allá de la carga estándar — todas las tablas ya vienen en el formato exacto que necesita cada visual (formato "largo", una fila por combinación de categoría). Esto es deliberado: las estadísticas complejas (fuga de datos, bootstrap, submuestras) ya están calculadas y verificadas en Python; reproducirlas en DAX sería trabajo innecesario y un riesgo real de que te salga un número distinto al de tu informe.

3. **No hace falta ninguna relación entre tablas** para esta presentación — cada visual usa una sola tabla. Si Power BI te propone autodetectar relaciones entre `listings`/`reviews`/`calendar` por columnas con nombre parecido, puedes ignorarlo o desactivarlo (Modelado → Administrar relaciones), no afecta a ningún visual de este manual.

4. **Una única medida DAX** en todo el informe — créala sobre la tabla `listings`:
```dax
Anuncios Auditados = COUNTROWS(listings)
```

5. **Tamaño de página**: en cada una de las 7 páginas, panel Formato → Página → tamaño personalizado → **1280 × 720 px**.

6. **Fondo de página**: panel Formato → Fondo de página → Agregar imagen → el PNG de esa página en `powerbi/fondos/` → Ajuste: **Ajustar** → Transparencia **0%**.

7. **Cada visual que montes**: después de crearlo, panel Formato → General → Propiedades → mete los **X / Y / Ancho / Alto** exactos de las tablas de abajo. Y en Efectos → Fondo del visual, transparencia al 100% (para que se mezcle con la tarjeta blanca ya dibujada).

---

### Página 1 — Portada
**Fondo**: `pagina1_portada.png`. **Nada que montar** — es texto fijo. Cero visuales nativos en esta página.

---

### Página 2 — Contexto y auditoría de calidad
**Fondo**: `pagina2_auditoria.png`.

| Visual | Tipo | X,Y,Ancho,Alto | Campos | Filtro de visual |
|---|---|---|---|---|
| Anuncios auditados | Tarjeta | 40,104,380,92 | Medida `Anuncios Auditados` | — |
| Hallazgos encontrados | Tarjeta | 450,104,380,92 | `resumen_kpis[valor]` | `etiqueta = "hallazgos_totales"` |
| Tablas auditadas | Tarjeta | 860,104,380,92 | `resumen_kpis[valor]` | `etiqueta = "tablas_auditadas"` |
| % problema de licencia por distrito | Barras horizontales | 40,232,760,436 | Eje: `licencia_por_distrito[distrito]` · Valor: `[pct_problema]` | ordena el eje por `pct_problema` descendente (clic derecho en el eje → Ordenar por) |
| Hallazgos por dimensión | Columnas agrupadas | 820,232,420,436 | Eje: `resumen_kpis[etiqueta]` · Valor: `[valor]` | `etiqueta` en `{hallazgos_completitud, hallazgos_integridad, hallazgos_plausibilidad}` |

**Interacción entre visuales**: deja la interacción cruzada por defecto (clic en una barra del gráfico de distrito no necesita filtrar nada más en esta página) — no añadas slicers, esto es para proyectar, no para explorar en vivo.

**Tabla de detalle opcional**: si quieres un drill-down de los 14 hallazgos completos (no obligatorio para la narrativa de 20-30 min), añade una Tabla con `hallazgos_14` (columnas `id`, `tabla`, `resumen`, `decision_gobernanza`) escondida detrás de un botón "Ver detalle" — solo si te sobra tiempo de montaje.

---

### Página 3 — El hallazgo crítico
**Fondo**: `pagina3_hallazgo_critico.png`.

| Visual | Tipo | X,Y,Ancho,Alto | Campos | Filtro de visual |
|---|---|---|---|---|
| 2.686 casos no estimables | Tarjeta | 40,100,300,88 | `resumen_kpis[valor]` | `etiqueta = "casos_no_estimables"` |
| Brecha de ingresos (barras agrupadas) | Columnas agrupadas | 40,238,1200,300 | Eje: `impacto_particular_profesional[momento]` · Leyenda: `[tipo_anfitrion]` · Valor: `[ingreso_medio_eur]` | — |
| Brecha sin auditar | Tarjeta | 40,566,580,88 | `resumen_kpis[valor]` | `etiqueta = "gap_sin_auditar_pct"` |
| Brecha auditada | Tarjeta | 660,566,580,88 | `resumen_kpis[valor]` | `etiqueta = "gap_auditado_pct"` |

**Formato del gráfico de barras agrupadas**: Formato → Colores de datos → fija manualmente "Sin auditar" en `#D03B3B` (rojo, tu color de "crudo/problema") y "Auditado" en `#0CA30C` (verde, tu color de "tratado") — así coincide exactamente con la paleta que ya usas en Streamlit y en el informe PDF.

**El texto de la fórmula** ("¿De dónde sale el 0€?") ya está dibujado en el fondo, no es un visual — no intentes montar nada ahí.

---

### Página 4 — Diseño experimental
**Fondo**: `pagina4_diseno_experimental.png`. **Nada que montar** — las 4 tarjetas de versiones y sus "n filas" son texto fijo (no cambian, no necesitan ser "en vivo"). Cero visuales nativos en esta página.

---

### Página 5 — La fuga de datos y los resultados
**Fondo**: `pagina5_fuga_resultados.png`.

| Visual | Tipo | X,Y,Ancho,Alto | Campos | Filtro de visual |
|---|---|---|---|---|
| R² por versión (propia población) | Columnas | 40,238,580,400 | Eje: `modelo_r2_comparaciones[version]` · Valor: `[r2]` | `grupo_comparacion = "propia_poblacion"` |
| R² sobre muestra de 426 (sin fuga) | Columnas | 660,238,580,400 | Eje: `[version]` · Valor: `[r2]` | `grupo_comparacion = "muestra_426_sin_fuga"` |

**Formato**: en ambos gráficos, colores por categoría: A=`#D03B3B`, D=`#5C7A99`, B=`#0CA30C`, Sensibilidad=`#C98A1B` (mismos colores que usas en Streamlit para estas 4 versiones — clic derecho sobre cada barra → asignar color, o Formato → Colores de datos).

**Eje Y**: fija el mismo rango (0 a 0,5) en ambos gráficos (Formato → Eje Y → Mínimo 0, Máximo 0,5) para que la comparación visual entre "antes de corregir la fuga" y "después" sea honesta — si Power BI autoescala cada gráfico distinto, puede exagerar o esconder la diferencia real.

---

### Página 6 — Robustez
**Fondo**: `pagina6_robustez.png`.

| Visual | Tipo | X,Y,Ancho,Alto | Campos |
|---|---|---|---|
| Distribución de las 5.000 submuestras | Histograma | 40,160,700,340 | `simulacion_5000_diffs[diferencia_r2_a_menos_d]` |
| Percentil del resultado real | Tarjeta | 760,160,480,160 | `resumen_kpis[valor]` filtro `etiqueta = "percentil_resultado_real"` |
| Intervalos de confianza (bootstrap) | Tabla | 40,560,1200,116 | `bootstrap_intervalos[comparacion]`, `[diferencia_media]`, `[ic95_inferior]`, `[ic95_superior]` |

**Sobre el histograma**: Power BI no trae un visual de histograma 100% nativo en el panel por defecto, pero Microsoft publica uno gratuito y certificado. Insertar → Obtener más visuales (o el icono "..." en el panel Visualizaciones) → busca **"Histogram"** → el de Microsoft Corporation → Agregar. Úsalo con el campo de arriba. Si tu organización bloquea AppSource y no puedes instalarlo, alternativa de respaldo: añade una columna calculada en Power Query que agrupe `diferencia_r2_a_menos_d` en bins de 0,01 — usa **suelo, no redondeo**, para que cada bin represente de verdad el intervalo `[inicio, inicio+0,01)` en vez de "el valor más cercano a X": `= Number.RoundDown([diferencia_r2_a_menos_d] / 0.01, 0) * 0.01`. Con `Number.Round` (redondeo) un valor justo en el borde de un bin podría caer en el bin equivocado; con `Number.RoundDown` (suelo) no.

**Línea de referencia en el histograma**: añade dónde cae el resultado real observado (-0,0405) dentro de la distribución — así se ve de un vistazo que es un caso extremo (percentil 1,2), no solo se lee en la tarjeta de al lado. En el visual del histograma, panel Formato → **Analítica** → **Línea constante** → Agregar → valor `-0.0405` → nombre "Resultado real observado" → color `#D03B3B` (rojo, tu color de alerta) → línea discontinua para que se distinga de las barras.

**Sobre la tabla del bootstrap**: añade formato condicional a la columna `incluye_cero` (clic derecho en la columna dentro del visual → Formato condicional → Color de fondo → regla: si el valor es `TRUE` color ámbar `#FFF8EC`, si es `FALSE` color verde `#E7F6E7`) — así se ve de un vistazo cuál de las 3 comparaciones es la concluyente (A-B) sin que tengas que explicarlo con texto extra.

---

### Página 7 — Conclusiones
**Fondo**: `pagina7_conclusiones.png`. **Nada que montar** — las 4 filas de certeza, la recomendación y la caja de advertencia son texto fijo, igual que en tu Streamlit. Cero visuales nativos en esta página.

---

### Navegación entre páginas

Dado que es para proyectar ante 20 personas (no para que ellos interactúen), **no añadas slicers ni filtros visibles**. Lo único recomendable: en cada página, un botón pequeño de "Página siguiente" en la esquina inferior derecha (Insertar → Botones → Navegación de página → Siguiente página), o simplemente usa las flechas del teclado en modo Presentación (F5 o Ctrl+Mayús+F) — Power BI ya navega con las flechas por defecto, no necesitas botones si vas a controlar tú el ratón/teclado durante la defensa.

---

## D. Preparación de los datos — ya hecha, resumen de qué contiene cada archivo

| Archivo | Filas | Columnas | Para qué página |
|---|---|---|---|
| `listings.parquet` | 15.293 | curadas | Página 2 (medida Anuncios Auditados) — **único Parquet a importar** |
| `resumen_kpis.csv` | 25 | `seccion, etiqueta, valor, nota` | 2, 3, 6 (todas las tarjetas) |
| `licencia_por_distrito.csv` | 10 | `distrito, pct_problema, n_anuncios` | 2 |
| `hallazgos_14.csv` | 14 | `id, tabla, resumen, decision_gobernanza, prioridad` | 2 (tabla de detalle opcional) |
| `impacto_particular_profesional.csv` | 4 | `tipo_anfitrion, momento, ingreso_medio_eur` | 3 |
| `modelo_r2_comparaciones.csv` | 11 | `grupo_comparacion, version, r2, mae_eur, n_test` | 5 |
| `simulacion_5000_diffs.csv` | 5.000 | `n_submuestra, diferencia_r2_a_menos_d` | 6 |
| `bootstrap_intervalos.csv` | 3 | `comparacion, diferencia_media, ic95_inferior, ic95_superior, incluye_cero` | 6 |

Si en algún momento decides ampliar la presentación con algo de `reviews` o `calendar` (no está en este guion), entonces sí los importarías — pero para las 7 páginas de este manual, no hace falta.

---

## E. Guion oral — qué decir en cada página

**Página 1.** "Mi proyecto parte de una pregunta: ¿puede la calidad de los datos cambiar las conclusiones de un análisis, incluso cuando los datos parecen completos y el modelo ofrece buenas métricas? Lo investigo con datos reales de Airbnb Barcelona."

**Página 2.** "Audité tres tablas —15.293 anuncios, más de un millón de reseñas, 5,6 millones de filas de calendario— contra tres dimensiones de calidad. Encontré 14 hallazgos. El más visible: el campo de licencia mezcla dos sistemas de registro distintos, y un 21% no es verificable, con bastante variación según el distrito." *(Transición: "Pero el hallazgo de mayor impacto no está en la auditoría de licencias — está en un campo que parecía perfectamente numérico.")*

**Página 3.** "`estimated_revenue_l365d` es el ingreso anual que estima Inside Airbnb. Encontré 2.686 anuncios con ese valor en cero — pero no es un cero real, es un fallo estructural de la fórmula cuando un anuncio no tiene reseñas recientes y tiene estancia larga. Si no lo investigas, la brecha de ingresos entre anfitriones particulares y profesionales parece del 39,7%. Si lo investigas, es del 23,1% — casi diecisiete puntos de diferencia solo por entender bien un campo." *(Transición: "Para comprobar si esto también afecta a un modelo predictivo, diseñé un experimento con cuatro versiones de los datos.")*

**Página 4.** "Entrené el mismo Random Forest bajo cuatro versiones, separando deliberadamente el efecto de qué población se usa del efecto de cómo se construyen las variables — A y D comparten población, B cambia ambas cosas a la vez, y hay un chequeo de sensibilidad para comprobar que el criterio de imputación elegido no es arbitrario." *(Transición: "Antes de comparar estos modelos, encontré y corregí un problema serio en mi propio diseño.")*

**Página 5.** "Un primer intento de comparación dio un R² sospechosamente alto, de 0,82. Investigué por qué: el 80% de las filas de test de uno de los modelos ya habían sido vistas en el entrenamiento de los otros. Lo corregí usando solo una muestra de 426 filas verdaderamente seguras. Con esa muestra, la comparación válida muestra una mejora clara del modelo tratado." *(Transición: "Pero 426 filas es una muestra pequeña — así que investigué cuánta confianza puedo tener en ese resultado.")*

**Página 6.** "Hice dos cosas: simulé 5.000 submuestras distintas del mismo tamaño, y el resultado real cae en un percentil poco habitual, el 1,2. Y con un bootstrap de 5.000 repeticiones, la mejora combinada del modelo tratado se distingue estadísticamente de cero — pero no puedo repartir con precisión cuánto viene de la población y cuánto de las variables por separado, con esta muestra." *(Transición: "Para cerrar, quiero ser muy clara sobre qué he demostrado y qué no.")*

**Página 7.** "Reúno todo en cuatro niveles de certeza, del más al menos demostrado. Y quiero remarcar algo: no afirmo que Airbnb o un anfitrión real tomaran una decisión equivocada — no tengo esos datos. Lo que demuestro es un riesgo analítico medible: tomar decisiones sobre datos sin auditar es arriesgado, y en este caso, ese riesgo se puede cuantificar."

### Qué debo recordar que el público se lleve
Que "cero" en un dataset no siempre significa cero real, y que esa confusión cambia tanto una decisión humana de negocio como el resultado de un modelo automatizado — el mismo hallazgo, aplicado a dos tipos de decisión distintos.

### Preguntas técnicas probables (resumidas — el detalle completo con más preguntas está en `guion_presentacion_completo.md`, en la raíz del proyecto)
- *¿Por qué no hay Modelo C?* — No existe como escenario formal; es una confusión con una tabla auxiliar interna del notebook. Los escenarios reales son A, D, B y el chequeo de sensibilidad.
- *¿Por qué calculated_host_listings_count y no host_listings_count?* — Porque el segundo es un conteo global de toda la plataforma, no específico de Barcelona; usar el correcto es lo que sostiene la cifra de 39,7%→23,1% en todos mis entregables.
- *¿Qué es NRUA?* — El nuevo registro estatal de alquileres de corta duración, obligatorio desde julio de 2025, que convive con el HUTB catalán.
- *¿Por qué el R² sube de 0,82 a algo mucho más bajo?* — El 0,82 inicial tenía fuga de datos (filas de test ya vistas en entrenamiento); el número real, sin fuga, es más bajo pero honesto.
- *¿Cómo sabes que esos ceros no son ingresos reales? ¿Eso lo dice Inside Airbnb o lo infieres tú de los datos?* — Hay que separar dos cosas. Que 0 reseñas produce ocupación 0 y por tanto ingreso 0 **sí lo dice la metodología publicada por Inside Airbnb** (insideairbnb.com/data-assumptions): la fórmula es reseñas ÷ tasa de conversión del 50% × duración de estancia; reseñas está en el numerador, así que si reseñas=0, ocupación=0 por construcción matemática de su propia fórmula, no por un patrón que yo haya visto en los datos. Lo de `ingreso = ocupación × precio` lo verifiqué empíricamente contra todo el dataset (coincide con un error menor a 0,0001). Lo que **sí es una decisión propia del proyecto**, no un hecho de Inside Airbnb, es el criterio adicional "Y estancia ≥28 noches" para decidir qué ceros marcar como no estimables — se basa en que los huéspedes de estancia larga reseñan menos, una hipótesis razonable pero no demostrada por la fuente.

  **Respuesta corta para decir ante el tribunal**: *"Inside Airbnb estima la ocupación a partir de las reseñas recibidas durante los últimos 365 días. Por tanto, cuando no hay reseñas, la fórmula produce una ocupación estimada de cero y, en consecuencia, unos ingresos estimados de cero. Esto no demuestra que el alojamiento no haya generado ingresos, sino que la metodología no dispone de reseñas para estimarlos. En nuestro proyecto identificamos un subconjunto de estos casos con estancia mínima de 28 noches. Consideramos que es un patrón compatible con una menor capacidad de estimación de la fórmula, pero lo tratamos como una hipótesis de análisis, no como un hecho demostrado."*

### Limitaciones que debo reconocer si me preguntan
`estimated_revenue_l365d` es una estimación de terceros, no ingreso real observado; la muestra sin fuga es de solo 426 filas; el experimento cubre un único dataset y un único algoritmo; no hay evidencia de que un inversor real haya usado estos datos para decidir.

---

## F. Checklist final

**Técnico**
- [ ] Las 8 tablas/archivos cargados (1 Parquet `listings` + 7 CSV) — `reviews.parquet`, `calendar.parquet` y `database/airbnb.db` NO se importan, ningún visual los usa.
- [ ] La medida `Anuncios Auditados` creada y funcionando en la tarjeta de la página 2.
- [ ] Las 7 páginas con tamaño de página 1280×720 y el fondo correcto asignado (sin transparencia).
- [ ] Cada visual con sus X/Y/Ancho/Alto exactos (no a ojo) y fondo del visual transparente.
- [ ] Filtros de visual aplicados correctamente en las tarjetas que usan `resumen_kpis` (una etiqueta por tarjeta, no toda la tabla).
- [ ] Colores de las versiones A/D/B/Sensibilidad consistentes en páginas 3 y 5 (mismos hex que en Streamlit).

**Visual**
- [ ] Ninguna etiqueta de texto se solapa con otra (ya verificado en los PNG de fondo, pero revisa tras montar los visuales reales encima).
- [ ] El eje Y de los dos gráficos de R² en la página 5 tiene el mismo rango (0–0,5).
- [ ] La tabla de bootstrap en la página 6 tiene el formato condicional en `incluye_cero`.

**Validación de cifras (cross-check contra tu informe PDF y Streamlit, no deberían diferir)**
- [ ] Brecha: 39,7% → 23,1% (149.958€/año).
- [ ] R² muestra de 426: 0,348 / 0,388 / 0,448.
- [ ] Fuga: 80% (1.708 de 2.134).
- [ ] Percentil: 1,2. Bootstrap A-B: IC95% no incluye el cero.
- [ ] Hallazgos: 14 totales (8 listings, 4 reviews, 2 calendar).

**Preparación para presentar**
- [ ] Ensayado el guion oral de la sección E en voz alta, con cronómetro.
- [ ] Exportado a PDF (Archivo → Exportar a → Exportar a PDF) — entregable oficial del Sprint 13, guardar en `report/`.
- [ ] Revisadas las 7 páginas del PDF exportado, sin recortes ni elementos tapados.
- [ ] Modo Presentación probado una vez de principio a fin (F5 o Ctrl+Mayús+F) antes del día de la defensa.
