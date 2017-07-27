#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psutil, time
import argparse, sys
import numpy as np
from datetime import datetime, timedelta
import funcs as ff


#--- retrieve args
parser = argparse.ArgumentParser(
formatter_class=argparse.ArgumentDefaultsHelpFormatter,
description="""
script to monitor memory info about processes that match 
a given pattern.
""",
)
parser.add_argument(
'-fo', '--fname_out',
type=str,
default='test.txt',
help='output filename.',
)
parser.add_argument(
'-pn', '--proc_name',
type=str,
default='SWMF.exe',
help='pattern for the process command we seek for',
)
pa = parser.parse_args()


t = []
mem_tot = psutil.virtual_memory()[0] # [bytes] RAM capacity

start = time.time() # mediante argparse, cambiarle el valor inicial
print('\n [*] Starting measurement at ' + ff.utc2date(start).strftime('%d %b %Y %H:%M:%S') + ' (UTC) \n')


# template
VIRT    = 0
SHR     = 1
RES     = 2

NotFound = 1
while True:
    # look for target process...
    if NotFound:
        time.sleep(1)
        # these are the PID numbers for the processes described by 
        # the pattern `proc_name`; except for those that match with 
        # this very same process (i.e. the childrens of this script):
        PIDs, CMDs, raw = ff.look_for_process(pa.proc_name)
        NotFound = 1 if PIDs is None else 0
        continue
    else:
        break

# initialize data arrays for each of the processes
# listed in PIDs:
memdata = {} # keys are the PID numbers
for _pid in PIDs:
    memdata[_pid] = {VIRT: [], SHR: [], RES: []}
ndata = 0
while True:
    try:
        time.sleep(1)
        sys.stdout.write('> measure %d' % len(t) + '\r')
        sys.stdout.flush()
        t         += [ time.time() - start ] # [sec]
        for _pid in PIDs:
            pinfo               = psutil.Process(pid=int(_pid))
            memdata[_pid][RES]  += [ pinfo.memory_info()[0] ] # resident
            memdata[_pid][VIRT] += [ pinfo.memory_info()[1] ] # virtual
            memdata[_pid][SHR]  += [ pinfo.memory_info()[2] ] # shared
            ndata               += 1

    except KeyboardInterrupt:
        if len(t)==0:
            print("\n [-] No measurements made!\n")

        else:
            # build header (reporting the PID numbers for the columns of data)
            header = '\n time'
            for _pid in PIDs:
                header += ', ' + _pid
            header += '\n'

            print " [*] we captured %d processes" % len(memdata.keys())
            buff = []  # to save in ASCII
            for _pid in memdata.keys():
                for _dnm in memdata[_pid]:
                    buff += [ memdata[_pid][_dnm] ]

            print("\n [*] saving %d measurements...\n" % len(t))
            ff.save_measure(pa.fname_out, start, header, t, *buff)
            print('\n [+] success on saving:\n %s\n'%pa.fname_out)

        break



#EOF