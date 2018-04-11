#!/bin/bash
mkdir -p ../smoothed/
while read node;
do
    ssh -o StrictHostKeyChecking=no  jstruye@node${node}.lab.cityofthings.eu 'cd smoothed && find . -name '\''*line'\'' -exec rm {} \;'
	

    #echo "nodedone"
    #exit
done < nodes
