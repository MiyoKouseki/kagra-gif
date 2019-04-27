
import numpy
from miyopy.gif import findfiles
from gwpy.timeseries import TimeSeries
from gwpy.frequencyseries import FrequencySeries
from gwpy.time import tconvert
from gwpy.plot import Plot

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__=='__main__':
    #start = tconvert('Apr 23 2019 00:00:00 JST') # Before Replacement (b)
    #end = tconvert('Apr 23 2019 00:01:00 JST') # Before replacement (b) 
    start = tconvert('Apr 24 2019 00:00:00 JST') # After Replacement (a)
    end = tconvert('Apr 24 2019 00:01:00 JST') # After replacement (a)
    #start = tconvert('Apr 24 2019 10:00:00 JST') # After Replacement (a)
    #end = tconvert('Apr 24 2019 10:01:00 JST') # After replacement (a)    
    chname = 'X500_PD_PPOL_50k'
    segments = findfiles(start,end,chname,prefix='/Users/miyo/KagraData/gif')
    source = [path for files in segments for path in files]    
    ppol = TimeSeries.read(source=source,
                           name=chname,
                           format='gif',
                           pad=numpy.nan,
                               nproc=1)
    gif_ppol =  ppol.crop(ppol.t0.value,ppol.t0.value+0.04)
    #gif_ppol = gif_ppol - gif_ppol.mean()  
    
    chname = 'X500_PD_SPOL_50k'
    segments = findfiles(start,end,chname,prefix='/Users/miyo/KagraData/gif')
    source = [path for files in segments for path in files]    
    spol = TimeSeries.read(source=source,
                           name=chname,
                           format='gif',
                           pad=numpy.nan,
                               nproc=1)
    gif_spol =  spol.crop(spol.t0.value,spol.t0.value+0.04)

    ppol = TimeSeries.fetch('K1:GIF-X_PPOL_IN1_DQ',start,start+0.04,
                            host='10.68.10.121',port=8088)
    spol = TimeSeries.fetch('K1:GIF-X_SPOL_IN1_DQ',start,start+0.04,
                            host='10.68.10.121',port=8088)    
    c2V = 10.0/2**15*2
    print c2V
    kagra_spol = spol*c2V
    kagra_ppol = ppol*c2V
    #kagra_spol-kagra_spol.mean()
    
    plot = gif_ppol.plot()
    ax = plot.gca()
    ax.plot(gif_spol)    
    ax.plot(kagra_ppol)
    ax.plot(kagra_spol)    
    ax.legend(['PPOL (GIF)','SPOL (GIF)', 'PPOL (KAGRA)','SPOL (KAGRA)'])
    plot.savefig('hoge.png')

    if True:
        giffft = gif_ppol.average_fft(1, 0.5, window='hamming')
        kagrafft = kagra_ppol.average_fft(1, 0.5, window='hamming')
        
        size = min(giffft.size, kagrafft.size)
        tf = kagrafft[:size] / giffft[:size]
        print tf
        tf.write('ppol_tf_2300.hdf5','hdf5')
        from gwpy.plot import BodePlot
        plot = BodePlot(tf)
        plot.maxes.set_title(r'PPOL GIF $\rightarrow$ PPOL KAGRA transfer function')
        plot.maxes.set_ylim(-55, 50)
        plot.savefig('tf.png')

    if True:
        tf = FrequencySeries.read('ppol_tf_2300.hdf5')
        print tf
        freq = tf.frequencies        
        value = numpy.exp(1j*2.0*numpy.pi*freq.value*-300e-6)
        tf2 = FrequencySeries(value,df=tf.df,f0=tf.f0)
        print tf2        
        from gwpy.plot import BodePlot
        plot = BodePlot(tf,tf2)
        #print type(plot)
        #ax = plot.gca()        
        #plot.plot(tf2)
        plot.maxes.set_title(r'Transfer function \\ PPOL GIF $\rightarrow$ PPOL KAGRA',fontsize=15)
        plot.maxes.set_ylim(-5, 5)
        plot.savefig('tf.png')
        
