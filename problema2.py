import pandas as pd
from pymongo import MongoClient


try:
    
    df = pd.read_csv("winemag-data-130k-v2.csv", encoding="utf-8")
    print(" Archivo de vinos leído correctamente.")
except Exception as e:
    print(" Error al leer el archivo de vinos:", e)
    exit()

try:
    paises = pd.read_csv("paises_final.csv", encoding="utf-8")
    print(" Archivo de países leído correctamente.")
except Exception as e:
    print(" Error al leer paises_final.csv:", e)
    exit()


df = df.rename(columns={
    "country": "pais",
    "price": "precio",
    "points": "puntuacion",
    "variety": "variedad"
})


df = df.merge(paises, left_on="pais", right_on="nombre", how="left")


df = df.drop(columns=["nombre"], errors="ignore")


df["nivel_calidad"] = pd.cut(
    df["puntuacion"],
    bins=[0, 80, 90, 100],
    labels=["Baja", "Media", "Alta"]
)


df["rango_precio"] = pd.cut(
    df["precio"],
    bins=[0, 20, 50, 1000],
    labels=["Económico", "Medio", "Premium"]
)


reporte1 = df.groupby("continente")[["puntuacion", "precio"]].mean().reset_index()


reporte2 = df.groupby("pais")["puntuacion"].mean().reset_index().sort_values("puntuacion", ascending=False).head(10)


reporte3 = df["nivel_calidad"].value_counts().reset_index()
reporte3.columns = ["nivel_calidad", "cantidad"]


reporte4 = df.groupby(["continente", "variedad"])["precio"].mean().reset_index().sort_values("precio", ascending=False)

 
reporte1.to_csv("reporte1_continente.csv", index=False)
reporte2.to_excel("reporte2_top_paises.xlsx", index=False)
reporte3.to_json("reporte3_calidad.json", orient="records")

 
try:
    mongo_uri = "mongodb+srv://user1:user1@cluster0.hdwflim.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    cliente = MongoClient(mongo_uri)
    db = cliente["pc5"]
    coleccion = db["reporte4_precio_variedad"]
    datos = reporte4.to_dict("records")
    coleccion.insert_many(datos)
    print(" Reporte 4 exportado a MongoDB correctamente.")
except Exception as e:
    print(" Error al conectar con MongoDB:", e)


print("\n📊 Reportes generados:")
print("1. reporte1_continente.csv")
print("2. reporte2_top_paises.xlsx")
print("3. reporte3_calidad.json")
print("4. reporte4_precio_variedad → MongoDB")
