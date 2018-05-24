#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psutil, time
import argparse, sys
import numpy as np
from numpy import array
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
default='BINARY.exe',
help='pattern for the process command we seek for',
)
parser.add_argument(
'-pid', '--pid',
type=int,
default=None,
help='PID of the process',
)
parser.add_argument(
'-q', '--quiet',
action='store_true',
help='Don\'t show a "live" report while measuring. This \
is useful when running in background or piping the STDOUT \
to a file.',
)
pa = parser.parse_args()

t           = []
mem_used    = []
mem_tot     = psutil.virtual_memory()[0] # [bytes] RAM capacity

start = time.time() # mediante argparse, cambiarle el valor inicial
print('\n [*] Starting measurement at ' + ff.utc2date(start).strftime('%d %b %Y %H:%M:%S') + ' (UTC) \n')


# template
VIRT    = 0
SHR     = 1
RES     = 2

if pa.pid is not None:
    PIDs = [str(pa.pid),]
    NotFound = 0
else:
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
        print '\n [+] monitoring these PID(s):\n     ', PIDs
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
        t          += [ time.time() - start ] # [sec]
        mem_avail   = psutil.virtual_memory()[1]        # [B]
        mem_used   += [ (mem_tot - mem_avail) ]         # [B]
        for _pid in PIDs:
            pinfo               = psutil.Process(pid=int(_pid))
            res, virt, shr      = pinfo.memory_info()[:3]
            memdata[_pid][RES]  += [ res  ] # resident
            memdata[_pid][VIRT] += [ virt ] # virtual
            memdata[_pid][SHR]  += [ shr  ] # shared

            # report on screen
            _report = '> measure #%d (PID:%s); RES:%g, VIRT:%g, SHR:%g, TOT:%g'%(\
            len(t), _pid, res/(2.**20), virt/(2.**20), shr/(2.**20), mem_used[-1]/(2.**20))
            if not(pa.quiet):
                sys.stdout.write(_report + '\r')
                sys.stdout.flush()

        # nmbr of **successful** measurements
        ndata               += 1

    except (KeyboardInterrupt, psutil.NoSuchProcess):
        # stop measuring either if:
        # - we press Ctrl+C, or
        # - processes terminate
        if len(t)==0:
            print("\n [-] No measurements made!\n")

        else:
            # truncate to a valid length
            t           = t[:ndata]                                 # [sec]
            mem_used    = array(mem_used[:ndata])/(2.**20)          # [MB]
            for _pid in PIDs:
                memdata[_pid][RES]  = array(memdata[_pid][RES][:ndata])/(2.**20)   # [MB]
                memdata[_pid][VIRT] = array(memdata[_pid][VIRT][:ndata])/(2.**20)  # [MB]
                memdata[_pid][SHR]  = array(memdata[_pid][SHR][:ndata])/(2.**20)   # [MB]

            # build header (reporting the PID numbers for the columns of data)
            header =  '\n For each PID, three columns of memory usage:'
            header += '\n Virtual (VIRT), Shared (SHR), and Resident (RES)\n'
            header += '\n time [sec], total RAM used [MB]'
            for _pid in PIDs:
                header += ', ' + _pid
            header += '\n'

            print " [*] we captured %d processes" % len(memdata.keys())
            buff = []  # to save in ASCII
            buff += [ mem_used ]    # 2nd column (time is 1st column)
            for _pid in memdata.keys():
                for _dnm in [VIRT, SHR, RES]:
                    buff += [ memdata[_pid][_dnm] ]

            print("\n [*] saving %d measurements...\n" % len(t))
            ff.save_measure(pa.fname_out, start, header, t, *buff)
            print('\n [+] success on saving:\n %s\n'%pa.fname_out)

        break



#EOF
