# -*- coding: utf-8 -*-
'''
Channel routing methods
'''

import numpy as np 


def muskingum(in_flow:np.ndarray, del_t:float, k:float, x:float) -> np.ndarray:

    '''
    Returns routed flow using Muskingum routing method
    (Lumped channel routing)
    
    Units:
    ------
    in_flow  - m^3/s
    del_t    - hr
    x        - hr

    @test_data: https://www.engr.colostate.edu/~ramirez/ce_old/classes/cive322-Ramirez/CE322_Web/Example_MuskingumRouting.htm
    '''

    # calculate timesetp
    n_step:int = in_flow.shape[0]
    
    # create a zero array of out_flow
    out_flow:np.ndarray = np.zeros(n_step, dtype=np.float64)

    C0:float = (-k*x+0.5*del_t) / (k*(1-x)+0.5*del_t)
    C1:float = ( k*x+0.5*del_t) / (k*(1-x)+0.5*del_t)
    C2:float = (k*(1-x)-0.5*del_t) / (k*(1-x)+0.5*del_t)

    # constraints check
    if (C0+C1+C2) > 1 or x >0.5 or (del_t/k + x) > 1:
        print("WARNING-MUSKINGUM-01: violates k, x constraints")

    # initial condition
    out_flow[0] = in_flow[0]

    for t in np.arange(1,n_step):

        out_flow[t] = C0*in_flow[t] + C1*in_flow[t-1] + C2*out_flow[t-1]

    return out_flow

