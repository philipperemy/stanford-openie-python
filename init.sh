#!/bin/bash
mkdir stanford-openie
wget -nc http://nlp.stanford.edu/projects/naturalli/stanford-openie.jar
wget -nc http://nlp.stanford.edu/projects/naturalli/stanford-openie-models.jar
mv stanford-openie.jar stanford-openie-models.jar stanford-openie
echo "Google bought IBM for $10." > samples.txt
python main.py -f samples.txt -v
