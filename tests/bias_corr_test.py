

from tank_core.bias_correction import gqm
from pathlib import Path
import pandas as pd 


# def test_gqm():
#     sample_data_path = Path(__file__).absolute().parent

#     data = pd.read_csv(sample_data_path / 'sample-data' / 'biascorr_dat.csv')

#     _gqm = gqm()

#     _gqm.fit(data['obs'].values,data['sim'].values)

#     corr = _gqm.correct(data['sim'])

