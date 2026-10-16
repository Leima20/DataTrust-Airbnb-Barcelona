import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

base = "data/airbnb_bcn/"

calendar = pd.read_csv(base + "calendar.csv", low_memory=False)
listings = pd.read_csv(base + "listings.csv", low_memory=False)

print("=" * 70)
print("SHAPE")
print("calendar:", calendar.shape)

print("=" * 70)
print("COLUMNAS")
print(calendar.columns.tolist())

print("=" * 70)
print("NULOS")
print(calendar.isna().sum())

print("=" * 70)
print("DUPLICADOS (filas completas)")
print(calendar.duplicated().sum())

print("=" * 70)
print("DUPLICADOS por listing_id + date (deberia ser unico, un registro por dia por alojamiento)")
print(calendar.duplicated(subset=["listing_id", "date"]).sum())

print("=" * 70)
print("Rango de fechas")
calendar["date"] = pd.to_datetime(calendar["date"], errors="coerce")
print("min:", calendar["date"].min(), "max:", calendar["date"].max())
print("fechas nulas tras conversion:", calendar["date"].isna().sum())

print("=" * 70)
print("Valores unicos de 'available'")
print(calendar["available"].unique())

print("=" * 70)
print("Integridad referencial: listing_id de calendar que no existe en listings")
orphan = ~calendar["listing_id"].isin(listings["id"])
print("filas huerfanas:", orphan.sum())

print("=" * 70)
print("Listings SIN ninguna fila en calendar (alojamiento sin calendario publicado)")
listings_sin_calendario = ~listings["id"].isin(calendar["listing_id"])
print(listings_sin_calendario.sum())

print("=" * 70)
print("PRECIO en calendar: columna existe?")
print("columnas disponibles:", calendar.columns.tolist())
print("-> 'price' NO esta en este snapshot de calendar.csv (hallazgo en si mismo)")

print("=" * 70)
print("minimum_nights / maximum_nights en calendar: valores absurdos")
print(calendar["minimum_nights"].describe())
print(calendar["maximum_nights"].describe())
print("maximum_nights con valores como 1125 (valor por defecto de Airbnb, no real):", (calendar["maximum_nights"] >= 1125).sum())
