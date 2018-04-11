#!/bin/bash
mkdir -p ../smoothed/
while read -u 5 node;
do
    ssh -o StrictHostKeyChecking=no  jstruye@node${node}.lab.cityofthings.eu 'cd citylab-interference-demo && git pull'
	

    #echo "nodedone"
    #exit
done 5< nodes
