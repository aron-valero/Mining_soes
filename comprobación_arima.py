import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymysql
db = pymysql.connect("localhost", "root", "kacvo123", "UG_SOES")
#Consulta y obtención de los datos
sql = "select Id from  Users_Country where Users_Country.Country LIKE 'ecuador';"
ec_id = pd.read_sql_query(sql, db)
#Extracción de los id de los usuarios ecuatorianos
ecuatorianos= np.array(ec_id["Id"])
#Dataset con los datos de los meses de abril-septiembre
dataset= pd.read_csv("/home/aronvalero/PycharmProjects/Ejercicio_1/Abril-Septiembre.csv", error_bad_lines=False)
dataset["CreationDate"]= pd.to_datetime(dataset["CreationDate"])
dataset["OwnerUserId"]=dataset["OwnerUserId"].fillna(0)
dataset["OwnerUserId"]= pd.to_numeric(dataset["OwnerUserId"], downcast='integer')
post= pd.DataFrame(columns=list(dataset))
preguntas= pd.DataFrame(columns=list(dataset))
respuestas= pd.DataFrame(columns=list(dataset))
#comprobación de cada uno de los datos
for pre in range (0,len(dataset)):
    print(pre, " de ", len(dataset))
    print("ID Consultado: ",dataset.iloc[pre]["OwnerUserId"])
    if dataset.iloc[pre]["OwnerUserId"] in ecuatorianos:
            print("Ecuatoriano: ------------SI------------")
            post = post.append(dataset.iloc[pre], ignore_index=True)
            if dataset.iloc[pre]["PostTypeId"] == 1:
                preguntas = preguntas.append(dataset.iloc[pre], ignore_index=True)
            elif dataset.iloc[pre]["PostTypeId"] == 2:
                respuestas = respuestas.append(dataset.iloc[pre], ignore_index=True)
    else:
            print("Ecuatoriano: NO")
print("TOTAL CONSULTADO de ABRIL A SEPTIEMBRE: ", dataset.shape)
print("Post:",post.shape)
print("Preguntas: ", preguntas.shape)
print("Respuestas: ",respuestas.shape)
print("Datos:")
post["Mes"]= pd.DatetimeIndex(post["CreationDate"]).month
print(post.groupby("Mes").count())
