import xshape
import imageio
from shapely.geometry.polygon import LinearRing
import xarray as xr
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
from cartopy.feature import ShapelyFeature
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
from netCDF4 import Dataset
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

mdir = '/home/tompkins-archive/acasallas/ERA5/'
med = '/media/acasallas/ALEJO_HD/Mac_backup/Documents/PhD/Plots/Reals/'

print('Reading SST')
ds_sst = xr.open_dataset(mdir+'SST_all_climate.nc')
print('Reading Precip')
ds_precip = xr.open_dataset(mdir+'Precip_GPM_climate.nc')

a_lat = [2,2,9,9]
a_lon = [135,145,145,135]
ring = LinearRing(list(zip(a_lon, a_lat)))
a1_lat = [-0.25,-0.25,11.5,11.5]
a1_lon = [133,147,147,133]
ring1 = LinearRing(list(zip(a1_lon, a1_lat)))

fig = plt.figure(figsize=(8,6))
gs = GridSpec(2,1,left = 0.09, right = 0.95, hspace=0.2, wspace=0.1, top = 0.88, bottom = 0.2,height_ratios=[1,0.05])
ax = plt.subplot(gs[0],projection= ccrs.PlateCarree(central_longitude=180))
im = plt.contourf(ds_precip['longitude'],ds_precip['latitude'], ds_precip.Precip[0,:,:], cmap='YlGnBu', transform = ccrs.PlateCarree(), extend = 'both', levels=np.arange(3000,10000.01,500))
im1 = plt.contour(ds_sst['longitude'],ds_sst['latitude'], ds_sst.sst[0,:,:], cmap='Reds', transform = ccrs.PlateCarree(), extend = 'both', linewidths = 1, levels=np.arange(301.75,303.26,0.25))
ax.clabel(im1, inline=True, fontsize=8)
ax.add_geometries([ring], ccrs.PlateCarree(), facecolor='none', edgecolor='k', linewidth = 1.25, linestyle = '-')
ax.add_geometries([ring1], ccrs.PlateCarree(),facecolor='none',edgecolor='k',linewidth = 1, linestyle = '--')
plt.text(-46.75,10.75,'Domain 1', fontweight = 'bold')
plt.text(-44.75,8.25,'Domain 2', fontweight = 'bold')
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax.set_extent([130, 150, -1.5, 12.5], crs=ccrs.PlateCarree())
gl = ax.gridlines(crs = ccrs.PlateCarree(), draw_labels = True, linewidth = 0.5, color='k', alpha = 0.5, linestyle = '--')
gl.ylocator = mticker.FixedLocator([0,5,10])
gl.xlocator = mticker.FixedLocator([132.5,137.5,142.5,147.5])
plt.ylim(-1.5,12.5)

ax = plt.subplot(gs[1])
cbar = plt.colorbar(im,cax=ax,orientation='horizontal',shrink = 0.4, ticks=np.arange(3000,10000.01,1000))
#cbar.ax.xaxis.set_ticks_position("top")
#cbar.ax.set_title('mm year$^{-1}$')
cbar.set_label('mm year$^{-1}$')

plt.savefig(med+'Domains_climatology.jpg', bbox_inches='tight',dpi=300)
plt.savefig(med+'Domains_climatology.pdf', bbox_inches='tight',dpi=300)
#plt.show()


