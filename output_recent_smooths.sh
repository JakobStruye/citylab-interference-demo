#!/bin/bash
freq=$1
#echo $freq
cd ~/smoothed/67/output/
if [ -f ${freq}.out.line ]; then
    linefrom=$(cat ${freq}.out.line)
else
    linefrom=0
fi
lineto=$(wc -l < ${freq}.out ) &&
echo ${lineto} > ${freq}.out.line
#echo $linefrom
#echo $lineto
awk "NR >= ${linefrom} && NR < ${lineto}" ${freq}.out &&
