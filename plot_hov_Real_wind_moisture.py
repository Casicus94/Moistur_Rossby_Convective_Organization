import xarray as xr
from netCDF4 import Dataset
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import matplotlib.gridspec as gridspec
from pylab import *
from scipy import stats
from Casicus import hov_wrf

med = '/media/acasallas/ALEJO_HD/Mac_backup/Documents/PhD/Plots/Reals/'
reals = '/home/tompkins-archive/acasallas/Real1_run/'
scra = '/home/netapp-clima/scratch/acasallas/wrf/Real_run/WRF/'
obdr = '/home/tompkins-archive2/acasallas/Real1_run/'

###### Dates 
dates_MAM = [d.strftime('%Y-%m-%d') for d in pd.date_range('2017-03-15 00:00:00','2017-05-13 23:00:00', freq='3d')]
tval_MAM = pd.date_range('2017-03-15 00:00:00','2017-05-13 23:00:00', freq='1H')

########### WRF model
### MAM
sst_ds_MAM = xr.open_dataset(reals+'control/TSK_control.nc')
tcwv_ds_MAM = xr.open_dataset(reals+'control/qv_vert_control.nc')
sst_wrf_MAM, tcwv_wrf_MAM, hovx_wrf, ntime_wrf_MAM = hov_wrf(sst_ds_MAM, tcwv_ds_MAM)
data = pd.DataFrame(sst_wrf_MAM[0])
data.to_csv('/home/tompkins-archive/acasallas/Data_to_plot/Slope_control.csv')

tipo = '12apr' #20mar or 12apr

### Moisture
sst_ds_qv = xr.open_dataset(reals+'qv_'+tipo+'/TSK_qv_'+tipo+'.nc')
tcwv_ds_qv = xr.open_dataset(reals+'qv_'+tipo+'/qv_vert_qv_'+tipo+'.nc')
sst_wrf_qv, tcwv_wrf_qv, hovx_wrf, ntime_wrf_qv = hov_wrf(sst_ds_qv, tcwv_ds_qv)
data = pd.DataFrame(sst_wrf_qv[0])
data.to_csv('/home/tompkins-archive/acasallas/Data_to_plot/Slope_qv_'+tipo+'.csv')

### Wind
sst_ds_uv = xr.open_dataset(reals+'uv_'+tipo+'/TSK_uv_'+tipo+'.nc')
tcwv_ds_uv = xr.open_dataset(reals+'uv_'+tipo+'/qv_vert_uv_'+tipo+'.nc')
sst_wrf_uv, tcwv_wrf_uv, hovx_wrf, ntime_wrf_uv = hov_wrf(sst_ds_uv, tcwv_ds_uv)
data = pd.DataFrame(sst_wrf_uv[0])
data.to_csv('/home/tompkins-archive/acasallas/Data_to_plot/Slope_uv_'+tipo+'.csv')

### Components
# U
if tipo == '20mar':
    path = obdr
else:
    path = reals
sst_ds_u = xr.open_dataset(path+'u_'+tipo+'/TSK_u_'+tipo+'.nc')
tcwv_ds_u = xr.open_dataset(path+'u_'+tipo+'/qv_vert_u_'+tipo+'.nc')
sst_wrf_u, tcwv_wrf_u, hovx_wrf, ntime_wrf_u = hov_wrf(sst_ds_u, tcwv_ds_u)
data = pd.DataFrame(sst_wrf_u[0])
data.to_csv('/home/tompkins-archive/acasallas/Data_to_plot/Slope_u_'+tipo+'.csv')

# V
sst_ds_v = xr.open_dataset(path+'v_'+tipo+'/TSK_v_'+tipo+'.nc')
tcwv_ds_v = xr.open_dataset(path+'v_'+tipo+'/qv_vert_v_'+tipo+'.nc')
sst_wrf_v, tcwv_wrf_v, hovx_wrf, ntime_wrf_v = hov_wrf(sst_ds_v, tcwv_ds_v)
data = pd.DataFrame(sst_wrf_v[0])
data.to_csv('/home/tompkins-archive/acasallas/Data_to_plot/Slope_v_'+tipo+'.csv')

levs = np.arange(-0.3, 0.31, 0.05)
plots = [sst_wrf_MAM, sst_wrf_qv, sst_wrf_uv, sst_wrf_u, sst_wrf_v]
titles = ['(a)','(b)','(c)','(d)','(e)']
########### Plotting
fig = plt.figure(figsize=(12,8))
gs = GridSpec(2,5,left = 0.1, right = 0.96, hspace=0.15, wspace=0.15, top = 0.9, bottom = 0.08, height_ratios = [0.05,1], width_ratios = [1,1,1,1,1])
for i,plot in enumerate(plots):
    ax = plt.subplot(gs[1,i])
    im = plt.contourf(hovx_wrf,tval_MAM,plot[0,:len(tval_MAM),:], cmap = 'bwr', levels = levs, extend = 'both')
    ax.set_yticks(dates_MAM)
    ax.set_yticklabels(dates_MAM)
    plt.xticks(np.arange(0,100.1,20))
    plt.title(titles[i], loc = 'left')
    plt.xlabel('TCWV %-tile')
    if i > 0:
        plt.setp(ax.get_yticklabels(), visible=False)
ax = plt.subplot(gs[0,0:5])
cbar = plt.colorbar(im, cax = ax, orientation = 'horizontal', shrink = 0.2, ticks = levs)
cbar.ax.set_title('SST anomaly (K)')
cbar.ax.xaxis.set_ticks_position("top")
plt.savefig(med+'Hov_moist_wind_components_'+tipo+'.jpg', bbox_inches = 'tight', dpi = 300)
plt.savefig(med+'Hov_moist_wind_components_'+tipo+'.pdf', bbox_inches = 'tight', dpi = 300)
 
