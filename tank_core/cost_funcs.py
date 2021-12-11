'''
Necessary cost function for model calibration and validation
    R2:
        Pearson’s correlation coefficient(R) squared
        Range [0 to 1]
        higher is better maximum possible value =1
    
    NSE: 
        Nash-Sutcliffe Efficiency coefficienct
        Range [-inf to 1]
        NSE value 1 means a perfect model
        NSE > 0.6 is considerd as a good model.
    
    MSE: 
        Mean Squared Error
        lower is better
    
    RMSE:    
        Root Mean Squared Error
        squared root of MSE
        lower is better
'''

import numpy as np
from tank_core.tank_compute import shape_alike

def R2(x,y):
    '''
        Pearson correlation coefficient
    '''
    # check & calculate sample shape
    if shape_alike(x,y):
        n = x.shape[0]
    else:
        return -1

    NU = (n * ((x*y).sum()) - (x.sum()) * (y.sum()))**2
    DE = (n * ((x**2).sum()) - (x.sum())**2 ) * ( n * ((y**2).sum()) - (y.sum())**2 ) 

    return NU/DE


def NSE(sim,obs):
    '''
        Nash Schutliff efficiency coefficient
    '''
    # N.B. sim and obs is not interchangeable for NSE

    if not shape_alike(sim,obs): return -1

    return 1 - ( ((sim - obs)**2).sum() / ((obs-obs.mean())**2).sum() )

def MSE(x,y):
    '''
        Mean squared error
    '''
    if not shape_alike(x,y): return -1

    return ((x - y)**2).sum() / x.shape[0]

def RMSE(x,y):
    '''
        Root mean squared error = sqrt(mse)
    '''

    if not shape_alike(x,y): return -1

    return np.sqrt(MSE(x,y))
