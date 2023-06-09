# -*- coding: utf-8 -*-
'''
This file contains parameter bounds &
necessary parameter definition  and variables
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

tank_param_bounds:dict = {
    # tank-0
    "t0_is":     {"min" : 0.01, "max" : 100},
    "t0_boc":    {"min" : 0.1,  "max" : 0.5},
    "t0_soc_uo": {"min" : 0.1,  "max" : 0.5},
    "t0_soc_lo": {"min" : 0.1,  "max" : 0.5},
    "t0_soh_uo": {"min" : 75,   "max" : 100},
    "t0_soh_lo": {"min" : 0,    "max" : 50},

    # tank-1
    "t1_is":  {"min" : 0.01, "max" : 100},
    "t1_boc": {"min" : 0.01, "max" : 0.5},
    "t1_soc": {"min" : 0.01, "max" : 0.5},
    "t1_soh": {"min" : 0,    "max" : 100},
    
    # tank-2
    "t2_is":  {"min" : 0.01, "max" : 100},
    "t2_boc": {"min" : 0.01, "max" : 0.5},
    "t2_soc": {"min" : 0.01, "max" : 0.5},
    "t2_soh": {"min" : 0,    "max" : 100},
    
    # tank-3
    "t3_is":  {"min" : 0.01, "max" : 100},
    "t3_soc": {"min" : 0.01, "max" : 0.5}
}


# tank parameter lower bounds
tank_lb:np.ndarray = np.array([
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


# tank parameter upper bounds
tank_ub:np.ndarray = np.array([ 
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

muskingum_param_bound:dict = {
    "k" : {"min": 0, "max": 5},
    "x" : {"min": 0, "max": 0.5}

}

# muskingum parameter lower bounds
muskingum_lb:np.ndarray = np.array([
    muskingum_param_bound["k"]["min"],
    muskingum_param_bound["x"]["min"],
])

# muskingum parameter upper bounds
muskingum_ub:np.ndarray = np.array([
    muskingum_param_bound["k"]["max"],
    muskingum_param_bound["x"]["max"],
])

# order of tank parameter in parameter-array
TANK_PARAMETER_ORDER:list = [
    # T-0
    't0_is', 't0_boc', 't0_soc_uo', 't0_soc_lo', 't0_soh_uo', 't0_soh_lo', 
    # T-1
    't1_is', 't1_boc', 't1_soc', 't1_soh', 
    # T-2
    't2_is', 't2_boc', 't2_soc', 't2_soh', 
    # T-3
    't3_is', 't3_soc'
]

# order of muskingum parameter in parameter-array
MUSKINGUM_PARAMETER_ORDER:list = ['k', 'x']

# total number fo parameter for basin & channel nodes
NUM_PARAMETER:dict = {
    'Subbasin': len(TANK_PARAMETER_ORDER),
    'Reach': len(MUSKINGUM_PARAMETER_ORDER)
}

# project file io time format
DATE_FMT:str = '%Y-%m-%dT%H:%M:%S.%f%z'

# project file io float format
FLOAT_FMT:str = '%.3f'