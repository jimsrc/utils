# -*- coding: utf-8 -*-
import psutil, time
import argparse, sys
import numpy as np
from datetime import datetime, timedelta
from subprocess import Popen, PIPE, STDOUT


def look_for_process(pname):
    # grab the PID numbers and the command string, for processes
    # whose command string follows the pattern `pname`
    CMD = 'ps aux | grep "%s" | awk \'{s=""; for(i=11;i<=NF;i++) s = s $i " "; print $2, s}\' ' % pname
    p = Popen(CMD, stdin=PIPE, stdout=PIPE, stderr=STDOUT, 
        bufsize=1, shell=True)
    out_, _ = p.communicate()
    # [:-1] is because the last one is an empty string ''
    out = out_.split('\n')[:-1]

    _pid, _cmd = [], []
    # get a 2D array
    #for _o in out:
    for i in range(len(out)):
        _o   = out[i]
        _pid += [ _o.split()[0] ]
        _cmd += [ _o.replace(_pid[-1]+' ', '') ]
        print " [*] " + _cmd[-1]
        if _cmd[-1].startswith('/bin/sh -c ') or \
                _cmd[-1].startswith('grep '+pname):
            print "     [+] removing..."
            # reject this process, because it refers to me
            _pid.pop(-1); _cmd.pop(-1)

    if len(_pid)==0:
        return None, None, None
    else:
        return _pid, _cmd, out


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


def save_measure(fname, start, header, t, *data):
    buff = build_measure_array(t, *data)
    timestmp = utc2date(start).strftime('%d %b %Y %H:%M:%S')

    # header
    if header is None:
        HEADER = """
        Memory consumption measurements.
        Measurement started at {timestmp} (UTC)
        """.format(timestmp=timestmp)
    else:
        HEADER = header

    print "\n [*] buff.dtype :", type(buff), '\n'
    print " [*] output shape: ", buff.shape
    np.savetxt(fname, X=buff, fmt='%g', header=HEADER)


#EOF