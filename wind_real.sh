#!/bin/bash

echo Extracting wind 
for run in vel_rela ; do
    echo ${run}
    cd /home/tompkins-archive/acasallas/Real1_run/${run}/
    echo Zonal
    cdo -L -fldmean -selvar,U test_${run}.nc zonal_${run}_fldmean.nc
    echo Meridional
    cdo -L -fldmean -selvar,V test_${run}.nc meridional_${run}_fldmean.nc
done
