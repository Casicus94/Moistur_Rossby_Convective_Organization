import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pdb
from netCDF4 import Dataset
from Casicus import moving_average
import matplotlib.gridspec as gridspec
from pylab import *


#Paths!
scra = '/home/netapp-clima/scratch/acasallas/wrf/Real_run/WRF/'
reals = '/home/tompkins-archive/acasallas/Real1_run/'
user = '/home/netapp-clima/users/acasallas/'
med = '/media/acasallas/ALEJO_HD/Mac_backup/Documents/PhD/Plots/Reals/'
mdir = '/home/tompkins-archive/acasallas/Real1_run/Observations/'

####################################################################
### Read data
tests = ['control','uu','qv_time','vv','vel0','12_apr','20_mar','u_rela']
#tests = ['vel0']
bot = '0'
end = 55

colors = ['k','purple','darkorange','darkcyan','blue',
          'grey','green','magenta']
compos = ['U10','V10','Speed']
alpha = 0.05

for j,compo in enumerate(compos):
    print('########## '+compo+' ##########')
    plt.figure(figsize=(10,9))
    gs = gridspec.GridSpec(3,1, left=0.1, right=0.975, hspace=0.25, wspace=0.05, top=0.9, bottom=0.1)
    for i,test in enumerate(tests):
        print('########## '+test+' ##########')
        ### Wind
        if test == 'Obs':
            if j == 0:
                dsu = xr.open_dataset(mdir+'u_component_of_wind_15-20.nc')
                dsu = dsu.sel(time=slice('2017-03-15','2017-05-15'))
                ucmin = dsu.u.min(dim=['latitude','longitude'])
                ucmax = dsu.u.max(dim=['latitude','longitude'])
                Uc = dsu.u.mean(dim=['latitude','longitude'])
                del(dsu)
            elif j == 1:
                dsv = xr.open_dataset(mdir+'v_component_of_wind_15-20.nc')
                dsv = dsv.sel(time=slice('2017-03-15','2017-05-15'))
                ucmin = dsv.v.min(dim=['latitude','longitude'])
                ucmax = dsv.v.max(dim=['latitude','longitude'])
                Uc = dsv.v.mean(dim=['latitude','longitude'])
                del(dsv)
            elif j == 2:
                dsu = xr.open_dataset(mdir+'u_component_of_wind_15-20.nc')
                dsu = dsu.sel(time=slice('2017-03-15','2017-05-15'))
                dsv = xr.open_dataset(mdir+'v_component_of_wind_15-20.nc')
                dsv = dsv.sel(time=slice('2017-03-15','2017-05-15'))
                Vel = (dsu.u[:,1,:,:]*dsu.u[:,1,:,:] + dsv.v[:,1,:,:]*dsv.v[:,1,:,:])**(0.5) 
                del(dsu)
                del(dsv)
                ucmin = Vel.min(dim=['latitude','longitude'])
                ucmax = Vel.max(dim=['latitude','longitude'])
                Uc = Vel.mean(dim=['latitude','longitude'])
                del(Vel)
        else:
            if j == 0:
                ds3 = xr.open_dataset(reals+test+'/u10_'+test+'.nc')
                Uc = ds3[compo].mean(dim=['south_north','west_east'])
                ucmin = ds3[compo].min(dim=['south_north','west_east'])
                ucmax = ds3[compo].max(dim=['south_north','west_east'])
                del(ds3)
            elif j == 1:
                ds3 = xr.open_dataset(reals+test+'/v10_'+test+'.nc')
                Uc = ds3[compo].mean(dim=['south_north','west_east'])
                ucmin = ds3[compo].min(dim=['south_north','west_east'])
                ucmax = ds3[compo].max(dim=['south_north','west_east'])
                del(ds3)
            elif j == 2:
                ds3 = xr.open_dataset(reals+test+'/u10_'+test+'.nc')
                ds4 = xr.open_dataset(reals+test+'/v10_'+test+'.nc')
                vel = (ds3['U10']*ds3['U10'] + ds4['V10']*ds4['V10'])**(0.5)
                del(ds3)
                del(ds4)
                Uc = vel.mean(dim=['south_north','west_east'])
                ucmin = vel.min(dim=['south_north','west_east'])
                ucmax = vel.max(dim=['south_north','west_east'])
                del(vel)
        ucmin = moving_average(ucmin,12)
        ucmax = moving_average(ucmax,12)
        x = np.linspace(0,55,len(Uc))
        xm = np.linspace(0,55,len(ucmin))
        #pdb.set_trace()
        ### Min
        ax = subplot(gs[0])
        plt.plot(xm,ucmin, label = test, color = colors[i])
        plt.xticks(np.arange(0,55.1,5))
        plt.xlabel('Days')
        plt.axvspan(15,25,color = 'cyan', alpha=alpha)
        plt.axvspan(27,30,color = 'red', alpha=alpha)
        plt.axvspan(37,40,color = 'red', alpha=alpha)
        plt.axvspan(45,46.9,color = 'cyan', alpha=alpha)
        plt.axvspan(47,50,color = 'red', alpha=alpha) 
        plt.ylabel(compo+'-min (m/s)')
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=len(tests))
        ### Mean
        ax = subplot(gs[1])
        plt.plot(x,Uc, label = test, color = colors[i])
        plt.axhline(0.0, color = 'k', linestyle = ':', linewidth = 0.8)
        plt.axvspan(15,25,color = 'cyan', alpha=alpha)
        plt.axvspan(27,30,color = 'red', alpha=alpha)
        plt.axvspan(37,40,color = 'red', alpha=alpha)
        plt.axvspan(45,46.9,color = 'cyan', alpha=alpha)
        plt.axvspan(47,50,color = 'red', alpha=alpha)
        plt.xticks(np.arange(0,55.1,5))
        plt.xlabel('Days')
        plt.ylabel(compo+'-mean (m/s)')
        ### Max
        ax = subplot(gs[2])
        plt.plot(xm,ucmax, label = test, color = colors[i])
        plt.axvspan(15,25,color = 'cyan', alpha=alpha)
        plt.axvspan(27,30,color = 'red', alpha=alpha)
        plt.axvspan(37,40,color = 'red', alpha=alpha)
        plt.axvspan(45,46.9,color = 'cyan', alpha=alpha)
        plt.axvspan(47,50,color = 'red', alpha=alpha)
        plt.xticks(np.arange(0,55.1,5))
        plt.xlabel('Days')
        plt.ylabel(compo+'-max (m/s)')
    plt.savefig(med+'Comparations/'+compo+'_compare.jpg')
    #plt.show()
    plt.close()

### Wind Shear from pre process file!!!
plt.figure(figsize=(10,6))
gs = gridspec.GridSpec(2,1, left=0.1, right=0.975, hspace=0.25, wspace=0.05, top=0.9, bottom=0.1)
print('Shear')
for i,test in enumerate(tests):
    if test == 'Obs':
        dsu = xr.open_dataset(mdir+'u_component_of_wind_15-20.nc')
        dsu = dsu.sel(time=slice('2017-03-15','2017-05-15'))
        dsv = xr.open_dataset(mdir+'v_component_of_wind_15-20.nc')
        dsv = dsv.sel(time=slice('2017-03-15','2017-05-15'))
        du = (dsu.u[:,1,:,:] - dsu.u[:,2,:,:])/2000
        du = du.mean(dim=['latitude','longitude'])
        dv = (dsv.v[:,1,:,:] - dsv.v[:,2,:,:])/2000
        dv = dv.mean(dim=['latitude','longitude'])
        del(dsu)
        del(dsv)
    else:
        du = xr.open_dataset(reals+test+'/shear_u_'+test+'_13-'+bot+'.nc')
        du = du.U
        dv = xr.open_dataset(reals+test+'/shear_v_'+test+'_13-'+bot+'.nc')
        dv = dv.V
    x = np.linspace(0,55,len(du))
    ax = subplot(gs[0])
    plt.plot(x,du, label = test, color = colors[i])
    plt.xticks(np.arange(0,55.1,5))
    plt.axhline(0.0, color = 'k', linestyle = ':', linewidth = 0.8)
    plt.axvspan(15,25,color = 'cyan', alpha=alpha)
    plt.axvspan(27,30,color = 'red', alpha=alpha)
    plt.axvspan(37,40,color = 'red', alpha=alpha)
    plt.axvspan(45,46.9,color = 'cyan', alpha=alpha)
    plt.axvspan(47,50,color = 'red', alpha=alpha)
    plt.xlabel('Days')
    plt.ylabel('Zonal shear (m/s)')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.2), ncol=len(tests))
    ax = subplot(gs[1])
    plt.plot(x,dv, label = test, color = colors[i])
    plt.xticks(np.arange(0,55.1,5))
    plt.axvspan(15,25,color = 'cyan', alpha=alpha)
    plt.axvspan(27,30,color = 'red', alpha=alpha)
    plt.axvspan(37,40,color = 'red', alpha=alpha)
    plt.axvspan(45,46.9,color = 'cyan', alpha=alpha)
    plt.axvspan(47,50,color = 'red', alpha=alpha)
    plt.axhline(0.0, color = 'k', linestyle = ':', linewidth = 0.8)
    plt.xlabel('Days')
    plt.ylabel('Meridional shear (m/s)')
plt.savefig(med+'Comparations/Shear_compare.jpg')
#plt.show()
plt.close()
print('##### Complete #####')
