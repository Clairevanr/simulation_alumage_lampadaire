"""Permet de réaliser une graphique qui permet de tracer le graphique de la consomation en fonction du temps de simulation
"""
from simul import *
from matplotlib import pyplot
import os
import json

interalle = 1
tps_simulation_max = 24

###Parametre de simulation###
nbr_simulation = 100
tps_simulation = interalle
cst_tps = 0
puissance = 70
nbr_utilisateur = 100
type = 1
###Parametre de simulation###

X = [ i*interalle for i in range(1, round(tps_simulation_max/interalle) + 1) ]
Y = []
for i in range(1, round(tps_simulation_max/interalle) + 1) :
    os.system('cls' if os.name == 'nt' else 'clear')
    info = "temps de simulation : " + str(tps_simulation) + " | Etape : " + str(i) + "/" + str(round(tps_simulation_max/interalle)) + " | "
    Y.append(simulation(nbr_simulation, tps_simulation, cst_tps, puissance, nbr_utilisateur, proba=[1, 10, False], info_sup = info)["moy"][0])
    tps_simulation += interalle

with open('./Donnees/save_graphe4.json', 'w') as mon_fichier: # on créer le fichier voulue et on l'enregistre a l'endroit souhaité 
	json.dump({
     "axeX" : X,
     "axeY" : Y
     }, mon_fichier)

###
pyplot.plot(X, Y)
pyplot.xlabel('temps (en s)')
pyplot.ylabel('consomation (en Wh)')
pyplot.title('Cosomation en fonction du temps de simulation')
pyplot.show()