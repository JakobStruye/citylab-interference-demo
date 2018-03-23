from os import listdir, stat, makedirs
from os.path import exists
import datetime
import subprocess
from freq_channelnr_map import map_ as channels

srcdir = "/mnt/euterpe/cotShortTest/"
#srcdir = "./data/"
nodes = ["1", "14", "16", "18", "21", "23", "25", "28", "33", "35", "4", "7", "9"]
freqs = channels.values()
freqs.sort()
#freqs = freqs[:1]
#freqs = ["5220"]

for node in nodes:
    outdir = "./freq_out/" + node + "/"
    if not exists(outdir): 
        makedirs(outdir)
    thisdir = srcdir + node + "/output/"
    files = [f for f in listdir(thisdir) ]
    times = [datetime.datetime.strptime(ts, "%Y-%m-%d_%H-%M-%S.%f") for ts in files]
    times.sort()
    times = [datetime.datetime.strftime(ts, "%Y-%m-%d_%H-%M-%S.%f")[:-3] for ts in times]
    #print times
    for freq in freqs:
        ctr = 0 
        with open(outdir + freq + ".out", 'w') as f:
            for time in times:
                if (stat(thisdir + time).st_size > 400000) == (int(freq) > 4000):
                    signalstr = subprocess.check_output(
                        ['./fft_get_max_rssi.out', thisdir + time, freq])
                    f.write(str(ctr) + " " +  str(int(signalstr)) + "\n")
                    ctr += 1
    
