"""Permet de faire des tests du programme
"""

from Code.graph import *
from Code.graph_comparaison import *
from Code.graph_save import *

iteration = 100
tps_simulation = 1
cst_tps = 0
puissance = 70
nbr_utilisateur = 100
proba = [1, 10, False]
save = False

graphe1(iteration, tps_simulation, cst_tps, puissance, nbr_utilisateur, 1, 0, 1, proba, save)