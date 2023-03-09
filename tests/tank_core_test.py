from tank_core import tank_basin 
import tank_core.global_config as gp
import pandas as pd
from pathlib import Path


def test_tank_core():

    sample_data = Path(__file__).absolute().parent / 'sample-data' / 'tank_sample_data.csv'

    data= pd.read_csv(sample_data)

    params = 0.5*(gp.tank_ub+gp.tank_lb)

    q = tank_basin.tank_discharge(data['Pr'].values,data['ET'].values,24,3000,*params)

    

