# -*- coding: utf-8 -*-
'''
Helper functions for computation
'''
import numpy as np
import pandas as pd
from queue import Queue
from scipy.optimize import minimize
from .tank_basin import tank_discharge
from .channel_routing import muskingum
from . import utils
from .cost_functions import PBIAS, R2, RMSE, NSE, MSE, PBIAS
from . import global_config as gc



def check_input_consistancy(precipitation, evapotranspiration, del_t, start_time, end_time):

    '''
    Check input data consistancy
    '''

    pass


def build_computation_stack(project:dict) -> list:

    '''
        Traverse project tree and build computation stack
        First traverse the tree with queue(fifo) ass all the 
        upstream node needs to be computed before computing
        a specific node, while traversing node put them in stack

        N.B. Upstream is clild node.
    '''
    computation_stack = []

    node_qeue = Queue()

    # enque root note
    for root_node in project['root_node']:
        node_qeue.put(root_node)

    while not node_qeue.empty():

        # deque node
        node = node_qeue.get()

        # add node to the top of computation stack
        computation_stack.append(node)

        # get child nodes and enque child nodes
        if project['basin_def'][node].get('upstream',False):
            childs = project['basin_def'][node]['upstream']

            for child in childs:
                node_qeue.put(child)

    return computation_stack

# computation

def compute_project(basin:dict, precipitation:pd.DataFrame, 
                    evapotranspiration:pd.DataFrame, del_t:float)->pd.DataFrame:
    
    '''
    Computes project for provided precipitation and evapotranspiration data
    
    Caveats: 
        - assumes all kind of timestep check has been completed
        - and contains no null data or missing data
    '''
    computation_stack = build_computation_stack(basin)
    
    n_step = len(precipitation.index)
    
    computation_result = pd.DataFrame()

    computation_result.index = precipitation.index

    while len(computation_stack) > 0:

        # pop node from top of the node
        curr_node_name = computation_stack.pop()

        curr_node_def = basin['basin_def'][curr_node_name]

        if curr_node_def['type'] == 'Subbasin':
            
             
            computation_result[curr_node_name] = tank_discharge(
                precipitation = precipitation[curr_node_name].to_numpy(),
                evapotranspiration = evapotranspiration[curr_node_name].to_numpy(), 
                del_t = del_t,
                area = curr_node_def['area'],
                ** curr_node_def['parameters']
            )
            
        elif curr_node_def['type'] == 'Reach':

            sum_node = np.zeros(n_step, dtype=np.float64)
            
            for us_node_name in curr_node_def['upstream']:
                sum_node += muskingum( 
                    in_flow= computation_result[us_node_name].to_numpy(),
                    del_t=del_t,
                    ** curr_node_def['parameters']
                )

            computation_result[curr_node_name] = sum_node
            

        elif curr_node_def['type'] in ['Sink','Junction']:

            

            sum_node = np.zeros(n_step, dtype=np.float64)
            
            for us_node_name in curr_node_def['upstream']:
                sum_node += computation_result[us_node_name].to_numpy()
            
            computation_result[curr_node_name] = sum_node

    return computation_result
    
    


def compute_statistics(basin:dict, result:pd.DataFrame, discharge:pd.DataFrame)->dict:

    merged = merge_obs_sim(observed=discharge, simulated=result)

    merged_keys = merged.keys()
    
    statistics = dict()
    
    for node in basin['basin_def'].keys():

        obs_key, sim_key = f'{node}_obs', f'{node}_sim'

        if obs_key in merged_keys and sim_key in merged_keys:
            statistics[node]={
                "RMSE": RMSE(merged[obs_key].to_numpy(), merged[sim_key].to_numpy()),
                "NSE" : NSE(merged[sim_key].to_numpy(), merged[obs_key].to_numpy() ),
                "R2"  : R2(merged[sim_key].to_numpy(), merged[obs_key].to_numpy() ),
                "PBIAS"  : PBIAS(sim=merged[sim_key].to_numpy(),obs=merged[obs_key].to_numpy() )
            }

    return statistics



# creates a single list of parameter stacking each nodes parameter
def parameter_stack(basin:dict)->tuple:
    '''
    Stackes all parameters into a list of a given basin
    '''
    node_order_type = []
    stacked_parameter = []
    basin_def = basin['basin_def']

    for node in basin_def.keys():

        node_type = basin_def[node]['type']
        
        if node_type in ['Subbasin', 'Reach']:
            
            if node_type == 'Subbasin':
                stacked_parameter.extend(
                    utils.tank_param_dict2list(basin_def[node]['parameters'])
                )
            
            elif node_type == 'Reach':
                stacked_parameter.extend(
                    utils.muskingum_param_dict2list(basin_def[node]['parameters'])
                )
            # append to node order
            node_order_type.append((node, node_type ))
            
                
    # node order, stacked_parameter
    return (node_order_type, stacked_parameter) 

# Unstacks parameters stacked by parameter_stack function 
def parameter_unstack(node_order_type:list, stacked_parameter:list)->dict:
    '''
    returns unstacked parameters of a basin for provided unstacked parameters
    '''
    unstacked_parameter = dict()
    
    # later have to change this if other routhing method is added
    conv_fn = {
        'Subbasin': utils.tank_param_list2dict,
        'Reach': utils.muskingum_param_list2dict
    }
    offset = 0
    for node, node_type  in node_order_type:

        num_parameter = gc.NUM_PARAMETER[node_type]
        unstacked_parameter[node] = conv_fn[node_type](stacked_parameter[offset:offset+num_parameter])
        offset += num_parameter 

        
    return unstacked_parameter

def update_basin_with_unstacked_parameter(basin:dict, unstacked_parameter:dict)->dict:
    '''
    returns updatated basin for provided unstacked parameters
    '''
    for node in unstacked_parameter.keys():
        
        basin['basin_def'][node]['parameters'] = unstacked_parameter[node]


    return basin

def update_basin_with_stacked_parameter(basin:dict, node_order_type:list, stacked_parameter:list)->dict:
    '''
    returns updatated basin for provided stacked parameters
    '''
    # check if stacked parameter length is okay
    conv_fn = {
        'Subbasin': utils.tank_param_list2dict,
        'Reach': utils.muskingum_param_list2dict
    }
    offset = 0
    for node, node_type  in node_order_type:

        num_parameter = gc.NUM_PARAMETER[node_type]
        basin['basin_def'][node]['parameters'] = conv_fn[node_type](stacked_parameter[offset:offset+num_parameter])
        offset += num_parameter
    

    return basin

def merge_obs_sim(observed:pd.DataFrame, simulated:pd.DataFrame)-> pd.DataFrame:
    ''' 
    Inner joins observed and simulated output with their indexe (time) 
    '''
    return pd.merge(
        simulated,observed, 
        how='inner', 
        left_index=True, 
        right_index=True, 
        suffixes=('_sim', '_obs')
    )
    

def stat_by_stacked_parameter(
        stacked_parameter:list, node_order_type:list, basin:dict,
        rainfall:pd.DataFrame, evapotranspiration:pd.DataFrame, 
        discharge:pd.DataFrame, del_t:float)->float:
    '''
    Returns model performance statistics for stacked parameters
    (right now set to nse only)
    '''
    updated_basin = update_basin_with_stacked_parameter(basin, node_order_type, stacked_parameter)
    
    result = compute_project(updated_basin, rainfall, evapotranspiration, del_t)

    merged = merge_obs_sim(observed=discharge, simulated=result)
    
    root_node = updated_basin['root_node'][0]
    sim_key, obs_key = f'{root_node}_sim', f'{root_node}_obs' 
    _nse = NSE(merged[sim_key].to_numpy(),merged[obs_key].to_numpy())
    

    return 1 - _nse



def optimize_project(basin:dict, 
    precipitation:pd.DataFrame, evapotranspiration:pd.DataFrame, 
    discharge:pd.DataFrame, del_t:float)->dict:
    '''
    Optimizes parameters of a basin and returns updated basin file
    '''

    node_order_type, stacked_parameter = parameter_stack(basin)
    
    upper_bound_stacked = list()
    lower_bound_stacked = list()
    
    for _, node_type in node_order_type:

        if node_type == 'Subbasin':
            
            upper_bound_stacked.extend(gc.tank_ub.tolist())
            lower_bound_stacked.extend(gc.tank_lb.tolist())

        if node_type == 'Reach':
            upper_bound_stacked.extend(gc.muskingum_ub.tolist())
            lower_bound_stacked.extend(gc.muskingum_lb.tolist())
    
    initial_guess = np.array(stacked_parameter)

    param_bounds = np.column_stack((lower_bound_stacked,upper_bound_stacked))
    
    optim_func_static_args = (node_order_type, basin,precipitation,evapotranspiration, discharge, del_t)
    optimizer = minimize(
            fun =stat_by_stacked_parameter, 
            x0 = initial_guess,
            args = optim_func_static_args,
            method ='L-BFGS-B',
            bounds =param_bounds
        )
    
    return update_basin_with_stacked_parameter(basin, node_order_type, optimizer.x)

    
