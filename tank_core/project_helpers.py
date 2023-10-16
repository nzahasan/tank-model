# -*- coding: utf-8 -*-
'''
Helper functions for project creation
'''
from . import global_config as gc
from .utils import (
    tank_param_list2dict,
    muskingum_param_list2dict,
)


# converts hec-hms basin to tank basin definition
def hms_basin_to_tank_basin(hms_basin_def:str)->dict:

    basin_default = tank_param_list2dict(gc.tank_lb)
    channel_default = muskingum_param_list2dict(gc.muskingum_lb)
    
    parsed_node = dict()
    
    nodes = hms_basin_def.split('End:')

    # nodes and properties required to create tank basin definition
    required_nodes = ["Subbasin", "Reach", "Junction", "Sink"]
    generic_props = ["Downstream", "Computation Point"]
    numeric_props = ["Area"]
    req_props = generic_props + numeric_props

    # converts line to attr,value pairs
    line_to_kv = lambda line : [x.strip() for x in line.strip().split(':')]

    for node in nodes:

        node = node.strip()
        node_lines = node.split('\n')
        
        node_type, node_name= line_to_kv(node_lines.pop(0)) 

        # skip if node is not required
        if node_type not in required_nodes : 
            continue
        
        # this is confusing! why did I do this?
        node_dict = parsed_node[node_name] = dict()
        
        node_dict['type'] = node_type
        
        if node_type=='Reach':
            node_dict['parameters'] = channel_default
        
        if node_type=='Subbasin':
            node_dict['parameters'] = basin_default

        for line in node_lines:
            
            # remove starting and ending whitespaces
            line=line.strip()
            
            # check for empty lines
            if len(line) == 0:
                continue 

            prop, val= line_to_kv(line)

            # skip if not a required property
            if prop not in req_props: 
                continue

            # if numeric property convert to float
            val = float(val) if prop in numeric_props else val

            # replace keys to lower cases and replace whitespace with _
            prop = prop.lower().replace(' ','_')
            
            # set node property
            node_dict[prop] = val

    basin = dict(
        basin_def= parsed_node
    )

    # add add downstream/parent nodes, root node information
    for node in basin['basin_def']:
        ds = basin['basin_def'][node].get('downstream',None)
        
        if ds is None:
            # this is root node || needs to be changed
            # can basins have multiple root node? 
            # > by definition everything should drain through a point
            # but a project can contain 2 basin with 2 root node
            # need to find a good way to handle this
            if basin.get('root_node', None) is None:
                basin['root_node'] = [node]
            else:
                basin['root_node'].append(node)
        
        else:
            if basin['basin_def'][ds].get('upstream',None) == None:

                basin['basin_def'][ds]['upstream'] = [node]
            else:
                basin['basin_def'][ds]['upstream'].append(node)
    
    return basin
