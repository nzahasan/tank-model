
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

def compute_project(
		basin:dict, 
		precipitation:pd.DataFrame, 
		evapotranspiration:pd.DataFrame
	)->pd.DataFrame:
	
	computation_stack = build_computation_stack(basin)
	sum_basin = np.zeros(precipitation.values.shape[0])
	while len(computation_stack) > 0:

		# pop node from top of the node
		node_name = computation_stack.pop()


		node_compute = basin['basin_def'][node_name]

		if node_compute['type'] == 'Subbasin':
			
			print("compute tank for basin", node_name)
			 
			dis = tank_discharge(
				precipitation[node_name].values,
				evapotranspiration[node_name].values, 
				24,
				node_compute['area'],
				* node_compute['parameters']
			)
			sum_basin += dis

			# print(dis)

		if node_compute['type'] == 'Reach':
			print('route flow then sum', node_compute['upstream'])

		if node_compute['type'] in ['Sink','Junction']:

			print('>> sum flow', node_compute['upstream'])


	import pylab as pl
	pl.plot(sum_basin)
	pl.show()
	return pd.DataFrame()


def compute_statistics():

	return pd.DataFrame()


# optimization

def stack_parameter(basin:dict):

	pass 

def update_basin_parameter(basin:dict):
	pass

def optimize_project(basin:dict):

	# stacked_parameters = 
	pass
