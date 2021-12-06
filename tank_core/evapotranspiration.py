'''
    Reference evapotranspiration calculatin models
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
        extra-terrestrial radiation [mm/day]
    '''

    lat_r   = radians(lat)                            # convert lat lon to radians

    jul_day = date.timetuple().tm_yday                # calculate jul_day 

    nday    = days_in_year(date.timetuple().tm_year)  # total days in the year

    gsc     = 0.082                                   # global solar constant

    dr      = 1+(0.033*cos(2*pi* (jul_day/nday )))    # inv. rel. distance Earth-Sun

    sda     = 0.409*sin( (2*pi*jul_day)/365 - 1.39 )  # solar declination angle

    # valid for 66.5N to 66.5S
    sha     = acos( -1*tan(lat_r)*tan(sda) )          # sunset hour angle

    ext_ra  = (1440/pi) * gsc * dr * (                # extraterrestial radiation daily
                sha * sin(lat_r)*sin(sda) 
                + 
                cos(lat_r)*cos(sda)*sin(sha) 
              ) 
    # [0.408 * ra] for converting MJ/d to mm/day (Allen, 1998)
    return 0.408*ext_ra



def hargreaves(tmin:float,tmax:float,date:datetime,lat:float):
    '''
    Daily Evapotranspiration calculation (Hargreaves and Samani, 1982)
    ------------------------------------------------------------------
    inputs: tmin,tmax,date,lat
    
    Units:
    ------
    tmin: °C
    tmax: °C
    lat:  decimal degree 

    output: mm/day
    '''
    # check latitude
    if lat> 66.5 or lat<-66.5:
        return None

    tmean   = 0.5*(tmin+tmax)      # tmean

    ra = ext_ra(date,lat)

    et = 0.0023 * ra * sqrt(tmax-tmin)*(tmean+17.8) 

    if et<0: 
    #     print(f'{tmin:0.2f},{tmax:0.2f},{date},{lat},{et:0.2f}')
        return None #invalid et
    
    return et


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


