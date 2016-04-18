#!/usr/bin/env python
#-*- coding: utf-8 -*-

from cosine import textSim
from globalWeights import getGW

gW = getGW() # read general weights from external matrix file

def sim(a,b):
	'''linear feature-wise comparison,
	returns a matrix of similarities of the same shape'''

	c = textSim(a.text, b.text) # cosine similarity between two bags of words
	d = dist(a.point, b.point) # 3d-spatial distance between two points. (3D - linear datetime)
	dt = daytime(a.time, b.time, dkd=dkd) # probablistic daytime distance, using kerned dencity
	wt = weektime(a.wtime, b.wtime, wkd=wkd) # probablistic weektime distance, using kerned dencity
	return (c,d,dt,wt)

def crimeS(a, b, pW, gW=gW):
	'''
	similarity metric between two crimes,
	generated as a product of feature-vise similarities,
	muptiplied by general weights and pattern-wise weights.
	'''
	G = pW * gW # generalized weight matrix

	return sum(G*sim(a, b))/G


def pattern_crimeS(P, c, d=d):
	'''
	similarity metric between pattern and crime
	'''
	cP = P.append(c)
	# matixvise feature summation of similarities for all
	# features for all crimes in pattern + new potential member
	pW = sum([sim(a, b) for a in cP for b in cP if a != b])

	return sum([crimeS(p, c, pW)**d for p in P])**(1/d)


def cohesion(P):
	'''measuring cohesion of the pattern'''
	return sum([pattern_crimeS(a, P-a) for a in P]/len(P)


def main(iP, DB, d, th):
	'''
	traverse through database until 
	cohesion threshold is passed
	'''

	while True:
		nC = [(pattern_crimeS(iP, c, d=d), c) for c in DB].sorted(key=[0]) # get the most similar crime #TODO:implement smart alg
		if cohesion(iP + [nC]))>th:
			iP.append(nC)
		else:
			break
	return iP


if __name__ == '__main__':
	main()
