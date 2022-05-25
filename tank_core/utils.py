'''Collection of some utility function'''

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
