# gazstao DataExperiment1 2021-04-11 17h33

import json
arquivo = "/Users/gazstao/github/covid-19-data/public/data/latest/owid-covid-latest.json"

print("##########################################\nGazstao Data Parser (c) 2021-04-11")
print("Informacoes sobre o coronavirus carregadas do arquivo:\n"+arquivo+".\n##########################################\n")

with open(arquivo) as file:
    data = file.read()

json_obj = json.loads(data)

def printe(texto, valor):
    try:
        print(texto+": {:,}".format(valor))
    except:
        print(texto+": {}".format(valor))

def printp(texto, valor):
    try:
        print(texto+": {:.2f} %".format(valor))
    except:
        print(texto+": {}".format(valor))

def show(location):
    json_world = json_obj[location]
    json_world_date = json_world["last_updated_date"]
    json_location = json_world["location"]
    print ("\nReference date: " + json_world_date)
    print ("Location: "+json_location)

    json_world_population = json_world["population"]
    json_world_medianage = json_world["median_age"]
    json_world_age65older = json_world["aged_65_older"]
    json_world_age70older = json_world["aged_70_older"]
    json_world_lifeexpectancy = json_world["life_expectancy"]

    printe ("\nPopulation",json_world_population)
    printe ("Median Age",json_world_medianage)
    printp ("Age 65 and older",json_world_age65older)
    printp ("Age 70 and older",json_world_age70older)
    printe ("Life Expectancy",json_world_lifeexpectancy)

    json_world_totalcases = json_world["total_cases"]
    json_world_totaldeaths = json_world["total_deaths"]
    json_world_totalvaccinations = json_world["total_vaccinations"]
    json_world_peoplevaccinated = json_world["people_vaccinated"]
    json_world_peoplefullyvacinated = json_world["people_fully_vaccinated"]
    json_world_totalcasespermillion = json_world["total_cases_per_million"]
    json_world_totaldeathspermillion = json_world["total_deaths_per_million"]

    printe ("\nTotal cases",json_world_totalcases)
    printe ("Total deaths",json_world_totaldeaths)
    printe ("Total vaccinations",json_world_totalvaccinations)
    printe ("People fully vaccinated",json_world_peoplefullyvacinated)
    printe ("People vaccinated",json_world_peoplevaccinated)
    printe ("Total cases per million",json_world_totalcasespermillion)
    printe ("Total deaths per million",json_world_totaldeathspermillion)

    json_world_newcases = json_world["new_cases"]
    json_world_newdeaths = json_world["new_deaths"]
    json_world_newvaccinations = json_world["new_vaccinations"]
    json_world_newcasespermillion = json_world["new_cases_per_million"]
    json_world_newdeatspermillion = json_world["new_deaths_per_million"]

    printe ("\nNew cases",json_world_newcases)
    printe ("New deaths",json_world_newdeaths)
    printe ("New vaccinations",json_world_newvaccinations)
    printe ("New cases per million",json_world_newcasespermillion)
    printe ("New new_deaths_per_million",json_world_newdeatspermillion)

#show("OWID_WRL")
repeat = 1;
skipped = ""
while repeat:
    local = input("\nLocal: ")
    if (local == "exit"):
        repeat = 0
    if (local == "all"):
        local = "OWID_WRL"
    for place in json_obj:
        if (place == local):
            show (place)
        else:
            skipped = skipped + " " + place
    if (local == "?"):
        print (skipped)


print("")
