


# build computation graph [incomplete]


class node(object):
	def __init__(self, arg):
		self.name = None
		self.childs = []
		


class basin_tree(object):
	
	def __init__(self, arg):
		self.root  = None
		self.nodes = {}


	def add_node(self,node_name):

		self.nodes[node_name] = {'childs': [] }

	def add_child(self,parent_node_name,child_node_name):

		

		self.nodes[parent_node_name]['childs'].append(child_node_name)


	# basin_tree['node']['childs'] = ['B1','B2' ...]



# insert nodes into list


# build tree by index

t = node('W120','basin',0,None)


print(t.up)



