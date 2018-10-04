#!/bin/bash
cd /home/jstruye/citylab-interference-demo
mkdir -p ../smoothed/
while true
do


    #echo $node
    #while read -u 10 node;
    #do
    node="74"
    freq="2437"
        mkdir -p ../smoothed/${node}/
        #echo $freq
        sleep 1
        echo "RUNNING"
        ssh -o StrictHostKeyChecking=no  jstruye@node${node}.lab.cityofthings.eu "./citylab-interference-demo/output_recent_smooths.sh ${freq}" | grep ',' >> ../smoothed/${node}/${freq}.out
	
    #done 10< nodes
    #echo "nodedone"
    #exit

echo "RAN"
done
