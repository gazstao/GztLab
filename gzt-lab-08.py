# gazstao 2021-04-15 19h27
# Objetivo: Carregar arquivo com histórico no Banco de Dados

import json
import pymongo
import sys

#conStr = "mongodb://localhost:27017/"
conStr = "mongodb+srv://owner:zer0@cluster0.uvhcq.mongodb.net/gzt-lab"
collName = "data"

print("\n\n\n\nGazstao DataParserExperiment v0.08 2021-04-15 19h27")


#
#       Testa conexão ao Mongo e lista Bancos de Dados e Collections
#

def testaMongo(myclient):

    for eachDB in myclient.list_database_names():
        mydb = myclient[eachDB]

        for item in mydb.list_collection_names():
            print("\t{}:{}".format(eachDB,item))

#
#       Mongo Conection
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
    cliente = conectaMongoDB(conStr)
    testaMongo(cliente)

except:
    print("Erro: {}".format(sys.exc_info()[0]))

print("")
