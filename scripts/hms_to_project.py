'''
	parse hec-hms basin config file
	
	note: need to fix this

'''
import json,yaml
import click

def add_childs(project):

	for node in project['basin_def']:
	
		# identify root

		# add child notation

		ds = project['basin_def'][node].get('downstream',None)
		
		if ds==None:
			
			if project.get('root_node',None) is None:
				project['root_node'] = [node]

			else:
				project['root_node'].append(node)
		
		if ds!=None:
			if project['basin_def'][ds].get('childs',None) == None:

				project['basin_def'][ds]['childs'] = [node]
			else:
				project['basin_def'][ds]['childs'].append(node)

	return project


@click.command()
@click.option('--hms_basin', '-hb', 'HEC HMS Basin file location')
@click.option('--output_file', '-of', 'output json file location')
def main(hms_basin:str, output_file:str)->None:

	nodes = open(hms_basin,'r').read().split('End:')

	parsed_node = {}  #[]


	sel_node_list=["Subbasin","Reach","Junction","Sink"]
	sel_prop_list=["Downstream","Area","Computation Point"]
	numeric_props = ["Area"]

	for node in nodes:

		node = node.strip()
		node_lines = node.split('\n')
		# print(node_lines[0])
		node_type,node_name= (node_lines[0].strip()).split(':')
		node_type ,node_name = node_type.strip(),node_name.strip()

		if node_type not in sel_node_list: continue
		# if node
		node_dict = parsed_node[node_name.strip()] = {}
		node_dict['type'] = node_type.strip()
		# node_dict['name']= node_name.strip()


		for line in node_lines[1:]:
			line=line.strip()
			if len(line)==0: continue
			l_splits = line.split(':')

			key=l_splits[0].strip()

			if key not in sel_prop_list: continue

			val=(':'.join(l_splits[1:])).strip()

			if key in numeric_props: val=float(val)
			node_dict[key.lower().replace(' ','_')]=val

		# parsed_node.append(node_dict)


	project = {"basin_def":parsed_node,"config":{"pr_file":"/pr.csv","et_file":"/et.csv","output":"/output.csv"}}

	project = add_childs(project)

	print(project)

	with open(output_file,'w') as jwf:
		json.dump(project,jwf,indent=4)


if __name__ == "__main__":
	main()

	