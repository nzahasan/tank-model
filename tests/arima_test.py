import pandas as pd 
import numpy as np 
from tank_core.arima import autoARIMA 
import pylab as pl

from pathlib import Path



# def test_arima():
#     sample_data = Path(__file__).absolute().parent / 'sample-data' / 'arima_data.csv'
    
#     data = pd.read_csv(sample_data)

#     vals = data['Sales']

#     # model = autoARIMA(vals).fit()
    
#     # data = model.fitted_model.predict(typ='levels')
    