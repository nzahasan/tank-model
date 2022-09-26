# -*- coding: utf-8 -*-
'''
Collection of some utility function
'''

import numpy as np
from .global_config import TANK_PARAMETER_ORDER

def shape_alike(x:np.ndarray,y:np.ndarray) -> bool:
    # checks if x,y numpy array are of same shape
    return True if x.shape == y.shape else False


def tank_param_list2dict(parameters:list)->dict:

    parameter_dict = dict()

    for i,parameter_name in enumerate(TANK_PARAMETER_ORDER):

        parameter_dict[parameter_name] = parameters[i]
    
    return parameter_dict



def tank_param_dict2list(parameters:dict)->list:

    parameter_list = list()

    for parameter_name in TANK_PARAMETER_ORDER:

        parameter_list.append(parameters[parameter_name])
    
    return parameter_list


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

def check_time_delta(dt_pr, dt_et, del_t_proj)->float:
    # check for project time interval(in hour) with pr and et time interval
    # returns del_t in hours
    
    del_t = del_t_proj

    if dt_pr != dt_et:
        raise Exception ('Interval mismatch between PR and ET input files')
    
    dt_pr_hr = dt_pr.total_seconds() / 3600

    if del_t_proj != dt_pr_hr :

        print('WARNING: Project interval doesnt match with timeseries interval\n:::::::> computing with input timeseries interval')

        del_t = dt_pr_hr
    
    return del_t
