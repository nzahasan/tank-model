# -*- coding: utf-8 -*-
'''
 Core computation module for Tank Hydrologic model
 proposed by Sugawara and Funiyuki (1956)

 References:
 - A conceptual rainfall-runoff model considering seasonal variation
    (Kyungrock Paik, Joong H. Kim, Hung S. Kim and Dong R. Lee)
'''

import numpy as np
from . import utils



def tank_discharge(
    # time series information [should be of regular interval]
    precipitation:np.ndarray, evapotranspiration:np.ndarray, del_t:float,
    
    # basin characterstics
    area:float,
    
    # tank 0 
    t0_is:float, t0_boc:float, 
    t0_soc_uo:float, t0_soc_lo:float, 
    t0_soh_uo:float, t0_soh_lo:float,
    
    # tank 1
    t1_is:float, t1_boc:float, t1_soc:float, t1_soh:float,
    
    # tank 2
    t2_is:float, t2_boc:float, t2_soc:float, t2_soh:float,
    
    # tank 3
    t3_is:float, t3_soc:float) -> tuple:
    
    '''
    ________________________________________________
    |                UNITS:                        |
    |______________________________________________|
    |    area                 |       KM^2         |
    |    del_t                |       HR           |
    |    discharge            |       M^3/s        |
    |    precipitation        |       MM           |
    |    evapotranspiration   |       MM           |
    |_________________________|____________________|

    :: returns a tuple containing simulated discharge and model states
       -> [np.ndarray, dict[str, np.ndarray]]
    '''

    
    # calculate timestep length
    
    if not utils.shape_alike(precipitation, evapotranspiration):
    
        raise ValueError('ERROR-TANK-01: length mismatch between precipitation and evapotranspiration data')    
    
    time_step = precipitation.shape[0]

    # check for parameter: for Tank-0
    if t0_soh_uo < t0_soh_lo:
        print('WARNING-TANK-01: Invalid parameter upper outlet height is less than lower outlet height (Tank 0)')

    tank_storage       = np.zeros((time_step,4),dtype=np.float64)
    side_outlet_flow   = np.zeros((time_step,4),dtype=np.float64) 
    bottom_outlet_flow = np.zeros((time_step,3),dtype=np.float64)   
    
    # Difference of precipitation & evapotranspiration [only inflow to Tank 0]
    
    del_rf_et = precipitation - evapotranspiration
    
    
    # set initial tank storages | set to 0 if negetive value

    tank_storage[0,0] = max(t0_is, 0)
    tank_storage[0,1] = max(t1_is, 0)
    tank_storage[0,2] = max(t2_is, 0)
    tank_storage[0,3] = max(t3_is, 0)

    # main time loop 
    
    for t in np.arange(time_step):
    
        '''
        Side Outlet Flow :
        ------------------
        side outlet flow = fn(storage_above_outlet_height)
        
        There will be zero flow if tank storage less than outlet height
        Note: If Tank-0's storage is not greater than lower outlet
        then there is no flow from upper outlet
        '''

        # TANK 0 : surface runoff
        side_outlet_flow[t,0] = t0_soc_lo * max( tank_storage[t,0] - t0_soh_lo, 0 ) \
                            + t0_soc_uo * max( tank_storage[t,0] - t0_soh_uo, 0 )
        
        # TANK 1 : intermediate runoff
        side_outlet_flow[t,1]  = t1_soc * max( tank_storage[t,1] - t1_soh, 0 )
        

        # TANK 2 : sub-base runoff
        side_outlet_flow[t,2]  = t2_soc * max( tank_storage[t,2] - t2_soh, 0 )
        
        
        # TANK 3 : baseflow | Side outlet height = 0
        side_outlet_flow[t,3]  = t3_soc *  tank_storage[t,3]
        
        '''
        Bottom outlet flow :
        --------------------
        bottom outlet flow = fn(tank_storage)
        '''

        bottom_outlet_flow[t,0] = t0_boc * tank_storage[t,0]
        bottom_outlet_flow[t,1] = t1_boc * tank_storage[t,1]
        bottom_outlet_flow[t,2] = t2_boc * tank_storage[t,2]

        # N.B. tank 3 has no bottom outlet
        # Tank storage calculation of next time step

        '''
        Tank storage:
        -------------
        tank_storage[t+1] = tank_storage[t] 
                            + (precip[t+1] - evap[t+1])
                            + bottom_outlet_flow_of_upper_tank[t]
                            - (side_outlet_flow[t] + bottom_outlet_flow[t]) 
        '''
        if t< time_step -1:
            tank_storage[t+1,0] = tank_storage[t,0] + del_rf_et[t+1] - ( side_outlet_flow[t,0] + bottom_outlet_flow[t,0] )
        
            tank_storage[t+1,1] = tank_storage[t,1] + bottom_outlet_flow[t,0] - ( side_outlet_flow[t,1] + bottom_outlet_flow[t,1] ) 
            
            tank_storage[t+1,2] = tank_storage[t,2] + bottom_outlet_flow[t,1] - ( side_outlet_flow[t,2] + bottom_outlet_flow[t,2] ) 

            tank_storage[t+1,3] = tank_storage[t,3] + bottom_outlet_flow[t,2] - side_outlet_flow[t,3] 
            
            # Set tank storage = 0 if tank storage is negetive
            
            tank_storage[t+1,0] = max(tank_storage[t+1,0],0)
            tank_storage[t+1,1] = max(tank_storage[t+1,1],0)
            tank_storage[t+1,2] = max(tank_storage[t+1,2],0)
            tank_storage[t+1,3] = max(tank_storage[t+1,3],0)

            
        '''
        Outlet flow check
        -----------------
        If tank outflow becmes greater than  current storage(previous storage + inflow) 
        the storage will be negetive. Side outlet flow + bottom outlet flow must not be 
        greater than current storage. 
        
        The following sections checks for such error
        '''

        for i in range(4):

            total_tank_outflow = bottom_outlet_flow[t,i] + side_outlet_flow[t,i]  if i<=2 else side_outlet_flow[t,i]
            
            if total_tank_outflow > tank_storage[t,i]:
                print(f'WARNING-TANK-02: Total outlet flow exceeded tank storage for tank {i} at timestep {t}')
            

    '''
    unit conversion coefficent for m^3/s

        MM x KM^2     10^-3 x 10^6                1000
    :: ----------- = --------------- [m^3s^-1]  = -------- [m^3s^-1]
            Hr            60x60                   3600
    '''

    UNIT_CONV_COEFF = (area * 1000)/(del_t * 3600)

    discharge = UNIT_CONV_COEFF * side_outlet_flow.sum(axis=1)

    states = dict(
        tank_storage = tank_storage,
        side_outlet_flow =  side_outlet_flow, 
        bottom_outlet_flow = bottom_outlet_flow
    )

    # returns - time series of discharge & states
    return discharge, states
