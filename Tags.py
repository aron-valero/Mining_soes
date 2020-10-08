import pymysql
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from speechd_config import question

db = pymysql.connect("localhost", "root", "kacvo123", "UG_SOES")
cursor = db.cursor()
sql = "SELECT Tags.TagName as tag, count(*) as cantidad " \
      " FROM UG_SOES.Question, Posts_ES, Users_Country, Question_has_Tags, Tags" \
      " where " \
      " Question.Id= Posts_ES.Id and" \
      " Users_Country.Id = Posts_ES.OwnerUserId and" \
      " Users_Country.Country like 'ecuador' and" \
      " Question_has_Tags.Question_Id = Question.Id and" \
      " Question_has_Tags.Tags_Id = Tags.Id" \
      " group by Question_has_Tags.Tags_Id" \
      " order by count(*) desc ;"
cursor.execute(sql)
tags = cursor.fetchall()

sql = "SELECT Question_Id as id, COUNT(Tags_Id) as cantidad, Question.Tags as tags " \
      " FROM UG_SOES.Question_has_Tags, Posts_ES, Users_Country, Question" \
      " WHERE Question_has_Tags.Question_Id = Posts_ES.Id AND Question.Id = Posts_ES.Id" \
      " AND Users_Country.Id = Posts_ES.OwnerUserId AND Users_Country.Country LIKE 'ecuador'" \
      " GROUP BY Question_Id ORDER BY COUNT(Tags_Id) DESC;"
cursor.execute(sql)
grupos = cursor.fetchall()
pd.set_option('display.max_columns',None)
pd.set_option('display.max_row',None)
resultado =pd.DataFrame(data= {'Cantidad':['Tag1','Tag2','Tag3','Tag4','Tag5']})
sql1 = "select Question.Id, Question.Title, Posts_ES.Body, Question.Tags, Posts_ES.CreationDate," \
                      " Posts_ES.OwnerUserId, Question.AcceptedAnswerId, Question.AnswerCount, Question.FavoriteCount, " \
                      "Posts_ES.Score, Posts_ES.ViewCount, Posts_ES.CommentCount from Question, Posts_ES" \
                      " where   Question.Tags Like '%<{}>%' AND Question.Id={} and Posts_ES.Id ={};"
questions = pd.DataFrame(columns= list(pd.read_sql_query(sql1.format(0, 0, 0), db)))#+list(["TPredominante"]))
questions['Cant_tags']=[]
questions['Tag_Predominante']=[]
questions['Cant_caracteres']=[]
questions['Cant_palabras']=[]
cursor.execute("select  count(Question.Id) as preguntas FROM Posts_ES, Users_Country, Question WHERE"
               "	Question.Id = Posts_ES.Id"
               "   AND Users_Country.Id =Posts_ES.OwnerUserId"
               " AND Users_Country.Country LIKE 'ecuador'")
cantidad_p= cursor.fetchone()
tabla = pd.DataFrame(columns=('Conjunto','Tag','preguntas_ABS','preguntas_REL'))
i=0
d=0
cont=0
#Sin porcentaje
#for t in tags[:10]:
contador = 0
for t in tags:
    print(t)
    e = []
    acumulada=[]
    aux=0
    for c in range(1,6):
        for fila in  grupos:
            if fila[1]==c:
                band = pd.read_sql_query(sql1.format(t[0], fila[0],fila[0]),db)
                band['Cant_tags'] = c
                if contador < 10:
                    band['Tag_Predominante'] = t[0]
                else:
                    band['Tag_Predominante'] = None
                contador+=1
                if len(band)==1:
                    #band["Body"]=str(band["Body"][0])[3:-3]
                    #temp = str(band["Body"][0]).split()
                    temp = re.split(' |\<p>|\</p>', str(band["Body"][0]))
                    #print(temp)
                    carac = 0
                    for tem in temp:
                        carac += len(tem)
                    band['Cant_caracteres']=carac
                    band['Cant_palabras']=len(temp)
                    questions=questions.append(band[0:1],ignore_index=True)
                    d=d+1
                    aux=aux+1
                    i=i+1
        e = np.insert(e, c-1, d)
        acumulada= np.insert(acumulada,c-1, aux)
        d=0
    tabla.loc[cont]=["Dataset{0}".format(cont+1),t[0],aux,round((aux/int(cantidad_p[0]))*100,2) ]
    cont=cont+1
    resultado[t[0]]=pd.Series(e).astype(int)
    resultado[t[0]+"Acu"]=pd.Series(acumulada).astype(int)
print("Total de Preguntas: ",i)
print(resultado)
print("TABLA DE VALORES")
print(tabla)
"""print("Estadísticos:")
print(resultado.describe())
print("Datos:")
print(questions)
"""
#print(questions["Body"][2])
print("Exportando CSV....")
questions.to_csv("/home/aronvalero/PycharmProjects/Ejercicio_1/UG_Tesis.csv", index=False, encoding='utf-8')
print("CSV Exportado!")
#Dataset = pd.read_csv("/home/aronvalero/PycharmProjects/Ejercicio_1/preguntas.csv")
#print("Imprimiendo Csv...")
#print(Dataset)
#Con porcentaje
"""for t in tags[:3]:
    e = []
    p = []
    #print("Tag: ",t[0])
    for c in range(1,6):
        for fila in  grupos:
            if fila[1]==c:
                sql1 = "Select * from  Question where Question.Tags Like '%<{}>%' AND Question.id={}".format(t[0], fila[0])
                cursor.execute(sql1)
                band = cursor.fetchall()
                if len(band)==1:
                    d=d+1
                i=i+1
        #print("Cantidad de Tags: ", c, " Total de Preguntas: ", i, "Uso del Tag: ",d )
        e = np.insert(e, c-1, d)
        p = np.insert(p, c - 1, round((d/i)*100,2))
        i=0
        d=0
    resultado[t[0]]=pd.Series(e).astype(int)
    resultado[t[0]+"%"]=pd.Series(p)
print(resultado)"""


#Con ID
"""resultado =pd.DataFrame()
for t in tags[:3]:
    e = []
    q = []
    #print("Tag: ",t[0])
    for c in range(1,6):
        for fila in  grupos:
            f = 0
            if fila[1]==c:
                sql1 = "Select * from  Question where Question.Tags Like '%<{}>%' AND Question.id={}".format(t[0], fila[0])
                cursor.execute(sql1)
                band = cursor.fetchall()
                if len(band)==1:
                    d=d+1
                    q = np.insert(q, f, fila[0])
                i=i+1
        #print("Cantidad de Tags: ", c, " Total de Preguntas: ", i, "Uso del Tag: ",d )
        e = np.insert(e, c-1, d)
        i=0
        d=0
    resultado[t[0]]=pd.Series(q).astype(int)

print(resultado)
"""