import numpy as np
import matplotlib
matplotlib.rcParams['backend'] = 'TkAgg'

from gwpy.detector import ChannelList
from gwpy.plot import text
from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert
from astropy import units as u
import matplotlib.pyplot as plt

start = tconvert('Nov 21 2018 18:18:00 JST')
end = tconvert('Nov 21 2018 18:43:00 JST')
#end = tconvert('Nov 21 2018 18:23:00 JST')

ch = ['K1:ALS-PDHX_SLOW_DAQ_OUT_DQ',
      'K1:VIS-ETMX_IP_BLEND_LVDTL_IN1_DQ',
      'K1:PEM-EXV_SEIS_WE_SENSINF_OUT_DQ']
chlst= ChannelList.query_nds2(ch,host='10.68.10.121',port=8088)
chlst = [ ch.name for ch in chlst]
data = TimeSeriesDict.fetch(chlst,start,end,host='10.68.10.121',port=8088,verbose=True,pad=np.nan)

seis = data['K1:PEM-EXV_SEIS_WE_SENSINF_OUT_DQ']
pdh = data['K1:ALS-PDHX_SLOW_DAQ_OUT_DQ']


asd = pdh.asd(fftlength=2**4)
plot = asd.plot()
plot.savefig('ASD.png')

# coh = seis.coherence(pdh, fftlength=2**5, overlap=2**4)
# plot = coh.plot(
#     xlabel='Frequency [Hz]', xscale='log',
#     ylabel='Coherence', yscale='linear', ylim=(0, 1),
# )
# plot.savefig('Coherence.png')
