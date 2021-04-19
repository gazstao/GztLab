# Gzt-Web-01 2021-04-19 16h15
# - Pede a senha pra conectar no MongoDB
# - Procura pelo Banco de Dados
# - Procura pelos locais com dados disponíveis
# - Compila todos os dados do local
# - Criar gráficos automáticos para todos os países

# Desafios:
# - Criar um arquivo Web com os links pros gráficos.

import os
import json
import pymongo
import sys
import datetime
import matplotlib.pyplot as plt

conStr = "mongodb://localhost:27017/"
#conStr = "mongodb+srv://owner:{}@cluster0.uvhcq.mongodb.net/"
dbName = "Data-Backup"
collName = "data20210419"
imageDirName = "Covid19-Graphs"
fileName = "Covid19-Evolution-Graphic"
horaInicio = datetime.datetime.now()

htmlStart = '<!DOCTYPE html><html lang="en" dir="ltr"><head><meta charset="utf-8"><link rel="stylesheet" href="css/style.css"><title>Covid-19 Evolution by Country</title></head><body><h1>Covid-19 Evolution by Country</h1><p>Atualizado em {}</p><br><ul>'.format(horaInicio)
htmlEnd = '</ul><div class="bloco end">by Gazstao 2021<br>Dados retirados do projeto <a href="https://github.com/owid/covid-19-data/">Owid</a></div></body></html>'
htmlMiddle = ''

norm_factor = 40

x = []
yc = []
yd = []
graphstyle = "solid"
contagem = 1

print("\n-----------------------------------------------\n"+
"Gazstao DataCrunch v2.0 2021-04-18 21h45\nRodando em: "+
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
    print("------------  Locais disponíveis --------------")
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

print("\nCriando arquivo html e gráficos...\n")
print(htmlStart)
for local in locaisDisponiveis:

    for registro in coll.find( { "location" : local , "newdeaths" : {"$ne" : "'"}}).sort("date", 1):

        novos_casos = registro["new_cases_smoothed"]
        novas_mortes = registro["new_deaths_smoothed"]

        if (novos_casos != ""):
            x.append(registro["date"])
            yc.append(novos_casos)
            yd.append(novas_mortes*norm_factor)

    print("\n{} - Adicionando {} registros de {} - {}, construindo gráfico e adicionando html.".format( contagem, len(x),registro["location"], registro["date"]))

    plt.plot(x,yc, color="blue", label = "Novos Casos", linestyle = graphstyle, linewidth = 0.5)
    plt.plot(x,yd, color="green" , label = "Novas Mortes * {}".format(norm_factor), linestyle = graphstyle, linewidth = 0.5 )

    plt.legend()
    plt.title("Covid Evolution in {}".format(local))
    plt.xlabel("Data")
    plt.ylabel("Novos Casos vs Novas Mortes * {}".format(norm_factor))
    if (len(x) > 1):
        nomeArq = "{}-{}-{}.png".format(fileName, registro["date"], local)
        novoHtml = '<li><a href="{}/{}">{}</a></li>'.format(imageDirName, nomeArq, local)
        htmlMiddle = htmlMiddle+novoHtml
        print(novoHtml)
        plt.savefig("./{}/{}".format(imageDirName, nomeArq), dpi=200)
        contagem += 1
    else:
        print("Figura .{}/{} não foi salva por falta de dados.".format(imageDirName, nomeArq))
    x.append(0)
    yc.append(0)
    yd.append(0)
    plt.close()
    plt.clf()
    x.clear()
    yc.clear()
    yd.clear()
print(htmlEnd)
horaFinal = datetime.datetime.now()

htmlFile = open("./index.html", "w")
htmlFile.write(htmlStart)
htmlFile.write(htmlMiddle)
htmlFile.write(htmlEnd)
htmlFile.close()

print("Hora inicio: \t{}".format(horaInicio))
print("Hora final: \t{}".format(horaFinal))
