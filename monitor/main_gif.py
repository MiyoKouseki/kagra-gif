
import numpy
from miyopy.gif import findfiles
from gwpy.timeseries import TimeSeries
from gwpy.frequencyseries import FrequencySeries
from gwpy.time import tconvert
from gwpy.plot import Plot

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

if __name__=='__main__':
    #start = tconvert('Apr 24 2019 00:00:00 JST') # After Replacement (a)
    #end = tconvert('Apr 24 2019 01:00:00 JST') # After replacement (a)
    start = tconvert('Apr 25 2019 10:00:00 JST') # After Replacement (a)
    end = tconvert('Apr 25 2019 11:30:00 JST') # After replacement (a)
    start = tconvert('Apr 25 2019 15:00:00 JST') # After Replacement (a)
    end = tconvert('Apr 25 2019 16:30:00 JST') # After replacement (a)        
    chname = 'CALC_STRAIN'
    segments = findfiles(start,end,chname,prefix='/Users/miyo/KagraData/gif')
    source = [path for files in segments for path in files]    
    strain = TimeSeries.read(source=source,
                           name=chname,
                           format='gif',
                           pad=numpy.nan,
                               nproc=1)
    strain = strain*3000#*2 # 2 ????
    strain16 = strain.resample(16,ftype='fir',n=60)        
    ixv = TimeSeries.fetch('K1:PEM-SEIS_IXV_GND_X_OUT_DQ',start,end,
                            host='10.68.10.121',port=8088)
    ixv = ixv*1e-6
    
    exv = TimeSeries.fetch('K1:PEM-SEIS_EXV_GND_X_OUT_DQ',start,end,
                            host='10.68.10.121',port=8088)
    exv = exv*1e-6

    st = TimeSeries.fetch('K1:GIF-X_STRAIN_OUT16',start,end,
                            host='10.68.10.121',port=8088)
    st.override_unit(strain.unit)
    st = st*3000
    diff = ixv - exv
    diff = diff
    sg = ixv.spectrogram2(fftlength=300, overlap=150, window='hanning') ** (1/2.)
    asd_ixv = sg.percentile(50)
    sg = exv.spectrogram2(fftlength=300, overlap=150, window='hanning') ** (1/2.)
    asd_exv = sg.percentile(50)
    sg = diff.spectrogram2(fftlength=300, overlap=150, window='hanning') ** (1/2.)
    asd_diff = sg.percentile(50)
    freq = asd_diff.frequencies
    asd_diff = asd_diff/(2.0*numpy.pi*freq.value)
    sg = strain.spectrogram2(fftlength=300, overlap=150, window='hanning') ** (1/2.)
    asd_strain = sg.percentile(50)
    sg = st.spectrogram2(fftlength=300, overlap=150, window='hanning') ** (1/2.)
    asd_st = sg.percentile(50)
    from miyopy.utils import trillium
    tr = trillium.Trillium('120QA')
    asd_diff = trillium._v2vel(tr,asd_diff)

    if False:
        strain = strain.crop(strain.t0.value,strain.t0.value+600)
        strain16 = strain16.crop(strain16.t0.value,strain16.t0.value+600)        
        st = st.crop(st.t0.value,st.t0.value+600)
        strain = strain - strain.mean()
        strain16 = strain16 - strain16.mean()
        st = st - st.mean()
        from gwpy.signal import filter_design
        bp = filter_design.bandpass(0.1, 0.3, strain16.sample_rate)
        strain16 = strain16.filter(bp, filtfilt=True)        
        st = st.filter(bp, filtfilt=True)
        # -----------------
        # Comparison of DAQ
        # -----------------
        plot = Plot(strain16,ylim=(-2e-7,2e-7))        
        ax = plot.gca()
        ax.plot(st,alpha=0.7)
        ax.set_title('Comparizon of DAQ around micro-seismic band')
        ax.set_ylabel('Strain')
        ax.legend(['0.1-0.3Hz BandPassed GIF DAQ (16Hz resampled from 200Hz)','0.1-0.3Hz BandPassed KAGRA DAQ (16Hz)'])
        plot.savefig('img_comparison_of_DAQ.png')
        plot.close()
        # --------
        # Residual
        # --------
        res = strain16 - st
        plot = Plot(res,
                    xlim=(strain.t0.value,strain.t0.value+600),
                    ylim=(-2.0e-7,2.0e-7)
                    )
        ax = plot.gca()
        ax.set_title('Residual')
        ax.set_ylabel('Strain')
        ax.legend(['GIF DAQ - KAGRA DAQ'])
        plot.savefig('img_comparison_of_DAQ_residual.png')        
        
    
    if True:
        #
        # ASD
        # 
        from gwpy.plot import Plot        
        plot = Plot()
        ax = plot.gca(xscale='log', xlim=(0.01, 2),
                    xlabel='Frequency [Hz]',
                    yscale='log', ylim=(1e-10, 1e-5),
                    ylabel=r'Displacement [m/$\sqrt{\mathrm{Hz}}$]')
        #ax.plot(asd_ixv, color='gwpy:ligo-hanford')
        #ax.plot(asd_exv, color='gwpy:ligo-livingston')
        ax.set_title('Length changes in the 3000 m X arm',fontsize=20)
        ax.plot(asd_diff, color='gwpy:ligo-livingston',label='Seismometer')
        ax.plot(asd_strain, color='gwpy:ligo-hanford',label='Strain-meter (GIF DAQ)')
        ax.plot(asd_st, color='k',label='Strain-meter (KAGRA DAQ)')        
        ax.legend()
        plot.savefig('img_comparison_of_DAQ_asd.png')
    
