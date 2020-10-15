#Paquetes y módulos
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

#Declaraciones e inicializaciones
#1 configuración para ver todos los datos del Dataframe
pd.set_option('display.max_columns',None)
pd.set_option('display.max_row',None)
#2 cargar el diccionario a usar 
nlp= es_core_news_sm.load()

#Preparación de los Datos
#1 extracción de Datos
dataset= pd.DataFrame(pd.read_csv("/home/aronvalero/PycharmProjects/Ejercicio_1/UG_Tesis.csv"))
print(dataset.shape)

#2 categorías gramaticales que se van a eliminar
gramatica = "SPACE", "PRON", "VERB", "AUX", "DET", "SCONJ", "ADP", "CCONJ", "ADV", "ADJ", "NUM", "INTJ"
Todas_Palabras = []

#Limpieza de datos
#1 rango de acción
for pre in range (0,len(dataset)):
    print("Listo ",pre)
    print("Pregunta con ruido")
    print(str(dataset.iloc[pre]["Body"]).lower())
    preguntas_ALL = str(dataset.iloc[pre]["Body"]).lower()
    #2 expresiones regulares 
    #2.1. eliminar Etiquetas
    preguntas_ALL = re.sub('&(#)*[a-z]{2,2}.', ' ', preguntas_ALL)
    preguntas_ALL = re.sub('http(s)*\:\/\/', '', preguntas_ALL)
    preguntas_ALL = re.sub(r'<[^>]*>', ' ', preguntas_ALL)
    preguntas_ALL = re.sub(r'\s+', ' ', preguntas_ALL)
    preguntas_ALL = re.sub(r'[a-z]*(\-)*[a-z]+\=(\"|\')+[a-z\s]+(\-)*[a-z]*(\"|\')+', ' ', preguntas_ALL)
    preguntas_ALL = re.sub('&(#)*[a-z]{2,2}.', ' ', preguntas_ALL)
    preguntas_ALL = re.sub('[a-z]+\-[a-z]+', ' ', preguntas_ALL)
    #2.2. eliminar Número y Carcateres Especiales
    preguntas_ALL = re.sub('[^a-zA-ZáéíóúÁÉÍÓÚ]', ' ', preguntas_ALL)
    #2.3. eliminar más de dos espacios en blanco
    preguntas_ALL = re.sub(r'\s+', ' ', preguntas_ALL)
    preguntas_ALL = re.sub('base(s)* de dato(s)*', 'database', preguntas_ALL)
    aux= {"Body": preguntas_ALL, "Tags": dataset.iloc[pre]["Tags"], "Tag_Predominante":dataset.iloc[pre]["Tag_Predominante"]}
    #3 transformar 
    ora = nlp(u'{0}'.format(aux["Body"]))
    texto = []
    #3.1. eliminación de palabras vacias 	
    for token in ora:
        if (token.pos_ not in gramatica) and (token.is_stop == False):
            texto.append(token.text)
            Todas_Palabras.append(token.text)
    #3.2. actualizar los registros del dataset
    dataset.loc[dataset["Body"] == dataset.iloc[pre]["Body"], "Body"] = ' '.join(texto)
    tags_ALL= str(dataset.iloc[pre]["Tags"]).lower()
    #4 eliminar simbolos <> de las etiquetas
    tags_ALL = re.sub('\<', '', tags_ALL)
    tags_ALL = re.sub('\>', ' ', tags_ALL)
    tags_ALL = re.sub('\s+', ' ', tags_ALL)
    dataset.loc[dataset["Tags"] == dataset.iloc[pre]["Tags"], "Tags"] = tags_ALL
    print("Pregunta luego de aplicar expresiones regulares y PLN")
    print(dataset.iloc[pre]["Body"])
#Exportar el resultado
print("Exportando CSV....")
dataset.to_csv("/home/aronvalero/PycharmProjects/Ejercicio_1/UG_Tesis_pre.csv", index=False, encoding='utf-8')
print("CSV Exportado!")
