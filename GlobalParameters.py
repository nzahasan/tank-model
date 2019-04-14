#! /usr/bin/env python3
import numpy as np


'''
This file contains parameter bounds &

 necessary parameter defination for calibrating the model


Parameter order & description of vertical tanks:

t0 (6)
    - is  : initial storage
    - boc : bottom outlet coefficient
    - soc : side outlet coefficient [2]
        - uo : upper outlet
        - lo : lower outlet
    - soh : side outlet height [2]
        - uo : upper outlet
        - lo : lower outlet

t1 (4)
    - is  : initial storage
    - boc : bottom outlet coefficient
    - soc : side outlet coefficient [1]
    - soh : side outlet height [1]
t2 (4)
    - is  : initial storage
    - boc : bottom outlet coefficient
    - soc : side outlet coefficient [1]
    - soh : side outlet height [1]

t3 (2)
    - is  : initial storage
    - soc : side outlet coefficient [1]

'''

tankParamBounds = {

    't0':{
        'is'  : {'min':0.01,'max':100},
        'boc' : {'min':0.1,'max':0.5},
        'soc' : { 
                'uo': {'min':0.1,'max':0.5}, 
                'lo': {'min':0.1,'max':0.5} 
                }, 
        'soh' : { 
                'uo': {'min':25,'max':50}, 
                'lo': {'min':0,'max':20} 
                }
    },

    't1':{
        'is'  : {'min':0.01,'max':100},
        'boc' : {'min':0.01,'max':0.5},
        'soc' : {'min':0.01,'max':0.5},
        'soh' : {'min':0,'max':50},
    },

    't2':{
        'is'  : {'min':0.01,'max':100},
        'boc' : {'min':0.01,'max':0.5},
        'soc' : {'min':0.01,'max':0.5},
        'soh' : {'min':0,'max':50},
    },
    't3':{
        'is'  : {'min':0.01,'max':100},
        'soc' : {'min':0.01,'max':0.5},
    }
}


tankLowerBounds = np.array([
            
            # [Tank-0] 
    tankParamBounds['t0']['is']['min'],
    tankParamBounds['t0']['boc']['min'],
    tankParamBounds['t0']['soc']['uo']['min'],
    tankParamBounds['t0']['soc']['lo']['min'],
    tankParamBounds['t0']['soh']['uo']['min'],
    tankParamBounds['t0']['soh']['lo']['min'],
            
            # [Tank-1]
    tankParamBounds['t1']['is']['min'],
    tankParamBounds['t1']['boc']['min'],
    tankParamBounds['t1']['soc']['min'],
    tankParamBounds['t1']['soh']['min'],
            
            # [Tank-2]
    tankParamBounds['t2']['is']['min'],
    tankParamBounds['t2']['boc']['min'],
    tankParamBounds['t2']['soc']['min'],
    tankParamBounds['t2']['soh']['min'],
            
            # [Tank-3]
    tankParamBounds['t3']['is']['min'],
    tankParamBounds['t3']['soc']['min'],

    ])



tankUpperBounds = np.array([ 
            
            # [Tank-0]
    tankParamBounds['t0']['is']['max'],
    tankParamBounds['t0']['boc']['max'],
    tankParamBounds['t0']['soc']['uo']['max'],
    tankParamBounds['t0']['soc']['lo']['max'],
    tankParamBounds['t0']['soh']['uo']['max'],
    tankParamBounds['t0']['soh']['lo']['max'],

            # [Tank-1]
    tankParamBounds['t1']['is']['max'],
    tankParamBounds['t1']['boc']['max'],
    tankParamBounds['t1']['soc']['max'],
    tankParamBounds['t1']['soh']['max'],
            
            # [Tank-2]
    tankParamBounds['t2']['is']['max'],
    tankParamBounds['t2']['boc']['max'],
    tankParamBounds['t2']['soc']['max'],
    tankParamBounds['t2']['soh']['max'],
            
            # [Tank-3]
    tankParamBounds['t3']['is']['max'],
    tankParamBounds['t3']['soc']['max'],

    ])


