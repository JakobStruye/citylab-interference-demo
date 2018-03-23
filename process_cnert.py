from os import listdir, stat

import datetime
import subprocess


srcdir = "/mnt/euterpe/cotShortTest/1/output/"

files = [f for f in listdir(srcdir) ]
times = [datetime.datetime.strptime(ts, "%Y-%m-%d_%H-%M-%S.%f") for ts in files]
times.sort()
times = [datetime.datetime.strftime(ts, "%Y-%m-%d_%H-%M-%S.%f")[:-3] for ts in times]
#print times

ctr = 0 
for time in times:
    if stat(srcdir + time).st_size > 400000:
        signalstr = subprocess.check_output(
            ['./fft_get_max_rssi.out', srcdir + time, '5220'])
        print str(ctr) + " " +  str(int(signalstr))
        ctr += 1
    
