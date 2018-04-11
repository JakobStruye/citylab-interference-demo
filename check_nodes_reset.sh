#!/bin/bash
mkdir -p ../smoothed/
while read node;
do
    ssh -o StrictHostKeyChecking=no  jstruye@node${node}.lab.cityofthings.eu 'ls citylab-interference-demo'
	

    #echo "nodedone"
    #exit
done < nodes
