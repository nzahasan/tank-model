#! /usr/bin/env python3

import numpy as np
from scipy.stats import gamma


class gqm(object):
    
    '''
    Gamma Quantile Mapping (Piani et.el. 2009)
    ------------------------------------------
    Parametric bias correction using gamma distribution

    cdf(obs) + C_obs = cdf(sim) + C_sim
    cdf(obs) = cdf(sim) + C_sim - C_obs
    cdf(obs) = cdf(sim) + delC
     
    >> obs = cdf^-1 [ cdf(sim) + delC ]
    
    here, C_sim/C_obs = fraction of dry days / days with 0 rainfall
    
    :: in gamma fit force location parameter to 0
    '''
    def __init__(self):

        self.obs_param = {'a':None,'b':None,'c':None}
        self.sim_param = {'a':None,'b':None,'c':None}
     
    def fit(self,obs_data,sim_data):

        #: estimates parameters from provided data
        #: dry day fraction
        self.obs_param['c'] = (obs_data[obs_data==0].shape[0]) / (obs_data.shape[0])  
        self.sim_param['c'] = (sim_data[sim_data==0].shape[0]) / (sim_data.shape[0])

        #: fit gamma with non zero values with floc=0
        self.obs_param['a'], _, self.obs_param['b'] = gamma.fit(obs_data[obs_data>0], floc=0)
        self.sim_param['a'], _, self.sim_param['b'] = gamma.fit(sim_data[sim_data>0], floc=0)
        
        
        return self

    def set_params(self,obs_param_arr,sim_param_arr):

        self.obs_param['a'] = obs_param_arr[0]
        self.obs_param['b'] = obs_param_arr[1]
        self.obs_param['c'] = obs_param_arr[2]

        self.sim_param['a'] = sim_param_arr[0]
        self.sim_param['b'] = sim_param_arr[1]
        self.sim_param['c'] = sim_param_arr[2]

        return self

    def correct(self,simVal):
        
        delC = self.sim_param['c']-self.obs_param['c']
        simValCDF = gamma.cdf(simVal,a=self.sim_param['a'],scale=self.sim_param['b'],loc=0)
        
        #: return the bias corrected value
        return gamma.ppf( (simValCDF + delC),a=self.obs_param['a'], scale=self.obs_param['b'], loc=0)
