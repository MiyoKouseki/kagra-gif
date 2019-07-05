#
#! coding:utf-8
__author__ = 'Koseki Miyo'

import warnings
warnings.filterwarnings('ignore')

from gwpy.segments import SegmentList
from gwpy.time import tconvert

from lib.plot import plot_timeseries,plot_segmentlist,plot_averaged_asd
from lib.segment import divide_segmentlist,random_segments,read_segmentlist
from lib.utils import save_spectrogram, save_longterm_spectrogram, save_asd

import lib.logger
log = lib.logger.Logger('main')


''' Seismic Noise

'''

            
if __name__ == "__main__":
    log.info('# ------------------------------')
    log.info('# Start SeismicNoise            ')
    log.info('# ------------------------------')
    start = 1211817600 # 2018-05-31T15:59:42 UCT 
    end   = 1245372032 # 2019-06-24T00:40:14 UTC (end = start+2**25)
    kwargs = {'nproc':28, 'prefix':'./data'}
    
    log.info('Get Segments')
    #total = random_segments(start,end,nseg=6000,write=True,**kwargs)
    total = divide_segmentlist(start,end,bins=4096,**kwargs)
    #total = divide_into_bins(start,end,bins=4096,**kwargs)

    log.info('Check Segments')
    good,none,lack,glitch = read_segmentlist(total,skip=True,**kwargs)
    fmt = '{0} \t - {1}\t - {2}\t - {3} \t = {4}'
    log.info(fmt.format('All','NoData','LackOfData','Glitch','Available'))
    log.info(fmt.format(len(total),len(none),len(lack),len(glitch),len(good)))
    log.info('Plot Segments')
    plot_segmentlist(total,none,lack,glitch,good,start,end,**kwargs)    
    #exit()
    
    save_spectrogram(good,fftlength=2**10,overlap=2**9,**kwargs)

    log.info('Calculate Percentile')
    for axis in ['X','Y','Z']:
        for pctl in [5,10,50,90,95]:
            save_asd(axis,good,percentile=pctl,**kwargs)

    log.debug('Finish!')
    
