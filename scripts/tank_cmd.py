#!/usr/bin/env python3
'''
Command line utility for model operation
Supports:
    - Generation of new project
    - Compute project
    - Optimize basin paramemeters
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
def new_project(project_name):

    """creates a project directory generates a json formatted project file"""
    # hours [ 0.25, 0.5, 1.0, 2.0, 3.0 . . . . N ]
    project  = {
        "interval"           : 24.0,                         # time interval in hour :float
        "basin"              : f'{project_name}.basin.json', # basin path - json-file
        "precipitation"      : f'{project_name}.pr.csv',     # precipitation path - csv file
        "evapotranspiration" : f'{project_name}.et.csv',     # evapotranspiration path - csv file
        "discharge"          : f'{project_name}.q.csv',      # observered discharge path - csv file
        "result"             : f'{project_name}.result.csv', # output file for discharge - csv file
        "statistics"         : f'{project_name}.stats.json'  # statistics calculated form observed discharge - json-file
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
    '''Computes tank model for given project file'''
    # get project root directory
    project_dir = Path(project_file).resolve().parent
    
    project = ioh.read_project_file(project_file)
    basin_file = project_dir / project['basin']
    precipitation_file = project_dir / project['precipitation']
    evapotranspiration_file = project_dir / project['evapotranspiration']
    discharge_file = project_dir / project['discharge']
    statistics_file = project_dir / project['statistics']
    result_file =project_dir / project['result']

    
    basin = ioh.read_basin_file(basin_file)
    precipitation, dt_pr = ioh.read_ts_file(precipitation_file)
    evapotranspiration, dt_et = ioh.read_ts_file(evapotranspiration_file)
    discharge, _ = ioh.read_ts_file(discharge_file,check_time_diff=False)
    
    del_t_proj = project['interval']

    del_t = utils.check_time_delta(dt_pr, dt_et, del_t_proj)

    computation_result = ch.compute_project(basin, precipitation, evapotranspiration, del_t)
    statistics = ch.compute_statistics(basin=basin, result=computation_result, discharge=discharge)

    ioh.write_ts_file(computation_result,result_file)
     
    print( 
        tabulate(
            [
                ('NSE', statistics['BAHADURABAD']['NSE']),
                ('RMSE', statistics['BAHADURABAD']['RMSE']),
                ('R2', statistics['BAHADURABAD']['R2']),
                ('PBIAS', statistics['BAHADURABAD']['PBIAS']),
            ],
            headers=['Statistics', 'BAHADURABAD'], tablefmt='psql'
        ) 
    )

    with open(statistics_file,'w') as stat_file_write_buffer:
        json.dump(statistics, stat_file_write_buffer, indent=2)
    
    # N.B. always calculate statistics based on the availablity of data 
    # in discharge file!!

@cli.command()
@click.option('-pf', '--project-file', help="project file")
def plot_result(project_file):
    '''Generets plots of model simuation results in project directory'''
    
    project_dir = Path(project_file).resolve().parent
    project = ioh.read_project_file(project_file)
    
    result_file = project_dir / project['result']
    discharge_file = project_dir / project['discharge']
    
    result,_ = ioh.read_ts_file(result_file)

    discharge, _ = ioh.read_ts_file(discharge_file,check_time_diff=False)

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
@click.option('-pf', '--project-file', help="project file")
def optimize(project_file):
    '''Automatically optimizes tank basin parameters for a given projects'''
    project_dir = os.path.dirname(os.path.abspath(project_file))
    
    project = ioh.read_project_file(project_file)
    
    basin_file = os.path.join(project_dir, project['basin'])
    precipitation_file = os.path.join(project_dir, project['precipitation'])
    evapotranspiration_file = os.path.join(project_dir, project['evapotranspiration'])
    discharge_file = os.path.join(project_dir, project['discharge'])
    statistics_file = os.path.join(project_dir, project['statistics'])
    result_file = os.path.join(project_dir, project['result'])
    delt_proj = project['interval']

    precipitation, delt_pr = ioh.read_ts_file(precipitation_file)
    evapotranspiration, delt_et = ioh.read_ts_file(evapotranspiration_file)
    discharge, _ = ioh.read_ts_file(discharge_file,check_time_diff=False)

    del_t = utils.check_time_delta(delt_pr, delt_et, delt_proj)

    basin = ioh.read_basin_file(basin_file)

    optimized_basin = ch.optimize_project(basin, precipitation, evapotranspiration, discharge, del_t )

    with open(basin_file,'w') as wf:
        json.dump(optimized_basin, wf,indent=2)


if __name__ == '__main__':
    cli()