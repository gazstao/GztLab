# gazstao 2021-04-12 10h
# Carrega dados JSON obtidos do arquivo para o MongoDB e mostra
# https://github.com/owid/covid-19-data/tree/master/public/data

import json
import pymongo
import sys

dbName = "gztlab"
collName = "data20210414"
arquivo = "/Users/gazstao/github/covid-19-data/public/data/latest/owid-covid-latest.json"

print("\n\n\n\n\n\n\nGazstao DataParserExperiment v0.05 2021-04-15 8h59")


#
#       Leitura do arquivo e criação de objeto JSON
#

def file2data(arquivo):

    print("\nArquivo {} carregado com sucesso!".format(arquivo))

    with open(arquivo) as file:
        dados = file.read()
        objJSON = json.loads(dados)
        return objJSON


#
#     Lista dados
#

def listaDados(listaJSON):
    listaDados = []
    for item in listaJSON:
        listaDados.append(listaJSON[item])
        print("{}){}".format(item, listaJSON[item]["location"]), end="\t\t\t\t")
        if (len(listaDados)%3 == 0):
            print("")
    print ("A lista tem {} itens.".format(len(listaDados)))


#
#       Função insere dados
#

def insereDados(listaJSON, dbConn):
    for item in listaJSON:
        print(json.dumps(item),end=" ")
        # print(json.dumps(objJSON[item], indent = 4, sort_keys = True))
        objID = dbConn.insert_one(listaJSON[item]).inserted_id
        print("Objeto {} inserido com sucesso.".format(objID))

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

try:

    conStr = "mongodb://localhost:27017/"
    myclient = pymongo.MongoClient(conStr)
    print("\nConectado :{}".format(conStr))
    testaMongo(myclient)

except:

    print("Erro: {}".format(sys.exc_info()[0]))


#
#   EL PROGRAMO
#

prodDB = myclient[dbName]
prodCollection = prodDB[collName]

dadosJSON = file2data(arquivo)

resposta = input ("\nDeseja carregar os dados para o Banco de Dados?\t")
if (resposta == "y" or resposta == "Y"):
    print("Carregando dados para {}".format(prodCollection))
    insereDados(dadosJSON, prodCollection)
else:
    print("Passando...")

resposta = input ("\nDeseja visualizar os dados?\t")
if (resposta == "y" or resposta == "Y"):
    repete = True
    listaDados(dadosJSON)
else:
    print("Passando...")
    repete = False

while repete:
    item = input ("\nDeseja ver quais informações? ")
    if (item == "exit"):
        repete = False
    else:
        if (item == "" or item == "?"):
            listaDados(dadosJSON)
            print("Digite exit para sair")
        else:
            try:
                print(json.dumps(dadosJSON[item], indent = 4, sort_keys = True))
            except:
                print("Não foi possível carregar os dados.")

print("")
