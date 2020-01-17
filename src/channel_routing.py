#! /usr/bin/env python3

import numpy as np 


def muskingum(in_flow,del_t,k,x):

	'''
	Returns routed flow using Muskingum routing method
	(Lumped channel routing)
	
	Units:
	------
	in_flow  - m^3/s
	del_t    - hr
	x        - hr

	'''

	# calculate timesetp
	time_step = in_flow.shape[0]
	
	# create a zero array of out_flow
	out_flow = np.zeros(time_step)

	C0 = (-k*x+0.5*del_t) / (k-k*x+0.5*del_t)
	C1 = ( k*x+0.5*del_t) / (k-k*x+0.5*del_t)
	C2 = 1- (C0+C1)

	for t in range(time_step):

		if t==0: 
			out_flow[t] = in_flow[t]
		
		if t>0:
			out_flow[t] = C0*in_flow[t] + C1*in_flow[t-1] + C2*out_flow[t-1]

	return out_flow

