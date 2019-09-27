import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeries,TimeSeriesDict
import numpy as np

channels = [
    'K1:GIF-X_STRAIN_OUT16',
    'K1:VIS-ETMX_GIF_ARM_L_OUT16',
    'K1:CAL-CS_PROC_XARM_FILT_AOM_OUT16',
    'K1:CAL-CS_PROC_XARM_FILT_TM_OUT16',
    'K1:VIS-ETMX_IP_BLEND_ACCL_IN1_DQ',
    'K1:VIS-ITMX_IP_BLEND_ACCL_IN1_DQ',
    'K1:VIS-ETMX_IP_BLEND_LVDTL_IN1_DQ',
    'K1:VIS-ITMX_IP_BLEND_LVDTL_IN1_DQ',
    'K1:PEM-SEIS_EXV_GND_X_OUT16',
    'K1:PEM-SEIS_IXV_GND_X_OUT16',
    'K1:PEM-SEIS_EXV_GND_X_OUT_DQ',
    'K1:PEM-SEIS_IXV_GND_X_OUT_DQ',    
    ]
# Seismometer SC (IPdcdamp + IPsc with seismometers)
start = 'Sep 06 2019 00:30:00 JST'
end   = 'Sep 06 2019 01:30:00 JST'
# No Control (IPdcdamp only)
start = 'Sep 06 2019 01:40:00 JST'
end   = 'Sep 06 2019 02:40:00 JST'
# # Strainmeter 1st trial (IPdcdamp + GIFsc, mat=1,gain=-1)
# start = 'Sep 06 2019 02:52:00 JST' # correct sign.
# end   = 'Sep 06 2019 03:02:00 JST'
# # Strainmeter 2nd trial (IPdcdamp + GIFsc, mat=-1,gain=-1)
# start = 'Sep 06 2019 03:10:00 JST' # wrong sign...
# end   = 'Sep 06 2019 03:20:00 JST'
# # Strainmeter 3rd trial (IPdcdamp + GIFsc, mat=1,gain=-1)
# start = 'Sep 06 2019 03:22:00 JST' # dame! , control signal saturated because of output limitter.
# end   = 'Sep 06 2019 04:00:00 JST'
# # Strainmeter 4th trial (IPdcdamp + GIFsc, mat=1,gain=-1)
# start = 'Sep 06 2019 03:42:00 JST' 
# end   = 'Sep 06 2019 04:42:00 JST'

# setting
fftlen = 2**7
ovlp = fftlen/2.0

def timeseries(start,end,plot=True):
    kwargs = {'verbose':True,'host':'10.68.10.121','port':8088}
    data = TimeSeriesDict.fetch(channels,start,end,**kwargs)
    c = 299792458 # m/sec
    lam = 1064e-9 # m
    gif = data['K1:VIS-ETMX_GIF_ARM_L_OUT16']
    xarm = data['K1:CAL-CS_PROC_XARM_FILT_AOM_OUT16']*3000.0/(c/lam)*1e6 # [um]
    #xarm = data['K1:CAL-CS_PROC_XARM_FILT_TM_OUT16']*3000.0/(c/lam)*1e6 # [um]
    _etmx_seis = data['K1:PEM-SEIS_EXV_GND_X_OUT16']
    _itmx_seis = data['K1:PEM-SEIS_IXV_GND_X_OUT16']
    etmx_seis = data['K1:PEM-SEIS_EXV_GND_X_OUT_DQ']
    itmx_seis = data['K1:PEM-SEIS_IXV_GND_X_OUT_DQ']    
    _diff_seis = etmx_seis - itmx_seis
    diff_seis = etmx_seis - itmx_seis
    etmx_lvdt = data['K1:VIS-ETMX_IP_BLEND_LVDTL_IN1_DQ']
    itmx_lvdt = data['K1:VIS-ITMX_IP_BLEND_LVDTL_IN1_DQ']
    diff_lvdt = etmx_lvdt + itmx_lvdt
    comm_seis = etmx_seis + itmx_seis
    #comm_seis = diff_seis
    if plot:
        plt.plot(gif)
        plt.savefig('timeseries.png')
        plt.close()
    return gif,xarm,diff_seis,comm_seis,diff_lvdt

def coherence(gif,xarm,diff_seis,comm_seis,diff_lvdt,fftlen=2**8,ovlp=2**7):
    coh_gif2xarm = gif.coherence(xarm,fftlength=fftlen,overlap=ovlp)
    coh_gif2seis = gif.coherence(diff_seis,fftlength=fftlen,overlap=ovlp)
    coh_xarm2seiscomm = xarm.coherence(comm_seis,fftlength=fftlen,overlap=ovlp)
    coh_xarm2lvdt = xarm.coherence(diff_lvdt,fftlength=fftlen,overlap=ovlp)
    return coh_gif2xarm,coh_gif2seis,coh_xarm2seiscomm,coh_xarm2lvdt


def asd(gif,xarm,diff_seis,comm_seis,diff_lvdt,fftlen=2**8,ovlp=2**7):
    gif = gif.asd(fftlength=fftlen,overlap=ovlp)
    xarm = xarm.asd(fftlength=fftlen,overlap=ovlp)
    diff_seis = diff_seis.asd(fftlength=fftlen,overlap=ovlp)
    diff_lvdt = diff_lvdt.asd(fftlength=fftlen,overlap=ovlp)
    comm_seis = comm_seis.asd(fftlength=fftlen,overlap=ovlp)
    w = 2.0*np.pi*(diff_seis.frequencies.value)
    diff_seis = diff_seis/w
    comm_seis = comm_seis/w
    return gif,xarm,diff_seis,comm_seis,diff_lvdt


# start = 'Sep 06 2019 03:25:00 JST'
# #end   = 'Sep 06 2019 03:55:00 JST'
# end   = 'Sep 06 2019 04:25:00 JST'
# gif,xarm,diff_seis,comm_seis,diff_lvdt = timeseries(start,end)
# fig, (ax1,ax2) = plt.subplots(2,1,figsize=(12,7))
# plt.subplots_adjust(hspace=0.11)
# ax1.plot(gif,color='k',label='Strainmeter Signal')
# ax1.set_xscale('auto-gps')
# ax1.set_ylabel('Displacement [um]')
# ax1.set_ylim(5,13)
# ax1.set_yticks(range(5,15,2))
# ax2.plot(xarm,color='k',label='X-Arm Feedback Signal')
# ax2.set_xscale('auto-gps')
# ax2.set_ylabel('Displacement [um]')
# ax2.set_ylim(51,59)
# ax2.set_yticks(range(51,60,2))
# ax1.legend(fontsize=20,loc='upper left')
# ax2.legend(fontsize=20,loc='upper left')
# plt.savefig('timeseries.png')
# plt.close()
# exit()

# Timeseries when No control
gif,xarm,diff_seis,comm_seis,diff_lvdt = timeseries(start,end)
coh_gif2xarm, coh_gif2seis, coh_xarm2seiscomm,coh_xarm2lvdt = coherence(gif,xarm,diff_seis,comm_seis,diff_lvdt,
                                                                        fftlen=fftlen,ovlp=ovlp)
gif,xarm,diff_seis,comm_seis,diff_lvdt = asd(gif,xarm,diff_seis,comm_seis,diff_lvdt,
                                             fftlen=fftlen,ovlp=ovlp)

#xarm.rms().write('./off_xarm_rms.hdf5')
from gwpy.frequencyseries import FrequencySeries
xarm_rms_off = FrequencySeries.read('./off_xarm_rms.hdf5')
# plot ASD and coherence
fig, (ax1,ax2) = plt.subplots(2,1,figsize=(10,10),sharex=True)
plt.subplots_adjust(hspace=0.06)
ax1.set_title('Sensor Correction ON',fontsize=40)
ax1.loglog(xarm,label='X-Arm',color='g',linewidth=3)
ax1.loglog(xarm.rms(),color='g',linewidth=3,linestyle='--')
#ax1.loglog(xarm_rms_off,color='b',linewidth=3,linestyle='--')
ax1.loglog(gif,label='GIF strainmeter',color='k')
ax1.loglog(diff_seis,label='Seismometer diff.',color='k',linestyle='--',linewidth=1)
#ax1.loglog(diff_lvdt,label='Lvdt diffs',color='g',linestyle='--')
#ax1.loglog(comm_seis,label='Seismometer comm.',color='r',linestyle='--')
ax1.set_ylabel('Displacement [um/rtHz or um]',fontsize=25)
ax1.legend(fontsize=20,loc='lower left')
ax1.set_ylim(1e-4,2)
ax2.set_ylabel('Coherence',fontsize=25)
ax2.semilogx(coh_gif2xarm,label='X-arm vs. GIF',color='g',linewidth=3)
#ax2.semilogx(coh_xarm2seiscomm,label='X-arm vs. Seis Comm',color='r',linewidth=2)
#ax2.semilogx(coh_xarm2lvdt,label='X-arm vs. LVDT diffs',color='g',linewidth=2)
ax2.legend(fontsize=20,loc='upper left')
ax2.set_xlabel('Frequency [Hz]',fontsize=25)
ax2.set_ylim(0,1)
#ax2.set_xlim(5e-3,8)
ax2.set_xlim(1e-2,8)
plt.savefig('result.png')
plt.close()
