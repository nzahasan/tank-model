'''
	parse hec-hms basin config file
	 

'''
import json,yaml
nodes = open('Brahmaputra.basin','r').read().split('End:')

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
		node_dict[key]=val

	# parsed_node.append(node_dict)



with open('basin.json','w') as jwf:
	d = {"BASIN_DEF":parsed_node,"CONFIG":{"subbasin_shapefile":"/sb.shp","pr_file":"/pr.csv","et_file":"/et.csv","output_file":"/output.csv"}}
	t = json.dumps(d,allow_nan=True,indent=4)
	# t = yaml.dump(d)

	jwf.write(t)


with open('basin.yaml','w') as ywf:
	d = {"BASIN_DEF":parsed_node,"CONFIG":{"subbasin_shapefile":"/sb.shp","pr_file":"/pr.csv","et_file":"/et.csv","output_file":"/output.csv"}}
	# t = json.dumps(d,allow_nan=True,indent=4)
	t = yaml.dump(d)

	ywf.write(t)



def main():

	pass


if if __name__ == "__main__":
	main()