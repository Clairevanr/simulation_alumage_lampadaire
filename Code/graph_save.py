import json
from matplotlib import pyplot
import numpy as np

def graph_save(filepath = "./Donnees/save.json")->None:
    """Permet de génerer un graphique d'une simulation a partir d'une sauvegarde

    Parameters
    ----------
    filepath : str, optional
        le chemin ver la sauvegarde, by default "./Donnees/save.json"
    
    Returns
    -------
    None
    """
    with open('./Donnees/save.json') as json_carte:
        save = json.load(json_carte)

    iteration = save["parametre"]["nbr_simulation"]
    val = save
    val_opti = [ i[0] for i in save["rep_simulation"]["sim"] ]
    val_norm = [ i[1] for i in save["rep_simulation"]["sim"] ]

    born_min = min(val_opti) - 5
    born_max = max(val_opti) + 5

    # méthode montecarlo
    uopti = (1/(iteration-1)*sum((np.array(val_opti)-val["rep_simulation"]["moy"][0])**2.))**0.5

    print("\n")
    print("Valeur moyenne : \n")
    print(" - Optimiser : " + str(val["rep_simulation"]["moy"][0]) + "wh")
    print(" - Normale : " + str(val["rep_simulation"]["moy"][1]) + "wh \n")
    print("u(consomation optimiser) = " + str(uopti) + "\n")
    print("Ecart : " + str(((abs(val["rep_simulation"]["moy"][0] - val["rep_simulation"]["moy"][1]) / val["rep_simulation"]["moy"][1]) * 100)) + "%\n")
    print("Temps : \n")
    print(" - Temps totale : " + str(val["rep_simulation"]["tps_tot"]) + "s")
    print(" - Temps boucle : " + str(val["rep_simulation"]["tps_boucle"]) + "s")
    print("\n")
    ##################################################################################################################
    pyplot.hist(val_opti, range = (born_min, born_max), bins = 200, color = 'blue', edgecolor = 'black')
    pyplot.xlabel('consomation (en wh)')
    pyplot.ylabel('effectif')
    pyplot.title('Pour ' + str(iteration) + ' iterations - Consomation optimisé')
    pyplot.show()