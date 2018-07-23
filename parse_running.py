from os import listdir, stat, makedirs, remove
from os.path import exists
import datetime
import subprocess
#import numpy as np
from shared import *
from platform import uname
from time import sleep, mktime
import socket

import pyodbc
import sys

from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity, EntityProperty, EdmType

the_connection_string = "DefaultEndpointsProtocol=https;AccountName=citylab;AccountKey=ZyNTFkoIEuJWu17JdHO9QiivRo3aHGmUkxZwfLHOVep4KswAZoINnfFFQ5xONQhp3OajntW90OBPxrj0bgcnLA==;TableEndpoint=https://citylab.table.cosmosdb.azure.com:443/;"
table = TableService(endpoint_suffix = "table.cosmosdb.azure.com", connection_string= the_connection_string)

#task = {'PartitionKey': 'nodeTest', 'RowKey': '001', 'f1' : -101}
#table.insert_entity('citylab', task)


#server = 'citylab.database.windows.net'
#database = 'citylab'
#username = 'jstruye'
#password = sys.argv[1]
#driver= '{ODBC Driver 17 for SQL Server}'
#cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
#cursor = cnxn.cursor()

myname = socket.gethostname().split(".")[0]#uname()[1].split(".")[0]

#try:
#    cursor.execute("SELECT TOP 1 NULL FROM " + myname)
#except:
#    freqs.sort()
#    sql = "CREATE TABLE " + myname + " ("
#    for freq in freqs:
#        sql += "f"+str(freq) + " SMALLINT, "
#    sql = sql[:-2]
#    sql += ")"
#    print(sql)
#    cursor.execute(sql)

#freqs = channels.values()
def build_entity(pkey, entries, time):
    entity = Entity()
    entity.PartitionKey = pkey
    time = datetime.datetime.strptime(time, "%Y-%m-%d_%H-%M-%S.%f")
    epoch = mktime(time.timetuple()) + time.microsecond / 1000000.0
    entity.RowKey = str(epoch)
    for f in range(len(freqs)):
        freq = "f" + str(freqs[f])
        val = entries[f]
        entity[freq] = EntityProperty(EdmType.INT32, val)
    return entity
while True:
    sleep(1)
    freqs.sort()
    #freqs = freqs[:1]

    nodes = [uname()[1].split(".")[0][4:]]
    for node in nodes:
        raw_parse = raw_parse_dir_base + node + "/"
        if not exists(raw_parse):
            makedirs(raw_parse)
        dump_dir = dump_dir_base# + node + "/output/"
        smooth_dir = smooth_dir_base# + node + "/output/"
        if not exists(smooth_dir):
            makedirs(smooth_dir)

        files = [f for f in listdir(dump_dir)]
        times = [datetime.datetime.strptime(ts, "%Y-%m-%d_%H-%M-%S.%f") for ts in files]
        #if len(times) < 120:
        #    #wait a while
        #    break

        times.sort()
        times = [datetime.datetime.strftime(ts, "%Y-%m-%d_%H-%M-%S.%f")[:-3] for ts in times]
        freqlists = []
        #times = times[:1200]
        for freq in freqs:
            these_times = []
            raw_vals = []
            with open(raw_parse + freq + ".out", 'a') as f:
                for time in times:
                    if (True): #stat(dump_dir + time).st_size > 400000) == (int(freq) > 4000):
                        signalstr = subprocess.check_output(
                            ['./fft_get_max_rssi.out', dump_dir + time, freq])
                        val = int(signalstr)
                        f.write(time + "," + str(val) +  "\n")
                        raw_vals.append(val)
                        these_times.append(time)
            smooth_file = smooth_dir + freq + ".out"
            if exists(smooth_file) and stat(smooth_file).st_size > 0:
                smooth_val = float(subprocess.check_output(['tail', '-1', smooth_file]).split(",")[1])
            else:
                #smooth_val = sum(raw_vals[:100]) / 100.0#np.mean(raw_vals[:100])
                smooth_val = -80.0
            with open(smooth_file, 'a+') as smooth_f:

                smooth_vals = []
                prev_val = smooth_val
                for i in range(len(raw_vals)):
                    val = prev_val * 0.96 + raw_vals[i] * 0.04
                    smooth_vals.append(val)
                    smooth_f.write(these_times[i] + "," + str(val) + "\n")
                    prev_val = val
            freqlists.append(raw_vals)
        entrieslist = []
        for i in range(len(freqlists[0])):
            entries = []
            for freqlist in freqlists:
                try:
                    entries.append(freqlist[i])
                except:
                    entries.append(0)
            entrieslist.append(entries)


        for e in range(len(entrieslist)):
            assert len(entrieslist) == len(times)
            entries = entrieslist[e]
            time = times[e]
            #sql = "insert into " + myname + " values ("
            entity = build_entity(myname, entries, time)
            try:
                table.insert_entity('citylab', entity)
            except:
                pass #Probably duplicate, ignore for now
            #for entry in entries:
            #    sql += str(entry) + ", "
            #sql = sql[:-2]
            #sql += ")"
            #print(sql)
            #cursor.execute(sql)
        #cnxn.commit()
        for time in times:
            remove(dump_dir + time)

