#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psutil, time
import argparse, sys
import numpy as np
from datetime import datetime, timedelta
import funcs as ff


def measure(start, now):
    if start is None:
        return True
    else:
        return now > start


def main():
    #--- retrieve args
    parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
    '-fo', '--fname_out',
    type=str,
    default='test.txt',
    help='output filename.',
    )
    pa = parser.parse_args()

    #++++++++++++++++++++++++++++++++++
    t = []
    mem_used, mem_used2 = [], []
    mem_tot = psutil.virtual_memory()[0] # [bytes]

    start = time.time() # mediante argparse, cambiarle el valor inicial
    print('\n [*] Starting measurement at ' + ff.utc2date(start).strftime('%d %b %Y %H:%M:%S') + ' (UTC) \n')
    #while measure(start, time.time()):
    while True:
        try:
            time.sleep(1)
            #print " > measure "
            sys.stdout.write('> measure %d' % len(t) + '\r')
            sys.stdout.flush()
            t         += [ time.time() - start ] # [sec]
            mem_avail  = psutil.virtual_memory()[1]/(1024.*1024.) # [MB]
            mem_used2 += [ (mem_tot-mem_avail)/(1024.*1024.) ]    # [MB]
            mem_used  += [ psutil.virtual_memory()[3]/(1024.*1024.) ] # [MB]

        except KeyboardInterrupt:
            print("\n [*] saving measurements...\n")
            ff.save_measure(pa.fname_out, start, None, t, mem_used2, mem_used)
            print('\n [+] success on saving:\n %s\n'%pa.fname_out)
            break


if __name__=='__main__':
    main()


#EOF
