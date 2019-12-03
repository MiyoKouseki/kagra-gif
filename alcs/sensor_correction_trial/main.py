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
# --------------------------------------------------
elif hoge == 'sc2_0': 
    # 4.  Gain 0.5 
    start = tconvert('Sep 17 2019 05:26:00 JST')  
    end   = tconvert('Sep 17 2019 05:36:00 JST')
elif hoge == 'sc2_1':
    # 5. GIF injection    
    start = tconvert('Sep 17 2019 05:39:00 JST')  
    end   = tconvert('Sep 17 2019 05:49:00 JST')
# --------------------------------------------------
elif hoge == 'sc3_0':
    # 1st G=1.4
    start = tconvert('Sep 23 2019 20:43:00 JST')  
    end   = tconvert('Sep 23 2019 20:53:00 JST')
elif hoge == 'sc3_1':
    # 2nd G=1.0
    start = tconvert('Sep 23 2019 21:09:00 JST')  
    end   = tconvert('Sep 23 2019 21:19:00 JST')
elif hoge == 'sc3_2':
    # 3rd G=1.2
    start = tconvert('Sep 23 2019 21:22:00 JST')  
    end   = tconvert('Sep 23 2019 21:32:00 JST')
elif hoge == 'sc3_3':
    # 4th G=0.8
    start = tconvert('Sep 23 2019 21:34:00 JST')  
    end   = tconvert('Sep 23 2019 21:44:00 JST')
elif hoge == 'sc3_4':
    # 5th G=1.1
    start = tconvert('Sep 23 2019 21:46:00 JST')  
    end   = tconvert('Sep 23 2019 21:56:00 JST')
elif hoge == 'sc3_5':
    # 6th G=1.0, LoopGain=0.5
    start = tconvert('Sep 23 2019 22:35:00 JST')  
    end   = tconvert('Sep 23 2019 22:45:00 JST') # Include Glitch caused by GIF
elif hoge == 'sc3_6':
    # 7th G=1.0, LoopGain=0.5
    start = tconvert('Sep 23 2019 22:46:00 JST')  
    end   = tconvert('Sep 23 2019 22:56:00 JST') 
elif hoge == 'sc3_7':
    # 8th G=1.0, LoopGain=1
    start = tconvert('Sep 23 2019 23:25:00 JST')  
    end   = tconvert('Sep 23 2019 23:35:00 JST')     
elif hoge == 'sc3_8':
    # 0nd G=0.0
    start = tconvert('Sep 23 2019 20:57:00 JST')  
    end   = tconvert('Sep 23 2019 21:07:00 JST')    
# --------------------------------------------------
elif hoge == 'sc4_0':
    # 1st 
    start = tconvert('Sep 24 2019 21:55:00 JST')  
    end   = tconvert('Sep 24 2019 22:05:00 JST')
elif hoge == 'sc4_1':
    # 2nd Notch210mHz at ETMX MN P12
    start = tconvert('Sep 24 2019 23:20:00 JST')  
    end   = tconvert('Sep 25 2019 00:10:00 JST')
elif hoge == 'sc4_2':
    # 3d Notch210mHz at ETMX BF YAW
    start = tconvert('Sep 25 2019 00:11:00 JST')  
    end   = tconvert('Sep 25 2019 00:38:00 JST')
elif hoge == 'sc4_3':
    # 4th Update P12
    start = tconvert('Sep 25 2019 00:53:00 JST')  
    end   = tconvert('Sep 25 2019 01:03:00 JST')
elif hoge == 'sc4_4':
    # 5th
    start = tconvert('Sep 25 2019 01:15:00 JST')
    end   = tconvert('Sep 25 2019 01:40:00 JST')
elif hoge == 'sc4_5':
    start = tconvert('Sep 24 2019 22:08:00 JST')  
    end   = tconvert('Sep 24 2019 22:18:00 JST')
elif hoge == 'sc4_6':
    start = tconvert('Sep 24 2019 22:42:00 JST')  
    end   = tconvert('Sep 24 2019 22:52:00 JST')        


# setting
tlen = int(end) - int(start)
ave = 8
fftlen = tlen/ave
#fftlen = 2**6
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
etmx_ip_y = data['K1:VIS-ETMX_IP_DAMP_Y_OUT16']
itmx_ip_y = data['K1:VIS-ITMX_IP_DAMP_Y_OUT16']
etmx_ip_t = data['K1:VIS-ETMX_IP_DAMP_T_OUT16']
itmx_ip_t = data['K1:VIS-ITMX_IP_DAMP_T_OUT16']
diff_seis = etmx_seis - itmx_seis
comm_seis = etmx_seis + itmx_seis

# Coherence
coh_gif2xarm = gif.coherence(xarm,fftlength=fftlen,overlap=ovlp)
coh_gif2seis = gif.coherence(diff_seis,fftlength=fftlen,overlap=ovlp)
coh_xarm2seiscomm = xarm.coherence(comm_seis,fftlength=fftlen,overlap=ovlp)
coh_xarm2itmxipy = xarm.coherence(itmx_ip_y,fftlength=fftlen,overlap=ovlp)
coh_xarm2etmxipy = xarm.coherence(etmx_ip_y,fftlength=fftlen,overlap=ovlp)
coh_xarm2itmxipt = xarm.coherence(itmx_ip_t,fftlength=fftlen,overlap=ovlp)
coh_xarm2etmxipt = xarm.coherence(etmx_ip_t,fftlength=fftlen,overlap=ovlp)

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
ax1.set_title(hoge,fontsize=40)
ax1.loglog(xarm,label='X-Arm',color='r',linewidth=2)
ax1.loglog(xarm.rms(),color='r',linewidth=2,linestyle='--')
ax1.loglog(gif,label='GIF strainmeter',color='g')
#ax1.loglog(comm_seis,label='Seismometer comm.',color='k',linestyle='--',linewidth=1)
ax1.loglog(diff_seis,label='Seismometer diff.',color='k',linestyle='-',linewidth=1)
ax1.loglog(diff_seis.rms(),color='k',linestyle='--',linewidth=2)
ax1.set_ylabel('Displacement [um/rtHz or um]',fontsize=25)
ax1.legend(fontsize=20,loc='lower left')
ax1.set_ylim(1e-4,10)
ax2.set_ylabel('Coherence',fontsize=25)
ax2.semilogx(coh_gif2xarm,label='X-arm vs. GIF',color='r',linewidth=1)
#ax2.semilogx(coh_xarm2seiscomm,label='X-arm vs. Comm.',color='k',linewidth=1,linestyle='--')
#ax2.semilogx(coh_gif2seis,label='Diff. vs. GIF',color='k',linewidth=1)
ax2.legend(fontsize=20,loc='upper left')
ax2.set_xlabel('Frequency [Hz]',fontsize=25)
ax2.set_ylim(0,1)
ax2.set_xlim(1e-2,8)
plt.savefig('./{0}/{1}.png'.format(hoge.split('_')[0],hoge))
plt.close()


# plot
fig, (ax1,ax2) = plt.subplots(2,1,figsize=(15,15),sharex=True)
plt.subplots_adjust(hspace=0.06)
ax1.set_title(hoge,fontsize=40)
ax1.loglog(xarm,label='X-Arm',color='r',linewidth=2)
ax1.loglog(xarm.rms(),color='r',linewidth=2,linestyle='--')
ax1.loglog(gif,label='GIF strainmeter',color='g')
ax1.loglog(comm_seis,label='Seismometer comm.',color='k',linestyle='--',linewidth=1)
ax1.loglog(diff_seis,label='Seismometer diff.',color='k',linestyle='-',linewidth=1)
ax1.loglog(diff_seis.rms(),color='k',linestyle='--',linewidth=2)
ax1.set_ylabel('Displacement [um/rtHz or um]',fontsize=25)
ax1.legend(fontsize=20,loc='lower left')
ax1.set_ylim(1e-4,10)
ax2.set_ylabel('Coherence',fontsize=25)
ax2.semilogx(coh_gif2xarm,label='X-arm vs. GIF',color='r',linewidth=1)
ax2.semilogx(coh_xarm2seiscomm,label='X-arm vs. Comm.',color='k',linewidth=1,linestyle='--')
#ax2.semilogx(coh_gif2seis,label='Diff. vs. GIF',color='k',linewidth=1)
ax2.semilogx(coh_xarm2itmxipy,label='X-arm vs. ITMX_IP_Y_DAMP',linewidth=1)
ax2.semilogx(coh_xarm2itmxipt,label='X-arm vs. ITMX_IP_T_DAMP',linewidth=1)
ax2.semilogx(coh_xarm2etmxipy,label='X-arm vs. ETMX_IP_Y_DAMP',linewidth=1)
ax2.semilogx(coh_xarm2etmxipt,label='X-arm vs. ETMX_IP_T_DAMP',linewidth=1)

ax2.legend(fontsize=20,loc='upper left')
ax2.set_xlabel('Frequency [Hz]',fontsize=25)
ax2.set_ylim(0,1)
ax2.set_xlim(1e-2,8)
plt.savefig('./{0}/{1}_commseis.png'.format(hoge.split('_')[0],hoge))
plt.close()
