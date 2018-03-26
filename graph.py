from shared import *
import matplotlib.pyplot as plt
import numpy as np
import random
import subprocess

graph_predict_range = 120
graph_smoothed_range = 60

def get_latest_predictions(node, freq):
    recent_preds_lines = subprocess.check_output(['tail', '-n' + str(graph_predict_range), predict_dir_base + node + "/output/" + str(freq) + ".out"])
    recent_preds = [float(val.split(",")[1]) for val in recent_preds_lines]
    smooth_start_timestamp = recent_preds_lines[0].split(",")[0]
    smooth_stop_timestamp = recent_preds_lines[graph_smoothed_range-1].split(",")[0]
    return (smooth_start_timestamp, smooth_stop_timestamp, recent_preds)


def get_latest_smoothings(node, freq, smooth_start_timestamp, smooth_stop_timestamp):
    start_line = subprocess.check_output(
        ['grep', '-n', smooth_start_timestamp, smooth_dir_base + node + "/output/" + str(freq) + ".out"])
    start_line = int(start_line.split(" ")[0])
    recent_smooths_lines = subprocess.check_output(
        ['head', '-n' + str(start_line + graph_predict_range), predict_dir_base + node + "/output/" + str(freq) + ".out", "|", "tail", "-n" + str(graph_predict_range)])
    recent_smooths = [float(val.split(",")[1]) for val in recent_smooths_lines]
    if recent_smooths_lines[-1].split(",")[0] != smooth_stop_timestamp:
        print("Final line of smoothed data not at expected timestamp!")


def plot_data(predictions, smoothings):
    t = np.arange(graph_predict_range)


    #t_arr = np.array(t)
    #actual_len = 60
    #actual_tail_len = 5
    #actual_lim = np.array(actual[:actual_len+1])
    #actual_tail = np.array(actual[actual_len:actual_len+actual_tail_len])

    t_smooth = t[:graph_predict_range]

    smoothings = np.array(smoothings)
    predictions = np.array(predictions)

    # plot it!
    fig, ax = plt.subplots(1, figsize=(4,6))
    #ax.plot(t, mu1, lw=2, label='mean population 1', color='blue')
    ax.plot(t_smooth, smoothings, lw=2, label='mean population 2', color='orange')
    ax.fill_between(t, predictions+2.5, predictions-2.5, facecolor='blue', alpha=0.35)
    #ax.fill_between(t, mu2+sigma2, mu2-sigma2, facecolor='yellow', alpha=0.5)
    #plt.ylim([-41,-20])
    #plt.xlim([15,85])
    plt.tight_layout()
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off') # labels along the bottom edge are off
    #ax.set_title('Predicted and measured signal strength')
    #ax.legend(loc='upper left')
    ax.set_xlabel('Time (minutes)')
    ax.set_ylabel('Signal Strength (dBm)')
    ax.grid()

    plt.show(block=True)
