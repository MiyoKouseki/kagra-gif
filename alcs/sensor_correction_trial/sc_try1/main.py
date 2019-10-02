# /usr/bin/env python
# 
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
    ]
import argparse   
parser = argparse.ArgumentParser(description='')
parser.add_argument('hoge', help='hoge')    
args = parser.parse_args() 
hoge = args.hoge
if hoge == 'sc1_0':
    # SC1_0 : Seismometer SC (IPdcdamp + IPsc with seismometers)
    start = tconvert('Sep 06 2019 00:30:00 JST')
    end   = tconvert('Sep 06 2019 01:30:00 JST')
elif hoge == 'sc1_1':
    # SC1_1 : No Control (IPdcdamp only)
    start = tconvert('Sep 06 2019 01:40:00 JST')
    end   = tconvert('Sep 06 2019 02:40:00 JST')
elif hoge == 'sc1_2':
    # SC1_2 : Strainmeter 1st trial (IPdcdamp + GIFsc, mat=1,gain=-1)
    start = tconvert('Sep 06 2019 02:52:00 JST') # correct sign.
    end   = tconvert('Sep 06 2019 03:02:00 JST')
elif hoge == 'sc1_3':
    # SC1_3 : Strainmeter 2nd trial (IPdcdamp + GIFsc, mat=-1,gain=-1)
    start = tconvert('Sep 06 2019 03:10:00 JST') # wrong sign...
    end   = tconvert('Sep 06 2019 03:20:00 JST')
elif hoge == 'sc1_4':
    # SC1_4 : Strainmeter 3rd trial (IPdcdamp + GIFsc, mat=1,gain=-1)
    start = tconvert('Sep 06 2019 03:22:00 JST') # dame! , control signal saturated because of output limitter.
    end   = tconvert('Sep 06 2019 04:00:00 JST')
elif hoge == 'sc1_5':
    # SC1_5 : Strainmeter 4th trial (IPdcdamp + GIFsc, mat=1,gain=-1)
    start = tconvert('Sep 06 2019 03:42:00 JST') 
    end   = tconvert('Sep 06 2019 04:42:00 JST')

# setting
fftlen = 2**6
ovlp = fftlen/2.0

# Timeseries
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

# plot
fig, (ax1,ax2) = plt.subplots(2,1,figsize=(10,10),sharex=True)
plt.subplots_adjust(hspace=0.06)
ax1.set_title('Sensor Correction ON',fontsize=40)
ax1.loglog(xarm,label='X-Arm',color='g',linewidth=3)
ax1.loglog(xarm.rms(),color='g',linewidth=3,linestyle='--')
ax1.loglog(gif,label='GIF strainmeter',color='k')
ax1.loglog(diff_seis,label='Seismometer diff.',color='k',linestyle='--',linewidth=1)
ax1.set_ylabel('Displacement [um/rtHz or um]',fontsize=25)
ax1.legend(fontsize=20,loc='lower left')
ax1.set_ylim(1e-4,2)
ax2.set_ylabel('Coherence',fontsize=25)
ax2.semilogx(coh_gif2xarm,label='X-arm vs. GIF',color='g',linewidth=3)
ax2.legend(fontsize=20,loc='upper left')
ax2.set_xlabel('Frequency [Hz]',fontsize=25)
ax2.set_ylim(0,1)
ax2.set_xlim(1e-2,8)
plt.savefig('{0}.png'.format(hoge))
plt.close()
