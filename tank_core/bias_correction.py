# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import NamedTuple
import numpy as np
from scipy.stats import gamma


class GammaParam(NamedTuple):
    a: float = np.nan   # shape
    b: float = np.nan   # scale
    c: float = np.nan   # dry day fraction


class gqm:

    '''
    Gamma Quantile Mapping
    ----------------------
    Parametric bias correction of daily precipitation

    Piani, C., Haerter, J. O., & Coppola, E. (2010). Statistical bias
    correction for daily precipitation in regional climate models over
    Europe. Theor Appl Climatol, 99, 187-192.
    https://doi.org/10.1007/s00704-009-0134-9

    dry days and wet day gamma combined as bernoulli-gamma cdf:

    F(x) = C + (1 - C) * G(x)

    transfer function:
    :: F_obs = F_sim
    => C_obs + (1-C_obs) * G(obs) = F(sim)
    => G(obs) = ( F_sim - C_obs ) / (1 - C_obs)
    => obs = G_obs^-1 [ ( F_sim - C_obs ) / (1 - C_obs) ]

    >> obs = 0, if F(sim) <= C_obs or sim is dry

    here, C_sim/C_obs = fraction of dry days, G = gamma cdf of wet days

    :: in gamma fit force location parameter to 0

    '''


    def __init__(self):

        self.obs_param = GammaParam()
        self.sim_param = GammaParam()
        self.wet_threshold = 0.01

    def fit(self,obs_data,sim_data, wet_threshold=0.01):

        self.wet_threshold = wet_threshold

        #: estimates parameters from provided data
        #: dry day fraction
        obs_c = (obs_data[obs_data<=wet_threshold].shape[0]) / (obs_data.shape[0])
        sim_c = (sim_data[sim_data<=wet_threshold].shape[0]) / (sim_data.shape[0])

        #: fit gamma with non zero values with floc=0
        obs_a, _, obs_b = gamma.fit(obs_data[obs_data>wet_threshold], floc=0)
        sim_a, _, sim_b = gamma.fit(sim_data[sim_data>wet_threshold], floc=0)

        self.obs_param = GammaParam(obs_a, obs_b, obs_c)
        self.sim_param = GammaParam(sim_a, sim_b, sim_c)

        return self

    def set_params(self,obs_param_arr:np.ndarray, sim_param_arr:np.ndarray)->object:

        self.obs_param = GammaParam(*obs_param_arr[:3])
        self.sim_param = GammaParam(*sim_param_arr[:3])

        return self

    def correct(self,simVal:float|np.ndarray) -> float|np.ndarray :

        simVal = np.asarray(simVal, dtype=float)
        C_obs = self.obs_param.c
        C_sim = self.sim_param.c

        # caluclate G_obs following transfer function
        G_sim = gamma.cdf(simVal, a=self.sim_param.a, scale=self.sim_param.b, loc=0)

        F_sim = C_sim + (1 - C_sim) * G_sim

        G_obs = (F_sim - C_obs) / (1 - C_obs)

        # clip gamma cdf value between [0,1]
        G_obs = np.clip(G_obs, 0, 1)

        # inverse gamma to get obs/corrected
        corrVal = gamma.ppf(G_obs,a=self.obs_param.a, scale=self.obs_param.b, loc=0)

        # simulated dry days stay dry
        corrVal = np.where(simVal <= self.wet_threshold, 0, corrVal)

        return corrVal
