import subprocess
import time
import matplotlib.pyplot as plt
from keras.layers.recurrent import GRU
from keras.layers import Dense, Dropout
from keras.models import Sequential
import keras.backend as K
import numpy as np
from sys import argv
from math import floor, log, exp
from os import makedirs
from os.path import exists
import flock
from earlystop import EarlyStop


movavg=-999
alpha=1.0
group = 30
hor = 10*30
window = 30*30
w=1

model = Sequential()
model.add(GRU(5,input_shape=(1, window)))
#model.add(Dropout(0.5))
model.add(Dense(1))
model.compile(loss='mse', optimizer='adam')
model.save_weights("init.h5")
learn = False #True to create weights, False to use them

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

argctr = 0

while (len(argv) >= argctr + 2):
    #K.clear_session()
    model.load_weights("init.h5")
    loopstart = time.time()
    node = argv[argctr+1]
    freq = argv[argctr+2]
    nodefreq = node + "/" + freq
    argctr+= 2
    print("node", node, "freq", freq)

    times = []
    if exists("thepredicts/" + node + "/" + freq + ".out"):
        last_predict = subprocess.check_output(['tail', '-1', 'thepredicts/' + node + '/' + freq + ".out"]).decode("utf-8").split(",")[0]
    else:
        last_predict = -99999
    try:
        read_from = subprocess.check_output(['grep', '-n', last_predict, '/home/jstruye/outs/verysmooth/' + nodefreq + ".out"]).decode("utf-8").split(":")[0]
        read_from = int(read_from)
    except:
        read_from = window
    read_from -= window - 1
    if learn:
        read_from = 0
    print(read_from)
    loopmid = time.time()

    #with open("/home/jstruye/outs/verysmooth/" +  nodefreq + ".out", "r") as f:
    if True:
        #lines = f.readlines()[read_from:]
        lines = subprocess.check_output(["tail", "-n+"+str(read_from), "/home/jstruye/outs/verysmooth/"+nodefreq+".out"]).decode("utf-8").split("\n")[:-1]
        if len(lines) > 100000 and learn:
            lines = lines[-100000:]
        loopend = time.time()
        print(lines[0].split(","))
        vals = [float(val.split(",")[1].strip()) for val in lines]
        times = [int(val.split(",")[0].strip()) for val in lines]

        #length = int(len(vals) / group)
        #vals = vals[:length*group]
        vals = np.array(vals)
        #vals[vals > 0] = -999
        #vals = np.reshape(vals, (length, group))
        #vals = np.max(vals, axis=1)
        #vals = np.percentile(vals, 95, axis=1)
        newvals = []
        for val in vals:
            movavg = movavg * (1. - alpha) + val * alpha if movavg > -999 else val

            newvals.append(movavg)
        newvals = np.array(newvals)
        vals = newvals
        vals = np.convolve(vals, np.ones(w), 'valid') / w
        print(vals.shape)

    #with open("parsed/" + nodefreq + "-time", "r") as f:
    #    time = [int(val) for val in f.readlines()]
    #    #time = time[w-1:length*group]
    #    time = np.array(time)
    #    length -= w-1
    #    #time = np.reshape(time, (length, group))
    #    #time = np.max(time, axis=1)

    #stamp = time[0]
    #millis = 24*60*60*1000
    #stamp = floor(stamp / millis) * millis
    #while stamp < time[-1]:
    #    stamp += millis
    #    plt.axvline(stamp, color="red")


    movingwindow = []
    outs = []
    limit = 0 if not learn else hor
    for i in range(vals.shape[0] - window - limit):
        if (i % 1000 == 0): print(i)
        movingwindow.extend(vals[i:i+window])
        if learn:
            outs.append(vals[i+window+hor])
    movingwindow = np.reshape(np.array(movingwindow), (-1,1,window))
    print("reshaped")
    outs = np.reshape(np.array(outs), (-1,1))
    print("reshaped")
    movingwindow = normalize(movingwindow)
    print("normalized")
    outs = normalize(outs)
    preshaped = time.time()
    print("normalized")
    print("Total size:", movingwindow.shape[0])
    if movingwindow.shape[0] == 0:
        #nothing to do
        continue
    reshaped = time.time()

    weights_dir_base = "./weights/"
    weights_file = weights_dir_base + node + '/' + freq + '.h5'
    if learn:
        callbacks = [EarlyStop(threshold=0.0001, min_epochs=0, verbose=1)]
        model.fit(movingwindow[:500000,:,:], outs[:500000,:], epochs=1 if int(freq)>5000 else 1, callbacks=callbacks)

        if not exists(weights_dir_base + node + '/'):
            makedirs(weights_dir_base + node + '/')
        with open(weights_file, 'w') as w_file:
            #with flock.Flock(w_file, flock.LOCK_EX) as lock:
            model.save_weights(weights_file)
    else:
        start = time.time()
        model.load_weights(weights_file)
        mid = time.time()
        print("loaded")
        preds = model.predict(movingwindow)
        done = time.time()
        print("readingi1", (loopmid-loopstart), "reading2", (loopend-loopmid), "loadtime", (mid-start), "predicttime", (done-mid))
        print("shapetime", (reshaped-preshaped))
        #outs = denormalize(outs)
        preds = denormalize(preds)
        print(len(times))
        print(len(preds))
        assert len(times) - window == len(preds)
        preds_dir = "./thepredicts/" + node
        if not exists(preds_dir):
            makedirs(preds_dir)
        with open(preds_dir + "/" + freq + ".out", "a") as f:
            for i in range(window, len(times)):
                f.write(str(times[i]) +  "," + str(preds[i-window][0]) + "\n")

        #plt.plot(outs)
        #plt.plot(preds)
        #plt.savefig("predicts_final/" + node + "-" + freq + ".png")
