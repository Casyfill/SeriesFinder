#!/usr/bin/env python
#-*- coding: utf-8 -*-
import numpy as np


def rankpres(mask):
    '''for bool series, returns averaging score'''
    n = np.arange(mask.shape[0]) + 1

    N = (1 / n).sum()
    A = (mask.astype(float) / n).sum()
    return A / N


print rankpres(np.array((True, True, False, True, False, True)))
