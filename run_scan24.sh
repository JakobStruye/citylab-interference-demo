#!/bin/bash

# Read all the freqs to scan to one line
freqs=$(tr '\n' ' ' < freqs)

# Determine which physical interface to use, differs from deployment to deployment
ATHPATH=/sys/kernel/debug/ieee80211/phy0/ath10k
PHY="0"
if [ ! -d "$ATHPATH" ]; then
    ATHPATH=/sys/kernel/debug/ieee80211/phy1/ath10k
    PHY="1"
fi

if [ ! -d "$ATHPATH" ]; then
    echo "No ath10k interface found!"
    exit
fi

devname=wlp1s0

# Enable device and wait until enabled
until ip link set dev $devname up; do : ; done;


PREVTIME=$(date +%s%N) # Timestamp of latest scan, dummy for now
NEXT=$(date +%s%N)     # Timestamp of earliest moment to start next scan
DOFIVE=true            # Scan on 5GHz instead of 2.4GHz?
while true
do
    TOSECOND=1000000000 # date command returns microseconds
    INTERVAL=3          # Scan every INTERVAL seconds
    NOW=$(date +%s%N)

    if [ $NOW -lt $NEXT ]
    then
        # Calculate how long to wait until next scan and then wait
        sleep $(bc -l <<< $(( $NEXT - $NOW ))/$TOSECOND)
    fi
    TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S.%3N")
    NEXT=$(( $NEXT + $TOSECOND * $INTERVAL ))
    UNPARSED_COUNT=$(ls -f1 /users/jstruye/output | wc -l)
    if [ "$UNPARSED_COUNT" -gt 500 ]
    then
        echo "Too many unparsed scans, not scanning again"
        continue
    fi
    echo background > $ATHPATH/spectral_scan_ctl
    echo trigger > $ATHPATH/spectral_scan_ctl
    /sbin/iw dev $devname scan freq ${freqs} &> /dev/null
    echo disable > $ATHPATH/spectral_scan_ctl
    cat $ATHPATH/spectral_scan0 > /users/jstruye/output/$TIMESTAMP
    #echo "Output copied"
    chown -R jstruye:wal-cityofthings /users/jstruye/output/$TIMESTAMP
    NEWTIME=$(date +%s%N)
    PREVTIME=$NEWTIME
done
