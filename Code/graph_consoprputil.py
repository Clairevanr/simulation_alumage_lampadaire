"""Permet de réaliser une graphique qui permet de tracer le graphique de la consomation en fonction d'un nombre d'utilisateur
"""
from simul import *
from matplotlib import pyplot
import os
import json

interalle = 15
nombre_max = 230

###Parametre de simulation###
nbr_simulation = 100
tps_simulation = 1
cst_tps = 0
puissance = 70
nbr_utilisateur = interalle
type = 1
###Parametre de simulation###

X = [ i*interalle for i in range(1, round(nombre_max/interalle) + 1) ]
Y = []
for i in range(1, round(nombre_max/interalle) + 1) :
    os.system('cls' if os.name == 'nt' else 'clear')
    info = "Nombre d'utilisateur : " + str(nbr_utilisateur) + " | Etape : " + str(i) + "/" + str(round(nombre_max/interalle)) + " | "
    Y.append(simulation(nbr_simulation, tps_simulation, cst_tps, puissance, nbr_utilisateur, proba=[1, 10, False], info_sup = info)["moy"][0])
    nbr_utilisateur += interalle

with open('./Donnees/save_graphe3.json', 'w') as mon_fichier: # on créer le fichier voulue et on l'enregistre a l'endroit souhaité 
	json.dump({
     "axeX" : X,
     "axeY" : Y
     }, mon_fichier)

###
pyplot.plot(X, Y)
pyplot.xlabel('Nombre d\'utilisateur')
pyplot.ylabel('consomation (en Wh)')
pyplot.title('Cosomation en fonction du nombre d\'utilisateur')
pyplot.show()