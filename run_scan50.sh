#!/bin/bash

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")

ATHPATH=/sys/kernel/debug/ieee80211/phy1/ath10k
echo "Resetting wls6"
ip link set dev wls6 down
ip link set dev wls6 up
echo "Reset wls6"
echo background > $ATHPATH/spectral_scan_ctl
echo trigger > $ATHPATH/spectral_scan_ctl
echo "Set pre-scan values; scanning..."
/sbin/iw dev wls6 scan freq 5180 5200 5220 5240 5260 5280 5300 5320 5500 5520 5540 5560 5580 5600 5620 5640 5660 5680 5700 #Will probably fail
echo "Scan 1 complete"
/sbin/iw dev wls6 scan freq 5180 5200 5220 5240 5260 5280 5300 5320 5500 5520 5540 5560 5580 5600 5620 5640 5660 5680 5700 #Will probably work
echo "Scan 2 complete"
echo disable > $ATHPATH/spectral_scan_ctl
echo "Spectral scan disabled"
cat $ATHPATH/spectral_scan0 > /root/output/$TIMESTAMP
echo "Output copied"

