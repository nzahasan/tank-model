# -*- coding: utf-8 -*-
'''
Helper functions for project creation
'''
from . import global_config as gc
from .utils import (
    tank_param_list2dict,
    muskingum_param_list2dict,
)


# converts line to attr,value pairs
def line2list(line:str)->list: 
    _line = line.strip()
    # split by first occurance of ":"
    return [x.strip() for x in _line.split(':',1)]

# converts hec-hms basin to tank basin definition
def hms_basin_to_tank_basin(hms_basin_def:str)->dict:

    parsed_node = dict()
    
    # split txt by "End:"
    all_node_text_splits = hms_basin_def.split('End:')

    # nodes and properties required to create tank basin definition
    required_nodes = ["Subbasin", "Reach", "Junction", "Sink"]
    generic_props  = ["Downstream", "Computation Point"]
    numeric_props  = ["Area"]
    req_props = generic_props + numeric_props

    # default parameters for basin and reach
    basin_default = tank_param_list2dict(gc.tank_lb.tolist())
    channel_default = muskingum_param_list2dict(gc.muskingum_lb.tolist())

    for node_text in all_node_text_splits:
        
        # strip each node text of empty spaces
        # split lines and remove empty lines
        node_lines = [line for line in node_text.strip().splitlines() if line.strip()]
        
        node_type, node_name= line2list(node_lines.pop(0)) 

        # skip if node is not required
        if node_type not in required_nodes : 
            continue
        
        node_dict = dict(type=node_type)
        
        if node_type == 'Reach':
            node_dict['parameters'] = channel_default
        
        if node_type == 'Subbasin':
            node_dict['parameters'] = basin_default

        for line in node_lines:
            
            prop, val= line2list(line)

            # skip if not a required property
            if prop not in req_props: 
                continue

            # if numeric property convert to float
            val = float(val) if prop in numeric_props else val

            # replace keys to lower cases and replace whitespace with _
            prop = prop.lower().replace(' ','_')
            
            # set node property
            node_dict[prop] = val

        if node_name in parsed_node:
            raise ValueError(f'Duplicate node name found in basin file: "{node_name}"')

        parsed_node[node_name] = node_dict

        
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
