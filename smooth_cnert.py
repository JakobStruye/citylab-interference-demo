import numpy as np

with open('freq_out/1/5220.out') as f:
    lines = f.readlines()
    lines = [int(l.split(' ')[1]) for l in lines]
    init = np.mean(lines[:100])
    vals = [init]
    for i in range(100,len(lines)):
        vals.append(vals[-1] * 0.96 + lines[i] * 0.04)
    for val in vals:
         print val
