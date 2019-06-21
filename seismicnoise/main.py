#
#! coding:utf-8
import os
from numpy.random import rand
import numpy as np

import subprocess
from gwpy.segments import Segment,SegmentList,DataQualityFlag
from gwpy.time import tconvert
from gwpy.timeseries import TimeSeries,TimeSeriesDict

def fw_segments(fw_name='fw0',scp=False):
    ''' FrameWriterにデータが書き込まれている期間のセグメントを返す関数

    書き込まれているかどうかは、T.Yamamoto のスクリプトが自動で"fw0-latest.txt" に生成している。なのでそれを適当に整形したのちGwpyのセグメントリストとして吐き出すようにしている。

    Parameters
    ----------
    fw_name : `str`, optional
        Name of the frame writer. KAGRA have a fw0 (default) an fw1.     
    scp : `str`, optional
        If download from control machine, please choose True. In default, False.

    Returns
    -------
    ok : `gwpy.segments.SegmentList`
        SegmentList whihch only contain segments when fw has write data on main strage.
    '''
    if scp:
        download = subprocess.call('scp k1ctr7:/users/DGS/Frame/{0}-latest.txt ./ '.\
                                   format(fw_name), shell=True)
    make_tmp_txt = subprocess.call("less ./{0}-latest.txt".format(fw_name) + \
                                    " | awk '{if ($4>86400) print $1 , $2}' > " + \
                                    "tmp_{0}.txt".format(fw_name),shell=True)
    ok = SegmentList.read('tmp_{0}.txt'.format(fw_name))
    remove_tmp_txt = subprocess.call("rm tmp_{0}.txt".format(fw_name), shell=True)
    return ok


def random_segments(start,end,tlen=3600,n=200,seed=3434,
                    check_fw=True,write=True):
    ''' ランダムにセグメントをとってくる。
    
    Parameters
    ----------
    start : `float`
        start time
    end : `float`
        end time
    n : `int`, optional
        number of segments
    seed : `int`, optional
        seed. 3434 is a default value.
    tlen : `int`, optional
        duration. default is 3600 seconds.    

    Returns
    -------
    good : `gwpy.segments.SegmentList`
        SegmentList which 
    '''
    np.random.seed(seed=seed)        
    duration = end - start
    _start = start*np.ones(n) + duration*rand(n)
    _end = _start + tlen
    random = SegmentList(map(Segment,zip(_start,_end)))
    if write:
        random.write('random.txt')
        print('saved random.txt')
    return random

def path_to_gwf(start,end,trend='minute'):
    ''' フレームファイルの
    '''
    sources = []
    basedir = {'full':'/data/full/',
              'minute':'/data/trend/minute',
              'second':'/data/trend/second',}
    for i in range(int(start[0:5]),int(end[0:5])+1):
        dir = basedir[trend] + str(i) + '/*'
        source = glob.glob(dir)
        sources.extend(source)        
    sources.sort()    
    removelist = []    
    for x in sources:
        if int(x[32:42])<(int(gpsstart)-3599):
            removelist.append(x)
        if int(x[32:42])>int(gpsend):
            removelist.append(x)            
    for y in removelist:
        sources.remove(y)
    

def save_gwf(segmentlist,chname,nds=True,trend='minute',stype='rms'):
    ''' 
    
    '''
    print('save gwf files')
    if nds and (trend=='minute') and (stype=='rms'):
        for i,segment in enumerate(segmentlist):
            start,end = segment
            fname = './data/mtrend_rms_{0}_{1}.gwf'.format(int(start),int(end))
            if os.path.exists(fname):
                pass
            else:
                data = TimeSeriesDict.fetch(chname,start,end,
                                            host='10.68.10.122',
                                            port=8088,verbose=False,
                                            pad=0.0)
                assert None not in [d.name for d in data.values()], 'not exit!'
                data.write(fname,format='gwf.lalframe')
                print '{0:03d}/{1:03d}'.format(i,len(segmentlist)),fname            
    elif not nds (trend=='minute') and (stype=='rms'):
        from Kozapy.script.mylib import mylib
        for i,segment in enumerate(segmentlist):
            start,end = segment
            fname = './data/mtrend_rms_{0}_{1}.gwf'.format(int(start),int(end))
            if os.path.exists(fname):
                pass
            else:
                sources = mylib.GetFilelist(start,end)
                data = TimeSeriesDict.read(sources,chname,format='gwf.lalframe',
                                           start=start,end=end)
                assert None not in [d.name for d in data.values()], 'not exit!'
                data.write(fname,format='gwf.lalframe')
                print '{0:03d}/{1:03d}'.format(i,len(segmentlist)),fname
    else:
        raise('!')
    

def check_badsegment(segmentlist,chname,plot=True):
    '''
    '''
    print('check bad segments')
    bad = SegmentList()
    chname = [ch.split(',')[0] for ch in chname]
    for i,segment in enumerate(segmentlist):
        start,end = segment
        fname = './data/mtrend_rms_{0}_{1}.gwf'.format(int(start),int(end))       
        data = TimeSeriesDict.read(fname,chname,nproc=2,verbose=False)
        label = [d.replace('_','\_') for d in data]
        fname_img = './data/img_100M_300M_{0}_{1}.png'.format(int(start),int(end))
        nodata = True in [0.0 in d.value for d in data.values()]
        bigeq = True in [0.5 < d.diff().abs().max().value for d in data.values()]
        flag = nodata or bigeq
        print '1, {0:03d}/{1:03d}'.format(i,len(segmentlist)),fname_img,nodata,bigeq
        if plot:
            plot = data.plot(ylabel='Velocity [um/sec]',epoch=start,
                             ylim=(0,1),title='BLRMS\_100M\_300M')
            ax = plot.gca()
            ax.plot(data.values()[0].diff().abs(),'k--')
            ax.plot(data.values()[1].diff().abs(),'r--')
            ax.plot(data.values()[2].diff().abs(),'b--')
            ax.legend(label + ['X Diffs','Y Diffs','Z Diffs'])
            if flag:
                ax.axvspan(start, end, alpha=0.5, color='red')
                bad.append(segment)
            plot.savefig(fname_img)
            plot.close()
    segmentlist -= bad
    bad.write('baddata.txt')
    return segmentlist

        
if __name__ == "__main__":
    import warnings
    warnings.filterwarnings('ignore')

    start = int(tconvert("Feb 01 2019 00:00:00 JST"))
    end = int(tconvert("Jun 01 2019 00:00:00 JST"))

    chname = [
        'K1:PEM-SEIS_EXV_GND_X_OUT16.rms,m-trend',        
        'K1:PEM-SEIS_EXV_GND_X_BLRMS_30M_100M_OUT16.rms,m-trend',
        'K1:PEM-SEIS_EXV_GND_X_BLRMS_100M_300M_OUT16.rms,m-trend',
        'K1:PEM-SEIS_EXV_GND_X_BLRMS_300M_1_OUT16.rms,m-trend',
        'K1:PEM-SEIS_EXV_GND_Y_OUT16.rms,m-trend',                
        'K1:PEM-SEIS_EXV_GND_Y_BLRMS_30M_100M_OUT16.rms,m-trend',
        'K1:PEM-SEIS_EXV_GND_Y_BLRMS_100M_300M_OUT16.rms,m-trend',
        'K1:PEM-SEIS_EXV_GND_Y_BLRMS_300M_1_OUT16.rms,m-trend',
        'K1:PEM-SEIS_EXV_GND_Z_OUT16.rms,m-trend',                
        'K1:PEM-SEIS_EXV_GND_Z_BLRMS_30M_100M_OUT16.rms,m-trend',
        'K1:PEM-SEIS_EXV_GND_Z_BLRMS_100M_300M_OUT16.rms,m-trend',
        'K1:PEM-SEIS_EXV_GND_Z_BLRMS_300M_1_OUT16.rms,m-trend',        
        ]
    chname = [
        'K1:PEM-SEIS_EXV_GND_X_BLRMS_100M_300M_OUT16.rms,m-trend',
        'K1:PEM-SEIS_EXV_GND_Y_BLRMS_100M_300M_OUT16.rms,m-trend',
        'K1:PEM-SEIS_EXV_GND_Z_BLRMS_100M_300M_OUT16.rms,m-trend',
        ]                
    data_segment = random_segments(start,end,tlen=3600,n=10,write=False)
    save_gwf(data_segment,chname,nds=False)
    data_segment = check_badsegment(data_segment,chname)
    data_segment.write('random_segment.txt')
    exit()
