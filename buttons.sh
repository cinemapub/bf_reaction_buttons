#/bin/bash

cd /home/pi/github/bf_reaction_buttons
LOGFILE=log/buttons.log
OUTFILE=log/buttons.txt
/usr/bin/python ./buttons.py 2> $LOGFILE > $OUTFILE
