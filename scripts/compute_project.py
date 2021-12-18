#!/usr/bin/env python3

'''
	compute tank model form config files
	may be do recursive
'''

import json,pprint
from queue import Queue
import pandas as pd
import click


from tank_core.tank_basin import tank_discharge
from tank_core.channel_routing import muskingum

from tank_core.computation_helpers import (
	build_computation_stack, 
	compute_project
)


@click.command()
@click.option('-pf', '--project_file',  help='Project JSON file path')
def main(project_file):

	_project = json.load(open(project_file,'r'))

	c_stack = build_computation_stack(_project)
	compute_project(c_stack, _project)
	

if __name__ == '__main__':
	main()

