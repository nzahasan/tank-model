from . import global_config as gc

def tank_param_list2dict(parameters:list)->dict:


    return {
        # [Tank-0]
        "t0_is"     : parameters[0],
        "t0_boc"    : parameters[1],
        "t0_soc_uo" : parameters[2],
        "t0_soc_lo" : parameters[3], 
        "t0_soh_uo" : parameters[4],
        "t0_soh_lo" : parameters[5],
            
        # [Tank-1]
        "t1_is"     : parameters[6],
        "t1_boc"    : parameters[7],
        "t1_soc"    : parameters[8],
        "t1_soh"    : parameters[9],
                
        # [Tank-2]
        "t2_is"     : parameters[10],
        "t2_boc"    : parameters[11],
        "t2_soc"    : parameters[12],
        "t2_soh"    : parameters[13],
                
        # [Tank-3]
        "t3_is"     : parameters[14],
        "t3_soc"    : parameters[15],
    }

def tank_param_dict2list(parameters:dict)->list:

    return [
        # [Tank-0]
        parameters["t0_is"],    
        parameters["t0_boc"],   
        parameters["t0_soc_uo"],
        parameters["t0_soc_lo"],
        parameters["t0_soh_uo"],
        parameters["t0_soh_lo"],
            
        # [Tank-1]
        parameters["t1_is"],    
        parameters["t1_boc"],   
        parameters["t1_soc"],   
        parameters["t1_soh"],   
                
        # [Tank-2]
        parameters["t2_is"],    
        parameters["t2_boc"],   
        parameters["t2_soc"],   
        parameters["t2_soh"],   
                
        # [Tank-3]
        parameters["t3_is"],    
        parameters["t3_soc"],   
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


# converts hec-hms basin to tank basin defination
def hms_basin_to_tank_basin(hms_basin_def:str):

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

    basin = {"basin_def":parsed_node}

    # add add downsteram/child nodes, root node information
    for node in basin['basin_def']:
        ds = basin['basin_def'][node].get('downstream',None)
        
        if ds is None:
            #  this is root node
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

    