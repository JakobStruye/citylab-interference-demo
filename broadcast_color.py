#!/usr/bin/env python
# coding=utf-8

import sys
import colorsys

from lifxlan import BLUE, COLD_WHITE, CYAN, GOLD, GREEN, LifxLAN, \
    ORANGE, PINK, PURPLE, RED, WARM_WHITE, WHITE, YELLOW
import time
import subprocess
from shared import *

colors = {
    "red": RED, 
    "orange": ORANGE, 
    "yellow": YELLOW, 
    "green": GREEN, 
    "cyan": CYAN, 
    "blue": BLUE, 
    "purple": PURPLE, 
    "pink": PINK, 
    "white": WHITE, 
    "cold_white": COLD_WHITE, 
    "warm_white": WARM_WHITE, 
    "gold": GOLD
}
error_message = """Usage:

   python set_color_all.py blue
   python set_color_all.py 43634 65535 65535 3500

The four numbers are HSBK values: Hue (0-65535), Saturation (0-65535), Brightness (0-65535), Kelvin (2500-9000).
See get_colors_all.py to read the current HSBK values from your lights.

The available predefined colors are:
""" + ", ".join(colors.keys())

lifxlan = LifxLAN()

prevval = 0
previndex = -1
color = []
while True:
    #time.sleep(0.5)
    #Get the 100 most recent measurements
    recent_smooth_lines = subprocess.check_output(['tail', '-n100', raw_parse_dir_base + "70" + "/" + "2437" + ".out"])
    vals = []
    for line in recent_smooth_lines.split("\n")[:-1]: #-1 for newline at end of file
        vals.append(float(line.split(",")[1]))
    latestval = vals[-1]
    vals.sort()
    index = vals.index(latestval)
    #The latest measurement is the index-th lowest of the 100 most recent ones

    #if latestval < -85:
    #    rgb = (0,0,1)
    color = colors["red"]
    minval = -65
    maxval = 0
    perc25 = minval + abs(maxval - minval)  * 0.75
    perc50 = minval + abs(maxval - minval) * 0.5
    perc75 = minval + abs(maxval - minval) * 0.25
    #print perc25
    #print perc50
    #print perc75
    if len(sys.argv) > 1:
        latestval = float(sys.argv[1])
    #print latestval
    if latestval > maxval:
        rgb = (1,0,0)
    elif latestval > perc25:
        rgb = (1., 1 - 0.35 *((latestval - perc25) / (maxval - perc25)), 0.)
    elif latestval > perc50:
        rgb = (0.65 + 0.35 * ((latestval - perc50) / (perc25 - perc50)), 1., 0.)
    elif latestval > perc75:
        rgb = (0., 1., 1 - 0.35*((latestval - perc75) / (perc50 - perc75)))
    elif latestval > minval:
        rgb = (0.,  0.65 + 0.35*((latestval - minval) / (perc75 - minval)), 1.)
    else:
        rgb = (0,0,1)
    print(rgb)
    #rgbs = [(0,0,1), (0,0.5,0.5), (0,1,0), (0.5,0.5,0), (1,0,0)]
    #percentage = (latestval - minval) / (maxval - minval)
    #percentage = max(0.0, min(1.0,percentage))
    #hue = percentage * 42000
    #percentage *= len(rgbs)
    #ind = int(percentage)
    #print ind
    #rgb = rgbs[ind]
    #if latestval < -45:
    ##    color = colors["blue"]
    ##    #print "blue"
    #elif latestval > -10:
    #    color = colors["red"]
    #    print "RED"
    #elif latestval > -25:
    #    color = colors["yellow"]
    #else:
    #    color = colors["purple"]
    #rgb = (1,0.7,0)
    hls = colorsys.rgb_to_hls(rgb[0], rgb[1], rgb[2])
    color[0] = hls[0] * 65535
    color[1] = hls[2] * 65535
    color[2] = hls[1]
    #color = colors[sys.argv[2]]
    #color[3] = 30000
    #color = colors["green"]
    print(color)
    #print latestval, index
    #color = colors["yellow"]
    #Determine intensity based on difference with previous measurement (closer to an extreme <-> brighter)    
    if latestval != prevval:
        prevval = latestval
        change = index - previndex
        if color == "green":
            change = -1 * change
        previndex = index
    try: 
        change
    except:
        change = 0

    #3rd value of color 4-tuple contains intensity 0-65535
    if change > 2:
        color[2] = 65535
    elif change < 0:
        color[2] = 20000
    else:
        color[2] = 40000
    color[2] = 20000
    #Broadcast color to any light in the local network
    lifxlan.set_color_all_lights(color, rapid=True)
    #print lifxlan.get_power_all_lights()
