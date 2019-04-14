
import sys
sys.path.append('../')
import numpy as np
import ChannelRouting as CR

def main():

	# subramanya example

	inflowDat = np.array([10,20,50,60,55,45,35,27,20,15])

	delT = 6
	K =12
	X = 0.2


	a = CR.Muskingum(inflowDat,delT,K,X)
	print(a)


if __name__ == '__main__':
	main()