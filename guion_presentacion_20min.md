# DataTrust — guion recortado para 20 minutos

Versión corta del guion completo (`guion_presentacion_completo.md`), pensada para caber en 20 minutos reales de presentación. Cálculo: ~1.910 palabras de texto hablado, a un ritmo de ~130 palabras/minuto son ~14-15 minutos de habla; sumando cambios de pestaña, carga de gráficos y pausas naturales, queda en torno a 19-20 minutos. Deja algo de margen — no lo agotes todo, así tienes aire si una pregunta espontánea te interrumpe.

Qué se recortó y por qué: se mantiene prácticamente intacta la página 7 (Resultados y robustez, el corazón del proyecto) y el hallazgo crítico (página 4). Se recortó detalle secundario en Contexto (lista de herramientas una por una), en Auditoría (el detalle de L6/L7 sobre NRUA por distrito, parte de la narración de los dos ejemplos) y en Conclusiones (se resumen las 4 pestañas en lugar de narrarlas una por una). La página 9 (Metodología) y las preguntas probables **no se repiten aquí** — siguen solo en el guion completo, porque no se leen en vivo.

Los paréntesis en *cursiva* son acotaciones para ti, no se leen en voz alta.

---

## 1 · Inicio

Antes de hablar de mi proyecto, el caso Zillow: la mayor plataforma inmobiliaria de Estados Unidos. En noviembre de 2021 cerraron su división de compra-venta automatizada de viviendas, Zillow Offers, y recortaron el 25% de la plantilla. Su algoritmo sobreestimó el valor de reventa de las casas que compraban, lo que les costó 881 millones de dólares de pérdida en el año. El propio CEO dijo: "la imprevisibilidad al pronosticar precios de vivienda superó ampliamente lo que anticipamos". No fue un modelo roto — fue un modelo que confió en datos sin entenderlos del todo.

Mi proyecto parte de la misma pregunta: ¿puede la calidad de los datos cambiar las conclusiones de un análisis, incluso cuando el modelo parece funcionar bien? No parto asumiendo que los datos de Airbnb Barcelona están mal — los audito primero. Como adelanto: encuentro 2.686 casos, un 20,1%, donde el ingreso estimado aparece como cero sin serlo realmente, y al corregirlo, un modelo predictivo mejora de forma medible, el R² sube de 0,348 a 0,448. La calidad de los datos no se reduce al porcentaje de nulos — eso es lo que voy a demostrar.

---

## 2 · Contexto del proyecto

Los datos vienen de Inside Airbnb, un proyecto independiente de la empresa Airbnb, con fines de transparencia. Trabajo con tres tablas: anuncios, 15.293 filas; reseñas, más de un millón; y calendario, 5,6 millones de filas —esta última la trabajo con SQL, no con pandas, por su volumen—. *(señalas el mapa)* El análisis se centra en Barcelona, donde los anuncios se concentran de forma muy desigual por distrito.

El proyecto tiene cinco objetivos —auditar, priorizar, curar con justificación, y comparar el efecto en una conclusión de negocio y en un modelo predictivo— y cada uno se resuelve en una página distinta de esta app. Usé herramientas estándar de ciencia de datos: Python y pandas para la limpieza, SQLite para integridad referencial, scikit-learn para el modelo, y Plotly y Streamlit para toda la visualización. El flujo es: auditoría, gobernanza, tratamiento, y luego dos comparaciones en paralelo — negocio y modelo.

---

## 3 · Auditoría de calidad

Revisé las tres tablas contra tres preguntas: ¿falta información?, ¿las filas conectan bien entre tablas?, y ¿un valor válido tiene sentido real? Encontré 14 hallazgos en total: ocho en `listings`, cuatro en `reviews`, dos en `calendar`. No todo es un problema — `reviews` y `calendar` salieron 100% completas, y los `id` de `listings` no tienen duplicados.

*(sub-pestaña "Plausibilidad")* El hallazgo más ilustrativo es el campo `license`: un 21,1% no es verificable, y 5.470 registros tienen el formato roto, con HTML sin limpiar o dos licencias concatenadas. El dataset mezcla dos registros: `HUTB`, el catalán histórico, y `NRUA`, el nuevo registro estatal obligatorio desde julio de 2025 — convive con el HUTB, no lo sustituye.

*(sub-pestaña "Integridad referencial")* También usé SQL para encontrar filas huérfanas: 6.592 en `reviews`, 41.245 en `calendar` — en este último, 113 alojamientos por 365 días da exactamente esa cifra, lo que confirma que no es un error de carga.

*(pestaña "Gobernanza y tratamiento")* Cada hallazgo recibió una decisión: cambio de datos, bandera sin cambiar el valor, o mantener sin tratamiento consciente. Les muestro dos ejemplos reales. Primero, imputación de nulos: un anuncio con `price` nulo pasó a 216,67 euros, imputado por la mediana del grupo — nunca un precio inventado. Aquí también soy honesta con una limitación que yo misma detecté: esa imputación no distingue tipo de habitación, lo que afecta al 5,9% de los `bedrooms` imputados — medí el efecto y es pequeño, por eso no rehice todo el pipeline, pero queda documentado. Segundo ejemplo, normalización de licencias: limpié el HTML y extraje los códigos y la categoría de licencia, aplicado a los 15.293 anuncios.

*(pestaña "Conclusión")* El hallazgo de mayor impacto de todo el proyecto no está aquí: surge de investigar los ceros en `estimated_revenue_l365d`, que es lo que viene a continuación.

---

## 4 · El hallazgo crítico

Esta es la página central de mi argumento. Encontré 2.686 anuncios —un 20,1%— donde el ingreso anual estimado aparece como cero. Esta variable, `revenue_no_estimable`, la creé yo para marcarlos, no viene así de Inside Airbnb.

*(señalas el diagrama)* La fórmula de Inside Airbnb calcula el ingreso como la ocupación estimada —a partir de reseñas y duración de estancia— multiplicada por el precio. El problema: cuando un anuncio tiene cero reseñas recientes Y una estancia mínima de 28 noches o más, la fórmula no tiene con qué estimar la ocupación, y el resultado es cero — pero ese cero significa "no se pudo estimar", no "no genera ingresos".

Si calculo la brecha de ingresos entre particulares y profesionales sin investigar esto, sale un 39,7% de diferencia. Si excluyo esos 2.686 casos, la brecha real es del 23,1% — casi diecisiete puntos de diferencia solo por entender bien un campo.

Para hacerlo tangible, simulé algo concreto: alguien que descarta automáticamente cualquier anuncio con ingreso estimado igual a cero. No tengo evidencia de que un inversor real haga esto — es un escenario hipotético sobre datos reales. Sin auditar, esa regla descartaría 4.181 anuncios, un 31,3% del universo. Auditando, 2.686 de esos —el mismo patrón— deberían pasar a revisión en vez de descartarse, y 1.495 sí seguirían descartados con razón: un 64,2% de los originalmente descartados cambia de clasificación.

Lo demostrado con datos: el cambio de clasificación es real y medible. La hipótesis abierta, no demostrada: que esos anuncios generen ingresos reales — no tengo datos de reservas reales, así que no lo afirmo.

---

## 5 · Diseño experimental

Para comprobar si la curación cambia algo, entrené el mismo Random Forest bajo cuatro versiones de los datos, separando el efecto de la población del efecto de las variables. A es el crudo, 13.355 filas. B es el tratado principal, 10.669 filas, excluye los 2.686 casos e imputa por capacidad. D aísla el efecto de las variables: misma población que A, pero bien construidas. Y un chequeo de sensibilidad que imputa por barrio en vez de capacidad, para comprobar que la conclusión no depende del criterio exacto.

Las tres comparaciones son: A contra D, que aísla el efecto de las variables; A contra B, que combina ambos efectos; y una muestra común de 426 filas, sin fuga de datos, que es la única comparación verdaderamente limpia — eso lo explico en la página central del proyecto.

---

## 6 · Comparación de modelos

Con las cuatro versiones entrenadas, el R² de cada una sobre su propia población de test es: A 0,470, D 0,464, B 0,439, sensibilidad 0,440. A y D, que comparten población, solo difieren en 0,006 — cambiar las variables apenas mueve el resultado.

Pero A y B se evalúan sobre conjuntos de test distintos —2.671 filas contra 2.134— así que comparar sus R² directamente no es riguroso. Esa comparación válida la hago en la siguiente página, el corazón analítico del proyecto. Un chequeo rápido: en las tres versiones, Random Forest le gana claramente a predecir solo la mediana, así que el modelo sí aprende algo real.

---

## 7 · Resultados, robustez e interpretación

Esta es la página más importante. *(pestaña "Resultados")*

**Primero, la fuga de datos**: al comparar A y D contra el test de B obtuve un R² de 0,82, sospechosamente alto. Investigué y encontré que el 80% de las filas de test de B, 1.708 de 2.134, ya habían sido vistas en el entrenamiento de A y D. Lo documento como parte del proceso. Corregí usando la única intersección segura: 426 filas no vistas por ninguno de los tres modelos.

**Segundo, de dónde viene realmente la diferencia entre A y B**: evaluando todo sobre la misma población limpia, cambiar solo las variables mueve el R² apenas 0,006; cambiar solo la población lo mueve entre 0,036 y 0,04 — un efecto seis a siete veces mayor. El factor dominante es qué población se evalúa, no cómo se construyen las variables.

**Tercero, sobre la muestra común de 426 filas**, la progresión es clara: A 0,348, D 0,388, B 0,448 — mejora en cada paso. Comprobé que estas 426 filas son representativas del universo en precio, capacidad y tipo de habitación. Y un chequeo de sensibilidad confirma que cambiar el criterio de imputación apenas mueve 10,5 euros de error — la conclusión no depende de eso.

*(pestaña "Confianza y conclusión")* **Cuarto, cuánta confianza hay en esto**: detecté que en la muestra grande A y D difieren solo 0,006, pero en la pequeña de 426, difieren 0,04 — lo investigué con dos métodos. Simulé 5.000 submuestras de 426 filas del mismo universo: el resultado real cae en el percentil 1,2, es decir, poco habitual, aunque no es una prueba definitiva. Y con un bootstrap de 5.000 repeticiones: la diferencia A contra B, el efecto combinado, tiene un intervalo que no incluye el cero — se distingue de cero. Pero los efectos parciales, solo variables o solo población, por separado sí incluyen el cero — no puedo repartir con precisión cuánto corresponde a cada causa.

**La conclusión**: lo observado es que el modelo tratado predice mejor que el crudo, con un intervalo que lo respalda. La interpretación razonable es que la mejora viene de ambos efectos juntos. Y lo que sigue sin resolver es el reparto exacto entre esas dos causas.

---

## 8 · Conclusiones y recomendaciones

Reúno todo en cuatro niveles de certeza. Lo demostrado: la brecha cambia de 39,7% a 23,1%; sobre las 426 filas sin fuga, el modelo tratado tiene mejor R² con un intervalo que lo respalda; la imputación no depende del criterio usado; y detecté y corregí una fuga de datos real en mi propio experimento.

Interpretación razonable, no demostrada al cien por cien: que la mejora venga de ambos efectos juntos, y que la discrepancia entre muestras se explique por tamaño de muestra — la explicación más simple, no una prueba definitiva.

Limitaciones, en resumen: la validación sin fuga usa solo 426 filas, el target es una estimación de Inside Airbnb, no un ingreso real observado, y el experimento cubre un solo dataset y un solo algoritmo.

Y cierro con la recomendación que más destaco: investigar la semántica de las variables antes de tratar sus valores — el caso de los 2.686 ceros no se habría encontrado solo mirando el porcentaje de nulos.

Para terminar, cuatro niveles de certeza sobre el impacto: el hallazgo observado y el resultado del experimento están medidos; el cambio de clasificación simulado está medido pero sobre un escenario hipotético; y el impacto económico real no está observado — no tengo datos de reservas reales. No afirmo que Airbnb o un anfitrión real tomaran una decisión equivocada — hablo de riesgo analítico medible, no de un error ya demostrado.

Y cierro con esto: la calidad de los datos no se reduce al porcentaje de valores nulos — una diferencia en las métricas, por sí sola, nunca demuestra un impacto real sin investigar qué la produce.

---

*Para la página 9 (Metodología y limitaciones) y el bloque completo de preguntas probables del público, consulta `guion_presentacion_completo.md` — no se repiten aquí porque no se leen en vivo, pero sigue siendo el material de estudio para el turno de preguntas.*
