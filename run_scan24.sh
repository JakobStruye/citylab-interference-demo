#!/bin/bash

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
CURPHY="/home/jstruye/AdvNetwLab/phy"
PHYSWAP="/home/jstruye/AdvNetwLab/physwap"

ATHPATH=/sys/kernel/debug/ieee80211/phy0/ath10k
PHY="0"
if [ ! -d "$ATHPATH" ]; then
    ATHPATH=/sys/kernel/debug/ieee80211/phy1/ath10k
    PHY="1"
fi
echo $PHY

if [ -e $CURPHY ]
then
    PREVPHY=$(cat $CURPHY)
else
    PREVPHY=$PHY
fi

if [ $PHY != $PREVPHY ]
then
    date >> $PHYSWAP
fi
echo $PHY > $CURPHY

devname=wlp1s0

echo "Resetting $devname"
ip link set dev $devname down
ip link set dev $devname up
echo "Reset $devname"
echo background > $ATHPATH/spectral_scan_ctl
echo trigger > $ATHPATH/spectral_scan_ctl
echo "Set pre-scan values; scanning..."
/sbin/iw dev $devname scan freq 2412 2417 2422 2427 2432 2437 2442 2447 2452 2457 2462 #Will probably fail
echo "Scan 1 complete"
/sbin/iw dev $devname scan freq 2412 2417 2422 2427 2432 2437 2442 2447 2452 2457 2462 #Will probably work
echo "Scan 2 complete"
echo disable > $ATHPATH/spectral_scan_ctl
echo "Spectral scan disabled"
cat $ATHPATH/spectral_scan0 > /home/jstruye/output/$TIMESTAMP
echo "Output copied"
chown -R jstruye:jstruye /home/jstruye/output
