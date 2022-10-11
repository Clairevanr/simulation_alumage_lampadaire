from Code.graph import *
from Code.graph_comparaison import *
from Code.graph_save import *
import os

vitesse = [7.2, 54, 72, 90, 108] # en km/h
temps = [3, 1.6, 1.2, 0.96, 0.8] # en s1

def F():
    print(" ___                               _\n| _ \ __ _  _ _  __ _  _ __   ___ | |_  _ _  __ _  __ _  ___\n|  _// _` || '_|/ _` || '  \ / -_)|  _|| '_|/ _` |/ _` |/ -_)\n|_|  \__,_||_|  \__,_||_|_|_|\___| \__||_|  \__,_|\__, |\___|\n                                                  |___/")

print(" ___  _               _        _    _                 _           _             _                                   _           _____  ___  ___  ___\n/ __|(_) _ __   _  _ | | __ _ | |_ (_) ___  _ _    __| | ___   __| | ___  _ __ | | __ _  __  ___  _ __   ___  _ _  | |_   ___  |_   _||_ _|| _ \| __|\n\__ \| || '  \ | || || |/ _` ||  _|| |/ _ \| ' \  / _` |/ -_) / _` |/ -_)| '_ \| |/ _` |/ _|/ -_)| '  \ / -_)| ' \ |  _| |___|   | |   | | |  _/| _|\n|___/|_||_|_|_| \_,_||_|\__,_| \__||_|\___/|_||_| \__,_|\___| \__,_|\___|| .__/|_|\__,_|\__|\___||_|_|_|\___||_||_| \__|         |_|  |___||_|  |___|\n                                                                         |_|")
graphe_type = int(input("Quel type de graphique vous voulez : \n 1. Normale \n 2. Double \n 3. A partir d'une sauvegarde \n>>> "))
os.system('cls' if os.name == 'nt' else 'clear')
F()
if graphe_type == 1 :
    puissance = int(input("Puissance = "))
    cst_tps = int(input("Constante de temps = "))
    iteration = int(input("Nombre de simulation = "))
    tps_simulation = int(input("Temps de la simulation = "))
    nbr_utilisateur = int(input("Nombre d'utilisateur = "))
    os.system('cls' if os.name == 'nt' else 'clear')
    F()
    fonction = int(input("Methode de calcule du trajet : \n 1. Logique \n 2. Chaotique \n>>> "))
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
    save = bool(input("Activer la sauvegarde ? (True ou False) \n>>> "))
    os.system('cls' if os.name == 'nt' else 'clear')
    graphe1(iteration, tps_simulation, temps, cst_tps, puissance, vitesse, nbr_utilisateur, Type, nbr_allumage, fonction, save)

elif graphe_type == 2 : 
    puissance = int(input("Puissance = "))
    cst_tps = int(input("Constante de temps = "))
    iteration = int(input("Nombre de simulation = "))
    tps_simulation = int(input("Temps de la simulation = "))
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
    graphe2(iteration, tps_simulation, temps, cst_tps, puissance, vitesse, nbr_utilisateur, Type, nbr_allumage)

elif graphe_type == 3:
    filepath = input("Chemin vers le fichier de sauvegarde (par default = './Donnees/save.json') : \n>>> ")
    os.system('cls' if os.name == 'nt' else 'clear')
    graph_save(filepath)