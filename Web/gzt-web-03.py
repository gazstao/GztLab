# Gzt-Web-01 2021-04-19 16h15

# Antes de começar a usar o programa é necessário carregar os dados para o mongodb
# Para isso, baixe o arquivo https://covid.ourworldindata.org/data/owid-covid-data.csv
# e importe para o MongoDB usando o comando:
# Para o MongoDB local: mongoimport --db NOME_DO_BANCO --collection NOME_DA_COLLECTION --file owid-covid-data.csv --type csv --headerline
# Para o MongoDB na nuvem: mongoimport mongodb+srv://USUARIO:SENHA@cluster0.uvhcq.mongodb.net/NOME_DO_BANCO --collection NOME_DA_COLLECTION --file owid-covid-data.csv --type csv --headerline
# Depois execute o programa e ele:

# - Pede a senha pra conectar no MongoDB
# - Procura pelo Banco de Dados
# - Procura pelos locais com dados disponíveis
# - Compila todos os dados do local
# - Cria gráficos automáticos para todos os países
# - Cria um arquivo Web com os links pros gráficos.

import os
import json
import pymongo
import sys
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

conStr = "mongodb://localhost:27017/"
#conStr = "mongodb+srv://owner:{}@cluster0.uvhcq.mongodb.net/"
dbName = "Data-Backup"
collName = "data20210422"
imageDirName = "Vaccionation-Graphs"
fileName = "Vaccination-Evolution-Graphic"

htmlStart = '<!DOCTYPE html><html lang="en" dir="ltr">\n<head><meta charset="utf-8"><link rel="shortcut icon"  type="image/x-icon" href="favicon.ico"><link rel="stylesheet" href="css/style.css"><title>Covid19 Vaccination Evolution by Country</title></head>\n<body><h1>Covid19 Vaccination Evolution by Country</h1><p><table><tr>\n'
htmlEnd = '</t></table></p><div class="bloco end">by Gazstao 2021<br></div></body></html>'
htmlMiddle = ''

norm_factor = 40

x = []
yc = []
yd = []
graphstyle = "solid"
contagem = 1

horaInicio = datetime.datetime.now()

print("\n-----------------------------------------------\n"+
"Gazstao DataVac v1.0 2021-04-20 12h51\nRodando em: "+
"{}\n-----------------------------------------------".format(horaInicio))

#senha = input("Qual a senha de conexão do Banco de Dados? ")


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
        horaInicio = datetime.datetime.now()
        return myclient

    except:
        print("Erro: {}".format(sys.exc_info()[0]))

#
#       MongoDB lista listaLocais
#

locaisDisponiveis = []
def listaLocais(collection):
    print("Locais com dados disponíveis:")
    for registro in collection.find().distinct("location"):
        print ("{} , ".format(registro), end=" ")
        locaisDisponiveis.append(registro)
    print (" iniciando compilação de dados.")

#
#   EL PROGRAMO
#

try:
    clienteMongoDB = conectaMongoDB(conStr)
    testaMongo(clienteMongoDB)

except:
    print("Erro: {}".format(sys.exc_info()[0]))
    sys.exit()

try:
    os.mkdir(imageDirName)
    print("Diretório de imagens: {} foi criado.".format(imageDirName))
except:
    print("Diretório de imagens: {} já existe.".format(imageDirName))

db = clienteMongoDB[dbName]
coll = db[collName]
listaLocais(coll)

print("\n{}".format(htmlStart))

for local in locaisDisponiveis:

    plt.rc('grid', linestyle=':', color="lightgrey")
    plt.grid()

    for registro in coll.find( { "location" : local , "newdeaths" : {"$ne" : "'"}}).sort("date", 1):

        novos_casos = registro["new_vaccinations_smoothed"]
        novas_mortes = registro["new_deaths_smoothed"]

        if (novos_casos != ""):
            x.append(registro["date"])
            yc.append(novos_casos)
            yd.append(novas_mortes*norm_factor)

    print("\n{} - Adicionando {} registros de {} - {} e construindo gráfico".format( contagem, len(x),registro["location"], registro["date"]))

    plt.plot(x,yc, color="black", label = "Novas vacinações por dia", linestyle = graphstyle, linewidth = 0.5)

    plt.xticks(np.arange(0,len(x)+1,30), rotation=30, fontsize="x-small")

    plt.legend()
    plt.title("Vaccination Evolution in {}".format(local))
    plt.xlabel("Data")
    plt.ylabel("Novas Vacinacoes")
    nomeArq = "{}-{}-{}.png".format(fileName, registro["date"], local)
    nomeArqRed = "{}-{}-{}-Small.png".format(fileName, registro["date"], local)

    if (len(x) > 1):
        htmlNovo='<th><a href="{}/{}" target="_blank"><figure><img src="{}/{}"><figcaption>{}-{}</figcaption></figure></a></th>\n'.format(imageDirName, nomeArq, imageDirName,nomeArqRed, local, registro["date"])
        htmlMiddle = htmlMiddle+htmlNovo
        plt.savefig("{}/{}".format(imageDirName, nomeArqRed), dpi=50)
        print(htmlNovo)
        plt.savefig("{}/{}".format(imageDirName, nomeArq), dpi=200)
        if ( (contagem%3)==0 ):
            htmlNovo = "</tr><tr>"
            htmlMiddle = htmlMiddle+htmlNovo
        contagem += 1

    else:
        print("Figura {}/{} não foi salva por falta de dados.".format(imageDirName, nomeArq))
    x.append(0)
    yc.append(0)
    yd.append(0)
    plt.close()
    plt.clf()
    x.clear()
    yc.clear()
    yd.clear()

horaFinal = datetime.datetime.now()

htmlFile = open("./indexvacc.html", "w")
htmlFile.write(htmlStart)
htmlFile.write(htmlMiddle)
htmlFile.write(htmlEnd)
htmlFile.close()

print(htmlEnd)

print("Hora inicio: \t{}".format(horaInicio))
print("Hora final: \t{}".format(horaFinal))
