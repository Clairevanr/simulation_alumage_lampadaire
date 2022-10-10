import sys

def progressbar(it, prefix="", size=60, file=sys.stdout):
    """
    Il prend un itérable et renvoie un itérable qui imprime une barre de progression à l'écran lorsqu'il
    parcourt l'itérable d'origine.
    
    :param it: l'objet itérable sur lequel vous voulez itérer
    :param prefix: Le texte à afficher avant la barre de progression
    :param size: La longueur de la barre de progression en caractères, defaults to 60 (optional)
    :param file: Le fichier dans lequel écrire la barre de progression. La valeur par défaut est
    sys.stdout afin qu'il s'imprime à l'écran
    """
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()
        file.write("\n")
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
        file.write("\n")
    file.flush()
    
import time
import os
rep = 0
for i in progressbar(range(100), "Computing: ", 40):
    rep += 1
    os.system('cls' if os.name == 'nt' else 'clear')
    time.sleep(0.1)

print(rep)


