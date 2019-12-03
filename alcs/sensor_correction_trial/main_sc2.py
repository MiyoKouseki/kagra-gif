import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeries,TimeSeriesDict
import numpy as np
from Kozapy.utils import filelist
from gwpy.time import tconvert
channels = [
    'K1:GIF-X_STRAIN_OUT16',
    'K1:VIS-ETMX_GIF_ARM_L_OUT16',
    'K1:CAL-CS_PROC_XARM_FILT_AOM_OUT16',
    'K1:CAL-CS_PROC_XARM_FILT_TM_OUT16',
    'K1:PEM-SEIS_EXV_GND_X_OUT16',
    'K1:PEM-SEIS_IXV_GND_X_OUT16',
    'K1:VIS-ETMX_BF_DAMP_Y_OUT16',
    'K1:VIS-ITMX_BF_DAMP_Y_OUT16',
    'K1:VIS-ETMX_IP_DAMP_Y_OUT16',
    'K1:VIS-ITMX_IP_DAMP_Y_OUT16',
    'K1:VIS-ETMX_BF_DAMP_T_OUT16',
    'K1:VIS-ITMX_BF_DAMP_T_OUT16',
    'K1:VIS-ETMX_IP_DAMP_T_OUT16',
    'K1:VIS-ITMX_IP_DAMP_T_OUT16',
    ]

# --------------------------------------------------

start0 = tconvert('Sep 17 2019 05:26:00 JST')  
end0   = tconvert('Sep 17 2019 05:36:00 JST')
start1 = tconvert('Sep 17 2019 05:39:00 JST')  
end1   = tconvert('Sep 17 2019 05:49:00 JST')

# setting
tlen = int(end1) - int(start1)
ave = 8
fftlen = tlen/ave
#fftlen = 2**6
ovlp = fftlen/2.0

# Timeseries
def huge(start,end):
    source = filelist(start,end,trend='full',place='kashiwa')    
    data = TimeSeriesDict.read(source,channels,start=start,end=end,nproc=4)
    c = 299792458 # m/sec
    lam = 1064e-9 # m
    gif = data['K1:VIS-ETMX_GIF_ARM_L_OUT16']
    xarm = data['K1:CAL-CS_PROC_XARM_FILT_AOM_OUT16']*3000.0/(c/lam)*1e6 # [um]
    etmx_seis = data['K1:PEM-SEIS_EXV_GND_X_OUT16']
    itmx_seis = data['K1:PEM-SEIS_IXV_GND_X_OUT16']
    diff_seis = etmx_seis - itmx_seis
    comm_seis = etmx_seis + itmx_seis

    # Coherence
    coh_gif2xarm = gif.coherence(xarm,fftlength=fftlen,overlap=ovlp)
    coh_gif2seis = gif.coherence(diff_seis,fftlength=fftlen,overlap=ovlp)
    coh_xarm2seiscomm = xarm.coherence(comm_seis,fftlength=fftlen,overlap=ovlp)
    
    # ASD
    gif = gif.asd(fftlength=fftlen,overlap=ovlp)
    xarm = xarm.asd(fftlength=fftlen,overlap=ovlp)
    diff_seis = diff_seis.asd(fftlength=fftlen,overlap=ovlp)
    comm_seis = comm_seis.asd(fftlength=fftlen,overlap=ovlp)
    w = 2.0*np.pi*(diff_seis.frequencies.value)
    diff_seis = diff_seis/w
    comm_seis = comm_seis/w
    return xarm
    
xarm0 = huge(start0,end0)
xarm1 = huge(start1,end1)
# plot
title = 'sc2'
fig, ax1 = plt.subplots(1,1,figsize=(7,7),sharex=True)
#ax1.set_title(title,fontsize=40)
ax1.loglog(xarm0,label='OFF',color='k',linewidth=2)
ax1.loglog(xarm0.rms(),color='k',linewidth=2,linestyle='--')
ax1.loglog(xarm1,label='ON',color='r',linewidth=2)
ax1.loglog(xarm1.rms(),color='r',linewidth=2,linestyle='--')
ax1.set_ylabel('Displacement [um/rtHz or um]',fontsize=20)
ax1.legend(fontsize=20,loc='lower left')
ax1.set_ylim(1e-4,10)
ax1.set_xlabel('Frequency [Hz]',fontsize=20)
#ax1.set_ylim(0,1)
ax1.set_xlim(5e-3,8)
plt.savefig('./{0}.png'.format(title))
plt.close()
