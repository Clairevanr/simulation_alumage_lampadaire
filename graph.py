from main import *
from matplotlib import pyplot
import numpy as np

vitesse = [7.2, 54, 72, 90, 108] # en km/h
temps = [3, 1.6, 1.2, 0.96, 0.8] # en s
puissance = 70 # en W
cst_tps = 6 # en s

iteration = 1000
tps_simulation = 12
nbr_utilisateur = 50

val = simulation(iteration, tps_simulation, temps, cst_tps, puissance, vitesse, nbr_utilisateur, 1)
val_opti = [ i[0] for i in val["sim"] ]
val_norm = [ i[1] for i in val["sim"] ]

born_min = min(val_opti) - 5
born_max = max(val_opti) + 5

uopti = (1/(iteration-1)*sum((np.array(val_opti)-val["moy"][0])**2.))**0.5

print("\n")
print("Valeur moyenne 1 : \n")
print(" - Optimiser : " + str(val["moy"][0]) + "wh")
print(" - Normale : " + str(val["moy"][1]) + "wh \n")
print("u(consomation optimiser) = " + str(uopti) + "\n")
print("Ecart : " + str(((abs(val["moy"][0] - val["moy"][1]) / val["moy"][1]) * 100)) + "%")
print("\n")
##################################################################################################################
pyplot.hist(val_opti, range = (born_min, born_max), bins = 200, color = 'blue', edgecolor = 'black')
pyplot.xlabel('consomation (en wh)')
pyplot.ylabel('effectif')
pyplot.title('Pour ' + str(iteration) + ' iterations - Consomation optimisé')
pyplot.show()
