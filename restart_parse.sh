#!/bin/bash
while read -u 5 node;
do
    echo ${node}
    ssh -o StrictHostKeyChecking=no  jstruye@node${node}.lab.cityofthings.eu 'killall python && cd citylab-interference-demo && (nohup python parse_running.py & disown)' &
	
    sleep 1
    #echo "nodedone"
    #exit
done 5< nodes
