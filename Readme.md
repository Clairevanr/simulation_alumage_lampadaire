# Simulation Allumage Lampadaire 
*L'objectif de cette simulation est de pouvoir obtinir la comparaison entre la consomation normale d'une ville (au niveau des lampadaires par rapport a une version optimiser)*

## Sommaire 
1. [Description](#description)
2. [Utilisation](#utilisation)


## Description 

### Hypothèse 
* On assimile les utilisateur a un **point** il peut y en avoir une quantiter infinie en dessous d'un lapadaire cepandant celui-ci ne comptera qu'un allumage simple a un instant `t`
* On simplifie le réseau routier au lampadaire. On cosidère donc que tout les lampdaire sont accésible par les utilisateur et ceux par la route.
* On ne considère pas les ambouteillages ou la saturation du réseau routier

### Pris en cmpte dans la simulation
* On prend en compte les diverse vitesse des utilisateur
* On prend en compte la variations du temps d'allumage des lampadaire en fonction de la vitesse des utilisteur 
* On prend en compte que les utilisateur puisse etre plusieur sous un lampadaire sans pour compter un nombre d'allumage multiple 
* On prend en compte la probabiliter qu'un utilisateur puisse s'arrter devant un lampdaire pendant un certain temps

## Utilisation  
Explication de commment utiliser le programme. \
Dans un premier temps il faut exécuter le fichier [`play.py`](./play.py) ou bien le fichier [`start.sh`](./Start.sh) si vous utiliser linux ou macos et ceux directement dans le Terminale. \
A noté que le fichier [`start.sh`](./Start.sh) permet une utilisation plus simple des ficier se trouvant dans `./Code`, il n'est donc pas obligatoire.

***
### Etape 1 - Choix du resulta 
L'utilisateur a le choix entre diverse mise en forme des résulta : 
1. `Normale` :
> A la fin de la simulation on obtien un résulta sout la forme d'un graphique simple (grace a la bibilotèque `mathplotlib`), deplus on a une mise en forme des résultas et valeur importante de la simulation.
> ```txt
>  ___                 _  _          _
>| _ \ ___  ___ _  _ | || |_  __ _ | |_  ___
>|   // -_)(_-<| || || ||  _|/ _` ||  _|(_-<
>|_|_\\___|/__/ \_,_||_| \__|\__,_| \__|/__/
>Valeur moyenne : 
>
> - Optimiser : 26160.82wh
> - Normale : 44520.0wh 
>
>u(consomation optimiser) = 1134.5508467399704
>
>Ecart : 41.238050314465404%
>
>Temps : 
>
> - Temps totale : 59.231847047805786s
> ```
2. `Double` :
> On obtien alors le meme résultas que le 1. `Normale` a la différence que nous obtenons la valeur simuler pour la fonction `1` et `2` ainsi qu'un graphique double.
3. `A partir d'une sauvegarde` :
> Permet a partir d'une sauvegarde (fichier en `.json`) de regénérer les résultas d'une simulation enregsitré. On onbtien alors le résulta donné en 1. `Normale` (la sauvegarde n'étant pas disponible pour 2. `Double`)

***
### Etape 2 - Parametrage des constantes
Il vous est alors demande quel sont les paramettre que vous voulez utiliser pour la simulation.

`Puissance = ` :
> Il faut indiquer le puissance des lampadaire en W.

`Constante de temps = ` :
> Il sagit du temps d'allumage supplémentaire des lampadaires il est en s.

`Nombre de simulation = ` :
> Il sagit du nombre de simulation qui seront effectuer.

`Temps de la simualtion = ` :
> Il sagit du temps que la simulation va duré en h. Ce paramètre conditionne donc la distance maximale que peut parcourire un utilisateur lors de la simulation.

`Nombre d'utilisateur = ` :
> Il sagit du nombre d'utilisateur qui seront simuler pour se deplacer dans la ville 

***
### Etape 3  - Parametrage de la fonction de calcule de trajet
On choisie ici la fonction de calcule du trajet des utilisateur 

#### Etape 3a - Choix de la fonction
1. `Logique` :
> Se système de simulation permet d'voir un deplacement logique, les utilisateur ne repasse jamais devant le meme lamapdaire et se deplacement en allant de l'avant vers une sortie. se type de deplacment donne alors une direction suivant une diagonale allant du coin gache en supérieur vers le droit inférieur.

2. `Chaotique` :
> Se système de deplacement laisse les utilisateur aller ou bon leur semble le trajet est finie qu'a la condition ou ou atteint une "sortie". Se deplacment est moin réaliste d'un vrais deplacmement cependant il permet d'avoir une plus grand varieter de trajet ainsi que d'allumage des lamapdaire.

#### Etape 3b - Parametrage de la fonction 
1. `Aléatoire` :
> On laisse la fonction se dérouler normalement sans condition précise 

2. `Deplacement en continue (saturation)` : 
> Les trajets sont établie de façon a se que l'utilisateur de deplace durant toute la simulation. On dit en saturation car le deplacement des utilisteurs est tel que les lamapdaires reste allumer en permanance on alors le meme résulta que si les lamapdaire reste allumer en continue.

3. `Avec minimum de deplacmement` :
> On reprend le principe de la **1.** mais cette fois si on immpose un nombre minimum de lampadaire a allumé. Une fois un premier trajet simulé si il est trop cour on reprend alors de la sortie pour aller vers une autre et on lajoute au trajet existant, on recommence jusqu'a que la longeur du trajet soit supétieur ou égale a la valeur minimum

4. `deplacement aleatoire etandu (avec min aleatoire)`
> Même système que la **3.** a la différence que la longeur min n'est pas fixé identique pour chaque utilisateur mais diférente. La longeur du trajet est choisie de façon aléatoire entre `6` et `5000` deplacement.

***
### Etape 4 - Arret des utilisateurs
On choisi ici d'activer ou non la prise en compte du fait que les utilisateur puisse s'arreter devant un lampadaire. (A noter que pour la fonction 1. `Logique` la prise en cmpte de se paramttre se fait de façon externe au cacule du deplacment de se fait elle est moin precise, par default on est regler sur une palge de 1 a 5 pour le nombre de fois ou on rest devant le lampdaire).

Si vous choisez `oui` ou `o` :
> On vous demande de choisir la probabiliter que l'utilisateur reste devant un lampadaire.
> On a donc $\frac{1}{10}$ qui donne `1/10`

***
### Etape 5 - Activativation de la sauvegarde*
Il est possible d'activer la sauvegarde du resulta la simmulation dans un fichier [`save.json`](./Donnees/save.json), il est stocker dans `./Donnees/`. \
*Attention la sauvegarde n'est disponible que pour le choix 1. `Normale` et non `Double`.
\
\
\
*Réaslisation de se programme dans le cadre du TIPE PSI - 2022/2023*