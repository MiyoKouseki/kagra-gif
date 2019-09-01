import numpy as np
import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert

start = tconvert('Aug 09 2019 00:00:00 JST') # IP_DAMP
#start = tconvert('Aug 09 2019 13:00:00 JST') # IP_DAMP, IP_SC
#start = tconvert('Aug 13 2019 11:30:00 JST') # IP_DAMP, BF_DAMP, IP_SC
start = tconvert('Aug 13 2019 12:30:00 JST') # IP_DAMP, BF_DAMP
end = start + 2**11
chname = ['K1:VIS-ETMX_IP_DAMP_L_IN1_DQ',
          'K1:VIS-ETMX_IP_DAMP_T_IN1_DQ',
          'K1:VIS-ETMX_IP_DAMP_Y_IN1_DQ',
          #'K1:VIS-ETMX_IP_SENSCORR_L_OUT16',
          'K1:VIS-ETMX_BF_DAMP_L_IN1_DQ',
          'K1:VIS-ETMX_BF_DAMP_T_IN1_DQ',
          'K1:VIS-ETMX_BF_DAMP_Y_IN1_DQ',
          'K1:VIS-ETMX_TM_DAMP_L_IN1_DQ',
          'K1:VIS-ETMX_TM_DAMP_Y_IN1_DQ',
          'K1:PEM-SEIS_EXV_GND_X_OUT_DQ',
         ] 
data = TimeSeriesDict.fetch(chname,start,end,host='10.68.10.121',port=8088,verbose=True)
data = data.resample(32)
ip_l = data['K1:VIS-ETMX_IP_DAMP_L_IN1_DQ']
bf_l = data['K1:VIS-ETMX_BF_DAMP_L_IN1_DQ']
tm_l = data['K1:VIS-ETMX_TM_DAMP_L_IN1_DQ']/2.3 
gnd_l = data['K1:PEM-SEIS_EXV_GND_X_OUT_DQ']
gnd_l_ = gnd_l.highpass(3e-3).zpk([], [0], 1)
gnd_l_.override_unit('um')
tm_l.override_unit('um')
ip_l.override_unit('um')
bf_l.override_unit('um')

tm = tm_l - gnd_l_
ip = ip_l - gnd_l_
ip_ = ip_l + gnd_l_
bf = bf_l - gnd_l_

if True:
    plot = gnd_l.plot()
    ax = plot.gca()
    ax.plot(gnd_l_)
    plot.savefig('huge.png')
    plot.close()
    #exit()

fftlength = 2**8
overlap = 2**7
ip_l = ip_l.asd(fftlength=fftlength,overlap=overlap)
bf_l = bf_l.asd(fftlength=fftlength,overlap=overlap)
tm_l = tm_l.asd(fftlength=fftlength,overlap=overlap) 
gnd_l = gnd_l.asd(fftlength=fftlength,overlap=overlap)
gnd_l = gnd_l/(2.0*np.pi*gnd_l.frequencies.value)
gnd_l_ = gnd_l_.asd(fftlength=fftlength,overlap=overlap)
ip = ip.asd(fftlength=fftlength,overlap=overlap)
ip_ = ip_.asd(fftlength=fftlength,overlap=overlap)
bf = bf.asd(fftlength=fftlength,overlap=overlap)
tm = tm.asd(fftlength=fftlength,overlap=overlap)

fig,(ax,ax2) = plt.subplots(2,1,figsize=(8,8))
plt.suptitle('IP\_DAMP+BF\_DAMP+IP\_SC',fontsize=25)
plt.suptitle('IP\_DAMP',fontsize=25)
ax.loglog(gnd_l,label='GND L',color='k',linewidth=3)
ax.loglog(gnd_l_,label='GND L',color='r',linewidth=3)
ax.loglog(ip_l,label='IP L')
ax.loglog(bf_l,label='BF L')
ax.loglog(tm_l,label='TM L')
ax.legend()
ax.set_ylim(1e-3,10)
ax.set_xlim(1e-2,10)
ax.set_ylabel('Diplacement [um/rtHz]')
ax2.loglog(ip,label='IP')
ax2.loglog(ip_,linestyle='--',color='k')
ax2.loglog(bf,label='BF')
ax2.loglog(tm,label='TM')
ax2.loglog(gnd_l_,label='GND')
ax2.loglog(tm_l,label='TM\_L')
ax2.set_xlabel('Frequency [Hz]')
ax2.set_ylabel('Residual [um/rtHz]')
ax2.legend()
ax2.set_ylim(1e-3,10)
ax2.set_xlim(1e-2,10)
plt.savefig('hoge.png')
plt.close()
