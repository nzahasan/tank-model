# -*- coding: utf-8 -*-
'''
Helper functions for computation
'''
from inspect import stack
from queue import Queue
from turtle import update
import pandas as pd
from .tank_basin import tank_discharge
from .channel_routing import muskingum

from .utils import (
    tank_param_dict2list,
    tank_param_list2dict, 
    muskingum_param_dict2list,
    muskingum_param_list2dict
)
from .cost_functions import R2, RMSE, NSE
from .global_config  import (
    NUM_PARAMETER, 
    tank_ub, tank_lb,
    muskingum_ub, muskingum_lb
)
import numpy as np

from scipy.optimize import minimize, shgo,dual_annealing

def check_input_consistancey():

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
    
    computation_stack = build_computation_stack(basin)
    
    n_step = precipitation.index.shape[0]
    
    computation_result = pd.DataFrame()

    computation_result.index = precipitation.index

    while len(computation_stack) > 0:

        # pop node from top of the node
        curr_node_name = computation_stack.pop()


        curr_node_def = basin['basin_def'][curr_node_name]

        if curr_node_def['type'] == 'Subbasin':
            
            print(curr_node_def['type'],"compute tank for basin", curr_node_name)
             
            computation_result[curr_node_name] = tank_discharge(
                precipitation = precipitation[curr_node_name].to_numpy(),
                evapotranspiration = evapotranspiration[curr_node_name].to_numpy(), 
                del_t = del_t,
                area = curr_node_def['area'],
                ** curr_node_def['parameters']
            )
            

        elif curr_node_def['type'] == 'Reach':
            print('RC','route upstream flow then sum', curr_node_def['upstream'])

            sum_node = np.zeros(n_step, dtype=np.float64)
            
            for us_node_name in curr_node_def['upstream']:
                sum_node += muskingum( 
                    in_flow= computation_result[us_node_name].to_numpy(),
                    del_t=del_t,
                    ** curr_node_def['parameters']
                )

            
            computation_result[curr_node_name] = sum_node
            

        elif curr_node_def['type'] in ['Sink','Junction']:

            print(curr_node_def['type'],'>> sum flow', curr_node_def['upstream'])

            sum_node = np.zeros(n_step, dtype=np.float64)
            
            for us_node_name in curr_node_def['upstream']:
                sum_node += computation_result[us_node_name].to_numpy()
            
            computation_result[curr_node_name] = sum_node


    

    return computation_result
    
    


def compute_statistics(basin:dict, result:pd.DataFrame, discharge:pd.DataFrame)->dict:

    # merge using index
    merged = pd.merge(
        result,discharge, 
        how='inner', 
        left_index=True, 
        right_index=True, 
        suffixes=('_sim', '_obs')
    )

    merged_keys = merged.keys()
    
    statistics = dict()
    
    for node in basin['basin_def'].keys():

        obs_key, sim_key = f'{node}_sim', f'{node}_obs'

        if obs_key in merged_keys and sim_key in merged_keys:
            statistics[node]={
                "RMSE": RMSE(merged[obs_key].to_numpy(), merged[sim_key].to_numpy()),
                "NSE" : NSE(merged[sim_key].to_numpy(), merged[obs_key].to_numpy() ),
                "R2"  : R2(merged[sim_key].to_numpy(), merged[obs_key].to_numpy() )
            }

    return statistics



# creates a single list of parameter stacking each nodes parameter
def parameter_stack(basin:dict)->tuple:

    node_order_type = []
    stacked_parameter = []
    basin_def = basin['basin_def']

    for node in basin_def.keys():

        node_type = basin_def[node]['type']
        
        if node_type in ['Subbasin', 'Reach']:
            
            if node_type == 'Subbasin':
                stacked_parameter.extend(
                    tank_param_dict2list(basin_def[node]['parameters'])
                )
            
            elif node_type == 'Reach':
                stacked_parameter.extend(
                    muskingum_param_dict2list(basin_def[node]['parameters'])
                )
            # append to node order
            node_order_type.append((node, node_type ))
            
                
    # node order, stacked_parameter
    return (node_order_type, stacked_parameter) 

# Unstacks parameters stacked by parameter_stack function 
def parameter_unstack(node_order_type:list, stacked_parameter:list)->dict:
    
    unstacked_parameter = dict()
    
    # later have to change this if other routhing method is added
    conv_fn = {
        'Subbasin': tank_param_list2dict,
        'Reach': muskingum_param_list2dict
    }
    offset = 0
    for node, node_type  in node_order_type:

        num_parameter = NUM_PARAMETER[node_type]
        unstacked_parameter[node] = conv_fn[node_type](stacked_parameter[offset:offset+num_parameter])
        offset += num_parameter 

        
    return unstacked_parameter

def update_basin_with_unstacked_parameter(basin:dict, unstacked_parameter:dict)->dict:
    print(unstacked_parameter)
    for node in unstacked_parameter.keys():
        
        basin['basin_def'][node]['parameters'] = unstacked_parameter[node]


    return basin

def update_basin_with_stacked_parameter(basin:dict, node_order_type:list, stacked_parameter:dict)->dict:
    
    conv_fn = {
        'Subbasin': tank_param_list2dict,
        'Reach': muskingum_param_list2dict
    }
    offset = 0
    for node, node_type  in node_order_type:

        num_parameter = NUM_PARAMETER[node_type]
        basin['basin_def'][node]['parameters'] = conv_fn[node_type](stacked_parameter[offset:offset+num_parameter])
        offset += num_parameter
    

    return basin



def stat_by_stacked_parameter(
        stacked_parameter:list, node_order_type:list, basin:dict,
        rainfall:pd.DataFrame, evapotranspiration:pd.DataFrame, 
        discharge:pd.DataFrame, )->float:
    
    updated_basin = update_basin_with_stacked_parameter(basin, node_order_type, stacked_parameter)
    # updated_basin = basin
    
    result = compute_project(updated_basin,rainfall,evapotranspiration,24.0)

    # merge using index
    merged = pd.merge(
        result,discharge, 
        how='inner', 
        left_index=True, 
        right_index=True, 
        suffixes=('_sim', '_obs')
    )

    return 1-NSE(merged['BAHADURABAD_sim'].to_numpy(),merged['BAHADURABAD_obs'].to_numpy())



def optimize_project(basin:dict, precipitation, evapotranspiration, discharge):


    node_order_type, stacked_parameter = parameter_stack(basin)
    
    upper_bound_stacked = list()
    lower_bound_stacked = list()
    
    for _, node_type in node_order_type:

        if node_type == 'Subbasin':
            
            upper_bound_stacked.extend(tank_ub.tolist())
            lower_bound_stacked.extend(tank_lb.tolist())

        if node_type == 'Reach':
            upper_bound_stacked.extend(muskingum_ub.tolist())
            lower_bound_stacked.extend(muskingum_lb.tolist())
    
    initialGuess = np.array(stacked_parameter)
    

    paramBounds = np.column_stack((lower_bound_stacked,upper_bound_stacked))
    print(initialGuess.shape, paramBounds.shape)
    print('optimizing')
    # optimizer = minimize(stat_by_stacked_parameter, initialGuess,
    #         args=(node_order_type, basin,precipitation,evapotranspiration,discharge),
    #         method='L-BFGS-B',
    #         bounds=paramBounds
    #     )

    # optimizer = minimize(stat_by_stacked_parameter, initialGuess,
    #         args=(node_order_type, basin,precipitation,evapotranspiration,discharge),
    #         method='powell',
    #     )

    optimizer = dual_annealing(stat_by_stacked_parameter, bounds=paramBounds,
            args=(node_order_type, basin,precipitation,evapotranspiration,discharge),
            
        )

    
    return update_basin_with_stacked_parameter(basin, node_order_type, optimizer.x)

    # print(
    #     stat_by_stacked_parameter(
    #         stacked_parameter, node_order_type, basin,
    #         precipitation, evapotranspiration, discharge
    #         )
    # )
