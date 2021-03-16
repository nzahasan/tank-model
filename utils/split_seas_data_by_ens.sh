#!/usr/bin/env bash
#:-split ecmwf seas (R1Lmmdd0000MM______1) into seperte files for each ensemble
#:-3 input required yyyy($1) mm($2) 
#:-out 41 grib files containing parameter of cp,lsp & t2m

#:-check if input is provided
if [ -z $1 ] || [ -z $2  ]; then
    echo "Error: provide year and month argument as yyyy mm"
    exit 100
fi
#:-get input vars
year=$1
month=$2
day="01" # comes at every month's first day

#:-define dirs
root_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
concat_out_file="/home/nazmul/__tmp__/R1L.concat.${year}${month}${day}.grib"
split_out_loc="/home/nazmul/seas_split"
seas_data_loc="/ECMWF/Historical_ECMWF/${year}/${month}/${day}"


file_list=""

for m_i in {0..2}; do 

    file_month=$(( $(( $month + $m_i )) % 12 ))

    if [ $file_month -lt 10 ]; then
        file_list="${file_list} ${seas_data_loc}/R1L030100000${file_month}______1"
    else
        file_list="${file_list} ${seas_data_loc}/R1L03010000${file_month}______1"
    fi

done

#:-concatenate files
echo "** - Cat grib files for first 3 month - **"
cat $file_list > $concat_out_file

#:-replace filter templates out directory
sed "s|{{out_dir}}|$split_out_loc|g" $root_dir/seas_cp_lsp_t2m.filter.T > $root_dir/seas_cp_lsp_t2m.filter

#:-split combined grib by grib_filter (requires libeccodes-tools)
echo "** - execute grib filter to split for each ensemble - **"
grib_filter $root_dir/seas_cp_lsp_t2m.filter $concat_out_file

#:-check if files are there
file_prefix="seas.${year}${month}${day}"

for en_no in {00..40}; do 

    file_loc="$split_out_loc/${file_prefix}.en_${en_no}.grib"

    size=$(du -h "$file_loc" | awk '{print $1}')

    if [ -f $file_loc ]; then
        echo "${file_loc}......OK----${size}"
    else 
        echo "${file_loc}......??"

    fi

done
 

#:-delete combined file 
rm $concat_out_file
