import os 
import re
import warnings
import numpy as np

from gwpy.frequencyseries import FrequencySeries
from gwpy.timeseries import TimeSeries
from gwpy.spectrogram import Spectrogram

def get_csd_specgram(chname1,chname2,remake=True,fftlength=2**6,overlap=0.0,**kwargs):
    hdf5fname = to_hdf5fname(chname1,chname2)
    if remake:
        if os.path.exists(hdf5fname):
            os.remove(hdf5fname)
        timeseries1 = get_timeseries(chname1,from_nds=False,**kwargs)
        timeseries2 = get_timeseries(chname2,from_nds=False,**kwargs)
        specgram = timeseries1.csd_spectrogram(timeseries2,
                                               stride=fftlength*2,
                                               fftlength=fftlength,
                                               overlap=overlap,
                                               window='hanning',
                                               nproc=2)
        specgram.write(hdf5fname)
        return specgram
    else:
        #warnings.warn('Dont use fftlength option..')
        specgram = Spectrogram.read(hdf5fname)
        return specgram


def get_asd(chname,**kwargs):
    fftlength = kwargs.pop('fftlength',2**7)
    remake = kwargs.pop('remake',False)
    overlap = kwargs.pop('overlap',None)    
    timeseries = get_timeseries(chname,from_nds=False,**kwargs)    
    asd = timeseries.asd(fftlength=fftlength,
                         overlap=overlap,
                         window='hanning')
    return asd

def get_csd(chname1,chname2,**kwargs):
    fftlength = kwargs.pop('fftlength',2**7)
    remake = kwargs.pop('remake',False)
    overlap = kwargs.pop('overlap',None)    
    timeseries1 = get_timeseries(chname1,from_nds=False,**kwargs)
    timeseries2 = get_timeseries(chname2,from_nds=False,**kwargs)    
    csd = timeseries1.csd(timeseries2,
                          fftlength=fftlength,
                          overlap=overlap,
                          window='hanning')
    return csd


def get_coherence(chname1,chname2,**kwargs):
    fftlength = kwargs.pop('fftlength',2**7)
    remake = kwargs.pop('remake',False)
    overlap = kwargs.pop('overlap',None)    
    timeseries1 = get_timeseries(chname1,from_nds=False,**kwargs)
    timeseries2 = get_timeseries(chname2,from_nds=False,**kwargs)    
    coherence = timeseries1.coherence(timeseries2,
                                      fftlength=fftlength,
                                      overlap=overlap,
                                      window='hanning')
    return coherence

    
def get_specgram(*chname,**kwargs):
    fftlength = kwargs.pop('fftlength',2**7)
    remake = kwargs.pop('remake',False)
    overlap = kwargs.pop('overlap',None)
    #print chname
    n = len(chname)
    if n==2:
        chname1,chname2 = chname
        specgram = get_csd_specgram(chname1,chname2,
                                    remake=remake,
                                    overlap=overlap,
                                    fftlength=fftlength,**kwargs)
        return specgram
    elif n==1:
        chname = chname[0]
    else:
        raise ValueError('Wrong chname arguments')

    
    hdf5fname = to_hdf5fname(chname)        
    if remake:
        if os.path.exists(hdf5fname):
            os.remove(hdf5fname)        
        timeseries = get_timeseries(chname,from_nds=False,**kwargs)
        specgram = timeseries.spectrogram(stride=fftlength*2,
                                          fftlength=fftlength,
                                          overlap=overlap,
                                          window='hanning')
        specgram.write(hdf5fname)
        return specgram
    else:
        #warnings.warn('Dont use fftlength option..')
        specgram = Spectrogram.read(hdf5fname)
        return specgram




def get_timeseries(chname,prefix='./data',from_nds=False,**kwargs):
    fname = to_gwffname(chname)
    start = kwargs.pop('start')
    end = kwargs.pop('end')
    if not from_nds and os.path.exists(fname):
        #print('!')
        #print fname
        #exit()
        print('Skip fetch from nds {0}'.format(fname))
        data = TimeSeries.read(fname,chname,start,end,
                                format='gwf.lalframe',
                                verbose=True,
                                pad=np.nan)
        
        return data
    else:
        #print('!')
        #exit()
        data = TimeSeries.fetch(chname, start, end,
                                verbose=True,
                                host='10.68.10.121', port=8088,
                                pad=np.nan,
                                verify=True,type=1,dtype=np.float32)
        data.write(fname,format='gwf.lalframe')
        print('wrote data in '+fname)
        return data




def to_gwffname(chname,prefix='./data/'):
    print(chname)
    #m = re.search(r'K1:PEM-(.*)_SENSINF_IN1_DQ',chname)
    m = re.search(r'K1:PEM-(.*)_OUT_DQ',chname)    
    try:
        fname = prefix + m.group(1).lower() + '.gwf'
    except Exception as e:
        print e
        exit()
    return fname


def to_hdf5fname(*args,**kwargs):
    prefix = kwargs.pop('prefix','./data/')
    N = len(args)
    if N==2:
        chname1,chname2 = args
        #m1 = re.search(r'K1:PEM-(.*)_SENSINF_IN1_DQ',chname1)
        #m2 = re.search(r'K1:PEM-(.*)_SENSINF_IN1_DQ',chname2)
        m1 = re.search(r'K1:PEM-(.*)_OUT_DQ',chname1)
        m2 = re.search(r'K1:PEM-(.*)_OUT_DQ',chname2)        
        fname = prefix + m1.group(1).lower() + '-' + m2.group(1).lower() + '.hdf5'
    elif N==1:
        chname = args[0]
        #m = re.search(r'K1:PEM-(.*)_SENSINF_IN1_DQ',chname)
        m = re.search(r'K1:PEM-(.*)_OUT_DQ',chname)        
        try:
            fname = prefix + m.group(1).lower() + '.hdf5'
        except Exception as e:
            print e
    return fname
    


def to_pngfname(chname,ftype,prefix='./'):
    if not chname:
        return  'None.png'
    
    #m = re.search(r'K1:PEM-(.*)_SENSINF_IN1_DQ',chname) old
    m = re.search(r'K1:PEM-(.*)_OUT_DQ',chname)
    try:
        fname = prefix + ftype + '_' + m.group(1).lower() + '.png'
    except Exception as e:
        print e
        exit()
    return fname
