#!/usr/bin/env python
#-*- coding: utf-8 -*-
# TODO: check wheter numpy is faster than pandas
import numpy as np
# import pandas as pd
# from timeitDec import timeit


# @timeit
def rankpres(mask):
    '''for bool series, returns averaging score'''
    n = np.arange(mask.shape[0]) + 1

    N = (1 / n).sum()
    A = (mask.astype(float) / n).sum()
    return A / N

# @timeit
# def rankpres2(pd_mask):
#     '''for bool series, returns averaging score'''
#     n = pd_mask.index + 1

#     N = pd.Series((1 / n)).sum()
#     A = (pd_mask.astype(float) / n).sum()
#     return A / N


# def test():
# 	'''trying to unders'''
# 	rankpres(np.array((True, True, False, True, False, True)))
# 	rankpres2(pd.Series((True, True, False, True, False, True)))

# if __name__ == '__main__':
#     test()
