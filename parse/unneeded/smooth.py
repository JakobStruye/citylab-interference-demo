from sys import argv
from os.path import exists
from os import makedirs

node = argv[1]
freq = argv[2]
movavg = -80.0
movavgs = []
times = []
with open("parsed/"+node+"-"+freq + "-time", "r") as f:
    lines = f.readlines()
    for line in lines:
        times.append(int(line.decode("UTF-8")))
with open("parsed/"+node+"-"+freq, "r") as f:
    lines = f.readlines()
    for line in lines:
        movavg = 0.96 * movavg + 0.04 * float(line.decode("UTF-8"))
        movavgs.append(movavg)
if not exists("smoothed/" + node + '/'):
    makedirs("smoothed/" + node + '/')
print(len(times), len(movavgs))
with open("smoothed/" + node + "/" + freq, "w") as f:
    for i in range(min(len(times), len(movavgs))):
        f.write(str(times[i]) + "," +  str(movavgs[i]) + "\n")


