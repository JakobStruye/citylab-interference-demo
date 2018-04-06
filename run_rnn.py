from shared import *

from keras.models import Sequential
from keras.layers import LSTM, GRU, Dropout, Dense
from keras.optimizers import adam
import numpy as np

import flock
from os.path import exists
from os import makedirs
import subprocess

def run_model(node, freq):


    rnn = Sequential()
    rnn_layer = GRU(units, input_shape=input_shape)
    rnn.add(rnn_layer)

    rnn.add(Dropout(0.5))
    rnn.add(Dense(1))
    opt = adam(lr=0.001, decay=0.0)

    rnn.compile(loss='mse', optimizer=opt)

    weights_file = weights_dir_base + node + '/' + freq + '.h5'
    if exists(weights_file):
        with open(weights_file, 'r') as w_file:
            with flock.Flock(w_file, flock.LOCK_EX) as lock:
                rnn.load_weights(weights_file)
    else:
        print("No weights yet!")
        exit(0)


    if not exists(predict_dir_base + node + '/'):
        makedirs(predict_dir_base + node + '/')

    predict_file = predict_dir_base + node + '/' + freq + '.out'
    if exists(predict_file):
        predict_latest_time = subprocess.check_output(['tail', '-1', predict_file]).decode('utf-8').split(",")[0]
    else:
        predict_latest_time = None

    smooth_file = smooth_dir_base + node + '/' + freq + '.out'

    if predict_latest_time:
        start_line = subprocess.check_output(
            ['grep', '-n', predict_latest_time, smooth_file])
        start_line = int(start_line.split(" ")[0]) - lb + 1
    else:
        start_line = 0



    smooth_lines = subprocess.check_output(['tail', '-n', '+' + str(start_line), smooth_dir_base + node + "/output/" + str(freq) + ".out"])
    smooth_lines = smooth_lines.decode("utf-8")
    smooth_lines = smooth_lines.split("\n")
    input_smooth_lines = [float(val.split(",")[1]) for val in smooth_lines[:-1]]
    print(len(input_smooth_lines))
    timestamps = [val.split(",")[0] for val in smooth_lines[lb - 1:-1]]


    #recent_smooths = [float(val.split(",")[1]) for val in recent_smooth_lines.split("\n")[:-1]]
    input_data = []
    #output_data = []
    for i in range(len(input_smooth_lines) - lb + 1):
        input_data.append(input_smooth_lines[i:i+lb])
        #output_data.append(recent_smooths[i+lb+predict_step])

    input_data = np.reshape(np.array(input_data), (-1,1, lb))
    input_data = normalize(input_data)
    #output_data = np.reshape(np.array(output_data), (-1,1))

    results = rnn.predict(input_data)
    results = denormalize(results)
    print(results)
    results = np.reshape(results, (-1))
    print(results.shape[0])
    print(len(timestamps))
    assert results.shape[0] == len(timestamps)
    with open(predict_file, 'a+') as f:

        for i in range(results.shape[0]):
            f.write(timestamps[i] + "," + str(results[i]) + '\n')


    # if not exists(weights_dir_base + node + '/'):
    #     makedirs(weights_dir_base + node + '/')
    # with open(weights_file, 'w') as w_file:
    #     with flock.Flock(w_file, flock.LOCK_EX) as lock:
    #         rnn.save_weights(weights_file)

if __name__ == '__main__':
    run_model("1", "5220")


