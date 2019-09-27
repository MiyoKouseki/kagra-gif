import numpy as np
import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert

import re
import warnings
warnings.filterwarnings('ignore')

    
#start = tconvert('Jul 20 2019 19:00:00 JST')
end   = tconvert('Jul 20 2019 21:25:00 JST')
start = end - 2**11
channels = ['K1:PEM-SEIS_EXV_GND_X_OUT_DQ',
            'K1:PEM-SEIS_IXV_GND_X_OUT_DQ',
            'K1:GIF-X_STRAIN_IN1_DQ',
            'K1:ALS-X_PDH_SLOW_DAQ_OUT_DQ'
           ]
    
data = TimeSeriesDict.fetch(channels,start,end,host='10.68.10.122',port=8088,
                            verbose=True,pad=0.0)


exv_x = data.values()[0]
ixv_x = data.values()[1]
gif   = data.values()[2]*((532e-9/2)/(2.0*np.pi))/1500*3000.0*1e6 # um
pdh   = data.values()[3]

gif = gif.resample(512)
pdh = pdh.resample(512)

# Timeseries
plot = pdh.plot(label=pdh.name.replace('_',' '),ylabel='Count?')
ax = plot.gca()
ax.legend()
plot.savefig('huge.png')
plot.close


# differential motion of the seismometers
diff = exv_x - ixv_x
comm = exv_x + ixv_x

# coherence
csd_gif_diff = gif.csd(diff, fftlength=2**6, overlap=2**5)  # 2**7 = 128
csd_pdh_gif  = pdh.csd(gif,  fftlength=2**6, overlap=2**5)  # 2**7 = 128
csd_pdh_diff = pdh.csd(diff, fftlength=2**6, overlap=2**5)  # 2**7 = 128
csd_pdh_comm = pdh.csd(comm, fftlength=2**6, overlap=2**5)  # 2**7 = 128

gif  =  gif.asd(fftlength=2**6, overlap=2**5)
diff = diff.asd(fftlength=2**6, overlap=2**5)
comm = comm.asd(fftlength=2**6, overlap=2**5)
pdh  =  pdh.asd(fftlength=2**6, overlap=2**5)

coh_gif_diff = csd_gif_diff/gif/(diff*1j)
coh_pdh_gif  = csd_pdh_gif/pdh/gif
coh_pdh_diff = csd_pdh_diff/pdh/(diff*1j)
coh_pdh_comm = csd_pdh_comm/pdh/(comm*1j)

comm = comm/(2.0*np.pi*comm.frequencies.value)
diff = diff/(2.0*np.pi*diff.frequencies.value)


# plot Coherence
fig, (ax0,ax1,ax2) = plt.subplots(3,1,figsize=(10,10))
ax0.loglog(gif,label='GIF',color='k')
ax0.loglog(pdh,label='PDH (um?)',color='b',linestyle='-')
ax0.loglog(diff,label='Seis Diff',color='r',linestyle='-')
ax0.loglog(comm,label='Seis Comm',color='r',linestyle='--')
ax0.legend(fontsize=15,loc='upper right')
ax0.set_ylabel('Diplacement [um/rtHz]')
ax0.set_ylim(1e-3,1e1)
ax0.set_xlim(3e-2, 10)
ax1.semilogx(coh_gif_diff.abs()**2,label='GIF vs Seis Diff',color='g',linestyle='-')
ax1.semilogx(coh_pdh_gif.abs()**2,label='PDH vs GIF',color='k',linestyle='-')
ax1.semilogx(coh_pdh_diff.abs()**2,label='PDH vs Diffs',color='b',linestyle='-')
ax1.semilogx(coh_pdh_comm.abs()**2,label='PDH vs Comms',color='b',linestyle='--')
ax1.set_xlabel('Frequency [Hz]')
ax1.set_ylabel('Magnitude-Squared \n Coherence')
ax1.set_ylim(0, 1)
ax1.set_xlim(3e-2, 10)
ax1.legend(fontsize=15,loc='upper right')
ax2.semilogx(coh_gif_diff.angle().rad2deg(),label='GIF vs Seis Diff',color='g',linestyle='-')
ax2.semilogx(coh_pdh_gif.angle().rad2deg(),label='PDH vs GIF',color='k',linestyle='-')
ax2.semilogx(coh_pdh_diff.angle().rad2deg(),label='PDH vs Diffs',color='b',linestyle='-')
ax2.semilogx(coh_pdh_comm.angle().rad2deg(),label='PDH vs Comms',color='b',linestyle='--')
ax2.set_ylim(-180, 180)
ax2.set_yticks(range(-180, 181, 90))
ax2.set_xlim(3e-2, 10)
ax2.legend(fontsize=15,loc='upper right')
ax2.set_ylabel('Phase [Deg.]')
plt.savefig('hoge.png')
plt.close()
