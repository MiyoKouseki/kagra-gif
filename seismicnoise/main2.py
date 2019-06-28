#
#! coding:utf-8
__author__ = 'Koseki Miyo'

import logger
log = logger.Logger('main2')

from plot import plot_timeseries,plot_segmentlist,plot_averaged_asd
from utils import allsegmentlist,save_timeseriesdict,check_badsegment,save_spectrogram,random_segments

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
    nproc = 16
    trend = 'full'
    
    # ----------------------------------------    
    log.info('Saving all timeseries as gwf') 
    # ----------------------------------------
    segnum = 3000
    seed = 3434
    random = random_segments(start,end,tlen=2**12,n=segnum,seed=seed)
    random.write('random.txt')
    base = random
    prefix = './data'
    #base.write('base.txt')
    good,nodata = save_timeseriesdict(base,nds=False,trend='full',nproc=nproc,prefix=prefix)
    #nodata.write('nodata.txt')    
    
    # ----------------------------------------    
    log.info('Checking bad segments')
    # ----------------------------------------    
    good,bad,eq = check_badsegment(good,trend='full',nproc=nproc,prefix=prefix)
    #good.write('good.txt')
    #bad.write('bad.txt')
    #eq.write('eq.txt')
    log.debug('All \t- None \t- Bad \t- EQ  \t= Good')
    log.debug('{0} \t- {1}  \t- {2} \t- {3} \t= {4}'.format(len(base),len(nodata),len(bad),len(eq),len(good)))
    fname = prefix + '/segment.png'
    plot_segmentlist(base,nodata,bad,eq,good,start,end,fname)
    
    # ----------------------------------------    
    log.info('Saving spectrogram data as hdf5')
    # ----------------------------------------        
    save_spectrogram(good,nproc=nproc,prefix=prefix)
    
    # ----------------------------------------    
    log.info('Calculate averaged ASD')
    # ----------------------------------------            
    from gwpy.spectrogram import Spectrogram
    import os
    axis = 'X'
    fname = filter(lambda x: "{0}_".format(axis) in x, os.listdir(prefix))
    fname = map(lambda x:prefix+'/'+x,fname)
    specgrams = Spectrogram.read(fname[0],format='hdf5')
    for fname in fname[1:]:
        specgrams.append(Spectrogram.read(fname,format='hdf5'),gap='ignore')        
    fname_hdf5 = prefix + '/SG_LongTerm_{0}.hdf5'.format(axis)
    specgrams.write(fname_hdf5,format='hdf5',overwrite=True)
    fname = prefix + '/ASD_LongTerm_{0}.png'.format(axis)
    #plot_averaged_asd(specgrams,fname)

    #
    axis = 'Y'
    fname = filter(lambda x: "{0}_".format(axis) in x, os.listdir(prefix))
    fname = map(lambda x:prefix+'/'+x,fname)
    specgrams = Spectrogram.read(fname[0],format='hdf5')
    for fname in fname[1:]:
        specgrams.append(Spectrogram.read(fname,format='hdf5'),gap='ignore')        
    fname_hdf5 = prefix + '/SG_LongTerm_{0}.hdf5'.format(axis)
    specgrams.write(fname_hdf5,format='hdf5',overwrite=True)
    fname = prefix + '/ASD_LongTerm_{0}.png'.format(axis)
    #plot_averaged_asd(specgrams,fname)
    #
    #
    axis = 'Z'
    fname = filter(lambda x: "{0}_".format(axis) in x, os.listdir(prefix))
    fname = map(lambda x:prefix+'/'+x,fname)
    specgrams = Spectrogram.read(fname[0],format='hdf5')
    for fname in fname[1:]:
        specgrams.append(Spectrogram.read(fname,format='hdf5'),gap='ignore')        
    fname_hdf5 = prefix + '/SG_LongTerm_{0}.hdf5'.format(axis)
    specgrams.write(fname_hdf5,format='hdf5',overwrite=True)
    fname = prefix + '/ASD_LongTerm_{0}.png'.format(axis)
    #plot_averaged_asd(specgrams,fname)

    log.info('Finish!')
