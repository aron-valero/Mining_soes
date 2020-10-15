#Package necesarios para el proceso
#1 estructuras de datos
import pandas as pd
import numpy as np
from collections import Counter, OrderedDict
from sklearn.feature_extraction.text import CountVectorizer
import operator
import matplotlib.pyplot as plt
#2 NAIVE BAYES
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
#[opcional] configuración para observar todos los registros del dataset
"""pd.set_option('display.max_columns',None)
pd.set_option('display.max_row',None)"""
#Consulta y obtención de los datos
dataset= pd.DataFrame(pd.read_csv("/home/aronvalero/PycharmProjects/Ejercicio_1/preguntas_pre.csv"))
#Definición de carcaterísticas 
x = dataset["Body"]
y = dataset["Tag_Predominante"]
#Separación de los datos: 80% entrenamiento y 20% prueba
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.2, random_state=42)
countervectorize = CountVectorizer()
entrenamiento = countervectorize.fit_transform(x_train)
prueba = countervectorize.transform(x_test)
#dataset que contiene las preguntas que se usaran en el clasificador
dataset1= pd.DataFrame(pd.read_csv("/home/aronvalero/PycharmProjects/Ejercicio_1/UG_Tesis_pre.csv", engine='python', encoding='utf-8'))
#[opcional] en caso de error con el tipo de  encoding
"""import chardet
rawdata= open("C:/Users/VALERO/Desktop/UG_Tesis_pre.csv",'rb').read()
result= chardet.detect(rawdata)
charenc= result['encoding']
print(charenc)
"""
#creación del modelo
naiveB = MultinomialNB()
naiveB.fit(entrenamiento, y_train)

predicciones = naiveB.predict(countervectorize.transform(dataset1["Body"]))
predicciones = naiveB.predict(prueba)
print(predicciones)
#Evaluación del modelo
from sklearn.metrics import  accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
print("Numero de filas: {} ".format(dataset.shape[0]))
print("X: {} ".format(x.shape))
print("X Entrenamiento: {} ".format(x_train.shape[0]))
print("X Prueba: {} ".format(x_test.shape[0]))
print("Y: {} ".format(y.shape))
print("Y Entrenamiento: {} ".format(y_train.shape[0]))
print("Y Prueba: {} ".format(y_test.shape[0]))
print("Exactitud: {}".format(accuracy_score(y_test,predicciones)))
print("Precision: {}".format(precision_score(y_test, predicciones, average=None)))
print("Sensibilidad: {}".format(recall_score(y_test, predicciones,average=None)))
print("Peso medio de las Puntuaciones: {}".format(f1_score(y_test,predicciones, average=None)))

print("Matriz de Confusión")
print(confusion_matrix(y_test, predicciones, labels=list(dataset["Tag_Predominante"].unique())))
print("Resumen: ")
print(classification_report(y_test, predicciones))
print(classification_report(y_test, predicciones))

#proceso de análisis de las preguntas que no tiene uno de los 10 tags principales
for pre in range(788,len(dataset1)):
    print(pre, " de ", len(dataset1))
    vector= [dataset1.iloc[pre]["Body"]]
    prueba = countervectorize.transform(vector)
    predicciones = naiveB.predict(prueba)
    print("Anterior: ",dataset1.loc[pre]["Tag_Predominante"])
    print("Prediccion: ",predicciones[0])
    dataset1.loc[pre,"Tag_Predominante"] = predicciones[0]
    print("Nuevo: ",dataset1.loc[pre]["Tag_Predominante"] )
print("Cambios: ",dataset1["Tag_Predominante"][788:800] )
print("Listo....")
print("Exportando CSV....")
dataset1.to_csv("/home/aronvalero/PycharmProjects/Ejercicio_1/UG_Tesis_Pre_Final.csv", index=False, encoding='utf-8')
print("CSV Exportado!")
dataset2= pd.DataFrame(pd.read_csv("/home/aronvalero/PycharmProjects/Ejercicio_1/UG_Tesis_Pre_Final.csv", engine='python', encoding='utf-8'))
print(dataset2.shape)
print(dataset2.groupby("Tag_Predominante").count())
