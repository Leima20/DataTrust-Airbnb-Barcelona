import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

base = "data/airbnb_bcn/"

listings = pd.read_csv(base + "listings.csv", low_memory=False)
reviews = pd.read_csv(base + "reviews.csv", low_memory=False)

print("=" * 70)
print("SHAPE")
print("listings:", listings.shape)
print("reviews:", reviews.shape)

print("=" * 70)
print("DUPLICADOS (filas completas)")
print("listings:", listings.duplicated().sum())
print("reviews:", reviews.duplicated().sum())

print("=" * 70)
print("listing_id: unicos en listings")
print("filas:", len(listings), "ids unicos:", listings["id"].nunique())

print("=" * 70)
print("NULOS EN LISTINGS (top 25 columnas con mas nulos, % del total)")
nulls = listings.isna().sum().sort_values(ascending=False)
nulls_pct = (nulls / len(listings) * 100).round(1)
print(pd.DataFrame({"nulos": nulls, "pct": nulls_pct}).head(25))

print("=" * 70)
print("PRECIO: tipo de dato y valores nulos")
print(listings["price"].head(5))
print("nulos en price:", listings["price"].isna().sum())

print("=" * 70)
print("REVIEWS: integridad referencial contra listings")
orphan_reviews = ~reviews["listing_id"].isin(listings["id"])
print("reviews con listing_id que no existe en listings:", orphan_reviews.sum())

print("=" * 70)
print("REVIEWS: comentarios duplicados EXACTOS (texto identico)")
dup_comments = reviews["comments"].dropna()
print("total comentarios no nulos:", len(dup_comments))
print("comentarios duplicados exactos:", dup_comments.duplicated().sum())

print("=" * 70)
print("REVIEWS: mismo reviewer_id con comentario identico en distintos listings (posible copy-paste)")
rev_text = reviews.dropna(subset=["comments"])
dup_by_reviewer = rev_text.duplicated(subset=["reviewer_id", "comments"]).sum()
print("casos:", dup_by_reviewer)

print("=" * 70)
print("REVIEWS: distribucion de longitud de comentario (posibles reviews genericas/cortas)")
rev_text = rev_text.copy()
rev_text["len_comment"] = rev_text["comments"].astype(str).str.len()
print(rev_text["len_comment"].describe())
print("comentarios con menos de 5 caracteres:", (rev_text["len_comment"] < 5).sum())

print("=" * 70)
print("LISTINGS: host con numero de propiedades (host_listings_count) vs anfitrion 'profesional'")
print(listings["host_listings_count"].describe())
print("hosts con mas de 50 anuncios:", (listings["host_listings_count"] > 50).sum())

print("=" * 70)
print("LISTINGS: valores unicos room_type y neighbourhood (buscar inconsistencias de escritura)")
print(listings["room_type"].unique())
print("num barrios unicos:", listings["neighbourhood_cleansed"].nunique())

print("=" * 70)
print("LISTINGS: fechas imposibles - host_since en el futuro o muy antigua")
listings["host_since"] = pd.to_datetime(listings["host_since"], errors="coerce")
print("host_since nulo:", listings["host_since"].isna().sum())
print("host_since despues de hoy:", (listings["host_since"] > pd.Timestamp.now()).sum())
print("host_since antes de 2008 (Airbnb no existia):", (listings["host_since"] < pd.Timestamp("2008-01-01")).sum())

print("=" * 70)
print("LISTINGS: minimo_noches con valores absurdos (ej. > 365)")
print(listings["minimum_nights"].describe())
print("minimum_nights > 365:", (listings["minimum_nights"] > 365).sum())
