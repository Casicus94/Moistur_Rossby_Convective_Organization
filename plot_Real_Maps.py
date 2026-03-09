import xarray as xr
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
from cartopy.feature import ShapelyFeature
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LinearSegmentedColormap
import pdb
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
from pylab import *
import pandas as pd
import datetime as dt
import os

#### Make the three plots we need! 
# Paths
mdir = '/home/tompkins-archive/acasallas/'
mdir1 = '/home/tompkins-archive2/acasallas/'
user = '/home/tompkins-archive2/acasallas/ERA5_real/'
med = '/media/acasallas/ALEJO_HD/Mac_backup/Documents/PhD/Plots/Reals/'
scr = '/home/netapp-clima/scratch/acasallas/'

### Dates
org_date = '2017-03-21 12:00:00' 
rev_date = '2017-04-12 16:00:00'

### Figure ERA5
print('----------> First ERA5')
ds_sst = xr.open_dataset(user+'Area_2-9_135-145/SST_area.nc') 
ds_tcwv = xr.open_dataset(user+'Area_2-9_135-145/TCWV_area.nc')
ds_u = xr.open_dataset(user+'Area_2-9_135-145/Zonal_850_area.nc')
ds_v = xr.open_dataset(user+'Area_2-9_135-145/Meridional_850_area.nc')

# SST
print('Reading SST')
sst_MAM = ds_sst.sst.loc['2017-03-15 00:00:00':'2017-05-15 23:00:00']
sst_rev = ds_sst.sst.loc[rev_date]
sst_org = ds_sst.sst.loc[org_date] 
sst_JJA = ds_sst.sst.loc['2017-06-15 00:00:00':'2017-08-15 23:00:00']
# TCWV
print('Reading TCWV')
tcw_MAM = ds_tcwv.tcwv.loc['2017-03-15 00:00:00':'2017-05-15 23:00:00']
tcw_rev = ds_tcwv.tcwv.loc[rev_date]
tcw_org = ds_tcwv.tcwv.loc[org_date] 
tcw_JJA = ds_tcwv.tcwv.loc['2017-06-15 00:00:00':'2017-08-15 23:00:00']
# Zonal wind
print('Reading Zonal')
u_MAM = ds_u.u.loc['2017-03-15 00:00:00':'2017-05-15 23:00:00']
u_rev = ds_u.u.loc[rev_date]
u_org = ds_u.u.loc[org_date] 
u_JJA = ds_u.u.loc['2017-06-15 00:00:00':'2017-08-15 23:00:00']
#Meridional wind
print('Reading Meridional')
v_MAM = ds_v.v.loc['2017-03-15 00:00:00':'2017-05-15 23:00:00']
v_rev = ds_v.v.loc[rev_date]
v_org = ds_v.v.loc[org_date] 
v_JJA = ds_v.v.loc['2017-06-15 00:00:00':'2017-08-15 23:00:00']

ssts = [sst_MAM.mean(dim=['time']), sst_JJA.mean(dim=['time']), sst_org, sst_rev]
tcwvs = [tcw_MAM.mean(dim=['time']), tcw_JJA.mean(dim=['time']), tcw_org, tcw_rev]
us = [u_MAM.mean(dim=['time']), u_JJA.mean(dim=['time']), u_org, u_rev]
vs = [v_MAM.mean(dim=['time']), v_JJA.mean(dim=['time']), v_org, v_rev]
titles = ['(a)','(b)','(c)','(d)']
jum1 = 6

fig = plt.figure(figsize=(9,6))
gs = GridSpec(2,4, left = 0.09, right = 0.9, hspace=0.05, wspace=0.1, top = 0.95, bottom = 0.08, width_ratios = [1,1,0.15,0.1])
for i,sst in enumerate(ssts):
    if i < 2:
        ax = plt.subplot(gs[i],projection= ccrs.PlateCarree(central_longitude=180))
    else:
        ax = plt.subplot(gs[i+2],projection= ccrs.PlateCarree(central_longitude=180))
    # TCWV
    im = plt.contourf(ds_tcwv['longitude'],ds_tcwv['latitude'], tcwvs[i], cmap='BrBG', transform = ccrs.PlateCarree(), extend = 'both', levels=np.arange(30,71,2.5))
    # SST
    im1 = plt.contour(ds_sst['longitude'],ds_sst['latitude'], sst, cmap='hot_r', transform = ccrs.PlateCarree(), extend = 'both', linewidths = 0.7, levels = np.arange(301,303.51,0.25))
    ax.add_feature(cfeature.COASTLINE)
    ax.set_extent([135, 145, 2, 9], crs=ccrs.PlateCarree()) 
    plt.clabel(im1, fontsize=8, inline=1, fmt = '%4.2f', levels = np.arange(301,303.51,0.25))
    # Wind
    im2 = plt.quiver(ds_u['longitude'][::jum1],ds_u['latitude'][::jum1],np.array(us[i][0,::jum1,::jum1]),  np.array(vs[i][0,::jum1,::jum1]), transform = ccrs.PlateCarree(), edgecolor='k', linewidth = 0.8, units='xy',  headlength = 4, headwidth = 2.5, scale = 15, color = 'k')
    if i == 1:
        ax.quiverkey(im2,0.7,-0.1,10,'10 m s$^{-1}$', labelpos='E', fontproperties={'size':12})
    gl = ax.gridlines(crs = ccrs.PlateCarree(), draw_labels = True, linewidth = 1, color='k', alpha = 0.5, linestyle = '--')
    gl.xlocator = mticker.FixedLocator([137.5, 140, 142.5]) 
    gl.ylocator = mticker.FixedLocator([3.75, 5.5, 7.25])
    if i == 0:
        gl.xlabels_bottom = False; gl.ylabels_right = False
    elif i == 1:
        gl.xlabels_bottom = False; gl.ylabels_left = False 
    elif i == 2:
        gl.xlabels_top = False; gl.ylabels_right = False
    elif i == 3:
        gl.xlabels_top = False; gl.ylabels_left = False
    plt.title(titles[i], loc = 'left')

ax = plt.subplot(gs[:,3])
cbar = plt.colorbar(im,cax=ax,shrink = 0.4, ticks=np.arange(30,71,5))
cbar.set_label('TCWV (mm)')
plt.savefig(scr+'ERA5_maps_MAM_JJA_Rev_Org.jpg', bbox_inches = 'tight', dpi = 300)
plt.savefig(scr+'ERA5_maps_MAM_JJA_Rev_Org.pdf', bbox_inches = 'tight', dpi = 300)
#plt.show()
plt.close() 

#### Figure WRF General
print('----------> Second WRF, control and JJA')
data = {}
varis = ['TSK','QVAPOR','U','V']
nam = ['TSK','qv_vert','Zonal_850','Meridional_850']
times = ['XTIME','time','XTIME','XTIME']
tipos = ['control', 'JJA']
org_date = '2017-03-21 12:00:00'
rev_date = '2017-04-12 23:00:00'
dato = '_mean' #_mean 
for tipo in tipos:
    for i,var in enumerate(varis):
        if tipo == 'JJA':
            tmp = xr.open_dataset(mdir1+'Real1_run/'+tipo+'/'+nam[i]+'_'+tipo+'.nc')
        else:
            tmp = xr.open_dataset(mdir+'Real1_run/'+tipo+'/'+nam[i]+'_'+tipo+'.nc')
        if dato == '':
            data[var+'_'+tipo] = tmp[var].mean(dim=times[i])
            if tipo == 'JJA':
                data[var+'_'+tipo].to_netcdf(mdir1+'Real1_run/'+tipo+'/'+nam[i]+'_'+tipo+'_mean.nc')
            else:
                data[var+'_'+tipo].to_netcdf(mdir+'Real1_run/'+tipo+'/'+nam[i]+'_'+tipo+'_mean.nc')
        else:
            if tipo == 'JJA':
                tmp1 = xr.open_dataset(mdir1+'Real1_run/'+tipo+'/'+nam[i]+'_'+tipo+dato+'.nc')
            else:
                tmp1 = xr.open_dataset(mdir+'Real1_run/'+tipo+'/'+nam[i]+'_'+tipo+dato+'.nc')
            data[var+'_'+tipo] = tmp1[var]
        if tipo == 'control':
            data[var+'_'+tipo+'_rev'] = tmp[var].loc[rev_date][:,:]
            data[var+'_'+tipo+'_org'] = tmp[var].loc[org_date][:,:]

print('Calculating means and creating list')
### Lists to plot
print('SST')
var = 'TSK'
ssts = [data[var+'_control'],data[var+'_JJA'],data[var+'_control_org'],data[var+'_control_rev']]
print('TCWV')
var = 'QVAPOR'
tcwvs = [data[var+'_control'],data[var+'_JJA'],data[var+'_control_org'],data[var+'_control_rev']]
print('U')
var = 'U'
us = [data[var+'_control'],data[var+'_JJA'],data[var+'_control_org'],data[var+'_control_rev']]
print('V')
var = 'V'
vs = [data[var+'_control'],data[var+'_JJA'],data[var+'_control_org'],data[var+'_control_rev']]

### Plotting
jum1 = 42
fig = plt.figure(figsize=(9,6))
gs = GridSpec(2,4, left = 0.09, right = 0.9, hspace=0.05, wspace=0.1, top = 0.95, bottom = 0.08, width_ratios = [1,1,0.15,0.1])
for i,sst in enumerate(ssts):
    if i < 2:
        ax = plt.subplot(gs[i],projection= ccrs.PlateCarree(central_longitude=180))
    else:
        ax = plt.subplot(gs[i+2],projection= ccrs.PlateCarree(central_longitude=180))
    # TCWV
    im = plt.contourf(sst['XLONG'],sst['XLAT'], tcwvs[i][0,:,:], cmap='BrBG', transform = ccrs.PlateCarree(), extend = 'both', levels=np.arange(30,71,2.5))
    # SST
    im1 = plt.contour(sst['XLONG'],sst['XLAT'], sst, cmap='hot_r', transform = ccrs.PlateCarree(), extend = 'both', linewidths = 0.7, levels = np.arange(301,303.51,0.5))
    ax.add_feature(cfeature.COASTLINE)
    ax.set_extent([135, 145, 2.05, 9], crs=ccrs.PlateCarree())
    plt.clabel(im1, fontsize=8, inline=1, fmt = '%4.2f', levels = np.arange(301,303.51,0.5))
    # Wind
    im2 = plt.quiver(us[i]['XLONG_U'][0,::jum1],us[i]['XLAT_U'][::jum1,0],np.array(us[i][0,::jum1,::jum1]),  np.array(vs[i][0,::jum1,::jum1]), transform = ccrs.PlateCarree(), edgecolor='k', linewidth = 0.8, units='xy',  headlength = 4, headwidth = 2.5, scale = 15, color = 'k')
    if i == 1:
        ax.quiverkey(im2,0.7,-0.1,10,'10 m s$^{-1}$', labelpos='E', fontproperties={'size':12})
    gl = ax.gridlines(crs = ccrs.PlateCarree(), draw_labels = True, linewidth = 1, color='k', alpha = 0.5, linestyle = '--')
    gl.xlocator = mticker.FixedLocator([137.5, 140, 142.5])
    gl.ylocator = mticker.FixedLocator([3.75, 5.5, 7.25])
    if i == 0:
        gl.xlabels_bottom = False; gl.ylabels_right = False
    elif i == 1:
        gl.xlabels_bottom = False; gl.ylabels_left = False
    elif i == 2:
        gl.xlabels_top = False; gl.ylabels_right = False
    elif i == 3:
        gl.xlabels_top = False; gl.ylabels_left = False
    plt.title(titles[i], loc = 'left')

ax = plt.subplot(gs[:,3])
cbar = plt.colorbar(im,cax=ax,shrink = 0.4, ticks=np.arange(30,71,5))
cbar.set_label('TCWV (mm)')
plt.savefig(scr+'WRF_maps_MAM_JJA_Rev_Org.jpg', bbox_inches = 'tight', dpi = 300)
plt.savefig(scr+'WRF_maps_MAM_JJA_Rev_Org.pdf', bbox_inches = 'tight', dpi = 300)
#plt.show()
plt.close()

##### Figure for the experiments!
print('----------> Third WRF, experiments')
data = {}
varis = ['TSK','QVAPOR','U','V']
nam = ['TSK','qv_vert','Zonal_850','Meridional_850']
times = ['XTIME','time','XTIME','XTIME']
tipos = ['qv_12apr', 'qv_20mar', 'uv_20mar', 'u_12apr', 'u_20mar', 'v_12apr', 'v_20mar', '12_apr', '20_mar', 'uv_12apr']
dato = '' #_mean 
for tipo in tipos:
    print(tipo)
    for i,var in enumerate(varis):
        try:
            if tipo == 'u_20mar' or tipo == 'v_20mar':
                tmp1 = xr.open_dataset(mdir1+'Real1_run/'+tipo+'/'+nam[i]+'_'+tipo+'_mean.nc')
            else:
                tmp1 = xr.open_dataset(mdir+'Real1_run/'+tipo+'/'+nam[i]+'_'+tipo+'_mean.nc')
            data[var+'_'+tipo] = tmp1[var]
        except:
            tmp = xr.open_dataset(mdir+'Real1_run/'+tipo+'/'+nam[i]+'_'+tipo+'.nc')
            if tipo == 'uv_12apr':
                data[var+'_'+tipo] = tmp[var].mean(dim='Time')
            else:
                data[var+'_'+tipo] = tmp[var].mean(dim=times[i])
            data[var+'_'+tipo].to_netcdf(mdir+'Real1_run/'+tipo+'/'+nam[i]+'_'+tipo+'_mean.nc')
            data[var+'_'+tipo] = tmp1[var]

### List to plot
print('SST')
var = 'TSK'
ssts = [data[var+'_12_apr'], data[var+'_20_mar'], data[var+'_qv_12apr'], data[var+'_qv_20mar'], data[var+'_uv_12apr'], data[var+'_uv_20mar'], data[var+'_u_12apr'], data[var+'_u_20mar'], data[var+'_v_12apr'], data[var+'_v_20mar']]
print('TCWV')
var = 'QVAPOR'
tcwvs = [data[var+'_12_apr'], data[var+'_20_mar'], data[var+'_qv_12apr'], data[var+'_qv_20mar'], data[var+'_uv_12apr'], data[var+'_uv_20mar'], data[var+'_u_12apr'], data[var+'_u_20mar'], data[var+'_v_12apr'], data[var+'_v_20mar']]
print('U')
var = 'U'
us = [data[var+'_12_apr'], data[var+'_20_mar'], data[var+'_qv_12apr'], data[var+'_qv_20mar'], data[var+'_uv_12apr'], data[var+'_uv_20mar'], data[var+'_u_12apr'], data[var+'_u_20mar'], data[var+'_v_12apr'], data[var+'_v_20mar']]
print('V')
var = 'V'
vs = [data[var+'_12_apr'], data[var+'_20_mar'], data[var+'_qv_12apr'], data[var+'_qv_20mar'], data[var+'_uv_12apr'], data[var+'_uv_20mar'], data[var+'_u_12apr'], data[var+'_u_20mar'], data[var+'_v_12apr'], data[var+'_v_20mar']] 

#### Plotting
jum1 = 42
tcwlev = np.arange(30,71,2.5)
titles = ['(a)','(b)','(c)','(d)','(e)','(f)','(g)','(h)','(i)','(j)']

fig = plt.figure(figsize=(8,15))
gs = GridSpec(6,2, left = 0.09, right = 0.9, hspace=0.15, wspace=0.05, top = 0.95, bottom = 0.08, height_ratios = [1,1,1,1,1,0.1])
for i,sst in enumerate(ssts):
    ax = plt.subplot(gs[i],projection= ccrs.PlateCarree(central_longitude=180))
    # TCWV
    im = plt.contourf(sst['XLONG'],sst['XLAT'], tcwvs[i][0,:,:], cmap='BrBG', transform = ccrs.PlateCarree(), extend = 'both', levels=tcwlev)
    # SST
    im1 = plt.contour(sst['XLONG'],sst['XLAT'], sst, cmap='hot_r', transform = ccrs.PlateCarree(), extend = 'both', linewidths = 1, levels = np.arange(301,303.51,0.5))
    ax.add_feature(cfeature.COASTLINE)
    ax.set_extent([135, 145, 2.05, 9], crs=ccrs.PlateCarree())
    plt.clabel(im1, fontsize=8, inline=1, fmt = '%4.2f', levels = np.arange(301,303.51,0.5))
    # Wind
    if i == 4:
        im2 = plt.quiver(us[i]['XLONG_U'][0,::jum1],us[i]['XLAT_U'][::jum1,0],np.array(us[i][0,::jum1,::jum1]),  np.array(vs[i][::jum1,::jum1]), transform = ccrs.PlateCarree(), edgecolor='k', linewidth = 0.8, units='xy',  headlength = 4, headwidth = 2.5, scale = 15, color = 'k')
    else:
        im2 = plt.quiver(us[i]['XLONG_U'][0,::jum1],us[i]['XLAT_U'][::jum1,0],np.array(us[i][0,::jum1,::jum1]),  np.array(vs[i][0,::jum1,::jum1]), transform = ccrs.PlateCarree(), edgecolor='k', linewidth = 0.8, units='xy',  headlength = 4, headwidth = 2.5, scale = 15, color = 'k')
    if i == 1 or i == 0:
        ax.quiverkey(im2,0.45,1.17,10,'10 m s$^{-1}$', labelpos='E', fontproperties={'size':12})
    gl = ax.gridlines(crs = ccrs.PlateCarree(), draw_labels = True, linewidth = 1, color='k', alpha = 0.5, linestyle = '--')
    gl.xlocator = mticker.FixedLocator([137.5, 140, 142.5])
    gl.ylocator = mticker.FixedLocator([3.75, 5.5, 7.25])
    if i > 1:
        gl.xlabels_top = False
    if i < 8:
        gl.xlabels_bottom = False
    if i == 0 or i == 2 or i == 4 or i == 6 or i == 8:
        gl.ylabels_right = False
    else:
        gl.ylabels_left = False
    plt.title(titles[i], loc = 'left')

ax = plt.subplot(gs[5,:])
cbar = plt.colorbar(im,cax=ax,shrink = 0.4,ticks=np.arange(30,71,5),orientation = 'horizontal')
cbar.set_label('TCWV (mm)')
plt.savefig(scr+'WRF_maps_Exps.jpg', bbox_inches = 'tight', dpi = 300)
plt.savefig(scr+'WRF_maps_Exps.pdf', bbox_inches = 'tight', dpi = 300)
#plt.show()
plt.close()

#### Other example
fig = plt.figure(figsize=(12,6))
gs = GridSpec(3,4, left = 0.09, right = 0.9, hspace=0.2, wspace=0.1, top = 0.95, bottom = 0.08)
for i,sst in enumerate(ssts):
    ax = plt.subplot(gs[i],projection= ccrs.PlateCarree(central_longitude=180))
    # TCWV
    im = plt.contourf(sst['XLONG'],sst['XLAT'], tcwvs[i][0,:,:], cmap='BrBG', transform = ccrs.PlateCarree(), extend = 'both', levels=tcwlev)
    # SST
    im1 = plt.contour(sst['XLONG'],sst['XLAT'], sst, cmap='hot_r', transform = ccrs.PlateCarree(), extend = 'both', linewidths = 1, levels = np.arange(301,303.51,0.5))
    ax.add_feature(cfeature.COASTLINE)
    ax.set_extent([135, 145, 2.05, 9], crs=ccrs.PlateCarree())
    plt.clabel(im1, fontsize=8, inline=1, fmt = '%4.2f', levels = np.arange(301,303.51,0.5))
    # Wind
    if i == 4:
        im2 = plt.quiver(us[i]['XLONG_U'][0,::jum1],us[i]['XLAT_U'][::jum1,0],np.array(us[i][0,::jum1,::jum1]),  np.array(vs[i][::jum1,::jum1]), transform = ccrs.PlateCarree(), edgecolor='k', linewidth = 0.8, units='xy',  headlength = 4, headwidth = 2.5, scale = 15, color = 'k')
    else:
        im2 = plt.quiver(us[i]['XLONG_U'][0,::jum1],us[i]['XLAT_U'][::jum1,0],np.array(us[i][0,::jum1,::jum1]),  np.array(vs[i][0,::jum1,::jum1]), transform = ccrs.PlateCarree(), edgecolor='k', linewidth = 0.8, units='xy',  headlength = 4, headwidth = 2.5, scale = 15, color = 'k')
    if i == 6:
        ax.quiverkey(im2,1,-0.525,10,'10 m s$^{-1}$', labelpos='E', fontproperties={'size':12})
    gl = ax.gridlines(crs = ccrs.PlateCarree(), draw_labels = True, linewidth = 1, color='k', alpha = 0.5, linestyle = '--')
    gl.xlocator = mticker.FixedLocator([137.5, 140, 142.5])
    gl.ylocator = mticker.FixedLocator([3.75, 5.5, 7.25])
    if i > 3:
        gl.xlabels_top = False
    if i < 8:
        gl.xlabels_bottom = False
    if i == 0 or i == 1 or i == 2 or i == 4 or i == 5 or i == 6 or i == 8:
        gl.ylabels_right = False
    if i == 1 or i == 2 or i == 3 or i == 5 or i == 6 or i == 7 or i == 9:
        gl.ylabels_left = False
    plt.title(titles[i], loc = 'left')

gs1 = GridSpec(3,4)
gs1.update(left=0.2, right = 0.88, top= 0.3, bottom=0.19)
ax = plt.subplot(gs1[2,2:4])
cbar = plt.colorbar(im,cax=ax,shrink = 0.4,ticks=np.arange(20,71,5),orientation = 'horizontal')
cbar.set_label('TCWV (mm)')
#plt.savefig(scr+'WRF_maps_Exps_example2.jpg', bbox_inches = 'tight', dpi = 300)
#plt.savefig(scr+'WRF_maps_Exps_example2.pdf', bbox_inches = 'tight', dpi = 300)
#plt.show()
plt.close()
