
# Análisis Airbnb Lisboa

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Análisis  de los datos

# Leemos 
df = pd.read_csv("airbnb.csv")

# Exploración 
print("Dimensiones del dataset:", df.shape)
print("\nColumnas del dataset:\n", df.columns)
print("\nPrimeras filas:\n", df.head())
print("\nInformación general:\n")
df.info()
print("\nEstadísticas descriptivas:\n", df.describe())

# 2. Filtrados de datos

# --- CASO 1: Alicia ---
# Requisitos:
# - 4 personas → accommodates >= 4
# - habitaciones separadas → bedrooms >= 2
# - más de 10 críticas → reviews > 10
# - puntuación > 4
# - ordenar por satisfacción y luego críticas (descendente)
# - mostrar 3 mejores opciones

alicia = df[
    (df["accommodates"] >= 4) &
    (df["bedrooms"] >= 2) &
    (df["reviews"] > 10) &
    (df["overall_satisfaction"] > 4)
].sort_values(
    by=["overall_satisfaction", "reviews"],
    ascending=[False, False]
).head(3)

print("\nOpciones para Alicia:\n", alicia)

# --- CASO 2: Roberto y Clara ---
# Roberto host_id = 97503
# Clara host_id = 90387

roberto_clara = df[df["host_id"].isin([14455, 66015])]
print("\nCasas de Roberto y Clara:\n", roberto_clara)

# Guardamos como Excel
roberto_clara.to_excel("roberto.xlsx", index=False)
print("\nArchivo 'roberto.xls' guardado correctamente.")

# --- CASO 3: Diana ---
# Requisitos:
# - presupuesto ≤ 50
# - 10 propiedades más baratas
# - preferencia: Shared room
# - en shared room, mejor puntuación primero

diana = df[df["price"] <= 50]

diana = diana.sort_values(
    by=["room_type", "overall_satisfaction", "price"],
    ascending=[True, False, True]
).head(10)

print("\nOpciones para Diana:\n", diana)

# 3. Agrupamientos de datos

# Agrupamiento 1: Precio promedio por tipo de habitación
group1 = df.groupby("room_type")["price"].mean().sort_values(ascending=False)
print("\nPrecio promedio por tipo de habitación:\n", group1)

plt.figure()
group1.plot(kind='bar')
plt.title("Precio promedio por tipo de habitación")
plt.xlabel("Tipo de habitación")
plt.ylabel("Precio promedio (€)")
plt.show()

# Agrupamiento 2: Satisfacción media por barrio
group2 = df.groupby("neighborhood")["overall_satisfaction"].mean().sort_values(ascending=False).head(10)
print("\nSatisfacción media por barrio (Top 10):\n", group2)

plt.figure()
sns.barplot(x=group2.values, y=group2.index)
plt.title("Top 10 barrios con mejor puntuación")
plt.xlabel("Satisfacción promedio")
plt.ylabel("Barrio")
plt.show()
