#!/usr/bin/env python3

# parse hec-hms basin configuration file
# and generates a basin file compatible for 
# tank model

import sys
import json
from typing_extensions import Required
import click

sys.path.append('.')

from tank_core import global_parameters as gp

basin_default = 0.5 * (gp.tank_lb + gp.tank_ub)
channel_default = 0.5 * (gp.muskingum_lb + gp.muskingum_ub)

def defines_downstream_nodes(project):

	for node in project['basin_def']:
	
		ds = project['basin_def'][node].get('downstream',None)
		
		if ds==None:
			
			if project.get('root_node',None) is None:
				project['root_node'] = [node]

			else:
				project['root_node'].append(node)
		
		if ds!=None:
			if project['basin_def'][ds].get('upstream',None) == None:

				project['basin_def'][ds]['upstream'] = [node]
			else:
				project['basin_def'][ds]['upstream'].append(node)

	return project


@click.command()
@click.option('-hb','--hms_basin', help='HEC HMS Basin file location', required=True)
@click.option('-of','--output_file', help='output json file location', required=True)
def main(hms_basin, output_file)->None:

	print(hms_basin, output_file)
	nodes = open(hms_basin,'r').read().split('End:')

	parsed_node = {}  #[]


	sel_nodes =["Subbasin","Reach","Junction","Sink"]
	generel_props =["Downstream","Area","Computation Point"]
	numeric_props = ["Area"]

	for node in nodes:

		node = node.strip()
		node_lines = node.split('\n')
		# print(node_lines[0])
		node_type,node_name= (node_lines[0].strip()).split(':')
		node_type ,node_name = node_type.strip(),node_name.strip()

		if node_type not in sel_nodes : continue
		# if node
		node_dict = parsed_node[node_name.strip()] = {}
		node_dict['type'] = node_type.strip()
		
		if node_type=='Reach':
			node_dict['parameters'] = list(channel_default)
		
		if node_type=='Subbasin':
			node_dict['parameters'] = list(basin_default)
		# node_dict['name']= node_name.strip()


		for line in node_lines[1:]:
			line=line.strip()
			if len(line)==0: continue
			l_splits = line.split(':')

			key=l_splits[0].strip()

			if key not in generel_props : continue

			val=(':'.join(l_splits[1:])).strip()

			if key in numeric_props: val=float(val)
			node_dict[key.lower().replace(' ','_')]=val

		# parsed_node.append(node_dict)


	project = {"basin_def":parsed_node}

	project = defines_downstream_nodes(project)

	with open(output_file,'w') as jwf:
		json.dump(project,jwf,indent=4)


if __name__ == "__main__":
	main()

	