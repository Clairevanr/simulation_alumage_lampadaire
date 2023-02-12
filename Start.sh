#!/bin/bash
cd $(dirname $(readlink -f $0)) # on se rend la ou le fichier se trouve

test=$(pm2 -v)

arrIN2=(${test//./ }) #on sépare par '.'

if [ ${arrIN2} -ge 5 ] # si le version est supérieur ou égale a 16 
then 
    pm2 start play.py --name play_simul --interpreter python3
else
    python play.py
fi