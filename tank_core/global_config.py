# -*- coding: utf-8 -*-
'''
This file contains parameter bounds &
necessary parameter defination  and variables
'''

import numpy as np

# Basin - TANK

'''
Parameter order & description of vertical tanks:

t0 (6)
    - is  : initial storage
    - boc : bottom outlet coefficient
    - soc : side outlet coefficient [2]
        - uo : upper outlet
        - lo : lower outlet
    - soh : side outlet height [2]
        - uo : upper outlet
        - lo : lower outlet

t1 (4)
    - is  : initial storage
    - boc : bottom outlet coefficient
    - soc : side outlet coefficient [1]
    - soh : side outlet height [1]
t2 (4)
    - is  : initial storage
    - boc : bottom outlet coefficient
    - soc : side outlet coefficient [1]
    - soh : side outlet height [1]

t3 (2)
    - is  : initial storage
    - soc : side outlet coefficient [1]
'''

tank_param_bounds = {
    # tank-0
    "t0_is":      {"min" : 0.01, "max" : 100},
    "t0_boc":     {"min" : 0.1,  "max" : 0.5},
    "t0_soc_uo":  {"min" : 0.1,  "max" : 0.5},
    "t0_soc_lo":  {"min" : 0.1,  "max" : 0.5},
    "t0_soh_uo" : {"min" : 25,   "max" : 50 },
    "t0_soh_lo":  {"min" : 0,    "max" : 20 },

    # tank-1
    "t1_is":      {"min" : 0.01, "max" : 100},
    "t1_boc":     {"min" : 0.01, "max" : 0.5},
    "t1_soc":     {"min" : 0.01, "max" : 0.5},
    "t1_soh":     {"min" : 0,    "max" : 50 },
    
    # tank-2
    "t2_is":      {"min" : 0.01, "max" : 100},
    "t2_boc":     {"min" : 0.01, "max" : 0.5},
    "t2_soc":     {"min" : 0.01, "max" : 0.5},
    "t2_soh":     {"min" : 0,    "max" : 50 },
    
    # tank-3
    "t3_is":      {"min" : 0.01, "max" : 100},
    "t3_soc":     {"min" : 0.01, "max" : 0.5}
}



tank_lb = np.array([
    # [Tank-0] 
    tank_param_bounds['t0_is']['min'],
    tank_param_bounds['t0_boc']['min'],
    tank_param_bounds['t0_soc_uo']['min'],
    tank_param_bounds['t0_soc_lo']['min'],
    tank_param_bounds['t0_soh_uo']['min'],
    tank_param_bounds['t0_soh_lo']['min'],
            
    # [Tank-1]
    tank_param_bounds['t1_is']['min'],
    tank_param_bounds['t1_boc']['min'],
    tank_param_bounds['t1_soc']['min'],
    tank_param_bounds['t1_soh']['min'],
            
    # [Tank-2]
    tank_param_bounds['t2_is']['min'],
    tank_param_bounds['t2_boc']['min'],
    tank_param_bounds['t2_soc']['min'],
    tank_param_bounds['t2_soh']['min'],
            
    # [Tank-3]
    tank_param_bounds['t3_is']['min'],
    tank_param_bounds['t3_soc']['min'],

])



tank_ub = np.array([ 
    # [Tank-0] 
    tank_param_bounds['t0_is']['max'],
    tank_param_bounds['t0_boc']['max'],
    tank_param_bounds['t0_soc_uo']['max'],
    tank_param_bounds['t0_soc_lo']['max'],
    tank_param_bounds['t0_soh_uo']['max'],
    tank_param_bounds['t0_soh_lo']['max'],
            
    # [Tank-1]
    tank_param_bounds['t1_is']['max'],
    tank_param_bounds['t1_boc']['max'],
    tank_param_bounds['t1_soc']['max'],
    tank_param_bounds['t1_soh']['max'],
            
    # [Tank-2]
    tank_param_bounds['t2_is']['max'],
    tank_param_bounds['t2_boc']['max'],
    tank_param_bounds['t2_soc']['max'],
    tank_param_bounds['t2_soh']['max'],
            
    # [Tank-3]
    tank_param_bounds['t3_is']['max'],
    tank_param_bounds['t3_soc']['max'],
])

# Chanel - MUSKINGUM

muskingum_param_bound = {
    "k" : {"min": 0, "max": 5},
    "x" : {"min": 0, "max": 0.5}

}

muskingum_lb = np.array([
    muskingum_param_bound["k"]["min"],
    muskingum_param_bound["x"]["min"],
])


muskingum_ub = np.array([
    muskingum_param_bound["k"]["max"],
    muskingum_param_bound["x"]["max"],
])


TANK_PARAMETER_ORDER = [
    # T-0
    't0_is', 't0_boc', 't0_soc_uo', 't0_soc_lo', 't0_soh_uo', 't0_soh_lo', 
    #T-1
    't1_is', 't1_boc', 't1_soc', 't1_soh', 
    #T-2
    't2_is', 't2_boc', 't2_soc', 't2_soh', 
    #T-3
    't3_is', 't3_soc'
]

MUSKINGUM_PARAMETER_ORDER = ['k', 'x']

NUM_PARAMETER = {
    'Subbasin': len(TANK_PARAMETER_ORDER),
    'Reach': len(MUSKINGUM_PARAMETER_ORDER)
}

DATE_FMT = '%Y-%m-%dT%H:%M:%S.%fZ'
FLOAT_FMT = '%.3f'