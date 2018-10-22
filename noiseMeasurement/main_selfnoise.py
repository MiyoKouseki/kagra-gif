#
#! coding:utf-8
import numpy as np

#from miyopy.utils.tips import read
from miyopy.io import read 
from miyopy.signal import coherence,asd
from miyopy.plot import coherenceplot,asdplot
#import matplotlib.pyplot as plt
from miyopy.utils.trillium import H120QA,TRselfnoise
from gwpy.timeseries import TimeSeries

c2V = 10.0/2**15
deGain = 10**(-30.0/20.0)

def coh2snr(coh):
    '''
    
    '''
    _coh2snr = lambda x:  abs(x)/(1.0-abs(x))
    snr = [_coh2snr(_coh) for _coh in coh]
    return np.array(snr)



def sensor_noise(coh12,coh13,asd1,asd2,asd3):
    ''' Estimate the noise level of sensor using Peterson-Method(1980).
    
            
    Parameters
    ----------
    coh12 : numpy.array 
        The coherence between "adjacent two sensors" so that the 
        external noise from local environment is same each other.
    coh13 : numpy.array
        The coherence between "well-separate two sensors" so that the
        external noise from local environment dont have correlation
        earch other.        
    asd1 : numpy.array
       Amplitude spectrum density of the sensor1.
    asd2 : numpy.array
       Amplitude spectrum density of the sensor2.
    asd3 : numpy.array
       Amplitude spectrum density of the sensor3.
    
    Returns
    -------
    asd_x : numpy.array
        The noise existing globally with coherently. This noise could
        be called "signal", because this noise have coherent globally.
    asd_n : numpy.array
        The noise existing globally with incoherently. This noise could 
        be called "self-noise", because this incoherenct noise dont 
        disappear even separated well.
    asd_xb : numpy.array
        The noise existing locally with coherently. This noise is a 
        sum of the signal and local environmental noise.
    '''
    coh13 = np.sqrt(coh13)
    coh12 = np.sqrt(coh12)
    snr13 = coh2snr(coh13)
    snr12 = coh2snr(coh12)
    n12 = asd1*np.sqrt(1.0/(1+snr12))
    s12 = asd1*np.sqrt(1.0/(1+snr12)*snr12)
    s13 = np.sqrt(asd1*asd3*coh13)
    envnoise = s12 - s13
    asd_n = n12
    asd_x = s13
    asd_xb = s12
    return asd_x,asd_n,asd_xb




def huge(t1,t2,t3,start,end,fs,ave=32):
    t1_we,t1_ns,t1_zz = t1
    t2_we,t2_ns,t2_zz = t2
    t3_we,t3_ns,t3_zz = t3
    f_, asd1_we = asd(t1_we,fs,ave=ave)
    f_, asd2_we = asd(t2_we,fs,ave=ave)
    f_, asd3_we = asd(t3_we,fs,ave=ave)    
    asd1_we = asd1_we/H120QA(f_)
    asd2_we = asd2_we/H120QA(f_)
    asd3_we = asd3_we/H120QA(f_)    
    asdplot([[f_,asd1_we],[f_,asd2_we],[f_,asd3_we]],
            legend=['1_we','2_we','3_we'],
            fname='asd')

    
def plot_asd_all(t1,t2,t3,start,end,fs,ave=32):
    #
    t1_we,t1_ns,t1_zz = t1
    t2_we,t2_ns,t2_zz = t2
    t3_we,t3_ns,t3_zz = t3
    f_, asd1_we = asd(t1_we,fs,ave=ave)
    f_, asd2_we = asd(t2_we,fs,ave=ave)
    f_, asd3_we = asd(t3_we,fs,ave=ave)    
    asd1_we = asd1_we/H120QA(f_)
    asd2_we = asd2_we/H120QA(f_)
    asd3_we = asd3_we/H120QA(f_)
    f, coh13_wewe, deg13_wewe = coherence(t1_we,t3_we,fs,ave=ave)
    f, coh12_wewe, deg12_wewe = coherence(t1_we,t2_we,fs,ave=ave)
    #
    asd_x,asd_n,asd_xb = sensor_noise(coh12_wewe,coh13_wewe,
                                      asd1_we,asd2_we,asd3_we)
    #
    snr13_wewe = coh2snr(coh13_wewe)
    snr12_wewe = coh2snr(coh12_wewe)
    asdplot([[f_,snr12_wewe],[f_,snr13_wewe]],
            legend=['1_we','2_we'],
            fname='snr')
    #
    f,_selfnoise = TRselfnoise(acc='velo')    
    asdplot([[f,_selfnoise],[f_,asd_x],[f_,asd_n],[f_,asd_xb]],
            legend=['Self-Noise',
                    '1_we',
                    'x : Coherent Signal b/w 1 and 3 (Global Noise)',
                    'n : Incoherent Signal b/w 1 and 2 (Internal Instrument Noise)',
                    'x+b : Coherent Signal b/w 1 and 2 (Local Noise)',       
                    ],
            linestyle=[':o','-','-','-'],
            ylim=[1e-11,5e-6],
            xlim=[min(f_[1:]),200],
            fname='selfnoise')    

   
    

if __name__ == "__main__":
    tlen = 2**13
    start = 1220194818
    start = 1221922818
    end = start+tlen
    #
    #
    t1_ns = read(start,end,'K1:PEM-IXV_SEIS_NS_SENSINF_IN1_DQ')*c2V
    ch = 'K1:PEM-IXV_SEIS_NS_SENSINF_IN1_DQ'
    t1_ns = TimeSeries.fetch(ch, start, end, host="k1nds0", port=8088)
    exit()
    t1_we = read(start,end,'K1:PEM-IXV_SEIS_WE_SENSINF_IN1_DQ')*c2V
    t1_zz = read(start,end,'K1:PEM-IXV_SEIS_Z_SENSINF_IN1_DQ')*c2V
    t3_ns = read(start,end,'K1:PEM-EXV_SEIS_NS_SENSINF_IN1_DQ')*c2V*deGain
    t3_we = read(start,end,'K1:PEM-EXV_SEIS_WE_SENSINF_IN1_DQ')*c2V*deGain
    t3_zz = read(start,end,'K1:PEM-EXV_SEIS_Z_SENSINF_IN1_DQ')*c2V*deGain
    t2_ns = read(start,end,'K1:PEM-IXV_SEIS_TEST_NS_SENSINF_IN1_DQ')*c2V
    t2_we = read(start,end,'K1:PEM-IXV_SEIS_TEST_WE_SENSINF_IN1_DQ')*c2V
    t2_zz = read(start,end,'K1:PEM-IXV_SEIS_TEST_Z_SENSINF_IN1_DQ')*c2V
    # init
    tlen = end - start
    fs = len(t1_we)/tlen
    ave = 64
    t1 = [t1_we,t1_ns,t1_zz]
    t2 = [t2_we,t2_ns,t2_zz]
    t3 = [t3_we,t3_ns,t3_zz]
    #
    # plot
    huge(t1,t2,t3,start,end,fs,ave=ave)
    plot_asd_all(t1,t2,t3,start,end,fs,ave=ave)
    #plot_sensor_noise(t1,t2,t3,)
    #plot_Coherence_SameAxis(t1,t2,t3,'1_23',start,end,fs,ave)
    #plot_Coherence_SameAxis(t1,t2,t3,'2_13',start,end,fs,ave)
    #plot_Coherence_DifferentAxis(t1,t1,'11',start,end,fs,ave)
    #plot_Coherence_DifferentAxis(t2,t2,'22',start,end,fs,ave)
    #plot_Coherence_DifferentAxis(t3,t3,'33',start,end,fs,ave)    
    #plot_Coherence_DifferentAxis(t1,t2,'12',start,end,fs,ave)
    #plot_Coherence_DifferentAxis(t1,t3,'13',start,end,fs,ave)
    #plot_Coherence_DifferentAxis(t2,t3,'23',start,end,fs,ave)

