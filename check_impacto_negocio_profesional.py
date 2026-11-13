import pandas as pd

listings = pd.read_csv("data/airbnb_bcn/listings.csv", low_memory=False)

listings["profesional"] = listings["calculated_host_listings_count"] > 50
tiene_revenue = listings["estimated_revenue_l365d"].notna()

naive = listings[tiene_revenue].groupby("profesional")["estimated_revenue_l365d"].agg(["mean", "median", "count"])

print("=" * 70)
print("CONCLUSIÓN NAIVE (solo dropna, sin investigar los ceros)")
print("=" * 70)
print(naive.round(0))
media_particular_naive = naive.loc[False, "mean"]
media_profesional_naive = naive.loc[True, "mean"]
gap_naive = media_particular_naive - media_profesional_naive
print(f"\nGap particular vs profesional: {gap_naive:.0f} EUR/año "
      f"({gap_naive / media_particular_naive * 100:.1f}% peor el profesional)")

es_cero = listings["estimated_revenue_l365d"] == 0
zero_pro = listings[tiene_revenue & es_cero & listings["profesional"]]
activo_pro = listings[tiene_revenue & ~es_cero & listings["profesional"]]

print("\n" + "=" * 70)
print("DIAGNÓSTICO: anuncios profesionales con revenue = 0")
print("=" * 70)
print(f"% de profesionales en 0 EUR: {es_cero[tiene_revenue & listings['profesional']].mean() * 100:.1f}%")
print(f"  de ellos, sin ninguna reseña en el último año: {(zero_pro['number_of_reviews_ltm'] == 0).mean() * 100:.1f}%")
print(f"  de ellos, con estancia mínima >= 28 noches: {(zero_pro['minimum_nights'] >= 28).mean() * 100:.1f}%")
print(f"  (vs. en los profesionales SI activos: "
      f"{(activo_pro['minimum_nights'] >= 28).mean() * 100:.1f}% con estancia larga)")
print("Interpretación: estimated_revenue_l365d se calcula a partir de reseñas de los")
print("últimos 365 días. Un huésped de estancia larga (28+ noches) deja como mucho")
print("una reseña al año, así que la fórmula no puede estimar ingresos ahí, aunque")
print("el alojamiento esté ocupado. No es ingreso real cero, es 'no estimable'.")

no_estimable = tiene_revenue & es_cero & (listings["number_of_reviews_ltm"] == 0) & (listings["minimum_nights"] >= 28)
print(f"\nAnuncios marcados como 'no estimable' en todo el dataset: {no_estimable.sum()} "
      f"({no_estimable.sum() / tiene_revenue.sum() * 100:.1f}% de los que tienen dato)")

corregido = listings[tiene_revenue & ~no_estimable].groupby("profesional")["estimated_revenue_l365d"].agg(["mean", "median", "count"])

print("\n" + "=" * 70)
print("CONCLUSIÓN CORREGIDA (excluyendo anuncios estructuralmente no estimables)")
print("=" * 70)
print(corregido.round(0))
media_particular_corr = corregido.loc[False, "mean"]
media_profesional_corr = corregido.loc[True, "mean"]
gap_corr = media_particular_corr - media_profesional_corr
print(f"\nGap particular vs profesional: {gap_corr:.0f} EUR/año "
      f"({gap_corr / media_particular_corr * 100:.1f}% peor el profesional)")

n_grupo = 50
impacto_naive = gap_naive * n_grupo
impacto_corregido = gap_corr * n_grupo

print("\n" + "=" * 70)
print(f"TRADUCCIÓN A DINERO: grupo ilustrativo de {n_grupo} anuncios (ayuda de intuición, no una decisión individual)")
print("=" * 70)
print(f"Con datos crudos, la penalización estimada para el grupo profesional: "
      f"{impacto_naive:,.0f} EUR/año".replace(",", "."))
print(f"Con datos auditados, la penalización real es de: "
      f"{impacto_corregido:,.0f} EUR/año".replace(",", "."))
print(f"Diferencia entre medir con datos crudos vs. auditados: "
      f"{impacto_naive - impacto_corregido:,.0f} EUR/año".replace(",", "."))
