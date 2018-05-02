from shared import *
import time
import threading
import subprocess
from concurrent.futures import ThreadPoolExecutor

def run_model(node, freq):
    subprocess.check_output(["python", "run_rnn.py", node, freq])

if __name__ == '__main__':
  with ThreadPoolExecutor(max_workers=4) as e:
    while True:
        ts = []
        for node in nodes:
            for freq in freqs:
                future = e.submit(run_model, str(node), str(freq))
                #t.start()
                #ts.append(t)
                time.sleep(0.1)
            
        #for t in ts:
        #    t.join()
        while not future.done():
            time.sleep(1)
        time.sleep(30)
