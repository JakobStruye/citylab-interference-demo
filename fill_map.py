from shared import *
import subprocess
import operator

def get_latest_smoothings(freq = None):
    smoothings = dict()
    for node in nodes:
        if freq:
            smoothing = subprocess.check_output(['tail', '-1', smooth_dir_base+node+"/output/"+ str(freq) + ".out"])
            smoothings[node] = float(smoothing.split(",")[1])
    return smoothings

def get_colors(smoothings):

    sorted_smoothings = sorted(smoothings.items(), key=operator.itemgetter(1))
    smoothing_count = float(len(sorted_smoothings))
    colors = dict()
    ctr = 0
    for smoothing in sorted_smoothings:
        ctr += 1
        if coloring_strategy == 'relative':
            if ctr / smoothing_count < absolute_thresh_green:
                color = 'green'
            elif ctr / smoothing_count > absolute_thresh_red:
                color = 'red'
            else:
                color = 'yellow'
        elif coloring_strategy == 'absolute':
            if smoothing[1] < absolute_thresh_green:
                color = 'green'
            elif smoothing[1] > absolute_thresh_red:
                color = 'red'
            else:
                color = 'yellow'
        colors[smoothing[0]] = color

def fill_in_colors(colors):

    with open("nodes_template.json", "r") as fin:
        lines = fin.readlines()

    changed_lines = []

    for line in lines:
        for point in colors.iteritems():
            line = line.replace('"node' + point[0].zfill(2) + '"', point[1])
        changed_lines.append(line)

    with open("nodes.json", "w") as fout:
        for line in changed_lines:
            fout.write(line)

def build_map():
    smoothings = get_latest_smoothings(2412)
    colors = get_colors(smoothings)
    fill_in_colors(colors)

if __name__ =='__main__':
    build_map()