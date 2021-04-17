import json
import pymongo
import sys
import datetime
import pprint
import matplotlib.pyplot as plt

conStr = "mongodb://localhost:27017/"
# conStr = "mongodb+srv://owner:{}@cluster0.uvhcq.mongodb.net/gzt-lab"
dbName = "Historical"
collName = "data-history"

norm_factor = 40

x = []
yc = []
yd = []

print("\n-----------------------------------------------\n"+
"Gazstao DataCrunch v1.0 2021-04-17 14h27\nRodando em: "+
"{}\n-----------------------------------------------".format(datetime.datetime.now()))


#
#       Testa conexão ao Mongo e lista Bancos de Dados e Collections
#

def testaMongo(myclient):

    encontrado = False
    for eachDB in myclient.list_database_names():
        mydb = myclient[eachDB]

        for item in mydb.list_collection_names():
            #print("\t\t{}.{}".format(eachDB,item))
            if ( (eachDB == dbName) and (item == collName)):
                encontrado = True
    if (encontrado):
        print("Banco de Dados {}.{} encontrado.".format(dbName, collName))
        return True
    else:
        print("Banco de Dados {}.{} não foi encontrado e será criado.".format(dbName, collName))
        return False


#
#       ConectaMongo = MongoDB Conection
#

def conectaMongoDB(connectionString):

    try:
        myclient = pymongo.MongoClient(connectionString)
        print("Conectando :{}".format(connectionString))
        return myclient

    except:
        print("Erro: {}".format(sys.exc_info()[0]))


#
#   EL PROGRAMO
#

try:
    clienteMongoDB = conectaMongoDB(conStr)
    testaMongo(clienteMongoDB)

except:
    print("Erro: {}".format(sys.exc_info()[0]))
    sys.exit()

db = clienteMongoDB[dbName]
coll = db[collName]

repeat = True
while repeat:

    local = input ("Que local? ")
    if (local == "exit"):
         repeat = False
         sys.exit()

    for registro in coll.find( { "location" : local , "newdeaths" : {"$ne" : "'"}}).sort("date", 1):

        novos_casos = registro["new_cases_smoothed"]
        novas_mortes = registro["new_deaths_smoothed"]
        pprint.pprint("{} - {} : Novos casos: {}              Novas mortes: {}".format(registro["location"], registro["date"], novos_casos, registro["new_deaths"]))

        if (novos_casos != ""):
            x.append(registro["date"])
            yc.append(novos_casos)
            yd.append(novas_mortes*norm_factor)

            #plt.bar(x,yc,color="grey")
            #plt.bar(x,yd,color="red")

    print("Construindo o gráfico...")

    plt.plot(x,yc, color="black", linestyle="--", label = "Novos Casos")
    plt.plot(x,yd, color="red", linestyle="--" , label = "Novas Mortes * {}".format(norm_factor) )

    plt.legend()
    plt.title("Covid Evolution in {}".format(local))
    plt.xlabel("Data")
    plt.ylabel("Novos Casos vs Novas Mortes * {}".format(norm_factor))
    plt.savefig("Covid-Evolution-{}.png".format(local))
    plt.show()

print("")
