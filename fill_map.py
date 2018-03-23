from shared import *
import subprocess

def get_latest_smoothings(freq = None):
    smoothings = dict()
    for node in nodes:
        if freq:
            smoothing = subprocess.check_output(['tail', '-1', smooth_dir_base+node+"/output/"+ str(freq) + ".out"])
            smoothings[node] = float(smoothing.split(",")[1])
    return smoothings

def do_maps():
    smoothings = get_latest_smoothings(2412)

    #copyfile("nodes_template.json", "nodes_temp.json")
    with open("nodes_template.json", "r") as fin:
        lines = fin.readlines()

    changed_lines = []
    for line in lines:
        for point in smoothings.iteritems():
            color = '"green"' if point[1] < -80.0 else '"yellow"'
            line = line.replace('"node' + point[0].zfill(2) + '"', color)
        changed_lines.append(line)

    with open("nodes.json", "w") as fout:
        for line in changed_lines:
            fout.write(line)



do_maps()
