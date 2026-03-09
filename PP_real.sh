#!/lin/bash

#Modify run and the last line

for run in test_JJA ; do
    echo ${run}
    cd /home/netapp-clima/scratch/acasallas/wrf/Real_run/WRF/
    file=${run}.nc
    echo $file
    nstep=`cdo -s ntime $file`
    echo $nstep
    timediff=3600
    for var in ACLHF ACHFX RAINNC ; do
        cdo selvar,$var $file tmp_${var}_AC1.nc
        cdo -r divc,$timediff tmp_${var}_AC1.nc tmp_${var}_AC.nc
        rm -f tmp_${var}_AC1.nc
        cdo -L sub -seltimestep,2/$nstep tmp_${var}_AC.nc -seltimestep,1/`expr $nstep - 1` tmp_${var}_AC.nc tmp_${var}1.nc 
        cdo seltimestep,1 tmp_${var}_AC.nc tmp_1.nc
        cdo -mergetime tmp_1.nc tmp_${var}1.nc fld_${run}_${var}_d${timediff}_file.nc
        rm -f tmp_1.nc
    done

    for fld in ACLW ACSW ; do # TYPE
    	for clr in "" C ; do # C=clear sky ""=all sky
    	for dir in DN UP ; do  # DIRECTION
    	for bdy in B T ; do # TOA, SURF
            # deaccumulate var
            if [ "$fld" = "LW" ] || [ "$fld" = "SW" ]; then 
                var=${fld}${dir}${bdy}${clr}
                echo $var
                ofile=fld_${run}_${var}_d${timediff}_file.nc
                cdo selvar,$var $file $ofile
            else
                var=${fld}${dir}${bdy}${clr}
                echo $var
                ofile=fld_${run}_${var}_d${timediff}_file.nc
                cdo selvar,$var $file tmp_${var}_AC1.nc
                cdo -r divc,$timediff tmp_${var}_AC1.nc tmp_${var}_AC.nc
                rm -f tmp_${var}_AC1.nc
                cdo -L sub -seltimestep,2/$nstep tmp_${var}_AC.nc -seltimestep,1/`expr $nstep - 1` tmp_${var}_AC.nc tmp_${var}1.nc
                cdo seltimestep,1 tmp_${var}_AC.nc tmp_1.nc
                cdo -mergetime tmp_1.nc tmp_${var}1.nc $ofile
                rm -f tmp_1.nc
            fi 
    	done
    	done

	mlist=fld_${run}_*${fld}*_d${timediff}_file.nc
	rm -f tmp_merge.nc tmp_?.nc
	cdo merge $mlist tmp_merge.nc
	var=${fld}TBNET${clr}
        if [ "$fld" = "LW" ] || [ "$fld" = "SW" ]; then
	    cdo expr,"${var}=${fld}UPB${clr}-${fld}UPT${clr}+${fld}DNT${clr}-${fld}DNB${clr}" tmp_merge.nc fld_${run}_${var}_d${timediff}_file.nc
	    var=${fld}BNET${clr}
	    cdo expr,"${var}=${fld}UPB${clr}-${fld}DNB${clr}" tmp_merge.nc fld_${run}_${var}_d${timediff}_file.nc
	    var=${fld}TNET${clr}
	    cdo expr,"${var}=-${fld}UPT${clr}" tmp_merge.nc fld_${run}_${var}_d${timediff}_file.nc
        else
            cdo expr,"${var}=${fld}UPB${clr}-${fld}UPT${clr}+${fld}DNT${clr}-${fld}DNB${clr}" tmp_merge.nc fld_${run}_${var}_d${timediff}_file.nc
            var=${fld}BNET${clr}
            cdo expr,"${var}=${fld}UPB${clr}-${fld}DNB${clr}" tmp_merge.nc fld_${run}_${var}_d${timediff}_file.nc
            var=${fld}TNET${clr}
            cdo expr,"${var}=${fld}DNT${clr}-${fld}UPT${clr}" tmp_merge.nc fld_${run}_${var}_d${timediff}_file.nc
        fi
	#ncatted -O -a units,${fld},a,
	done # clr / all sky
    rm -f tmp_*
    done # radn field
    cdo merge fld_${run}_*.nc allfld_${run}_flux_d3600.nc
    rm -f fld_${run}_*.nc
    #cp allfld_${run}_flux_d3600.nc /home/tompkins-archive/acasallas/Real1_run/HML/
done

