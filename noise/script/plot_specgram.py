#
#! coding:utf-8

from gwpy.time import tconvert

from miyopy.files import (get_timeseries,get_specgram,get_csd_specgram,
                          to_gwffname,to_pngfname,to_hdf5fname,
                          get_asd,get_csd,get_coherence)

from miyopy.plot import (plot_asd,plot_coherence,plot_spectrogram)

#from miyopy.utils import trillium    
#from miyopy.calibration import vel2vel


if __name__ == '__main__':    
    start = tconvert('Dec 6 12:00:00 JST')
    fftlength = 2**9
    ave = 256
    overlap = 0.5
    end = start + fftlength*(ave*(1.0-overlap))
    
    kwargs = {}
    kwargs['start'] = start
    kwargs['end'] = end
    kwargs['nds'] = True
    kwargs['replot'] = True
    kwargs['overlap'] = fftlength*overlap
    kwargs['remake'] = True
    kwargs['fftlength'] = fftlength
    kwargs['nproc'] = 2
    kwargs['prefix'] = '../data/Dec06_12h00_2e9/'

    # get data
    chname1 = 'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ'
    chname2 = 'K1:PEM-IXV_GND_TR120QTEST_X_OUT_DQ'
    chname3 = 'K1:PEM-EXV_GND_TR120Q_X_OUT_DQ'
    psd_specgram1 = get_specgram(chname1,**kwargs)
    plot_spectrogram(psd_specgram1,**kwargs)
