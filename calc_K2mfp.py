#!/usr/bin/env python
# -*- coding: utf-8 -*-
import phys
import argparse

# retrieve args
parser = argparse.ArgumentParser(
formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
'-K', 
type=float, 
default=1e22,  # [1]
help='spatial diffusion coeff, in [cm2/s]'
)
parser.add_argument(
'-Ek', 
type=float, 
default=1e9,  # [1]
help='kinetic energy of proton, in [eV]'
)
pa = parser.parse_args()

mfp_in_AU = phys.K2mfp(pa.K, pa.Ek)
print " - mfp/AU : %e" % mfp_in_AU


#EOF
