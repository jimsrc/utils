# -*- coding: utf-8 -*-
import psutil, time
import argparse, sys
import numpy as np
from datetime import datetime, timedelta



def utc2date(utcsec):
    utcini = datetime(1970,1,1,0,0)
    return utcini + timedelta(seconds=utcsec)

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


#EOF
