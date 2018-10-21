#!/usr/bin/env python
# coding:utf-8
from gwpy.timeseries import TimeSeries
from gwpy.time import tconvert
import nds2
import gwpy
#print gwpy.__file__
#print gwpy.__version__
import nds2
#print nds2.__file__

gps_beg = tconvert('Oct 20 2018 00:00:00').gpsSeconds
gps_end = tconvert('Oct 20 2018 00:10:00').gpsSeconds
ch = "K1:PEM-EXV_SEIS_NS_SENSINF_INMON"
print gps_beg
print gps_end
print type(gps_end)
conn = nds2.connection('10.68.10.121', 8088) # nds0
#print gps_beg
buffers = conn.fetch(gps_beg, gps_end, [ch])

data = TimeSeries.from_nds2_buffer(buffers[0])
print data
#data = TimeSeries.fetch(ch, gps_beg, gps_end, host="k1nds0", port=8088, verbose=True)

#plot = data.plot()
#plot.savefig("hoge.png")


'''
メモ：何故か速いチャンネルのDQしか見れない。OUTMONとかみれない。
Aggにしないとぷろっとできない。


'''
