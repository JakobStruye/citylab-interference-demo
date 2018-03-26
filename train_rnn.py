from shared import *

from keras.models import Sequential
from keras.layers import LSTM, GRU, Dropout, Dense
from keras.optimizers import adam
import numpy as np

import flock
from os.path import exists
from os import makedirs
import subprocess

def train_model(node, freq):

    lb = 50
    predict_step = 10
    input_shape = (1,lb)
    nodes = 50
    epochs = 20
    epochs_init = 100
    train_size = 5000
    rnn = Sequential()
    rnn_layer = GRU(nodes, input_shape=input_shape)
    rnn.add(rnn_layer)

    rnn.add(Dropout(0.5))
    rnn.add(Dense(1))
    opt = adam(lr=0.001, decay=0.0)

    rnn.compile(loss='mae', optimizer=opt)

    weights_file = weights_dir_base + node + '/' + freq + '.h5'
    if exists(weights_file):
        with open(weights_file, 'r') as w_file:
            with flock.Flock(w_file, flock.LOCK_EX) as lock:
                rnn.load_weights(weights_file)
    else:
        epochs = epochs_init

    recent_smooth_lines = subprocess.check_output(['tail', '-n' + str(train_size + predict_step), smooth_dir_base + node + "/output/" + str(freq) + ".out"])

    recent_smooths = [float(val.split(",")[1]) for val in recent_smooth_lines.split("\n")[:-1]]
    input_data = []
    output_data = []
    for i in range(train_size-lb):
        input_data.append(recent_smooths[i:i+lb])
        output_data.append(recent_smooths[i+lb+predict_step])

    input_data = np.reshape(np.array(input_data), (-1,1,lb))
    output_data = np.reshape(np.array(output_data), (-1,1))

    rnn.fit(input_data, output_data, epochs=epochs)

    if not exists(weights_dir_base + node + '/'):
        makedirs(weights_dir_base + node + '/')
    with open(weights_file, 'w') as w_file:
        with flock.Flock(w_file, flock.LOCK_EX) as lock:
            rnn.save_weights(weights_file)

if __name__ == '__main__':
    train_model("1", "2412")


