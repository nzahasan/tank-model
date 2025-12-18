# -*- coding: utf-8 -*-
'''
Collection of some utility function
'''

import numpy as np
import pandas as pd
from datetime import datetime as dt

from . import global_config as gc

def shape_alike(x:np.ndarray,y:np.ndarray) -> bool:
    # checks if x,y numpy array are of same shape
    return True if x.shape == y.shape else False

# @marked for removal
def tank_param_list2dict_(parameters:list)->dict:

    parameter_dict = dict()

    for i,parameter_name in enumerate(gc.TANK_PARAMETER_ORDER):

        parameter_dict[parameter_name] = parameters[i]
    
    return parameter_dict


# @marked for removal
def tank_param_dict2list_(parameters:dict)->list:

    parameter_list = list()

    for parameter_name in gc.TANK_PARAMETER_ORDER:

        parameter_list.append(parameters[parameter_name])
    
    return parameter_list

def tank_param_list2dict(parameters:list)->dict:
    # converts flattened parameter to a dict based on gc.TANK_PARAMETER_ORDER
    
    return {
        parameter_name:parameters[i] 
        for i,parameter_name in enumerate(gc.TANK_PARAMETER_ORDER) 
    }


def tank_param_dict2list(parameters:dict)->list:
    # returns a list of flattened parameter following gc.TANK_PARAMETER_ORDER
    return [ 
        parameters[parameter_name] 
        for parameter_name in gc.TANK_PARAMETER_ORDER
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


def get_delt(delt_pr, delt_et)->float:
    # returns delt in hours
    # also checks if delt for both is equal also

    if delt_pr != delt_et:
        raise Exception ('Interval mismatch between PR and ET input files')
    
    delt_pr_hr = delt_pr.total_seconds() / 3600

    return delt_pr_hr 

def get_sim_start_end(precipitation, evapotranspiration)->tuple[str, str]:
    # validates both indexes are identical and returns start/end timestamps
    if len(precipitation) == 0 or len(evapotranspiration) == 0:
        raise ValueError('Empty precipitation or evapotranspiration time-series')

    if len(precipitation) != len(evapotranspiration):
        raise ValueError('Mismatched precipitation and evapotranspiration record counts')

    try:
        same_index = precipitation.equals(evapotranspiration)
    except AttributeError:
        same_index = np.array_equal(np.asarray(precipitation), np.asarray(evapotranspiration))

    if not same_index:
        raise ValueError('Time indexes of precipitation and evapotranspiration do not match')

    start = precipitation[0]
    end = precipitation[-1]

    if isinstance(start, dt):
        start_str = start.strftime(gc.DATE_FMT)
        end_str = end.strftime(gc.DATE_FMT)
    else:
        start_str = str(start)
        end_str = str(end)

    return start_str, end_str


def parse_date_str(date_str:str, label:str|None=None)->dt:
    # checks if date string is in proper format
    try:
        return dt.strptime(date_str, gc.DATE_FMT)
    except ValueError:
        raise ValueError(f'Invalid date format {date_str} {f"of {label}" if label else ""}, expected format: {gc.DATE_FMT}')

def trim_df(df:pd.DataFrame, start:str|None, end:str|None)->pd.DataFrame:
    # trims dataframe based on start/end datetime strings
    if start is not None:
        df = df.loc[df.index >= parse_date_str(start,'start')]

    if end is not None:
        df = df.loc[df.index <= parse_date_str(end,'end')]
    
    return df