#!/usr/bin/env python
# -*- coding: utf-8 -*-
import phys
import argparse

# retrieve args
parser = argparse.ArgumentParser(
formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
'-Ek', 
type=float, 
default=1e9,  # [1]
help='kinetic energy of proton'
)
pa = parser.parse_args()

beta = phys.calc_beta_relativist(pa.Ek)
print " - beta: %g" % beta

#EOF
