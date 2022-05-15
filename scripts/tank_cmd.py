#!/usr/bin/env python3
'''
Command line utility for model operation
'''

import json, os, click
from click.decorators import option
from tank_core.computation_helpers import compute_project, compute_statistics
from tank_core.io_helpers import (read_project_file, 
                                read_basin_file, 
                                read_ts_file, 
                                write_ts_file
                            )
from tank_core.project_helpers import hms_basin_to_tank_basin
import tank_core.global_config as gc


@click.group()
def cli(): 
    """Utility tool for tank-model"""
    pass
    

# -- Project Generation -- #

@cli.command()
@click.option('-bf', '--hms-basin-file', type=click.File('r'), help="HEC-HMS basin file path", required=True)
@click.option('-of', '--output-file', type=click.File('w'), help="output basin file", required=True)
def hms2tank(hms_basin_file, output_file):
    """converts hec-hms basin file to tank basin file"""
    
    hms_basin_file_content = hms_basin_file.read()

    basin_def = hms_basin_to_tank_basin(hms_basin_file_content)

    output_file.write(json.dumps(basin_def,indent=2))



@cli.command()
@click.argument('project_name', nargs=1)
def new_project(project_name):

    """creates a project directory generates a json formatted project file"""

    project  = {
        "interval": 24.0, # time interval in hour :float
        "basin": f'{project_name}.basin.json', #basin path :JSON
        "precipitation": f'{project_name}.pr.csv', #precipitation path :CSV
        "evapotranspiration": f'{project_name}.et.csv', #evapotranspiration path :CSV
        "discharge": f'{project_name}.q.csv', # observered discharge path :CSV
        "result": f'{project_name}.result.csv', # output file for discharge :CSV
        "statistics": f'{project_name}.stats.json' # statistics calculated form observed discharge :JSON
    }
    
    if not os.path.exists(project_name):
        os.makedirs(project_name)
    
    project_file_path = os.path.join(project_name,f'{project_name}.project.json')

    with open(project_file_path,'w') as project_file:
        f = project_file.write(json.dumps(project,indent=2))

    print(f'# An empty project structure for {project_name} has been created')
    return f



# -- Computation/Optimization/Execution -- #

@cli.command()
@click.option('-pf', '--project-file', type=click.Path(exists=True), help="project file", required=True)
def compute(project_file):
    
    # get project root directory
    project_dir = os.path.dirname(os.path.abspath(project_file))
    

    project = read_project_file(project_file)
    
    basin_file = os.path.join(project_dir, project['basin'])
    precipitation_file = os.path.join(project_dir, project['precipitation'])
    evapotranspiration_file = os.path.join(project_dir, project['evapotranspiration'])
    discharge_file = os.path.join(project_dir, project['discharge'])
    statistics_file = os.path.join(project_dir, project['statistics'])
    result = os.path.join(project_dir, project['result'])

    print(basin_file,precipitation_file,evapotranspiration_file,
        discharge_file, statistics_file, result
    )

    basin = read_basin_file(basin_file)
    precipitation, dt_pr = read_ts_file(precipitation_file)
    evapotranspiration, dt_et = read_ts_file(evapotranspiration_file)



    compute_project(basin, precipitation, evapotranspiration)

    
    # always calculate statistics based on the availablity of data in discharge file!!

@cli.command()
@click.option('-pf', '--project-file', help="project file")
def optimize_project(project_file):
    
    project = read_project_file(project_file)
    compute_project(project)


if __name__ == '__main__':
    cli()