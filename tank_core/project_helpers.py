# -*- coding: utf-8 -*-
'''
Helper functions for project creation
'''
from . import global_config as gc
from .utils import (
    muskingum_param_list2dict,
    tank_param_list2dict,
)


# converts hec-hms basin to tank basin defination
def hms_basin_to_tank_basin(hms_basin_def:str)->dict:

    basin_default = gc.tank_lb
    channel_default = 0.5 * (gc.muskingum_lb + gc.muskingum_ub)
    parsed_node = dict()
    
    nodes = hms_basin_def.split('End:')

    # nodes and properties required to create tank basin defination
    sel_nodes = ["Subbasin","Reach","Junction","Sink"]
    generel_props =["Downstream","Area","Computation Point"]
    numeric_props = ["Area"]

    for node in nodes:

        node = node.strip()
        node_lines = node.split('\n')
        
        node_type, node_name= (node_lines[0].strip()).split(':')
        node_type ,node_name = node_type.strip(),node_name.strip()

        if node_type in sel_nodes : 
            
            node_dict = parsed_node[node_name.strip()] = {}
            node_dict['type'] = node_type.strip()
            
            if node_type=='Reach':
                node_dict['parameters'] = muskingum_param_list2dict(list(channel_default))
            
            if node_type=='Subbasin':
                node_dict['parameters'] = tank_param_list2dict(list(basin_default))

            for line in node_lines[1:]:
                
                line=line.strip()
                
                if len(line) != 0: 

                    l_splits = line.split(':')

                    key=l_splits[0].strip()

                    if key not in generel_props : continue

                    val=(':'.join(l_splits[1:])).strip()

                    if key in numeric_props: val=float(val)
                    node_dict[key.lower().replace(' ','_')]=val

    basin:dict = {"basin_def":parsed_node}

    # add add downsteram/child nodes, root node information
    for node in basin['basin_def']:
        ds = basin['basin_def'][node].get('downstream',None)
        
        if ds is None:
            #  this is root node || needs to be changed
            # no basin will have multiple root node
            if basin.get('root_node',None) is None:
                basin['root_node'] = [node]
            else:
                basin['root_node'].append(node)
        
        else:
            if basin['basin_def'][ds].get('upstream',None) == None:

                basin['basin_def'][ds]['upstream'] = [node]
            else:
                basin['basin_def'][ds]['upstream'].append(node)
    
    return basin

    