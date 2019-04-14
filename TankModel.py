#! /usr/bin/env python3

'''
    Tank Hydrologic model

'''


import numpy as np
from scipy.optimize import minimize
import GlobalParameters as GP


def formatParameters(paramArr):

    # parameter structure is in GlobalParameters.py

    if (isinstance(paramArr,np.ndarray)!=True) or (paramArr.shape[0]!=16):
        print('ERROR: Passed data is not a numpy array or not of size 16')


    return {
        't0':{
            'is'  : paramArr[0],
            'boc' : paramArr[1],
            'soc' : { 
                    'uo': paramArr[2],
                    'lo': paramArr[3] 
                    },
            'soh' : { 
                    'uo': paramArr[4],
                    'lo': paramArr[5] 
                    }
        },

        't1':{
            'is'  : paramArr[6],
            'boc' : paramArr[7],
            'soc' : paramArr[8],
            'soh' : paramArr[9]
        },

        't2':{
            'is'  : paramArr[10],
            'boc' : paramArr[11],
            'soc' : paramArr[12],
            'soh' : paramArr[13]
        },
        't3':{
            'is'  : paramArr[14],
            'soc' : paramArr[15]
        }
    }


def shapeAlike(x,y):
    if x.shape==y.shape:
        return True
    else:
        return False


def tankDischarge(rainfall,evapotranspiration,parameterArr,area,delT):
    '''
    UNITS:
    ------
    area               - km^2
    delT               - hr
    discharge          - m^3/s
    rainfall           - mm
    evapotranspiration - mm


    returns a time-series of simulated discharge
    '''


    # calculate timestep length
    
    if shapeAlike(rainfall, evapotranspiration):
        timeSetp = rainfall.shape[0]
    else:
        print('ERROR: length mismatch between rainfall and evapotranspiration data')
        return -1

    # convert parameters to a more meaningful formats
    parameters = formatParameters(parameterArr)

    # check for parameter: for Tank-0
    if parameters['t0']['soh']['uo'] < parameters['t0']['soh']['lo']:
        print('WARNING: Parameter error upper outlet height is less than lower outlet height (Tank 0)')

    tankStorage      = np.zeros((timeSetp,4),dtype=np.float64)
    sideOutletFlow   = np.zeros((timeSetp,4),dtype=np.float64) 
    bottomOutletFlow = np.zeros((timeSetp,3),dtype=np.float64)   
    
    # Difference of rainfall & evapotranspiration [only inflow to Tank 0]
    
    delRf_Et = rainfall - evapotranspiration
    
    # Loop through the timeseries 
    
    for t in range(timeSetp):
    
       

        if t == 0:
            # set initial storage of the tank's
            tankStorage[t,0] = parameters['t0']['is']
            tankStorage[t,1] = parameters['t1']['is']
            tankStorage[t,2] = parameters['t2']['is']
            tankStorage[t,3] = parameters['t3']['is']
        
        else:
            
            '''
                Tank Storage Calculation
            ----------------------------
            storage  =  inflow - outflow
            
            '''
            
            tankStorage[t,0] = ( tankStorage[t-1,0] + delRf_Et[t] ) - ( sideOutletFlow[t-1,0] + bottomOutletFlow[t-1,0] )
        
            tankStorage[t,1] = ( tankStorage[t-1,1] + bottomOutletFlow[t-1,0] ) - ( sideOutletFlow[t-1,1] + bottomOutletFlow[t-1,1] ) 
            
            tankStorage[t,2] = ( tankStorage[t-1,2] + bottomOutletFlow[t-1,1] ) - ( sideOutletFlow[t-1,2] + bottomOutletFlow[t-1,2] ) 

            tankStorage[t,3] = ( tankStorage[t-1,3] + bottomOutletFlow[t-1,2] ) - ( sideOutletFlow[t-1,3]  ) 
                
        '''
        Handling negetive tank storage:
        -------------------------------
        Set tank storage = 0 if tank storage is negetive
        
        N.B. evapotranspiration rate can be more than precipitation rate
        in that case tank storage can be negetive value
        '''
        
        for i in range(4): tankStorage[t,i]= max(tankStorage[t,i],0)

        '''
        If tank outflow becmes greater than  current storage(previous storage + inflow) the storage will be negetive
        which is incorrect. Side outlet flow + bottom outlet flow must not be greater than current storage.
        
        As example if the bottom outlet storage coefficient is 1 and side outlet height 0 and coefficient is 1
        the output flow will be greater than what in storage which is impossible. 
        '''
        

        '''
        Side Outlet Flow :
        ------------------
        side outlet flow = f(tankStorage,outletHeight)
        
        There will be zero flow if tank storage less than outlet height
        '''

        # --- TANK 0 / surface runoff ---
        
        '''
        Note: If Tank-0's storage is not greater than lower outlet then
        there is no way there will be flow from upper outlet
        '''
        
        # Check if storage height > Lower Outlet
        if tankStorage[t,0] >  parameters['t0']['soh']['lo']:
            sideOutletFlow[t,0] = parameters['t0']['soc']['lo'] * ( tankStorage[t,0] - parameters['t0']['soh']['lo'] )
            
            # Lower outlet is filled check for upper outlet
            if tankStorage[t,0] >  parameters['t0']['soh']['uo']:
                sideOutletFlow[t,0] += parameters['t0']['soc']['uo'] * ( tankStorage[t,0] - parameters['t0']['soh']['uo'] )
        
        else:
            sideOutletFlow[t,0] = 0


        # --- TANK 1 / intermediate runoff ---
        
        if tankStorage[t,1] > parameters['t1']['soh']:
            sideOutletFlow[t,1]  = parameters['t1']['soc'] * ( tankStorage[t,1] - parameters['t1']['soh'] )
        
        else:
            sideOutletFlow[t,1] = 0

        # --- TANK 2 / sub-base runoff---
        
        if tankStorage[t,2] > parameters['t2']['soh']:
            sideOutletFlow[t,2]  = parameters['t2']['soc'] * ( tankStorage[t,2] - parameters['t2']['soh'] )
    
        else:
            sideOutletFlow[t,2] = 0
            
        
        # --- TANK 3 / baseflow ---
        '''
        Side outlet height = 0
        '''
        if tankStorage[t,3] >=0:
            sideOutletFlow[t,3]  = parameters['t3']['soc'] * ( tankStorage[t,3] )

        else:
            sideOutletFlow[t,3]
        
        
        '''
        Bottom outlet flow :
        --------------------
        bottom outlet flow = f(tankStorage)
        
        No need apply condition here, 
        because theoritacilly tankStorage will never be negetive
        '''

        bottomOutletFlow[t,0] = parameters['t0']['boc'] * tankStorage[t,0]

        bottomOutletFlow[t,1] = parameters['t1']['boc'] * tankStorage[t,1]
        
        bottomOutletFlow[t,2] = parameters['t2']['boc'] * tankStorage[t,2]

        # N.B. tank 3 has no bottom outlet

        '''
        Check for parameter error (parameter debugging)
        -----------------------------------------------
        Check that enough water was availble in the tank 
        to satisfy side and bottom outlet flow.
        '''

        for i in range(4):
            if i <=2:
                if tankStorage[t,i] < bottomOutletFlow[t,i] + sideOutletFlow[t,i]:
                    print('WARNING: Total outlet flow exceeded tank storage for tank '+str(i))
            if i==3:
                # again no bottom outlet in Tank-3
                if tankStorage[t,i] < sideOutletFlow[t,i]:
                    print('WARNING: Side outlet flow exceeded tank storage for tank '+str(i))
    
    discharge = sideOutletFlow.sum(axis=1) * ( (area * 1e3) / (delT*60*60)  ) 


    return discharge


'''
Necessary cost function for model calibration and validation

    R2:

        Pearson’s correlation coefficient(R) squared
        Range [0 to 1]
        higher is better maximum possible value =1

    NSE: 

        Nash-Sutcliffe Efficiency coefficienct
        Range [-inf to 1]

        NSE value 1 means a perfect model
        NSE > 0.6 is considerd as a good model.

    MSE: 
        
        Mean Squared Error
        lower is better

    RMSE:
        
        Root Mean Squared Error
        squared root of MSE
        lower is better

'''



def R2(x,y):
    
    # check & calculate sample shape
    if shapeAlike(x,y):
        n = x.shape[0]
    else:
        return -1

    NU = (n * ((x*y).sum()) - (x.sum()) * (y.sum()))**2
    DE = (n * ((x**2).sum()) - (x.sum())**2 ) * ( n * ((y**2).sum()) - (y.sum())**2 ) 
    
    return NU/DE


def NSE(sim,obs):

    # N.B. sim and obs is not interchangeable for NSE
    
    if not shapeAlike(sim,obs): return -1

    return 1 - ( ((sim - obs)**2).sum() / ((obs-obs.mean())**2).sum() )

def MSE(x,y):
    
    if not shapeAlike(x,y): return -1

    return ((x - y)**2).sum() / x.shape[0]

def RMSE(x,y):

    if not shapeAlike(x,y): return -1
    
    return np.sqrt(MSE(x,y))



def objectiveFunc(parameterArr,rainfall,evapotranspiration,area,delT,observedDischarge,errorFunc):


    simulatedDischarge = tankDischarge(rainfall,evapotranspiration,parameterArr,area,delT)

    if errorFunc == 'RMSE':
        return RMSE(simulatedDischarge,observedDischarge)
    
    elif errorFunc == 'MSE':
        return RMSE(simulatedDischarge,observedDischarge)
    
    elif errorFunc == 'NSE':
        return 1 - NSE(simulatedDischarge,observedDischarge)

    elif errorFunc == 'R2':
        return R2(simulatedDischarge,observedDischarge)


def calibrate(rainfall,evapotranspiration,area,delT,observedDischarge,errorFunc='RMSE'):

    '''
    Single watershed/Grid calibration
    ---------------------------------
    produces calibrated parameter for a single watershed
    '''

    # randomly generate initial values within bounds
    
    initialGuess = np.random.uniform(GP.tankLowerBounds,GP.tankUpperBounds) 

    paramBounds = np.column_stack((GP.tankLowerBounds,GP.tankUpperBounds))

    optimizer = minimize(objectiveFunc,initialGuess,
                args=(rainfall,evapotranspiration,area,delT,observedDischarge,errorFunc),
                method='L-BFGS-B',
                bounds=paramBounds
                )
    
    return optimizer.x

#__end__


