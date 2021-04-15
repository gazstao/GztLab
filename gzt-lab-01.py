# gazstao DataExperiment1 2021-04-11 17h33

import json
arquivo = "/Users/gazstao/github/covid-19-data/public/data/latest/owid-covid-latest.json"

print("##########################################\nGazstao Data Parser (c) 2021-04-11")
print("Informacoes sobre o coronavirus carregadas do arquivo:\n"+arquivo+".\n##########################################")

num_format = "{:,}".format

with open(arquivo) as file:
    data = file.read()

json_obj = json.loads(data)

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

    print ("\nPopulation: {:,}".format(json_world_population))
    print ("Median Age : {:,}".format(json_world_medianage))
    print ("Age 65 and older : {:,}".format(json_world_age65older))
    print ("Age 70 and older : {:,}".format(json_world_age70older))
    print ("Life Expectancy : {:,}".format(json_world_lifeexpectancy))

    json_world_totalcases = json_world["total_cases"]
    json_world_totaldeaths = json_world["total_deaths"]
    json_world_totalvaccinations = json_world["total_vaccinations"]
    json_world_peoplevaccinated = json_world["people_vaccinated"]
    json_world_peoplefullyvacinated = json_world["people_fully_vaccinated"]
    json_world_totalcasespermillion = json_world["total_cases_per_million"]
    json_world_totaldeathspermillion = json_world["total_deaths_per_million"]

    print ("Total cases: {:,}".format(json_world_totalcases))
    print ("Total deaths: {:,}".format(json_world_totaldeaths))
    print ("Total vaccinations: {:,}".format(json_world_totalvaccinations))
    print ("People fully vaccinated: {:,}".format(json_world_peoplefullyvacinated))
    print ("People vaccinated: {:,}".format(json_world_peoplevaccinated))
    print ("Total cases per million: {:,}".format(json_world_totalcasespermillion))
    print ("Total deaths per million: {:,}".format(json_world_totaldeathspermillion))

    json_world_newcases = json_world["new_cases"]
    json_world_newdeaths = json_world["new_deaths"]
    json_world_newvaccinations = json_world["new_vaccinations"]
    json_world_newcasespermillion = json_world["new_cases_per_million"]
    json_world_newdeatspermillion = json_world["new_deaths_per_million"]

    print ("\nNew cases: {:,}".format(json_world_newcases))
    print ("New deaths: {:,}".format(json_world_newdeaths))
    print ("New vaccinations: {:,}".format(json_world_newvaccinations))
    print ("New cases per million: {:,}".format(json_world_newcasespermillion))
    print ("New new_deaths_per_million: {:,}".format(json_world_newdeatspermillion))

show("OWID_WRL")
show("BRA")
show("IND")
show("USA")

# json_world_ = json_world[""]
# print ("\n xxxx : {:,}".format(json_world_))

print("")
