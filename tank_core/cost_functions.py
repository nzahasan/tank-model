# -*- coding: utf-8 -*-
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
        NSE > 0.6 is considered as a good model.
    
    MSE: 
        Mean Squared Error
        Lower is better
    
    RMSE:    
        Root Mean Squared Error
        squared root of MSE
        Lower is better
    
    PBIAS:
        Percent bias
        Lower is better 
        +ve values indicate underestimation
        -ve values indicate model overestimation
'''

import numpy as np
from .utils import shape_alike

def R2(x:np.ndarray, y:np.ndarray)->float:
    '''
    Pearson correlation coefficient (R^2)
    '''
    # check & calculate sample shape
    if not shape_alike(x,y):
        raise Exception('shape mismatch between x and y')
    
    n = x.shape[0]

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

    obs_mean = obs.mean()

    return 1 - (  np.square( obs - sim).sum() / np.square(obs-obs_mean).sum() )

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

def PBIAS(obs:np.ndarray, sim:np.ndarray)->float:
    '''
    Percentage Bias
    '''
    if not shape_alike(sim,obs):
        raise Exception('shape mismatch between x and y')
    
    return (obs-sim).sum() * 100 / obs.sum()