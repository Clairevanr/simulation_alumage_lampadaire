from random import *
# pour stocker les valeurs calculer
import json
with open('lampadaire.json') as json_data:
    lampadaire = json.load(json_data)
# pour stocker les valeurs calculer

# constante 
nbr_lampadaire = 50
const_tps = 40000 #en ms
puissance = 70 #en W
# constante 

Data = { i : {"nb_allumage" : 0, "tps_allumage" : 0} for i in range(nbr_lampadaire) } # initialisations de la liste des données 

def tps_éclairage(const_tps_:int)->int: 
    """Permet de générer un temps aléatoire de simulation de pour l'allumage des lampadaires 

    Returns
    -------
    int
        Renvoie un temps en `ms`
    """
    tps = [3000, 1600, 1200, 960, 800]
    return (tps[randint(0, len(tps) - 1)] * const_tps_)

def alea_personne(nbr_utilisateur:int, nbr_passage:int, lampadaire_data:dict)->None:
    """Permet de simuler le comportement aléatoire dun certain nombre d'utilisateur en fonction du nombre de lampadaire

    Parameters
    ----------
    nbr : int
        le nombre d'utilisateur
    lampadaire_data : dict
        le dictionnaire qui contiens les donner des lampadaire 

    Returns
    -------
    dict
        renvoie le dictionnaire modifier en fonction de l'utilisation des lampadaire 
    """
    for p in range(nbr_passage) :
        for u in range(nbr_utilisateur) :
            alea = randint(0, nbr_lampadaire - 1)
            lampadaire_data[alea]["nb_allumage"] += 1
            lampadaire_data[alea]["tps_allumage"] += tps_éclairage(const_tps)

def consommation_optimiser(puissance:int, data:dict)->float :
    """Calcule de la consommation avec la méthode optimiser

    Parameters
    ----------
    puissance : int
        La puissance du lampadaire étudier 
    data : dict
        Le dictionnaire qui contient toute les données 

    Returns
    -------
    float
        Renvoie la consommation en Wh pour la simulation donnée 
    """
    tps = 0
    for i in data :
        tps += data[i]["tps_allumage"]
    return (tps/3.6*10**-6) * puissance 

def consommation_classique(puissance:int, nbr_lampadaire:int, data:dict)->float :
    """Calcule de la consommation avec la méthode classique 

    Parameters
    ----------
    puissance : int
        Puissance du lampadaire étudier
    nbr_lampadaire : int
        le nombre de lampadaire étudier 
    data : dict
        Le dictionnaire qui contient toute les données 

    Returns
    -------
    float
        Renvoie la consommation en Wh pour la simulation donnée 
    """
    tps = max([ data[i]["tps_allumage"] for i in range(len(data)) ])
    return (tps/3.6*10**-6) * nbr_lampadaire * puissance

def mise_en_forme(nbr_utilisateur:int, nbr_passage:int, data:dict)->None:
    """Permet la mise ne forme dans le terminale des réponses 

    Parameters
    ----------
    nbr_utilisateur : int
        nombre d'utilisateur
    nbr_passage : int
        nombre de passage de chaque utilisateur 
    data : dict
        le dictionnaire qui contient toute les données 
    """
    alea_personne(nbr_utilisateur, nbr_passage, data)
    print("\n")
    print(" - Consommation optimiser : " + str(round(consommation_optimiser(puissance, Data))) + "Wh = " + str(round(consommation_optimiser(puissance, Data)*10**-3)) + "kWh")
    print(" - Consommation classique : " + str(round(consommation_classique(puissance, nbr_lampadaire, Data))) + "Wh = " + str(round(consommation_classique(puissance, nbr_lampadaire, Data)*10**-3)) + "kWh")
    print(" - Écart : " + str(round((abs(consommation_classique(puissance, nbr_lampadaire, Data) - consommation_optimiser(puissance, Data)) / consommation_classique(puissance, nbr_lampadaire, Data)) * 100)) + "%")
    print("\n")
    
mise_en_forme(30, 10, Data)
       
with open('lampadaire.json', 'w') as mon_fichier: # on sauvegarde dans un fichier pour facilité la lecture 
	json.dump(Data, mon_fichier)