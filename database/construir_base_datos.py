"""
Construye la base de datos SQLite completa del proyecto (database/airbnb.db)
a partir de los CSV originales de Inside Airbnb. Se ejecuta una sola vez (o cada
vez que se quiera reconstruir desde cero); los notebooks de auditoría y
tratamiento se conectan a este archivo, no vuelven a cargar los CSV en SQL.
"""

import sqlite3
import pandas as pd

con = sqlite3.connect("airbnb.db")

print("Cargando listings...")
listings = pd.read_csv("../data/airbnb_bcn/listings.csv", low_memory=False)
listings.to_sql("listings", con, index=False, if_exists="replace")
print(f"  listings: {listings.shape[0]} filas, {listings.shape[1]} columnas")

print("Cargando reviews...")
reviews = pd.read_csv("../data/airbnb_bcn/reviews.csv", low_memory=False)
reviews.to_sql("reviews", con, index=False, if_exists="replace")
print(f"  reviews: {reviews.shape[0]} filas, {reviews.shape[1]} columnas")

print("Cargando calendar...")
calendar = pd.read_csv("../data/airbnb_bcn/calendar.csv", low_memory=False)
calendar.to_sql("calendar", con, index=False, if_exists="replace")
print(f"  calendar: {calendar.shape[0]} filas, {calendar.shape[1]} columnas")

con.close()
print("Listo: database/airbnb.db construida con las 3 tablas completas.")
