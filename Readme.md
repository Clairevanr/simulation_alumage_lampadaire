# Simulation Allumage Lampadaire 
*L'objectif de cette simulation est de pouvoir obtinir la comparaison entre la consomation normale d'une ville (au niveau des lampadaires par rapport a une version optimiser)*

## Sommaire 
1. [Description](#description)
2. [Utilisation](#utilisation)
3. [Les Fonctions](#les-fonctions)


## Description 

### Hypothèse 
* On assimile les utilisateur a un **point** il peut y en avoir une quantiter infinie en dessous d'un lapadaire cepandant celui-ci ne comptera qu'un allumage simple a un instant `t`
* On simplifie le réseau routier au lampadaire. On cosidère donc que tout les lampdaire sont accésible par les utilisateur et ceux par la route.
* On ne considère pas les ambouteillages ou la saturation du réseau routier

### Pris en cmpte dans la simulation
* Les diverse vitesse des utilisateur
* La variations du temps d'allumage des lampadaire en fonction de la vitesse des utilisteur 
* Les utilisateur peuvent etre plusieur sous un lampadaire sans pour compter un nombre d'allumage multiple 
* La probabiliter qu'un utilisateur puisse s'arrter devant un lampdaire pendant un certain temps

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
> Même système que la **3.** a la différence que la longeur min n'est pas fixé identique pour chaque utilisateur mais diférente. La longeur du trajet est choisie de façon aléatoire entre `6` et le nombre max de lampadaire allumable pour le deplacement.

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

## Les fonctions 
On va ici décrire le fonctionnement des fonctions importante du programme

***
### `adaptation(trajet:list, vitesse:float, tps_simulation:int)->list:`
> Cette fonction permet de rajouter a la liste le fait que les utilisateur se deplace plus ou moin vite et qu'il arrive donc par conséquent par au meme endroit en focntion de la vitesse en fonction du temps.

On prend donc ici une résolution de $0,25$ s pour le calcule afin d'avoir de pourvoir voir une différence dans les haute vitesse (>130km/h) on aura donc pour formule :
$$
L_{\text{max}} = \frac{0,25 \times Tps}{6.94444e-5} \text{ (formule de la taille de la liste) } (1)
$$
Ou $L_{\text{max}}$ : est la taille de la liste a créer, $0,25$ : la résolution de la liste et $6.94444e-5$ : correspond a $0,25$ en heure. \
Il sagit d'un produit en croix :
| $Tps$ | $L_{\text{max}}$ |
|-------|------------------|
| $6.94444e-5$ | $0,25$ |

$$
\text{Nb} = \frac{20}{V \times 0,25} \text{ (formule du nombre de point) }(2)
$$
Ou $Nb$ : est le nombre de point avant un lampadaire, $V$ : la vitesse en m/s et $0,25$ : la résolution. \
Il s'agit d'un produit en croix pour $V \times 0,25$ :
| $V$ | $1$ |
|---|---|
| $X$ | $0,25$ |

Ou $X$ : est la vitesse ramener en nombre de point

#### Vérification de la méthode : 
On se place dans le cas ou $V = 40$ km/h $\approx 11,1$ m/s : \
On ara donc $X = 11,1 \times 0,25 \approx 2,8$ d'ou $Nb = \frac{20}{2,8} \approx 7,1$ on a donc $Nb$ qui est le nombre qui correspond au nombre de point nécéssaire pour parcourire environ 20m (soit la distance entre les lampadaire). \
On vérifie la cohérence : \
$T_{\text{tot}} = 7,1 \times 0,25 \approx 1,8$ s, soit $V_{\text{verif}} = \frac{D}{T_{\text{tot}}}$ ou $D = 20$ m on aura $V_{\text{verif}} = \frac{20}{1,8} \approx 11,1$ m/s on retrouve donc bien notre vitesse initiale lla formule est donc cohérente.

#### Homogénité :
* Pour la formule $(1)$ : 
$$
A = \frac{A \times T}{T} = A
$$
Le $0,25$ n'a pas de dimention ici car il représente la précision de l'échelle et non un temps
* Pour la formule $(2) :$
$$
A = \frac{D}{\frac{D}{T} \times T} = \frac{D}D = A
$$
Le $0,25$ a une dimmension ici car il represente l'intervalle de temps \
On a $A$ pour adimentionné
\
\
\
*Réaslisation de se programme dans le cadre du TIPE PSI - 2022/2023*