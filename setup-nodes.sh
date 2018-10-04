#!/bin/bash

for node in 12 16 21 22 23 24 25 27 28
do
  ssh -o StrictHostKeyChecking=no  jstruye@node${node}.lab.cityofthings.eu "mkdir output && git clone https://github.com/jakobstruye/citylab-interference-demo.git && cd citylab-interference-demo && git checkout parse_on_node && make && (nohup sudo ./run_scan24.sh &> outscan & disown) && sleep 1 && (nohup python parse_running.py &> outparse & disown) && echo 'done' "
  echo "done"
done
