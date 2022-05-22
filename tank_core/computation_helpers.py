from queue import Queue
import pandas as pd
from tank_core.tank_basin import tank_discharge
from tank_core.channel_routing import muskingum

from tank_core.cost_functions import R2, RMSE, NSE
import numpy as np

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
                precipitation = precipitation[curr_node_name].values,
                evapotranspiration = evapotranspiration[curr_node_name].values, 
                del_t = del_t,
                area = curr_node_def['area'],
                ** curr_node_def['parameters']
            )
            

        elif curr_node_def['type'] == 'Reach':
            print('RC','route upstream flow then sum', curr_node_def['upstream'])

            sum_node = np.zeros(n_step, dtype=np.float64)
            
            for us_node_name in curr_node_def['upstream']:
                sum_node += muskingum( 
                    in_flow= computation_result[us_node_name].values,
                    del_t=del_t,
                    ** curr_node_def['parameters']
                )

            
            computation_result[curr_node_name] = sum_node
            

        elif curr_node_def['type'] in ['Sink','Junction']:

            print(curr_node_def['type'],'>> sum flow', curr_node_def['upstream'])

            sum_node = np.zeros(n_step, dtype=np.float64)
            
            for us_node_name in curr_node_def['upstream']:
                sum_node += computation_result[us_node_name].values
            
            computation_result[curr_node_name] = sum_node


    

    return computation_result
    
    


def compute_statistics(basin:dict,result:pd.DataFrame, discharge:pd.DataFrame)->dict:

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
                "RMSE": RMSE(merged[obs_key].values,merged[sim_key].values),
                "NSE": NSE(merged[sim_key].values,merged[obs_key].values ),
                "R2": R2(merged[sim_key].values,merged[obs_key].values )
            }

    return statistics


# optimization

def stack_parameter(basin:dict):

    pass 

def update_basin_parameter(basin:dict):
    pass

def optimize_project(basin:dict):

    # stacked_parameters = 
    pass

