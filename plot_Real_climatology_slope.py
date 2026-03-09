import xarray as xr
from netCDF4 import Dataset
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import matplotlib.gridspec as gridspec
from pylab import *
from scipy import stats
import Casicus as casi

def hovmuller(date_ini,date_end):
    sst_ds = xr.open_dataset(dir_era+'SST_area.nc')
    tcwv_ds = xr.open_dataset(dir_era+'TCWV_area.nc')
    sst_ds = sst_ds.sel(time=slice(date_ini,date_end))
    tcwv_ds = tcwv_ds.sel(time=slice(date_ini,date_end))
    time1 = 0*24
    time2 = len(sst_ds.sst) - 1
    ntime=time2-time1+1 # 240 quick hack should be read from the netcdf file really...
    yticki= 5.0
    qv_press=1100. # low press qv integration hPA
    dtime=3600 #This depends on the ouput frequency
    difftime=str(dtime)
    fstr=difftime+'-'+str(time1)+'-'+str(time2)

    #Domain and splits
    nx=57
    ny=81

    npts=nx*ny
    hovchunk=81  #1024 # averaging length for chunking, power of 2, larger=smoother.
    nhov=int(npts/hovchunk)
    hovx=100*(np.arange(nhov)+0.5)/nhov

    #Start matrixes 
    times=np.array(range(ntime)) # start from day 1 for spin up
    #slices=times+time1
    hovtimes=(times+time1)*dtime/86400.
    sst_hov=np.zeros([1,ntime,nhov])
    tcwv_hov=np.zeros([1,ntime,nhov])

    for itime in times:
        itime1 = itime+time1
        print("slice ",itime1)
        tcwv = np.array(tcwv_ds.variables['tcwv'][itime,:,:])
        sst =  np.array(sst_ds.variables["sst"][itime,:,:])
        print("min max tcwv ",np.min(tcwv),np.max(tcwv))
        # sort the tcwv
        isort=np.argsort(tcwv.flatten()) # sort tcwv
        sstpert=sst.flatten()-np.mean(sst)
        sst_hov[0,itime,:]=np.mean(sstpert[isort].reshape(-1,hovchunk),axis=1)
        tcwv_hov[0,itime,:]=np.mean(tcwv.flatten()[isort].reshape(-1,hovchunk),axis=1)
    return(sst_hov, tcwv_hov, hovx, hovtimes)

#Directories
#dir_era = '/home/netapp-clima/users/acasallas/ERA5_real/Area_2-9_135-145/'
dir_era = '/home/tompkins-archive2/acasallas/ERA5_real/Area_2-9_135-145/'
dir_pcs = '/home/netapp-clima/users/acasallas/ERA5_real/REOFs/'
mdir = '/home/tompkins-archive/acasallas/'
med = '/media/acasallas/ALEJO_HD/Mac_backup/Documents/PhD/Plots/Reals/'
scra = '/home/netapp-clima/scratch/acasallas/'

###First we need to preprocess

print('Starting Hovmuller script!')
sst_hov_MAM, tcwv_hov_MAM, hovx, hovtimes = hovmuller('2017-03-15 00:00:00','2017-05-15 23:00:00')
sst_hov_JJA, tcwv_hov_JJA, hovx, hovtimes = hovmuller('2017-06-15 00:00:00','2017-08-15 23:00:00')

sst_av_MAM = np.mean(sst_hov_MAM,axis=1); tcwv_av_MAM = np.mean(tcwv_hov_MAM,axis=1)
sst_av_JJA = np.mean(sst_hov_JJA,axis=1); tcwv_av_JJA = np.mean(tcwv_hov_JJA,axis=1)

mon_org = [65, 61, 79, 64, 51, 13, 13, 12, 14, 17, 42, 63] 
mon_rev = [22, 15, 8, 22, 18, 6, 24, 32, 26, 25, 14, 5]

print('Slopes')
slopes = pd.read_csv(dir_era+'Slopes_data_2-9_135-145_ERA5.csv', parse_dates = True, index_col = 0)

slope_MAM = slopes.loc['2017-03-15 00:00:00':'2017-05-15 23:00:00']
slope_JJA = slopes.loc['2017-06-15 00:00:00':'2017-08-15 23:00:00']

dates_MAM = [d.strftime('%Y-%m-%d') for d in pd.date_range('2017-03-15 00:00:00','2017-05-15 23:00:00', freq='3d')]
dates_JJA = [d.strftime('%Y-%m-%d') for d in pd.date_range('2017-06-15 00:00:00','2017-08-15 23:00:00', freq='3d')]
tval_MAM = pd.date_range('2017-03-15 00:00:00','2017-05-15 23:00:00', freq='1H')
tval_JJA = pd.date_range('2017-06-15 00:00:00','2017-08-15 23:00:00', freq='1H')

########################### Plotting
fig = plt.figure(figsize=(10,15)) 
gs = GridSpec(5,5,left = 0.12, right = 0.98, hspace=0.35, wspace=0.15, top = 0.95, bottom = 0.05, height_ratios = [0.1,1,1,0.5,0.5], width_ratios = [1,0.5,0.4,1,0.5])
ax = plt.subplot(gs[1:3,0])
im = plt.contourf(hovx,tval_MAM,sst_hov_MAM[0,:,:], cmap = 'bwr', levels = np.arange(-0.4,0.41,0.1), extend = 'both')
ax.set_yticks(dates_MAM)
ax.set_yticklabels(dates_MAM)
plt.xticks(np.arange(0,100.1,20))
plt.title('(a)', loc = 'left')
plt.xlabel('TCWV %-tile')

ax = plt.subplot(gs[1:3,1])
plt.plot(slope_MAM['Slope']*1000, tval_MAM, color = 'darkcyan', label = 'Slope')
plt.fill_between(np.arange(-10,12.1), tval_MAM[-820], tval_MAM[-770], alpha = 0.25, color = 'purple')
plt.fill_between(np.arange(-10,12.1), tval_MAM[-560], tval_MAM[-400], alpha = 0.25, color = 'purple')
plt.fill_between(np.arange(-10,12.1), tval_MAM[-1350], tval_MAM[-1410], alpha = 0.25, color = 'purple')
plt.fill_between(np.arange(-10,12.1), tval_MAM[-740], tval_MAM[-600], alpha = 0.25, color = 'blue')
plt.fill_between(np.arange(-10,12.1), tval_MAM[-1010], tval_MAM[-880], alpha = 0.25, color = 'blue')
plt.fill_between(np.arange(-10,12.1), tval_MAM[-1330], tval_MAM[-1250], alpha = 0.25, color = 'blue')

ax.set_yticks(dates_MAM)
ax.set_yticklabels(dates_MAM)
plt.setp(ax.get_yticklabels(), visible=False)
plt.ylim(tval_MAM[0],tval_MAM[-1])
plt.title('(b)', loc = 'left')
plt.xlim(-10,12)
plt.xticks([-5,0,5,10])
plt.xlabel('Slope (10$^{-3}$)')

ax = plt.subplot(gs[3,0:2])
plt.plot(hovx, sst_av_MAM[0], color = 'darkred', label = 'MAM')
plt.yticks(np.arange(-0.3,0.31,0.1))
plt.axhline(0, linestyle = ':', color = 'k')
plt.title('(c)', loc = 'left')
plt.xticks(np.arange(0,100.1,20))
plt.xlim(0,100)
plt.ylabel('SST Anomaly (K)')
plt.xlabel('TCWV %-tile')

ax = plt.subplot(gs[1:3,3])
im = plt.contourf(hovx,tval_JJA,sst_hov_JJA[0,:,:], cmap = 'bwr', levels = np.arange(-0.4,0.41,0.1), extend = 'both')
ax.set_yticks(dates_JJA)
ax.set_yticklabels(dates_JJA)
plt.xticks(np.arange(0,100.1,20))
plt.title('(d)', loc = 'left')
plt.xlabel('TCWV %-tile')

ax = plt.subplot(gs[1:3,4])
plt.plot(slope_JJA['Slope']*1000, tval_JJA, color = 'darkcyan', label = 'Slope')
#plt.fill_between(np.arange(-10,12.1), tval_JJA[-130], tval_JJA[-100], alpha = 0.25, color = 'purple')
#plt.fill_between(np.arange(-10,12.1), tval_JJA[-500], tval_JJA[-450], alpha = 0.25, color = 'blue')
ax.set_yticks(dates_JJA)
ax.set_yticklabels(dates_JJA)
plt.setp(ax.get_yticklabels(), visible=False)
plt.ylim(tval_JJA[0],tval_JJA[-1])
plt.title('(e)', loc = 'left')
plt.xlim(-10,12)
plt.xticks([-5,0,5,10])
plt.xlabel('Slope (10$^{-3}$)')

ax = plt.subplot(gs[3,3:5])
plt.plot(hovx, sst_av_JJA[0], color = 'darkred', label = 'JJA')
plt.yticks(np.arange(-0.3,0.31,0.1))
plt.axhline(0, linestyle = ':', color = 'k')
plt.title('(f)', loc = 'left')
plt.xticks(np.arange(0,100.1,20))
plt.xlim(0,100)
plt.ylabel('SST Anomaly (K)')
plt.xlabel('TCWV %-tile')

ax = plt.subplot(gs[0,0:5])
cbar = plt.colorbar(im, cax = ax, orientation = 'horizontal', shrink = 0.6)
cbar.ax.set_title('SST anomaly (K)')
cbar.ax.xaxis.set_ticks_position("top")

width = 0.25
ax = plt.subplot(gs[4,0:5])
plt.bar(np.arange(1,13)-width/2, np.array(mon_rev)/4, edgecolor = 'k', color = 'darkorchid', label = 'Reversals', width = width)
plt.bar(np.arange(1,13)+width/2, np.array(mon_org)/4, edgecolor = 'k', color = 'blue', label = 'Organized', width = width)
plt.legend(loc = 'upper center', ncol = 2, frameon = False)
plt.xticks(np.arange(1,13))
plt.ylabel('Number of events')
plt.xlabel('Months')
plt.title('(g)', loc = 'left', fontsize = 12)
plt.savefig(mdir+'Hov_SST_Slope_clim.jpg', bbox_inches = 'tight', dpi = 300)
plt.savefig(mdir+'Hov_SST_Slope_clim.pdf', bbox_inches = 'tight', dpi = 300)
#plt.show()
