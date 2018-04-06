from os import listdir, stat, makedirs, remove
from os.path import exists
import datetime
import subprocess
import numpy as np
from shutil import move
from shared import *

length = 5000

def build_graph(node, freq):
    smooth_file = smooth_dir_base + node + '/output/' + freq + '.out'
    predict_file = smooth_dir_base + node + '/output/' + freq + '.out'

    recent_predicts = subprocess.check_output(['tail', '-n' + str(length), predict_file ]).decode("utf-8").split("\n")[:-1]
    predict_latest_time = recent_predicts[-1].split(",")[0]
    preds = [float(val.split(",")[1]) for val in recent_predicts]
    stop_line = subprocess.check_output(
        ['grep', '-n', predict_latest_time, smooth_file]).decode("utf-8")
    stop_line = int(stop_line.split(":")[0]) - lb + 1
    ps = subprocess.Popen(('head', '-n' + str(stop_line), smooth_file), stdout=subprocess.PIPE)

    recent_smooths = subprocess.check_output(["tail", '-n', str(length - pred_step + 1)], stdin=ps.stdout).decode("utf-8").split("\n")[:-1]
    ps.wait()
    smooths = [float(val.split(",")[1]) for val in recent_smooths]

    with open("graph_data_temp.js", "w") as f:
        f.write("graph_data = [\n")
        f.write("['a',    'b',   'c',   'd'],\n")
        for i in range(len(preds)):
            #if i % interval:
            #    continue
            pred_bot = preds[i] - 5 +  16 * (i / len(preds))
            pred_top = preds[i] + 5 +  16 * (i / len(preds))
            actual = smooths[i] +  16 * (i / len(preds)) if i < len(smooths)  else '"__"'
            f.write("['" + str(i) + "', " + str(pred_top) + ", " + str(actual) + ", " + str(pred_bot - pred_top) + "],\n")
        f.write("]\n")
    move("graph_data_temp.js", "graph_data.js")
if __name__ == '__main__':
    build_graph("1", "5220")