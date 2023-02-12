"""Permet de simuler le déplacement aléatoire d'utilisateur au seins d'une `carte` afin de déterminer la consomation de ces utilisateur en fonction de leur déplacament (allumage de lampadaire)
"""
import json
import os
from time import perf_counter
from random import * 
from random import * 
from threading import Thread
import sys

with open('./Donnees/carte.json') as json_carte:
    carte = json.load(json_carte)
    
Data = { i : {"nb_allumage" : 0, "tps_allumage" : 0} for i in range(len(carte)) } # initialisations de la liste des données 
start = [ i for i in carte if carte[i]["entree/sortie"] == True ]
lien_sens = {
    "N" : ["NO", "NE"],
    "S" : ["SO", "SE"],
    "O" : ["NO", "SO"],
    "E" : ["NE", "SE"],
    "NO" : ["O", "N"],
    "NE" : ["N", "E"],
    "SO" : ["S", "O"],
    "SE" : ["S", "E"]
}
ecart_lampadaire = 20 #en m
lien_sens = {
    "N" : ["NO", "NE"],
    "S" : ["SO", "SE"],
    "O" : ["NO", "SO"],
    "E" : ["NE", "SE"],
    "NO" : ["O", "N"],
    "NE" : ["N", "E"],
    "SO" : ["S", "O"],
    "SE" : ["S", "E"]
}
ecart_lampadaire = 20 #en m

chg = " ___  _               _        _    _\n/ __|(_) _ __   _  _ | | __ _ | |_ (_) ___  _ _\n\__ \| || '  \ | || || |/ _` ||  _|| |/ _ \| ' \  _  _  _\n|___/|_||_|_|_| \_,_||_|\__,_| \__||_|\___/|_||_|(_)(_)(_)\n"

# on verifie qu'il n'y a pas d'erreur dans le fichier
err = []
for i in carte :
    for p in ["N", "S", "O", "E", "NO", "NE", "SO", "SE"] :
        for s in carte[i][p] : 
            R = s in carte[i]["voisins"] + [0]
            if R != True :
                err.append(i)
if len(err) != 0 :
    val_err = "|"
    for i in err :
        val_err += " " + i + " |"
    raise SyntaxError("Les données des points suivant sont mal édité : " + val_err)
# on verifie qu'il n'y a pas d'erreur dans le fichier

def time_adap(a:int)->str:
    """Permet de convertien un temps en second en fonction de sa valeur

    Parametres
    ----------
    a : int
        le temps en seconde

    Renvoies
    --------
    str
        le temps convertie
    """
    if a >= 86400 : #jours
        return str(round(a/86400)) + "j"
    if a >= 3600 : #heure
        return str(round(a/3600)) + "h"
    if a >= 60 : #min
        return str(round(a/60)) + "min"
    if a < 60 : #second
        return str(a) + "s"

def updt(total, progress, prefix:str = "Calculs en cours : ", dim:int = 40)->sys:
    """
    Displays or updates a console progress bar.

    Original source: https://stackoverflow.com/a/15860757/1391441
    """
    etat = progress
    fin = total
    barLength, status = dim, ""
    progress = float(progress) / float(total)
    if progress >= 1.:
        progress, status = 1, "\r\n"
    block = int(round(barLength * progress))
    text = "\r" + prefix + str(etat) + "/" + str(fin) + " " + "[{}] {:.0f}% {}".format(
        "#" * block + "." * (barLength - block), round(progress * 100, 0),
        status)
    sys.stdout.write(text)
    sys.stdout.flush()

def cal_vit_tps(intervale:list = [4, 130])->tuple:
    """Permet de generer une vitesse aleatoire suivant une intervalle et de l'associer a un temps d'allumage du lampdaire

    Parametres
    ----------
    intervale : list, optionnel 
        l'intervale suivant le quel on prendra les vitesse (en km/h), par defaut [4, 130]

    Renvoies
    --------
    tuple
        un tuple de la vitesse et du temps associer : `(vit, tps)`
    """
    vit = randint(intervale[0], intervale[1]) #en km/h
    tps = ecart_lampadaire / (vit/3.6) # en s
    return (vit, tps)

def trajet_voisin(tps_simulation:int, vitesse:float, type:int = 1, nbr_lampadaire:int = 0, prob:list = [1, 20, True])->list:
    """Permet de générer le trajet de façon aléatoire d'un utilisateur dans la ville (trajet absurde) \n
    On suppose un déplacement chaotique des utilisateurs (les utilisateur se deplace comme il veule sans logique)

    Parametres
    ----------
    tps_simulation : int
        le temps de la simulation
    vitesse : float
        la vitesse de l'utilisateur 
    type : int
        type de deplacement : 1-deplacement noramale, 2-deplacemnt en saturation du réseau, 3-deplacement avec condition du nbr de deplacement (+ ou - le nombre demander), 4-trajet aléaroire étandu avec aléatoir du min, par default 1
    nbr_lampadaire : int
        nombre min de lampadaire a allumer (pris en compte qu'avec type = 3), par default 0
    prob : list
        probabiliter que l'utilisateur fasse un arret (devant un lampadaire) ou on aura [ numérateur, denminominateur, activer ou non], par default [1, 10, True]
    
    Renvoies
    -------
    list
        liste de devant quel lampadaire passe chaque utilisateur
    """
    if prob[0] == prob[1] : # on evite les boucle infinie
        prob = [1, 20, prob[2]]
    begin = start[randint(0, len(start) - 1)]
    trajet = [begin]
    if carte[begin]["voisins"][0] == 0 : # on prend le point qui n'est pas 0 pour continue
        begin = str(carte[begin]["voisins"][1])
    else :
        begin = str(carte[begin]["voisins"][0])
    trajet.append(begin)
    mem = trajet[:]
    mem_begin = begin
    if type == 1 : # deplacement aléatoire
        trajet_tot = []
        while len(trajet) < 6 : # 6 et le trajet le plus cours pour sortir
            trajet = mem[:] # on reinitialise avec les valeur par default pour recommencer et on le refait jusqu'a avoir >= 6
            begin = mem_begin
            while 0 not in carte[begin]["voisins"]: # on parcoure la carte jusqu'a toruver un point d'arret 
                arret = randint(1, prob[1])
                if arret <= prob[0] and prob[2] == True :
                    trajet.append(begin)
                else :
                    begin = str(carte[begin]["voisins"][randint(0, len(carte[begin]["voisins"]) - 1)])
                    trajet.append(begin)
        trajet_tot = trajet[:]
    elif type == 2 : # deplacement en continue
         
        distance_max = vitesse * tps_simulation # on cacule la distance max que peut parcourire les utilisateur en fonction de leur temps impartie
        lampadaire_max = round(distance_max / 0.02) # on determine le nombre max de lampadaire q'il peuvent allumer en fonction de leur vitesse et du temps de l'expérimentation | on a des lampadaire espacer de 20m = 0,02km 
        trajet_tot = []
        while lampadaire_max - len(trajet_tot) > 0 : # on vaut un certain nombre deplacement
            mem = trajet[:]
            mem_begin = begin
            while len(trajet) < 6 : # 6 et le trajet le plus cours pour sortir
                trajet = mem[:] # on reinitialise avec les valeur par default pour recommencer et on le refait jusqu'a avoir >= 6
                begin = mem_begin
                while 0 not in carte[begin]["voisins"]: # on parcoure la carte jusqu'a toruver un point d'arret 
                    arret = randint(1, prob[1])
                    if arret <= prob[0] and prob[2] == True :
                        trajet.append(begin)
                    else :
                        begin = str(carte[begin]["voisins"][randint(0, len(carte[begin]["voisins"]) - 1)])
                        trajet.append(begin)
            
            trajet_tot += trajet # on ajoute le trajet au deplacement totale
            
            trajet = []
            if carte[begin]["voisins"][0] == 0 : # on prend le point qui n'est pas 0 pour continue
                begin = str(carte[begin]["voisins"][1])
            else :
                begin = str(carte[begin]["voisins"][0])
            trajet.append(begin)
    elif type == 3 : # deplacement avec condition
        
        trajet_tot = []
        while nbr_lampadaire - len(trajet_tot) > 0 : # on vaut un certain nombre deplacement
            mem = trajet[:]
            mem_begin = begin
            while len(trajet) < 6 : # 6 et le trajet le plus cours pour sortir
                trajet = mem[:] # on reinitialise avec les valeur par default pour recommencer et on le refait jusqu'a avoir >= 6
                begin = mem_begin
                while 0 not in carte[begin]["voisins"]: # on parcoure la carte jusqu'a toruver un point d'arret 
                    arret = randint(1, prob[1])
                    if arret <= prob[0] and prob[2] == True :
                        trajet.append(begin)
                    else :
                        begin = str(carte[begin]["voisins"][randint(0, len(carte[begin]["voisins"]) - 1)])
                        trajet.append(begin)
            
            trajet_tot += trajet # on ajoute le trajet au deplacement totale
            
            trajet = []
            if carte[begin]["voisins"][0] == 0 : # on prend le point qui n'est pas 0 pour continue
                begin = str(carte[begin]["voisins"][1])
            else :
                begin = str(carte[begin]["voisins"][0])
            trajet.append(begin)         
    elif type == 4 :
        distance_max = vitesse * tps_simulation # on cacule la distance max que peut parcourire les utilisateur en fonction de leur temps impartie
        lampadaire_max = abs(randint(6, round(distance_max / 0.02)) - (randint(6, round(distance_max / 0.02))))
        trajet_tot = []
        while lampadaire_max - len(trajet_tot) > 0 : # on vaut un certain nombre deplacement
            mem = trajet[:]
            mem_begin = begin
            while len(trajet) < 6 : # 6 et le trajet le plus cours pour sortir
                trajet = mem[:] # on reinitialise avec les valeur par default pour recommencer et on le refait jusqu'a avoir >= 6
                begin = mem_begin
                while 0 not in carte[begin]["voisins"]: # on parcoure la carte jusqu'a toruver un point d'arret 
                    arret = randint(1, prob[1])
                    if arret <= prob[0] and prob[2] == True :
                        trajet.append(begin)
                    else :
                        begin = str(carte[begin]["voisins"][randint(0, len(carte[begin]["voisins"]) - 1)])
                        trajet.append(begin)
            
            trajet_tot += trajet # on ajoute le trajet au deplacement totale
            
            trajet = []
            if carte[begin]["voisins"][0] == 0 : # on prend le point qui n'est pas 0 pour continue
                begin = str(carte[begin]["voisins"][1])
            else :
                begin = str(carte[begin]["voisins"][0])
            trajet.append(begin)
    return trajet_tot

def trajet(tps_simulation:int, vitesse:float, prob:list = [1, 20, True], int:tuple = (1, 5))->list:
    """Permet de simulter le deplacment d'un utilisateur suivant une direction

    Parametres
    ----------
    tps_simulation : int
        temps de la simulation
    vitesse : float
        vitesse de l'utilisateur 
    prob : list, optionnel 
        porbabiliter que l'utilisateur s'arret devant un lampadaire (1/10 => [1, 10, "si on active ou pas : bool"]), par defaut [1, 20, True]
    int : tuple, optionnel 
        le nombre de tentative pour réaliser la probabiliter ("de" , "à"), par defaut (1, 5)

    Renvoies
    --------
    list
        renvoie la liste des lampadaire a allumer
    """

    def next(A:str)->str:
        """Permet de donner le prochain lampadaire qui sera allumer

        Parametres
        ----------
        A : str
            le lampadaire ou on se trouve

        Renvoies
        -------
        str
            le prochain lampdaire
        """
        N = carte[A][orientation][randint(0, len(carte[A][orientation]) - 1)]
        if N == 0 :
            R = lien_sens[orientation][:]
            shuffle(R)
            for i in R :
                N = carte[A][i][randint(0, len(carte[A][i]) - 1)]
                if N != 0 :
                    return str(N)
            if N == 0 : 
                B = [ p for i in ["N", "S", "O", "E", "NO", "NE", "SO", "SE"] for p in carte[A][i] if p != 0]
                N = B[randint(0, len(B) - 1)]
                return str(N)
        else :
            return str(N)
    
    sens = ["N", "S", "O", "E", "NO", "NE", "SO", "SE"]
    orientation = sens[randint(0, len(start) - 1)]
    begin = start[randint(0, len(start) - 1)]
    trajet = [begin]
    begin = next(begin)
    trajet.append(begin)
    
    trajet_tot = []
    distance_max = vitesse * tps_simulation # on cacule la distance max que peut parcourire les utilisateur en fonction de leur temps impartie
    lampadaire_max = round(distance_max / 0.02)
    while lampadaire_max - len(trajet_tot) > 0 :
        while carte[begin]["entree/sortie"] == False :
            mem = begin
            i = 0
            while begin in trajet :
                begin = next(mem)
                i += 1
                if i >= 10 :
                    break
            trajet.append(begin)
            if prob[2] == True :
                for _ in range(randint(int[0], int[1])) :
                    arret = randint(1, prob[1])
                    if arret <= prob[0]:
                        trajet.append(begin)
        trajet_tot += trajet
        begin = start[randint(0, len(start) - 1)]
        trajet = [begin]
        begin = next(begin)
        trajet.append(begin)
        orientation = sens[randint(0, len(start) - 1)]
    return trajet_tot

import random
from typing import List, Tuple

map_data = carte 
link_directions = lien_sens
def simulate_trip(time: int, speed: float, prob: Tuple[int, int, bool] = (1, 20, True), attempts: Tuple[int, int] = (1, 5)) -> List[str]:
    """Simulates the movement of a user in a specific direction.

    Parameters
    ----------
    time : int
        The time of the simulation
    speed : float
        The speed of the user
    prob : Tuple[int, int, bool], optional
        The probability that the user stops in front of a street lamp (1/10 => [1, 10, "if we activate or not: bool"]), default [1, 20, True]
    attempts : Tuple[int, int], optional
        The number of attempts to make the probability ("from", "to"), default (1, 5)

    Returns
    -------
    List[str]
        Returns the list of street lamps to turn on
    """

    def get_next(current: str) -> str:
        """Gets the next street lamp that will be turned on

        Parameters
        ----------
        current : str
            The street lamp where we are currently located

        Returns
        -------
        str
            The next street lamp
        """
        next_lamp = map_data[current][orientation][random.randint(0, len(map_data[current][orientation]) - 1)]
        if next_lamp == 0:
            random.shuffle(link_directions[orientation])
            for i in link_directions[orientation]:
                next_lamp = map_data[current][i][random.randint(0, len(map_data[current][i]) - 1)]
                if next_lamp != 0:
                    return str(next_lamp)
            if next_lamp == 0:
                valid_options = [p for i in ["N", "S", "O", "E", "NO", "NE", "SO", "SE"] for p in map_data[current][i] if p != 0]
                next_lamp = valid_options[random.randint(0, len(valid_options) - 1)]
                return str(next_lamp)
        else:
            return str(next_lamp)
    
    directions = ["N", "S", "O", "E", "NO", "NE", "SO", "SE"]
    orientation = directions[random.randint(0, len(start) - 1)]
    current_lamp = start[random.randint(0, len(start) - 1)]
    trip = [current_lamp]
    current_lamp = get_next(current_lamp)
    trip.append(current_lamp)
    
    total_trip = []
    max_distance = speed * time 
    max_lamps = round(max_distance / 0.02)
    while max_lamps - len(total_trip) > 0:
        while not map_data[current_lamp]["entree/sortie"]:
            prev_lamp = current_lamp
            i = 0
            while current_lamp in trip:
                current_lamp = get_next(prev_lamp)
                i += 1
                if i >= 10:
                    break
            trip.append(current_lamp)
            if prob[2]:
                for _ in range(random.randint(attempts[0], attempts[1])):
                    stop = random.randint(1, prob[1])
                    if stop <= prob[0]:
                        trip.append(current_lamp)
        total_trip += trip
        current_lamp = start[random.randint(0, len(start) - 1)]
        trip = [current_lamp]
        current_lamp = get_next(current_lamp)
        trip.append(current_lamp)
        orientation = directions[random.randint(0, len(start) - 1)]
    return total_trip

import timeit

""" time_elapsed = timeit.timeit(lambda: simulate_trip(1, 30), number=1000)
print("Le temps d'exécution est de 1: ", time_elapsed)

time_elapsed = timeit.timeit(lambda: trajet(1, 30), number=1000)
print("Le temps d'exécution est de 2: ", time_elapsed)
 """
 
def adaptation(trajet:list, vitesse:float, tps_simulation:int)->list:
    """Permet de lier la vitesse de l'utilisateur a son deplacment ainsi qu'a sa vitesse, on cosidère une liste ou chaque element représente 0.5s

    Parametres
    ----------
    trajet : list
        la list du trajet de l'utilisateur
    vitesse : float
        la vitesse de l'utilisateur
    tps_simulation : int
        le temps de la simulation 

    Renvoies
    --------
    list
        list a vec les nouveau parametre pris en compte 

    Exceptions
    ----------
    ValueError
       3.6 <= vitesse <= 200 (en km/h), pour pouvoir réaliser le calcule
    """
    if vitesse < 3.6 :
        raise ValueError("La vitesse est bien trop petite pour réaliser le calcule (vitesse_min = 3.6km/h)")
    if vitesse > 200 :
        raise ValueError("La vitesse est bien trop élever pour réaliser le calcule (vitesse_max = 130km/h, la résolution des calcules limite la vitesse max)")
    A = [ 0 for _ in range(round((0.25 * tps_simulation) / 6.94444e-5)) ] # pas de 0.1s pour le niveau de precision on a donc une vitesse max de 130km/h | pour la formule il sagit d'un produit en croix
    V = round(ecart_lampadaire/((vitesse / 3.6) * 0.25)) # on a ici le nombre de point a parcourire avant d'allumer un lampadaire | on passe la vitesse pour 0.1s | pour la formule il sagit d'un produit en croix
    r = 0
    j = 0
    z = 0
    for i in range(len(A)) :
        r += 1
        if r == V :
            b = 0
            if j < len(trajet) :
                b = trajet[j]
                z = i
            A[i] += int(b)
            j += 1
            r = 0
    A = [ A[i] for i in range(len(A)) if i <= z ]
    return A
    
def deplacement(tps_simulation:int, nbr_utilisateur:int, type:int = 1, nbr_lampadaire:int = 0, fonction:int = 1, prob:list = [1, 10, True])->dict:
    """Permet de de simuler le deplacement simultane de plusieur utilisateu en meme temps sur un temps donner pour un nombre donné d'utilisateur

    Parametres
    ----------
    tps_simulation : int
        le temps de la simulation
    nbr_utilisateur : int
        le nombre d'utilisateur
    type : int
        type de deplacement : 1-deplacement noramale, 2-deplacemnt en saturation du réseau, 3-deplacement avec condition du nbr de deplacement (+ ou - le nombre demander), 4-deplavcement aleatoire etandu (avec min aleatoir), par default 1
    nbr_lampadaire : int
        nombre min de lampadaire a allumer (pris en compte qu'avec type = 3), par default 0
    fonction : int
        la fonction a utiliser pour la simulation du trajet. 1-trajet() | 2-trajet_voisin(), par default trajet()
    prob : list
        probabiliter que l'utilisateur fasse un arret (devant un lampadaire) ou on aura [ numérateur, denminominateur, activer ou non], par default [1, 10, True]

    Renvoies
    -------
    dict
        renvoie alors les trajet, les vitesses et le nombre de lampadaire allumable par les utilisateurs
    """
    Data_d = {}
    for i in range(nbr_utilisateur):
        vit_tps = cal_vit_tps()
        vitesse_utilisateur = vit_tps[0] # on choisie une vitesse aléatoire pour l'utilisateur
        if fonction == 1 : # on definie le type de trajet a prendre 
            trajet_utilisateur = adaptation(trajet(tps_simulation, vitesse_utilisateur, prob), vitesse_utilisateur, tps_simulation)
        elif fonction == 2 :
            trajet_utilisateur = adaptation(trajet_voisin(tps_simulation, vitesse_utilisateur, type, nbr_lampadaire, prob), vitesse_utilisateur, tps_simulation)
        distance_max = vitesse_utilisateur * tps_simulation # on cacule la distance max que peut parcourire les utilisateur en fonction de leur temps impartie
        lampadaire_max = round(distance_max / 0.02) # on determine le nombre max de lampadaire q'il peuvent allumer en fonction de leur vitesse et du temps de l'expérimentation | on a des lampadaire espacer de 20m = 0,02km 
        if len(trajet_utilisateur) > lampadaire_max : # si il y a trop de lampadaire allumer lors du trajet on en retire 
            trajetV2 = [ trajet_utilisateur[i] for i in range(lampadaire_max) ]
            trajet_utilisateur = trajetV2
        Data_d[i] = {
            "trajet" : trajet_utilisateur,
            "vitesse" : vitesse_utilisateur,
            "lampadaire_max" : lampadaire_max,
            "temps" : vit_tps[1]
        }
    
    return Data_d

def fusion(data:dict)->dict:
    """Permet de rendre tout les liste de la meme taille pour faciliter la comparaison

    Parametres
    ----------
    data : dict
        les données de déplacement de l'utilisateur (vien de la fonction deplacement)

    Renvoies
    -------
    dict
        la liste des déplacement uniformiser 
    """
    up = max([ len(data[i]["trajet"]) for i in data ]) # on prend l'utilisateur avec le plus de lampadaire d'alumer 
    data_harmo = { i : (data[i]["trajet"]) + [ 0 for _ in range(up - len(data[i]["trajet"])) ] if (len(data[i]["trajet"]) < up) else data[i]["trajet"] for i in data }
    return data_harmo

def deplacement_affectation(data:dict, data_deplacement:dict)->list:
    """Permet de renvoyer la liste d'allumage des lamapadaire en prenans en compte le fait qu'il peut y avaoir plusieur utilisateur au meme endroit au meme moment

    Parametres
    ----------
    data : dict
        la liste qui vien de fusion et qui va permettre de mettre tout ensemble
    data_deplacement : dict 
        dictionnaire des donner de déplaecemment des utilisateurs

    Renvoies
    -------
    list
        la liste avec le nombr d'allumage de chacun des utilisateur
    """
    lampdaire_list = [ [] for _ in range(len(carte) + 1)] # on compte pas le 0 donc o ajoute 1 (la liste d'utilisateur commence a 1 et se termine donc a n+1)
    calcule = [ lampdaire_list[int(data[p][i])].append(data_deplacement[p]["temps"]) for i in range(len(data[0])) for p in range(len(data)) if int(data[p][i]) != 0 and len(lampdaire_list[int(data[p][i])]) <= i]
    return lampdaire_list

def calcule(tps_simulation:int, puissance:int, cst_tps:int, data:list)->tuple:
    """Permet le calcule de la consomation

    Parametres
    ----------
    tps_simulation : int
        temps de la simulation
    puissance : int
        la puissance des lampadaires
    data : list
        les données du temps d'alumage des lamapdaires 

    Renvoies
    -------
    tuple
        (consomation optimiser , consomation classique)
    """
    simulation_classic = len(carte) # nombre de lampadaire 
    tps_opti = 0 # le temps totale lors de l'expérimentation optimiser 
    for i in data :
        tps = 0
        for p in i :
            tps += p + cst_tps
        if tps > tps_simulation * 3600 :
            tps = tps_simulation * 3600
        tps_opti += tps 
    conso_opti = ((tps_opti)/3600) * puissance # calcule de la puissance 
    conso_classic = (tps_simulation * simulation_classic) * puissance  
    return (round(conso_opti), round(conso_classic))

def f_save(data:dict, filepath = "./Donnees/save.json")->None:
    """Permet de sauvegarder les résultats de la simulation et c parametre dans un fichier 

    Parametres
    ----------
    data : dict
        les données a sauvegarder
    filepath : path, optional
        le chemin vers le fichier a sauvegarder, by default "save.json"
    """
    with open(filepath, 'w') as mon_fichier: # on créer le fichier voulue et on l'enregistre a l'endroit souhaité 
	    json.dump(data, mon_fichier)

def simulation(nbr_simulation:int, tps_simulation:int, cst_tps:int, puissance:int, nbr_utilisateur:int, type:int = 1, nbr_lampadaire:int = 0, fonction:int = 1, proba:list = [1, 10, True], save:bool = False, info_sup:str = "")->dict:
    """Permet de simuler la consomation des lampadaires

    Parametres
    ----------
    nbr_simulation : int
        la nombre de simulation a effectuer
    tps_simulation : int
        le temps de la simulation 
    cst_tps : int
        le temps d'allumage des lampadaires 
    puissance : int
        puissance des lamapdaires
    nbr_utilisateur : int
        nombre d'utilisateur
    type : int
        type de deplacement : 1-deplacement noramale, 2-deplacemnt en saturation du réseau, 3-deplacement avec condition du nbr de deplacement (+ ou - le nombre demander), 4-deplacment normale etandu (avec min aleatoire), par default 1
    nbr_lampadaire : int
        nombre min de lampadaire a allumer (pris en compte qu'avec type = 3), par default 0
    fonction : int
        la fonction a utiliser pour la simulation du trajet. 1-trajet() | 2-trajet_voisin(), par default trajet()
    prob : list
        probabiliter que l'utilisateur fasse un arret (devant un lampadaire) ou on aura [ numérateur, denminominateur, activer ou non], par default [1, 10, True]
    save : bool
        si on sauvegarde ou non les données ?, par defaut non
    info_sup : str
        les info supllémentaire sur la barre de chargement (/!\ ajouter " | " a la fin de votre info pour plus de lisibiliter), par defaut ""

    Renvoies
    -------
    dict
        renvoie alors la consomation moyenne otimiser et celle classique ainsi que tout les valeur de simmulation. ( { "sim" : [...], "moy" : (.., ..)} )
    """
        
    print(chg)
    simulation_L = []
    time_b = []
    updt(nbr_simulation, 0, info_sup + "Calcule : ")
    
    start = perf_counter()
    
    for i in range(nbr_simulation):
        start_in = perf_counter() # temps
        etape1 = deplacement(tps_simulation, nbr_utilisateur, type, nbr_lampadaire, fonction, proba)
        etape2 = fusion(etape1)
        etape3 = deplacement_affectation(etape2, etape1)
        etape4 = calcule(tps_simulation, puissance, cst_tps, etape3)
        simulation_L.append(etape4)
        end_in = perf_counter() # temps
        time_b.append(end_in - start_in) # temps calucle
        time_estim = round((sum(time_b)/len(time_b)) * (nbr_simulation - i))
        updt(nbr_simulation, i + 1, info_sup +  "Temps restant : " + time_adap(time_estim) + " | Calcule : ")
    
    end = perf_counter()
    
    print()
    optimiser_list = [ i[0] for i in simulation_L ] # on fait les moyenne 
    classic_list = [ i[1] for i in simulation_L ]
    moy_opti = sum(optimiser_list)/len(simulation_L)
    moy_classic = sum(classic_list)/len(simulation_L)
    
    rep = {
        "sim" : simulation_L,
        "moy" : (moy_opti, moy_classic),
        "tps_tot" : end - start,
    }
    
    if save == True :
        data = {"rep_simulation" : rep, "parametre" : {"nbr_simulation" : nbr_simulation, "tps_simulation" : tps_simulation, "cst_tps" : cst_tps, "puissance": puissance, "nbr_utilisateur": nbr_utilisateur, "type": type, "nbr_lampadaire": nbr_lampadaire, "fonction": fonction, "prob" : proba,  "save": save}}
        f_save(data) 
    return rep
