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
"""pd.set_option('display.max_columns',None)
pd.set_option('display.max_row',None)"""
nlp= es_core_news_sm.load()

#Preparación de los Datos
#Extraccion de Datos
dataset= pd.DataFrame(pd.read_csv("/home/aronvalero/PycharmProjects/Ejercicio_1/UG_Tesis_Pre_Final.csv"))
categoria=['javascript','python','php','java','html','django','jquery','mysql','c#', 'sql']
colores=['gray','rosybrown','cyan','sandybrown','slategray','plum','salmon','sienna','','coral']
#javascript = pd.DataFrame(columns= ("Body","Tags","Tag_Predominante"))
gramatica = "SPACE", "PRON", "VERB", "AUX", "DET", "SCONJ", "ADP", "CCONJ", "ADV", "ADJ", "NUM", "INTJ"
Todas_Palabras = []
#Palabras a eliminar
palabras_Reservadas=["null","comando","consulta","val","model","periodo","datos","elementos","main","void","j","t","int","new","select","true",
                     "información","if","for","aplicación","sistema","express","campo","clase","import","b","rhom",
                     "name","from","rho","x","self","var","botón","prueba","res","err","bar","result","com","cantidad","return",
                     "programa","let","problema","código","td","texto","codigo","error","this","nombre","usuario","ayuda",
                     "forma", "funció", "proyecto", "función"]
#Limpieza de datos
for cat in categoria[3:4]:
    tags = {}
    for pre in range (0,len(dataset)):
        if dataset.iloc[pre]["Tag_Predominante"]== cat:
            ora = nlp(u'{0}'.format(dataset.iloc[pre]["Body"]))
            texto = []
            for token in ora:
                if token.text not in palabras_Reservadas and token.text != cat:
                    texto.append(token.text)
                    Todas_Palabras.append(token.text)
            palabras=nlp(dataset.iloc[pre]["Tags"])
            for palabra in palabras:
                if palabra.text != ' ' and palabra.text != cat:
                    if palabra.text not in tags.keys():
                        tags[palabra.text] = 1
                    else:
                        tags[palabra.text] += 1
        #Tranformacion y eliminacion de palabras innecesarias
        #Palabras comunes dentro del cuerpo de las preguntas
        word_freq = Counter(Todas_Palabras)
        palabras_comunes = word_freq.most_common(11)
    #Mostrar palabras Comunes
    i=1
    pal=[]
    cant=[]
    print("Palabras Comunes en ", cat)
    for p in palabras_comunes:
        pal.append(p[0])
        cant.append(p[1])
        print("Palabra N. "+str(i)+": "+str(p))
        i=i+1
    #print(palabras_comunes.values())
    tags_ordenados = OrderedDict(sorted(tags.items(), key=lambda x: x[1], reverse=True))
    print("Tags Comunes en ", cat)
    print(list(tags_ordenados)[:10])
    plt.figure(figsize=(10,10))
    plt.subplot(2,2,1)
    plt.title("Palabras de discusión para "+ cat)
    plt.ylabel("Temas")
    plt.xlabel("Cantidad")
    plt.barh(range(0, 10), cant[:10], align='center', color=colores[categoria.index(cat)])
    plt.yticks(range(0, 10), pal[:10] )

    plt.subplot(2,2,2)
    plt.title("Temas Candentes de discusión para " + cat)
    plt.ylabel("Temas")
    plt.xlabel("Cantidad")
    plt.barh(range(0, 10), list(tags_ordenados.values())[:10], align='center', color=colores[categoria.index(cat)])
    plt.yticks(range(0, 10), list(tags_ordenados.keys())[:10])
    plt.tight_layout()
    plt.show()
    Todas_Palabras.clear()
    tags.clear()
