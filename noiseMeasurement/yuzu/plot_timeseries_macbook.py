#!/usr/bin/env python
# coding:utf-8
from gwpy.timeseries import TimeSeries
from gwpy.time import tconvert
import gwpy
print gwpy.__file__
print gwpy.__version__
import nds2
print nds2.__file__

gps_beg = tconvert('Oct 01 2018 00:00:00')
gps_end = tconvert('Oct 20 2018 00:00:00')

ch = "K1:PEM-EXV_SEIS_NS_SENSINF_INMON"

data = TimeSeries.fetch(ch, gps_beg, gps_end, host="k1nds0", port=8088, verbose=True)

plot = data.plot()
plot.savefig("hoge.png")


'''
メモ：何故か速いチャンネルのDQしか見れない。OUTMONとかみれない。
Aggにしないとぷろっとできない。


'''
