#!/usr/bin/env python
# coding=utf-8

import sys

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


color = []
while True:
    time.sleep(1)
    recent_smooth_lines = subprocess.check_output(['tail', '-n100', smooth_dir_base + "67" + "/output/" + "5220" + ".out"])
    vals = []
    for line in recent_smooth_lines.split("\n")[:-1]:
        vals.append(line.split(","))[1]
    vals.sort()
    index = vals.index(recent_smooth_lines.split("\n")[-2].split(",")[1])
    if index < 10:
        color = colors["green"]
    elif index > 90:
        color = colors["red"]
    else:
        color = colors["yellow"]


    print(color)
    lifxlan.set_color_all_lights(color, rapid=True)

