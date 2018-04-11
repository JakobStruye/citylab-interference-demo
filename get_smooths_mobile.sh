#!/bin/bash
cd /home/jstruye/citylab-interference-demo
mkdir -p ../smoothed/
while true
do
    node="67"
    echo $node
    mkdir -p ../smoothed/${node}/
    while read -u 10 freq;
    do
        echo $freq
        (nohup ssh -o StrictHostKeyChecking=no  -p 2210 citylab-user@localhost "./citylab-interference-demo/output_recent_smooths.sh ${freq}" | grep ',' >> ../smoothed/${node}/${freq}.out &)
	
    done 10< freqs
    #echo "nodedone"
    #exit
sleep 10
done
