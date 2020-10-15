#Package necesarios para el proceso
import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymysql
import seaborn as sb
from jedi.api.refactoring import inline
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn import preprocessing
from mpl_toolkits.mplot3d import Axes3D

#Conexión a la Base de datos
db = pymysql.connect("localhost", "root", "kacvo123", "UG_SOES")
cursor = db.cursor()
#Configuraciones para las figuras
plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')
#Consulta y obtención de los datos
sql = "select Question.Id, Question.Tags, Question.AnswerCount, Question.FavoriteCount," \
      " Posts_ES.Score, Posts_ES.ViewCount, Posts_ES.CommentCount" \
      " from Posts_ES, Question, Users_Country, Users" \
      " where" \
      "		Question.Id = Posts_ES.Id" \
      "        AND Users_Country.Id = Posts_ES.OwnerUserId" \
      "        and Users.Id = Posts_ES.OwnerUserId" \
      "        AND Users_Country.Country LIKE 'ecuador';"
preguntas = pd.read_sql_query(sql, db)
#Reemplazo de los valores NAN por 0
preguntas['FavoriteCount'] = preguntas['FavoriteCount'].replace(np.nan, 0)

#Creación de la Varible importancia en base a las caracteristicas ViewCount, FavoriteCount, Score
e= []
for p in range(0, len(preguntas)):
    if (preguntas.iloc[p]['ViewCount'] > 714.031138) and (preguntas.iloc[p]['Score'] > 1.022754) and (
            preguntas.iloc[p]['FavoriteCount'] > 0.167665):
        e =  np.insert(e, p, 1)
    else:
        e = np.insert(e, p, 0)
preguntas= preguntas.assign(Importancia=pd.Series(e).astype(int))


#Defición de las caracteristicas a usar y del objetivo
caracteristicas = preguntas[['ViewCount', 'Score', 'FavoriteCount']]
targets = preguntas['Importancia']

#Datos por Categoria
print(preguntas.groupby('FavoriteCount').size())
print(preguntas.groupby('Importancia').size())

#Graficos
"""preguntas.drop(['Importancia'],1).hist()
plt.show()
sb.pairplot(preguntas.dropna(), hue='Importancia', height=4, vars=['ViewCount', 'FavoriteCount', 'Score'], kind='scatter')
plt.show()
"""
#Asginar variables
x = np.array(preguntas[['ViewCount', 'Score', 'FavoriteCount']])
y = np.array(preguntas['Importancia'])

#Obtener valor de K
nc = range(1,30)
kmeans = [KMeans(n_clusters=i) for i in nc]
print(kmeans)
score = [kmeans[i].fit(x).score(x) for i in range(len(kmeans))]
print(score)
plt.plot(nc, score)
plt.xlabel("Número de Clusters")
plt.ylabel("Puntuación")
plt.title("Curva de Elbow")
plt.show()


#Ejecución de K-means
kmeans= KMeans(n_clusters=5).fit(x)
centroids = kmeans.cluster_centers_
print("Centroides: ")
print(centroids)

#Graficar
labels = kmeans.predict(x)
C = kmeans.cluster_centers_

fig = plt.figure()
ax = Axes3D(fig)
colores = ['blue', 'red', 'green', 'cyan', 'yellow']
asignar = []
for row in y:
    asignar.append(colores[row])
ax.scatter(x[:, 0], x[:, 1], x[:, 2], c=asignar, s=60)
ax.scatter(C[:, 0], C[:, 1], C[:, 2], marker='*', c=colores, s=1000)
plt.xlabel("ViewCount")
plt.ylabel("Score")
plt.clabel("FavoriteCount")
plt.show()


#Análisis en dos dimensiones
#primera forma: figuras individuales 
#1 ViewCount-Score
f1= preguntas["ViewCount"]
f2= preguntas["Score"]
plt.scatter(f1, f2, c= asignar, s=70)
plt.scatter(C[:, 0], C[:, 1],marker= '*', c= colores, s=1000)
plt.xlabel("ViewCount")
plt.ylabel("Score")
plt.show()
#2 ViewCount-FavoriteCount
f1= preguntas["ViewCount"]
f2= preguntas["FavoriteCount"]
plt.scatter(f1, f2, c= asignar, s=70)
plt.scatter(C[:, 0], C[:, 2],marker= '*', c= colores, s=1000)
plt.xlabel("ViewCount")
plt.ylabel("FavoriteCount")
plt.show()
#3 FavoriteCount-Score
f1= preguntas["FavoriteCount"]
f2= preguntas["Score"]
plt.scatter(f1, f2, c= asignar, s=70)
plt.scatter(C[:, 2], C[:, 1],marker= '*', c= colores, s=1000)
plt.xlabel("FavoriteCount")
plt.ylabel("Score")
plt.show()

#segunda forma: figuras individuales 
#1 ViewCount-Score
plt.figure(figsize=(6,4))
plt.subplot(2,2,1)
f1= preguntas["ViewCount"]
f2= preguntas["Score"]
plt.scatter(f1, f2, c= asignar, s=70)
plt.scatter(C[:, 0], C[:, 1],marker= '*', c= colores, s=1000)
plt.xlabel("ViewCount")
plt.ylabel("Score")
#2 ViewCount-FavoriteCount
plt.subplot(2,2,2)
f1= preguntas["ViewCount"]
f2= preguntas["FavoriteCount"]
plt.scatter(f1, f2, c= asignar, s=70)
plt.scatter(C[:, 0], C[:, 2],marker= '*', c= colores, s=1000)
plt.xlabel("ViewCount")
plt.ylabel("FavoriteCount")
#3 FavoriteCount-Score
plt.subplot(2,2,3)
f1= preguntas["FavoriteCount"]
f2= preguntas["Score"]
plt.scatter(f1, f2, c= asignar, s=70)
plt.scatter(C[:, 2], C[:, 1],marker= '*', c= colores, s=1000)
plt.xlabel("FavoriteCount")
plt.ylabel("Score")
plt.tight_layout()
plt.show()


copy= pd.DataFrame()
copy["FavoriteCount"] = preguntas["FavoriteCount"].values
copy["Score"] = preguntas["Score"].values
copy["Importancia"] = preguntas["Importancia"].values
copy["label"]=labels;
cantidadGrupo= pd.DataFrame()
cantidadGrupo["color"] = colores
cantidadGrupo["cantidad"]=copy.groupby("label").size()
print(cantidadGrupo)

#Evaluación
#Cantidad de Etiquetas por cluster
print(kmeans.labels_)
print(np.unique(kmeans.labels_,return_counts=True))
