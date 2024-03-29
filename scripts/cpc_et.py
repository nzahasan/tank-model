#!/usr/bin/env python3
'''
    Calculate reference evapotranspiration (ETo) form CPC 
    global gridded temperature data using 
    Hargreaves and Samani,1982 et0 model

    CPC data link:
     - https://psl.noaa.gov/data/gridded/data.cpc.globaltemp.html
'''

import click
import numpy as np
from datetime import datetime
from netCDF4 import Dataset, num2date

from tank_core import evapotranspiration as et


@click.command('Generate ET0 netCDF from CPC tmax & tmin data.')
@click.option('--tmax_nc', '-tx',  help='tmax netcdf path', required=True)
@click.option('--tmin_nc', '-tn',  help='tmax netcdf path', required=True)
@click.option('--outfile', '-o',  help='output netcdf path', required=True)
def main(tmax_nc, tmin_nc, outfile):


    tmax_nc = Dataset(tmax_nc,'r')
    tmin_nc = Dataset(tmin_nc,'r')
    # check if file is already exists

    # check variable
    lats = tmax_nc.variables['lat'][:]
    lons = tmax_nc.variables['lon'][:]


    time_tmax = tmax_nc.variables['time']
    time_tmin = tmin_nc.variables['time']

    if not np.array_equal(time_tmax[:],time_tmin[:]):
        print('time mismatch between min and max nc')

    dates = num2date(time_tmax[:],time_tmax.units)
    tmin_var = tmin_nc.variables['tmin'][:]

    tmax_var = tmax_nc.variables['tmax'][:]

    # move this to argument parser
    lat_min,lat_max=15,45
    lon_min,lon_max=60,110

    lat_mask = (lats>=lat_min) & (lats <= lat_max)
    lon_mask = (lons>=lon_min) & (lons <= lon_max)

    

    lat_f = lats[lat_mask]
    lon_f = lons[lon_mask]

    root_mask = tmax_var.mask[np.ix_( [True]*dates.shape[0] ,lat_mask,lon_mask )]


    var_et = np.ma.masked_array(
                data = np.zeros((dates.shape[0],lat_f.shape[0],lon_f.shape[0])),
                mask = root_mask
                )

    # zip with original index
    lat_z = list(zip( np.arange( lats.shape[0] )[lat_mask], lat_f ))
    lon_z = list(zip( np.arange( lons.shape[0] )[lon_mask], lon_f ))


    for ic,(io,i_lat) in enumerate(lat_z):
        for jc,(jo,j_lon) in enumerate(lon_z):
            # vectorize for each location
            var_et[:,ic,jc] = np.vectorize(et.hargreaves)(tmin_var[:,io,jo],tmax_var[:,io,jo],dates,i_lat)
            

    # write to nc file

    with Dataset(outfile,'w') as ncwf:

        ncwf.createDimension("time",None)
        ncwf.createDimension("lat",lat_f.shape[0])
        ncwf.createDimension("lon",lon_f.shape[0])

        # time var
        time_var = ncwf.createVariable('time','f8',dimensions=('time'))
        time_var[:]            = time_tmax[:]
        time_var.long_name     = tmax_nc.variables['time'].long_name
        time_var.standard_name = tmax_nc.variables['time'].standard_name
        time_var.axis          = tmax_nc.variables['time'].axis
        time_var.units         = tmax_nc.variables['time'].units
        # time_var.delta_t       = tmax_nc.variables['time'].delta_t


        lat_var = ncwf.createVariable('lat','f4',dimensions=('lat'))
        lat_var[:]            = lat_f
        lat_var.long_name     = tmax_nc.variables['lat'].long_name
        lat_var.standard_name = tmax_nc.variables['lat'].standard_name
        lat_var.axis          = tmax_nc.variables['lat'].axis
        lat_var.units         = tmax_nc.variables['lat'].units


        lon_var = ncwf.createVariable('lon','f4',dimensions=('lon'))
        lon_var[:]            = lon_f
        lon_var.long_name     = tmax_nc.variables['lon'].long_name
        lon_var.standard_name = tmax_nc.variables['lon'].standard_name
        lon_var.axis          = tmax_nc.variables['lon'].axis
        lon_var.units         = tmax_nc.variables['lon'].units

        et0_nc = ncwf.createVariable('et0','f4',dimensions=('time','lat','lon'))
        et0_nc[:]          = var_et
        et0_nc.long_name   = 'Reference Evapotranspiration'
        et0_nc.var_desc    = 'Daily reference evapotranspiration using Hargreaves & Samani'
        et0_nc.units       = 'mm'
        et0_nc.description = 'Reference et derived from CPC daily temperature data'
        et0_nc.level_desc  = tmax_nc.variables['tmax'].level_desc

        # global attr
        ncwf.version         = "CPC_HS_ET0_V1.0"
        ncwf.dataset_title   = "Reference evapotranspiration derived from CPC temperature data using Hargreaves & Samani model"
        ncwf.cpc_data_source = "https://psl.noaa.gov/data/gridded/data.cpc.globaltemp.html"
        ncwf.creation_time   = datetime.today().strftime('%Y-%m-%dT%H:%M%S')
        


if __name__ == '__main__':
    main()