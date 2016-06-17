#/bin/bash

cd /home/pi/github/bf_reaction_buttons
DAY=$(date +%Y-%m-%d)
LSTDERR=log/buttons.$DAY.err.log
LSTDOUT=log/buttons.$DAY.out.txt
/usr/bin/python ./buttons.py 2> $LSTDERR > $LSTDOUT
