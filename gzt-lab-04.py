# gazstao 2021-04-12 20h37

import json
import pymongo


#
#       Leitura do arquivo e criação de objeto JSON
#

arquivo = "/Users/gazstao/github/covid-19-data/public/data/latest/owid-covid-latest.json"
print("\nGazstao DataParserExperiment 2021-04-12\nArquivo :"+arquivo)

with open(arquivo) as file:
    dados = file.read()

objeto = json.loads(dados)

def listaDados():
    listaDados = []
    for item in objeto:
        listaDados.append(objeto[item])
        print("{}){}".format(item, objeto[item]["location"]), end="\t\t\t\t")
        if (len(listaDados)%3 == 0):
            print("")
    print ("A lista tem {} itens.".format(len(listaDados)))

#    resposta = input ("Mostrar "+item+" ? ")
#    if (resposta == "y" or resposta == "Y"):
#         print(json.dumps(objeto[item], indent = 4, sort_keys = True))

listaDados()

repete = True
while repete:
    numItem = input ("\nDeseja ver qual informações? ")
    if (numItem == "exit"):
        repete = False
    else:
        if (numItem == "?"):
            listaDados()
        else:
            print(json.dumps(objeto[numItem], indent = 4, sort_keys = True))
