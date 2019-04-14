#! /usr/bin/env python3

import numpy as np
from scipy.stats import gamma


class GQM(object):
    
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

        self.obsParam = {'a':None,'b':None,'c':None}
        self.simParam = {'a':None,'b':None,'c':None}
     
    def fit(self,obsData,simData):

        #: estimates parameters from provided data
        #: dry day fraction
        self.obsParam['c'] = (obsData[obsData==0].shape[0]) / (obsData.shape[0])  
        self.simParam['c'] = (simData[simData==0].shape[0]) / (simData.shape[0])

        #: fit gamma with non zero values with floc=0
        self.obsParam['a'], _, self.obsParam['b'] = gamma.fit(obsData[obsData>0], floc=0)
        self.simParam['a'], _, self.simParam['b'] = gamma.fit(simData[simData>0], floc=0)
        
        
        return self

    def setParams(self,obsParamArr,simParamArr):

        self.obsParam['a'] = obsParamArr[0]
        self.obsParam['b'] = obsParamArr[1]
        self.obsParam['c'] = obsParamArr[2]

        self.simParam['a'] = simParamArr[0]
        self.simParam['b'] = simParamArr[1]
        self.simParam['c'] = simParamArr[2]

        return self

    def correct(self,simVal):
        
        delC = self.simParam['c']-self.obsParam['c']
        simValCDF = gamma.cdf(simVal,a=self.simParam['a'],scale=self.simParam['b'],loc=0)
        
        #: return the bias corrected value
        return gamma.ppf( (simValCDF + delC),a=self.obsParam['a'], scale=self.obsParam['b'], loc=0)
