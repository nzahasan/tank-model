# -*- coding: utf-8 -*-
'''
Necessary file i/o helper functions 
- for reading files
- checking time consistency of input files
'''
import numpy as np
import pandas as pd 
import json
import os
from datetime import datetime as dt
from pathlib import Path

from . import global_config as gc, utils

def read_ts_file(file_path:str, check_missing:bool=True, start:str|None=None, end:str|None=None)-> tuple:
    '''
        reads model input/output timeseries files (precip, et, discharge, result etc.)
        optional filtering between start/end date strings matching gc.DATE_FMT
        returns tuple(dataframe, del_time[seconds])
    '''


    # read file as pandas dataframe
    df = pd.read_csv(
        file_path,
        index_col = 'Time',
        parse_dates = True,  # will parse index for datetime
        date_format = gc.DATE_FMT,
    )

    # sort by time
    df = df.sort_index()

    # filter the dataframe
    df = utils.trim_df(df, start, end)

    # warn if no data found in the requested range
    if df.empty:
        raise ValueError('No data found within the requested date range')
    
    # check if missing date
    t_diff = np.diff(df.index, n=1)
    del_t = t_diff[0] if len(t_diff) else None

    if check_missing:
        if del_t is None:
            raise ValueError('Not enough data points to evaluate time difference')
        if not np.all(t_diff==del_t):
            raise Exception('Time difference is not equal, possible missing/irregular dates')

    return (df , del_t ) if check_missing else (df, None)


def write_ts_file(df:pd.DataFrame,file_path:str)->None:

    '''
    writes model input/output timeseries files (precip, et, discharge, result etc.)
    returns 
    '''
    # abort if index name is not Time
    if df.index.name != 'Time':
        raise Exception('Error: invalid time-series data no Time index found')

    status  = df.to_csv(
        file_path,
        float_format=gc.FLOAT_FMT,
        date_format=gc.DATE_FMT,
        index=True,
        index_label='Time'
    )

    return status

def check_project(project:dict, project_dir:Path, check_discharge_file:bool)->tuple:

    input_keys = ["basin", "precipitation", "evapotranspiration" ]
    if check_discharge_file: 
        input_keys.append('discharge')
    
    # check if mandatory keys are present in the project definition
    mandatory_keys = ["interval" , *input_keys]

    for k in mandatory_keys:
        if k not in project.keys():
            return (False, f'Missing mandatory field {k} in project file')
    
    fract_intervals = [0.25, 0.5, 0.75]

    # check if time interval is okay
    interval_ok = ( 
        (
            project['interval'] > 0
        ) 
        and 
        ( 
            (project['interval'] in fract_intervals) or  project['interval'].is_integer() 
        ) 
    )
    
    if not interval_ok :
        return (False, f'invalid interval {project["interval"]} hr')
    
    # check if files of input_keys are present
    for k in input_keys:
        if not os.path.exists(project_dir /  project[k]):
            return (False, f'no file for {k} found in project directory')

    return (True, 'All checks passed')

def read_project_file(project_file:str, check_discharge_file=False)->dict:

    if not os.path.exists(project_file):
        raise Exception('provided project file doesn\'t exists')

    with open(project_file,'r') as pfrb:
        
        project = json.load(pfrb)

        # check if project file is okay
        project_dir = Path(project_file).resolve().parent
        check_ok, msg = check_project(project, project_dir, check_discharge_file)

        if check_ok == False:
            raise Exception(msg)

        return project 


def read_basin_file(basin_file:str)->dict:

    if not os.path.exists(basin_file):
        raise Exception('provided basin file doesn\'t exists')

    with open(basin_file,'r') as basin_file_rd_buffer:
        
        basin = json.load(basin_file_rd_buffer)

        # check if basin file is  okay [will work on it later, 
        # basically check for missing link

        return basin 


