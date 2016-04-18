#!/usr/bin/env python
#-*- coding: utf-8 -*-


def rankpres(mask):
	'''for bool series, returns averaging score'''
	A, N = 0, 0
	for i, a in enumerate(mask):
		N += 1 / i
		A += int(a) / i

	return A/N
