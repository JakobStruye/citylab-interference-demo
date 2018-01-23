#!/bin/bash
#if [ $(ps aux | grep run_scan | wc -l) -gt 4 ]; then
#    exit
#fi

#CURPHY="/users/jstruye/advnetwlab/phy"
#PHYSWAP="/users/jstruye/advnetwlab/physwap"

ATHPATH=/sys/kernel/debug/ieee80211/phy0/ath10k
PHY="0"
if [ ! -d "$ATHPATH" ]; then
    ATHPATH=/sys/kernel/debug/ieee80211/phy1/ath10k
    PHY="1"
fi

#if [ ! -d "$ATHPATH" ]; then
    #Chip down
#    reboot
#fi

#echo $PHY

#if [ -e $CURPHY ]
#then
#    PREVPHY=$(cat $CURPHY)
#else
#    PREVPHY=$PHY
#fi

#if [ $PHY != $PREVPHY ]
#then
#    date >> $PHYSWAP
#fi
#echo $PHY > $CURPHY

devname=wlp1s0

#echo "Resetting $devname"
#ip link set dev $devname down
until ip link set dev $devname up; do : ; done;

#echo "Reset $devname"
PREVTIME=$(date +%s%N)
NEXT=$(date +%s%N)
while true
do
    TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S.%3N")
    NOW=$(date +%s%N)
    
    if [ $NOW -lt $NEXT ]
    then
        sleep $(bc -l <<< $(( $NEXT - $NOW ))/1000000000)
    fi
    NEXT=$(( $NEXT + 100000000 ))
    echo background > $ATHPATH/spectral_scan_ctl
    echo trigger > $ATHPATH/spectral_scan_ctl
    #echo "Set pre-scan values; scanning..."
    #/sbin/iw dev $devname scan freq 2412 2417 2422 2427 2432 2437 2442 2447 2452 2457 2462 & kill $! #Will probably fail
    #echo "Scan 1 complete"
    /sbin/iw dev $devname scan freq 2412 &> /dev/null #2417 2422 2427 2432 2437 2442 2447 2452 2457 2462 #Will probably work
    #echo "Scan 2 complete"
    echo disable > $ATHPATH/spectral_scan_ctl
    #echo "Spectral scan disabled"
    cat $ATHPATH/spectral_scan0 > /users/jstruye/output/$TIMESTAMP
    #echo "Output copied"
    chown -R jstruye:wal-cityofthings /users/jstruye/output/$TIMESTAMP
    NEWTIME=$(date +%s%N)
    #sleep $(bc -l <<< $(( 100000000 - $(( $(date +%s%N) - $PREVTIME )) ))/1000000000) &> /dev/null
    PREVTIME=$NEWTIME
done

