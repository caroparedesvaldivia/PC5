import os
import zipfile
import pandas as pd
from pymongo import MongoClient

# 1. Definir rutas
zip_path = "0303.zip"           # Archivo subido
extract_path = "datos_youtube"  # Carpeta destino

# 2. Descomprimir el ZIP
with zipfile.ZipFile(zip_path, "r") as zip_ref:
    zip_ref.extractall(extract_path)

print("Archivos extraídos en:", extract_path)
print("Contenido de la carpeta:", os.listdir(extract_path))

# 3. Leer el archivo .txt (ajusta el nombre si es distinto)
file_path = os.path.join(extract_path, "0303.txt")
df = pd.read_csv(file_path, sep="\t", header=None)

# 4. Asignar nombres de columnas
df.columns = [
    "video_id", "uploader", "age", "category", "length",
    "views", "rate", "ratings", "comments", "related_IDs"
]

# 5. Seleccionar columnas relevantes
df_filtrado = df[["video_id", "age", "category", "views", "rate"]]

# 6. Filtrar por categorías específicas (puedes cambiarlas)
categorias_permitidas = ["Music", "Comedy", "Sports"]
df_filtrado = df_filtrado[df_filtrado["category"].isin(categorias_permitidas)]

print("\nDatos filtrados por categorías:")
print(df_filtrado.head())

# 7. Exportar a MongoDB
try:
    client = MongoClient("mongodb://localhost:27017/")  # Cambiar si usas MongoDB Atlas
    db = client["youtube_db"]
    collection = db["videos_filtrados"]

    collection.insert_many(df_filtrado.to_dict("records"))
    print("\nDatos exportados correctamente a MongoDB.")
    print("Base de datos: youtube_db | Colección: videos_filtrados")

except Exception as e:
    print("\nNo se pudo conectar a MongoDB:", e)

# 8. Guardar una copia local en CSV
df_filtrado.to_csv("youtube_filtrado.csv", index=False)
print("\nArchivo 'youtube_filtrado.csv' guardado correctamente.")

