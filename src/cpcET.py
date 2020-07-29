#!/usr/bin/env python3
'''
	Calculate ETo  form CPC global gridded temperature data
	using Hargreaves and Samani,1982 et0 model

'''

from netCDF4 import Dataset as nco ,num2date
import numpy as np
import evapotranspiration as et
import argparse
from datetime import datetime

def main():


	# 
	arg_parser = argparse.ArgumentParser(
		description="Calculate ET0 from cpc tmin & tmin data",
		usage='use "%(prog)s --help" for more information',
	)

	arg_parser.add_argument('-tmax_nc',dest="tmax_nc",required=True,type=str,help='CPC tmax nc file')

	arg_parser.add_argument('-tmin_nc',dest="tmin_nc",required=True,type=str,help='CPC tmax nc file')

	arg_parser.add_argument('-o',dest="out",required=True,type=str,help='output file name')

	args = arg_parser.parse_args()


	tmax_nc = nco(args.tmax_nc,'r')
	tmin_nc = nco(args.tmin_nc,'r')
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

	# zip with initial index
	lat_z = list(zip(np.arange(lats.shape[0])[lat_mask],lat_f))
	lon_z = list(zip(np.arange(lons.shape[0])[lon_mask],lon_f))

	for ic,(io,i_lat) in enumerate(lat_z):
		for jc,(jo,j_lon) in enumerate(lon_z):
			# vectorize for each location
			var_et[:,ic,jc] = np.vectorize(et.hargreaves)(tmin_var[:,io,jo],tmax_var[:,io,jo],dates,i_lat)


	# write nc file

	with nco(args.out,'w') as ncwf:

		time_dim = ncwf.createDimension("time",None)
		lat_dim  = ncwf.createDimension("lat",lat_f.shape[0])
		lon_dim  = ncwf.createDimension("lon",lon_f.shape[0])

		# time var
		time_var = ncwf.createVariable('time','f8',dimensions=('time'))
		time_var[:]            = time_tmax[:]
		time_var.long_name     = tmax_nc.variables['time'].long_name
		time_var.standard_name = tmax_nc.variables['time'].standard_name
		time_var.axis          = tmax_nc.variables['time'].axis
		time_var.units         = tmax_nc.variables['time'].units
		time_var.delta_t       = tmax_nc.variables['time'].delta_t


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
		et0_nc.level_desc  = tmax_nc.variables['tmax'].level_desc;

		# global attr
		ncwf.version         = "CPC_HS_ET0_V1.0"
		ncwf.dataset_title   = "Reference evapotranspiration derived from CPC temperature data using Hargreaves & Samani model"
		ncwf.cpc_data_source = "https://psl.noaa.gov/data/gridded/data.cpc.globaltemp.html"
		ncwf.creation_time   = datetime.today().strftime('%Y-%m-%d %H:%M')
		


if __name__ == '__main__':
	main()