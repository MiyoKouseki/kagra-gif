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
coh1 = gif.coherence(diff, fftlength=2**6, overlap=2**5) # 2**7 = 128
coh2 = gif.coherence(pdh, fftlength=2**6, overlap=2**5)  # 2**7 = 128
coh3 = pdh.coherence(diff, fftlength=2**6, overlap=2**5)  # 2**7 = 128
coh4 = pdh.coherence(comm, fftlength=2**6, overlap=2**5)  # 2**7 = 128

gif  =  gif.asd(fftlength=2**6, overlap=2**5)
diff = diff.asd(fftlength=2**6, overlap=2**5)
comm = comm.asd(fftlength=2**6, overlap=2**5)
pdh  =  pdh.asd(fftlength=2**6, overlap=2**5)
gif = gif
comm = comm/(2.0*np.pi*comm.frequencies.value)
diff = diff/(2.0*np.pi*diff.frequencies.value)

# plot Coherence
fig, (ax0,ax1) = plt.subplots(2,1,figsize=(10,7))
ax0.loglog(gif,label='GIF',color='k')
ax0.loglog(pdh,label='PDH (um?)',color='b',linestyle='-')
ax0.loglog(diff,label='Seis Diff',color='r',linestyle='-')
ax0.loglog(comm,label='Seis Comm',color='r',linestyle='--')
ax0.legend(fontsize=15,loc='upper tight')
ax0.set_ylabel('Diplacement [um/rtHz]')
ax0.set_ylim(1e-3,1e1)
ax0.set_xlim(3e-2, 10)
ax1.semilogx(coh1,label='GIF vs Seis Diff',color='g',linestyle='-')
ax1.semilogx(coh2,label='PDH vs GIF',color='k',linestyle='-')
ax1.semilogx(coh3,label='PDH vs Diffs',color='b',linestyle='-')
ax1.semilogx(coh4,label='PDH vs Comms',color='b',linestyle='--')
ax1.set_xlabel('Frequency [Hz]')
ax1.set_ylabel('Coherence')
ax1.set_ylim(0, 1)
ax1.set_xlim(3e-2, 10)
plt.legend(fontsize=15,loc='upper tight')
plt.savefig('hoge.png')
plt.close()


