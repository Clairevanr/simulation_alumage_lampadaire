from Code.main import *
from matplotlib import pyplot
import numpy as np

vitesse = [7.2, 54, 72, 90, 108] # en km/h
temps = [3, 1.6, 1.2, 0.96, 0.8] # en s
puissance = 70 # en W
cst_tps = 6 # en s

iteration = 1000
tps_simulation = 12
nbr_utilisateur = 50
Type = 1
nbr_allumage = 100

val1 = simulation(iteration, tps_simulation, temps, cst_tps, puissance, vitesse, nbr_utilisateur, Type, nbr_allumage, 1)
val_opti1 = [ i[0] for i in val1["sim"] ]
val_norm1 = [ i[1] for i in val1["sim"] ]

born_min1 = min(val_opti1) - 5
born_max1 = max(val_opti1) + 5

# méthode montecarlo
uopti = (1/(iteration-1)*sum((np.array(val_opti1)-val1["moy"][0])**2.))**0.5

print("\n")
print("Valeur moyenne 1 : \n")
print(" - Optimiser : " + str(val1["moy"][0]) + "wh")
print(" - Normale : " + str(val1["moy"][1]) + "wh \n")
print("u(consomation optimiser) = " + str(uopti) + "\n")
print("Ecart : " + str(((abs(val1["moy"][0] - val1["moy"][1]) / val1["moy"][1]) * 100)) + "%")
print("\n")
##################################################################################################################

val2 = simulation(iteration, tps_simulation, temps, cst_tps, puissance, vitesse, nbr_utilisateur, Type, nbr_allumage, 2)
val_opti2 = [ i[0] for i in val2["sim"] ]
val_norm2 = [ i[1] for i in val2["sim"] ]

born_min2 = min(val_opti2) - 5
born_max2 = max(val_opti2) + 5

# méthode montecarlo
uopti = (1/(iteration-1)*sum((np.array(val_opti2)-val2["moy"][0])**2.))**0.5

print("\n")
print("Valeur moyenne 2 : \n")
print(" - Optimiser : " + str(val2["moy"][0]) + "wh")
print(" - Normale : " + str(val2["moy"][1]) + "wh \n")
print("u(consomation optimiser) = " + str(uopti) + "\n")
print("Ecart : " + str(((abs(val2["moy"][0] - val2["moy"][1]) / val2["moy"][1]) * 100)) + "%")
print("\n")
##################################################################################################################

born_max = max(born_max1, born_max2)
born_min = min(born_min1, born_min2)

figure = pyplot.figure(figsize = (7, 7))
pyplot.gcf().subplots_adjust(left = 0.1, bottom = 0.1, right = 0.9, top = 0.9, wspace = 0, hspace = 0.3)
axes = figure.add_subplot(2, 1, 1)
axes.set_xlabel('consomation (en wh)')
axes.set_ylabel('effectif')
axes.set_title('Consomation des lamapdaires par la méthode trajet() - Pour ' + str(iteration) + ' iterations')
axes.hist(val_opti1, range = (born_min, born_max), bins = 200, color = 'blue', edgecolor = 'black')
axes = figure.add_subplot(2, 1, 2)
axes.set_xlabel('consomation (en wh)')
axes.set_ylabel('effectif')
axes.set_title('Consomation des lamapdaires par la méthode trajet_voisins() - Pour ' + str(iteration) + ' iterations')
axes.hist(val_opti2, range = (born_min, born_max), bins = 200, color = 'red', edgecolor = 'black')
pyplot.show()