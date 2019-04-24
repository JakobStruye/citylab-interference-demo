#!/bin/bash

nodes=$(cat nodes)
freqs="2412 2437 2462 5180 5200 5220 5240"
for node in $nodes
do
	for freq in $freqs
	do
		#./a.out $node $freq time > parsed/$node-$freq-time
		#./a.out $node $freq vals 95 > parsed/$node-$freq
		./a.out $node $freq both 95 > parsed2/$node-$freq
	done
done

