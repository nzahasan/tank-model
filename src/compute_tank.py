#!/usr/bin/env python3

'''
	compute tank model form config files
	may be do recursive
'''

# build computation graph [incomplete]

import json,pprint
from queue import Queue

pp = pprint.PrettyPrinter(width=41, compact=True)

project = json.load(open('basin.json','r'))





# build node tree
for node in project['basin_def']:
	
	# identify root

	# add child notation

	ds = project['basin_def'][node].get('Downstream',None)
	
	if ds==None:
		project['basin_root_node'] = node
	
	if ds!=None:
		if project['basin_def'][ds].get('childs',None) == None:

			project['basin_def'][ds]['childs'] = [node]
		else:
			project['basin_def'][ds]['childs'].append(node)


# pp.pprint(project)	


# traverse tree and build computation stack
compute_stack = []

node_qeue = Queue()


# enque root note
for root_node in project['root_node']:
	node_qeue.put(root_node)

while not node_qeue.empty():

	node = node_qeue.get()

	# compute_stack.append( project['basin_def'][node] )
	compute_stack.append(node)
	print(node)
	# print(project['basin_def'])
	if project['basin_def'][node].get('childs',False):
		childs = project['basin_def'][node]['childs']

		for child in childs:
			node_qeue.put(child)

print(compute_stack)


# compute tank
while len(compute_stack)>0:

	node_name = compute_stack.pop()
	node_compute = project['basin_def'][node_name]

	print(node_name)

	if node_compute['type'] == 'Subbasin':
		print("compute tank for basin", node_name)

	if node_compute['type'] == 'Reach':
		print('route flow', node_compute['childs'])

	if node_compute['type'] in ['Sink','Junction']:

		print('>> sum flow', node_compute['childs'])

