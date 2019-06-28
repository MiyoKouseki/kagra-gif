#
#! coding:utf-8
__author__ = 'Koseki Miyo'

import logger
log = logger.Logger('main')

from gwpy.segments import SegmentList

from plot import plot_timeseries,plot_segmentlist,plot_averaged_asd
from utils import allsegmentlist,save_timeseriesdict,check_badsegment,save_spectrogram,save_longterm_spectrogram

''' Seismic Noise

'''

            
if __name__ == "__main__":
    import warnings
    warnings.filterwarnings('ignore')
    
    # ----------------------------------------    
    # Setting                                  
    # ----------------------------------------    
    from gwpy.time import tconvert
    start = int(tconvert("Jun 01 2018 00:00:00 JST"))
    end = int(tconvert("Jun 02 2019 00:00:00 JST"))
    #end = int(tconvert("Jun 2 2018 00:00:00 JST"))
    nproc = 8
    trend = 'full'
    save_all_timeseries = True
    check_bad_segments = True
    save_spectrogram_data = True
    # ----------------------------------------
    log.info('Saving all timeseries as gwf')  
    # ----------------------------------------
    prefix = './data'
    base = allsegmentlist(start,end)
    if save_all_timeseries:
        good,nodata = save_timeseriesdict(base,nds=False,trend='full',nproc=nproc,prefix=prefix)
        good.write('good.txt')
        nodata.write('nodata.txt')
    else:
        good = SegmentList.read('good.txt')
        nodata = SegmentList.read('nodata.txt')

    # ----------------------------------------    
    log.info('Checking bad segments')
    # ----------------------------------------    
    if check_bad_segments:
        good,bad,eq = check_badsegment(good,trend='full',nproc=nproc,prefix=prefix)
        good.write('good.txt')    
        bad.write('bad.txt')    
        eq.write('eq.txt')
    else:
        good = SegmentList.read('good.txt')
        bad = SegmentList.read('bad.txt')
        eq = SegmentList.read('eq.txt')
    fmt = '{0} \t - {1}\t - {2}\t - {3} \t= {4}'
    log.debug(fmt.format('All','None','Lack','EQ','Good'))
    log.debug(fmt.format(len(base),len(nodata),len(bad),len(eq),len(good)))
    if not (len(base)-len(nodata)-len(bad)-len(eq)==len(good)):
        log.debug('SegmentListError!')
        raise ValueError('!')
    plot_segmentlist(base,nodata,bad,eq,good,start,end,fname=prefix+'/segment.png')

    # ----------------------------------------    
    log.info('Saving spectrogram data as hdf5')
    # ----------------------------------------        
    if save_spectrogram_data:
        save_spectrogram(good,nproc=nproc,prefix=prefix)

    # ----------------------------------------    
    log.info('Calculate averaged ASD')
    # ----------------------------------------            
    save_longterm_spectrogram('X',good,prefix=prefix)
    save_longterm_spectrogram('Y',good,prefix=prefix)
    save_longterm_spectrogram('Z',good,prefix=prefix)


    log.debug('Finish!')
