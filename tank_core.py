#! /usr/bin/env python3


'''
: Core computation module for Tank Hydrologic model

'''


import numpy as np


def shapeAlike(x,y):
    # checks if x,y numpy array are of same shape
    if x.shape==y.shape: return True
    else: return False



def tank_discharge(
    #time series information
    rainfall,evapotranspiration,delT,
    # basin characterstics
    area,
    # tank 0 
    t0_is,t0_boc,t0_soc_uo,t0_soc_lo,t0_soh_uo,t0_soh_lo,
    # tank 1
    t1_is,t1_boc,t1_soc,t1_soh,
    # tank 2
    t2_is,t2_boc,t2_soc,t2_soh,
    # tank 3
    t3_is,t3_soc):
    
    '''
        ------------------------------------------------
        |                UNITS:                        |
        ------------------------------------------------
        |    area                 |       km^2         |
        |    delT                 |       hr           |
        |    discharge            |       m^3/s        |
        |    rainfall             |       mm           |
        |    evapotranspiration   |       mm           |
        ------------------------------------------------

        :: returns a time-series of simulated discharge
    '''


    # calculate timestep length
    
    if shapeAlike(rainfall, evapotranspiration):
        timeSetp = rainfall.shape[0]
    else:
        print('ERROR 1001: length mismatch between rainfall and evapotranspiration data')
        return -1


    # check for parameter: for Tank-0
    if t0_soh_uo < t0_soh_lo:
        print('WARNING 1001: Parameter error upper outlet height is less than lower outlet height (Tank 0)')

    tankStorage      = np.zeros((timeSetp,4),dtype=np.float64)
    sideOutletFlow   = np.zeros((timeSetp,4),dtype=np.float64) 
    bottomOutletFlow = np.zeros((timeSetp,3),dtype=np.float64)   
    
    # Difference of rainfall & evapotranspiration [only inflow to Tank 0]
    
    delRf_Et = rainfall - evapotranspiration
    
    # Loop through the timeseries 
    
    for t in range(timeSetp):
    
       

        if t == 0:
            # set initial storage of the tank's
            tankStorage[t,0] = t0_is
            tankStorage[t,1] = t1_is
            tankStorage[t,2] = t2_is
            tankStorage[t,3] = t3_is
        
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
        if tankStorage[t,0] >  t0_soh_lo:
            
            sideOutletFlow[t,0] = t0_soc_lo * ( tankStorage[t,0] - t0_soh_lo )
            
            # Lower outlet is filled check for upper outlet
            if tankStorage[t,0] >  t0_soh_uo:
                sideOutletFlow[t,0] += t0_soc_uo * ( tankStorage[t,0] - t0_soh_uo )
        
        else:
            sideOutletFlow[t,0] = 0


        # --- TANK 1 / intermediate runoff ---
        
        if tankStorage[t,1] > t1_soh:
            sideOutletFlow[t,1]  = t1_soc * ( tankStorage[t,1] - t1_soh )
        
        else:
            sideOutletFlow[t,1] = 0

        # --- TANK 2 / sub-base runoff---
        
        if tankStorage[t,2] > t2_soh:
            sideOutletFlow[t,2]  = t2_soc * ( tankStorage[t,2] - t2soh )
    
        else:
            sideOutletFlow[t,2] = 0
            
        
        # --- TANK 3 / baseflow ---
        '''
        Side outlet height = 0
        '''
        if tankStorage[t,3] >=0:
            sideOutletFlow[t,3]  = t3_soc * ( tankStorage[t,3] )

        else:
            sideOutletFlow[t,3]
        
        
        '''
        Bottom outlet flow :
        --------------------
        bottom outlet flow = f(tankStorage)
        
        No need apply condition here, 
        because theoritacilly tankStorage will never be negetive
        '''

        bottomOutletFlow[t,0] = t0_boc * tankStorage[t,0]

        bottomOutletFlow[t,1] = t1_boc * tankStorage[t,1]
        
        bottomOutletFlow[t,2] = t2_boc * tankStorage[t,2]

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
                    print('WARNING 1002: Total outlet flow exceeded tank storage for tank ',i)
            if i==3:
                # again no bottom outlet in Tank-3
                if tankStorage[t,i] < sideOutletFlow[t,i]:
                    print('WARNING 1003: Side outlet flow exceeded tank storage for tank ',i)
    
    discharge = sideOutletFlow.sum(axis=1) * ( (area * 1e3) / (delT*60*60)  ) 


    return discharge