import sys

from tank_core.bias_correction import GQM

import pandas as pd 


data = pd.read_csv('sample-data/biascorr_dat.csv')

gqm = GQM()


print(gqm.obsParam['b'])

gqm.fit(data['obs'].values,data['sim'].values)

print(gqm.obsParam['a'])

corr = gqm.correct(data['sim'])


import pylab as pl 

pl.plot(data['obs'],label='observed')
# pl.plot(data['sim'],label='simulated')
pl.plot(corr,label='corrected')
pl.legend()
pl.plot()
pl.show()