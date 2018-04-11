#!/bin/bash
cd /home/jstruye/citylab-interference-demo
mkdir -p ../smoothed/
while true
do
while read -u 5 freq;
do
    #echo $node
    while read -u 10 node;
    do
        mkdir -p ../smoothed/${node}/
        #echo $freq
        (nohup ssh -o StrictHostKeyChecking=no  jstruye@node${node}.lab.cityofthings.eu "./citylab-interference-demo/output_recent_smooths.sh ${freq}" | grep ',' >> ../smoothed/${node}/${freq}.out &)
	
    done 10< nodes
    #echo "nodedone"
    #exit
done 5< freqs
sleep 10
done
