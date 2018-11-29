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

chname_grd = 'K1:GRD-ALS_PDHX_STATE_N'
chlst_grd = ChannelList.query_nds2([chname_grd],host='10.68.10.121',port=8088)
chname_pdh = 'K1:ALS-PDHX_SLOW_DAQ_OUTPUT'
chlst_pdh = ChannelList.query_nds2([chname_pdh],host='10.68.10.121',port=8088)
chname_etmx = 'K1:VIS-ETMX_IP_BLEND_LVDTL_INMON'
chlst_etmx = ChannelList.query_nds2([chname_etmx],host='10.68.10.121',port=8088)
chname_seis = 'K1:PEM-EXV_SEIS_WE_SENSINF_OUTPUT'
chlst_seis = ChannelList.query_nds2([chname_seis],host='10.68.10.121',port=8088)

chlst = chlst_grd + chlst_pdh + chlst_seis
chlst = [ ch.name for ch in chlst]
data = TimeSeriesDict.fetch(chlst,start,end,host='10.68.10.121',port=8088,verbose=True,pad=np.nan)


grd = data['K1:GRD-ALS_PDHX_STATE_N']
seis = data['K1:PEM-EXV_SEIS_WE_SENSINF_OUTPUT']
pdh = data['K1:ALS-PDHX_SLOW_DAQ_OUTPUT']
green_lock = grd == 45*u.ct
seis.override_unit('m/s')
pdh.override_unit(None)
highseis = seis < 1.5*u.um/u.s
segments_highseis = highseis.to_dqflag(round=False)
segments_greenlock = green_lock.to_dqflag(round=True)

from gwpy.plot import Plot
plot = Plot(figsize=(12,10))
ax = plot.gca()
ax.plot(seis,label=text.to_string(seis.name))
from matplotlib.artist import setp
setp(ax.get_xticklabels(), visible=False)
from mpl_toolkits.axes_grid1 import make_axes_locatable
ax1 = make_axes_locatable(ax).append_axes('bottom', '100%', pad=0.1)
ax1.plot(pdh,label=text.to_string(seis.name))
ax.set_ylabel(text.to_string(seis.unit))
ax1.set_ylabel(text.to_string(pdh.unit))
text.default_unit_label(ax.yaxis, seis.unit)
ax.legend()
ax1.legend()
ax.set_xscale('auto-gps')
plot.add_segments_bar(segments_greenlock,label='GreenLock')
plot.add_segments_bar(segments_highseis,label='HighSeis')
plot.savefig('TimeSeries.png')
plot.close()
