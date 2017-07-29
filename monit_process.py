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
Script to monitor memory info about processes that match 
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
        time.sleep(0.3)
        # these are the PID numbers for the processes described by 
        # the pattern `proc_name`; except for those that match with 
        # this very same process (i.e. the childrens of this script):
        PIDs, CMDs, raw = ff.look_for_process(pa.proc_name)
        NotFound = 1 if PIDs is None else 0
        continue
    else:
        print('\n [+] monitoring these PID(s):\n     ', PIDs)
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
        #sys.stdout.write('> measure %d' % len(t) + '\r')
        #sys.stdout.flush()
        t         += [ time.time() - start ] # [sec]
        for _pid in PIDs:
            pinfo               = psutil.Process(pid=int(_pid))
            res, virt, shr      = pinfo.memory_info()[:3]
            memdata[_pid][RES]  += [ res  ] # resident
            memdata[_pid][VIRT] += [ virt ] # virtual
            memdata[_pid][SHR]  += [ shr  ] # shared

            # report on screen
            _report = '> measure #%d;  RES: %g,  VIRT: %g,  SHR: %g'%(\
                    len(t), res/(2.**20), virt/(2.**20), shr/(2.**20))
            sys.stdout.write(_report + '\r')
            sys.stdout.flush()

        # nmbr of **successful** measurements
        ndata               += 1

    except (KeyboardInterrupt, psutil.NoSuchProcess):
        if len(t)==0:
            print("\n [-] No measurements made!\n")

        else:
            # truncate to a valid length
            t                   = t[:ndata]
            for _pid in PIDs:
                memdata[_pid][RES]  = memdata[_pid][RES][:ndata]
                memdata[_pid][VIRT] = memdata[_pid][VIRT][:ndata]
                memdata[_pid][SHR]  = memdata[_pid][SHR][:ndata]

            # build header (reporting the PID numbers for the columns of data)
            header =  '\n For each PID, three columns of memory usage:'
            header += '\n Virtual (VIRT), Shared (SHR), and Resident (RES)\n'
            header += '\n time [sec]'
            for _pid in PIDs:
                header += ', ' + _pid
            header += '\n'

            print " [*] we captured %d processes" % len(memdata.keys())
            buff = []  # to save in ASCII
            for _pid in memdata.keys():
                for _dnm in [VIRT, SHR, RES]:
                    buff += [ memdata[_pid][_dnm] ]

            print("\n [*] saving %d measurements...\n" % len(t))
            ff.save_measure(pa.fname_out, start, header, t, *buff)
            print('\n [+] success on saving:\n %s\n'%pa.fname_out)

        break



#EOF
