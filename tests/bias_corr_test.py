import sys
sys.path.append('../')
from BiasCorrection import GQM

import pandas as pd 


data = pd.read_csv('sample-data/biascorr_dat.csv')

gqm = GQM()


print(gqm.obsParam['b'])

gqm.fit(data['obs'].values,data['sim'].values)

print(gqm.obsParam['a'])