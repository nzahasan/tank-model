#!/usr/bin/env python3

'''
	compute tank model form config files
	may be do recursive
'''

# build computation graph [incomplete]

import json,pprint
from queue import Queue
import pandas as pd
import click
from tank_core import tank_discharge
from channel_routing import muskingum


def build_computation_stack(project:dict) -> list:

	# traverse project tree and build computation stack
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
		if project['basin_def'][node].get('childs',False):
			childs = project['basin_def'][node]['childs']

			for child in childs:
				node_qeue.put(child)

	return computation_stack




def compute_project(computation_stack:list, project:dict)->int:
	
	while len(computation_stack)>0:

		node_name = computation_stack.pop()
		node_compute = project['basin_def'][node_name]

		print(node_name)

		if node_compute['type'] == 'Subbasin':
			print("compute tank for basin", node_name)

		if node_compute['type'] == 'Reach':
			print('route flow', node_compute['childs'])

		if node_compute['type'] in ['Sink','Junction']:

			print('>> sum flow', node_compute['childs'])

	return 0

def check_input_consistancey():

	pass

@click.command()
@click.option('--project_file', '-pf',  help='Project JSON file path')
def main(project_file):

	_project = json.load(open(project_file,'r'))

	c_stack = build_computation_stack(_project)
	compute_project(c_stack, _project)
	

if __name__ == '__main__':
	main()

