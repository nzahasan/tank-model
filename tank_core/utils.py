# -*- coding: utf-8 -*-
'''
Collection of some utility function
'''

import numpy as np
from .global_config import TANK_PARAMETER_ORDER

def shape_alike(x:np.ndarray,y:np.ndarray) -> bool:
    # checks if x,y numpy array are of same shape
    return True if x.shape == y.shape else False

# @marked for removal
def tank_param_list2dict_(parameters:list)->dict:

    parameter_dict = dict()

    for i,parameter_name in enumerate(TANK_PARAMETER_ORDER):

        parameter_dict[parameter_name] = parameters[i]
    
    return parameter_dict


# @marked for removal
def tank_param_dict2list_(parameters:dict)->list:

    parameter_list = list()

    for parameter_name in TANK_PARAMETER_ORDER:

        parameter_list.append(parameters[parameter_name])
    
    return parameter_list

def tank_param_list2dict(parameters:list)->dict:
    # converts flattened parameter to a dict based on TANK_PARAMETER_ORDER
    
    return {
        parameter_name:parameters[i] 
        for i,parameter_name in enumerate(TANK_PARAMETER_ORDER) 
    }


def tank_param_dict2list(parameters:dict)->list:
    # returns a list of flattened parameter following TANK_PARAMETER_ORDER
    return [ 
        parameters[parameter_name] 
        for parameter_name in TANK_PARAMETER_ORDER
    ]


def muskingum_param_list2dict(parameters:list)->dict:

    return {
        "k" : parameters[0],
        "x" : parameters[1],
    }

def muskingum_param_dict2list(parameters:dict)->list:

    return [
        parameters["k"], 
        parameters["x"], 
    ]

def check_time_delta(delt_pr, delt_et, delt_proj)->float:
    # check for project time interval(in hour) with pr and et time interval
    # returns del_t in hours
    
    del_t = delt_proj

    if delt_pr != delt_et:
        raise Exception ('Interval mismatch between PR and ET input files')
    
    delt_pr_hr = delt_pr.total_seconds() / 3600

    if delt_proj != delt_pr_hr :

        print('WARNING: Project interval doesn\'t match with time-series interval\n:::::::> computing with input timeseries interval')

        del_t = delt_pr_hr
    
    return del_t
