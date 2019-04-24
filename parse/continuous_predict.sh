#!/bin/bash

nodes=$(cat nodes)
freqs="2412 2437 2462 5180 5200 5220 5240"
arglist=""

for node in $nodes
do
	for freq in $freqs
	do
		arglist=$arglist" "$node" "$freq
		#python3 learn2.py $node $freq
	done
done
arglist=$arglist" 51 2412 51 2437 51 2462"
#echo $arglist
while true;
do
	echo "Running for "$arglist
	python3 learn2.py $arglist
	echo "Sleeping!"
	sleep 1
	echo "Slept!"
done
