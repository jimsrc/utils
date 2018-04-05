# -*- coding: utf-8 -*-
import psutil, time
import argparse, sys, re
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
    del p
    # [:-1] is because the last one is an empty string ''
    out = out_.split('\n')[:-1]

    print(' +++++++++++++++++++++++++++++++++++++++++++')
    _strtime = utc2date(time.time()).strftime('%d %b %Y %H:%M:%S')
    print(' [*] List of processes that match \''+pname+'\' \n     ({:s}):\n'.format(
        _strtime))
    _pid, _cmd = [], []
    pattern = re.compile('.*monit_process.py .*')
    # get a 2D array
    for i in range(len(out)):
        _o   = out[i]
        _pid += [ _o.split()[0] ]                   # 1st column is PID
        _cmd += [ _o.replace(_pid[-1]+' ', '') ]    # from 2nd to the last column is the full command
        # report the PID and the full command
        print " [*] %05d  %s" % (int(_pid[-1]), _cmd[-1])

        # The conditions below are:
        # 1) the command 'CMD' itself
        # 2) the grep command executed by this 'CMD' command
        # 3) the command 'CMD' itself, again
        # 4) editing the 'pattern' file ()
        if _cmd[-1].startswith('/bin/sh -c ') or \
                _cmd[-1].startswith('grep '+pname) or \
                pattern.match(_cmd[-1]) or \
                _cmd[-1].startswith('vim '):                # editing the 'pattern' file ()
            print "     [+] removing..."
            # reject this process, because it refers to me
            _pid.pop(-1); _cmd.pop(-1)

    print(' +++++++++++++++++++++++++++++++++++++++++++\n')
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

    #--- header
    HEADER = """
    Memory consumption measurements.
    Measurement started at {timestmp} (UTC)
    """.format(timestmp=timestmp)
    if header is not None:
        HEADER += '\n'+header

    print " [*] output-array shape: ", buff.shape
    np.savetxt(fname, X=buff, fmt='%g', header=HEADER)


#EOF
