from shared import *
import subprocess
import operator
import random
from time import sleep
import datetime

def get_latest_smoothings(freq = None):
    smoothings = dict()
    print(nodes)
    for node in ["67"]:
        if freq:
            try:
                smoothing = subprocess.check_output(['tail', '-1', smooth_dir_base+node+ "/"+ str(freq) + ".out"]).decode('utf-8')
                smoothings[node] = float(smoothing.split(",")[1])
                thisdate = datetime.datetime.strptime(smoothing.split(",")[0], "%Y-%m-%d_%H-%M-%S.%f")
            except:
                print("Couldn't fetch for node", node)
    with open("latest_date_mobile", "w") as f:
        f.write(thisdate.strftime("%Y-%m-%d %H:%M:%S"))
    return smoothings

def get_colors(smoothings):

    sorted_smoothings = sorted(smoothings.items(), key=operator.itemgetter(1))
    smoothing_divisor = float(len(sorted_smoothings) - 1)
    colors = dict()
    ctr = 0
    for smoothing in sorted_smoothings:
        #if coloring_strategy == 'relative':
        #    if ctr / smoothing_divisor < relative_thresh_green:
        #        color = 'green'
        #    elif ctr / smoothing_divisor > relative_thresh_red:
        #        color = 'red'
        #    else:
        #        color = 'yellow'
        print smoothing[1]
        if True:
            if smoothing[1] < absolute_thresh_green:
                color = 'blue'
            elif smoothing[1] > absolute_thresh_red:
                color = 'red'
            else:
                color = 'yellow'
        ctr += 1
        colors[smoothing[0]] = color
    #for node in range(99):
    #    if node == 20:
    #        colors[str(node)] = "green" if random.random() > 2/3.0 else "yellow" if random.random() > 1/2.0 else "red"

    return colors

def fill_in_colors(colors):

    with open("nodes_mobile_colors_template.txt", "r") as fin:
        lines = fin.readlines()

    changed_lines = []

    for line in lines:
        for point in colors.items():
            line = line.replace('NODE' + point[0].zfill(2), str(point[1]))
        changed_lines.append(line)

    with open("nodes_mobile_colors.txt", "w") as fout:
        for line in changed_lines:
            fout.write(line)

def build_map():
    smoothings = get_latest_smoothings(2437)
    colors = get_colors(smoothings)
    fill_in_colors(colors)

if __name__ =='__main__':
    while True:
        try:
            build_map()
        except:
            pass
        sleep(3)
