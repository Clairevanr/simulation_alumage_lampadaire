import json
from random import *

with open('carte.json') as json_carte:
    carte = json.load(json_carte)
    
Data = { i : {"nb_allumage" : 0, "tps_allumage" : 0} for i in range(len(carte)) } # initialisations de la liste des données 
start = [ i for i in carte if carte[i]["entree/sortie"] == True ]
vitesse = [7.2, 54, 72, 90, 108] # en km/h
puissance = 70 # en W
cst_tps = 6 # en s

def trajet()->list:
    """Permet de générer le trajet de façon aléatoire d'un utilisateur dans la ville (trajet logique) \n
    On suppose que les utilisateur vont en avant

    Returns
    -------
    list
        liste de devant quel lampadaire passe chaque utilisateur
    """
    sens = ""
    begin = start[randint(0, len(start) - 1)]
    trajet = [begin]
    if carte[begin]["avant"][0] == 0 :
        sens = "arriere"
    else :
        sens = "avant"
    while carte[begin][sens][0] != 0 :
        mem = begin
        while begin in trajet :
            begin = str(carte[mem][sens][randint(0, len(carte[mem][sens]) - 1)])
        trajet.append(begin)
    return trajet

def trajet_voisin()->list:
    """Permet de générer le trajet de façon aléatoire d'un utilisateur dans la ville (trajet absurde) \n
    On suppose un déplacement chaotique des utilisateurs

    Returns
    -------
    list
        liste de devant quel lampadaire passe chaque utilisateur
    """
    begin = start[randint(0, len(start) - 1)]
    trajet = [begin]
    if carte[begin]["voisins"][0] == 0 :
        begin = str(carte[begin]["voisins"][1])
    else :
        begin = str(carte[begin]["voisins"][0])
    trajet.append(begin)
    while 0 not in carte[begin]["voisins"]:
        begin = str(carte[begin]["voisins"][randint(0, len(carte[begin]["voisins"]) - 1)])
        trajet.append(begin)
    return trajet

def deplacement(tps:int, vitesse:list, nbr_utilisateur:int)->dict:
    """Permet de de simuler le deplacement simultane de plusieur utilisateu en meme temps sur un temps donner pour un nombre donné d'utilisateur

    Parameters
    ----------
    tps : int
        le temps de la simulation
    vitesse : list
        les vitesse possible entre utilisateur
    nbr_utilisateur : int
        le nombre d'utilisateur

    Returns
    -------
    dict
        renvoie alors les trajet, les vitesses et le nombre de lampadaire allumable par les utilisateurs
    """
    data = {}
    for i in range(nbr_utilisateur):
        vitesse_utilisateur = vitesse[randint(0, len(vitesse) - 1)]
        trajet_utilisateur = trajet()
        distance_max = vitesse_utilisateur * tps
        lampadaire_max = round(distance_max / 20)
        if len(trajet_utilisateur) > lampadaire_max :
            trajetV2 = [ trajet_utilisateur[i] for i in range(lampadaire_max)]
            trajet_utilisateur = trajetV2
        data[i] = {
            "trajet" : trajet_utilisateur,
            "vitesse" : vitesse_utilisateur,
            "lampadaire_max" : lampadaire_max
        }
    return data

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
    data_harmo = {}
    up = max([ data[i]["lampadaire_max"] for i in data ])
    for i in data :
        data_harmo[i] = data[i]["trajet"]
        if len(data[i]["trajet"]) < up :
            rajout = up - len(data[i]["trajet"])
            for _ in range(rajout) :
                data_harmo[i].append(0)
    return data_harmo

def deplacement_affectation(data:dict)->list:
    """Permet de renvoyer la liste d'allumage des lamapadaire en prenans en compte le fait qu'il peut y avaoir plusieur utilisateur au meme endroit au meme moment

    Parameters
    ----------
    data : dict
        la liste qui vien de fusion et qui va permettre de mettre tout ensemble

    Returns
    -------
    list
        la liste avec le nombr d'allumage de chacun des utilisateur
    """
    lampdaire_list = [ 0 for _ in range(len(carte) + 1)] # on compte pas le 0 
    for i in range(len(data[0])) :
        for p in range(len(data)) :
            if int(data[p][i]) != 0 and lampdaire_list[int(data[p][i])] <= i: # le 0 est tjr vide 
                lampdaire_list[int(data[p][i])] += 1
    return lampdaire_list

def calcule(tps_simulation:int, tps_allumage:int, puissance:int, data:list)->tuple:
    """Permet le calcule de la consomation

    Parameters
    ----------
    tps_simulation : int
        temps de la simulation
    tps_allumage : int
        temps d'allumage des lamapdaires 
    puissance : int
        la puissance des lampadaires
    data : list
        les données d'alumage des lamapdaires 

    Returns
    -------
    tuple
        (consomation optimiser , consomation classique)
    """
    simulation_optimiser = 0
    for i in data :
        simulation_optimiser += i
    simulation_classic = len(carte)
    conso_opti = ((tps_allumage*simulation_optimiser)/3600) * puissance 
    conso_classic = (tps_simulation*simulation_classic) * puissance 
    return (round(conso_opti), round(conso_classic))

def simulation(nbr_simulation:int, tps_simulation:int, cst_tps:int, puissance:int, vitesse:list, nbr_utilisateur:int)->dict:
    """Permet de simuler la consomation des lampadaires

    Parameters
    ----------
    nbr_simulation : int
        la nombre de simulation a effectuer
    tps_simulation : int
        le temps de la simulation 
    cst_tps : int
        le temps d'allumage des lampadaires 
    puissance : int
        puissance des lamapdaires
    vitesse : list
        vitesse des utilisateur 
    nbr_utilisateur : int
        nombre d'utilisateur

    Returns
    -------
    dict
        renvoie alors la consomation moyenne otimiser et celle classique ainsi que tout les valeur de simmulation. ( { "sim" : [...], "moy" : (.., ..)} )
    """
    simulation = []
    for _ in range(nbr_simulation) : 
        etape1 = deplacement(tps_simulation, vitesse, nbr_utilisateur)
        etape2 = fusion(etape1)
        etape3 = deplacement_affectation(etape2)
        etape4 = calcule(tps_simulation, cst_tps, puissance, etape3)
        simulation.append(etape4)

    optimiser_list = [ i[0] for i in simulation]
    classic_list = [ i[1] for i in simulation]
    moy_opti = sum(optimiser_list)/len(simulation)
    moy_classic = sum(classic_list)/len(simulation)
    rep = {
        "sim" : simulation,
        "moy" : (moy_opti, moy_classic)
    }
    return rep