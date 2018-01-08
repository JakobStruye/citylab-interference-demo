import os
import sys
from datetime import datetime, timedelta
origpath = os.getcwd()
os.chdir(sys.argv[1])
for directory in os.listdir('.'):
    if not os.path.isdir(directory):
        continue
    os.chdir(directory)
    os.chdir("output")
    for name in os.listdir('.'):
        time = datetime.strptime(name, '%Y-%m-%d_%H-%M-%S')
        newname = (time + timedelta(hours=8)).strftime('%Y-%m-%d_%H-%M')
        os.rename(name, newname)
    os.chdir("../..")



os.chdir(origpath)
