#!/bin/bash

echo Pre-process real data
for run in JJA ; do
    echo ${run}
    cd /home/netapp-clima/scratch/acasallas/wrf/Real_run/WRF/
    echo Merging files
    #ncrcat test_${run}_file* test_${run}.nc
    if [ -f test_${run}.nc ]; then
        rm -f test_${run}_file*
    fi
    #cp test_${run}.nc /home/tompkins-archive/acasallas/Real1_run/${run}/
    echo Calculating TCWV
    cd /home/tompkins-archive/acasallas/Scripts/
    python3 vert_to_file.py
    #cp /home/netapp-clima/scratch/acasallas/wrf/Real_run/WRF/qv_vert_${run}.nc /home/tompkins-archive/acasallas/Real1_run/${run}/
    echo Calculating shear
    python3 shear_selvar.py
    echo Selecting variables
    echo TSK
    cd /home/netapp-clima/scratch/acasallas/wrf/Real_run/WRF/
    cdo selvar,TSK test_${run}.nc TSK_${run}.nc
    #cp TSK_${run}.nc /home/tompkins-archive/acasallas/Real1_run/${run}/
    echo U10 and V10
    cdo selvar,U10 test_${run}.nc u10_${run}.nc
    cdo selvar,V10 test_${run}.nc v10_${run}.nc
    #cp v10_${run}.nc /home/tompkins-archive/acasallas/Real1_run/${run}/
    #cp u10_${run}.nc /home/tompkins-archive/acasallas/Real1_run/${run}/
    echo HML
    cdo selvar,HML test_${run}.nc HML_${run}.nc
    cdo fldmean HML_${run}.nc HML_${run}_fldmean.nc
    if [ -f HML_${run}_fldmean.nc ]; then
        rm -f HML_${run}.nc
    fi
    cp HML_${run}_fldmean.nc /home/tompkins-archive/acasallas/Real1_run/${run}/
    echo U and V
    #cdo selvar,U test_${run}.nc u_${run}.nc
    #cdo selvar,V test_${run}.nc v_${run}.nc
    cdo -L -fldmean -selvar,U test_${run}.nc zonal_${run}_fldmean.nc
    cdo -L -fldmean -selvar,V test_${run}.nc meridional_${run}_fldmean.nc
    #cp meridional_${run}_fldmean.nc /home/tompkins-archive/acasallas/Real1_run/${run}/
    #cp zonal_${run}_fldmean.nc /home/tompkins-archive/acasallas/Real1_run/${run}/
    echo Calculating fluxes and precipitation
    cd /home/tompkins-archive/acasallas/Scripts/
    bash PP_real.sh
    cd /home/netapp-clima/scratch/acasallas/wrf/Real_run/WRF/
    echo Calculating fldmean
    cdo fldmean allfld_test_${run}_flux_d3600.nc all_fldmean_${run}.nc
    #cp allfld_test_${run}_flux_d3600.nc /home/tompkins-archive/acasallas/Real1_run/${run}/
    #cp all_fldmean_${run}.nc /home/tompkins-archive/acasallas/Real1_run/${run}/
    echo Calculation cloud fraction real 
    cd /home/tompkins-archive/acasallas/Scripts/
    bash cloud_cover_real.sh
    echo Completed
done
