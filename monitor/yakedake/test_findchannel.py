import numpy as np
import matplotlib
matplotlib.rcParams['backend'] = 'TkAgg'

from gwpy.detector import ChannelList
from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert
start = tconvert('Nov 23 2018 00:00:00 JST')
end = tconvert('Nov 26 2018 00:00:00 JST')

chname_etmx = 'K1:VIS-ETMX_IP_BLEND_LVDTL_INMON'
chlst_etmx = ChannelList.query_nds2([chname_etmx],host='10.68.10.121',port=8088)
chname_seis = 'K1:PEM-EXV_SEIS*_WE_SENSINF_IN1_DQ'
chlst_seis = ChannelList.query_nds2([chname_seis],host='10.68.10.121',port=8088)
chlst = chlst_etmx + chlst_seis
#chlst = chlst_seis
data = TimeSeriesDict.fetch(chlst,start,end,host='10.68.10.121',port=8088,verbose=True,pad=np.nan)
labels = [d.name[3:].replace('_',' ') for d in data]
print labels
plot = data.plot()
plot.legend(labels)
plot.savefig('hoge.png')
