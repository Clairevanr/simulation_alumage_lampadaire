"""Permet de simuler le déplacement aléatoire d'utilisateur au seins d'une `carte` afin de déterminer al consomation de ces utilisateur en focntion de leur déplacament (allumage de lampadaire)
"""
from concurrent.futures import thread
import json
import os
import time
from random import randint 
from threading import Thread
import sys

with open('./Donnees/carte.json') as json_carte:
    carte = json.load(json_carte)
    
Data = { i : {"nb_allumage" : 0, "tps_allumage" : 0} for i in range(len(carte)) } # initialisations de la liste des données 
start = [ i for i in carte if carte[i]["entree/sortie"] == True ]

chg = " ___  _               _        _    _\n/ __|(_) _ __   _  _ | | __ _ | |_ (_) ___  _ _\n\__ \| || '  \ | || || |/ _` ||  _|| |/ _ \| ' \  _  _  _\n|___/|_||_|_|_| \_,_||_|\__,_| \__||_|\___/|_||_|(_)(_)(_)\n"

######################## Parametre de la simulation ######################## 
simulation_L = []
nbr_simulation = 0
tps_simulation = 0
temps = 0
cst_tps = 0
puissance = 0 
vitesse = 0
nbr_utilisateur = 0
type = 0
nbr_lampadaire = 0
fonction = 0
Data_d = {}
######################## Parametre de la simulation ######################## 

def updt(total, progress, prefix:str = "Calculs en cours : ", dim:int = 40):
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

def trajet(tps_simulation:int, vitesse:float, type:int = 1, nbr_lampadaire:int = 0)->list:
    """Permet de générer le trajet de façon aléatoire d'un utilisateur dans la ville (trajet logique) \n
    On suppose que les utilisateur vont en avant ou en arrière (ici on parcour la caret en diagonale)

    Parameters
    ----------
    tps_simulation : int
        le temps de la simulation
    vitesse : float
        la vitesse de l'utilisateur 
    type : int
        type de deplacement : 1-deplacement noramale, 2-deplacemnt en saturation du réseau, 3-deplacement avec condition du nbr de deplacement (+ ou - le nombre demander), par default 1
    nbr_lampadaire : int
        nombre min de lampadaire a allumer (pris en compte qu'avec type = 3), par default 0

    Returns
    -------
    list
        liste de devant quel lampadaire passe chaque utilisateur
    """
    sens = "" # on definie le sens dans le quel on va rouler
    begin = start[randint(0, len(start) - 1)] # on choisie un point de départ de façon aléatoire 
    trajet = [begin] # on ajoute le point de depart au trajet 
    if carte[begin]["avant"][0] == 0 : # detection de si on avance ou on va en arrière par rapport au sens de parcours definie par le parametrage de la carte 
        sens = "arriere"
    else :
        sens = "avant"
    if type == 1 : # deplacement aleatoire 
        trajet_tot = []
        while carte[begin][sens][0] != 0 : # on parcours la carte jusqu'a un point de sortie 
            mem = begin
            while begin in trajet : # si on est deja passe par la on prend un autre point 
                begin = str(carte[mem][sens][randint(0, len(carte[mem][sens]) - 1)])
            trajet.append(begin)
        trajet_tot = trajet[:]
    elif type == 2 : # deplacement contine
        trajet_tot = []
        distance_max = vitesse * tps_simulation # on cacule la distance max que peut parcourire les utilisateur en fonction de leur temps impartie
        lampadaire_max = round(distance_max / 0.02) # on determine le nombre max de lampadaire q'il peuvent allumer en fonction de leur vitesse et du temps de l'expérimentation | on a des lampadaire espacer de 20m = 0,02km 
        while lampadaire_max - len(trajet_tot) > 0 :
            while carte[begin][sens][0] != 0 : # on parcours la carte jusqu'a un point de sortie 
                mem = begin
                while begin in trajet : # si on est deja passe par la on prend un autre point 
                    begin = str(carte[mem][sens][randint(0, len(carte[mem][sens]) - 1)])
                trajet.append(begin)
            trajet_tot += trajet # on ajoute le trajet au deplacement totale
            trajet = []
            if carte[begin]["avant"][0] == 0 : # detection de si on avance ou on va en arrière par rapport au sens de parcours definie par le parametrage de la carte 
                sens = "arriere"
            else :
                sens = "avant"
    elif type == 3 : # deplacement avec condition
        trajet_tot = []
        while nbr_lampadaire - len(trajet_tot) > 0 :
            while carte[begin][sens][0] != 0 : # on parcours la carte jusqu'a un point de sortie 
                mem = begin
                while begin in trajet : # si on est deja passe par la on prend un autre point 
                    begin = str(carte[mem][sens][randint(0, len(carte[mem][sens]) - 1)])
                trajet.append(begin)
            trajet_tot += trajet # on ajoute le trajet au deplacement totale
            trajet = []
            if carte[begin]["avant"][0] == 0 : # detection de si on avance ou on va en arrière par rapport au sens de parcours definie par le parametrage de la carte 
                sens = "arriere"
            else :
                sens = "avant"
    
    return trajet_tot

def trajet_voisin(tps_simulation:int, vitesse:float, type:int = 1, nbr_lampadaire:int = 0)->list:
    """Permet de générer le trajet de façon aléatoire d'un utilisateur dans la ville (trajet absurde) \n
    On suppose un déplacement chaotique des utilisateurs (les utilisateur se deplace comme il veule sans logique)

    Parameters
    ----------
    tps_simulation : int
        le temps de la simulation
    vitesse : float
        la vitesse de l'utilisateur 
    type : int
        type de deplacement : 1-deplacement noramale, 2-deplacemnt en saturation du réseau, 3-deplacement avec condition du nbr de deplacement (+ ou - le nombre demander), par default 1
    nbr_lampadaire : int
        nombre min de lampadaire a allumer (pris en compte qu'avec type = 3), par default 0
    
    Returns
    -------
    list
        liste de devant quel lampadaire passe chaque utilisateur
    """
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

def deplacement_calcule(id):
    """Permet le calcule du deplacmement

    Parameters
    ----------
    id : _type_
        id de l'utilisateur
    """
    global Data_d
    vitesse_utilisateur = vitesse[randint(0, len(vitesse) - 1)] # on choisie une vitesse aléatoire pour l'utilisateur
    if fonction == 1 : # on definie le type de trajet a prendre 
        trajet_utilisateur = trajet(tps_simulation, vitesse_utilisateur, type, nbr_lampadaire)
    elif fonction == 2 :
        trajet_utilisateur = trajet_voisin(tps_simulation, vitesse_utilisateur, type, nbr_lampadaire)
    distance_max = vitesse_utilisateur * tps_simulation # on cacule la distance max que peut parcourire les utilisateur en fonction de leur temps impartie
    lampadaire_max = round(distance_max / 0.02) # on determine le nombre max de lampadaire q'il peuvent allumer en fonction de leur vitesse et du temps de l'expérimentation | on a des lampadaire espacer de 20m = 0,02km 
    if len(trajet_utilisateur) > lampadaire_max : # si il y a trop de lampadaire allumer lors du trajet on en retire 
        trajetV2 = [ trajet_utilisateur[i] for i in range(lampadaire_max) ]
        trajet_utilisateur = trajetV2
    Data_d[id] = {
        "trajet" : trajet_utilisateur,
        "vitesse" : vitesse_utilisateur,
        "lampadaire_max" : lampadaire_max,
        "temps" : temps[vitesse.index(vitesse_utilisateur)]
    }

def deplacement(tps_simulation:int, temps:list, vitesse:list, nbr_utilisateur:int, type:int = 1, nbr_lampadaire:int = 0, fonction:int = 1)->dict:
    """Permet de de simuler le deplacement simultane de plusieur utilisateu en meme temps sur un temps donner pour un nombre donné d'utilisateur

    Parameters
    ----------
    tps_simulation : int
        le temps de la simulation
    temps : list
        liste des temps (en h) pris pa les utilisateur 
    vitesse : list
        les vitesse (en km/h) possible entre utilisateur
    nbr_utilisateur : int
        le nombre d'utilisateur
    type : int
        type de deplacement : 1-deplacement noramale, 2-deplacemnt en saturation du réseau, 3-deplacement avec condition du nbr de deplacement (+ ou - le nombre demander), par default 1
    nbr_lampadaire : int
        nombre min de lampadaire a allumer (pris en compte qu'avec type = 3), par default 0
    fonction : int
        la fonction a utiliser pour la simulation du trajet. 1-trajet() | 2-trajet_voisin(), par default trajet()

    Returns
    -------
    dict
        renvoie alors les trajet, les vitesses et le nombre de lampadaire allumable par les utilisateurs
    """
    global Data_d
    global nbr_simulation
    modif(nbr_simulation, tps_simulation, temps, cst_tps, puissance, vitesse, nbr_utilisateur, type, nbr_lampadaire, fonction)
    
    threads = []
    for i in range(nbr_utilisateur):
        t = Thread(target=deplacement_calcule, args=(i,))
        threads.append(t)
        t.start() 
    for p in threads:
        p.join()
    
    return Data_d

def fusion(data:dict)->dict:
    """Permet de rendre tout les liste de la meme taille pour faciliter la comparaison

    Parameters
    ----------
    data : dict
        les données de déplacement de l'utilisateur (vien de la fonction deplacement)

    Returns
    -------
    dict
        la liste des déplacement uniformiser 
    """
    up = max([ len(data[i]["trajet"]) for i in data ]) # on prend l'utilisateur avec le plus de lampadaire d'alumer 
    data_harmo = { i : (data[i]["trajet"]) + [ 0 for _ in range(up - len(data[i]["trajet"])) ] if (len(data[i]["trajet"]) < up) else data[i]["trajet"] for i in data }
    return data_harmo

def deplacement_affectation(data:dict, data_deplacement:dict)->list:
    """Permet de renvoyer la liste d'allumage des lamapadaire en prenans en compte le fait qu'il peut y avaoir plusieur utilisateur au meme endroit au meme moment

    Parameters
    ----------
    data : dict
        la liste qui vien de fusion et qui va permettre de mettre tout ensemble
    data_deplacement : dict 
        dictionnaire des donner de déplaecemment des utilisateurs

    Returns
    -------
    list
        la liste avec le nombr d'allumage de chacun des utilisateur
    """
    lampdaire_list = [ [] for _ in range(len(carte) + 1)] # on compte pas le 0 donc o ajoute 1 (la liste d'utilisateur commence a 1 et se termine donc a n+1)
    calcule = [ lampdaire_list[int(data[p][i])].append(data_deplacement[p]["temps"]) for i in range(len(data[0])) for p in range(len(data)) if int(data[p][i]) != 0 and len(lampdaire_list[int(data[p][i])]) <= i]
    return lampdaire_list

def calcule(tps_simulation:int, puissance:int, cst_tps:int, data:list)->tuple:
    """Permet le calcule de la consomation

    Parameters
    ----------
    tps_simulation : int
        temps de la simulation
    puissance : int
        la puissance des lampadaires
    data : list
        les données du temps d'alumage des lamapdaires 

    Returns
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

    Parameters
    ----------
    data : dict
        les données a sauvegarder
    filepath : path, optional
        le chemin vers le fichier a sauvegarder, by default "save.json"
    """
    with open(filepath, 'w') as mon_fichier: # on créer le fichier voulue et on l'enregistre a l'endroit souhaité 
	    json.dump(data, mon_fichier)

def modif(nbr_s:int, tps_s:int, tps:list, consttps:int, w:int, vit:list, nbr_u:int, Type:int = 1, nbr_l:int = 0, f:int = 1)->None:
    """Permet de mettre a jours les variables a utiliser pour la simulation 

    Parameters
    ----------
    nbr_s : int
        la nombre de simulation a effectuer
    tps_s : int
        le temps de la simulation 
    tps : list
        liste des temsppossible qui peuvent etre prise par les utilisateurs
    consttps : int
        le temps d'allumage des lampadaires 
    w : int
        puissance des lamapdaires
    vit : list
        vitesse des utilisateur 
    nbr_u : int
        nombre d'utilisateur
    Type : int
        type de deplacement : 1-deplacement noramale, 2-deplacemnt en saturation du réseau, 3-deplacement avec condition du nbr de deplacement (+ ou - le nombre demander), par default 1
    nbr_l : int
        nombre min de lampadaire a allumer (pris en compte qu'avec type = 3), par default 0
    f : int
        la fonction a utiliser pour la simulation du trajet. 1-trajet() | 2-trajet_voisin(), par default trajet()
        
    Returns
    -------
    None
    """
    global nbr_simulation
    nbr_simulation = nbr_s
    global tps_simulation
    tps_simulation = tps_s
    global temps
    temps = tps
    global cst_tps
    cst_tps = consttps
    global puissance
    puissance = w
    global vitesse
    vitesse = vit
    global nbr_utilisateur
    nbr_utilisateur = nbr_u
    global type
    type = Type
    global nbr_lampadaire
    nbr_lampadaire = nbr_l
    global fonction
    fonction = f
    
def simulation_calcule(id)->None:
    """Permet de generer une simulation

    Parameters
    ----------
    id : _type_
        id de la tache effectuer

    Returns
    -------
    None
    """
    etape1 = deplacement(tps_simulation, temps, vitesse, nbr_utilisateur, type, nbr_lampadaire, fonction)
    etape2 = fusion(etape1)
    etape3 = deplacement_affectation(etape2, etape1)
    etape4 = calcule(tps_simulation, puissance, cst_tps, etape3)
    simulation_L.append(etape4)

def simulation(nbr_simulation:int, tps_simulation:int, temps:list, cst_tps:int, puissance:int, vitesse:list, nbr_utilisateur:int, type:int = 1, nbr_lampadaire:int = 0, fonction:int = 1, save:bool = False)->dict:
    """Permet de simuler la consomation des lampadaires

    Parameters
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
        type de deplacement : 1-deplacement noramale, 2-deplacemnt en saturation du réseau, 3-deplacement avec condition du nbr de deplacement (+ ou - le nombre demander), par default 1
    nbr_lampadaire : int
        nombre min de lampadaire a allumer (pris en compte qu'avec type = 3), par default 0
    fonction : int
        la fonction a utiliser pour la simulation du trajet. 1-trajet() | 2-trajet_voisin(), par default trajet()
    save : bool
        si on sauvegarde ou non les données ?, par defaut non

    Returns
    -------
    dict
        renvoie alors la consomation moyenne otimiser et celle classique ainsi que tout les valeur de simmulation. ( { "sim" : [...], "moy" : (.., ..)} )
    """
    start = time.time()

    print(chg)
    modif(nbr_simulation, tps_simulation, temps, cst_tps, puissance, vitesse, nbr_utilisateur, type, nbr_lampadaire, fonction)
    threads = []
    for i in range(nbr_simulation):
        t = Thread(target=simulation_calcule, args=(i,))
        threads.append(t)
        t.start()
        updt(nbr_simulation, i + 1, "Initialisation : ")
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print(chg)
    a = 0
    for p in threads:
        p.join()
        a += 1
        updt(len(threads), a, "Verification : ")
        

    optimiser_list = [ i[0] for i in simulation_L ] # on fait les moyenne 
    classic_list = [ i[1] for i in simulation_L ]
    moy_opti = sum(optimiser_list)/len(simulation_L)
    moy_classic = sum(classic_list)/len(simulation_L)
    
    end = time.time()
    
    rep = {
        "sim" : simulation_L,
        "moy" : (moy_opti, moy_classic),
        "tps_tot" : end - start,
    }
    
    if save == True :
        data = {"rep_simulation" : rep, "parametre" : {"nbr_simulation" : nbr_simulation, "tps_simulation" : tps_simulation, "temps": temps, "cst_tps" : cst_tps, "puissance": puissance, "vitesse": vitesse, "nbr_utilisateur": nbr_utilisateur, "type": type, "nbr_lampadaire": nbr_lampadaire, "fonction": fonction, "save": save}}
        f_save(data) 
    return rep
