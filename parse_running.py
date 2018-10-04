from os import listdir, stat, makedirs, remove
from os.path import exists
import datetime
import subprocess
#import numpy as np
from shared import *
from platform import uname
from time import sleep

#freqs = channels.values()
while True:
    #sleep(1)
    freqs.sort()
    #freqs = freqs[:1]

    nodes = [uname()[1].split(".")[0][4:]]
    for node in nodes:
        raw_parse = raw_parse_dir_base + node + "/"
        if not exists(raw_parse):
            makedirs(raw_parse)
        dump_dir = dump_dir_base# + node + "/output/"
        smooth_dir = smooth_dir_base + node + "/output/"
        if not exists(smooth_dir):
            makedirs(smooth_dir)

        files = [f for f in listdir(dump_dir)]
        times = [datetime.datetime.strptime(ts, "%Y-%m-%d_%H-%M-%S.%f") for ts in files]

        #if len(times) < 120:
        #    #wait a while
        #    break

        times.sort()
        times = [datetime.datetime.strftime(ts, "%Y-%m-%d_%H-%M-%S.%f")[:-3] for ts in times]
        #times = times[:1200]
        for freq in freqs:
            print(freq)
            these_times = []
            raw_vals = []
            with open(raw_parse + freq + ".out", 'a') as f:
                for time in times:
                    if (stat(dump_dir + time).st_size > 400000) == (int(freq) > 4000):
                        signalstr = subprocess.check_output(
                            [basedir + 'citylab-interference-demo/fft_get_max_rssi.out', dump_dir + time, freq])
                        val = int(signalstr)
                        if val == 0:
                            continue
                        f.write(time + "," + str(val) +  "\n")
                        raw_vals.append(val)
                        these_times.append(time)

            smooth_file = smooth_dir + freq + ".out"
            if exists(smooth_file) and stat(smooth_file).st_size > 0:
                try:
                    smooth_val = float(subprocess.check_output(['tail', '-1', smooth_file]).split(",")[1])
                except:
                    smooth_val = float(subprocess.check_output(['tail', '-2', smooth_file]).split("\n")[0].split(",")[1].strip())

            else:
                #smooth_val = sum(raw_vals[:100]) / 100.0#np.mean(raw_vals[:100])
                smooth_val = -80.0
            with open(smooth_file, 'a+') as smooth_f:
                smooth_vals = []
                prev_val = smooth_val
                for i in range(len(raw_vals)):
                    #print "writing"
                    val = prev_val * 0.90 + raw_vals[i] * 0.1
                    smooth_vals.append(val)
                    smooth_f.write(these_times[i] + "," + str(val) + "\n")
                    prev_val = val


        for time in times:
            remove(dump_dir + time)

