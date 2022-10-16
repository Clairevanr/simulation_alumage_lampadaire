"""Permet a partir d'un ficher de sauvegarde `.json` de regénere le résulta de celle-ci
"""
import json
from matplotlib import pyplot
import numpy as np
import os

def graph_save(filepath:str = "./Donnees/save.json")->None:
    """Permet de génerer un graphique d'une simulation a partir d'une sauvegarde

    Parameters
    ----------
    filepath : str, optional
        le chemin ver la sauvegarde, by default "./Donnees/save.json"
    
    Returns
    -------
    None
    """
    with open(filepath) as json_carte:
        save = json.load(json_carte)

    iteration = save["parametre"]["nbr_simulation"]
    val = save
    val_opti = [ i[0] for i in save["rep_simulation"]["sim"] ]
    val_norm = [ i[1] for i in save["rep_simulation"]["sim"] ]

    born_min = min(val_opti) - 5
    born_max = max(val_opti) + 5

    # méthode montecarlo
    uopti = (1/(iteration-1)*sum((np.array(val_opti)-val["rep_simulation"]["moy"][0])**2.))**0.5
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(" ___                 _  _          _\n| _ \ ___  ___ _  _ | || |_  __ _ | |_  ___\n|   // -_)(_-<| || || ||  _|/ _` ||  _|(_-<\n|_|_\\\___|/__/ \_,_||_| \__|\__,_| \__|/__/\n")

    print("Valeur moyenne : \n")
    print(" - Optimiser : " + str(val["rep_simulation"]["moy"][0]) + "wh")
    print(" - Normale : " + str(val["rep_simulation"]["moy"][1]) + "wh \n")
    print("u(consomation optimiser) = " + str(uopti) + "\n")
    print("Ecart : " + str(((abs(val["rep_simulation"]["moy"][0] - val["rep_simulation"]["moy"][1]) / val["rep_simulation"]["moy"][1]) * 100)) + "%\n")
    print("Temps : \n")
    print(" - Temps totale : " + str(val["rep_simulation"]["tps_tot"]) + "s")
    print("\n")
    ##################################################################################################################
    pyplot.hist(val_opti, range = (born_min, born_max), bins = 200, color = 'blue', edgecolor = 'black')
    pyplot.xlabel('consomation (en wh)')
    pyplot.ylabel('effectif')
    pyplot.title('Pour ' + str(iteration) + ' iterations - Consomation optimisé')
    pyplot.show()