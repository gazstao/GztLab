import json
import pymongo
import sys
import datetime
import pprint
import matplotlib.pyplot as plt

#conStr = "mongodb://localhost:27017/"
conStr = "mongodb+srv://owner:{}@cluster0.uvhcq.mongodb.net/"
dbName = "Data-Backup"
collName = "data20210418"

norm_factor = 40

x = []
yc = []
yd = []
graphstyle = "solid"

print("\n-----------------------------------------------\n"+
"Gazstao DataCrunch v2.0 2021-04-18 16h01\nRodando em: "+
"{}\n-----------------------------------------------".format(datetime.datetime.now()))

senha = input("Qual a senha de conexão do Banco de Dados? ")

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
        myclient = pymongo.MongoClient(connectionString.format(senha))
        print("Conectando :{}".format(connectionString))
        return myclient

    except:
        print("Erro: {}".format(sys.exc_info()[0]))

#
#       MongoDB lista listaLocais
#

locaisDisponiveis = []
def listaLocais(collection):
    print("------------  Locais disponíveis --------------")
    for registro in collection.find({}).distinct("location"):
        print ("{} , ".format(registro), end=" ")
        locaisDisponiveis.append(registro)
    print ("digite exit para sair, clear para limpar o gráfico.")

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
listaLocais(coll)

repeat = True
while repeat:

    local = input ("Que local? ")
    if (local == "exit"):
         repeat = False
         sys.exit()

    elif (local == "?" or local==""):
        listaLocais(coll)

    elif (local == "clear"):
        plt.close()
        plt.clf()
        x.clear()
        yc.clear()
        yd.clear()
        print("Cleared")

    elif (local in locaisDisponiveis):

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

        print("Construindo o gráfico... Aguardando que a janela seja fechada.")

        plt.plot(x,yc, color="blue", label = "Novos Casos", linestyle = graphstyle, linewidth = 1.0)
        plt.plot(x,yd, color="green" , label = "Novas Mortes * {}".format(norm_factor), linestyle = graphstyle, linewidth = 1.0 )

        plt.legend()
        plt.title("Covid Evolution in {}".format(local))
        plt.xlabel("Data")
        plt.ylabel("Novos Casos vs Novas Mortes * {}".format(norm_factor))
        plt.savefig("Covid-Evolution-{}-{}.png".format(collName, local))
        plt.show()
        x.append(0)
        yc.append(0)
        yd.append(0)

    else:
        print ("Local indisponível ou não foi possível obter os dados.")

print("")
