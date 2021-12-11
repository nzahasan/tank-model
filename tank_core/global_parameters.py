import numpy as np


'''
This file contains parameter bounds &
necessary parameter defination 
for model calibration


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

class tankParamBounds:
    
    class t0:
        class _is:
            _min = 0.01
            _max = 100
        class _boc:
            _min = 0.1
            _max = 0.5
        class _soc: 
            class _uo:
                _min = 0.1 
                _max = 0.5 
            class _lo: 
                _min = 0.1 
                _max = 0.5 
        class _soh: 
            class _uo:
                _min = 25
                _max = 50 
            class _lo:
                _min = 0 
                _max = 20 

    class t1:
        class _is: 
            _min = 0.01
            _max = 100
        class _boc:
            _min = 0.01
            _max = 0.5
        class _soc:
            _min = 0.01
            _max = 0.5
        class _soh:
            _min = 0
            _max = 50

    class t2:
        class _is: 
            _min = 0.01
            _max = 100
        class _boc:
            _min = 0.01
            _max = 0.5
        class _soc:
            _min = 0.01
            _max = 0.5
        class _soh:
            _min = 0
            _max = 50

    class t3:
        class _is:
            _min = 0.01
            _max = 100
        class _soc:
            _min = 0.01
            _max = 0.5


tankLowerBounds = np.array([
            
            # [Tank-0] 
    tankParamBounds.t0._is._min,
    tankParamBounds.t0._boc._min,
    tankParamBounds.t0._soc._uo._min,
    tankParamBounds.t0._soc._lo._min,
    tankParamBounds.t0._soh._uo._min,
    tankParamBounds.t0._soh._lo._min,
            
            # [Tank-1]
    tankParamBounds.t1._is._min,
    tankParamBounds.t1._boc._min,
    tankParamBounds.t1._soc._min,
    tankParamBounds.t1._soh._min,
            
            # [Tank-2]
    tankParamBounds.t2._is._min,
    tankParamBounds.t2._boc._min,
    tankParamBounds.t2._soc._min,
    tankParamBounds.t2._soh._min,
            
            # [Tank-3]
    tankParamBounds.t3._is._min,
    tankParamBounds.t3._soc._min,

    ])



tankUpperBounds = np.array([ 
            
            # [Tank-0] 
    tankParamBounds.t0._is._max,
    tankParamBounds.t0._boc._max,
    tankParamBounds.t0._soc._uo._max,
    tankParamBounds.t0._soc._lo._max,
    tankParamBounds.t0._soh._uo._max,
    tankParamBounds.t0._soh._lo._max,
            
            # [Tank-1]
    tankParamBounds.t1._is._max,
    tankParamBounds.t1._boc._max,
    tankParamBounds.t1._soc._max,
    tankParamBounds.t1._soh._max,
            
            # [Tank-2]
    tankParamBounds.t2._is._max,
    tankParamBounds.t2._boc._max,
    tankParamBounds.t2._soc._max,
    tankParamBounds.t2._soh._max,
            
            # [Tank-3]
    tankParamBounds.t3._is._max,
    tankParamBounds.t3._soc._max,

])
