"""Permet e génerer un graphique a partir d'une simmulation
"""
from Code.simul import *
from matplotlib import pyplot
import numpy as np
import os

def graphe1(nbr_simulation:int, tps_simulation:int, cst_tps:int, puissance:int, nbr_utilisateur:int, type:int = 1, nbr_allumage:int = 0, fonction:int = 1, prob:list = [1, 10, True], save:bool = False)->None:
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
    fonction : int
        la fonction a utiliser pour la simulation du trajet. 1-trajet() | 2-trajet_voisin(), par default trajet()
    prob : list
        probabiliter que l'utilisateur fasse un arret (devant un lampadaire) ou on aura [ numérateur, denminominateur, activer ou non], par default [1, 10, True]
    save : bool
        si on sauvegarde ou non les données ?, par defaut non

    Renvoies
    -------
    None
        effectue une simulation et genere un graphique
    """
    
    val = simulation(nbr_simulation, tps_simulation, cst_tps, puissance, nbr_utilisateur, type, nbr_allumage, fonction, prob, save)
    val_opti = [ i[0] for i in val["sim"] ]

    born_min = min(val_opti) - 5
    born_max = max(val_opti) + 5

    # méthode montecarlo
    uopti = (1/(nbr_simulation-1)*sum((np.array(val_opti)-val["moy"][0])**2.))**0.5
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(" ___                 _  _          _\n| _ \ ___  ___ _  _ | || |_  __ _ | |_  ___\n|   // -_)(_-<| || || ||  _|/ _` ||  _|(_-<\n|_|_\\\___|/__/ \_,_||_| \__|\__,_| \__|/__/\n")

    print("Valeur moyenne : \n")
    print(" - Optimiser : " + str(val["moy"][0]) + "wh")
    print(" - Normale : " + str(val["moy"][1]) + "wh \n")
    print("u(consomation optimiser) = " + str(uopti) + "\n")
    print("Ecart : " + str(((abs(val["moy"][0] - val["moy"][1]) / val["moy"][1]) * 100)) + "%\n")
    print("Temps : \n")
    print(" - Temps totale : " + str(val["tps_tot"]) + "s")
    print("\n")
    ##################################################################################################################
    pyplot.hist(val_opti, range = (born_min, born_max), bins = 200, color = 'blue', edgecolor = 'black')
    pyplot.xlabel('consomation (en wh)')
    pyplot.ylabel('effectif')
    pyplot.title('Pour ' + str(len(val_opti)) + ' iterations - Consomation optimisé')
    pyplot.title('Pour ' + str(len(val_opti)) + ' iterations - Consomation optimisé')
    pyplot.show()
