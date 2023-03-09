
# from tank_core import tank_basin as TM
# import pylab as pl
# import pandas as pd 
# import numpy as np

# def main():
    


#     data = pd.read_csv('../sample_data/tank_sample_data.csv')
#     rf = data['Pr'].values
#     et = data['ET'].values
#     obsQ = data['Q'].values
#     area = 2000
#     delTime = 24

#     # calibrate & save the prameters
#     # param = TM.calibrate(rf,et,area,delTime,obsQ)
#     # np.savez('model_data.npz',param=param)
    
#     param = np.load('model_data.npz')['param']
#     simQ = TM.tankDischarge(rf,et,param,area,delTime)

#     pl.plot(simQ,label='sim')
#     pl.plot(obsQ,label='obs')
#     pl.legend()
#     pl.show()
    


# if __name__ == '__main__':
#     main()