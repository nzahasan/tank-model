#!/usr/bin/env bash
#: split ecmwf seas (R1Lmmdd0000MM______1) into seperte files for each ensemble
#: 3 input required yyyy($1) mm($2) dd($3)
#: out 41 grib files containing parameter of cp,lsp & t2m

# get input vars
year=$1
month=$2
day=$3

# define dirs
root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
concat_out_file="/home/nazmul/__tmp__/R1L.concat.01032021.grib"
split_out_loc="/home/nazmul/seas_split"
seas_data_loc="/ECMWF/Historical_ECMWF/${year}/${month}/${day}"


# concatenate grib files for frist 3 month
cat $seas_data_loc/R1L030100000[3-5]______1 > $concat_out_file


# split combined grib by grib_filter (requires libeccodes-tools)
grib_filter $root_dir/seas_cp_lsp_t2m.filter $concat_out_file

# check if files are there

# delete 
rm $concat_out_file
