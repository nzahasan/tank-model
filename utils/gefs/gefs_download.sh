#!/usr/bin/env bash
# Data download program of
# GFS Ensemble forecast products

# whole 35 days data comes one day late
# download at 10pm BST

if [ -z $1 ];then 
    echo "provide analysis date as argument in yyyymmdd format"
    exit 200
fi

adate=$1   

# url_def
sub_region="&leftlon=70&rightlon=100&toplat=35&bottomlat=20"
url_pre="https://nomads.ncep.noaa.gov/cgi-bin/filter_gefs_atmos_0p50a.pl"



tmp_dir="./tmp/${adate}"
final_grib_dir="./final/${adate}"

mkdir -p $tmp_dir $final_grib_dir

echo "" >  "${tmp_dir}/$adate.00.link.list"

for ens in {00..30}; do 

    file_pref="gep"

    if [ $ens -eq '00' ];then

        file_pref="gec"
    fi
    

    for step_hr in {000..840..6};do
        file_name="${file_pref}${ens}.t00z.pgrb2a.0p50.f${step_hr}"
        ens_step_url="${url_pre}?file=${file_name}&lev_2_m_above_ground=on&lev_surface=on&var_APCP=on&var_TMAX=on&var_TMIN=on&subregion=${sub_region}&dir=/gefs.${adate}/00/atmos/pgrb2ap5"
        echo $ens_step_url >> "${tmp_dir}/$adate.00.link.list"    
    done
    

done


# download 10 files in parallel

aria2c -j10 -i "${tmp_dir}/${adate}.00.link.list" --dir=$tmp_dir

for ens in {00..30}; do 

    file_pref="gep"

    if [ $ens -eq '00' ];then

        file_pref="gec"
    fi
    

    cat $tmp_dir/$file_pref$ens* > $final_grib_dir/gefs.${adate}00.en${ens}.grib
    
    grib_to_netcdf $final_grib_dir/gefs.${adate}00.en${ens}.grib -o $final_grib_dir/gefs.${adate}00.en${ens}.nc

    # remove temp_files
    rm $final_grib_dir/gefs.${adate}00.en${ens}.grib

done

# remove temp downloaded directory
rm -r $tmp_dir