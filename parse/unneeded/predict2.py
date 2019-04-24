import subprocess
import matplotlib.pyplot as plt
from keras.layers.recurrent import GRU
from keras.layers import Dense, Dropout
from keras.models import Sequential
import numpy as np
from sys import argv
from math import floor, log, exp
from os import makedirs
from os.path import exists
import flock
node = argv[1]
freq = argv[2]
nodefreq = node + "-" + freq

movavg=-999
alpha=1.0
group = 30
w=1
hor = 10
window = 20
lb = window

def normalize(arr):
    minval = 0
    maxval = 6
    range = maxval - minval
    print(arr.shape)
    for v in arr:
        for v2 in v:
          for v3 in v2:
            if v3 == 0:
                print("HERE", v3)
    arr = np.log(-arr)
    return (arr - minval) * 2 / (range) - 1

def denormalize(arr):
    minval = 0
    maxval = 6
    range = maxval - minval
    result = (arr + 1) * range / 2 + minval
    return -1 * np.exp(result)
    #return result
predict_dir_base = "thepredicts/"
if not exists(predict_dir_base + node + '/'):
    makedirs(predict_dir_base + node + '/')

predict_file = predict_dir_base + node + '/' + freq + '.out'
if exists(predict_file):
    predict_latest_time = subprocess.check_output(['tail', '-1', predict_file]).decode('utf-8').split(",")[0]
else:
    predict_latest_time = None

smooth_dir_base = "../../outs/"
smooth_file = smooth_dir_base + node + '/' + freq + '.out'

if predict_latest_time:
    start_line = subprocess.check_output(
        ['grep', '-n', predict_latest_time, smooth_file]).decode('utf-8')
    start_line = int(start_line.split(":")[0]) - lb + 1
else:
    start_line = 0



smooth_lines = subprocess.check_output(['tail', '-n', '+' + str(start_line), smooth_dir_base + node + "/" + str(freq) + ".out"])
smooth_lines = smooth_lines.decode("utf-8")
smooth_lines = smooth_lines.split("\n")
input_smooth_lines = []
for line in smooth_lines[:-1]:
    splits = line.split(",")
    if len(splits) == 2:
        try:
            input_smooth_lines.append(float(splits[1]))
        except:
            pass


#input_smooth_lines = [float(val.split(",")[1]) for val in smooth_lines[:-1]]
print("smooth lines len", len(input_smooth_lines))


#recent_smooths = [float(val.split(",")[1]) for val in recent_smooth_lines.split("\n")[:-1]]
#input_data = []
#output_data = []
#for i in range(len(input_smooth_lines) - lb + 1):
#    input_data.append(input_smooth_lines[i:i+lb])
#    #output_data.append(recent_smooths[i+lb+predict_step])

#input_data = np.reshape(np.array(input_data), (-1,1, lb))
#input_data = normalize(input_data)
#output_data = np.reshape(np.array(output_data), (-1,1))

#results = rnn.predict(input_data)
#results = denormalize(results)
#print(results)
#results = np.reshape(results, (-1))
#print(results.shape[0])
#print(len(timestamps))
#assert results.shape[0] == len(timestamps)







vals = input_smooth_lines
#vals = [int(val.split(","[1]) for val in f.readlines()]
length = int(len(vals) / group)
vals = vals[:length*group]
vals = np.array(vals)
vals[vals > 0] = -999
vals = np.reshape(vals, (length, group))
#vals = np.max(vals, axis=1)
vals = np.percentile(vals, 95, axis=1)

#with open("parsed/" + nodefreq + "-time", "r") as f:
#    time = [int(val) for val in f.readlines()]
#    time = time[w-1:length*group]
#    time = np.array(time)
#    length -= w-1
#    time = np.reshape(time, (length, group))
#    time = np.max(time, axis=1)

#stamp = time[0]
#millis = 24*60*60*1000
#stamp = floor(stamp / millis) * millis
#while stamp < time[-1]:
#    stamp += millis
#    plt.axvline(stamp, color="red")


movingwindow = []
outs = []
for i in range(vals.shape[0] - hor - window):
    movingwindow.extend(vals[i:i+window])
    outs.append(vals[i+window+hor])
movingwindow = np.reshape(np.array(movingwindow), (-1,1,window))
timestamps = [val.split(",")[0] for val in smooth_lines[lb - 1:-1]]
#outs = np.reshape(np.array(outs), (-1,1))
movingwindow = normalize(movingwindow)
#outs = normalize(outs)
model = Sequential()
model.add(GRU(5,input_shape=(1, window)))
#model.add(Dropout(0.5))
model.add(Dense(1))
#model.compile(loss='mse', optimizer='adam')
#print("Total size:", movingwindow.shape[0])


weights_dir_base = "./weights/"
weights_file = weights_dir_base + node + '/' + freq + '.h5'
if exists(weights_file):
    with open(weights_file, 'r') as w_file:
        #with flock.Flock(w_file, flock.LOCK_EX) as lock:
        model.load_weights(weights_file)
else:
    print("No weights yet!")
    exit(0)


preds = model.predict(movingwindow)
#outs = denormalize(outs)
preds = denormalize(preds)
with open(predict_file, 'a+') as f:
    for i in range(preds.shape[0]):
        f.write(timestamps[i] + "," + str(preds[i][0]) + '\n')
#plt.plot(outs)
#plt.plot(preds)
#plt.savefig("predicts_mse/" + nodefreq + ".png")
