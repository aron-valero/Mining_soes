#Package necesarios para el proceso
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymysql
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import  confusion_matrix
from sklearn.metrics import accuracy_score, hamming_loss
from sklearn.metrics import classification_report
import graphviz
from sklearn.tree import export_graphviz
from sklearn.model_selection import cross_val_score
#Package necesarioa para dibujar el arbol
from sklearn import tree
from io import  StringIO
from IPython.display import Image
from pydotplus import graph_from_dot_data as gfd
#Conexión a la Base de datos
db = pymysql.connect("localhost", "root", "kacvo123", "UG_SOES")
cursor = db.cursor()
#Estilo de las gráficas
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

# cursor.execute(sql)
# preguntas = cursor.fetchall()
# print(preguntas.sort_values(by=['ViewCount'], ascending= False))

#Reemplazo de los valores NAN por 0
#Estadisticos de las Variables
"""
print('Estadisticas Descriptiva: Media')
print(preguntas.mean())
print('Estadisticas Descriptiva: Mediana')
print(preguntas.median())
# porcentaje de poblamiento delas variables
print('Poblamiento de Variables')
print(preguntas.count(0) / preguntas.shape[0] * 100)"""
preguntas['FavoriteCount'] = preguntas['FavoriteCount'].replace(np.nan, 0)

#Creación de la Varible importancia en base a las caracteristicas ViewCount, FavoriteCount, Score
e= []
for p in range(0, len(preguntas)):
    if (preguntas.iloc[p]['ViewCount'] > 714.031138) and (preguntas.iloc[p]['Score'] > 1.022754) and (
            preguntas.iloc[p]['FavoriteCount'] > 0.167665):
        e =  np.insert(e, p, 1)
    else:
        e = np.insert(e, p, 0)
preguntas= preguntas.assign(Importancia=pd.Series(e))
#print(preguntas)
# preguntas.hist(column="ViewCount", histtype="bar")
# plt.show()
# print(preguntas.shape)
# print(preguntas.columms)
# print(preguntas.head())
# clf_gini = DecisionTreeClassifier(criterion="gini", random_state= 100, max_depth= 3, min_samples_leaf= 5)

#Defición de las caracteristicas a usar y del objetivo
caracteristicas = preguntas[['ViewCount', 'Score', 'FavoriteCount']]
targets = preguntas['Importancia']

#Creación de la muestra de Entrenamiento (Train) y del test, para el cual sera 60(Train) y 40(Test)
#Random_State= 0 reproduciblidad   None No reproducibilidad 42 constante
pred_train, pred_test, tar_train, tar_test = train_test_split(caracteristicas, targets, test_size=0.3, random_state=42)

#Visualizacón del tamaño de las muestras
"""print(pred_test.shape)
print(pred_train.shape)
print(tar_test.shape)
print(tar_train.shape)"""

#Etiquetas a usar en el árbol
atributos = ['ViewCount', 'Score', 'FavoriteCount']

#creación del arbol y entreaniemto del mismo
arbolQ = DecisionTreeClassifier()
arbolQ = arbolQ.fit(pred_train, tar_train)

#Proabilidades de acierto del arbol con los datos de muestra y entrenamiento
print("------------------------------------------Árbol SIN Ajustar--------------------------------------------------")
print("Probabilidad del TEST: ", arbolQ.score(pred_test, tar_test))
print("Probabilidad de la ENTRENAMIENTO: ", arbolQ.score(pred_train, tar_train))

#Dibujado y pintado del Árbol
#dot_data= export_graphviz(clf,filled=True, rounded=True, special_characters=True, feature_names=feature_cols, class_names=['0', '1'])

dot_data= export_graphviz(arbolQ,filled=True,rounded=True,special_characters=True, class_names='Importancia', feature_names= atributos, impurity= False)
graph=  gfd(dot_data)
graph.write_png("Tesis_arbol_sin.png")
Image(graph.create_png())
predictions = arbolQ.predict(pred_test)

print("Matriz de Confusión")
print("Resultados: ", confusion_matrix(tar_test, predictions))

print("Cantidad de Aciertos")
print("Resultados: ", accuracy_score(tar_test, predictions))

print("Fracción de Etiquetas Incorrectas")
print("Resultados: ",hamming_loss(tar_test, predictions))

print("Datos De Predicción:", len(predictions))
print("Resultados: ", predictions)
print("Resumen:")


#Importancia de las Caracteristicas
caract= 3 # classifier.tree_.max_depth
plt.barh(range(caract), arbolQ.feature_importances_)
plt.yticks(np.arange(caract), atributos)
plt.xlabel("Importancia de las caracteristicas")
plt.ylabel("Caracteristicas")
plt.show()
print(arbolQ.feature_importances_)
#Sobreajuste del modelo para corregir el valor de acierto = 1
print("------------------------------------------Árbol SOBREAJUSTADO--------------------------------------------------")
arbolQ = DecisionTreeClassifier(max_depth=3)
arbolQ = arbolQ.fit(pred_train, tar_train)
print("Probabilidad del TEST: ", arbolQ.score(pred_test, tar_test))
print("Probabilidad de la PREDICCIÓN: ", arbolQ.score(pred_train, tar_train))
dot_data= export_graphviz(arbolQ,filled=True,rounded=True,special_characters=True, class_names='Importancia', feature_names= atributos, impurity= False)
graph=  gfd(dot_data)
graph.write_png("Tesis_arbol_con.png")
Image(graph.create_png())
#Datos Extas
print("Matriz de Confusión")
print("Resultados: ", confusion_matrix(tar_test, predictions))

print("Cantidad de Aciertos")
print("Resultados: ", accuracy_score(tar_test, predictions))

print("Fracción de Etiquetas Incorrectas")
print("Resultados: ",hamming_loss(tar_test, predictions))

print("Datos De Predicción:", len(predictions))
print("Resultados: ", predictions)
print("Resumen:")

print(np.unique(predictions,return_counts=True))

"""out = StringIO()
tree.export_graphviz(classifier, out_file='treeSOES.dot')"""