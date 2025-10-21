import zipfile
import os
import pandas as pd
from pymongo import MongoClient

zip_path = "0303.zip"
extract_dir = "datos_youtube"


if not os.path.exists(extract_dir):
    os.makedirs(extract_dir)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)
    print(f"Archivos extraídos en: {extract_dir}")
else:
    print("La carpeta ya existe, se omite la descompresión.")


files = os.listdir(os.path.join(extract_dir, "0303"))
print("Contenido de la carpeta principal:", files)

txt_file = os.path.join(extract_dir, "0303", "3.txt")
df = pd.read_csv(txt_file, sep="\t", header=None, usecols=range(10))


df.columns = [
    "video_id", "uploader", "age", "category", "length",
    "views", "rate", "ratings", "comments", "related_IDs"
]

print(f"Archivo leído correctamente. Filas: {df.shape[0]}  Columnas: {df.shape[1]}")


df_filtered = df[["video_id", "age", "category", "views", "rate"]]


categorias = ["Music", "Comedy"]
df_filtered = df_filtered[df_filtered["category"].isin(categorias)]

print("Datos filtrados por categoría:")
print(df_filtered.head())


csv_path = "youtube_filtrado.csv"
json_path = "youtube_filtrado.json"

df_filtered.to_csv(csv_path, index=False)
df_filtered.to_json(json_path, orient="records", lines=True)

print(f"Datos exportados a CSV: {csv_path}")
print(f"Datos exportados a JSON: {json_path}")


mongo_uri = "mongodb+srv://user1:user1@cluster0.hdwflim.mongodb.net/?retryWrites=true&w=majority"
import json
from pymongo import MongoClient

 
mongo_uri = "mongodb+srv://user1:user1@cluster0.hdwflim.mongodb.net/?retryWrites=true&w=majority"


client = MongoClient(mongo_uri)


db = client["youtube_db"]           
collection = db["videos_filtrados"] 


with open("youtube_filtrado.json", "r") as f:
    records = [json.loads(line) for line in f]  


if records:
    collection.insert_many(records)
    print(f"{len(records)} registros insertados en MongoDB.")
else:
    print("No hay registros para insertar.")
