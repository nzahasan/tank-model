#!/usr/bin/env python3

'''
Model operations command line tool

guide: https://click.palletsprojects.com/en/8.0.x/commands/
'''

from typing_extensions import Required
import click
import json
from click.decorators import option


import sys;
sys.path.append('.')

from tank_core.computation_helpers import (
    compute_project
)

from tank_core.io_helpers import (
    read_project_file
)

@click.group()
def cli(): pass


@click.command()
@click.option('-pf', '--project-file', help="project file")
def compute(project_file:str):
    
    project = read_project_file(project_file)
    compute_project(project)
    
    


@click.command()
@click.option('-bf', '--basin-file', type=click.File('r'), help="HEC-HMS basin file", required=True)
@click.option('-of', '--output-file', type=click.File('w'), help="output basin file", required=True)
def hms2tank( basin_file, output_file):
    
    pass

@click.command()
@click.option('-of', '--output-file', type=click.File('w'), help="output basin file", required=True)
def gen_tank_project( basin_file, output_file):
    
    pass



cli.add_command(compute)
cli.add_command(hms2tank)
cli.add_command(gen_tank_project)

if __name__ == '__main__':
    cli()