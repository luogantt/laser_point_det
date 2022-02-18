#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 14:25:55 2022

@author: oem
"""

for i in range(3):
    for j in range(3):
        if i==1 and j==1:
            continue
            # break
        print(i,j)
        
        
import numpy as np

import numba


@numba.jit(nopython=True)
def _k(a):
    a=a+2
    return 1

_k(a)
print(a)
