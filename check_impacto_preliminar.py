import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

listings = pd.read_csv("data/airbnb_bcn/listings.csv", low_memory=False)

df = listings.dropna(subset=["estimated_revenue_l365d"]).copy()
y = df["estimated_revenue_l365d"]

base_cats = ["room_type", "property_type", "neighbourhood_cleansed"]
base_nums = ["accommodates", "host_listings_count"]

# ---------- VERSION A: "crudo" (sin tratamiento real de los problemas encontrados) ----------
A = df.copy()
A["bedrooms"] = A["bedrooms"].fillna(-1)
A["bathrooms"] = A["bathrooms"].fillna(-1)
A["beds"] = A["beds"].fillna(-1)
A["amenities_count"] = A["amenities"].astype(str).str.len()  # proxy crudo, sin parsear de verdad
A["host_is_superhost"] = A["host_is_superhost"].fillna("f")

featsA = base_cats + base_nums + ["bedrooms", "bathrooms", "beds", "amenities_count", "host_is_superhost"]
XA = pd.get_dummies(A[featsA], columns=base_cats + ["host_is_superhost"], drop_first=True)

# ---------- VERSION B: "tratado" (aplicando decisiones justificadas) ----------
B = df.copy()

def parse_amenities(v):
    try:
        return len(json.loads(v))
    except Exception:
        return np.nan

B["amenities_count"] = B["amenities"].apply(parse_amenities)
B["amenities_count"] = B["amenities_count"].fillna(B["amenities_count"].median())

# imputar bedrooms/bathrooms/beds por mediana segun room_type + accommodates (logica real, no relleno arbitrario)
for col in ["bedrooms", "bathrooms", "beds"]:
    B[col] = B.groupby(["room_type", "accommodates"])[col].transform(lambda s: s.fillna(s.median()))
    B[col] = B[col].fillna(B[col].median())  # fallback global si el grupo no tenia dato

B["host_is_superhost"] = B["host_is_superhost"].fillna("f")
B["host_profesional"] = (B["host_listings_count"] > 50).astype(int)  # variable con sentido de negocio

featsB = base_cats + ["accommodates", "host_profesional"] + ["bedrooms", "bathrooms", "beds", "amenities_count", "host_is_superhost"]
XB = pd.get_dummies(B[featsB], columns=base_cats + ["host_is_superhost"], drop_first=True)

# ---------- Entrenar y comparar (mismo split, mismo modelo, misma semilla) ----------
def evaluar(X, y, nombre):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)
    modelo.fit(Xtr, ytr)
    pred = modelo.predict(Xte)
    mae = mean_absolute_error(yte, pred)
    r2 = r2_score(yte, pred)
    print(f"{nombre:10s} MAE={mae:9.1f}  R2={r2:.3f}  n_features={X.shape[1]}")
    return mae, r2, modelo, X.columns

print("=" * 60)
print(f"Filas usadas (con target no nulo): {len(df)}")
print("=" * 60)
maeA, r2A, modelA, colsA = evaluar(XA, y, "CRUDO")
maeB, r2B, modelB, colsB = evaluar(XB, y, "TRATADO")

print("=" * 60)
print(f"Diferencia MAE: {maeA - maeB:.1f}  ({(maeA-maeB)/maeA*100:.1f}% de mejora)" if maeA > maeB
      else f"Diferencia MAE: {maeA - maeB:.1f} (el tratado empeoro)")
print(f"Diferencia R2:  {r2B - r2A:.3f}")

print("=" * 60)
print("Top 8 variables mas importantes - CRUDO")
impA = pd.Series(modelA.feature_importances_, index=colsA).sort_values(ascending=False)
print(impA.head(8))

print("=" * 60)
print("Top 8 variables mas importantes - TRATADO")
impB = pd.Series(modelB.feature_importances_, index=colsB).sort_values(ascending=False)
print(impB.head(8))
