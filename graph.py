from main import *
from matplotlib import pyplot
import numpy as np

vitesse = [7.2, 54, 72, 90, 108] # en km/h
puissance = 70 # en W
cst_tps = 6 # en s

iteration = 5000

val = simulation(iteration, 5, cst_tps, puissance, vitesse, 50)
val_opti = [ i[0] for i in val["sim"]]
val_norm = [ i[1] for i in val["sim"]]

born_min = min(val_opti) - 5
born_max = max(val_opti) + 5

uopti = (1/(iteration-1)*sum((np.array(val_opti)-val["moy"][0])**2.))**0.5

print("\n")
print("Valeur moyenne : \n")
print(" - Optimiser : " + str(val["moy"][0]) + "wh")
print(" - Normale : " + str(val["moy"][1]) + "wh \n")
print("u(consomation optimiser) = " + str(uopti) + "\n")
print("Ecart : " + str(((abs(val["moy"][0] - val["moy"][1]) / val["moy"][1]) * 100)) + "%")
print("\n")

pyplot.hist(val_opti, range = (born_min, born_max), bins = 200, color = 'blue', edgecolor = 'black')
pyplot.xlabel('consomation (en wh)')
pyplot.ylabel('effectif')
pyplot.title('Pour ' + str(iteration) + ' iterations - Consomation optimisé')
pyplot.show()

"""figure = pyplot.figure(figsize = (7, 7))
pyplot.gcf().subplots_adjust(left = 0.1, bottom = 0.1, right = 0.9, top = 0.9, wspace = 0, hspace = 0.3)
axes = figure.add_subplot(2, 1, 1)
axes.set_xlabel('consomation (en wh)')
axes.set_ylabel('effectif')
axes.set_title('Consomation des lamapdaires par la méthode otimisé')
axes.hist(val_opti, range = (born_min, born_max), bins = 200, color = 'blue', edgecolor = 'black')
axes = figure.add_subplot(2, 1, 2)
axes.set_xlabel('consomation (en wh)')
axes.set_ylabel('effectif')
axes.set_title('Consomation des lamapdaires par la méthode classique')
axes.hist(val_norm, range = (18000, 20000), bins = 200, color = 'blue', edgecolor = 'black')
pyplot.show()"""