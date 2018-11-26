import os 
import re
import warnings
import numpy as np

from gwpy.frequencyseries import FrequencySeries
from gwpy.timeseries import TimeSeries
from gwpy.spectrogram import Spectrogram

def get_csd_specgram(chname1,chname2,remake=True,fftlength=2**6,**kwargs):
    hdf5fname = to_hdf5fname(chname1,chname2)
    if remake:
        if os.path.exists(hdf5fname):
            os.remove(hdf5fname)
        timeseries1 = get_timeseries(chname1,from_nds=False,**kwargs)
        timeseries2 = get_timeseries(chname2,from_nds=False,**kwargs)
        specgram = timeseries1.csd_spectrogram(timeseries2,
                                               stride=fftlength,
                                               fftlength=fftlength,
                                               overlap=0,
                                               window='hanning',
                                               nproc=2)
        specgram.write(hdf5fname)
        return specgram
    else:
        warnings.warn('Dont use fftlength option..')
        specgram = Spectrogram.read(hdf5fname)
        return specgram


def get_specgram(chname,remake=False,fftlength=2**6,**kwargs):
    hdf5fname = to_hdf5fname(chname)

    if remake:
        if os.path.exists(hdf5fname):
            os.remove(hdf5fname)            
        timeseries = get_timeseries(chname,from_nds=False,**kwargs)
        specgram = timeseries.spectrogram(stride=fftlength,
                                          fftlength=fftlength,
                                          overlap=0,
                                          window='hanning')
        specgram.write(hdf5fname)
        return specgram
    else:
        warnings.warn('Dont use fftlength option..')
        specgram = Spectrogram.read(hdf5fname)
        return specgram




def get_timeseries(chname,prefix='./',from_nds=False,**kwargs):    
    fname = to_gwffname(chname)
    start = kwargs.pop('start')
    end = kwargs.pop('end')    
    if not from_nds and os.path.exists(fname):
        print('Skip fetch from nds {0}'.format(fname))
        data = TimeSeries.read(fname,chname,start,end,
                                format='gwf.lalframe',
                                verbose=True,
                                pad=np.nan)
        
        return data
    else:
        data = TimeSeries.fetch(chname, start, end,
                                verbose=True,
                                host='10.68.10.121', port=8088,
                                pad=np.nan,
                                verify=True,type=1,dtype=np.float32)
        data.write(fname,format='gwf.lalframe')
        print('wrote data in '+fname)
        return data







def to_gwffname(chname,prefix='./'):
    print(chname)
    m = re.search(r'K1:PEM-(.*)_SENSINF_(.*)',chname)
    try:
        fname = prefix + m.group(1).lower() + '.gwf'
    except Exception as e:
        print e
        exit()
    return fname


def to_hdf5fname(*args,**kwargs):
    prefix = kwargs.pop('prefix','./')
    N = len(args)
    if N==2:
        chname1,chname2 = args
        m1 = re.search(r'K1:PEM-(.*)_SENSINF_(.*)',chname1)
        m2 = re.search(r'K1:PEM-(.*)_SENSINF_(.*)',chname2)
        fname = prefix + m1.group(1).lower() + '-' + m2.group(1).lower() + '.hdf5'
    elif N==1:
        chname = args[0]
        m = re.search(r'K1:PEM-(.*)_SENSINF_(.*)',chname)
        try:
            fname = prefix + m.group(1).lower() + '.hdf5'
        except Exception as e:
            print e
    return fname
    


def to_pngfname(chname,ftype,prefix='./'):
    if not chname:
        return  'None.png'
    
    m = re.search(r'K1:PEM-(.*)_SENSINF_(.*)',chname)
    try:
        fname = prefix + ftype + '_' + m.group(1).lower() + '.png'
    except Exception as e:
        print e
        exit()
    return fname
