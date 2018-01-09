import subprocess
import sys

for node in [1,12,2,3,33,4,5,6,7,8,9]:
    for day in ["2017-12-26", "2017-12-27", "2017-12-28", "2017-12-29", "2017-12-30", "2017-12-31", "2018-01-01"]:
        for channel in range(1,13):
            process = subprocess.Popen("python plot_rssi.py " + sys.argv[1] + " " + str(node) + "/output/ "+  day + " " + str(0) + " " + str(5) + " " +  str(channel), shell=True)
            process.wait()
            print "Done:", node, day, channel
