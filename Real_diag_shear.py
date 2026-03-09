import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import pdb
from skimage.measure import label, regionprops, perimeter
import pandas as pd
from bisect import bisect_left
from joblib import dump,load
from mpl_toolkits.axes_grid1 import make_axes_locatable
from netCDF4 import Dataset
from scipy import stats
import Casicus as casi

#Paths!
scra = '/home/netapp-clima/scratch/acasallas/wrf/Real_run/WRF/'
reals = '/home/tompkins-archive/acasallas/Real1_run/'
user = '/home/netapp-clima/users/acasallas/'
med = '/media/acasallas/ALEJO_HD/Mac_backup/Documents/PhD/Plots/Reals/'

####################################################################
### Read data
#tests = ['control','qv_20mar','uv_mar20','20_mar','12_apr','HML']
tests = ['JJA']
bot = '9'
end = 55
verti = 'no' 

for test in tests:
    print('########## '+test+' ##########')
    ds = xr.open_dataset(scra+'qv_vert_'+test+'.nc')
    ###Calculate organization index
    BLWc = np.array([])
    BLWb = np.array([])
    IQR = np.array([])
    # BLW and IQR indexes for each time
    print('Calculating Organization indexes')
    print('BLW and IQR')
    for i in range(np.shape(ds.QVAPOR)[0]):
        CRH = ds.QVAPOR[i,0,:,:]
        BLWc = np.append(BLWc, casi.calc_MMLi(CRH,True,88))
        BLWb = np.append(BLWb, casi.calc_MMLi(CRH,False,88))
        IQR = np.append(IQR, np.quantile(CRH,0.75) - np.quantile(CRH,0.25))
    #BLWc = casi.moving_average(BLWc,6)
    #BLWb = casi.moving_average(BLWb,6)
    del(ds)

    # Iorg index for W
    # Only need to put a threshold and the variables you want! in 2D
    #ds1 = Dataset(reals+test+'/test_'+test+'.nc')
    ds1 = Dataset(scra+'qv_vert_'+test+'.nc')
    Iorg = np.array([])
    vari = 'QVAPOR'
    print('Iorg')
    for i in range(np.shape(ds1[vari])[0]):
        CRH = np.array(ds1[vari][i,0,:,:])
        #Iorg = np.append(Iorg,casi.calc_Iorg_complete(np.array(ds1[vari][i,12,:,:]),(0,40)))
        Iorg = np.append(Iorg,casi.calc_Iorg_complete(CRH,(np.quantile(CRH,0.72),np.quantile(CRH,1))))
    del(ds1)

    ### Starting hov muller
    print('Starting Hovmuller script!')
    time1 = 0*24
    time2 = end*24
    ntime=time2-time1+1 # 240 quick hack should be read from the netcdf file really...
    yticki= 5.0
    qv_press=1100.
    runlist=[scra+'test_'+test+'.nc']
    nrun=len(runlist)
    dtime=3600 #This depends on the ouput frequency
    difftime=str(dtime)
    ylab='Time (days)'
    xlab= "TCWV %-tile"
    funits="(W m$^{-2}$)"
    fstr=difftime+'-'+str(time1)+'-'+str(time2)
    sstconts=[-1,-0.5,-0.2,-0.1,0.1,0.2,0.5,1.0]
    sstconts=[-0.2,-0.1,-0.05,0.05,0.1,0.2]
    #Domain and splits
    nx=552
    ny=399
    nz=32
    npts=nx*ny # hardwired for moment
    hovchunk=1656  #1024 # averaging length for chunking, power of 2, larger=smoother.
    nhov=int(npts/hovchunk)
    hovx=100*(np.arange(nhov)+0.5)/nhov
    ilev1=0
    ilev2=8
    #constants
    Rd=287.05
    Cp=1005.0
    Lv=2.5e6
    Cpdsinday=Cp/86400.
    #Start matrixes 
    times=np.array(range(ntime)) # start from day 1 for spin up
    #slices=times+time1
    hovtimes=(times+time1)*dtime/86400.
    heights=np.array(range(nz))
    tcwv_hov=np.zeros([nrun,ntime,nhov])
    sst_hov=np.zeros([nrun,ntime,nhov])
    print("Read ",ntime,"timeslices")

    for irun,run in enumerate(runlist):
        difftimefstr=fstr+"_tcwv"+str(qv_press)
        #reset ds?
        dfile=run
        print("opening ",dfile)
        ds1=Dataset(dfile)
        print ("starting step loop")
        ds=Dataset(scra+'qv_vert_'+test+'.nc') 
        for itime in times:
            itime1 = itime+time1
            slice=itime1+time1
            sst=  np.array(ds1.variables["TSK"][slice,:,:])
            tcwv=np.array(ds['QVAPOR'][slice,:,:])
            # sort the tcwv
            isort=np.argsort(tcwv.flatten()) # sort tcwv
            sstpert=sst.flatten()-np.mean(sst)
            tcwv_hov[irun,itime,:]=np.mean(tcwv.flatten()[isort].reshape(-1,hovchunk),axis=1)
            sst_hov[irun,itime,:]=np.mean(sstpert[isort].reshape(-1,hovchunk),axis=1)
    del(ds)
    del(ds1)
    ds = xr.open_dataset(scra+'/test_'+test+'.nc')
    ps = ds.PSFC[400,:,:]
    znu=  ds.ZNU[0,:]*ps[0,0]/100.
    del(ds) 
    ### Wind Shear from pre process file!!!
    print('Shear')
    du = xr.open_dataset(scra+'shear_u_'+test+'_13-'+bot+'.nc')
    du = du.U
    dv = xr.open_dataset(scra+'shear_v_'+test+'_13-'+bot+'.nc')
    dv = dv.V

    ### Wind
    print('u-component')
    ds3 = xr.open_dataset(scra+'u10_'+test+'.nc')
    U10 = ds3['U10'].mean(dim=['south_north','west_east'])
    umin = ds3['U10'].min(dim=['south_north','west_east'])
    umax = ds3['U10'].max(dim=['south_north','west_east'])
    ds4 = xr.open_dataset(scra+'/v10_'+test+'.nc')
    print('Speed')
    vel = (ds3['U10']*ds3['U10'] + ds4['V10']*ds4['V10'])**(0.5)
    del(ds3)
    del(ds4)
    vel_me = vel.mean(dim=['south_north','west_east'])
    vel_mi = vel.min(dim=['south_north','west_east'])
    vel_ma = vel.max(dim=['south_north','west_east'])
    del(vel) 
    print('v-component')
    ds4 = xr.open_dataset(scra+'v10_'+test+'.nc')
    V10 = ds4['V10'].mean(dim=['south_north','west_east'])
    vmin = ds4['V10'].min(dim=['south_north','west_east'])
    vvmax = ds4['V10'].max(dim=['south_north','west_east'])
    #pdb.set_trace()
    del(ds4)
    ds5 = xr.open_dataset(scra+'zonal_'+test+'_fldmean.nc') 
    ds6 = xr.open_dataset(scra+'meridional_'+test+'_fldmean.nc')   
    zonal = ds5.U[:,:,0,0]
    merid = ds6.V[:,:,0,0]
 
    # average across flds and plot time height
    sst_av=np.mean(sst_hov,axis=1)
    tcwv_av=np.mean(tcwv_hov,axis=1)
    yticks=[1000,900,800,700,600,500,400,300,200,100]
    xticks=[10,30,50,70,90]
    xtickvals=[]
    for irun,run in enumerate(runlist):
        idx=[bisect_left(hovx,i) for i in xticks]
        vals=[round(i,1) for i in tcwv_av[irun,idx]]
        xtickvals.append([str(i)+" ("+str(j)+")" for i,j in zip(xticks,vals)])

    print('Starting plots')
    for irun,run in enumerate(runlist):
        print(run)
        ### Plot
        cl=[0.0]
        fs=9
        vmax = 0.25
        fig,(ax)=plt.subplots(nrows=1,ncols=8,figsize=(25,8)) #width,height
        if verti == 'yes':
            plt.subplots_adjust(hspace=0.0,wspace=0.35,top=0.9,right=0.98,left=0.05)
        else:
            plt.subplots_adjust(hspace=0.0,wspace=0.25,top=0.9,right=0.98,left=0.05)
        # Hov SST
        casi.make_fig(fig,ax[0],hovx,hovtimes,sst_hov[irun,:,:],lab='',ylab=ylab,fsize=fs,cont_levs=-999,yticki=yticki,vmax=vmax)
        ax[0].set_xlabel('TCWV %-tile',fontsize=fs)
        ax[0].set_title('SST anomaly (K)',fontsize=fs)
        # BLW
        #ax[1].plot(BLWb,hovtimes,color = 'k')
        #ax[1].set_title('Zonal Shear vs BLW - R = '+str(np.round(stats.pearsonr(du[0:len(hovtimes)],BLWb[0:len(hovtimes)])[0],3)), fontsize=fs)
        #ax[1].set_xlabel('BLW$_{S}$',fontsize=fs)
        #ax[1].set_ylim(0,end)
        #ax[1].set_xlim(0,0.5)
        #ax[1].set_yticks([0,4,8,12,16,20,24])
        # Iorg
        ax[1].plot(Iorg[0:len(hovtimes)],hovtimes,color = 'darkblue')
        #ax[1].set_title('Zonal Shear vs I$_{org}$ - R = '+str(np.round(stats.pearsonr(du[0:len(hovtimes)],Iorg[0:len(hovtimes)])[0],3)), fontsize=fs)
        ax[1].set_xlabel('Iorg',fontsize=fs)
        ax[1].set_ylim(0,end)
        if test == 'qv_time':
            ax[1].set_xlim(0.5,0.8) 
        elif test == '12_apr' or test == 'qv_12apr' or test == 'uv_12apr' :
            ax[1].set_xlim(0.55,0.85)
        elif test == 'uv_mar20':
            ax[1].set_xlim(0.5,0.92)
        else:
            ax[1].set_xlim(0.55,0.94)
        #ax[1].set_yticks([0,4,8,12,16,20,24])
        ax[1].set_yticks([0,5,10,15,20,25,30,35,40,45,50,55])
        # IQR 
        ax[2].plot(IQR[0:len(hovtimes)],hovtimes,color = 'blue')
        #ax[2].set_title('Zonal Shear vs IQR - R = '+str(np.round(stats.pearsonr(du[0:len(hovtimes)],IQR[0:len(hovtimes)])[0],3)), fontsize=fs)
        ax[2].set_xlabel('IQR (mm)',fontsize=fs)
        ax[2].set_ylim(0,end)
        if test == 'qv_time': 
            ax[2].set_xlim(2,8)
        elif test == '12_apr' or test == 'qv_12apr' or test == 'uv_12apr':
            ax[2].set_xlim(2,12)
        elif test == '20_mar':
            ax[2].set_xlim(10,40)
        elif test == 'uv_mar20' or test == 'qv_20mar':
            ax[2].set_xlim(0,40)
        else:
            ax[2].set_xlim(0,30)
        #ax[2].set_yticks([0,4,8,12,16,20,24])
        ax[2].set_yticks([0,5,10,15,20,25,30,35,40,45,50,55])
        ##### Zonal Shear
        if verti == 'yes':
            im = ax[3].contourf(znu[:],hovtimes,zonal[0:len(hovtimes)], cmap = 'seismic', levels=np.arange(-20,21,2.5),extend='both')
            fig.colorbar(im, ax=ax[3], shrink = 0.6)
            ax[3].set_title('Zonal wind (m s$^{-1}$)',fontsize=fs)
            ax[3].set_xlabel('Pressure (hPa)',fontsize=fs) 
            ax[3].set_xlim(1000,0)
        else:
            ax[3].plot(du[0:len(hovtimes)],hovtimes,color = 'purple')
            ax[3].axvline(0, linestyle = ':', color = 'k', linewidth = 0.7)
            ax[3].set_xlabel('Zonal shear (s$^{-1}$)',fontsize=fs)
        ax[3].set_ylim(0,end)
        #ax[3].set_yticks([0,4,8,12,16,20,24])
        ax[3].set_yticks([0,5,10,15,20,25,30,35,40,45,50,55])
        ##### Meridional Shear
        if verti == 'yes':
            im = ax[4].contourf(znu[:],hovtimes,merid[0:len(hovtimes)], cmap = 'seismic', levels=np.arange(-10,11,2),extend='both')
            fig.colorbar(im, ax=ax[4], shrink = 0.6)
            ax[4].set_title('Meridional wind (m s$^{-1}$)',fontsize=fs)
            ax[4].set_xlabel('Pressure (hPa)',fontsize=fs)
            ax[4].set_xlim(1000,0)
        else:
            ax[4].plot(dv[0:len(hovtimes)],hovtimes,color = 'royalblue')
            ax[4].axvline(0, linestyle = ':', color = 'k', linewidth = 0.7)
            ax[4].set_xlabel('Meridional shear (s$^{-1}$)',fontsize=fs)
        ax[4].set_ylim(0,end)
        #ax[4].set_yticks([0,4,8,12,16,20,24])
        ax[4].set_yticks([0,5,10,15,20,25,30,35,40,45,50,55])
        # U10 wind component
        ax[5].plot(umin[0:len(hovtimes)],hovtimes,color='r',label='Min')
        ax[5].plot(U10[0:len(hovtimes)],hovtimes,color='green',label='Mean')
        ax[5].plot(umax[0:len(hovtimes)],hovtimes,color='b',label='Max')
        ax[5].set_ylim(0,end)
        if test == 'vel_rela':
            ax[5].set_xlim(-65,65)
            ax[5].set_xticks([-60,-45,-30,-15,0,15,30,45,60])
        else:
            ax[5].set_xlim(-30,20)
            ax[5].set_xticks([-30,-20,-10,0,10,20])
        ax[5].axvline(0.0,linestyle=':',color='k')
        ax[5].set_xlabel('u-10m (m/s)',fontsize=fs)
        #ax[5].set_yticks([0,4,8,12,16,20,24])
        ax[5].set_yticks([0,5,10,15,20,25,30,35,40,45,50,55])
        ax[5].legend(loc='upper center',bbox_to_anchor=(0.5, 1.1),fontsize=fs,ncol=3)
        # V10 wind component
        ax[6].plot(vmin[0:len(hovtimes)],hovtimes,color='r',label='v-min')
        ax[6].plot(V10[0:len(hovtimes)],hovtimes,color='green',label='v-mean')
        ax[6].plot(vvmax[0:len(hovtimes)],hovtimes,color='b',label='v-max')
        ax[6].set_ylim(0,end)
        if test == 'vel_rela':
            ax[6].set_xlim(-65,65)
            ax[6].set_xticks([-60,-45,-30,-15,0,15,30,45,60])
        else:
            ax[6].set_xlim(-25,25)
        ax[6].axvline(0.0,linestyle=':',color='k')
        ax[6].set_xlabel('v-10m (m/s)',fontsize=fs)
        #ax[6].set_yticks([0,4,8,12,16,20,24])
        ax[6].set_yticks([0,5,10,15,20,25,30,35,40,45,50,55])
        # Vel10
        ax[7].plot(vel_mi[0:len(hovtimes)],hovtimes,color='r',label='Speed-min')
        ax[7].plot(vel_me[0:len(hovtimes)],hovtimes,color='green',label='Speed-mean')
        ax[7].plot(vel_ma[0:len(hovtimes)],hovtimes,color='b',label='Speed-max')
        ax[7].set_ylim(0,end)
        #ax[7].set_xlim(-0.5,25)
        ax[7].set_xlabel('Speed-10m (m/s)',fontsize=fs)
        ax[7].set_yticks([0,5,10,15,20,25,30,35,40,45,50,55])
        
        if verti == 'yes':
            #plt.savefig(reals+'Index_shear_'+test+'_vert.jpg')
            plt.savefig(med+test+'/Index_shear_'+test+'_vert.jpg')
        else:
            #plt.savefig(reals+'Index_shear_'+test+'_13-'+bot+'.jpg')
            plt.savefig(med+test+'/Index_shear_'+test+'_13-'+bot+'.jpg')
        plt.show()

print('##### Complete #####')
