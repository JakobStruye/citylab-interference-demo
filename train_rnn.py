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
        these_epochs = epochs
    else:
        these_epochs = epochs_init

    recent_smooth_lines = subprocess.check_output(['tail', '-n' + str(train_size + pred_step), smooth_dir_base + node + "/output/" + str(freq) + ".out"])
    recent_smooth_lines = recent_smooth_lines.decode("utf-8")

    recent_smooths = [float(val.split(",")[1]) for val in recent_smooth_lines.split("\n")[:-1]]
    input_data = []
    output_data = []
    print(train_size, pred_step, lb)
    for i in range(train_size-lb - pred_step + 1):
        input_data.append(recent_smooths[i:i+lb])
        output_data.append(recent_smooths[i+lb+pred_step])

    input_data = np.reshape(np.array(input_data), (-1,1,lb))
    output_data = np.reshape(np.array(output_data), (-1,1))
    print(input_data.shape)

    input_data = normalize(input_data)
    output_data = normalize(output_data)
    rnn.fit(input_data, output_data, epochs=these_epochs)
    out = rnn.predict(input_data)
    print(np.min(output_data), np.max(output_data))

    print(np.min(out), np.max(out))

    if not exists(weights_dir_base + node + '/'):
        makedirs(weights_dir_base + node + '/')
    with open(weights_file, 'w') as w_file:
        with flock.Flock(w_file, flock.LOCK_EX) as lock:
            rnn.save_weights(weights_file)

if __name__ == '__main__':
    train_model("1", "5220")


