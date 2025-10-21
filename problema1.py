


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

 
df = pd.read_csv("airbnb.csv")


print("Dimensiones del dataset:", df.shape)
print("\nColumnas del dataset:\n", df.columns)
print("\nPrimeras filas:\n", df.head())
print("\nInformación general:\n")
df.info()
print("\nEstadísticas descriptivas:\n", df.describe())



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



roberto_clara = df[df["host_id"].isin([14455, 66015])]
print("\nCasas de Roberto y Clara:\n", roberto_clara)


roberto_clara.to_excel("roberto.xlsx", index=False)
print("\nArchivo 'roberto.xls' guardado correctamente.")



diana = df[df["price"] <= 50]

diana = diana.sort_values(
    by=["room_type", "overall_satisfaction", "price"],
    ascending=[True, False, True]
).head(10)

print("\nOpciones para Diana:\n", diana)


group1 = df.groupby("room_type")["price"].mean().sort_values(ascending=False)
print("\nPrecio promedio por tipo de habitación:\n", group1)

plt.figure()
group1.plot(kind='bar')
plt.title("Precio promedio por tipo de habitación")
plt.xlabel("Tipo de habitación")
plt.ylabel("Precio promedio (€)")
plt.show()


group2 = df.groupby("neighborhood")["overall_satisfaction"].mean().sort_values(ascending=False).head(10)
print("\nSatisfacción media por barrio (Top 10):\n", group2)

plt.figure()
sns.barplot(x=group2.values, y=group2.index)
plt.title("Top 10 barrios con mejor puntuación")
plt.xlabel("Satisfacción promedio")
plt.ylabel("Barrio")
plt.show()
