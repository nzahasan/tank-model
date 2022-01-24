'''
Necessary cost function for model calibration and validation
    R2:
        Pearson’s correlation coefficient(R) squared
        Range [0 to 1]
        Higher is better maximum possible value =1
    
    NSE: 
        Nash-Sutcliffe Efficiency coefficient
        Range [-inf to 1]
        NSE value 1 means a perfect model
        NSE > 0.6 is considerd as a good model.
    
    MSE: 
        Mean Squared Error
        Lower is better
    
    RMSE:    
        Root Mean Squared Error
        squared root of MSE
        Lower is better
'''

import numpy as np
from tank_core.tank_basin import shape_alike

def R2(x:np.ndarray, y:np.ndarray)->float:
    '''
        Pearson correlation coefficient (R^2)
    '''
    # check & calculate sample shape
    if shape_alike(x,y):
        n = x.shape[0]
    else:
        raise Exception('shape mismatch between x and y')

    NU = (n * ((x*y).sum()) - (x.sum()) * (y.sum()))**2
    DE = (n * ((x**2).sum()) - (x.sum())**2 ) * ( n * ((y**2).sum()) - (y.sum())**2 ) 

    return NU/DE


def NSE(sim:np.ndarray, obs:np.ndarray)->float:
    '''
        Nash Schutliff Efficiency (NSE) coefficient
    '''
    # N.B. sim and obs is not interchangeable for NSE

    if not shape_alike(sim,obs):
        raise Exception('shape mismatch between x and y')

    return 1 - ( ((sim - obs)**2).sum() / ((obs-obs.mean())**2).sum() )

def MSE(x:np.ndarray, y:np.ndarray)->float:
    '''
        Mean squared error
    '''
    if not shape_alike(x,y): 
        raise Exception('shape mismatch between x and y')

    return ((x - y)**2).sum() / x.shape[0]

def RMSE(x:np.ndarray, y:np.ndarray)->float:
    '''
        Root mean squared error = sqrt(mse)
    '''

    if not shape_alike(x,y):
        raise Exception('shape mismatch between x and y')

    return np.sqrt(MSE(x,y))
