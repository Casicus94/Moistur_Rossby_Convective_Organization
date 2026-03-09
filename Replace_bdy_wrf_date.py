import xarray as xr
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pdb
import os

#Directories
wps = '/home/netapp-clima/scratch/acasallas/wrf/Real_run/WPS/'
wrf = '/home/netapp-clima/scratch/acasallas/wrf/Real_run/WRF/'
mdir = '/home/tompkins-archive/acasallas/WPS_modified/'

#First, lets select the boundaries that we want
filename = 'met_em.d01.2017-03-20_18:00:00.nc' #met_em.d01.2017-03-20_18:00:00.nc met_em.d01.2017-04-12_00:00:00.nc
#filename
print('Reading file '+filename)
ds = xr.open_dataset(wps+filename)
#Here the conditions we want!
RH = ds.RH
TT = ds.TT
UU = ds.UU
VV = ds.VV
repla = [UU]
del(ds)

# Now what variables are we replacing?
varis = ['UU']
no_shear = False

###Input dates to change
init_year = '2017'
init_mon = '03'
init_day = '15'

end_year   = '2017'
end_mon   = '05'
end_day   = '15'

#Hours!
times = ['00','06','12','18']
ls = 0
lf = 13

#Create a list of dates
dates = [d.strftime('%Y-%m-%d') for d in pd.date_range(init_year+init_mon+init_day,end_year+end_mon+end_day, freq='1D')]

for date in dates:
    for t in times:
        #Read data
        filename = 'met_em.d01.'+date[0:4]+'-'+date[5:7]+'-'+date[8:11]+'_'+t+':00:00.nc'
        print('Reading file '+filename)
        ds = xr.open_dataset(wps+filename)
        #First calculate the mean for every level
        for v,var in enumerate(varis):
            print('Starting '+var)
            print('Replacing values!!')
            if no_shear == False:
                ds[var][0,:,:,:] = repla[v][0,:,:,:] 
            elif no_shear == True:
                ds[var][0,ls:lf,:,:] = repla[v][0,ls,:,:]    
        print('Replacing finish')   
        ds.to_netcdf(mdir+filename)
        del(ds)
print('##### Complete #####')

