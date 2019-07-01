#
#! coding:utf-8
__author__ = 'Koseki Miyo'

import warnings
warnings.filterwarnings('ignore')

import logger
log = logger.Logger('main')

from gwpy.segments import SegmentList
from gwpy.time import tconvert

from plot import plot_timeseries,plot_segmentlist,plot_averaged_asd
from utils import allsegmentlist,check_nodata,check_badsegment,save_spectrogram,save_longterm_spectrogram,random_segments,read_segmentlist

''' Seismic Noise

'''

            
if __name__ == "__main__":    
    log.info('# --------------------')
    log.info('# Start SeismicNoise')
    log.info('# --------------------')
    log.info('Define Setup')
    start = int(tconvert("Jun 01 2018 00:00:00 JST"))
    end   = int(tconvert("Jun 02 2019 00:00:00 JST"))
    test = False
    skip_check = True
    save_spectrogram_data = True
    kwargs = {'write':True, 'write_gwf':False, 'nproc':8, 'skip':skip_check}
    
    log.info('Take segmentlists')
    if test:
        kwargs['prefix'] = './data'
        base = random_segments(start,end,nseg=30,**kwargs)
    else:
        #end   = int(tconvert("Jul 01 2018 00:00:00 JST"))
        kwargs['prefix'] = './data'
        base = allsegmentlist(start,end,**kwargs)


    log.info('Check segments')
    if skip_check:
        log.info('Skip chekking')
        good,nodata,bad,eq = read_segmentlist(prefix='./segmentlist')
        log.info('Plot segment.png')
        plot_segmentlist(base,nodata,bad,eq,good,start,end,**kwargs)
    else:
        log.info('Chekking..')
        kwargs['skip'] = False
        kwargs['check'] = False
        good,nodata = check_nodata(base,**kwargs)
        good,bad,eq = check_badsegment(good,**kwargs)
        log.info('Checking have done. Close.')
        exit()


    log.info('Saving spectrogram2')
    if save_spectrogram_data:
        save_spectrogram(good,**kwargs)
        

    log.info('Calculate averaged ASD')
    save_longterm_spectrogram('X',good,**kwargs)
    save_longterm_spectrogram('Y',good,**kwargs)
    save_longterm_spectrogram('Z',good,**kwargs)


    log.debug('Finish!')
