# -*- coding: utf-8 -*-
'''
Necessary file i/o helper functions 
- for reading files
- checking time consistancy of input files
'''
import numpy as np
import pandas as pd 
import json
import os
from datetime import datetime as dt

from . import global_config as gc

def read_ts_file(file_path:str, check_time_diff:bool=True)-> tuple:
    '''
        reads model input/output timeseries files (precip, et, discharge, result etc.)
        returns tuple(dataframe, del_time[seconds])
    '''

    # read file as pandas dataframe
    df = pd.read_csv(
        file_path,
        index_col=['Time'],
        parse_dates= True  # will parse index for datetime
    )
    
    # sort by time
    df = df.sort_index()
    
    # check if missing date
    t_diff = np.diff(df.index.to_numpy(), n=1)

    if check_time_diff and not np.all(t_diff==t_diff[0]):
        raise Exception('Time difference is not equal, possible missing/irregular dates')

    return (df , t_diff[0] ) if check_time_diff else (df, None)


def write_ts_file(df:pd.DataFrame,file_path:str)->int:

    '''
    writes model input/output timeseries files (precip, et, discharge, result etc.)
    returns 
    '''

    status  = df.to_csv(
        file_path,
        float_format=gc.FLOAT_FMT,
        date_format=gc.DATE_FMT,
        index=True,
        index_label='Time'
    )

    return status

def read_project_file(project_file:str)->dict:

    if not os.path.exists(project_file):
        raise Exception('provided project file doesnt exists')

    with open(project_file,'r') as pfrb:
        
        project = json.load(pfrb)

        # check if project file is okay

        # check if basin file is  okay


        return project 

    return None
        
def read_basin_file(basin_file:str)->dict:

    if not os.path.exists(basin_file):
        raise Exception('provided basin file doesnt exists')

    with open(basin_file,'r') as basin_file_rd_buffer:
        
        basin = json.load(basin_file_rd_buffer)

        # check if basin file is  okay [will work on it later]

        return basin 

    



