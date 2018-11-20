#
#! coding:utf-8
import sys
sys.path.insert(0,'/Users/miyo/Dropbox/Git/gwpy/')
import gwpy
print gwpy.__file__

from gwpy.frequencyseries import FrequencySeries

from gwpy.timeseries import TimeSeries
from gwpy.spectrogram import Spectrogram

from gwpy.time import tconvert
from gwpy.plot import Plot

from _file import (get_timeseries,get_specgram,get_csd_specgram,
                   to_gwffname,to_pngfname,to_hdf5fname)

from _plot import (plot_asd,plot_coherence,plot_spectrogram)                

def plot_coherence_with_scipy(data1,data2,fftlength=2**7,**kwargs):
    data1
    # ちゃんとASDとCSDが計算できているかテストプログラムを書いてから
    #ここにくる。
    exit()


if __name__ == '__main__':
    fmt = 'K1:PEM-{seismometer}_{dof}_SENSINF_IN1_DQ'
    
    start = tconvert('Nov 12 3:0:0') # work finish at 12:00 JST
    # Lack of Data!! 2018-11-12T12:48:14  --- 2018-11-12T12:50:54
    #start = tconvert('Nov 12 14:30:0') # after daq restart
    #start = tconvert('Nov 13 00:30:0') # after lack of data
    start = tconvert('Nov 13 01:00:0') #
    #end = tconvert('Nov 14 0:0:0') #
    fftlength = 2**7
    end = start + fftlength*2**4
    
    chname1 = 'K1:PEM-IXV_SEIS_NS_SENSINF_IN1_DQ'
    chname2 = 'K1:PEM-EXV_SEIS_NS_SENSINF_IN1_DQ'
    chname2 = 'K1:PEM-IXV_SEIS_TEST_NS_SENSINF_IN1_DQ'
    
    kwargs = {}
    kwargs['start'] = start
    kwargs['end'] = end

    timeseries1 = get_timeseries(chname1,remake=True,fftlength=2**6,**kwargs)
    timeseries2 = get_timeseries(chname2,remake=True,fftlength=2**6,**kwargs)    
    specgram1 = get_specgram(chname1,remake=True,fftlength=2**6,**kwargs)
    specgram2 = get_specgram(chname2,remake=True,fftlength=2**6,**kwargs)
    cds_specgram = get_csd_specgram(chname1,chname2,remake=True,
                                    fftlength=2**6,**kwargs)

    print specgram1.unit
    print specgram1.unit
    print cds_specgram.unit
    plot_asd(specgram1,replot=True,**kwargs)
    plot_asd(specgram2,replot=True,**kwargs)
    plot_spectrogram(specgram1,replot=True,**kwargs)
    plot_spectrogram(specgram2,replot=True,**kwargs)
    plot_coherence(cds_specgram,specgram1,specgram2,fftlength=2**7,**kwargs)
    #plot_coherence(chname1,chname2,fftlength=2**7,**kwargs)    
    #plot_coherence_with_scipy(timeseries1,timeseries2,fftlength=2**7,**kwargs)
    
