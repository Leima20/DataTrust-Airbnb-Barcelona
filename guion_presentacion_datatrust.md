# Guion de presentación — DataTrust

Oct 28, 2026

## Introducción

## Página 1 · Inicio

## Página 2 · Contexto del proyecto

## Página 3 · Auditoría de calidad

## Página 3 · Auditoría de calidad

**Patrón de negocio derivado** (no es un defecto de dato):

**Guion para 'Prioridad de tratamiento'** (anticiparse a la duda del tribunal):

"Aunque la mayoría de los hallazgos son de prioridad baja en impacto directo sobre el tratamiento de datos, catalogamos 5 como prioridad alta: 3 de ellos (`L1`, `R2`, `C1`) afectan a la integridad referencial o estructura de las tablas, y los otros 2 (`L3`, `C2`) son contradicciones lógicas internas en los datos."

'Profesional' -- anfitrión con más de 50 anuncios en Barcelona (`calculated_host_listings_count > 50`). 'Particular' -- el resto, 50 anuncios o menos en Barcelona. Es una distinción propia del proyecto, no de Airbnb, que mide gestión en la plataforma, no propiedad.

**`L6`** -- Profesionales sobrerrepresentados en NRUA: 65,7% vs. 18-25% del resto de categorías -- adoptan el trámite regulatorio más rápido.

**Caso de control en el Ejemplo 1 de imputación (id 18674, `price` sin cambios)**: no tiene ninguna función en el pipeline de tratamiento -- se eligió a propósito para la tabla en vivo. 409€ → 409€ demuestra visualmente que la regla de imputación solo toca valores nulos y deja intacto un dato que ya estaba completo, en vez de tener que afirmarlo sin evidencia.

## Página 4 · El hallazgo crítico

## Página 5 · Diseño experimental

## Página 6 · Comparación de modelos

## Página 7 · Resultados y robustez

## Página 8 · Conclusiones y recomendaciones

## Página 9 · Metodología y limitaciones

## Preguntas y respuestas previstas

## Preguntas y respuestas previstas

**Si preguntan por qué se audita tanto el campo `license`:**

"Porque la falta de verificación de este campo no es un problema puramente académico, tiene impacto en el riesgo de negocio. Históricamente, el Ayuntamiento de Barcelona ha impuesto sanciones de hasta 600.000€ a plataformas por publicar anuncios sin licencia o con licencia falsa, sin verificar antes de publicar. Nuestra auditoría muestra que, en el dataset crudo, el 21,1% del campo `license` no se puede verificar -- ni confirmar ni descartar -- antes de cualquier proceso de inspección o compliance."

*Fuente: multas a Airbnb/HomeAway por el Ayuntamiento de Barcelona, 2016-2020 (histórico, no reciente -- usar solo como contexto de riesgo, no como dato del dataset).*
