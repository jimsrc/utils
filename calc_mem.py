#!/usr/bin/env python
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


# asumiendo q los datos son floats de 4bytes:
scell   = 3.2*2.   # [Kbytes, KB] aprox. size of each cell

ncx, ncy, ncz   = pa.cells #4, 4, 4
blk_size        = 1.0*ncx*ncy*ncz*scell  # [KB] block size taking computational cells only, for each block
blk_size_tot    = 1.0*(ncx+4)*(ncy+4)*(ncz+4)*scell # [KB] block size taking total nmbr of cells, for each block

# nmbr of Root Blocks (in each dimension)
nbx, nby, nbz   = pa.blocks #2, 2, 2

size_comp       = 1.0*nbx*nby*nbz * blk_size    # [KB]
size_comp_max   = 1.0*size_comp*(8**(pa.glevel))   # [KB]
size_tot        = 1.0*nbx*nby*nbz * blk_size_tot
size_tot_max    = size_tot*(8**(pa.glevel))   # [KB]

print " nmbr of computational blocks                : %d" % (nbx*nby*nbz)
print " nmbr of computational blocks (w/ max refine): %d" % (nbx*nby*nbz * (8**(pa.glevel)))
print " nmbr of computationsl cells                 : %d" % (nbx*nby*nbz * ncx*ncy*ncz)
print " nmbr of computationsl cells (w/ max refine) : %d\n" % (nbx*nby*nbz * ncx*ncy*ncz *(8**(pa.glevel)))

print " total nmbr of cells (comp+ghost)            : %d" % (nbx*nby*nbz * (ncx+4)*(ncy+4)*(ncz+4))
print " total nmbr of cells (w/ max refine)         : %d" % (nbx*nby*nbz * (ncx+4)*(ncy+4)*(ncz+4) * (8**(pa.glevel)))
print ""


print " mem computational     : %g MB" % (size_comp/(1024.))
print " mem computational MAX : %g MB" % (size_comp_max/(1024.))
print " mem total             : %g MB " % (size_tot/(1024.))
print " mem total MAX         : %g MB " % (size_tot_max/(1024.))


#EOF
