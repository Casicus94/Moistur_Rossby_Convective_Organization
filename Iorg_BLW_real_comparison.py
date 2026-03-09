import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pdb
import pandas as pd
from netCDF4 import Dataset
from scipy import stats
import Casicus as casi

reals = '/home/tompkins-archive/acasallas/Real1_run/'
med = '/media/acasallas/ALEJO_HD/Mac_backup/Documents/PhD/Plots/Reals/'

####################################################################
### Read data
tests = ['control','12_apr','20_mar']
colors = ['k','blue','purple']
names = ['Control','Reversal','Organized']


plt.figure(figsize=(12,6))
for j,test in enumerate(tests):
    print('BLW')
    print('########## '+test+' ##########')
    # Iorg index for W
    # Only need to put a threshold and the variables you want! in 2D
    #ds1 = Dataset(reals+test+'/test_'+test+'.nc')
    ds = xr.open_dataset(reals+test+'/qv_vert_'+test+'.nc')
    BLWc = np.array([])
    BLWs = np.array([])
    IQR = np.array([])
    for i in range(np.shape(ds.QVAPOR)[0]):
        CRH = ds.QVAPOR[i,0,:,:]
        BLWc = np.append(BLWc, casi.calc_MMLi(CRH,True,72))
        BLWs = np.append(BLWs, casi.calc_MMLi(CRH,False,72))
        IQR = np.append(IQR, np.quantile(CRH,0.75) - np.quantile(CRH,0.25))
    #BLWc = casi.moving_average(BLWc,6)
    #BLWb = casi.moving_average(BLWb,6)
    del(ds)
    plt.plot(np.linspace(0,55,len(BLWs[10:44*24])), BLWs[10:44*24], label = names[j], color = colors[j])

plt.legend()
#plt.ylim(0.4,1)
plt.ylabel('BLW')
plt.xlabel('Days')
plt.savefig(med+'/Comparations/BLW_comparison.jpg')
plt.show()
plt.close()

plt.figure(figsize=(12,6))
for j,test in enumerate(tests):
    print('IQR')
    print('########## '+test+' ##########')
    # Iorg index for W
    # Only need to put a threshold and the variables you want! in 2D
    #ds1 = Dataset(reals+test+'/test_'+test+'.nc')
    ds = xr.open_dataset(reals+test+'/qv_vert_'+test+'.nc')
    IQR = np.array([])
    for i in range(np.shape(ds.QVAPOR)[0]):
        CRH = ds.QVAPOR[i,0,:,:]
        IQR = np.append(IQR, np.quantile(CRH,0.75) - np.quantile(CRH,0.25))
    #BLWc = casi.moving_average(BLWc,6)
    #BLWb = casi.moving_average(BLWb,6)
    del(ds)
    plt.plot(np.linspace(0,55,len(IQR[10:44*24])), IQR[10:44*24], label = names[j], color = colors[j])

plt.legend()
#plt.ylim(0.4,1)
plt.ylabel('IQR')
plt.xlabel('Days')
plt.savefig(med+'/Comparations/IQR_comparison.jpg')
plt.show()
plt.close()

plt.figure(figsize=(12,6))
for j,test in enumerate(tests):
    print('Iorg')
    print('########## '+test+' ##########')
    # Iorg index for W
    # Only need to put a threshold and the variables you want! in 2D
    #ds1 = Dataset(reals+test+'/test_'+test+'.nc')
    ds1 = Dataset(reals+test+'/qv_vert_'+test+'.nc')
    Iorg = np.array([])
    vari = 'QVAPOR'
    for i in range(np.shape(ds1[vari])[0]):
        CRH = np.array(ds1[vari][i,0,:,:])
        #Iorg = np.append(Iorg,casi.calc_Iorg_complete(np.array(ds1[vari][i,12,:,:]),(0,40)))
        Iorg = np.append(Iorg,casi.calc_Iorg_complete(CRH,(np.quantile(CRH,0.72),np.quantile(CRH,1))))
    plt.plot(np.linspace(0,55,len(Iorg[10:44*24])), Iorg[10:44*24], label = names[j], color = colors[j])

plt.legend()
#plt.ylim(0.4,1)
plt.ylabel('I$_{org}$')
plt.xlabel('Days')
#plt.savefig(med+'/Comparations/Iorg_comparison.jpg')
#plt.show()


