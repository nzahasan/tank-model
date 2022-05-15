# -*- coding: utf-8 -*-
'''
    Reference evapotranspiration calculatin models

    References: 
    1. Evaluation of alternative methods for estimating reference evapotranspiration
       (Daniel K. Fisher, H. C. Pringle)
    2. Assessing of evapotranspiration models using limited climatic data in Southeast Anatolian Project Region of Turkey
       (Yusuf Aydin)
    3. https://www.sciencedirect.com/topics/engineering/solar-hour-angle#tp-snippet-chp-title-B9780080253886500490
'''

from math import sqrt,pi,radians,sin,cos,tan,acos,atan,sqrt
from datetime import datetime

def days_in_year(year:int):
    '''
        calculate number of days in a year
        considering leap years
    '''
    if   year%400==0 and year%100==0: return 366
    elif year%4==0 and year%100!=0: return 366
    else: return 365


def ext_ra(date:datetime,lat:float):

    '''
    Daily extra-terrestrial radiation 
    ---------------------------------
    inputs: tmin,tmax,date,lat

    Units:
    ------
    lat:  decimal degree 

    Output: MJ m^-2 day^-1
    '''


    lat_r   = radians(lat)                            # convert lat lon to radians (φ)

    jul_day = date.timetuple().tm_yday                # calculate jul_day 

    nday    = days_in_year(date.timetuple().tm_year)  # total days in the year

    gsc     = 0.082                                   # global solar constant

    _f = (2*pi*jul_day) / 365
    
    dr      = 1 + 0.033 * cos( _f )                  # inv. rel. distance Earth-Sun

    sda     = 0.409 * sin( _f - 1.39 )               # solar declination angle (δ)

    # can return undefined 
    sha     = acos( -1*tan(lat_r) * tan(sda) )         # sunset hour angle (ωs)

    ext_ra  = (1440/pi) * gsc * dr * (               # extraterrestial radiation daily
                sha * sin(lat_r) * sin(sda) 
                + 
                sin(sha) * cos(lat_r) * cos(sda) 
              ) 

    return ext_ra


# NB. this can only be applied to calculate daily et0
def hargreaves(tmin:float,tmax:float,date:datetime,lat:float)->float:
    '''
    Daily Evapotranspiration calculation (Hargreaves and Samani, 1982)
    ------------------------------------------------------------------
    inputs: tmin,tmax,date,lat
    
    Units:
    ------
    tmin: °C
    tmax: °C
    lat:  decimal degree 

    output: mm day^-1
    
    '''
    # check latitude
    if lat> 66.5 or lat<-66.5:
        raise ValueError('latitude out of bound for ext_ra calculation')

    tmean = (tmin+tmax)/2      # tmean

    ra = ext_ra(date,lat)

    lhv = 2.45 
    # λ: the latent heat of vaporization MJ·kg−1 
    # converts to mm/day (1/2.45) = 0.408

    et0 = 0.0023 * (ra/lhv) * sqrt(tmax-tmin)*(tmean+17.8) 

    
    # et0 cannot be -ve
    return max(et0, 0.0)


'''
>> vectorization example

from datetime import datetime as dt,timedelta as delt

import numpy as np
tmin = np.arange(10,20)
tmax= np.arange(20,30)
start_date = dt.today()

# dates = np.vectorize(lambda sd,i: (sd+delt(days=int(i))) )(start_date,np.arange(10))
# et_ts = np.vectorize(hargreaves(tmax_arr,tmin_arr,date_arr,lat:fixed)


http://www.fao.org/3/X0490E/x0490e07.htm#solar%20radiation  [see example 8 for reference]
et_ts = hargreaves(10,20,datetime(2019,9,3),-20)
'''


