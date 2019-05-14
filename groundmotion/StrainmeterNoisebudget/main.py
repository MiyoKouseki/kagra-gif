#
#
import numpy as np
from control import matlab
from gwpy.timeseries import TimeSeriesDict,TimeSeries
from gwpy.frequencyseries import FrequencySeries
from gwpy.time import tconvert

def asd(data,fftlength=512,window='hanning',ovlp=0.5):
    sg = data.spectrogram2(fftlength=fftlength, overlap=fftlength*ovlp, window=window, nproc=nproc) ** (1/2.)
    median = sg.percentile(50)
    low = sg.percentile(5)
    high = sg.percentile(95)
    return median,low,high

# -----------------------------------------------
# Setting
# -----------------------------------------------
chnames = [
    'K1:PEM-SEIS_IXV_GND_X_OUT_DQ',
    'K1:PEM-SEIS_EXV_GND_X_OUT_DQ',
    'K1:GIF-X_STRAIN_OUT16',
    'K1:PEM-WEATHER_IXV_FIELD_PRES_OUT16'    
    ]
start = 'May 03 2019 00:00:00 JST'
end   = 'May 03 2019 06:00:00 JST'

nproc = 2
fftlength = 512
window = 'hanning'
ovlp = 0.5
tlen = tconvert(end)-tconvert(start)
ave = int(tlen/(fftlength/ovlp))
readgwf = True
readhdf5 = False
comparison_ixv1_diff12=True
comparison_diff12_diff13=True
comparison_comm13_diff13=True
comparison_comm12_diff12=True
comparison_seis_gif=True
plot_coherence=True
tplot = True
write = True

# -----------------------------------------------
# TimeSeriese data
# -----------------------------------------------
if readgwf:
    data = TimeSeriesDict.read('2019May03_6hours.gwf',chnames,start,end,
                               format='gwf.lalframe',nproc=nproc)
    ixv1 = data['K1:PEM-SEIS_IXV_GND_X_OUT_DQ']
    exv = data['K1:PEM-SEIS_EXV_GND_X_OUT_DQ']
    gif = data['K1:GIF-X_STRAIN_OUT16']*3e3*1e6
    ixv_press = data['K1:PEM-WEATHER_IXV_FIELD_PRES_OUT16']
    diff13 = (ixv1-exv)/np.sqrt(2)
    comm13 = (ixv1+exv)/np.sqrt(2)
    
if tplot and readgwf:
    plot = data.plot()
    plot.savefig('img_timeseries.png')
    plot.close()

if True:
    x500_press = TimeSeries.read('2019May03_6hours_x500_press.gwf','X500_BARO',start,end)
    x500_press = x500_press
    plot = x500_press.plot(ylabel='Pressure')
    plot.savefig('img_x500_press.png')
    plot.close()

# -----------------------------------------------
# Calc Coherence
# -----------------------------------------------
import matplotlib.pyplot as plt
if plot_coherence and readgwf:
    print('Calc Coherence ')
    coh13 = ixv1.coherence(exv, fftlength, fftlength*ovlp,window=window)
    deg13 = ixv1.csd(exv, fftlength, fftlength/2).angle().rad2deg()
    coh1 = gif.coherence(ixv_press, fftlength, fftlength*ovlp,window=window)
    deg1 = gif.csd(ixv_press, fftlength, fftlength/2).angle().rad2deg()    
    _gif = gif.resample(8)
    coh = _gif.coherence(x500_press, fftlength, fftlength*ovlp,window=window)
    deg = _gif.csd(x500_press, fftlength, fftlength/2).angle().rad2deg()
    df = coh13.df
    fig, [ax1,ax2] = plt.subplots(2,1,figsize=[7, 6],sharex=True)
    plt.subplots_adjust(wspace=0.4, hspace=0.08)
    ax1.plot(coh13,label='IXV1 vs EXV',color='r')
    ax1.plot(coh,label='GIF vs X500 PRESS',color='k')
    ax1.plot(coh1,label='GIF vs IXV PRESS',color='b')
    ax1.set_yscale('linear')
    ax1.set_xscale('log')
    ax1.set_ylabel('Coherence')
    ax1.set_ylim(0,1)
    ax1.grid(True, 'both', 'both')
    ax2.plot(deg13,color='r')
    ax2.plot(deg,color='k')
    ax2.plot(deg1,color='b')
    ax2.set_xlabel('Frequency [Hz]')
    ax2.set_ylabel('Phase [deg]')
    ax2.set_yticklabels(range(-180,181,90))
    ax2.set_ylim(-200,200)
    ax1.set_xlim(1e-3,100)
    ax2.set_xlim(1e-3,100)
    ax1.legend(fontsize=15)
    ax1.set_title('Coherence')
    ax2.text(110, -180, 'START : {0}'.format(start), rotation=90,ha='left',va='bottom')
    ax2.text(150, -180, 'BW : {0:3.2e}, Window : {1}, AVE : {2:3d}'.format(df,window,ave), rotation=90,ha='left',va='bottom')    
    plt.savefig('img_coherence.png')
    

# -----------------------------------------------    
# Calibrated ASD
# -----------------------------------------------
if readhdf5:
    print('Read from hdf5')
    ixv1 = FrequencySeries.read('./fs_ixv1.hdf5',format='hdf5')
    diff13 = FrequencySeries.read('./fs_diff13.hdf5',format='hdf5')
    comm13 = FrequencySeries.read('./fs_comm13.hdf5',format='hdf5')
    tr120_selfnoise = FrequencySeries.read('./fs_selfnoise.hdf5',format='hdf5')
    gif = FrequencySeries.read('./fs_gif.hdf5',format='hdf5')
    #x500_press = FrequencySeries.read('./fs_x500_press.hdf5',format='hdf5')
    df = ixv1.df
else:
    _,ixv1,_ = asd(ixv1,fftlength=fftlength,window='hanning',ovlp=0.5)
    _,gif,_ = asd(gif,fftlength=fftlength,window='hanning',ovlp=0.5)
    _,x500_press,_ = asd(x500_press,fftlength=fftlength,window='hanning',ovlp=0.5)
    _,ixv_press,_ = asd(ixv_press,fftlength=fftlength,window='hanning',ovlp=0.5)
    _,diff13,_ = asd(diff13,fftlength=fftlength,window='hanning',ovlp=0.5)
    _,comm13,_ = asd(comm13,fftlength=fftlength,window='hanning',ovlp=0.5)
    from utils import times,rms,_bode,degwrap,mybode
    from trillium import tr120,tr120_u,tr120_selfnoise
    freq = ixv1.frequencies.value
    mag_tr120_u,phase_tr120_u = mybode(tr120_u,freq=freq,Plot=False)
    mag_integ,phase_integ = mybode(matlab.tf([1],[1,0]),freq=freq,Plot=False)    
    ixv1 = ixv1/mag_tr120_u*mag_integ
    diff13 = diff13/mag_tr120_u*mag_integ
    comm13 = comm13/mag_tr120_u*mag_integ
    tr120_selfnoise = tr120_selfnoise*1e6
    
# -----------------------------------------------    
# write
# -----------------------------------------------
if write and not readhdf5:
    print('Write ')
    ixv1.write('./fs_ixv1.hdf5',format='hdf5',overwrite=True,path='hoge')
    diff13.write('./fs_diff13.hdf5',format='hdf5',overwrite=True,path='hoge')
    comm13.write('./fs_comm13.hdf5',format='hdf5',overwrite=True,path='hoge')
    tr120_selfnoise.write('./fs_selfnoise.hdf5',format='hdf5',overwrite=True,path='hoge')
    gif.write('./fs_gif.hdf5',format='hdf5',overwrite=True,path='hoge')
    x500_press.write('./fs_x500_press.hdf5',format='hdf5',overwrite=True,path='hoge')
    
    
# -----------------------------------------------
#                     Main
# -----------------------------------------------

# -----------------------------------------------
# IXV1 DIFF12
# -----------------------------------------------
if comparison_ixv1_diff12:
    print('Comparison_IXV1_DIFF12')
    from gwpy.plot import Plot
    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(1e-3, 100),
                yscale='log', ylim=(1e-7,1e2))                
    ax.plot(ixv1, color='k',label='IXV1')
    ax.plot(tr120_selfnoise, color='k',label='Selfnoise',linestyle='--',zorder=0)
    ax.set_xlabel('Frequency [Hz]',fontsize=15)
    ax.set_ylabel(r'Displacement [um/$\sqrt{\mathrm{Hz}}$]',fontsize=15)    
    ax.set_title('Trillium120QA Noise Investigation',fontsize=20)
    ax.text(110, 1e-7, 'START : {0}'.format(start), rotation=90,ha='left',va='bottom')
    ax.text(150, 1e-7, 'BW : {0:3.2e}, Window : {1}, AVE : {2:3d}'.format(df,window,ave), rotation=90,ha='left',va='bottom')        
    ax.legend(fontsize=12)
    plot.savefig('img_comparison_ixv1_diff12.png')

# -----------------------------------------------    
# DIFF12 DIFF13
# -----------------------------------------------
if comparison_diff12_diff13:
    from gwpy.plot import Plot
    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(1e-3, 100),yscale='log', ylim=(1e-7,1e2))
    ax.plot(diff13, color='k',label=r'(IXV1 - EXV)/$\sqrt{2}$')
    ax.plot(tr120_selfnoise, color='k',label='selfnoise',linestyle='--')    
    ax.set_xlabel('Frequency [Hz]',fontsize=15)
    ax.set_ylabel(r'Displacement [um/$\sqrt{\mathrm{Hz}}$]',fontsize=15)    
    ax.set_title('Common Mode Reduction',fontsize=20)
    ax.text(110, 1e-7, 'START : {0}'.format(start), rotation=90,ha='left',va='bottom')
    ax.text(150, 1e-7, 'BW : {0:3.2e}, Window : {1}, AVE : {2:3d}'.format(df,window,ave), rotation=90,ha='left',va='bottom')            
    ax.legend(fontsize=12)    
    plot.savefig('img_comparison_diff12_diff13.png')

# -----------------------------------------------    
# COMM13 DIFF13
# -----------------------------------------------
if comparison_comm13_diff13:
    from gwpy.plot import Plot
    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(1e-3, 100),yscale='log', ylim=(1e-7,1e2))
    ax.plot(comm13, color='k',label=r'(IXV1 + EXV)/$\sqrt{2}$')
    ax.plot(diff13, color='r',label=r'(IXV1 - EXV)/$\sqrt{2}$')
    ax.plot(tr120_selfnoise, color='k',label='selfnoise',linestyle='--')    
    ax.set_xlabel('Frequency [Hz]',fontsize=15)
    ax.set_ylabel(r'Displacement [um/$\sqrt{\mathrm{Hz}}$]',fontsize=15)    
    ax.set_title('Common and Differential Motion in Distant Seismometers',fontsize=20)
    ax.text(110, 1e-7, 'START : {0}'.format(start), rotation=90,ha='left',va='bottom')
    ax.text(150, 1e-7, 'BW : {0:3.2e}, Window : {1}, AVE : {2:3d}'.format(df,window,ave), rotation=90,ha='left',va='bottom')                    
    ax.legend(fontsize=12)        
    plot.savefig('img_comparison_comm13_diff13.png')

# -----------------------------------------------    
# COMM12 DIFF12
# -----------------------------------------------
if comparison_comm12_diff12:
    from gwpy.plot import Plot
    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(1e-3, 100), yscale='log', ylim=(1e-7,1e2))
    ax.plot(tr120_selfnoise, color='k',label='selfnoise',linestyle='--')
    ax.set_xlabel('Frequency [Hz]',fontsize=15)
    ax.set_ylabel(r'Displacement [um/$\sqrt{\mathrm{Hz}}$]',fontsize=15)    
    ax.set_title('Common and Differential Motion in Close Seismometers',fontsize=20)    
    ax.legend(fontsize=12)
    ax.text(110, 1e-7, 'START : {0}'.format(start), rotation=90,ha='left',va='bottom')
    ax.text(150, 1e-7, 'BW : {0:3.2e}, Window : {1}, AVE : {2:3d}'.format(df,window,ave), rotation=90,ha='left',va='bottom')                
    plot.savefig('img_comparison_comm12_diff12.png')

# -----------------------------------------------    
# GIF SEISMOMETER
# -----------------------------------------------
if comparison_seis_gif :
    from gwpy.plot import Plot
    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(1e-3, 100), yscale='log')#, ylim=(1e-7,1e2))
    ax.plot(diff13*np.sqrt(2), color='k',label=r'Corner - X End')
    ax.plot(gif, color='r',label=r'GIF',zorder=0)
    ax.plot(x500_press, color='b',label=r'IXV PRESS',zorder=1)
    ax.plot(tr120_selfnoise*np.sqrt(2), color='k',label=r'Seismomter Selfnoise $\times\sqrt{2}$',linestyle='--')
    ax.plot(np.logspace(-4,2,1e4),1e-12*1e6*3e3*np.ones(10000),'r--',label='GIF Noise (Preliminary)')
    ax.set_xlabel('Frequency [Hz]',fontsize=15)
    ax.set_ylabel(r'Displacement [um/$\sqrt{\mathrm{Hz}}$]',fontsize=15)    
    ax.set_title('X-arm Baseline Motion',fontsize=20)    
    ax.legend(fontsize=10)
    ax.text(110, 1e-7, 'START : {0}'.format(start), rotation=90,ha='left',va='bottom')
    ax.text(150, 1e-7, 'BW : {0:3.2e}, Window : {1}, AVE : {2:3d}'.format(df,window,ave), rotation=90,ha='left',va='bottom')                    
    plot.savefig('img_comparison_seis_gif.png')   
