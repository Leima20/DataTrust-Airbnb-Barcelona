# DataTrust — Plan del proyecto

**No es un entregable oficial** — es un documento de apoyo para explicar el proyecto de forma clara, sin código ni tecnicismos innecesarios.

## ¿De qué trata el proyecto?

Es una auditoría de calidad de datos sobre Airbnb Barcelona. Reviso si los datos públicos están bien o tienen errores, antes de usarlos para sacar conclusiones de negocio.

## ¿Qué voy a demostrar?

Que si no revisas los datos antes de usarlos, las conclusiones que saques pueden estar mal — con un caso real y números concretos, no en teoría.

## ¿Cuál es el problema? (los errores encontrados, en detalle)

Esta parte es la **auditoría**. Encontré 14 **hallazgos de calidad**, repartidos en las tres tablas de datos (`listings`, `reviews`, `calendar`):

**En los alojamientos:**
- 12 columnas completamente vacías (0% de datos en toda la tabla).
- El campo de licencia turística: 21,1% de los anuncios sin un dato verificable. Además, España creó en julio de 2025 un registro de licencias nuevo (el NRUA), distinto del catalán (HUTB) que ya existía. Si un análisis no reconoce el formato de este registro nuevo, puede contar como "sin licencia" a anuncios que en realidad sí la tienen correctamente — en mis datos, eso afecta a 948 anuncios (6,2% del total). Esto demuestra que auditar un campo normativo no es algo que se hace una sola vez: hay que revisarlo cada vez que cambia la ley.
- Precio: falta en el 12,7% de los anuncios.
- Dormitorios, baños, camas: faltan en 16-23%.

**En las reseñas:**
- 6.592 reseñas "huérfanas" (ligadas a un alojamiento que ya no existe en los datos).
- 48.302 reseñas duplicadas exactas.
- 512 veces que la misma persona dejó el mismo texto en alojamientos distintos (en 452 combinaciones de persona+texto).
- 9.917 reseñas de menos de 5 caracteres.

**En el calendario:**
- 41.245 filas huérfanas (hallazgo formal, con umbral objetivo — igual que los demás de esta lista).
- 746 filas con `minimum_nights` mayor que `maximum_nights` (una contradicción lógica imposible, en solo 6 alojamientos) — este es el otro hallazgo formal de la tabla `calendar`, no lo había puesto antes en esta lista.
- *(Observación, no un hallazgo formal con umbral objetivo, a diferencia de los dos de arriba)*: el 26,3% de las filas tiene `maximum_nights = 1.125` — un valor que se repite demasiado para ser decisión de cada anfitrión, compatible con un valor de relleno automático de la plataforma, pero el dataset no permite confirmar su significado exacto. Por eso el propio notebook lo documenta como observación, no lo cuenta junto a los hallazgos con certeza confirmada.

**El error más grave, el que más consecuencias tiene:**
**Importante: esto no es un cálculo de Airbnb la empresa, es un cálculo de Inside Airbnb** (la fuente de datos pública que uso, un proyecto independiente, no afiliado a Airbnb). Inside Airbnb estima cuánto gana un alojamiento a partir de las reseñas recientes, porque no tiene acceso a los datos reales de reservas de Airbnb. En los alojamientos de estancia larga (un mes o más) que estudié, casi nunca hay reseñas — el 78% de ellos no tiene ninguna reseña en toda su historia en la plataforma, no solo recientemente. No tengo forma de confirmar con estos datos si es porque de verdad están ocupados por inquilinos que no reseñan, o porque tienen poca demanda real — pero en cualquiera de los dos casos, el sistema calcula "0€ de ingreso" para ellos, y esto afectaba a más de la mitad de los anfitriones que gestionan muchos alojamientos. Quien sufre las consecuencias de este error es quien consulte estos datos públicos (investigadores, periodistas, analistas) — no Airbnb la empresa, que tiene sus propios datos reales de reservas, sin este problema.

## ¿Cómo se soluciona?

**Primero, la <span style="color:#2a78d6">gobernanza de datos</span>.** Es la etapa donde, para cada uno de los
14 hallazgos, se decide qué hacer con él — antes de tocar ningún dato. No es
solo "arreglarlo": para cada hallazgo se evalúa el **riesgo** que tiene (qué
tan grave es si se ignora), se le asigna una **prioridad** (alta, media o
baja, según ese riesgo), y se toma una **decisión** con su **justificación**
por escrito — por qué se eligió esa opción y no otra. Esto queda documentado
en una tabla completa (notebook 04), uno de los entregables técnicos del
proyecto.

Las decisiones posibles son siempre una de estas tres: ¿se ignora el
problema (porque no afecta al análisis), se corrige directamente, o se marca
con una columna nueva sin tocar el dato original (cuando corregirlo de
verdad significaría inventar información que no se tiene)? Ningún hallazgo
se trata igual por costumbre — cada uno pasa por esa pregunta. Algunos
ejemplos:
- Las columnas vacías: se eliminan.
- Las reseñas huérfanas: se excluyen.
- El error del ingreso en 0€: no se borra ni se inventa un valor — el dato
  original de `estimated_revenue_l365d` se queda exactamente igual. Lo que
  se hace es añadir una columna nueva, `revenue_no_estimable`, con un valor
  **True o False** por cada anuncio: True solo cuando se cumplen las dos
  señales juntas (cero reseñas recientes Y estancia mínima larga), False en
  todos los demás casos. Esa columna es la que luego se usa para excluir
  esos anuncios de un cálculo cuando hace falta, sin tocar ni perder el dato
  original — para no corregir de más ni de menos.

**Después, el tratamiento (o curación) de datos**: ejecutar esas decisiones
sobre los datos reales, para producir una versión "limpia" que se pueda
comparar contra la original.

**Por último, mido el impacto de haber hecho esto, en dos sitios distintos:**
- **Impacto en negocio**: cuánto parece ganar un anfitrión "profesional"
  (gestiona muchos alojamientos) frente a uno "particular", antes y después
  de tratar los datos — la diferencia baja de 39,7% a 23,1%.
- **Impacto en el modelo**: ver la sección siguiente, completa.

## El modelo predictivo — qué es, cómo funciona, y qué resultado da

**¿Por qué justo este modelo, y no otro?** Porque predice exactamente el
mismo dato que tiene el problema del 0€ (`estimated_revenue_l365d`). Si
entreno el modelo con los datos sin tratar, le estoy enseñando con miles de
ejemplos equivocados — alojamientos ocupados y rentables etiquetados como
"ganan 0€" solo por el error ya explicado (estancias largas, pocas reseñas).
El modelo podría aprender un patrón falso a partir de esos ejemplos. Por eso
se usa la misma corrección (`revenue_no_estimable`) en los dos sitios del
proyecto: en el caso de negocio, para no promediar ingresos falsos; en el
modelo, para no entrenarlo con ejemplos falsos. No son dos análisis sueltos
que casualmente comparten tema — es el mismo error de datos, aplicado a dos
formas distintas de usar esa información.

El modelo intenta adivinar **cuánto va a ganar un alojamiento al año**,
mirando solo sus características (tipo de propiedad, número de habitaciones,
capacidad, barrio, si el anfitrión tiene muchos anuncios, etc.) — sin que
nadie le diga el resultado de antemano.

**¿Cómo funciona, en términos simples?** Le doy al modelo miles de
alojamientos de los que SÍ sé cuánto ganan, para que aprenda el patrón entre
las características y el ingreso. Después le pido que use ese patrón
aprendido para calcular el ingreso de otros alojamientos, y comparo su
cálculo contra el valor real, para ver qué tan acertado es. 

El algoritmo que uso se llama Random Forest — es uno de los métodos más usados para este tipo
de predicción, porque combina muchos "árboles de decisión" pequeños y
promedia sus resultados.

**¿Por qué lo hago dos veces, con dos formas distintas de limpiar?** Para
comprobar que mi conclusión no depende de una elección arbitraria. Entreno el
mismo modelo tres veces: una con los datos sin tratar, y dos con los datos
tratados, cambiando solo el criterio usado para rellenar los datos
faltantes de habitaciones/baños/camas:
- **Criterio A**: rellenar con la mediana según la capacidad del alojamiento (`accommodates`).
- **Criterio B**: rellenar con la mediana según el barrio (`neighbourhood_cleansed`).

Si las dos versiones tratadas dan un resultado parecido entre sí, significa que
la conclusión es sólida, no una casualidad de cómo decidí limpiar los datos.

**¿Cómo mido si el modelo es bueno?** Con dos métricas:
- **MAE** (*Mean Absolute Error*, error absoluto medio): el **error promedio
  en euros** — cuánto se equivoca el modelo, de media, al calcular el
  ingreso de un alojamiento (más bajo es mejor).
- **R²** (coeficiente de determinación): un **puntaje de 0 a 1** que indica
  qué porcentaje de las diferencias entre alojamientos logra explicar el
  modelo (más alto es mejor, en teoría).

**El resultado, y por qué es contraintuitivo:** el modelo entrenado con datos
tratados tiene un puntaje más bajo (peor, en apariencia) que el entrenado con
datos sin tratar. Esto parece malo, pero no lo es: el modelo con datos sin
tratar incluía miles de casos de "0€ de ingreso" que eran fáciles de adivinar
(porque eran el error que ya expliqué arriba, no un ingreso real) — eso
inflaba artificialmente su puntaje. Al quitar esos casos falsos, el modelo
se enfrenta a una prueba más difícil y honesta, así que su puntaje baja,
aunque el modelo en sí no esté peor construido. Un modelo con puntaje más
bajo pero sin datos falsos es más confiable que uno con puntaje alto inflado
por un error.

**Pero esa primera explicación no bastaba, y fui más allá.** Decir "el
modelo tratado tiene peor puntaje porque se le evalúa con una prueba más
difícil" es una buena explicación, pero deja una pregunta sin responder:
¿y si en vez de comparar cada modelo con su propia prueba, los pongo a los
dos a resolver exactamente la misma prueba? Esa es la única forma de saber,
de verdad, cuál predice mejor.

Hacerlo bien fue más difícil de lo que esperaba, y aquí es donde está, para
mí, la parte más honesta de todo el proyecto:

- **Primer intento, con un error real que detecté yo misma**: comparé los
  dos modelos usando las mismas filas de prueba de uno de ellos. El
  resultado salió sospechosamente bueno — demasiado bueno. Antes de
  reportarlo, lo comprobé: el 80% de esas filas ya las había visto uno de
  los modelos durante su propio entrenamiento. Es como corregir un examen
  con las respuestas ya filtradas — el resultado se ve bien, pero no
  significa nada. Lo descarté y lo corregí.
- **La comparación corregida**: usé solo las filas que ninguno de los dos
  modelos había visto nunca, ni para entrenar ni para su propia prueba — en
  este caso, 426 alojamientos. Con esa comparación limpia, **el modelo
  tratado predice mejor que el crudo**, no solo "se mide con más honestidad"
  — de verdad se equivoca menos en euros y explica más variación, sobre
  datos que ninguno de los dos había visto antes.
- **Una complicación adicional, que no escondí**: entre el modelo crudo y el
  tratado cambian dos cosas a la vez — qué alojamientos se incluyen (la
  población) y cómo se construyen algunas variables (por ejemplo, cómo se
  cuentan los amenities, o cómo se rellenan los datos faltantes de
  habitaciones). Para no mezclar ambos efectos, entrené una tercera versión
  intermedia que aísla solo el cambio de variables, manteniendo la misma
  población que el modelo crudo. Repetí la comparación con muestras
  simuladas miles de veces, para ver cuánto puede variar el resultado solo
  por azar con una muestra de ese tamaño (426 es una muestra pequeña, y las
  muestras pequeñas varían más de lo que uno esperaría).

**La conclusión final, con el nivel de certeza real que tengo**: puedo
afirmar con confianza que el modelo tratado predice mejor en una comparación
limpia y sin trampas. Lo que **no puedo afirmar con la misma certeza** es
cuánto de esa mejora viene de quitar alojamientos problemáticos y cuánto
viene de construir mejor las variables — los dos efectos, por separado, son
demasiado pequeños para distinguirlos del ruido propio de una muestra de 426
filas. Que el tamaño de muestra explique esa parte sin resolver es la
explicación más simple y la que mejor encaja con lo que observé — pero es
una interpretación razonable, no algo que haya demostrado de forma
definitiva. Lo dejo así, documentado como una limitación abierta, en vez de
forzar una conclusión más bonita de la que los datos permiten sostener.

**Por qué esto importa para DataTrust, más allá del modelo en sí**: esta es
la misma idea central del proyecto, aplicada ahora al modelo en vez de al
caso de negocio. Una empresa puede obtener un resultado numérico que parece
bueno — o parece malo — y aun así estar tomando decisiones sobre datos cuya
calidad o cuyo tratamiento no se ha evaluado con suficiente rigor. Antes de
atribuir una mejora a una causa concreta (en este caso, "el tratamiento de
los datos funciona"), hay que comprobar cómo se construyeron esos datos y
cómo se evaluó el modelo — exactamente lo que hice aquí, incluyendo
reconocer y corregir mi propio error de diseño por el camino.

## El cierre

La calidad de los datos no es un paso opcional antes del análisis, es parte del análisis — y cambia lo que terminas creyendo que es verdad.
