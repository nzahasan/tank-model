#!/usr/bin/env python3
'''
Command line utility for model operation :
==========================================
Supports:
    - Generation of new project
    - Compute project
    - Optimize basin parameters
    - Plot project results
'''
import json, os, click
from pathlib import Path
from tank_core import computation_helpers as ch
from tank_core import io_helpers as ioh
from tank_core import project_helpers as ph
from tabulate import tabulate
from matplotlib import pyplot as pl, rcParams
from matplotlib.gridspec import GridSpec
import seaborn
from tank_core import utils 
import pickle

# plot config
rcParams['font.family'] = 'monospace'


@click.group()
def cli(): 
    """### Tank-Model Command Line Utility ###"""
    return
    

# -- Project Generation -- #

@cli.command()
@click.option('-bf', '--hms-basin-file', type=click.File('r'), help="HEC-HMS basin file path", required=True)
@click.option('-of', '--output-file', type=click.File('w'), help="output basin file", required=True)
def hms2tank(hms_basin_file, output_file):
    """converts hec-hms basin file to tank basin file"""
    
    hms_basin_file_content = hms_basin_file.read()

    basin_def = ph.hms_basin_to_tank_basin(hms_basin_file_content)

    output_file.write(json.dumps(basin_def,indent=2))



@cli.command()
@click.argument('project_name', nargs=1)
@click.option('-bf', '--hms-basin-file', type=click.File('r'), help="HEC-HMS basin file path")
def new_project(project_name, hms_basin_file):

    """creates a project directory generates a json formatted project file"""
    # preferred hours [ 0.25, 0.5, 1.0, 2.0, 3.0 . . . . N ]
    project  = dict(
        basin              = f'{project_name}.basin.json', # basin path - json-file
        precipitation      = f'{project_name}.pr.csv',     # precipitation path - csv file
        evapotranspiration = f'{project_name}.et.csv',     # evapotranspiration path - csv file
        discharge          = f'{project_name}.q.csv',      # observed discharge path - csv file
        result             = f'{project_name}.result.csv', # output file for discharge - csv file
        statistics         = f'{project_name}.stats.json'  # statistics calculated form observed discharge - json-file
    )
    
    project_path = Path(project_name)

    if not os.path.exists(project_path):
        os.makedirs(project_path)
    
    # write project def
    project_file_path = project_path / f'{project_name}.project.json'

    with open(project_file_path,'w') as project_file:
        f = project_file.write(json.dumps(project,indent=2))
    
    # write basin def converted form hms basin
    if hms_basin_file is not None:
        hms_basin_file_content = hms_basin_file.read()

        basin_def = ph.hms_basin_to_tank_basin(hms_basin_file_content)

        with open( project_path / project['basin'], 'w') as basin_out_file:
            basin_out_file.write(json.dumps(basin_def,indent=2))

    # check + copy precip and evap files to project location

    print(f'# Project structure for {project_name} has been created')




# -- Computation/Optimization/Execution -- #

@cli.command()
@click.option('-pf', '--project-file', type=click.Path(exists=True), help="project file", required=True)
def compute(project_file):
    '''Computes tank model for given project file'''

    # get project root directory
    project_dir = Path(project_file).resolve().parent

    # read project and build paths for computation
    project = ioh.read_project_file(project_file)
    basin_file = project_dir / project['basin']
    precipitation_file = project_dir / project['precipitation']
    evapotranspiration_file = project_dir / project['evapotranspiration']
    discharge_file = project_dir / project['discharge']
    statistics_file = project_dir / project['statistics']
    result_file =project_dir / project['result']

    # simulation date range, taken from project definition
    # (missing start/end means simulate for the full period)
    start = project.get('start')
    end = project.get('end')

    # read files required for computation
    basin = ioh.read_basin_file(basin_file)
    precipitation, dt_pr = ioh.read_ts_file(precipitation_file, start=start, end=end)
    evapotranspiration, dt_et = ioh.read_ts_file(evapotranspiration_file, start=start, end=end)
    discharge, _ = ioh.read_ts_file(discharge_file, check_missing=False, start=start, end=end)

    # required checking input consistency of precipitation and evapotranspiration
    # - check if time difference of both time-series is same also matches with project def (get_delt does this)
    # - check if both time-series has exactly same index (get_sim_start_end does this)
    # - check for basin nodes names time-series files column matches > not implemented yet!

    # checks and returns delt in hours
    del_t = utils.get_delt(dt_pr, dt_et, project['interval']) 
    sim_start, sim_end = utils.get_sim_start_end(precipitation.index, evapotranspiration.index)

    print(f"INFO: Simulating for the period {sim_start} to {sim_end}")

    computation_result, basin_states = ch.compute_project(basin, precipitation, evapotranspiration, del_t)
    statistics = ch.compute_statistics(basin=basin, result=computation_result, discharge=discharge)

    ioh.write_ts_file(computation_result,result_file)

    # stores tank-basin states in a pickle file for debugging
    with open( project_dir / 'basin_states.pkl', 'wb') as pkl_handler:
        pickle.dump(basin_states, pkl_handler, protocol=pickle.HIGHEST_PROTOCOL)

    heads = ["NSE", "RMSE", "R2", "PBIAS"]
    
    data = {key: [] for key in ('Root Node', *heads)}
    
    for node in basin["root_node"]:
        stat = statistics.get(node)
        if stat is None:
            continue

        data['Root Node'].append(node)
        for key in heads:
            data[key].append(stat.get(key))

    print(tabulate(data, headers='keys', tablefmt='psql'))
    
    with open(statistics_file,'w') as stat_file_write_buffer:
        json.dump(statistics, stat_file_write_buffer, indent=2)
    
    # N.B. always calculate statistics based on the availability of data 
    # in discharge file!!

@cli.command()
@click.option('-pf', '--project-file', help="project file", required=True)
def plot_result(project_file):
    '''Generates plots of model simulation results in project directory'''
    
    project_dir = Path(project_file).resolve().parent
    project = ioh.read_project_file(project_file)

    result_file = project_dir / project['result']
    discharge_file = project_dir / project['discharge']

    # simulation date range, taken from project definition
    # (missing start/end means simulate for the full period)
    start = project.get('start')
    end = project.get('end')

    result,_ = ioh.read_ts_file(result_file, start=start, end=end)

    discharge, _ = ioh.read_ts_file(discharge_file, check_missing=False, start=start, end=end)

    basin_file = project_dir / project['basin']
    basin = ioh.read_basin_file(basin_file)
    
    root_node = basin['root_node'][0]
    sim_key, obs_key = f'{root_node}_sim', f'{root_node}_obs'
    
    merged = ch.merge_obs_sim(observed=discharge,simulated=result)
    
    fig = pl.figure(constrained_layout=True, figsize=(10,10), dpi=600)
    
    gs = GridSpec(2,2, figure=fig)
    ax1 = fig.add_subplot(gs[0,:])
    ax2 = fig.add_subplot(gs[1,0])
    ax3 = fig.add_subplot(gs[1,1])

    
    ax1.plot(result.index,result[root_node],label='Simulated',color='black', linewidth=1.5)
    ax1.plot(discharge.index, discharge[root_node],label='Observed', color='gray', linewidth=1, linestyle='dashdot')
    ax1.title.set_text(f'Observed vs Simulated Discharge at {root_node}')
    ax1.legend()
    
    seaborn.regplot(x=merged[obs_key], y=merged[sim_key], ax=ax2, color='black',scatter_kws={'color':'#e9e9e9'} )
    ax2.title.set_text(f'Correlation R^2 ')

    seaborn.kdeplot(x=discharge[root_node],  color='gray', ax=ax3,label='Obs')
    seaborn.kdeplot(x=result[root_node],  color='black', ax=ax3, label='Sim')
    ax3.legend()
    ax3.title.set_text('KDE Plot')
    
    # pl.show()
    pl.savefig(project_dir / 'model_output.png')

    

@cli.command()
@click.option('-pf', '--project-file', help="project file", required=True)
def optimize(project_file):
    '''Automatically optimizes tank basin parameters for a given projects'''
    project_dir = os.path.dirname(os.path.abspath(project_file))
    
    # project must have discharge as this is mandatory 
    project = ioh.read_project_file(project_file, check_discharge_file=True)
    
    basin_file = os.path.join(project_dir, project['basin'])
    precipitation_file = os.path.join(project_dir, project['precipitation'])
    evapotranspiration_file = os.path.join(project_dir, project['evapotranspiration'])
    discharge_file = os.path.join(project_dir, project['discharge'])
    statistics_file = os.path.join(project_dir, project['statistics'])
    result_file = os.path.join(project_dir, project['result'])
    delt_proj = project['interval']

    # simulation date range, taken from project definition
    # (missing start/end means simulate for the full period)
    start = project.get('start')
    end = project.get('end')

    precipitation, delt_pr = ioh.read_ts_file(precipitation_file, start=start, end=end)
    evapotranspiration, delt_et = ioh.read_ts_file(evapotranspiration_file, start=start, end=end)
    discharge, _ = ioh.read_ts_file(discharge_file, check_missing=False, start=start, end=end)

    del_t = utils.get_delt(delt_pr, delt_et, delt_proj)

    basin = ioh.read_basin_file(basin_file)

    optimized_basin = ch.optimize_project(basin, precipitation, evapotranspiration, discharge, del_t )

    with open(basin_file,'w') as wf:
        json.dump(optimized_basin, wf,indent=2)


if __name__ == '__main__':
    cli()
