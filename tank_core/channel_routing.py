import numpy as np 


def muskingum(in_flow:np.ndarray, del_t:float, k:float, x:float) -> np.ndarray:

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
	n_step = in_flow.shape[0]
	
	# create a zero array of out_flow
	out_flow = np.zeros(n_step)

	C0 = (-k*x+0.5*del_t) / (k-k*x+0.5*del_t)
	C1 = ( k*x+0.5*del_t) / (k-k*x+0.5*del_t)
	C2 = 1- (C0+C1)

	# initial condition
	out_flow[0] = in_flow[0]

	for t in np.arange(1,n_step):

		out_flow[t] = C0*in_flow[t] + C1*in_flow[t-1] + C2*out_flow[t-1]

	return out_flow

