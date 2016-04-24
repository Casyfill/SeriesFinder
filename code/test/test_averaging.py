#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
nasty test placeholder, to be replaced
'''
# import unittest
import numpy as np
from ..averaging import rankpres


def testRankpress():
    return rankpres(np.array((True, True, False, True, False, True))) == 1.75


testRankpress()
