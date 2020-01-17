#! /usr/bin/env python3

import pickle
import warnings
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller
warnings.filterwarnings("ignore") 


'''
Time series error Correction Module for model
---------------------------------------------
ARIMA(p,d,q)
    p - autoregressive part
    d - integrated part / differentiation part
    q - moving average part

'''

class autoARIMA(object):

    '''
    A wrapper of statsmodels, ARIMA for easier model fitting and generating forecast
    this fits ARIMA model using brute force with lowest BIC(Bayesian Information Criteria) value.
      - Not the best way but its the easiest
    
    Possible alternative to look at - pyramid-arima
    '''

    def __init__(self,endog,max_p=5,max_d=5,max_q=5,helpText=True):
        
        self.endog        = endog
        self.max_p        = max_p
        self.max_d        = max_d
        self.max_q        = max_q
        self.helpText     = helpText
        self.fitted_model = None


    def getOrder(self):
        
        fittedOrder = {'order':[],'bic':[]}

        # iterate through (p,d,q) values
        for p in range(self.max_p):
            for d in range(self.max_d):
                for q in range(self.max_q):
                    try:
                        model = ARIMA(self.endog, order=(p,d,q)).fit(disp=0)
                        fittedOrder['bic'].append( model.bic )
                        fittedOrder['order'].append( (p,d,q) )
                    except: 
                        continue
        
        # find order with lowest bic value 
        bestOrder = fittedOrder['order'][ fittedOrder['bic'].index( min(fittedOrder['bic']) ) ]
        
        if self.helpText == True:
            print('Lowest BIC value with order ',bestOrder)
        
        return bestOrder

    def fit(self):
        
        # return a fitted ARIMA model with lowest bic value
        
        self.fitted_model = ARIMA(self.endog,order=self.getOrder()).fit(disp=0)
        
        return self

    
    def forecast(self,num_step):
        
        # returns forecasted values and confidence limit of the forecast

        if self.fitted_model == None:
            print('ERROR: Fit the model first')
            return None

        forecast,_,confLimit = self.fitted_model.forecast(steps=num_step)
        return (forecast,confLimit)

    def inSamplePlot(self):
        
        self.fitted_model.plot_predict()
        return self

    def saveModel(self,fileName):
    	with open(fileName,'wb') as outModelFile:
    		pickle.dump(self,outModelFile,pickle.HIGHEST_PROTOCOL)


    def loadModel(self,fileName):
    	with open(fileName,'rb') as inModelFile:
    		self = pickle.load(inModelFile)


    

    # N.B. predict() returns differentiated value by default
    # use typ='levels' for prediction in endog level/scale 