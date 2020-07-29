#!/usr/bin/env python3


'''
	compute tank model form config files
	may be do recursive
'''

# build computation graph [incomplete]

import yaml,pprint

pp = pprint.PrettyPrinter(width=41, compact=True)

project = yaml.load(open('basin.yaml','r'),Loader=yaml.FullLoader)

for node in project['BASIN_DEF']:
	
	# identify root

	# add child notation

	ds = project['BASIN_DEF'][node].get('Downstream',None)
	
	if ds==None:
		project['basin_root_node'] = node
	
	if ds!=None:
		if project['BASIN_DEF'][ds].get('childs',None) == None:

			project['BASIN_DEF'][ds]['childs'] = [node]
		else:
			project['BASIN_DEF'][ds]['childs'].append(node)


pp.pprint(project)	


# build computation stack while traversing


# c_stack = []

# jump_stack = []

# for 



# check time series for missing values


# compute tank