import numpy as np
import tank_core.channel_routing as cr

def test_muskingum():

	inflowDat = np.array([10,20,50,60,55,45,35,27,20,15])

	delT = 6
	K = 12
	X = 0.2

	a = cr.muskingum(inflowDat,delT,K,X)
