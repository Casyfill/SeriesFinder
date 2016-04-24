#!/usr/bin/env python
#-*- coding: utf-8 -*-
import numpy as np
from attributes import attr_similarity as ASM
from omega import OMEGA  # global attrweight matrix


def sm(c1, c2):
    '''
    generate direct similarity metric np.array,
    using special sim_metric for each attribute

    c1, c2 - crimes (????) #TODO: nd.arrays? pd.Series? dicts? tuples?
    named tuples? tuples, I guess, for now
    asm - similarities function tuple, to be created
    '''
    global ASM
    return np.array((ASM[i](c1[i], c2[i]) for i in xrange(asm.shape[0])))


def get_nu(p):
    '''
    calculates NU weight matrix for the pattern, 
    basically sum of each-to-each similarities

    p - crime pattern iterable
    '''
    return np.vstack((sm(c1, c2) for c1 in p
    							 for c2 in p if c1 != c2)).sum(0)  # TODO: skip twin tuples?


def crime_crime_sim(c1, c2, nu):
    '''
    returns overal crime-crime similarity
    c1, c2 - crime objects
    nu - pattern-vise attr weightss
    '''
    global OMEGA
    return (sm(c1, c2) * OMEGA * nu).sum() / (OMEGA * nu).sum()


def pattern_crime_sim(p, c, nu, d=1.2):
    '''
    returns simiarity between pattern and crime, with defined dynamics coeff

    p - crime pattern
    c - candidat crime
    d - dynamics coeff hyperparam
    nu - pattern-vise attr weightss
    '''

    return ((crime_crime_sim(c1, c, nu)**d for c1 in p) / len(p))**(1 / d)


def cohesion(p, d, nu):
	'''
	returns cohesion metric for chosen crime pattern

	p - crime pattern iterable
	d - dynamics coeff hyperparam
	nu - pattern-vise attr weightss
	'''
	return (pattern_crime_sim(p.remove(c1), c1, nu) for c1
			in p).sum() / p.shape[0]


def main(seeds, db, cutoff, d=1.2):
	'''
	main process of pattern search
	CAUTION: #TODO: for now there is no defined strategy
	on pattern overlap/concurency. I just remove crimes
	on first come - first serve basis.
	#NOTE: it might be smart to provide both series and cohesion/similarity metric

	seeds - initial patterns
	db - database of crimes, iterable
	cutoff - cohesion treshold level
	omega - overal attr weight array
	d - dynamics coeff hyperparam
	'''

	for ptrn in seeds:
		nu = get_nu(ptrn)  # get initial pattern-wise attr weighs

		while True:
			c = sorted(db, key=pattern_crime_sim(ptrn, c, nu, d),
				reverse=True)[0]  # get crime with the highest similarity measurement

			p1 = ptrn + (c,)
			nu1 = get_nu(p1)

			if cohesion(p1, nu1) < cutoff:
				yield ptrn
				break
			else:
				ptrn = p1 # update pattern
				db.remove(c) # remove crime from general database
				nu = nu1 # update patternwise attr weights
