# Ficha maestra del proyecto final

Documento de referencia para empezar a construir. Todo lo que aquí aparece ya fue
verificado con datos reales (no son suposiciones), usando los scripts en esta misma
carpeta (`explore_airbnb_bcn.py`, `explore_airbnb_calendar.py`,
`check_impacto_preliminar.py`, `check_impacto_negocio_profesional.py`). Los
scripts de exploración de datasets descartados (`explore_olist.py`,
`explore_accidents_bcn.py`) se eliminaron de la carpeta tras cerrar
definitivamente el tema del proyecto en Airbnb Barcelona.

## Especificaciones oficiales del Sprint 13 / Proyecto Final (fuente prioritaria)

Traducido del catalán, texto original de la plataforma del curso (Tasca S13.01.
Projecte final). **Esta sección manda sobre cualquier otra guía de este
documento basada en lecturas externas** — donde haya conflicto (ej. límite de
páginas, estructura de entregables), prevalece lo de aquí.

**Entregables obligatorios**:

1. **Informe del proyecto final en PDF, máximo 4 páginas.** Estructura
   obligatoria:
   - **Título**: visión clara y concisa del tema del estudio, específico y
     descriptivo.
   - **Resumen (máximo 250 palabras)**: propósito, metodología, resultados
     principales y conclusiones.
   - **Introducción**: contexto y propósito del estudio, su relevancia e
     importancia; debe formular claramente el problema de investigación y los
     objetivos del estudio.
   - **Metodología**: cómo se realizó el estudio, incluyendo el diseño de la
     investigación, descripción de los registros/datos trabajados, y
     herramientas y técnicas usadas para analizar los datos.
   - **Resultados**: hallazgos del estudio de forma clara y sistemática,
     normalmente respaldados por tablas, figuras y estadísticas, **sin
     interpretar los datos ni sacar conclusiones** (coincide exactamente con
     lo ya decidido más abajo: Resultados ≠ Discusión).
   - **Discusión**: interpretar los resultados, explicando cómo respaldan,
     refutan o amplían hallazgos de otros estudios; discutir las
     implicaciones de los resultados; se pueden plantear nuevas hipótesis o
     sugerir áreas de investigación futura. **Debe quedar explícito qué
     aportación se hace para la toma de decisiones empresariales** (en este
     proyecto: el caso de los 149.958 €/año de diferencia entre decidir con
     datos crudos o auditados debe estar nombrado aquí sin ambigüedad).
   - **Conclusión**: resume los hallazgos principales y su importancia,
     destacando cómo contribuyen al campo de estudio; puede incluir
     recomendaciones prácticas o sugerencias futuras.
   - **Referencias bibliográficas en formato APA.**
2. **Conjuntos de datos utilizados para trabajar en Power BI** (no solo el
   dashboard, los datos en sí — esto son los CSV curados de
   `data/airbnb_bcn_curado/`, generados por el notebook 05).
3. **El `.pbix` exportado como PDF.** Si se usan fórmulas DAX, documento
   aparte explicándolas.
4. **Documento con la presentación** a usar en la defensa del proyecto final.

**Aspectos importantes a tener en cuenta** (según el enunciado oficial):

- Nomenclatura consistente de archivos y carpetas, para facilitar la revisión.
- **Presentar el trabajo final como si fuera un artículo científico**, con
  todas las secciones correspondientes y su descripción correcta (justifica
  por qué se investigó la estructura de artículo científico en las lecturas
  de más abajo — no era una suposición nuestra, lo pedía el enunciado).
- Establecer un objetivo claro.
- Seleccionar correctamente qué visualización mostrar, junto a su correcta
  interpretación.
- Realizar un análisis crítico de los resultados, considerando limitaciones,
  implicaciones y posibles sesgos.
- Documentos que cumplan con el estilo APA.

**Objetivos del Sprint 13** (objetivos de aprendizaje del curso que esta
tarea evalúa, distintos de los 5 objetivos propios del proyecto definidos más
abajo en "Objetivos (5, sin ampliar)"):

- Integración efectiva de tecnologías y metodologías específicas del análisis
  de datos, para la extracción, limpieza, análisis, modelado y visualización
  de datos.
- Gestionar datos, identificar patrones y extraer insights valiosos que den
  soporte a la toma de decisiones.
- Desarrollar habilidades comunicativas para presentar los hallazgos de
  manera clara y eficaz a públicos variados.
- Ejercitar la creatividad, el pensamiento crítico y la habilidad para
  solucionar problemas complejos, aspectos fundamentales para un analista de
  datos de éxito en el mundo profesional.

**Entrega (Lliurament)** — texto oficial:

- **Almacenar en un repositorio de GitHub una carpeta con todos los
  documentos referidos al proyecto final.** Repite los 4 entregables ya
  listados arriba (informe PDF máx. 4 páginas, datasets usados en Power BI,
  `.pbix` exportado a PDF + documento DAX si hace falta, documento de la
  presentación).
- **En la entrega, se coloca el link al repositorio** — el entregable final
  es un enlace a GitHub, no archivos sueltos enviados por otro medio.

**Pendiente crítico detectado**: esta carpeta del proyecto **todavía no es un
repositorio git** (verificado: no hay `.git`, no hay remoto configurado). Hay
que inicializar el repo, crear uno en GitHub y subirlo antes de la entrega.
Punto a tener en cuenta al hacerlo: los CSV de `data/airbnb_bcn/` y
`data/airbnb_bcn_curado/` son grandes (cientos de MB en total, varios por
encima del límite de 100 MB por archivo de GitHub), así que subir `data/` tal
cual probablemente falle o infle el repo innecesariamente — hace falta
decidir estrategia (`.gitignore` sobre `data/` con instrucciones de descarga
en el README, Git LFS, o subir solo una muestra) antes de hacer el primer
commit.

**Evaluación**: una vez entregado el proyecto, se propone una fecha para la
defensa. La nota final se divide en **70% el documento entregado + 30% la
defensa**. Es necesario aprobar las dos partes por separado para superar la
fase de proyecto. Con la entrega y defensa del proyecto finaliza el curso.

**Ajustes que esto obliga a hacer sobre lo ya planeado en este documento**:
- La estructura de informe definida más abajo en "Guía de redacción del
  informe y estilo" se mantiene, pero con el límite de 4 páginas, las
  secciones de **Agradecimientos y Apéndices no están en la lista oficial y
  probablemente no quepan** — se recomienda eliminarlas o reducirlas a una
  sola línea si hace falta. La tabla completa de gobernanza (14 hallazgos) no
  cabe entera en 4 páginas: debe ir resumida/condensada en el informe, con el
  detalle completo quedando en el notebook 04 (que no tiene límite de
  páginas, es un entregable técnico aparte).
- Se añaden a "Entregables finales" (sección más abajo) los dos ítems nuevos:
  datasets usados en Power BI, y el `.pbix` exportado a PDF (+ documento DAX
  si aplica).

## Pregunta central

¿Cómo afectan los problemas de calidad, consistencia e integridad de los datos a las
conclusiones de negocio y al rendimiento de un modelo predictivo, en un caso real de
alquiler turístico en Barcelona?

## Dataset elegido: Airbnb Barcelona (Inside Airbnb)

- Fuente: https://insideairbnb.com/barcelona/ (snapshot 2026-06-24)
- Datos ya descargados en `data/airbnb_bcn/`: `listings.csv` (15.293 alojamientos, 90
  columnas), `reviews.csv` (1.033.523 reseñas), `calendar.csv` (5.623.190 filas,
  un registro por alojamiento y día), y `neighbourhoods.geojson` (75 barrios, límites
  geográficos, propiedades `neighbourhood`/`neighbourhood_group` compatibles con
  `neighbourhood_cleansed` de `listings`). Estas son las únicas 3 tablas de datos del
  proyecto (no hay una cuarta tabla oculta), el geojson es solo un archivo de mapas,
  no una tabla para auditar.
- **Uso del geojson**: mapa por barrio en el dashboard de Power BI (visual gratuito
  "Shape Map" o "Icon Map"), coloreado por rendimiento económico estimado o por score
  de calidad. No se usa Streamlit para esto, Streamlit se queda solo como demo
  opcional del modelo (ver sección "Extra opcional"), para no dispersar el alcance.
- Real, local (Barcelona), europeo, con licencia de uso abierta para este fin.
- Alternativas descartadas tras comparación con evidencia real: Olist (e-commerce
  Brasil, queda como plan B técnico), accidentes de tráfico de Open Data BCN
  (descartado por no tener variable de gravedad/desenlace de negocio), datasets de
  marketing/salud en Kaggle (descartados por ser sintéticos o muy repetidos en
  portafolios).

## Objetivos (5, sin ampliar)

1. Auditar la calidad de los datos (listings, calendar, reviews).
2. Identificar y priorizar los problemas encontrados según su impacto.
3. Aplicar un proceso de curación documentado y justificado (no "limpiar por limpiar").
4. Comparar las conclusiones de negocio antes y después del tratamiento.
5. Comparar el rendimiento de un modelo predictivo antes y después del tratamiento.

## Alcance cerrado (qué NO hacer)

- No seguir buscando datasets ni temas alternativos.
- No volver a cambiar la variable objetivo.
- No convertir `license` en variable objetivo del modelo (es un caso de gobernanza,
  no una prueba de legalidad real).
- No dejar que las reseñas sean el centro del proyecto, son una tabla más dentro de
  la auditoría.
- No construir cinco modelos distintos, uno solo, comparado antes/después.

## Hallazgos de calidad ya verificados (con cifras)

**Listings**
- 12 columnas con 100% de valores nulos (`host_since`, `host_response_rate`,
  `host_verifications`, `instant_bookable`, `neighborhood_overview`, entre otras),
  probable pérdida de fuente sin documentar.
- Codificación de caracteres rota en `neighbourhood_cleansed` (ej. "Sagrada Fam�lia").
- `price`: 12,7% nulos.
- `bedrooms`/`bathrooms`/`beds`: 16-23% nulos.

**Calendar**
- La columna `price` no existe en este snapshot (desapareció de la fuente).
- 41.245 filas con `listing_id` huérfano (no existe en `listings`).
- `maximum_nights = 1125` en 1.478.636 filas (26%), valor de relleno por defecto de
  la plataforma, no una decisión real del anfitrión.
- Sin nulos, sin duplicados por `listing_id`+`date`.

**Reviews**
- 6.592 reseñas con `listing_id` huérfano.
- 48.302 comentarios duplicados exactos.
- 609 casos del mismo `reviewer_id` con texto idéntico en alojamientos distintos.
- 9.917 reseñas con menos de 5 caracteres.

**License (caso estrella de gobernanza, no es el target)**
- 46,9% con número HUTB reconocible, 25,7% exento declarado, 19,9% sin dato, 7,6%
  texto no clasificable.
- 5.429 registros con DOS números HUTB concatenados en el mismo campo, con etiquetas
  HTML (`<br />`) sin limpiar.
- Los anfitriones profesionales (>50 propiedades) están sobrerrepresentados en la
  categoría "no clasificable" (54,9%) frente al resto (16-29%).
- Importante: un campo `license` mal formado NO equivale a "sin licencia real". Se
  audita como problema de calidad/formato, no se afirma incumplimiento legal.

## Traducción a impacto monetario (caso estrella de negocio)

Verificado con `check_impacto_negocio_profesional.py`. Responde directamente a la
pregunta de negocio sobre anfitriones profesionales vs. particulares, ya no solo
como correlación sino como una decisión real que cambia de resultado según se
audite o no el dato.

**Corrección metodológica (aplicada tras una revisión a fondo, no en el cálculo
original)**: se corrigieron dos variables en este análisis, ambas verificadas
contra el diccionario de datos oficial de Inside Airbnb antes de aplicarlas:

1. **"Anfitrión profesional" se mide con `calculated_host_listings_count`**
   (no `host_listings_count`). Según el diccionario oficial, `host_listings_count`
   es *"el número de anuncios que tiene el anfitrión, según los cálculos de
   Airbnb"* — un conteo **global de toda la plataforma**, no limitado a
   Barcelona. `calculated_host_listings_count` es *"el número de anuncios que
   tiene el anfitrión en el scrape actual, en la geografía de la ciudad/región"*
   — sin nulos (87 en la otra columna) y calculado directamente sobre este
   snapshot de Barcelona. Para un estudio específico de esta ciudad, es la
   columna correcta. Impacto del cambio: 478 anuncios (3,1%) cambian de
   clasificación, siempre en la misma dirección (anfitriones con muchos
   anuncios fuera de Barcelona dejan de contar como "profesional" aquí).
2. **"No estimable" se mide con `number_of_reviews_ltm`** (no
   `number_of_reviews`). El target (`estimated_revenue_l365d`) es una métrica
   de 1 año; la variable de control debe usar la misma ventana temporal
   (reseñas del **último año**, no el histórico completo del anuncio) para no
   comparar dos periodos distintos. Impacto del cambio: se capturan 791
   anuncios más como "no estimable" (2.686 en vez de 1.895, un 42% más).

**Ninguna de las dos correcciones debilita el hallazgo — lo fortalece** (ver
cifras abajo). Detalle completo de cómo se encontraron estas correcciones y la
comparación con la fuente oficial de Inside Airbnb: notebook 05, sección 1.2 y 1.6.

- **Conclusión con datos crudos (solo quitando nulos, sin investigar)**: los
  anfitriones profesionales (>50 anuncios en Barcelona) rinden un **39,7%** peor
  por anuncio que los particulares (24.338 € vs. 14.678 €/año de media).
- **Causa raíz encontrada**: el 54,2% de los anuncios profesionales tienen
  `estimated_revenue_l365d = 0`. Se confirma que esto es 100% mecánico: de esos
  ceros, el 100% tiene cero reseñas en el último año (`number_of_reviews_ltm = 0`;
  la fórmula de Inside Airbnb se basa exactamente en esas reseñas), y el 62,2%
  tiene estancia mínima ≥28 noches (frente a 26,1% en los profesionales con
  ingreso activo) — un huésped de estancia larga deja como mucho una reseña al
  año, así que la fórmula no puede estimar ingresos ahí aunque el alojamiento
  esté ocupado. Coincide con estancias de 31+ noches, que en Barcelona quedan
  fuera del régimen de licencia turística de corta estancia (conecta con el
  hallazgo de licencias de más arriba).
- **Decisión de gobernanza**: tratar como "no estimable" (no como ingreso real
  cero) solo los anuncios con esa doble evidencia (sin reseñas en el último año +
  estancia mínima ≥28 noches, un **20,1%** de los que tienen dato), no todos los
  ceros — para no sobrecorregir excluyendo anuncios que de verdad rinden mal.
- **Conclusión con datos auditados**: el gap baja de 39,7% a **23,1%**
  (6.661 €/año). No desaparece del todo, pero se reduce en más de un tercio.
- **Traducción a dinero**: para la decisión de escalar a un portafolio de 50
  propiedades, la "penalización" estimada por operar en grande pasa de
  483.000 €/año (dato crudo) a 333.042 €/año (dato auditado) — una diferencia
  de **149.958 €/año** entre decidir con datos sin auditar o auditados.

## Preguntas de negocio

- ¿Qué características del alojamiento y del anfitrión explican las diferencias en
  el rendimiento económico estimado entre alojamientos de Barcelona?
- ¿Los anfitriones profesionales (>50 propiedades) tienen un rendimiento por anuncio
  distinto al de los particulares? (ya hay una correlación débil negativa, -0,19,
  a confirmar tras el tratamiento).
- ¿Cambian esas conclusiones cuando se usan datos tratados en vez de originales?

## Target y variables

- **Target**: `estimated_revenue_l365d` (regresión).
- **Metodología del target (citar en el proyecto)**: Inside Airbnb la calcula como
  reservas estimadas (nº de reseñas de los últimos 365 días ÷ tasa de conversión del
  50%) × duración media de estancia × precio, con tope de ocupación del 70%. Fuente:
  https://insideairbnb.com/data-assumptions/
- **Limitación a declarar abiertamente**: es una estimación de un tercero, no
  ingresos reales observados. Se documenta como parte de la propia auditoría de
  calidad, no se oculta.
- **Predictoras permitidas (sin fuga)**: `room_type`, `property_type`,
  `accommodates`, `bedrooms`, `bathrooms`, `beds`, `neighbourhood_cleansed`,
  `amenities`, `host_listings_count`, `calculated_host_listings_count`,
  `host_is_superhost`. Se incluyen las dos variables de conteo de anuncios
  por anfitrión porque no son redundantes (correlación 0,93, no 1,0; 478
  anuncios divergen entre ambas — ver "Corrección metodológica" más abajo):
  `calculated_host_listings_count` capta la escala del anfitrión en
  Barcelona, `host_listings_count` su escala global. Se deja que el modelo
  muestre con la importancia de variables cuál aporta más señal, en vez de
  elegir una de antemano.
- **Excluidas por fuga de información**: `price`, `estimated_occupancy_l365d`,
  `number_of_reviews` (y variantes), `minimum_nights` (todas forman parte de la
  fórmula con la que se calcula el target).

## Limitaciones metodológicas (declarar explícitamente en el informe)

**Las decisiones de curación están justificadas, pero no validadas contra un
valor real conocido.** El proyecto compara "datos crudos" vs. "una versión
concreta de datos auditados" (la decidida en el notebook 04-05), pero no
puede probar que esa curación sea "la correcta", solo que es razonada,
documentada y verificada mecánicamente (las consultas SQL antes/después
confirman que el código hizo lo que decía que iba a hacer, no que el criterio
de imputación elegido sea el único válido). Esto es inherente a cualquier
proceso de imputación: si se conociera el valor real que falta, no habría
nada que imputar. Mismo espíritu que ya se aplica a `estimated_revenue_l365d`
(estimación de terceros, no ingreso real) y a no asumir de antemano que el
modelo tratado tiene que ganar — se declara la limitación en vez de
ocultarla.

**Mitigación parcial planeada: chequeo de sensibilidad en el notebook 06.**
En vez de imputar `bedrooms`/`bathrooms`/`beds` de una única forma (mediana
por `accommodates`, ya hecho en el notebook 05), se prueba un criterio
alternativo decidido: **mediana por `neighbourhood_cleansed`** (barrio) en
vez de por capacidad. Se genera una segunda versión del dataset curado con
este criterio (criterio B), y en el notebook 06 el modelo se entrena tres
veces: datos crudos, curados con criterio A (capacidad, notebook 05), y
curados con criterio B (barrio). Se comprueba si la conclusión final (el gap
de negocio de 149.958 €/año, las métricas MAE/RMSE/R² del modelo) se
mantiene estable o
cambia mucho entre ambos criterios. Si se mantiene estable con más de un
criterio de limpieza razonable, es evidencia de que la curación no es
arbitraria/frágil — no prueba que sea "la verdad", pero sí que no depende de
una elección caprichosa. Se reporta el resultado tal cual salga, igual que el
resto del proyecto (si cambia mucho, también se documenta y se discute por
qué).

## Los dos impactos a medir

1. **Impacto en negocio**: conclusiones (ej. qué características explican mejor
   rendimiento) con datos originales vs. tratados, variación absoluta y porcentual.
2. **Impacto en el modelo**: mismo modelo de regresión entrenado con datos originales
   vs. tratados, comparando MAE, RMSE y R². No se asume que el modelo tratado tiene
   que ganar, cualquier resultado (mejora, empeora, casi no cambia) es válido y se
   reporta.

## Cronograma (6 semanas, ~1,5 meses)

- Semana 1: formalizar la auditoría ya hecha en notebook + tabla de recomendaciones
  de gobernanza (problema → riesgo → decisión → justificación).
- Semana 2-3: tratamiento/curación de datos (raw → curated, reproducible en código)
  + preparación de variables (parsear `amenities`, codificar barrio, etc.).
- Semana 3-4: modelo con datos originales vs. tratados, comparar métricas.
- Semana 5: dashboard/informe y narrativa de negocio.
- Semana 6: preparar y ensayar la presentación (30 min + preguntas).

## Visión de negocio / framework reutilizable (narrativa de cierre, no alcance técnico nuevo)

DataTrust se aplica en este proyecto a Airbnb Barcelona, pero el problema que audita
no es exclusivo de Airbnb. Evidencia externa ya recopilada durante la investigación
del proyecto:

- **SEAT:CODE** (unidad tecnológica de SEAT en Barcelona) documentó públicamente
  problemas de calidad de datos al construir su app de movilidad sobre Open Data BCN.
- La industria del marketing pierde hasta el **47% del gasto** (~$66.000 millones
  anuales) por atribución rota y datos fragmentados.
- **Zillow** cerró su división Zillow Offers (pérdidas de $300M+) tras decisiones
  basadas en un modelo cuyos supuestos dejaron de representar la realidad del mercado.

Y el hallazgo propio del proyecto: **53,4% del inventario de Airbnb Barcelona tiene
al menos una incidencia de calidad** dentro de las reglas auditadas. El mismo patrón
se repite en sectores distintos (movilidad, marketing, inmobiliario), lo que sostiene
que el framework generaliza, no es una afirmación gratuita.

**Cómo se incorpora sin ampliar el alcance de las 6 semanas**:
1. Cierre de la presentación y de la memoria del proyecto: plantear DataTrust como
   framework aplicable a cualquier empresa que tome decisiones sobre datos propios,
   con Airbnb Barcelona como caso de estudio que lo demuestra, no como su límite.
2. Decisión técnica pequeña (no es alcance nuevo): escribir las funciones de
   auditoría del Bloque 1 recibiendo los nombres de columnas como parámetro (ej.
   `auditar_completitud(df, columnas_criticas)`) en vez de hardcodear los nombres de
   columnas de Airbnb. Mismo esfuerzo, buena práctica, y da una prueba real (no solo
   una promesa) de que el código podría apuntar a otro dataset.

Si en la defensa preguntan "¿esto solo sirve para Airbnb?", la respuesta es enseñar
que las funciones ya aceptan cualquier columna como parámetro, no prometer que se
construyó algo comercial que no existe.

## Fuentes de datos complementarias (no usadas, por si hiciera falta algo puntual)

No es un cambio de alcance ni reabre la decisión de dataset (ver "Alcance
cerrado"): son enlaces guardados por si en algún momento del tratamiento,
modelo o dashboard hiciera falta un dato puntual de contexto para Barcelona,
sin sustituir a Airbnb Barcelona como dataset principal.

- **Idescat** (Institut d'Estadística de Catalunya) — datos abiertos oficiales:
  https://www.idescat.cat/dades/obertes/. Posible uso: estadísticas oficiales
  por barrio/municipio (población, vivienda, turismo) para contextualizar
  algún hallazgo, si se decide en el momento que aporta valor real.
- **datos.gob.es** — portal nacional de datos abiertos de España:
  https://datos.gob.es/es/. Catálogo general (no específico de Barcelona ni
  de vivienda turística); útil solo como punto de búsqueda si algún dato
  puntual de contexto nacional hiciera falta más adelante.

## Herramienta para la presentación en vivo de la defensa (decisión tomada)

**Por defecto: todo en Power BI**, siguiendo un precedente real verificado:
un compañero (Biel Domènech) presentó su defensa usando únicamente Power BI
—sin PowerPoint aparte—, con una página de portada/título diseñada dentro del
propio `.pbix` (texto + imagen de fondo + su nombre, con el mismo aspecto de
una diapositiva) seguida de las páginas de datos interactivos. La autora de
este documento estuvo presente en esa defensa y confirma que fue así, no es
una suposición. Ventajas concretas: no duplica trabajo (no hay que diseñar la
narrativa dos veces, una en slides y otra en Power BI), aprovecha el
`.pbix` que de todas formas hay que construir, y permite mostrar
interactividad real en el momento exacto de la narrativa (filtrar por barrio,
hacer clic en el mapa) en vez de una captura estática.

En la práctica: el `.pbix` incluye, además de las páginas de datos
(coroplético por barrio, KPIs de brecha económica, etc.), una o dos páginas
de portada/cierre con texto y diseño, para que toda la presentación de 30 min
viva en un solo archivo.

**Extra opcional (solo si sobra tiempo, no comprometido)**: la autora
considera que una demo en **Streamlit** podría causar más impacto visual que
Power BI, y se plantea cambiar de herramienta para la presentación completa
—no solo como demo aislada del modelo— si el resto del cronograma (semanas
1-5) se cumple sin retraso y queda tiempo real para construirla y pulirla
bien. Esta es una decisión abierta, no cerrada: el plan por defecto sigue
siendo Power BI, Streamlit solo se activa si hay margen de tiempo real y se
valora que compensa el riesgo de cambiar de herramienta tan tarde.

## Prácticas a adoptar (aprendidas de proyectos previos de compañeros de ITA Academy)

- **Mostrar un hallazgo "tentador pero incompleto" antes del hallazgo real**: enseñar la
  lectura rápida/obvia de los datos y explícitamente decir por qué no basta, antes de
  profundizar con la auditoría. Demuestra madurez analítica, no solo un resultado.
- **Definir criterios técnicos explícitamente en el informe**, no dejarlos implícitos en
  el código (ej. "se define anfitrión profesional como aquel con más de 50 anuncios").
- **Mostrar el código de limpieza junto a la justificación**, no solo describirla en
  prosa, como evidencia visual de la tabla de recomendaciones (problema → decisión →
  justificación).
- **Citar explícitamente la licencia/términos de uso de Inside Airbnb** como evidencia
  de legitimidad de la fuente, además de declarar que `estimated_revenue_l365d` es una
  estimación de terceros, no un dato real observado.
- **Cerrar el informe respondiendo literalmente la pregunta central planteada al
  inicio**, con matices, no con una conclusión plana.
- **Diagrama de flujo simple en texto en el README** mostrando el pipeline (Auditoría →
  Gobernanza → Tratamiento → Comparación negocio → Comparación modelo).
- **Embeber capturas de las visualizaciones clave directamente en el README**, no solo
  dejarlas dentro del dashboard de Power BI.
- **Sección con nombre propio "Validación"** en el informe/README, listando de forma
  explícita las comprobaciones de rigor ya hechas (fuga de información descartada,
  balance de clases confirmado, integridad referencial comprobada).
- **Notebook de auditoría/limpieza separado por tabla** (uno para listings, otro para
  reviews, otro para calendar), en vez de mezclar las tres en un único notebook.
- **Introducción en tres bloques cortos**: Contexto (qué es Airbnb Barcelona) →
  Problema (con las cifras concretas ya encontradas) → Objetivo (los 5 objetivos).
- **Preguntas de negocio explícitas planteadas al inicio, respondidas una por una en
  la sección de impacto**, cada una con su propia visualización, en vez de mezclar
  todo el análisis de negocio en un solo bloque.
- **Diagrama simple del flujo de datos**: CSV de Inside Airbnb → limpieza en Python →
  dataset curado → Power BI, mostrado visualmente en el informe/README.

## Guía de redacción del informe y estilo (lecturas recomendadas)

Síntesis de 4 lecturas recomendadas sobre cómo escribir el artículo/informe final,
aplicada a este proyecto (no todo lo leído aplica, se filtra explícitamente qué sí
y qué no).

**Fuentes**: guía de Sobre Biotech sobre estructura de artículo científico; Baker,
P.N. "How to write your first paper" (*Obstetrics, Gynaecology and Reproductive
Medicine*, 2011); Huguet et al. "El estilo de la comunicación científica" (*Actas
Urológicas Españolas*, 2018); Databox, "How to Write Data Analysis Reports in 9
Easy Steps" (databox.com/data-analysis-report).

**Qué NO aplica** (para no desviar esfuerzo): todo el proceso de publicación en
revista de Baker (elegir revista por factor de impacto, autoría múltiple, carta al
editor, responder a revisores) — este es un informe de bootcamp, no una
publicación científica. Tampoco el vocabulario clínico de los ejemplos de Huguet
et al. (el principio de claridad/precisión/brevedad sí se adopta, los ejemplos
médicos no). Tampoco la herramienta Databox en sí (el artículo es en parte
publicidad de su producto); el proyecto usa Power BI, ya decidido.

**Qué sí cambia en el informe PDF**:

1. **Separar Resultados de Discusión** como dos secciones distintas: Resultados
   = solo cifras y gráficos, sin interpretar; Discusión = interpretación, impacto
   en negocio, impacto en el modelo, limitaciones. Esto es distinto de los
   notebooks (donde la interpretación va justo debajo del código a propósito, son
   documentos de trabajo), pero en el informe final sí conviene separarlo.
2. **El Resumen/Abstract se redacta al final**, aunque va primero en el
   documento, una vez se tiene la versión completa del informe.
3. **Checklist de estilo de redacción** (Huguet et al.): frases cortas (evitar
   subordinadas enredadas), voz activa en vez de pasiva, no repetir la misma
   palabra en la misma frase, usar conectores explícitos entre párrafos, evitar
   gerundios en exceso y anglicismos innecesarios (los términos técnicos propios
   del proyecto como "dataset", "target" o "pipeline" se mantienen, por ser
   estándar en el campo, no por descuido).
4. **Para el dashboard de Power BI** (Databox): no incluir todas las métricas
   posibles, solo las KPI vitales ya identificadas en este documento (brecha
   económica profesional/particular, % de incidencias de calidad, desglose por
   barrio); resumen/KPIs arriba, detalle abajo; cada visual responde una
   pregunta de negocio concreta (coincide con la práctica ya adoptada más abajo
   de "preguntas de negocio explícitas, cada una con su propia visualización");
   recomendaciones con tono objetivo y orientado a soluciones, no a señalar
   culpables.

**Estructura resultante para el informe PDF** — **actualizado tras conocer el
enunciado oficial del Sprint 13** (ver "Especificaciones oficiales" al inicio
del documento, que manda sobre esta guía): Título → Resumen (máx. 250
palabras) → Introducción (contexto, problema, objetivo) → Metodología (datos,
criterios de auditoría, decisiones de gobernanza) → Resultados (hallazgos,
cifras, visualizaciones, sin interpretar) → Discusión (impacto en negocio,
impacto en el modelo, limitaciones, aportación explícita a la toma de
decisiones empresariales, respuesta a la pregunta central) → Conclusiones →
Referencias (Inside Airbnb, licencia de uso, fuentes citadas). **Se eliminan
Agradecimientos y Apéndices** de esta versión: no están en la lista oficial y,
con el límite de **máximo 4 páginas**, no hay espacio para ellos. La tabla
completa de gobernanza (14 hallazgos) no cabe entera en el informe: va
condensada/resumida ahí, con el detalle completo disponible en el notebook 04
(entregable técnico aparte, sin límite de páginas).

**Checklist de autorrevisión antes de entregar** (adaptado de Cordeiro, Ortuño,
Paixão & Marôco, "Reading a Scientific Paper for Psychology and the Social
Sciences: A Critical Guide", 2015 — un paper sobre cómo *leer* críticamente un
artículo, no sobre cómo escribirlo; se reutiliza aquí como checklist para
autoevaluar el informe antes de entregarlo, como si lo leyera un revisor
externo). Preguntas adaptadas de su apéndice, solo las relevantes para este
proyecto (se descartan las específicas de psicología/participantes):

- **Título**: ¿es específico y refleja el contenido real del informe?
- **Resumen**: ¿se entiende sin leer el resto del documento? ¿indica qué se
  hizo, qué se encontró y la relevancia práctica? ¿hay alguna discrepancia
  entre el resumen y el resto del informe?
- **Introducción**: ¿el problema y el objetivo están claramente definidos?
  ¿las preguntas de negocio son relevantes y están bien planteadas?
- **Metodología**: ¿se describe con suficiente detalle como para que alguien
  pueda reproducir la auditoría y el tratamiento? ¿se justifica cada decisión
  de gobernanza, no solo se enuncia?
- **Resultados**: ¿se presentan sin interpretar (la interpretación va en
  Discusión)? ¿responden a todas las preguntas de negocio planteadas al
  inicio? ¿las tablas/gráficos son necesarios y se explican por sí solos?
- **Discusión**: ¿se dan explicaciones alternativas, no solo una lectura
  única de los hallazgos? ¿las limitaciones quedan explícitas (ej.
  `estimated_revenue_l365d` como estimación de terceros)? ¿las conclusiones
  son coherentes con los resultados presentados, sin introducir información
  nueva?
- **Figuras y tablas**: ¿están numeradas y tituladas? ¿se refieren
  correctamente en el texto? ¿podrían combinarse o simplificarse?

**Formato de citas: APA 7ª edición** (guía de Scribbr). Se usa el sistema
autor-fecha: cita entre paréntesis `(Autor, año)` o narrativa `Autor (año)`.
Cuando el autor es una organización (como en este proyecto), se cita igual que
un autor individual. Aplicado a las fuentes ya usadas en este documento:

- **Cita en el texto**: "...según la metodología de cálculo (Inside Airbnb,
  2026)" o, en forma narrativa, "Inside Airbnb (2026) calcula el ingreso
  estimado como...".
- **En la página de Referencias** (orden alfabético, sangría francesa,
  interlineado doble):
  - `Inside Airbnb. (2026). Barcelona dataset [Conjunto de datos].
    https://insideairbnb.com/barcelona/`
  - `Inside Airbnb. (s.f.). Data assumptions. Recuperado [fecha de consulta],
    de https://insideairbnb.com/data-assumptions/`
- Si se cita alguna de las lecturas de esta guía de redacción (por ejemplo,
  para justificar la separación Resultados/Discusión), el formato sería:
  `Cordeiro, P., Ortuño, V. E. C., Paixão, M. P., & Marôco, J. (2015). Reading
  a scientific paper for psychology and the social sciences: A critical
  guide. Psychology, Community & Health, 4(3), 114–122.
  https://doi.org/10.5964/pch.v4i3.136`
- Solo se incluyen en Referencias las fuentes citadas en el cuerpo del
  informe; no hace falta listar todo lo leído durante la preparación del
  proyecto si no se cita explícitamente.

**Gestor de referencias recomendado**: **Zotero** (gratuito, código abierto).
Se eligió frente a otras 9 opciones revisadas (BibMe, EasyBib, CiteULike —
cerrado desde 2019—, Mendeley, RefWorks, EndNote, Citation Machine, BibTeX
—solo para LaTeX, no aplica aquí—, Library Master) porque: (a) es gratuito,
(b) tiene extensión de navegador que captura la referencia con un clic desde
la página de Inside Airbnb o desde un PDF, y (c) se integra con Word/Google
Docs para generar las citas en el texto y la lista de Referencias en APA 7
automáticamente. Fuente: julianmarquina.es,
"10 gestores de referencias bibliográficas a tener en cuenta para tus
trabajos".

**Principios de visualización de datos** (Midway, S. R. (2020). Principles of
effective data visualization. *Patterns*, 1(9), 100141.
https://doi.org/10.1016/j.patter.2020.100141). Aplican tanto al dashboard de
Power BI como a las figuras del informe PDF:

1. Definir el mensaje de cada visual antes de elegir el tipo de gráfico.
2. Elegir la geometría adecuada al dato (líneas para tendencia, barras para
   comparación categórica, mapa para barrio) y mostrar el dato real, no solo
   un resumen vacío de contexto.
3. Usar el color con intención, legible también en escala de grises.
4. Incluir incertidumbre cuando aplique (ej. si se muestran medias, considerar
   si el rango o la dispersión importa para la conclusión).
5. Usar paneles pequeños repetidos ("small multiples") para comparar — encaja
   con la práctica ya adoptada más abajo de "una visualización por cada
   pregunta de negocio", en vez de un gráfico único que mezcle todo.
6. Distinguir dato observado de dato estimado/modelado (relevante aquí: dejar
   claro en las visualizaciones cuándo se muestra `estimated_revenue_l365d`,
   una estimación de terceros, y no un ingreso real).
7. Visuales simples, con leyendas/títulos que se entiendan sin leer el texto
   del informe.
8. Las tablas se dejan para consulta de valores exactos (ej. anexo con la
   tabla completa de gobernanza); para mostrar tendencias o comparaciones, un
   gráfico comunica mejor que una tabla.

**Herramienta de referencia para elegir el gráfico correcto**:
[data-to-viz.com](https://www.data-to-viz.com/) (Yan Holtz y Conor Healy).
Selector de gráficos por tipo de dato (numérico, categórico, num&cat, mapas,
red, series temporales) con árbol de decisión, galería por propósito
(distribución, correlación, ranking, parte de un todo, evolución, mapa,
flujo), y una sección de "errores comunes" por tipo de gráfico (ejes
recortados, abuso de gráficos de pastel, paletas arcoíris, mapas sin
normalizar). Consultar al construir el dashboard de Power BI: ej. para la
brecha económica profesional/particular (categórico + numérico) sugiere
barras, no pastel; para el mapa por barrio, avisa de normalizar los datos
antes de un mapa coroplético en vez de usar valores absolutos.

**Buenas prácticas adicionales de diseño** (DataCamp, "11 Data Visualization
Techniques for Every Use-Case with Examples", Javier Canales Luna —
solo lo que no se repite de las dos referencias anteriores):

- Elegir el gráfico también según cuántas variables se analizan a la vez
  (univariado, bivariado o multivariado), no solo según el tipo de dato.
- Conocer el nivel de la audiencia antes de diseñar el visual (relevante aquí:
  el dashboard de Power BI es para una audiencia de negocio, no técnica).
- Quitar ruido visual innecesario: "el objetivo principal de la visualización
  de datos es reducir la complejidad y dar claridad".
- Usar una sola tipografía con máximo 3 tamaños, y jerarquía clara (negrita
  para los elementos clave).
- Paleta de color consistente y con propósito (agrupar o jerarquizar), no
  decorativa.
- Al elegir herramienta (ya resuelto aquí con Power BI, pero como criterio
  general): curva de aprendizaje, flexibilidad, si es para un gráfico suelto
  o un dashboard completo, y coste.

## Estructura del repositorio y entregables

Antes de la entrega final, reorganizar la carpeta del proyecto siguiendo el patrón
que usan los proyectos mejor organizados de cohortes anteriores (visto en el
repositorio de proyectos de estudiantes de ITA):

```
Proyecto_Final/
├── data/           (datasets crudos, ya descargados)
├── notebooks/       (auditoría, tratamiento, modelo)
├── report/          (informe final en PDF)
└── slides/           (presentación de 30 min, separada del informe)
```

Los scripts de exploración actuales (`explore_*.py`, `check_impacto_preliminar.py`)
quedan como base para los notebooks de `notebooks/`.

**Entregables finales** (lista oficial del Sprint 13, ver sección
"Especificaciones oficiales" al inicio del documento):
1. **Informe en PDF, máximo 4 páginas**, estructura IMRaD + APA (ver detalle
   en "Especificaciones oficiales" y en "Guía de redacción del informe").
2. **Conjuntos de datos usados en Power BI** — los CSV curados de
   `data/airbnb_bcn_curado/` generados por el notebook 05.
3. **El `.pbix` de Power BI exportado como PDF**, más un documento aparte con
   las fórmulas DAX si se usa alguna.
4. **Documento con la presentación** (slides) para la defensa, como
   documento separado del informe.

## Dónde se usa SQL

SQL se usa donde aporta algo que pandas no aporta tan bien (relaciones entre tablas,
controles reproducibles), no para repetir en otro lenguaje lo ya hecho en pandas:

- **Motor**: SQLite (autocontenido, sin servidor que configurar, cualquiera que
  clone el repo lo ejecuta sin instalar nada). No se usa el MySQL local de sprints
  anteriores, esa habilidad ya está demostrada en otro proyecto del portafolio.
- **Notebooks 02 (`reviews`) y 03 (`calendar`)**: integridad referencial contra
  `listings` vía `LEFT JOIN ... WHERE ... IS NULL` (reviews/filas de calendario
  huérfanas), en vez de repetir el `isin()` de pandas.
- **Notebook 05 (tratamiento)**: las mismas consultas SQL de control (huérfanos,
  duplicados) se ejecutan antes y después de curar los datos, como evidencia
  reproducible de la mejora, no solo una afirmación.
- **No se vuelve a auditar `listings` en SQL** (notebook 01, ya cerrado con pandas),
  repetir el mismo análisis en otro lenguaje no aporta nada nuevo.

División de responsabilidades: SQL → relaciones/integridad/controles reproducibles;
Pandas → limpieza/transformación/EDA; Python/ML → medir impacto de la calidad;
Visualización → comunicar resultados.

## Glosario (para la presentación, diapositiva de apoyo)

Términos propios del proyecto que no son de uso general, con la definición exacta
que se usa aquí, para no dar por hecho que la audiencia los conoce:

- **Anfitrión profesional / particular**: distinción propia del proyecto, no de
  Airbnb. Profesional = cuenta de anfitrión asociada a más de 50 anuncios **en
  Barcelona** (`calculated_host_listings_count > 50` — no `host_listings_count`,
  que es un conteo global de toda la plataforma, no específico de esta ciudad;
  ver "Corrección metodológica" en la sección de impacto monetario). Mide
  gestión en la plataforma dentro de este mercado, no propiedad, un anfitrión
  con muchos anuncios probablemente es una agencia gestora, no alguien dueño de
  50 viviendas.
- **Fuga de información (data leakage)**: usar como variable predictora un dato que
  en realidad ya contiene, matemáticamente, la respuesta que se quiere predecir. En
  este proyecto: precio, ocupación y nº de reseñas se excluyen del modelo porque
  forman parte de la fórmula con la que se calcula `estimated_revenue_l365d`.
- **Integridad referencial**: que un identificador que aparece en una tabla (ej.
  `listing_id` en `reviews`) exista de verdad en la tabla a la que se supone que
  hace referencia (`listings`). Si no existe, es un registro "huérfano".
- **`estimated_revenue_l365d`**: variable objetivo del modelo. Estimación de Inside
  Airbnb (no ingreso real observado) del dinero generado por un alojamiento en los
  últimos 365 días, calculada a partir de reseñas, duración media de estancia y
  precio.
- **HUTB**: código del registro oficial de "Habitatge d'Ús Turístic" (vivienda de
  uso turístico) en Cataluña, el número de licencia que debería aparecer en el
  campo `license`.
- **Licencia "no clasificable"**: no significa "sin licencia" ni "ilegal", significa
  que el texto del campo no se pudo interpretar con las reglas definidas (puede ser
  una licencia real mal formateada). Distinción importante para no sobreafirmar.
- **Valor atípico / extremo / sospechoso / imposible**: un valor fuera de lo común
  (ej. precio muy alto) no es automáticamente un error. Se distingue entre extremo
  (posiblemente válido, requiere contexto), sospechoso (requiere investigación) e
  imposible (sin interpretación coherente para el negocio).
- **DataTrust**: nombre del framework/metodología de este proyecto (auditar →
  priorizar → curar → comparar negocio → comparar modelo), aplicado a Airbnb
  Barcelona como caso de estudio.

## Opciones de título en consideración (sin decidir aún)

El título actual del proyecto se mantiene sin cambios por ahora:

> **DataTrust**
> Auditoría de calidad y gobernanza de datos aplicada a un caso real de
> alquiler turístico en Barcelona.

Durante la discusión sobre la guía de presentaciones de Visme (más abajo), se
consideraron estas alternativas, sin decidir ninguna todavía — quedan aquí
anotadas para retomar la decisión más adelante:

- `DataTrust: 149.958 €/año, el coste real de no auditar tus datos (caso
  Airbnb Barcelona)` — descartada: mete la cifra en el título, lo que
  equivale a revelar la conclusión antes de tiempo, y reduce el proyecto a
  solo dinero cuando también mide gobernanza y calidad de decisión.
- `¿Puedes confiar en tus datos? Auditoría de calidad en Airbnb Barcelona` —
  título en forma de pregunta provocadora.
- `El precio de los datos sucios: cómo 149.958 €/año dependen de auditar bien
  tus datos` — descartada por la misma razón que la primera (cifra en el
  título).
- `DataTrust: ¿qué te cuesta no auditar tus datos? (caso Airbnb Barcelona)` —
  pregunta en segunda persona, deja abierto que el costo no sea solo
  monetario (usa "costar" en sentido amplio, no solo dinero).
- `DataTrust: ¿qué le puede costar a una empresa no auditar sus datos? (caso
  Airbnb Barcelona)` — misma idea que la anterior pero en tercera persona,
  conecta explícitamente con la sección "Visión de negocio / framework
  reutilizable" (DataTrust aplicable a cualquier empresa, no solo a Airbnb).
- `DataTrust: consecuencias de una mala auditoría de datos (caso Airbnb
  Barcelona)` — versión declarativa (no pregunta), propuesta directamente.
- `DataTrust: consecuencias de no auditar los datos (caso Airbnb Barcelona)` —
  variante más precisa de la anterior: el hallazgo central del proyecto es
  sobre qué pasa cuando NO se audita (dato crudo vs. dato auditado), no sobre
  una auditoría mal ejecutada.

## Guía de presentaciones efectivas (Visme)

Fuente: visme.co/blog/es/presentaciones-efectivas/. Guía completa en 4 partes,
sin recortar — se deja todo el detalle para no perder nada que pueda servir
más adelante, aunque algún punto no se use en la versión final.

**1. Planeando la presentación**

- **Elegir el tema**: el artículo lo marca como "sin discusión una de las
  partes más importantes" de la presentación. En este proyecto el tema
  (Airbnb Barcelona) sí se eligió activamente, comparando varias alternativas
  reales (Olist, accidentes de tráfico de Open Data BCN, datasets de
  marketing/salud en Kaggle — ver sección "Dataset elegido" más arriba), y
  después se cerró deliberadamente ("Alcance cerrado: no seguir buscando
  datasets ni temas alternativos"). No es una restricción externa impuesta
  por el proyecto final, es una decisión propia ya tomada — que en teoría
  sigue siendo modificable si hubiera una razón de peso, aunque a estas
  alturas (5 notebooks, base de datos y modelo ya avanzados) reabrirla tendría
  un coste alto. Dado que el tema sí se eligió con criterio, el "ángulo único"
  que pide el artículo no es un sustituto por no poder elegir tema, es un
  paso adicional ya cubierto en la sección "Visión de negocio / framework
  reutilizable": presentar DataTrust como framework generalizable (no solo
  como análisis de Airbnb).
- **Investigar el tema a fondo**: dominarlo lo suficiente para responder
  preguntas del tribunal, no solo para exponer lo preparado.
- **Conocer a la audiencia**: hablar en su lenguaje (en la defensa, el
  tribunal puede incluir perfiles técnicos y no técnicos, el glosario que ya
  tienes preparado en la ficha maestra ayuda aquí).
- **Definir el propósito**: informar, entretener, inspirar o persuadir — en
  este proyecto el propósito es mixto: informar (hallazgos) + persuadir (que
  la calidad de datos importa y cambia decisiones reales).
- **Crear un guion sólido**: introducción, desarrollo y conclusión. Regla
  orientativa **10-20-30** (10 diapositivas, 20 minutos, letra de al menos 30
  puntos) — el artículo aclara que no es estricta; tu estructura ya definida
  de 30 min con bloques de tiempo por sección es más detallada que esta regla
  genérica, así que prevalece la tuya.

**2. Escribiendo el contenido**

- Limitar el texto por diapositiva: **6 a 8 líneas como máximo**.
- Verificar toda la información con fuentes confiables (ya se hace en este
  proyecto: cada hallazgo está verificado con código, no son suposiciones).
- Usar narración y centrarse en personas/casos concretos (el caso de los
  anfitriones profesionales vs. particulares ya cumple esto).
- Incluir ejemplos prácticos.
- Usar notas del presentador (para detalle que no va en la diapositiva pero
  sirve de apoyo al hablar).
- Presentar la información visualmente: tablas, gráficos, mapas (coincide con
  los principios de visualización ya guardados más arriba).
- Usar multimedia si aporta: video, GIFs, audio, elementos interactivos
  (opcional, no comprometido para este proyecto).
- Preparar preguntas provocadoras para enganchar a la audiencia.
- Simplificar las oraciones (coincide con el checklist de estilo de Huguet et
  al. ya guardado: frases cortas, claridad).

**3. Diseñando la presentación**

- Adaptar el diseño al modelo de entrega (presencial vs. en línea) — confirmar
  con antelación cómo será la defensa.
- Usar hasta **3 tipografías compatibles**.
- Imágenes e iconos de alta calidad, no pixelados.
- Mantener alineación consistente (usar una cuadrícula/guías).
- Transición uniforme y consistente entre diapositivas, no mezclar varios
  estilos de transición.
- **Una sola idea principal por diapositiva**.
- Paleta de colores cohesiva y con buen contraste (coincide con el principio
  de Midway de que el gráfico se entienda también en escala de grises).
- Revisar y pulir el texto; pedir una segunda revisión a otra persona antes
  de la entrega final.
- Mantener identidad de marca consistente — en este caso, la identidad visual
  de "DataTrust" a lo largo de todas las diapositivas.

**4. Dando una presentación memorable**

- **Ensayar en voz alta**, frente a un espejo y con cronómetro — no basta con
  memorizar en silencio.
- Técnicas de memorización: "palacio de la memoria", escribir los puntos
  clave a mano, practicar por la tarde, grabarse y escucharse.
- **Empezar fuerte**: historia personal, pregunta directa, estadística
  sorprendente, objeto de utilería o video. Ya hay un candidato natural: el
  53,4% de incidencias de calidad, o la pregunta "¿podemos confiar en los
  datos con los que se toman decisiones de alquiler turístico?" (ya está en
  la estructura de apertura más abajo).
- Observar a la audiencia durante la exposición y ajustar sobre la marcha si
  hace falta.
- Ser auténtico, no sonar a guion memorizado palabra por palabra.
- **Cerrar con impacto**: cita memorable, repaso de puntos clave, historia, o
  llamada a la acción.
- Dejar tiempo explícito para preguntas al final (la estructura ya definida
  reserva los últimos minutos para esto).
- Preparar contenido de respaldo (diapositivas extra con detalle técnico, por
  si el tribunal pregunta algo específico que no cabía en el tiempo principal).
- **Si se pierde la atención de la audiencia a mitad de la exposición**: hacer
  una pregunta directa, cambiar de tema momentáneamente, usar humor, pedir que
  se pongan de pie, hacer una pausa breve, o invitar preguntas antes de tiempo.

## Preparación para la defensa del proyecto (preguntas y respuestas)

Fuente: jatg298384595.wordpress.com, "Preparación para la defensa de un
proyecto: estrategias y consejos" (jatapia99, 25/12/2023). Blog personal, no
fuente académica, pero con una sección (4) que no estaba cubierta por la guía
de Visme: cómo manejar las preguntas durante la defensa en sí, no solo cómo
presentar. Se deja el contenido completo, marcando qué es nuevo y qué ya
estaba cubierto por otras lecturas guardadas más arriba.

**1. Preparación de la defensa** (mayormente ya cubierto, se deja como
confirmación/refuerzo):
- Entender el proyecto a fondo: repasar objetivos, metodología, análisis de
  datos y conclusiones, construyendo una narrativa que conecte todas las
  partes — coincide con la práctica ya adoptada de "cerrar el informe
  respondiendo literalmente la pregunta central planteada al inicio".
- Organizar materiales: diapositivas claras con gráficos, tablas y
  visualizaciones para explicar la complejidad — coincide con los principios
  de visualización de Midway y data-to-viz.com ya guardados.
- Ensayar la presentación completa, con cronómetro, para ganar fluidez y
  ajustarse al tiempo — coincide con lo ya guardado de la guía de Visme
  ("ensayar en voz alta, con cronómetro").

**2. Presentación de datos y argumentos** (mayormente ya cubierto):
- Claridad y concisión: explicar metodología y hallazgos sin tecnicismos
  innecesarios — coincide con el checklist de estilo de Huguet et al. y con
  tener un glosario de apoyo (ya está en la ficha maestra).
- Enfatizar los puntos clave, usar historias o ejemplos para ilustrar ideas —
  coincide con "usar narración y centrarse en personas/casos concretos" de
  Visme (el caso profesional vs. particular ya cumple esto).

**3. Anticipar y responder preguntas** (esto SÍ es contenido nuevo, no estaba
cubierto por ninguna lectura anterior):
- **Preguntas comunes**: prever de antemano preguntas sobre metodología,
  resultados y aplicaciones prácticas, con respuestas claras y directas ya
  preparadas (no improvisadas en el momento). Aplicado a este proyecto: ya
  tienes una buena base para esto en la sección "Glosario" y en la lógica de
  "mostrar un hallazgo tentador pero incompleto antes del hallazgo real", que
  anticipa justo el tipo de pregunta "¿por qué no se ve esto directamente en
  los datos crudos?".
- **Preguntas difíciles o inesperadas**: mantener la calma, pensar antes de
  responder. Si no se tiene la respuesta, **admitirlo con honestidad** en vez
  de improvisar algo poco sólido, y ofrecer dar seguimiento después (por
  ejemplo, "no tengo esa cifra exacta ahora, pero puedo verificarla y
  enviarla después de la defensa").
- **Argumento sólido al responder**: respaldar cada respuesta con datos o
  referencias concretas (no con opiniones sueltas), evitar ponerse a la
  defensiva ante una crítica, y tratar cada pregunta como una oportunidad
  para profundizar en el tema, no como un ataque a defenderse.

**4. Conclusión del artículo**: la defensa es la oportunidad de demostrar el
valor y la viabilidad del proyecto. Para lograrlo, son necesarias tres cosas
juntas: preparación cuidadosa, presentación clara, y buen manejo de preguntas
y desafíos — ninguna de las tres sustituye a las otras dos.

## Estructura de la presentación (30 min)

- 0-3 min: el problema (¿podemos confiar en los datos con los que se toman
  decisiones de alquiler turístico?).
- 3-6 min: el dataset (Barcelona, listings/calendar/reviews).
- 6-12 min: la auditoría (hallazgos principales, con visualizaciones).
- 12-17 min: decisiones de gobernanza (qué se hizo con cada problema y por qué).
- 17-22 min: impacto en negocio (antes/después).
- 22-27 min: modelo (antes/después).
- 27-30 min: conclusiones.
