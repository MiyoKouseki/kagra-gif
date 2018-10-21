#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gwpy.timeseries import TimeSeries
from gwpy.time import tconvert
##########################

f_low  = 1
f_high = 20
gps_beg = tconvert('Oct 19 2018 08:00:0')
gps_end = tconvert('Oct 20 2018 08:10:0')
#gps_beg = 1223860112
#gps_end = 1223861112
ch      = "K1:VIS-PR3_TM_OPLEV_TILT_SUM_OUT_DQ"
#ch      = "K1:PEM-EXV_SEIS_NS_SENSINF_OUT_DQ"
##########################

print("gps_beg = ", gps_beg)
print("gps_end = ", gps_end)

data = TimeSeries.fetch(ch, gps_beg, gps_end, host="k1nds0", port=8088, verbose=True)
data_filtered = data.lowpass(f_high).highpass(f_low)
data_RMS = data_filtered.rms(1)
#plot = data_RMS.plot( title=ch, ylabel="Band-limited RMS" )
plot = data_RMS.plot()
plot.show()
plot.savefig("hoge.png")
