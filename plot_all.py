import subprocess
import sys
import os
from tqdm import trange, tqdm

for node in tqdm([1,12,2,3,33,4,5,6,7,8,9], position=0, leave=True, disable=False):
    try:
        os.makedirs(sys.argv[1] + str(node) + "/images/")
    except:
        pass #ignore
    days = ["2017-12-26", "2017-12-27", "2017-12-28", "2017-12-29", "2017-12-30", "2017-12-31", "2018-01-01", "2018-01-02", "2018-01-03", "2018-01-04", "2018-01-05", "2018-01-06", "2018-01-07", "2018-01-08", "2018-01-09"]
    for i in trange(1, len(days)-1, position=1, leave=True, disable=False):
        day = days[i]
        for channel in trange(1,12, position=2, leave=True, disable=False):
            process = subprocess.Popen("python plot_rssi.py " + sys.argv[1] + str(node) + "/output/ "+  day + " " + str(0) + " " + str(5) + " " +  str(channel) + " " + days[i-1] + " " + days[i+1] + " 1> /dev/null", shell=True)
            process.wait()
            #print "Done:", node, day, channel 
