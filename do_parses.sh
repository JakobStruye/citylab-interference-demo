#!/bin/bash
# for i in 1 2 3 4 5 6 7 8 9 10 11; do
#     echo -n "$i & " >> parsed_channels.txt
#     python parse.py 2 Lab_2/traces/text_traces/L2-3-1.$i.txt parsed_channels.txt
#   done
for i in 36 40; do
    echo -n "$i & " >> parsed_channels2.txt
    python parse.py 2 Lab_2/traces/text_traces/L2-4-1.$i.txt parsed_channels2.txt
  done
