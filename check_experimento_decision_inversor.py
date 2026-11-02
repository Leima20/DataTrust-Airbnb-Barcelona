import pandas as pd

listings = pd.read_csv("data/airbnb_bcn/listings.csv", low_memory=False)

# ---------- Universo: anuncios con dato en estimated_revenue_l365d ----------
tiene_revenue = listings["estimated_revenue_l365d"].notna()
sub = listings[tiene_revenue].copy()
universo = len(sub)

print("=" * 70)
print("EXPERIMENTO DE DECISION: regla original vs. regla auditada")
print("=" * 70)
print(f"Universo pertinente (anuncios con dato en estimated_revenue_l365d): {universo}")
print(f"(de un total de {len(listings)} anuncios; {len(listings) - universo} sin dato)")

# ---------- Regla ORIGINAL: descartar todo anuncio con revenue == 0 ----------
es_cero = sub["estimated_revenue_l365d"] == 0
n_descartados = es_cero.sum()
print(f"\nRegla ORIGINAL -- descartados (revenue == 0): {n_descartados} "
      f"({n_descartados / universo * 100:.1f}% del universo)")

# ---------- Patron identificado como potencialmente no estimable ----------
# (mismo patron que en check_impacto_negocio_profesional.py: 0 resenas recientes
#  Y estancia minima >= 28 noches)
cond_resenas = sub["number_of_reviews_ltm"] == 0
cond_estancia = sub["minimum_nights"] >= 28
patron = es_cero & cond_resenas & cond_estancia
n_revision = patron.sum()

cero_fuera_patron = es_cero & ~patron
n_siguen_descartados = cero_fuera_patron.sum()

print(f"\nRegla AUDITADA -- pasan a 'requiere revision' (patron no-estimable): "
      f"{n_revision} ({n_revision / universo * 100:.1f}% del universo)")
print(f"Regla AUDITADA -- siguen descartados (cero fuera del patron): "
      f"{n_siguen_descartados} ({n_siguen_descartados / universo * 100:.1f}% del universo)")
print(f"\nDe los {n_descartados} descartados originalmente, "
      f"{n_revision} ({n_revision / n_descartados * 100:.1f}%) cambian de clasificacion.")

# ---------- Desglose de por que los 'siguen descartados' no entran en el patron ----------
solo_resenas = es_cero & cond_resenas & ~cond_estancia
solo_estancia = es_cero & ~cond_resenas & cond_estancia
ninguna = es_cero & ~cond_resenas & ~cond_estancia
print("\nDesglose de los que siguen descartados (no cumplen el patron completo):")
print(f"  0 resenas recientes pero estancia < 28 noches: {solo_resenas.sum()}")
print(f"  estancia >= 28 noches pero SI tiene resenas recientes: {solo_estancia.sum()}")
print(f"  no cumple ninguna de las dos condiciones: {ninguna.sum()}")

# ---------- Caracteristicas: patron (revision) vs. resto de ceros ----------
def limpiar_price(serie):
    return pd.to_numeric(serie.astype(str).str.replace(r"[$,]", "", regex=True), errors="coerce")

grupo_revision = sub[patron]
grupo_descartado = sub[cero_fuera_patron]

print("\n" + "=" * 70)
print("CARACTERISTICAS: revision vs. siguen descartados")
print("=" * 70)
print("\nroom_type (% dentro de cada grupo):")
print("Revision:")
print((grupo_revision["room_type"].value_counts(normalize=True) * 100).round(1))
print("Siguen descartados:")
print((grupo_descartado["room_type"].value_counts(normalize=True) * 100).round(1))

print(f"\nprice mediana -- revision: {limpiar_price(grupo_revision['price']).median():.1f} EUR, "
      f"siguen descartados: {limpiar_price(grupo_descartado['price']).median():.1f} EUR, "
      f"universo: {limpiar_price(sub['price']).median():.1f} EUR")
print(f"accommodates mediana -- revision: {grupo_revision['accommodates'].median():.1f}, "
      f"siguen descartados: {grupo_descartado['accommodates'].median():.1f}")

print("\n" + "=" * 70)
print("LIMITES EXPLICITOS")
print("=" * 70)
print("No se afirma que los anuncios en 'revision' sean rentables ni que generen")
print("ingresos reales -- no hay datos de reservas/ingresos reales en este dataset.")
print("No se ha encontrado evidencia de que inversores reales usen Inside Airbnb")
print("de esta manera para decidir -- este es un escenario hipotetico aplicado a")
print("datos reales, no un caso de negocio documentado.")
