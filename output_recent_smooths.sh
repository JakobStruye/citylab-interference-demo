#!/bin/bash
freq=$1
#echo $freq
cd ~/smoothed/
if [ -f ${freq}.out.line ]; then
    linefrom=$(cat ${freq}.out.line)
else
    linefrom=0
fi
lineto=$(wc -l < ${freq}.out ) &&
#echo $linefrom
#echo $lineto
echo ${lineto} > ${freq}.out.line
awk "NR >= ${linefrom} && NR < ${lineto}" ${freq}.out
