import matplotlib.pyplot as plt
from keras.layers.recurrent import GRU
from keras.layers import Dense, Dropout
from keras.models import Sequential
import numpy as np
from sys import argv
from math import floor, log, exp
node = argv[1]
freq = argv[2]
nodefreq = node + "-" + freq

movavg=-999
alpha=1.0
group = 30
w=1

def normalize(arr):
    minval = 0
    maxval = 6
    range = maxval - minval
    arr = np.log(-arr)
    return (arr - minval) * 2 / (range) - 1

def denormalize(arr):
    minval = 0
    maxval = 6
    range = maxval - minval
    result = (arr + 1) * range / 2 + minval
    return -1 * np.exp(result)
    #return result
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
#    plt.axvline(stamp, color="red")


movingwindow = []
outs = []
hor = 10
window = 20
for i in range(vals.shape[0] - hor - window):
    movingwindow.extend(vals[i:i+window])
    outs.append(vals[i+window+hor])
movingwindow = np.reshape(np.array(movingwindow), (-1,1,window))
outs = np.reshape(np.array(outs), (-1,1))
movingwindow = normalize(movingwindow)
outs = normalize(outs)
model = Sequential()
model.add(GRU(5,input_shape=(1, window)))
#model.add(Dropout(0.5))
model.add(Dense(1))
model.compile(loss='mse', optimizer='adam')
print("Total size:", movingwindow.shape[0])
model.fit(movingwindow[:12000,:,:], outs[:12000,:], epochs=5)
preds = model.predict(movingwindow)
outs = denormalize(outs)
preds = denormalize(preds)
plt.plot(outs)
plt.plot(preds)
plt.savefig("predicts_mse/" + nodefreq + ".png")
