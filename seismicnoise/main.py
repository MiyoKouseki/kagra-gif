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
    log.info('# ------------------------------')
    log.info('# Start SeismicNoise            ')
    log.info('# ------------------------------')
    start = int(tconvert("Jun 01 2018 00:00:00 JST"))
    end   = int(tconvert("Jun 02 2019 00:00:00 JST"))
    test = False
    skip = True
    kwargs = {'nproc':8, 'prefix':'./data'}
    
    log.info('Get segmentlists')
    if test:
        log.info('Getting random segments')
        total = random_segments(start,end,nseg=30,write=True,**kwargs)
    else:
        log.info('Getting all segments')
        total = allsegmentlist(start,end,write=True,**kwargs)


    log.info('Check segments')    
    available,nodata,lackofdata,glitch = read_segmentlist(total,skip=False)
    fmt = '{0} \t - {1}\t - {2}\t - {3} \t = {4}'
    log.info(fmt.format('All','None','Lack','Glitch','Available'))
    log.info(fmt.format(len(total),len(nodata),len(lackofdata),
                        len(glitch),len(available)))


    log.info('Plot segmentlist')    
    plot_segmentlist(total,nodata,lackofdata,glitch,available,start,end,**kwargs)


    log.info('Calculate percentile.')
    for axis in ['X','Y','Z']:
        for pctl in [5,10,50,90,95]:
            save_asd(axis,available,percentile=pctl,**kwargs)

    log.debug('Finish!')
    
