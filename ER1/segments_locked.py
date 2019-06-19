#
#! coding:utf-8
import numpy as np

from astropy import units as u

from gwpy.timeseries import TimeSeriesDict,TimeSeries
from gwpy.segments import SegmentList
from gwpy.time import tconvert


''' Get segment list ordered in segment volume from specified time.

指定された期間内に条件を満たすセグメントのリストをつくり、セグメントの大きさでソートするスクリプト。

'''
def myprint(segmentlist):
    print '# No.: Start GPS, End GPS, Duration'
    for i,sgmt in enumerate(segmentlist):
        print '{0:02d}: {1:.4f}, {2:.4f}, {3}'.format(i,sgmt.start,sgmt.end, sgmt.end-sgmt.start)


start = 'Jun 8 2019 12:00 JST'
end = 'Jun 8 2019 18:00 JST'


def locked():
    lockstate = TimeSeries.fetch('K1:GRD-LSC_LOCK_OK',start,end,host='10.68.10.121',port=8088,pad=np.nan)
    fs = (1./lockstate.dt).value
    locked = (lockstate == 1.0*u.V).to_dqflag(round=False,minlen=2**10*fs) # *1
    ok = locked.active
    ok = SegmentList(sorted(ok,key=lambda x:x.end-x.start,reverse=True)) # *2
    myprint(ok)
    ok.write('segments_locked.txt')
    print('Finished segments_locked.txt')


# [注意]
# *1, なんでVolt?
# *2, SegmentList.sort()が効かない。わざわざsorted()してSegmentListに変換している。原因はGwpyの SegmentList の中身である K.Kipp の ligo-segment にあるが、Cで書かれているので良くわからない。とりあえず諦めることにする。ちなみに ligo-segment のURLはここ; https://git.ligo.org/lscsoft/ligo-segments 。



if __name__ == '__main__':
    locked()
