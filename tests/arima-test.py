import sys
sys.path.append('../')
import pandas as pd 
import numpy as np 
from ARIMA import autoARIMA 
import pylab as pl

def main():

    data = pd.read_csv('../sample-data/arima_data.csv')

    vals = data['Sales']

    model = autoARIMA(vals).fit()
    # pre,con = model.forecast(5)
    # model.inSamplePlot()

    
    # pl.show()
    data = model.fitted_model.predict(typ='levels')
    print('yodata',data)

    pl.plot(data,label='forecast')
    # pl.plot(vals,label='feed')
    # pl.legend()
    pl.show()
    # print(model.bestOrder)
    
if __name__ == '__main__':
    main()
