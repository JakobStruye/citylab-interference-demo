import matplotlib.pyplot as plt
import numpy as np
from sys import argv
from math import floor
node = argv[1]
freq = argv[2]
nodefreq = node + "-" + freq

movavg=-999
alpha=1.0
group = 30
w=1
with open(nodefreq, "r") as f:
    vals = [int(val) for val in f.readlines()]
    length = int(len(vals) / group)
    vals = vals[:length*group]
    vals = np.array(vals)
    vals[vals > 0] = -999
    vals = np.reshape(vals, (length, group))
    #vals = np.max(vals, axis=1)
    vals = np.percentile(vals, 95, axis=1)
    newvals = []
    for val in vals:
        movavg = movavg * (1. - alpha) + val * alpha if movavg > -999 else val
        
        newvals.append(movavg)
    newvals = np.array(newvals)
    vals = newvals
    vals = np.convolve(vals, np.ones(w), 'valid') / w
    print(vals.shape)

with open(nodefreq + "-time", "r") as f:
    time = [int(val) for val in f.readlines()]
    time = time[w-1:length*group]
    time = np.array(time)
    length -= w-1
    time = np.reshape(time, (length, group))
    time = np.max(time, axis=1)

stamp = time[0]
millis = 24*60*60*1000
stamp = floor(stamp / millis) * millis
while stamp < time[-1]:
    stamp += millis
    plt.axvline(stamp, color="red")
#plt.xlim(left=1.5538 * 10**12, right=1.5539*10**12)
plt.plot(time, vals)#, 'o', markersize=0.2)
#plt.savefig("images2/"+nodefreq+".png")
plt.show()
