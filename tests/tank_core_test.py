

import tank_core as tc

import tank_core.global_config as gp


import pandas as pd



data= pd.read_csv('sample-data/tank_sample_data.csv')


# print(data.head(10))



params = 0.5*(gp.tankUpperBounds+gp.tankLowerBounds)

q = tc.tank_discharge(data['Pr'].values,data['ET'].values,24,3000,*params)


import pylab as pl
pl.style.use('ggplot')
pl.plot(q,label='sim')
pl.plot(data['Q'].values,label='obs')
pl.legend()
pl.show()
