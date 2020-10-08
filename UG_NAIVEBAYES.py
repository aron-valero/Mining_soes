#Librerias
import pandas as pd
import numpy as np
import re
import spacy
import es_core_news_sm
from spacy_spanish_lemmatizer import  SpacyCustomLemmatizer
from spacy import displacy
from spacy.lang.es.stop_words import STOP_WORDS
from collections import Counter, OrderedDict
from sklearn.feature_extraction.text import CountVectorizer
import textacy
import operator
import matplotlib.pyplot as plt

#Declaraciones e inicializaciones
pd.set_option('display.max_columns',None)
pd.set_option('display.max_row',None)
nlp= es_core_news_sm.load()

#Preparación de los Datos
#Extraccion de Datos
#dataset= pd.DataFrame(pd.read_csv("/home/aronvalero/PycharmProjects/Ejercicio_1/preguntas.csv"))
"""
#javascript = pd.DataFrame(columns= ("Body","Tags","Tag_Predominante"))
gramatica = "SPACE", "PRON", "VERB", "AUX", "DET", "SCONJ", "ADP", "CCONJ", "ADV", "ADJ", "NUM", "INTJ"
Todas_Palabras = []

#Palabras a eliminar
palabras_Reservadas=["problema","código","td","texto","codigo","error","this","nombre","usuario","ayuda", "forma", ""]
#Limpieza de datos
#788
for pre in range (0,len(dataset[:788])):
    preguntas_ALL = str(dataset.iloc[pre]["Body"]).lower()
    #Eliminar Etiquetas
    preguntas_ALL = re.sub('&(#)*[a-z]{2,2}.', ' ', preguntas_ALL)
    preguntas_ALL = re.sub('http(s)*\:\/\/', '', preguntas_ALL)
    preguntas_ALL = re.sub(r'<[^>]*>', ' ', preguntas_ALL)
    preguntas_ALL = re.sub(r'\s+', ' ', preguntas_ALL)
    preguntas_ALL = re.sub(r'[a-z]*(\-)*[a-z]+\=(\"|\')+[a-z\s]+(\-)*[a-z]*(\"|\')+', ' ', preguntas_ALL)
    #preguntas_javascript = re.sub('\<(/)*[a-z]+\>', ' ', preguntas_javascript)
    preguntas_ALL = re.sub('&(#)*[a-z]{2,2}.', ' ', preguntas_ALL)
    preguntas_ALL = re.sub('[a-z]+\-[a-z]+', ' ', preguntas_ALL)
    #Eliminar Número y Carcateres Especiales
    preguntas_ALL = re.sub('[^a-zA-ZáéíóúÁÉÍÓÚ]', ' ', preguntas_ALL)
    #Eliminar más de dos espacios en blanco
    preguntas_ALL = re.sub(r'\s+', ' ', preguntas_ALL)
    preguntas_ALL = re.sub('base(s)* de dato(s)*', 'database', preguntas_ALL)
    aux= {"Body": preguntas_ALL, "Tags": dataset.iloc[pre]["Tags"], "Tag_Predominante":dataset.iloc[pre]["Tag_Predominante"]}
   # dataset.loc[dataset["Body"]==dataset.iloc[pre]["Body"], "Body"]= aux["Body"]
   # ora = nlp(u'{0}'.format(str(dataset.iloc[pre]["Body"])))
    ora = nlp(u'{0}'.format(aux["Body"]))
    texto = []
    for token in ora:
        if (token.pos_ not in gramatica) and (token.is_stop == False) and (token.text not in palabras_Reservadas):
            texto.append(token.text)
            Todas_Palabras.append(token.text)
    dataset.loc[dataset["Body"] == dataset.iloc[pre]["Body"], "Body"] = ' '.join(texto)
    tags_ALL= str(dataset.iloc[pre]["Tags"]).lower()
    # Eliminar Etiquetas
    tags_ALL = re.sub('\<', '', tags_ALL)
    #tags_ALL = re.sub('javascript', '', tags_ALL)
    tags_ALL = re.sub('\>', ' ', tags_ALL)
    tags_ALL = re.sub('\s+', ' ', tags_ALL)
    dataset.loc[dataset["Tags"] == dataset.iloc[pre]["Tags"], "Tags"] = tags_ALL

#Tranformacion y eliminacion de palabras innecesarias
#Palabras comunes dentro del cuerpo de las preguntas
word_freq = Counter(Todas_Palabras)
palabras_comunes = word_freq.most_common(30)
"""
"""#Mostrar palabras Comunes
i=1
for p in palabras_comunes:
    print("Palabra N. "+str(i)+": "+str(p))
    i=i+1

#Tags Mas comunes
tags = {}
for p in range (0,len(dataset[:788])):
    tags_ALL = str(dataset.iloc[p]["Tags"]).lower()
    palabras= nlp(tags_ALL)
    for palabra in  palabras:
        if palabra.text != ' ':
            if palabra.text not in tags.keys() :
                tags[palabra.text]=1
            else:
                tags[palabra.text] += 1
tags_ordenados = OrderedDict(sorted(tags.items(),key=lambda  x: x[1], reverse=True))
plt.bar(range(0,10), list(tags_ordenados.values())[:10],align='center')
plt.xticks(range(0,10),list(tags_ordenados.keys())[:10])
plt.show()
"""
#print(dataset.dtypes)
#NAIVE BAYES
dataset= pd.DataFrame(pd.read_csv("/home/aronvalero/PycharmProjects/Ejercicio_1/preguntas_pre.csv"))
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
#x = df.iloc[:,[2,3]]
carcateristicas = dataset[["Body","Tags"]]
x = dataset["Body"]
#x= carcateristicas
y = dataset["Tag_Predominante"]
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.10, random_state=0)
print("Numero de filas: {} ".format(dataset.shape[0]))
print("X: {} ".format(x.shape))
print("X Entrenamiento: {} ".format(x_train.shape[0]))
print("X Prueba: {} ".format(x_test.shape[0]))
print("Y: {} ".format(y.shape))
print("Y Entrenamiento: {} ".format(y_train.shape[0]))
print("Y Prueba: {} ".format(y_test.shape[0]))
countervectorize = CountVectorizer()
entrenamiento = countervectorize.fit_transform(x_train)
data_prueba= pd.DataFrame(pd.read_csv("/home/aronvalero/PycharmProjects/Ejercicio_1/UG_Tesis_pre.csv"))
prueba = countervectorize.transform(x_test)
prueba1 = countervectorize.transform(np.array(data_prueba["Body"][0:]))
from sklearn.naive_bayes import MultinomialNB
naiveB = MultinomialNB()
naiveB.fit(entrenamiento, y_train)
#naiveB.partial_fit(entrenamiento, y_train,classes=dataset["Tag_Predominante"])
predicciones = naiveB.predict(prueba1)
print(predicciones)
from sklearn.metrics import  accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
print("Exactitud: {}".format(accuracy_score(y_test,predicciones)))
print("Precision: {}".format(precision_score(y_test, predicciones, average=None)))
print("Sensibilidad: {}".format(recall_score(y_test, predicciones,average=None)))
print("Peso medio de las Puntuaciones: {}".format(f1_score(y_test,predicciones, average=None)))
print("Matriz de Confusión")
print(confusion_matrix(y_test, predicciones, labels=list(dataset["Tag_Predominante"].unique())))
print("Resumen: ")
print(classification_report(y_test, predicciones))