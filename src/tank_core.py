#! /usr/bin/env python3
#cython: language_level=3
'''
:: Core computation module for Tank Hydrologic model ::

'''

import numpy as np


def shape_alike(x,y):
    # checks if x,y numpy array are of same shape
    return True if x.shape == y.shape else False
        



def tank_discharge(
    # time series information
    rainfall, evapotranspiration, del_t,

    # basin characterstics
    area,
    # tank 0 
    t0_is, t0_boc, t0_soc_uo,t0_soc_lo, t0_soh_uo, t0_soh_lo,
    # tank 1
    t1_is, t1_boc, t1_soc, t1_soh,
    # tank 2
    t2_is, t2_boc, t2_soc, t2_soh,
    # tank 3
    t3_is, t3_soc):
    
    '''
        ________________________________________________
        |                UNITS:                        |
        |______________________________________________|
        |    area                 |       KM^2         |
        |    del_t                |       HR           |
        |    discharge            |       M^3/s        |
        |    rainfall             |       MM           |
        |    evapotranspiration   |       MM           |
        |_________________________|____________________|

        :: returns a time-series of simulated discharge
    '''


    # calculate timestep length
    
    if shape_alike(rainfall, evapotranspiration):
        time_step = rainfall.shape[0]
    else:
        print('ERROR 1001: length mismatch between rainfall and evapotranspiration data')
        return -1


    # check for parameter: for Tank-0
    if t0_soh_uo < t0_soh_lo:
        print('WARNING 5001: Parameter error upper outlet height is less than lower outlet height (Tank 0)')

    tank_storage       = np.zeros((time_step,4),dtype=np.float64)
    side_outlet_flow   = np.zeros((time_step,4),dtype=np.float64) 
    bottom_outlet_flow = np.zeros((time_step,3),dtype=np.float64)   
    
    # Difference of rainfall & evapotranspiration [only inflow to Tank 0]
    
    del_rf_et = rainfall - evapotranspiration
    
    
    # set initial tank storages

    tank_storage[0,0] = t0_is
    tank_storage[0,1] = t1_is
    tank_storage[0,2] = t2_is
    tank_storage[0,3] = t3_is

    # Loop through the timeseries 
    
    for t in np.arange(1,time_step):
    
           
        '''
            Tank Storage Calculation
        ----------------------------
        storage  =  inflow - outflow
        
        '''
        
        tank_storage[t,0] = ( tank_storage[t-1,0] + del_rf_et[t] ) - ( side_outlet_flow[t-1,0] + bottom_outlet_flow[t-1,0] )
    
        tank_storage[t,1] = ( tank_storage[t-1,1] + bottom_outlet_flow[t-1,0] ) - ( side_outlet_flow[t-1,1] + bottom_outlet_flow[t-1,1] ) 
        
        tank_storage[t,2] = ( tank_storage[t-1,2] + bottom_outlet_flow[t-1,1] ) - ( side_outlet_flow[t-1,2] + bottom_outlet_flow[t-1,2] ) 

        tank_storage[t,3] = ( tank_storage[t-1,3] + bottom_outlet_flow[t-1,2] ) - ( side_outlet_flow[t-1,3]  ) 
            
        

        '''
        Handling negetive tank storage:
        -------------------------------
        Set tank storage = 0 if tank storage is negetive
        
        N.B. evapotranspiration rate can be more than precipitation rate
        in that case tank storage can be negetive value
        '''
        
        tank_storage[t,0] = max(tank_storage[t,0],0)
        tank_storage[t,1] = max(tank_storage[t,1],0)
        tank_storage[t,2] = max(tank_storage[t,2],0)
        tank_storage[t,3] = max(tank_storage[t,3],0)

        '''
        If tank outflow becmes greater than  current storage(previous storage + inflow) the storage will be negetive
        which is incorrect. Side outlet flow + bottom outlet flow must not be greater than current storage.
        
        As example if the bottom outlet storage coefficient is 1 and side outlet height 0 and coefficient is 1
        the output flow will be greater than what in storage which is impossible. 
        '''
        

        '''
        Side Outlet Flow :
        ------------------
        side outlet flow = f(tank_storage,outletHeight)
        
        There will be zero flow if tank storage less than outlet height
        '''

        # TANK 0 : surface runoff
        
        '''
        Note: If Tank-0's storage is not greater than lower outlet
        then there is no flow from upper outlet
        '''
        
        # Check if storage height > Lower Outlet
        if tank_storage[t,0] >  t0_soh_lo:
            
            side_outlet_flow[t,0] = t0_soc_lo * ( tank_storage[t,0] - t0_soh_lo )
            
            # Lower outlet is filled check for upper outlet
            if tank_storage[t,0] >  t0_soh_uo:
                side_outlet_flow[t,0] += t0_soc_uo * ( tank_storage[t,0] - t0_soh_uo )
        
        else:
            side_outlet_flow[t,0] = 0


        # TANK 1 : intermediate runoff
        
        if tank_storage[t,1] > t1_soh:
            side_outlet_flow[t,1]  = t1_soc * ( tank_storage[t,1] - t1_soh )
        
        else:
            side_outlet_flow[t,1] = 0

        # TANK 2 : sub-base runoff
        
        if tank_storage[t,2] > t2_soh:
            side_outlet_flow[t,2]  = t2_soc * ( tank_storage[t,2] - t2_soh )
    
        else:
            side_outlet_flow[t,2] = 0
            
        
        # [TANK 3 : baseflow] 
        
        '''
        Side outlet height = 0
        '''
        if tank_storage[t,3] >=0:
            side_outlet_flow[t,3]  = t3_soc * ( tank_storage[t,3] )

        else:
            side_outlet_flow[t,3]
        
        
        '''
        Bottom outlet flow :
        --------------------
        bottom outlet flow = f(tank_storage)
        
        No need apply condition here, 
        because theoritacilly tank_storage will never be negetive
        '''

        bottom_outlet_flow[t,0] = t0_boc * tank_storage[t,0]

        bottom_outlet_flow[t,1] = t1_boc * tank_storage[t,1]
        
        bottom_outlet_flow[t,2] = t2_boc * tank_storage[t,2]

        # N.B. tank 3 has no bottom outlet

        '''
        Check for parameter error (parameter debugging)
        -----------------------------------------------
        Check that enough water was availble in the tank 
        to satisfy side and bottom outlet flow.
        '''

        for i in range(4):
            if i <=2:
                if tank_storage[t,i] < bottom_outlet_flow[t,i] + side_outlet_flow[t,i]:
                    print('WARNING 5002: Total outlet flow exceeded tank storage for tank ',i)
            if i==3:
                # again no bottom outlet in Tank-3
                if tank_storage[t,i] < side_outlet_flow[t,i]:
                    print('WARNING 5003: Side outlet flow exceeded tank storage for tank ',i)
    

    '''
        unit conversion coefficent for m^3/s

            MM x KM^2     10^-3 x 10^6                1000
        :: ----------- = --------------- [m^3/2]  = -------- [m^3/2]
                Hr            60x60                   3600


    '''

    UNIT_CONV_COEFF = 1000/3600

    discharge = UNIT_CONV_COEFF * (side_outlet_flow.sum(axis=1) *  area / del_t)


    # time series of discharge
    return discharge

