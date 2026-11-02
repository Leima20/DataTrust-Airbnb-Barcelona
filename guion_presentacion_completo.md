# DataTrust — guion para leer durante la presentación

Esto está escrito como el discurso en sí, en el orden exacto en que pasa en la app, para que lo sigas mientras presentas. Los paréntesis en *cursiva* son acotaciones para ti (qué pestaña tocar, qué señalar) — no se leen en voz alta. Al final hay un bloque aparte de preguntas probables, para estudiar antes, no para leer durante la presentación.

Todas las cifras están verificadas contra los datos reales del proyecto (JSON y notebooks) a fecha 2026-10-29.

---

## 1 · Inicio

*(estás en la pestaña "El caso Zillow")*

Antes de hablar de mi proyecto, quiero hablarles de Zillow. Zillow es la plataforma inmobiliaria más grande de Estados Unidos. Tenían una división, Zillow Offers, que compraba casas directamente a los vendedores usando un algoritmo para fijar el precio, las remodelaba, y las revendía con margen. En noviembre de 2021, cerraron esa división por completo y recortaron alrededor del 25% de toda la plantilla de la empresa.

¿Qué pasó? El algoritmo sobreestimó el valor de reventa de muchas de las viviendas que compraron. Eso forzó un ajuste contable de inventario de unos 304 millones de dólares solo en el tercer trimestre de 2021, y la pérdida total atribuida a esa división en el año fue de 881 millones de dólares. El propio CEO lo resumió así: "la imprevisibilidad al pronosticar precios de vivienda superó ampliamente lo que anticipamos".

No fue un modelo roto. Fue un modelo que confió en datos sin entender del todo lo que esos datos realmente significaban. Y de ahí nace mi proyecto: DataTrust parte exactamente de la misma pregunta, pero aplicada a los datos de Airbnb en Barcelona.

*(cambias a la pestaña "La pregunta de investigación")*

La pregunta que guía todo el proyecto es esta: ¿puede la calidad de los datos influir en la toma de decisiones y en las conclusiones de un análisis, incluso cuando los datos parecen suficientemente completos y el modelo predictivo ofrece buenos resultados?

Quiero ser clara en algo desde el principio: no parto asumiendo que los datos de Airbnb están mal. Los audito primero, y dejo que sean los propios datos los que muestren si hay un problema o no. De hecho, van a ver que varias partes de la auditoría salen perfectamente limpias.

Como adelanto de lo que van a ver: el dataset crudo, a primera vista, parece listo para trabajar. Pero al investigar un poco más, encuentro 2.686 casos —un 20,1%— donde el ingreso estimado aparece como "0 euros" sin serlo realmente. Y cuando corrijo eso, el modelo predictivo mejora de forma medible: el R² sube de 0,348 a 0,448 en la comparación más rigurosa que hice. La calidad de los datos no se reduce a mirar el porcentaje de valores nulos — eso es, en una frase, lo que voy a demostrar.

---

## 2 · Contexto del proyecto

Los datos vienen de Inside Airbnb, un proyecto independiente —no es Airbnb la empresa— que recopila datos públicos de la plataforma mediante web scraping, con fines de investigación y transparencia sobre el impacto de los alquileres turísticos.

Trabajo con tres tablas. `listings`, los anuncios: 15.293 filas y 90 columnas en crudo. `reviews`, las reseñas: más de un millón de filas, 1.033.523 exactamente, con solo 6 columnas. Y `calendar`, el calendario de disponibilidad: 5.623.190 filas —por eso, como van a ver en un momento, esa tabla la trabajo directamente con SQL en vez de cargarla entera en memoria.

*(señalas el mapa)* El análisis se centra en Barcelona, donde los anuncios se concentran de forma muy desigual por distrito — aquí lo pueden ver en el mapa, el barrio hereda el número de anuncios de su distrito, porque no hay un dato propio a nivel de barrio tan granular.

*(cambias a la pestaña "Objetivos")*

El proyecto tiene cinco objetivos, y cada uno se resuelve en una página distinta de esta app, así que se los voy a ir señalando a medida que avanzamos: auditar la calidad de los datos; identificar y priorizar los problemas según su impacto; aplicar un proceso de curación documentado y justificado, no limpiar por limpiar; comparar las conclusiones de negocio antes y después del tratamiento; y comparar el rendimiento de un modelo predictivo antes y después del tratamiento.

*(cambias a la pestaña "Herramientas")*

Para esto usé Python y pandas para la carga, exploración y limpieza; SQLite para comprobar integridad referencial, sobre todo en `calendar`, por su volumen; scikit-learn para el modelo predictivo, con cuatro versiones comparadas; y Plotly y Streamlit para toda la visualización, incluyendo esta misma app.

*(cambias a la pestaña "Flujo del proyecto")*

El flujo completo es: auditoría, gobernanza —decidir qué hacer con cada hallazgo—, tratamiento —ejecutar esa decisión— y luego, en paralelo, dos comparaciones finales: el efecto en una métrica de negocio, y el efecto en el rendimiento del modelo. Y, directamente desde la auditoría, sin pasar por el tratamiento, investigo también una simulación de decisión basada en el patrón de esos 2.686 ceros que les mencioné antes — eso lo verán en detalle en la página del hallazgo crítico.

---

## 3 · Auditoría de calidad

Revisé las tres tablas cruzando cada columna contra tres preguntas: ¿falta información? —eso es completitud—; ¿las filas conectan bien entre tablas? —integridad referencial—; y ¿un valor "válido" tiene sentido real? —plausibilidad semántica.

*(estás en la pestaña "Dimensiones")*

Antes de entrar en los números, una aclaración importante: no todo nulo es un error, y no todo cero es un error. Por eso clasifico cada hallazgo en una de cuatro categorías: problema detectado, decisión de tratamiento, limitación de la fuente propia, o hipótesis pendiente de validar. Y para que sea fácil seguir los códigos que van a ver: la letra L es de `listings`, R es de `reviews`, C es de `calendar` — el número es el orden dentro de esa tabla, no es correlativo entre las tres.

*(cambias a la pestaña "Resultados")*

En total encontré 14 hallazgos: ocho en `listings`, cuatro en `reviews`, dos en `calendar`.

*(sub-pestaña "Completitud")*

Doce columnas de `listings` están completamente vacías, cero por ciento de dato útil —eso es L1—, columnas como `host_since` o `host_response_rate`. Y hay seis columnas predictoras con nulos parciales —L2—: `price` con un 12,7% de nulos, `bedrooms` con 16,8%, `bathrooms` con 23,3%, `beds` con 16,0%, `host_about` con 31,8% y `host_location` con 20,3%. `reviews` y `calendar`, en cambio, salieron cien por cien completas en esta dimensión — es importante decirlo, no todo es un problema.

*(sub-pestaña "Plausibilidad")*

El hallazgo más ilustrativo de esta auditoría es el campo `license`. Un 21,1% no es verificable —ni dato ni texto clasificable—, y además hay 5.470 registros con el formato roto: HTML sin limpiar, o dos números de licencia concatenados en el mismo campo. Aquí conviene explicar el contexto legal: `HUTB` es el registro catalán histórico, el más frecuente en el dataset; `NRUA` es el nuevo registro estatal, obligatorio desde julio de 2025 por el Real Decreto 1312/2024, y convive con el HUTB, no lo sustituye. Por categorías: un 47,04% tiene número HUTB, un 25,66% está exento declarado, un 19,90% no tiene dato, un 6,20% ya tiene número NRUA, y un 1,20% es otro caso no clasificable. *(señalas el mapa de distritos)* Y esto varía bastante por zona de la ciudad, entre un 16,1% y un 33,1% de anuncios con problema de licencia según el distrito.

Un detalle curioso que encontré: los anfitriones profesionales —aquellos con más de 50 anuncios en Barcelona— están adoptando el nuevo registro NRUA mucho más rápido que el resto: un 65,7% frente a entre un 18 y un 25% en las demás categorías. Esto no es un error de dato, es un patrón de negocio: probablemente tienen más capacidad administrativa para tramitarlo rápido.

*(sub-pestaña "Integridad referencial")*

Aquí usé SQL, no pandas, para buscar filas huérfanas: filas que mencionan un `listing_id` que ya no existe en `listings`. En `reviews` encontré 6.592, un 0,64% del total. En `calendar`, 41.245, un 0,73% — y aquí hay un detalle que me gusta mencionar porque confirma que no es un error de carga parcial: 113 alojamientos por 365 días al año da exactamente 41.245, la cifra observada. Y en esta misma dimensión, varias verificaciones salieron perfectamente limpias: los `id` de `listings` son todos únicos, `reviews` está completo al 100% en sus cuatro campos estructurales, y `calendar` está completo y sin duplicados.

*(cambias a la pestaña "Gobernanza y tratamiento")*

Cada uno de los 14 hallazgos recibió exactamente una de tres decisiones: cambio de datos —se modificó el valor—, bandera sin cambiar el valor —se marca para revisión manual pero el dato original queda intacto—, o mantener sin tratamiento —una decisión consciente de no tocarlo, no un olvido—. Y además clasifiqué la prioridad de tratamiento, que mide urgencia y no relevancia narrativa: cinco hallazgos de prioridad alta, dos de media, siete de baja.

Les voy a mostrar dos ejemplos reales de cómo se ve esto aplicado fila por fila. *(abres el expander del ejemplo 1)* El primero es la imputación de valores nulos: por ejemplo, el anuncio con id 49968 tenía `price` nulo y pasó a 216,67 euros, un valor imputado por la mediana del grupo —barrio y tipo de habitación—, nunca un precio real inventado. El anuncio 190348 tenía `bedrooms` nulo y pasó a 1, imputado por la mediana según la capacidad del alojamiento. Y dejo también un caso de control, el anuncio 18674, que ya tenía `price` completo y no cambia — para que quede claro que no estoy tocando lo que ya estaba bien.

Aquí también quiero ser honesta con una limitación que yo misma detecté: esa imputación de `bedrooms`, `bathrooms` y `beds` se agrupa solo por capacidad del alojamiento, sin distinguir si es un piso entero o una habitación privada. Medí el efecto real: afecta a 151 de los 2.562 valores de `bedrooms` imputados, un 5,9%, con un sesgo promedio de poco más de una habitación de más; en `bathrooms` y `beds` el efecto es marginal, por debajo del 1%. No lo corregí porque, a esta altura del proyecto, rehacer todo el pipeline por un efecto de ese tamaño no se justificaba — pero queda documentado como limitación conocida, no escondida.

*(abres el expander del ejemplo 2)* El segundo ejemplo es la normalización de licencias. El mismo anuncio 18674 tenía en el campo `license` un texto con etiquetas HTML sin limpiar y dos códigos de licencia pegados en la misma celda. Lo limpié, y de ese texto extraje dos columnas nuevas: los códigos HUTB detectados y la categoría de licencia. Esta regla se aplicó a los 15.293 anuncios. Una aclaración importante aquí: que detecte dos códigos no significa que ambos sean licencias vigentes — confirmar eso exigiría consultar el registro oficial, algo fuera del alcance de este dataset.

*(cambias a la pestaña "Conclusión")*

En resumen: 14 hallazgos documentados, cada uno con su decisión de gobernanza justificada. Varias verificaciones salieron limpias —no todo resultó ser un problema—. Y el hallazgo de mayor impacto de todo el proyecto no está en esta página: surge de investigar los ceros en `estimated_revenue_l365d`, que es justo lo que viene a continuación.

---

## 4 · El hallazgo crítico

Esta es la página central de mi argumento, así que le voy a dedicar tiempo.

**Primer bloque.** Encontré 2.686 anuncios —un 20,1% de los que tienen dato— donde el ingreso anual estimado aparece como cero. Una aclaración desde ya: esta variable, `revenue_no_estimable`, la creé yo para marcarlos — no viene así etiquetada de Inside Airbnb.

**Segundo bloque — de dónde sale ese ingreso estimado.** *(señalas el diagrama)* La fórmula de Inside Airbnb parte de la ocupación estimada, que se calcula a partir de las reseñas recientes y la duración de estancia; luego, el ingreso estimado es esa ocupación multiplicada por el precio. El problema aparece cuando un anuncio tiene cero reseñas recientes Y una estancia mínima de 28 noches o más: en ese caso, la fórmula no tiene con qué estimar la ocupación, y el resultado que sale es cero — pero ese cero no significa "no genera ingresos", significa "no se pudo estimar".

**Tercer bloque — cómo cambia la interpretación.** Si uno calcula la brecha de ingresos entre anfitriones particulares y profesionales sin investigar esto, sale una diferencia del 39,7%. Si excluyo esos 2.686 casos no estimables, la brecha real es del 23,1%. Es casi diecisiete puntos de diferencia, solo por entender bien un campo. En cifras concretas: sin corregir, los particulares tienen una media de 24.338 euros y los profesionales 14.678; corrigiendo, sube a 28.794 euros para particulares y 22.134 para profesionales.

**Cuarto bloque — la simulación de decisión.** Para hacerlo tangible, simulé algo muy concreto: alguien que usa `estimated_revenue_l365d` para filtrar oportunidades, y descarta automáticamente cualquier anuncio con ingreso estimado igual a cero. Quiero ser honesta: no tengo evidencia de que ningún inversor real haga esto — es un escenario hipotético, aplicado a datos cien por cien reales. Sin auditar, esa regla simple descartaría 4.181 anuncios, un 31,3% del universo de 13.355. Auditando, de esos 4.181, exactamente 2.686 —el mismo patrón de cero reseñas y estancia larga— deberían pasar a revisión manual en vez de descartarse directamente, y 1.495 sí seguirían descartados con razón. Eso es un 64,2% de los anuncios originalmente descartados que cambian de clasificación. Y si miro el perfil de esos que pasan a revisión: son más pequeños, más baratos, y con más peso de habitación privada que los que siguen descartados — un patrón compatible con alojamientos de estancia larga.

**Quinto bloque — qué se ha demostrado y qué no.** *(señalas las dos tarjetas)* Lo demostrado con datos: el cambio de clasificación es real y medible, lo calculé en vivo contra el CSV crudo. La hipótesis abierta, no demostrada: que esos anuncios generen ingresos reales, o que exista un caso de inversión real afectado por esto — no tengo datos de reservas reales, así que no lo afirmo.

---

## 5 · Diseño experimental

Para comprobar si las decisiones de curación realmente cambian algo, entrené el mismo algoritmo —Random Forest— bajo cuatro versiones distintas de los datos, separando deliberadamente el efecto de qué población se usa del efecto de cómo se construyen las variables.

*(señalas las cuatro tarjetas)* La versión A es el escenario crudo, sin auditar: 13.355 filas, los nulos rellenados con un centinela arbitrario, y los 2.686 casos no estimables contados como ingreso real cero. La versión B es el escenario tratado, el criterio principal: 10.669 filas, excluye esos 2.686 casos e imputa los nulos por capacidad del alojamiento. La versión D aísla el efecto de las variables: mantiene la misma población completa que A, 13.355 filas, pero con las variables bien construidas. Y un chequeo de sensibilidad: las mismas 10.669 filas de B, pero imputando por barrio en vez de por capacidad, solo para comprobar que la conclusión no depende del criterio exacto elegido.

*(señalas el diagrama)* A y D parten de los datos crudos; B y el chequeo de sensibilidad parten de los datos ya curados. Los tres convergen al final en una muestra común segura de 426 filas, sin fuga de datos — eso es lo que explico en la página siguiente.

Las tres comparaciones que hago con este diseño son: A contra D, que aísla el efecto puro de construir mejor las variables, porque la población es idéntica; A contra B, que combina ambos efectos —población y variables— a la vez; y la muestra común de 426 filas, que es la única evaluación verdaderamente limpia entre las tres versiones.

---

## 6 · Comparación de modelos

Con las cuatro versiones ya entrenadas, lo primero que uno haría es mirar el R² de cada una sobre su propia población de test. *(señalas el gráfico)* A tiene 0,470, D tiene 0,464, B tiene 0,439, y el chequeo de sensibilidad 0,440.

Aquí aparece la primera señal interesante: A y D, que comparten exactamente la misma población, solo se diferencian en 0,006 de R². Cambiar únicamente la construcción de las variables apenas mueve el resultado.

Pero antes de comparar A contra B tengo que señalar algo importante, y por eso esta página termina con una advertencia, no con una conclusión: A y D se evalúan sobre un conjunto de test de 2.671 filas, y B sobre uno de 2.134 filas. Son poblaciones de test distintas, así que comparar sus R² directamente, sin más, no es metodológicamente riguroso. La comparación válida la investigo en la página siguiente, que es el corazón analítico de todo el proyecto.

Antes de pasar, un chequeo de sanidad que me parece importante mencionar: en las tres versiones, Random Forest le gana claramente a la regla trivial de predecir solo la mediana de ingresos del entrenamiento. Por ejemplo, en A el error medio del modelo es de 13.309 euros frente a 19.609 euros de la mediana — así que el modelo sí está aprendiendo algo real sobre los datos, no es ruido.

---

## 7 · Resultados, robustez e interpretación

Esta es la página más importante de la presentación, así que le dedico el tiempo que haga falta.

*(estás en la pestaña "Resultados")*

**Primero, la fuga de datos.** Antes de comparar nada entre A/D y B, intenté hacer la comparación "más controlada" posible, evaluando A y D directamente contra el conjunto de test de B. El resultado que obtuve fue un R² de alrededor de 0,82 — sospechosamente alto. Investigué por qué, y encontré un problema real: el 80% de las filas de test de B, 1.708 de 2.134, ya habían sido vistas durante el entrenamiento de A y D, porque A/D y B parten de particiones de entrenamiento y test completamente independientes. Lo documento como parte del proceso, no lo escondo. Corregí usándolo la única intersección verdaderamente segura: 426 filas que no habían sido vistas por ninguno de los tres modelos.

**Segundo, de dónde viene realmente la diferencia entre A y B.** *(señalas el gráfico de 4 barras)* Evalué a A sobre toda su población —R² de 0,470— y también solo sobre la población limpia —R² de 0,434—; evalué a D solo sobre la población limpia —0,428—; y a B sobre su propia población limpia —0,439—. La conclusión es clara: cambiar solo las variables, A contra D, mueve el R² apenas 0,006. Cambiar solo la población evaluada mueve el R² entre 0,036 y 0,04 — un efecto seis a siete veces mayor. El factor dominante es qué población se evalúa, no cómo se construyen las variables.

**Tercero, la comparación sobre la muestra común de 426 filas.** Aquí la progresión es: A con 0,348, D con 0,388, B con 0,448 — mejora en cada paso, primero solo por las variables, luego también por la población. Antes de confiar en esta muestra pequeña, comprobé su representatividad en precio mediano, capacidad media y mezcla de tipo de habitación frente al universo de 2.131 filas — es una comprobación útil de composición, no una prueba de que no exista ningún sesgo en otras variables que no revisé.

**Un chequeo adicional de sensibilidad:** si cambio el criterio de imputación —por barrio en vez de por capacidad— la diferencia es de apenas 10,5 euros de error medio, un 0,07% relativo — la conclusión del modelo no depende de cuál de los dos criterios razonables uso.

**Y sobre importancia de variables:** las mismas ocho variables dominan en las tres versiones — cosas como el número de amenities, la escala del anfitrión, si es superhost, la capacidad del alojamiento. Ninguna variable geográfica específica entra en ese top ocho. Y lo digo con cuidado: que una variable sea importante en un Random Forest no demuestra que la cause el resultado, es una contribución predictiva dentro del modelo, no un efecto causal verificado.

*(cambias a la pestaña "Confianza y conclusión")*

**Cuarto, cuánta confianza hay en todo esto.** Detecté algo que tuve que investigar a fondo antes de aceptar cualquier cifra: en la muestra grande, de 2.131 filas, A y D difieren solo 0,006 en R². Pero en la muestra pequeña, de 426 filas, difieren 0,04 — varias veces más, y con el signo invertido. Para entender esto, hice dos cosas.

La primera: tomé 5.000 submuestras aleatorias de 426 filas del mismo universo de 2.131, reutilizando las predicciones ya calculadas, sin reentrenar nada. La media de esas diferencias simuladas fue de 0,0060, con una desviación de 0,0213. El resultado real que observé, menos 0,0405, cae en el percentil 1,2 de esa distribución — es decir, aproximadamente solo 1 de cada 80 submuestras aleatorias produce algo igual de extremo. Es un resultado poco habitual, y la variabilidad de la muestra es la explicación más simple y mejor respaldada que tengo, pero no es una prueba definitiva de que no exista ningún otro efecto.

La segunda: un bootstrap emparejado de 5.000 repeticiones, remuestreando A, D y B exactamente sobre las mismas filas en cada vuelta. El resultado: la diferencia A menos D, solo variables, tiene un intervalo de confianza que incluye el cero — no es concluyente por sí sola. La diferencia D menos B, solo población, también incluye el cero. Pero la diferencia A menos B, el efecto combinado, el hallazgo principal de todo este bloque, tiene un intervalo que va de menos 0,2478 a menos 0,0043 — no incluye el cero. Es decir, se distingue de cero, aunque el límite superior está bastante cerca.

**La conclusión de esta sección**, y quiero decirla con las tres partes bien separadas: lo observado es que, en la única comparación sin fuga de datos, sobre 426 filas no vistas por ningún modelo, el modelo tratado predice mejor que el crudo, con un intervalo que respalda que esto no es casualidad. La interpretación razonable es que esa mejora probablemente viene tanto de la población —menos casos triviales de cero euros— como de las variables, y ambos efectos van en la misma dirección. Y lo que sigue sin resolver es que no puedo repartir con precisión qué proporción exacta corresponde a cada causa — resolver eso exigiría una muestra común mucho mayor que estas 426 filas.

---

## 8 · Conclusiones y recomendaciones

Reúno todo en cuatro niveles de certeza distintos, para no mezclar lo que demostré con lo que es solo una interpretación razonable.

*(pestaña "Hallazgos demostrados")* Lo que puedo defender con evidencia directa: la brecha particular-profesional cambia de 39,7% a 23,1% al investigar los 2.686 ceros no reales; sobre las 426 filas sin fuga, el modelo tratado tiene mejor R² que el crudo, con un intervalo que lo respalda; la imputación de bedrooms, bathrooms y beds no depende de cuál de los dos criterios razonables use, la diferencia es menor al 0,1% en el error; y detecté y corregí una fuga de datos real en el propio diseño de mi experimento.

*(pestaña "Interpretaciones razonables")* Lo que es compatible con los datos pero no está demostrado al cien por cien: que la mejora de B venga tanto de la población como de las variables, en la misma dirección, sin poder repartir la proporción exacta; que la discrepancia entre la muestra pequeña y la grande se explique por el tamaño de la muestra, que es la explicación más simple y mejor respaldada, pero no una prueba definitiva; y que los profesionales adopten el nuevo registro NRUA más rápido por tener más capacidad administrativa, algo compatible pero que no investigué directamente.

*(pestaña "Limitaciones")* En resumen: la validación sin fuga usa solo 426 filas, suficiente para el efecto combinado pero no para separar población de variables; el target es una estimación de Inside Airbnb, no un ingreso real observado; y el experimento cubre un solo dataset y un solo algoritmo. El detalle completo, con siete puntos, está en la página de metodología.

*(pestaña "Recomendaciones")* Y termino con siete recomendaciones de alcance general, transferibles a cualquier proyecto de datos: investigar la semántica de las variables antes de tratar sus valores —el caso de los 2.686 ceros no se habría encontrado solo mirando el porcentaje de nulos—; documentar las reglas de limpieza con la misma trazabilidad que una decisión de negocio; separar explícitamente valores desconocidos de ceros reales; evitar fugas entre entrenamiento y evaluación, sobre todo al comparar modelos entrenados sobre poblaciones de origen distintas; usar conjuntos de comparación equivalentes al evaluar dos versiones de un modelo; registrar las transformaciones para garantizar reproducibilidad; y revisar la calidad de los datos antes de interpretar las métricas de un modelo, no después.

*(bajas a la tabla final, fuera de las pestañas)* Para cerrar, quiero distinguir con cuidado cuatro niveles de certeza sobre qué decisión podría cambiar y qué evidencia tengo. El hallazgo observado —la brecha de 39,7% a 23,1%— está medido. El resultado del experimento —el R² de 0,348 a 0,448— está medido. El cambio de clasificación simulado —2.686 anuncios que pasarían a revisión, un 64,2% de los descartados— está medido con datos reales, pero sobre un escenario hipotético. Y el impacto económico real no está observado: no tengo datos de reservas o ingresos reales, ni un caso de inversión documentado que lo mida.

Por eso quiero remarcar algo antes de cerrar: no estoy afirmando que haya probado que Airbnb o un anfitrión real tomaron una decisión equivocada. Formulo la conclusión en términos de riesgo analítico: tomar decisiones sobre datos sin auditar es arriesgado, y en este caso, ese riesgo se puede medir con cifras reales — eso es distinto de haber demostrado ya un error concreto.

Y cierro con esto: la calidad de los datos no se reduce al porcentaje de valores nulos — y una diferencia en las métricas, por sí sola, nunca demuestra un impacto empresarial real sin investigar qué la produce.

---

## 9 · Metodología y limitaciones

*(esta página normalmente no se lee entera en voz alta — es para responder con precisión si alguien pregunta un detalle técnico)*

Si me preguntan algo muy específico durante el turno de preguntas, aquí está la respuesta exacta: el target es `estimated_revenue_l365d`; excluí como predictoras `price`, `estimated_occupancy_l365d`, el número de reseñas y sus variantes, y `minimum_nights`, porque forman parte de la propia fórmula con la que se calcula el target — usarlas sería hacer trampa al modelo. Las predictoras que sí uso son tipo de habitación, tipo de propiedad, barrio, capacidad, dormitorios, baños, camas, el tamaño del anfitrión en dos escalas distintas, si es superhost, y el número de amenities. El algoritmo es un `RandomForestRegressor` con 200 árboles, semilla aleatoria fija en 42, y una partición de entrenamiento y test de 80/20, también con semilla 42. El baseline de comparación es simplemente predecir la mediana del entrenamiento.

Y las seis limitaciones completas que reconozco abiertamente: el tamaño de la muestra común de 426 filas; que el target es una estimación, no un ingreso real observado; que los intervalos de confianza de los efectos parciales incluyen el cero; que el experimento cubre un solo dataset y un solo algoritmo; una fuga leve en la imputación del modelo D, porque la mediana se calculó sobre todo el dataframe antes de dividir en entrenamiento y test —la misma práctica que ya existía en el tratamiento original—; y que la imputación de dormitorios, baños y camas no distingue tipo de habitación.

---

## Preguntas probables del público — para estudiar antes, no para leer en la presentación

**Sobre el caso Zillow y la pregunta de investigación**
- *¿Por qué Zillow y no un caso de Airbnb?* — No encontré un caso de negocio real y documentado de alguien usando mal los datos de Inside Airbnb; por eso en la página de impacto hablo de "riesgo analítico" y no afirmo que haya ocurrido un error real. Zillow es el precedente real que justifica por qué este tipo de auditoría importa.
- *¿Esto significa que el dataset de Airbnb está mal?* — No parto de esa premisa. Audito primero y dejo que los datos muestren si hay un problema — de hecho varias verificaciones salieron limpias.

**Sobre contexto y herramientas**
- *¿Por qué Barcelona?* — Es el recorte geográfico del dataset público de Inside Airbnb que usé, no una decisión metodológica mía.
- *¿Por qué SQLite y no solo pandas?* — Por rendimiento: `calendar` tiene 5,6 millones de filas, y un `LEFT JOIN` en SQL es mucho más eficiente que hacerlo en pandas para ese volumen.

**Sobre la auditoría**
- *¿Por qué mediana y no media para imputar?* — Es menos sensible a valores extremos, y agrupé por las variables más relacionadas con cada campo en vez de usar una mediana global.
- *¿Por qué no corregisteis la limitación del `room_type` en la imputación?* — Medí el efecto real antes de decidir: solo 5,9% de los `bedrooms` imputados, sesgo promedio de poco más de una habitación, marginal en el resto. No se justificaba rehacer el pipeline completo por eso, pero quedó documentado.
- *¿El campo `license` no verificable significa que son ilegales?* — No. Significa que no se puede confirmar desde el dataset si tienen licencia — no asumo incumplimiento legal.
- *¿Qué es NRUA?* — El registro turístico único estatal, obligatorio desde julio de 2025, que convive con el HUTB catalán sin sustituirlo.

**Sobre el hallazgo crítico**
- *¿Por qué 28 noches como umbral?* — No lo inventé yo: es el patrón de estancia de larga duración que hace que la fórmula de ocupación de Inside Airbnb no tenga reseñas recientes con qué trabajar.
- *¿Esos 2.686 anuncios generan ingresos reales entonces?* — No lo sé, y lo digo explícitamente: no hay datos de reservas reales en este dataset. Demuestro que "no estimable" no es lo mismo que "cero real", no que sí generen ingresos.
- *¿Verificaste que los 2.686 de las dos páginas son los mismos anuncios?* — Sí, comparé los IDs directamente: son exactamente el mismo conjunto.
- *¿Por qué no borrar esos 2.686 casos?* — Borrar perdería información real; por eso se marcó con una bandera en vez de borrar o inventar un valor.

**Sobre el diseño experimental y la comparación de modelos**
- *¿Por qué hay modelo D y no C?* — Es la nomenclatura que fue surgiendo con el experimento; D ocupa el lugar que aísla el efecto de las variables manteniendo la población de A.
- *¿Por qué no comparar A y B directamente desde el principio?* — Porque cambia dos cosas a la vez, población y variables; sin un punto intermedio como D no podría saber de dónde viene la mejora.
- *Si A y D casi no cambian, ¿para qué sirvió tratar las variables?* — Precisamente para demostrar que el efecto grande no viene de ahí — viene de la población, como se ve en la siguiente página.

**Sobre resultados y robustez (las más difíciles, hay que tenerlas muy claras)**
- *¿Por qué no usar una muestra más grande para más confianza?* — 426 es el máximo que cumple no haber sido visto por ninguno de los tres modelos; ampliarla exigiría rediseñar el experimento desde el split original.
- *El intervalo de A-B casi toca el cero, ¿no es un resultado débil?* — Es real, pero lo señalo como "evidencia real, no una certeza absoluta" — por eso distingo "lo observado" de "lo que sigue sin resolver".
- *¿La fuga de datos no afecta a la credibilidad del proyecto?* — Al contrario: estaba en el diseño del experimento, no en los datos auditados, y se detectó y corrigió antes de reportar nada — es el mismo rigor que defiendo en todo el proyecto.
- *¿Qué significa el percentil 1,2?* — Que, de 5.000 muestras aleatorias del mismo universo, solo alrededor de 1 de cada 80 produce una diferencia tan extrema como la real — un resultado inusual, no imposible.
- *¿Por qué ninguna variable geográfica entra en el top 8 de importancia?* — Es lo que muestran los datos dentro de este modelo y estas variables concretas; no significa que la geografía no influya en el precio real.

**Sobre conclusiones**
- *¿Por qué distinguir "hallazgo observado" de "cambio de clasificación simulado"?* — Son niveles de certeza distintos: los dos primeros están medidos directamente; la simulación aplica una regla hipotética —nadie confirmó que un inversor real la use— a esos mismos datos reales.
- *¿Cuál es la recomendación más importante?* — Para mí, investigar la semántica de las variables antes de tratar sus valores: el caso de los 2.686 ceros no se habría encontrado solo mirando el porcentaje de nulos.

**Sobre metodología**
- *¿Por qué excluisteis `price` como predictora?* — Forma parte de la propia fórmula del target; usarla sería fuga de información.
- *¿Por qué Random Forest?* — Es una decisión estándar para este tipo de problema —relación no lineal, variables mixtas, robusto a outliers—; lo puedo explicar verbalmente, pero no lo convertí en contenido de la demo porque no aportaba al hallazgo central.
- *¿La app reentrena los modelos cada vez que la abres?* — No, usa resultados precalculados y guardados, excepto la simulación de decisión de la página 4, que sí se calcula en vivo contra el CSV crudo.

**Preguntas generales que pueden salir en cualquier momento**
- *¿Cuál es el hallazgo más importante, en una frase?* — Un campo que parecía un simple "0 euros" mezclaba ingresos reales con casos no estimables, y esa confusión cambia una conclusión de negocio medible y el rendimiento de un modelo predictivo, sin tocar ni una fila de datos obviamente sucios.
- *¿Qué harías distinto con más tiempo?* — Ampliar la muestra común más allá de 426 filas para repartir con precisión el efecto de población y variables, y corregir la limitación de `room_type` en la imputación.
- *¿Por qué confiar en tus propios números?* — Todas las cifras están verificadas contra los CSV originales o calculadas en vivo con scripts guardados en la raíz del proyecto — cada bloque cita su fuente.
- *¿Esto es generalizable a otras ciudades?* — No se ha probado; es una limitación reconocida explícitamente: un solo dataset, un solo algoritmo.

---

*Nota: este guion se preparó revisando el contenido real de las 9 páginas de la app Streamlit, incluidas todas sus sub-pestañas, a fecha 2026-10-29, cruzando cada cifra contra los archivos de datos y el código de los notebooks. Si cambias algo después de esta fecha, confirma la cifra en la app antes de memorizarla de nuevo.*
