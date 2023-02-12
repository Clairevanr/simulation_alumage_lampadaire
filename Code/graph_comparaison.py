"""Permet de gener un graphqque double pour les 2 type de fonction de calcule de trajet afin de les compares 
"""
from Code.simul import *
from matplotlib import pyplot
import numpy as np
import os

def graphe2(nbr_simulation:int, tps_simulation:int, cst_tps:int, puissance:int, nbr_utilisateur:int, type:int = 1, nbr_allumage:int = 0, prob:list = [1, 10, True])->None:
    """Permet de simuler la consomation des lampadaires et de générer un graphique 

    Parametres
    ----------
    nbr_simulation : int
        la nombre de simulation a effectuer
    tps_simulation : int
        le temps de la simulation 
    temps : list
        liste des temsppossible qui peuvent etre prise par les utilisateurs
    cst_tps : int
        le temps d'allumage des lampadaires 
    puissance : int
        puissance des lamapdaires
    vitesse : list
        vitesse des utilisateur 
    nbr_utilisateur : int
        nombre d'utilisateur
    type : int
        type de deplacement : 1-deplacement noramale, 2-deplacemnt en saturation du réseau, 3-deplacement avec condition du nbr de deplacement (+ ou - le nombre demander), 4-deplacment normale etandu (avec min aleatoire), par default 1
    nbr_allumage : int
        nombre min de lampadaire a allumer (pris en compte qu'avec type = 3), par default 0
    prob : list
        probabiliter que l'utilisateur fasse un arret (devant un lampadaire) ou on aura [ numérateur, denminominateur, activer ou non], par default [1, 10, True]
        
    Renvoies
    -------
    None
        effectue une simulation et genere un graphique
    """
    
    val1 = simulation(nbr_simulation, tps_simulation, cst_tps, puissance, nbr_utilisateur, type, nbr_allumage, 1, prob)
    val_opti1 = [ i[0] for i in val1["sim"] ]

    born_min1 = min(val_opti1) - 5
    born_max1 = max(val_opti1) + 5

    # méthode montecarlo
    uopti1 = (1/(nbr_simulation-1)*sum((np.array(val_opti1)-val1["moy"][0])**2.))**0.5
    ##################################################################################################################

    val2 = simulation(nbr_simulation, tps_simulation, cst_tps, puissance, nbr_utilisateur, type, nbr_allumage, 2, prob)
    val_opti2 = [ i[0] for i in val2["sim"] ]

    born_min2 = min(val_opti2) - 5
    born_max2 = max(val_opti2) + 5

    # méthode montecarlo
    uopti2 = (1/(nbr_simulation-1)*sum((np.array(val_opti2)-val2["moy"][0])**2.))**0.5
    ##################################################################################################################

    os.system('cls' if os.name == 'nt' else 'clear')
    print(" ___                 _  _          _\n| _ \ ___  ___ _  _ | || |_  __ _ | |_  ___\n|   // -_)(_-<| || || ||  _|/ _` ||  _|(_-<\n|_|_\\\___|/__/ \_,_||_| \__|\__,_| \__|/__/\n")
    
    print("Valeur moyenne 1 : \n")
    print(" - Optimiser : " + str(val1["moy"][0]) + "wh")
    print(" - Normale : " + str(val1["moy"][1]) + "wh \n")
    print("u(consomation optimiser) = " + str(uopti1) + "\n")
    print("Ecart : " + str(((abs(val1["moy"][0] - val1["moy"][1]) / val1["moy"][1]) * 100)) + "%")
    print("\n")

    print("\n")
    print("Valeur moyenne 2 : \n")
    print(" - Optimiser : " + str(val2["moy"][0]) + "wh")
    print(" - Normale : " + str(val2["moy"][1]) + "wh \n")
    print("u(consomation optimiser) = " + str(uopti2) + "\n")
    print("Ecart : " + str(((abs(val2["moy"][0] - val2["moy"][1]) / val2["moy"][1]) * 100)) + "%")
    print("\n")
    ##################################################################################################################

    born_max = max(born_max1, born_max2)
    born_min = min(born_min1, born_min2)

    figure = pyplot.figure(figsize = (7, 7))
    pyplot.gcf().subplots_adjust(left = 0.1, bottom = 0.1, right = 0.9, top = 0.9, wspace = 0, hspace = 0.3)
    axes = figure.add_subplot(2, 1, 1)
    axes.set_xlabel('consomation (en wh)')
    axes.set_ylabel('effectif')
    axes.set_title('Consomation des lamapdaires par la méthode trajet() - Pour ' + str(len(val_opti1)) + ' iterations')
    axes.set_title('Consomation des lamapdaires par la méthode trajet() - Pour ' + str(len(val_opti1)) + ' iterations')
    axes.hist(val_opti1, range = (born_min, born_max), bins = 200, color = 'blue', edgecolor = 'black')
    axes = figure.add_subplot(2, 1, 2)
    axes.set_xlabel('consomation (en wh)')
    axes.set_ylabel('effectif')
    axes.set_title('Consomation des lamapdaires par la méthode trajet_voisins() - Pour ' + str(len(val_opti2)) + ' iterations')
    axes.set_title('Consomation des lamapdaires par la méthode trajet_voisins() - Pour ' + str(len(val_opti2)) + ' iterations')
    axes.hist(val_opti2, range = (born_min, born_max), bins = 200, color = 'red', edgecolor = 'black')
    pyplot.show()
