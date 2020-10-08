import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymysql
from IPython.display import display
import ipywidgets as widgets
from scipy._lib._ccallback_c import plus1_t

db= pymysql.connect("localhost","root","kacvo123","UG_SOES")
cursor = db.cursor()

#TOTAL POSTS
"""sql ="select ( select count(*) Cantidad from Posts_ES) as TOTAL," \
     "	   ( select count(*) Cantidad" \
     "       from Posts_ES, Users_Country" \
     "       where Posts_ES.OwnerUserId = Users_Country.Id" \
     "       and Users_Country.Country not like 'ecuador') as SOES," \
     "   ( select count(*) Cantidad" \
     "       from Posts_ES, Users_Country" \
     "       where Posts_ES.OwnerUserId = Users_Country.Id" \
     "       and Users_Country.Country like 'ecuador') as Ecuador;"
posts= pd.DataFrame(pd.read_sql_query(sql, db))
cantidad = np.array([(np.array(posts))[0,1], (np.array(posts))[0,2]])
mensaje = "Total de POSTS: ",(np.array(posts))[0,0]
plt.title("Gráfico: Posts ")
plt.xlabel(mensaje)
plt.pie(cantidad, labels=list(posts.iloc[:, 1:3]), startangle=90, shadow=True, autopct= "%0.2f%%")
"""
#TOTAL QUESTIONS
"""sql ="select ( select count(*) Cantidad from Posts_ES, Question Where Question.Id=Posts_ES.Id) as TOTAL," \
     "	   ( select count(*) Cantidad" \
     "       from Posts_ES, Users_Country, Question" \
     "       where Question.Id=Posts_ES.Id and Posts_ES.OwnerUserId = Users_Country.Id" \
     "       and Users_Country.Country not like 'ecuador') as SOES," \
     "   ( select count(*) Cantidad" \
     "       from Posts_ES, Users_Country, Question" \
     "       where Question.Id=Posts_ES.Id and Posts_ES.OwnerUserId = Users_Country.Id" \
     "       and Users_Country.Country like 'ecuador') as Ecuador;"
posts= pd.DataFrame(pd.read_sql_query(sql, db))
cantidad = np.array([(np.array(posts))[0,1], (np.array(posts))[0,2]])
mensaje = "Total  QUESTIONS: ",(np.array(posts))[0,0]
plt.title("Gráfico: QUESTIONS ")
plt.xlabel(mensaje)
plt.pie(cantidad, labels=list(posts.iloc[:, 1:3]), startangle=90, shadow=True, autopct= "%0.2f%%")
"""
#TOTAL ANSWERS
"""sql ="select ( select count(*) Cantidad from Posts_ES, Answer Where Answer.Id=Posts_ES.Id) as TOTAL," \
     "	   ( select count(*) Cantidad" \
     "       from Posts_ES, Users_Country, Answer" \
     "       where Answer.Id=Posts_ES.Id and Posts_ES.OwnerUserId = Users_Country.Id" \
     "       and Users_Country.Country not like 'ecuador') as SOES," \
     "   ( select count(*) Cantidad" \
     "       from Posts_ES, Users_Country, Answer" \
     "       where Answer.Id=Posts_ES.Id and Posts_ES.OwnerUserId = Users_Country.Id" \
     "       and Users_Country.Country like 'ecuador') as Ecuador;"
posts= pd.DataFrame(pd.read_sql_query(sql, db))
cantidad = np.array([(np.array(posts))[0,1], (np.array(posts))[0,2]])
mensaje = "Total  ANSWERS: ",(np.array(posts))[0,0]
plt.title("Gráfico: ANSWERS ")
plt.xlabel(mensaje)
plt.pie(cantidad, labels=list(posts.iloc[:, 1:3]), startangle=90, shadow=True, autopct= "%0.2f%%")
"""

#POSTS
#TOTAL
"""
sql = "select year(CreationDate) Año, count(*) Cantidad from Posts_ES group by year(CreationDate);"
posts_año = pd.read_sql_query(sql, db)
px2= np.arange(6)
plt.xticks(px2, list(posts_año["Año"]))
plt.ylabel("Cantidad")
plt.title("Gráfico: Posts por año")
plt.bar(px2, posts_año["Cantidad"])
"""
#Ecuatorianos
"""sql = " select year(CreationDate) Año, count(*) Cantidad from Posts_ES, Users_Country where" \
      " Posts_ES.OwnerUserId = Users_Country.Id " \
      " and Users_Country.Country like 'ecuador' " \
      " group by year(CreationDate);"
posts_año_ec= pd.read_sql_query(sql, db)
px2= np.arange(6)
plt.xticks(px2, list(posts_año_ec["Año"]))
plt.ylabel("Cantidad")
plt.title("Gráfico: Posts de los Usuarios Ecuatorianos por año")
plt.bar(px2, posts_año_ec["Cantidad"])"""

#QUESTIONS
#Total
"""sql = "select year(CreationDate) Año, count(*) Cantidad from Posts_ES, Question, Users_Country" \
      " where Question.Id = Posts_ES.OwnerUserId" \
      " AND Posts_ES.OwnerUserId = Users_Country.Id" \
      " group by year(CreationDate);"
question= pd.read_sql_query(sql, db)
px2= np.arange(6)
plt.xticks(px2, list(question["Año"]))
plt.ylabel("Cantidad")
plt.title("Gráfico: Preguntas Agrupadas por año")
i = 0
for p in question["Cantidad"]:
      plt.text(i, p+60, p, horizontalalignment= "center", verticalalignment="center")
      i=i+1
plt.bar(px2, question["Cantidad"])
"""

#Ecuatorianos
"""sql = "select year(CreationDate) Año, count(*) Cantidad from Posts_ES, Question, Users_Country" \
      " where Question.Id = Posts_ES.OwnerUserId" \
      " AND Posts_ES.OwnerUserId = Users_Country.Id" \
      " group by year(CreationDate);"
question= pd.read_sql_query(sql, db)

sql = "select year(CreationDate) Año, count(*) Cantidad from Posts_ES,Question, Users_Country" \
      " where Question.Id = Posts_ES.OwnerUserId AND Posts_ES.OwnerUserId = Users_Country.Id" \
      " and Users_Country.Country like 'ecuador' group by year(CreationDate);"
question_ec= pd.read_sql_query(sql, db)
px2= np.arange(len(question_ec["Año"]))
plt.xticks(px2, list(question_ec["Año"]))
plt.ylabel("Cantidad")
plt.title("Gráfico: Preguntas de los Usuarios Ecuatorianos Agrupadas por año")
i= 0
for p in  question_ec["Cantidad"]:
      mensaje = str(p)+"-"+"{0:0.2%}".format(p/question["Cantidad"][i+1])
      plt.text(i,p+6, mensaje,horizontalalignment= "center", verticalalignment="center" )
      i=i+1
plt.bar(px2, question_ec["Cantidad"],color="r")
"""
#ANSWER
#TOTAL
"""
sql= " select year(CreationDate) Año, count(*) Cantidad from Posts_ES, Answer, Users_Country" \
     " where Answer.Id = Posts_ES.OwnerUserId AND Posts_ES.OwnerUserId = Users_Country.Id " \
     " group by year(CreationDate);"
answer= pd.read_sql_query(sql, db)
px2= np.arange(len(answer["Año"]))
plt.xticks(px2, list(answer["Año"]))
plt.ylabel("Cantidad")
plt.title("Gráfico: Respuestas Agrupadas por año")
i = 0
for p in answer["Cantidad"]:
      plt.text(i, p+100, p, horizontalalignment= "center", verticalalignment="center")
      i=i+1
plt.bar(px2, answer["Cantidad"])
"""
#Ecuatorianos
"""sql= " select year(CreationDate) Año, count(*) Cantidad from Posts_ES, Answer, Users_Country" \
     " where Answer.Id = Posts_ES.OwnerUserId AND Posts_ES.OwnerUserId = Users_Country.Id " \
     " group by year(CreationDate);"
answer= pd.read_sql_query(sql, db)

sql = "select year(CreationDate) Año, count(*) Cantidad from Posts_ES,Answer, Users_Country" \
      " where Answer.Id = Posts_ES.OwnerUserId AND Posts_ES.OwnerUserId = Users_Country.Id " \
      " and Users_Country.Country like 'ecuador'  group by year(CreationDate);"
answer_ec = pd.read_sql_query(sql, db)
px2= np.arange(len(answer_ec["Año"]))
plt.xticks(px2, list(answer_ec["Año"]))
plt.ylabel("Cantidad")
plt.title("Gráfico: Preguntas de los Usuarios Ecuatorianos Agrupadas por año")
i= 0
for p in answer_ec["Cantidad"]:
      mensaje = str(p)+"-"+"{0:0.2%}".format(p/answer["Cantidad"][i])
      plt.text(i,p+6, mensaje,horizontalalignment= "center", verticalalignment="center" )
      i=i+1
plt.bar(px2, answer_ec["Cantidad"],color="r")
"""
"""sql = "select year(CreationDate) Año, count(*) Cantidad from Posts_ES,Answer, Users_Country" \
      " where Answer.Id = Posts_ES.OwnerUserId AND Posts_ES.OwnerUserId = Users_Country.Id " \
      " and Users_Country.Country like 'ecuador'  group by year(CreationDate);"
answer_ec = pd.read_sql_query(sql, db)
px2= np.arange(len(answer_ec["Año"]))
sql = "select year(CreationDate) Año, count(*) Cantidad from Posts_ES,Question, Users_Country" \
      " where Question.Id = Posts_ES.OwnerUserId AND Posts_ES.OwnerUserId = Users_Country.Id" \
      " and Users_Country.Country like 'ecuador' group by year(CreationDate);"
question_ec= pd.read_sql_query(sql, db)
px1= np.array([1, 2, 3, 4, 5])
fig, ax= plt.subplots()
ax.bar(px2,answer_ec["Cantidad"], label="Respuestas")
ax.bar(px1,question_ec["Cantidad"], bottom= answer_ec["Cantidad"],label="Preguntas")
ax.legend(loc=(1.1,0.8))
"""
"""
#COMMENTS
select year(CreationDate) Año, count(*) Cantidad from Comments
group by year(CreationDate);

select year(CreationDate) Año, count(*) Cantidad from Comments,Users_Country
where
Comments.Users_Id=Users_Country.Id
and Users_Country.Country like 'ecuador'
group by year(CreationDate);
"""
#Tendencias
#Ecuatorianos

"""sql = " select year(CreationDate) Año, count(*) Cantidad from Posts_ES, Users_Country where" \
      " Posts_ES.OwnerUserId = Users_Country.Id " \
      " and Users_Country.Country like 'ecuador' " \
      " group by year(CreationDate);"
posts_año_ec= pd.read_sql_query(sql, db)"""
sql = "select year(CreationDate) Año, count(*) Cantidad from Posts_ES,Question, Users_Country" \
      " where Question.Id = Posts_ES.OwnerUserId AND Posts_ES.OwnerUserId = Users_Country.Id" \
      " and Users_Country.Country like 'ecuador' group by year(CreationDate);"
question_ec= pd.read_sql_query(sql, db)
print(question_ec)
sql = "select year(CreationDate) Año, count(*) Cantidad from Posts_ES,Answer, Users_Country" \
      " where Answer.Id = Posts_ES.OwnerUserId AND Posts_ES.OwnerUserId = Users_Country.Id " \
      " and Users_Country.Country like 'ecuador'  group by year(CreationDate);"
answer_ec = pd.read_sql_query(sql, db)
print(answer_ec)

posts_año_ec=pd.DataFrame({'Año':[2015, 2016, 2017, 2018, 2019, 2020], 'Cantidad':[answer_ec["Cantidad"][0],answer_ec["Cantidad"][1]+question_ec["Cantidad"][0],answer_ec["Cantidad"][2]+question_ec["Cantidad"][1],answer_ec["Cantidad"][3]+question_ec["Cantidad"][2],answer_ec["Cantidad"][4]+question_ec["Cantidad"][3],answer_ec["Cantidad"][5]+question_ec["Cantidad"][4] ]})
print(posts_año_ec)
posts_año_ec= posts_año_ec.assign(Etiqueta=pd.Series(["Posts" for a in range(len(posts_año_ec)) ]))
question_ec= question_ec.assign(Etiqueta=pd.Series(["Questions" for a in range(len(question_ec)) ]))
answer_ec= answer_ec.assign(Etiqueta=pd.Series(["Answers" for a in range(len(answer_ec)) ]))

todo= pd.concat([posts_año_ec, question_ec, answer_ec], axis=0, ignore_index=True)

import plotnine as p9
plot= p9.ggplot(data=todo, mapping=p9.aes(x='Año', y='Cantidad', color='Etiqueta')) +p9.geom_line() +p9.labs(title="Gráfico: Posts de los Usuarios Ecuatorianos por año")
plot.draw()

print("Ecuador")
print(todo)
#Todos
"""sql = "select year(CreationDate) Año, count(*) Cantidad from Posts_ES group by year(CreationDate);"
posts_año = pd.read_sql_query(sql, db)"""
sql = "select year(CreationDate) Año, count(*) Cantidad from Posts_ES, Question, Users_Country" \
      " where Question.Id = Posts_ES.OwnerUserId" \
      " AND Posts_ES.OwnerUserId = Users_Country.Id" \
      " group by year(CreationDate);"
question= pd.read_sql_query(sql, db)
sql= " select year(CreationDate) Año, count(*) Cantidad from Posts_ES, Answer, Users_Country" \
     " where Answer.Id = Posts_ES.OwnerUserId AND Posts_ES.OwnerUserId = Users_Country.Id " \
     " group by year(CreationDate);"
answer= pd.read_sql_query(sql, db)
posts_año=pd.DataFrame({'Año':[2015, 2016, 2017, 2018, 2019, 2020], 'Cantidad':[answer["Cantidad"][0]+question["Cantidad"][0],answer["Cantidad"][1]+question["Cantidad"][1],answer["Cantidad"][2]+question["Cantidad"][2],answer["Cantidad"][3]+question["Cantidad"][3],answer["Cantidad"][4]+question["Cantidad"][4],answer["Cantidad"][5]+question["Cantidad"][5] ]})
print(posts_año)

posts_año= posts_año.assign(Etiqueta=pd.Series(["Posts" for a in range(len(posts_año)) ]))
question= question.assign(Etiqueta=pd.Series(["Questions" for a in range(len(question)) ]))
answer= answer.assign(Etiqueta=pd.Series(["Answers" for a in range(len(answer)) ]))

todo= pd.concat([posts_año, question, answer], axis=0, ignore_index=True)

import plotnine as p9
plot= p9.ggplot(data=todo, mapping=p9.aes(x='Año', y='Cantidad', color='Etiqueta')) +p9.geom_line() +p9.labs(title="Gráfico: Posts de los Usuarios A nivel Mundial por año")
plot.draw()

print("Mundo")
print(todo)
plt.show()