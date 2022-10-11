#!/bin/bash
cd $(dirname $(readlink -f $0)) # on se rend la ou le fichier se trouve
python play.py