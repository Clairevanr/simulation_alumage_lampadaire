"""Permet de genrer une "interface" dans le terminale pour simplifier l'utilisation de l'ensemble des fonctions qui permet d'effectuer la simulation
"""
from Code.graph import *
from Code.graph_comparaison import *
from Code.graph_save import *
import os

def F():
    print(" ___                               _\n| _ \ __ _  _ _  __ _  _ __   ___ | |_  _ _  __ _  __ _  ___\n|  _// _` || '_|/ _` || '  \ / -_)|  _|| '_|/ _` |/ _` |/ -_)\n|_|  \__,_||_|  \__,_||_|_|_|\___| \__||_|  \__,_|\__, |\___|\n                                                  |___/")

def lecture(a:str)->tuple:
    """Convertie un str `A/B` en `(a,b)`

    Parametres
    ----------
    a : str
        le str sous dorme `a/b`

    Renvoies
    -------
    tuple
        `(int(a), int(b))`
    """
    rep1 = ""
    rep2 = ""
    b = False
    for i in a:
        if i != "/" and b == False :
            rep1 += i
        elif i != "/" and b == True :
            rep2 += i
        elif i == "/":
            b = True
    return (int(rep1), int(rep2))
    
print(" ___  _               _        _    _                 _           _             _                                   _           _____  ___  ___  ___\n/ __|(_) _ __   _  _ | | __ _ | |_ (_) ___  _ _    __| | ___   __| | ___  _ __ | | __ _  __  ___  _ __   ___  _ _  | |_   ___  |_   _||_ _|| _ \| __|\n\__ \| || '  \ | || || |/ _` ||  _|| |/ _ \| ' \  / _` |/ -_) / _` |/ -_)| '_ \| |/ _` |/ _|/ -_)| '  \ / -_)| ' \ |  _| |___|   | |   | | |  _/| _|\n|___/|_||_|_|_| \_,_||_|\__,_| \__||_|\___/|_||_| \__,_|\___| \__,_|\___|| .__/|_|\__,_|\__|\___||_|_|_|\___||_||_| \__|         |_|  |___||_|  |___|\n                                                                         |_|")
graphe_type = int(input("Quel type de graphique vous voulez : \n 1. Normale \n 2. Double \n 3. A partir d'une sauvegarde \n>>> "))

os.system('cls' if os.name == 'nt' else 'clear')
F()
if graphe_type == 1 :
    puissance = int(input("Puissance (en W) = "))
    if puissance == 0 :
        raise ValueError("La puissance ne peut pas être égale a 0")
    cst_tps = int(input("Constante de temps (en s) = "))
    iteration = int(input("Nombre de simulation = "))
    if iteration < 2 :
        raise ValueError("Le nombre de simulation est bien trop bas (min = 2)")
    tps_simulation = int(input("Temps de la simulation (en h) = "))
    if tps_simulation == 0 :
        raise ValueError("Le temps de simulation ne peut pas être égale a 0")
    nbr_utilisateur = int(input("Nombre d'utilisateur = "))
    os.system('cls' if os.name == 'nt' else 'clear')
    F()
    arret = input("Activer la fonction d'arret des utilisateur devant les lampadaires ? (o|n)\n>>> ")
    if arret == "o" or arret == "oui" :
        os.system('cls' if os.name == 'nt' else 'clear')
        F()
        proba = input("Probabiliter d'arret de l'utilisateur (ex: 1/10) = ")
        A = lecture(proba)
        proba = [A[0], A[1], True]
    else :
        proba = [1, 10, False]
    os.system('cls' if os.name == 'nt' else 'clear')
    F()
    save = input("Activer la sauvegarde ? (o|n) \n>>> ")
    if save == "o" or save == "oui" :
        save = True
    else :
        save = False
    os.system('cls' if os.name == 'nt' else 'clear')
    graphe1(iteration, tps_simulation, cst_tps, puissance, nbr_utilisateur, 1, 0, 1, proba, save)

elif graphe_type == 2 :
    puissance = int(input("Puissance (en W) = "))
    if puissance == 0 :
        raise ValueError("La puissance ne peut pas être égale a 0")
    cst_tps = int(input("Constante de temps (en s) = "))
    iteration = int(input("Nombre de simulation = "))
    if iteration < 2 :
        raise ValueError("Le nombre de simulation est bien trop bas (min = 2)")
    tps_simulation = int(input("Temps de la simulation (en h) = "))
    if tps_simulation == 0 :
        raise ValueError("Le temps de simulation ne peut pas être égale a 0")
    nbr_utilisateur = int(input("Nombre d'utilisateur = "))
    os.system('cls' if os.name == 'nt' else 'clear')
    F()
    Type = int(input("Type de trajet : \n 1. Aléatoire \n 2. Deplacement en continue (saturation) \n 3. Avec minimum de deplacmement \n>>> "))
    os.system('cls' if os.name == 'nt' else 'clear')
    F()
    if Type == 3 :
        nbr_allumage = int(input("Nombre min de deplacmement = "))
    else :
        nbr_allumage = 0
    os.system('cls' if os.name == 'nt' else 'clear')
    F()
    arret = input("Activer la fonction d'arret des utilisateur devant les lampadaires ? (o|n)\n>>> ")
    if arret == "o" or arret == "oui" :
        os.system('cls' if os.name == 'nt' else 'clear')
        F()
        proba = input("Probabiliter d'arret de l'utilisateur (ex: 1/10) = ")
        A = lecture(proba)
        proba = [A[0], A[1], True]
    else :
        proba = [1, 10, False]

    os.system('cls' if os.name == 'nt' else 'clear')
    graphe2(iteration, tps_simulation, cst_tps, puissance, nbr_utilisateur, Type, nbr_allumage, proba)

elif graphe_type == 3:
    filepath = input("Chemin vers le fichier de sauvegarde (par default = './Donnees/save.json') : \n>>> ")
    os.system('cls' if os.name == 'nt' else 'clear')
    graph_save(filepath)
