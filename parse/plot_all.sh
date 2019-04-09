#!/bin/bash

nodes=$(cat /mnt/hgfs/host/nodes)
freqs="2412 2437 2462 5180 5200 5220 5240"
for node in $nodes
do
	for freq in $freqs
	do
		python3 plot.py $node $freq
	done
done

