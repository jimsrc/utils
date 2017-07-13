#!/usr/bin/env python
# -*- coding: utf-8 -*-
import psutil, time
import argparse, sys
import numpy as np
from datetime import datetime, timedelta


def utc2date(utcsec):
    utcini = datetime(1970,1,1,0,0)
    return utcini + timedelta(seconds=utcsec)


def measure(start, now):
    if start is None:
        return True
    else:
        return now > start


def build_measure_array(t, *data):
    buff = np.array([t, data[0]]).T
    if len(data)==1:
        # we are done.
        return buff
   
    # iterate from the 2nd element
    for _data in data[1:]:
        data_elem = np.array(_data).reshape(len(_data),1)
        buff = np.concatenate([buff, data_elem], axis=1)
    return buff


def save_measure(fname, start, t, *data):
    buff = build_measure_array(t, *data)
    timestmp = utc2date(start).strftime('%d %b %Y %H:%M:%S')
    HEADER = """
    Memory consumption measurements.
    Measurement started at {timestmp} (UTC)
    """.format(timestmp=timestmp)
    np.savetxt(fname, X=buff, fmt='%g', header=HEADER)
    

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
    #while measure(start, time.time()):
    while True:
        try:
            time.sleep(1)
            #print " > measure "
            sys.stdout.write('> measure %d' % len(t) + '\r')
            sys.stdout.flush()
            t         += [ time.time() - start ] # [sec]
            mem_avail  = psutil.virtual_memory()[1] # [bytes]
            mem_used2 += [ mem_tot - mem_avail ]    # [bytes]
            mem_used  += [ psutil.virtual_memory()[3] ] # [bytes]

        except KeyboardInterrupt:
            print("\n [*] saving measurements...\n")
            save_measure(pa.fname_out, start, t, mem_used2, mem_used)
            print('\n [+] success on saving:\n %s\n'%pa.fname_out)
            break


if __name__=='__main__':
    main()


#EOF
