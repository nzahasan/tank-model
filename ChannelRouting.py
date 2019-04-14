#! /usr/bin/env python3

import numpy as np 


def Muskingum(inflow,delT,K,X):

	'''
	Returns routed flow using Muskingum routing method
	(Lumped channel routing)
	
	Units:
	------
	inflow - m^3/s
	delT   - hr
	X      - hr

	'''

	# calculate timesetp
	timeStep = inflow.shape[0]
	
	# create a zero array of outflow
	outFlow = np.zeros(timeStep)

	C0 = (-K*X+0.5*delT)/(K-K*X+0.5*delT)
	C1 = ( K*X+0.5*delT)/(K-K*X+0.5*delT)
	C2 = 1- (C0+C1)

	for t in range(timeStep):

		if t==0: 
			outFlow[t] = inflow[t]
		
		if t>0:
			outFlow[t] = C0*inflow[t] + C1*inflow[t-1] + C2*outFlow[t-1]

	return outFlow

