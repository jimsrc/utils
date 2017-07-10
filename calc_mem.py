#!/usr/bin/env ipython
# -*- coding: utf-8 -*-
import numpy as np
import argparse

#--- retrieve args
parser = argparse.ArgumentParser(
formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
'-c', '--cells',
type=int,
default=[4,4,4],
nargs=3,
help='number of cells (for each dimension) in each Root Block.',
)
parser.add_argument(
'-b', '--blocks',
type=int,
default=[2,2,2],
nargs=3,
help='number of block in each dimension.',
)
parser.add_argument(
'-l', '--glevel',
type=int,
default=5,
help='value of GRIDLEVELs (for AMR).',
)
pa = parser.parse_args()


scell   = 3.2   # [Kbytes, KB] aprox.

ncx, ncy, ncz   = pa.cells #4, 4, 4
blk_size_cells  = ncx*ncy*ncz  # [nmbr of cells]
blk_size        = 1.0*blk_size_cells*scell  # [KB]
blk_size_tot    = 1.0*(ncx+4)*(ncy+4)*(ncz+4)*scell # [KB]

# nmbr of Root Blocks (in each dimension)
nbx, nby, nbz   = pa.blocks #2, 2, 2

size_comp       = 1.0*nbx*nby*nbz * blk_size    # [KB]
size_tot        = 1.0*nbx*nby*nbz * blk_size_tot

print " mem computational: %g MB" % (size_comp/(1024.))
print " mem total: %g MB " % (size_tot/(1024.))
print " max total: %g MB " % (size_tot*(2**pa.glevel-1)/(1024.))


#EOF
