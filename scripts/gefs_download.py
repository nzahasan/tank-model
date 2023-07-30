#!/usr/bin/env python3

import time
import click
import shutil
import subprocess
import requests as req 
from pathlib import Path
from multiprocessing.pool import ThreadPool

SLEEP_TIME = 2*60 # in seconds

REQ_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0'
}

def eccodes_available() -> bool:

    if shutil.which('grib_copy') is None:
        return (False, 'eccodes# grib_copy command not found')
    
    if shutil.which('grib_to_netcdf') is None:
        return (False, 'eccodes#  grib_to_netcdf command not found')

    return (True, 'eccodes# grib_copy, grib_to_netcdf command available')

def download_file(parameters:tuple, logging=True) -> None:
    (url, filename, output_dir) = parameters
    
    output_path = output_dir / filename

    try:
        req_dat = req.get(url, headers=REQ_HEADERS)

        if req_dat.status_code==200:
            with open(output_path,'wb') as gf:
                for chunk in req_dat.iter_content(chunk_size=4096):
                    if chunk: gf.write(chunk)
                print(f'done# {filename}')
        else:
            if logging == True:
                print(f'status is not 200# {url}')
                print(f'status is not 200# sleeping then re-spawning')
            time.sleep(SLEEP_TIME)
            download_file(parameters)
    except:
        if logging == True:
            print(f'req crashed# {url}')
            print(f'req crashed# sleeping then re-spawning')
        time.sleep(SLEEP_TIME)
        download_file(parameters)

def merge_grib_convert_nc(output_dir, cycle):
    
    for ens in range(31):

        _pre = 'gec' if ens==0 else 'gep'
        
        file_paths = list()

        for hr in range(3,243,3):
            _fname = f'{_pre}{ens:02d}.t{cycle}z.pgrb2s.0p25.f{hr:03d}'

            _full_path = output_dir / _fname 

            file_paths.append(_full_path)

        file_checks = [fpath.exists() for fpath in file_paths]


        if False in file_checks:
            print(f'file check# all files are not available')
            print(f'file check# skipping for ens - {ens:02}')
            continue    
        
        
        _out_path_grib = output_dir / f'{_pre}{ens:02d}.t00z.pgrb2s.0p25.grib2'
        _out_path_nc = output_dir / f'{_pre}{ens:02d}.t00z.pgrb2s.0p25.nc4'

        grib_copy_commands = ['grib_copy'] + file_paths + [_out_path_grib]
        
        result = subprocess.run(grib_copy_commands, stdout=subprocess.PIPE)
        
        print("grib_copy#", result.stdout.decode('utf-8'))

        grib_to_nc_commands = ['grib_to_netcdf', '-k', '3'] + ['-o', _out_path_nc] + [ _out_path_grib]
        
        result = subprocess.run(grib_to_nc_commands, stdout=subprocess.PIPE)
        
        print("grib_to_netcdf#", result.stdout.decode('utf-8'))

@click.command('Downloads [GEFS - Atmos - pgrb2sp25] forecast data')
@click.option('--date', '-d',  help='forecast date in YYYYMMDD format', type=str, required=True)
@click.option('--cycle', '-c',  help='forecast cycle', type=click.Choice(['00', '06', '12', '18']), required=True)
@click.option('--left', '-l',  help='left longitude', type=float, required=True)
@click.option('--right', '-r',  help='right longitude', type=float,  required=True)
@click.option('--bottom', '-b',  help='bottom latitude', type=float, required=True)
@click.option('--top', '-t',  help='top latitude', type=float, required=True)
@click.option('--output-dir', '-o',  help='output path', type=click.Path(exists=False), required=True)
@click.option('--n-process', '-np',  help='how many files to download in parallel', type=int, default=1)
def main(date:str, cycle:str, left:float, right:float, bottom:float, top:float, output_dir:Path, n_process:int):

    status, msg = eccodes_available()

    print(msg)

    # exit if eccodes is not available
    if status!=True :
        return 
    
    output_dir = Path(output_dir)

    if not output_dir.exists():
        output_dir.mkdir()

    url_list = list()

    # build urls 

    for ens in range(31):

        _pre = 'gec' if ens==0 else 'gep'

        for hr in range(3,243,3):

            _fname = f'{_pre}{ens:02d}.t{cycle}z.pgrb2s.0p25.f{hr:03d}'

            full_url  = f"https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p25s.pl?"
            full_url += f"dir=/gefs.{date}/{cycle}/atmos/pgrb2sp25"
            full_url += f"&file={_fname}"
            full_url += f"&var_APCP=on&var_TMAX=on&var_TMIN=on&lev_surface=on"
            full_url += f"&subregion=&toplat={top}&leftlon={left}&rightlon={right}&bottomlat={bottom}"

            url_list.append( (full_url, _fname, output_dir) )

    
    # download files parallel
    pool = ThreadPool(processes=n_process)
    pool.map(download_file, url_list)
    pool.close()

    # merge grib files and convert to netcdf4
    merge_grib_convert_nc(output_dir, cycle)
    


if __name__ == "__main__":
    main()