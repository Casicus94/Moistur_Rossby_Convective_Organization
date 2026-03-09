#!/bin/bash

echo Calculating cloud fraction
for run in JJA ; do
    echo ${run}
    cd /home/netapp-clima/scratch/acasallas/wrf/Real_run/WRF/
    cdo -L -gec,1.e-5 -add -selvar,QICE test_${run}.nc -add -selvar,QSNOW test_${run}.nc -selvar,QCLOUD test_${run}.nc cloud.nc
    cdo vertsum cloud.nc cloud_versum.nc
    rm -f cloud.nc
    cdo gec,1 cloud_versum.nc cloud_mask.nc
    rm -f cloud_versum.nc
    cdo fldsum cloud_mask.nc cloud_fldmean.nc
    rm -f cloud_mask.nc
    cdo divc,220248 cloud_fldmean.nc cloud_${run}.nc
    rm -f cloud_fldmean.nc 
    cp cloud_${run}.nc /home/tompkins-archive/acasallas/Real1_run/${run}/ 
done

