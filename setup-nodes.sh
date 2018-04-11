#!/bin/bash

for node in 1 2 4 5 8 9 10 13 12 15 18 19 20 22 24 26 28 33 34 35 
do
  ssh -o StrictHostKeyChecking=no  jstruye@node${node}.lab.cityofthings.eu "mkdir output && git clone https://github.com/jakobstruye/citylab-interference-demo.git && cd citylab-interference-demo && git checkout parse_on_node && make && (nohup sudo ./run_scan24.sh &> outscan & disown) && sleep 1 && (nohup python parse_running.py &> outparse & disown) && echo 'done' "
  echo "done"
done
