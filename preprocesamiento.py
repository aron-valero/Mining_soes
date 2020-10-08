#Librerias
import pandas as pd
import re
import spacy
import es_core_news_sm
import numpy as np
from spacy_spanish_lemmatizer import  SpacyCustomLemmatizer
from spacy import displacy
from spacy.lang.es.stop_words import STOP_WORDS
from collections import Counter, OrderedDict
from sklearn.feature_extraction.text import CountVectorizer
import textacy
import operator
import matplotlib.pyplot as plt
"""
import pymysql
db = pymysql.connect("localhost", "root", "kacvo123", "UG_SOES")
cursor = db.cursor()

sql="select Question.Id, Question.Title, Posts_ES.Body, Question.Tags, Posts_ES.CreationDate," \
                      " Posts_ES.OwnerUserId, Question.AcceptedAnswerId, Question.AnswerCount, Question.FavoriteCount, " \
                      "Posts_ES.Score, Posts_ES.ViewCount, Posts_ES.CommentCount from Question, Posts_ES,Users_Country" \
                      " where 	Question.Id = Posts_ES.Id"\
     "   AND Users_Country.Id =Posts_ES.OwnerUserId"\
     " AND Users_Country.Country LIKE 'ecuador'"
preguntas = pd.read_sql_query(sql, db)
"""
#Declaraciones e inicializaciones
pd.set_option('display.max_columns',None)
pd.set_option('display.max_row',None)

nlp= es_core_news_sm.load()

#Preparación de los Datos
#Extraccion de Datos
dataset= pd.DataFrame(pd.read_csv("/home/aronvalero/PycharmProjects/Ejercicio_1/UG_Tesis.csv"))
print(dataset.shape)
"""print("Todas: ",dataset1.shape)
#error= pd.read_csv("/home/aronvalero/PycharmProjects/Ejercicio_1/preguntas.csv")
dataset2= pd.DataFrame(pd.read_csv("/home/aronvalero/PycharmProjects/Ejercicio_1/preguntas.csv"))
print("10 Tags: ",dataset2.shape)
ar= np.array(dataset2["Id"])
print("Preguntas: ",preguntas.shape)
Preguntas_sinUsar= pd.DataFrame(columns=list(dataset1.columns))
Preguntas_Usadas= pd.DataFrame(columns=list(dataset1.columns))
for pre in range (0,len(dataset1)):
    p= np.array(Preguntas_Usadas["Id"])
    print(p)
    if dataset1.iloc[pre]["Id"] not in ar :
        Preguntas_sinUsar = Preguntas_sinUsar.append(dataset1.iloc[pre], ignore_index=True)
    elif (dataset1.iloc[pre]["Id"] not in p ):
        Preguntas_Usadas = Preguntas_Usadas.append(dataset1.iloc[pre], ignore_index=True)
    else:
        print("Ya Esta")
print("SinUSar: ",Preguntas_sinUsar.shape)
print("Usadas: ", Preguntas_Usadas.shape)
"""

"""print(dataset.drop_duplicates(subset='Id', keep='first'))
print(dataset["Tag_Predominante"].value_counts())"""

#javascript = pd.DataFrame(columns= ("Body","Tags","Tag_Predominante"))

gramatica = "SPACE", "PRON", "VERB", "AUX", "DET", "SCONJ", "ADP", "CCONJ", "ADV", "ADJ", "NUM", "INTJ"
Todas_Palabras = []

#Limpieza de datos
#788
for pre in range (0,len(dataset)):
    print("Listo ",pre)
    print("Pregunta con ruido")
    print(str(dataset.iloc[pre]["Body"]).lower())
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
        if (token.pos_ not in gramatica) and (token.is_stop == False):
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
    print("Pregunta luego de aplicar expresiones regulares y PLN")
    print(dataset.iloc[pre]["Body"])
"""print("Exportando CSV....")
dataset.to_csv("/home/aronvalero/PycharmProjects/Ejercicio_1/UG_Tesis_pre.csv", index=False, encoding='utf-8')
print("CSV Exportado!")
print(dataset.shape)"""