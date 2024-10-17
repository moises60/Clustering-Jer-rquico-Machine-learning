# Clustering Jerárquico Adaptado

import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import seaborn as sns
import chardet
import scipy.cluster.hierarchy as sch

with open("car_purchasing.csv", 'rb') as f:
    result = chardet.detect(f.read(10000)) 
print(f"Codificación detectada: {result['encoding']}")

# 3. Cargar los datos con la codificación correcta
dataset = pd.read_csv("car_purchasing.csv", encoding=result['encoding'])

# 4. Exploración Inicial de Datos
print("Primeras filas del dataset:")
print(dataset.head())

print("\nInformación del dataset:")
print(dataset.info())

print("\nResumen estadístico:")
print(dataset.describe())

# 5. Manejo de Valores Faltantes
print("\nValores faltantes por columna:")
print(dataset.isnull().sum())

# Manejar valores faltantes eliminando filas con NaN
dataset = dataset.dropna()

# 6. Selección de Características
# Asegúrate de que las columnas 5 y 8 sean las que deseas usar
X = dataset.iloc[:, [5, 8]].values

# 7. Escalado de Características
# Aunque mencionas que no es necesario, es una buena práctica escalar los datos para clustering jerárquico
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 8. Visualización del Dendrograma para determinar el número óptimo de clusters
plt.figure(figsize=(10, 7))
dendrogram = sch.dendrogram(sch.linkage(X_scaled, method="ward"))
plt.title("Dendrograma")
plt.xlabel("Clientes")
plt.ylabel("Distancia Euclídea")
plt.show()

# 9. Evaluación con el Coeficiente de Silueta
# Dado que el método del codo no es aplicable directamente, nos enfocaremos en el coeficiente de silueta.

silhouette_scores = []
range_clusters = range(2, 11)  # Clusters de 2 a 10
for i in range_clusters:
    hc = AgglomerativeClustering(n_clusters=i, linkage="ward")  # Eliminado 'affinity'
    labels = hc.fit_predict(X_scaled)
    score = silhouette_score(X_scaled, labels)
    silhouette_scores.append(score)

plt.figure(figsize=(10,6))
plt.plot(range_clusters, silhouette_scores, marker='o', color='green')
plt.title("Coeficiente de Silueta para diferentes números de clusters")
plt.xlabel("Número de Clusters")
plt.ylabel("Coeficiente de Silueta")
plt.xticks(range_clusters)
plt.grid(True)
plt.show()

# Basándonos en el coeficiente de silueta, seleccionamos el número óptimo de clusters
# Supongamos que el valor óptimo es 3 (ajusta según tus resultados)
optimal_clusters = 2

# 10. Aplicar Clustering Jerárquico Aglomerativo con el número óptimo de clusters
hc = AgglomerativeClustering(n_clusters=optimal_clusters, linkage="ward")  # Eliminado 'affinity'
y_hc = hc.fit_predict(X_scaled)

# 11. Añadir los labels de clusters al dataset original
dataset['Cluster'] = y_hc

# 12. Visualización de los Clusters
plt.figure(figsize=(10,6))
colors = ['red', 'blue', 'green', 'cyan', 'magenta', 'yellow', 'black', 'orange', 'purple', 'brown']
for i in range(optimal_clusters):
    plt.scatter(
        X_scaled[y_hc == i, 0], 
        X_scaled[y_hc == i, 1], 
        s=100, 
        c=colors[i],
        label=f"Cluster {i+1}"
    )
# Nota: No hay centroides en Clustering Jerárquico, por lo que omitimos esta parte
plt.title("Clusters de Clientes (Clustering Jerárquico Aglomerativo)")
plt.xlabel("Ingresos Anuales (Escalados)")
plt.ylabel("Gastos (Escalados)")
plt.legend()
plt.grid(True)
plt.show()

# 13. Análisis de los Clusters
print("\nDescripción de los clusters:")
for i in range(optimal_clusters):
    cluster_data = dataset[dataset['Cluster'] == i]
    print(f"\nCluster {i+1}:")
    print(cluster_data.describe())



