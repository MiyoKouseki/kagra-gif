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
from utils import allsegmentlist,random_segments,read_segmentlist
from utils import check_nodata,check_badsegment
from utils import save_spectrogram, save_longterm_spectrogram, save_asd


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
    kwargs = {'write':True, 'write_gwf':False, 'nproc':8, 
              'skip':skip_check,'prefix':'./data'}

    
    log.info('Take segmentlists')
    if test:
        base = random_segments(start,end,nseg=30,**kwargs)
    else:
        base = allsegmentlist(start,end,**kwargs)


    log.info('Check segments')
    if skip_check:
        log.info('Skip chekking')
        available,nodata,bad,eq = read_segmentlist(prefix='./segmentlist')
        log.info('Plot segment.png')
        plot_segmentlist(base,nodata,bad,eq,available,start,end,**kwargs)
    else:
        log.info('Chekking..')
        kwargs['skip'] = False
        kwargs['check'] = False
        available,nodata = check_nodata(base,**kwargs)
        available,bad,eq = check_badsegment(available,**kwargs)
        log.info('Checking have done. Close.')
        exit()

    if False:
        log.info('Saving spectrogram2')
        kwargs.pop('write_gwf')
        kwargs['skip'] = False
        save_spectrogram(available,fftlength=100,overlap=50,**kwargs)
        log.info('Calculate averaged ASD')
        save_longterm_spectrogram('X',available,**kwargs)
        save_longterm_spectrogram('Y',available,**kwargs)
        save_longterm_spectrogram('Z',available,**kwargs)

    log.info('Calculate percentile.')
    for axis in ['X','Y','Z']:
        for pctl in [5,10,50,90,95]:
            save_asd(axis,available,percentile=pctl,**kwargs)

    log.debug('Finish!')
    
