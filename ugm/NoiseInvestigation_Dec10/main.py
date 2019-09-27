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
    'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ',
    'K1:PEM-IXV_GND_TR120QTEST_X_OUT_DQ',
    'K1:PEM-EXV_GND_TR120Q_X_OUT_DQ',
    ]
start = 'Dec 10 2018 00:00:00 UTC'
end   = 'Dec 10 2018 02:30:00 UTC'    

nproc = 2
fftlength = 512
window = 'hanning'
ovlp = 0.5
tlen = tconvert(end)-tconvert(start)
ave = int(tlen/(fftlength/ovlp))
readgwf = True
readhdf5 = True
readgif = True
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
    data = TimeSeriesDict.read('2019Dec10_3hours.gwf',chnames,start,end,
                               format='gwf.lalframe',nproc=nproc)
    ixv1 = data['K1:PEM-IXV_GND_TR120Q_X_OUT_DQ']*2 # klog8746
    ixv2 = data['K1:PEM-IXV_GND_TR120QTEST_X_OUT_DQ']*2 # klog8746
    exv = data['K1:PEM-EXV_GND_TR120Q_X_OUT_DQ']*2 # klog8746
    diff12 = (ixv1-ixv2)/np.sqrt(2)
    diff13 = (ixv1-exv)/np.sqrt(2)
    comm12 = (ixv1+ixv2)/np.sqrt(2)
    comm13 = (ixv1+exv)/np.sqrt(2)
    
if tplot and readgwf:
    plot = data.plot()
    plot.savefig('img_timeseries.png')
    plot.close()

# -----------------------------------------------
# Calc Coherence
# -----------------------------------------------
import matplotlib.pyplot as plt
if plot_coherence and readgwf:
    coh12 = ixv1.coherence(ixv2, fftlength, fftlength*ovlp,window=window)
    coh13 = ixv1.coherence(exv, fftlength, fftlength*ovlp,window=window)
    deg12 = ixv1.csd(ixv2, fftlength, fftlength/2).angle().rad2deg()
    deg13 = ixv1.csd(exv, fftlength, fftlength/2).angle().rad2deg()
    df = coh12.df
    fig, [ax1,ax2] = plt.subplots(2,1,figsize=[7, 6],sharex=True)
    plt.subplots_adjust(wspace=0.4, hspace=0.08)
    ax1.plot(coh13,label='IXV1 vs EXV',color='r')
    ax1.plot(coh12,label='IXV1 vs IXV2',color='k')
    ax1.set_yscale('linear')
    ax1.set_xscale('log')
    ax1.set_ylabel('Coherence')
    ax1.set_ylim(0,1)
    ax1.grid(True, 'both', 'both')
    ax2.plot(deg13,color='r')
    ax2.plot(deg12,color='k')    
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

if readgif:
    #strain = TimeSeries.read('Dec10_4days_strain.gwf','CALC_STRAIN',start,end)
    strain = TimeSeries.read('2019Dec10_3hours_strain.gwf','CALC_STRAIN',start,end)
    gif = strain*3e3*1e6
    plot = gif.plot(ylabel='Strain')
    plot.savefig('img_gif.png')
    plot.close()
    _,gif,_ = asd(gif,fftlength=fftlength)

# -----------------------------------------------    
# Calibrated ASD
# -----------------------------------------------
if readhdf5:
    print('Read from hdf5')
    ixv1 = FrequencySeries.read('./fs_ixv1.hdf5',format='hdf5')
    exv = FrequencySeries.read('./fs_exv.hdf5',format='hdf5')
    diff12 = FrequencySeries.read('./fs_diff12.hdf5',format='hdf5')
    diff13 = FrequencySeries.read('./fs_diff13.hdf5',format='hdf5')
    comm12 = FrequencySeries.read('./fs_comm12.hdf5',format='hdf5')
    comm13 = FrequencySeries.read('./fs_comm13.hdf5',format='hdf5')
    tr120_selfnoise = FrequencySeries.read('./fs_selfnoise.hdf5',format='hdf5')
    df = ixv1.df    
else:
    _,ixv1,_ = asd(ixv1,fftlength=fftlength)
    _,exv,_ = asd(exv,fftlength=fftlength)
    _,diff12,_ = asd(diff12,fftlength=fftlength,window='hanning',ovlp=0.5)
    _,diff13,_ = asd(diff13,fftlength=fftlength,window='hanning',ovlp=0.5)
    _,comm12,_ = asd(comm12,fftlength=fftlength,window='hanning',ovlp=0.5)
    _,comm13,_ = asd(comm13,fftlength=fftlength,window='hanning',ovlp=0.5)
    from utils import times,rms,_bode,degwrap,mybode
    from trillium import tr120,tr120_u,tr120_selfnoise
    freq = ixv1.frequencies.value
    mag_tr120_u,phase_tr120_u = mybode(tr120_u,freq=freq,Plot=False)
    mag_integ,phase_integ = mybode(matlab.tf([1],[1,0]),freq=freq,Plot=False)    
    ixv1 = ixv1/mag_tr120_u*mag_integ
    diff12 = diff12/mag_tr120_u*mag_integ
    diff13 = diff13/mag_tr120_u*mag_integ
    comm12 = comm12/mag_tr120_u*mag_integ
    comm13 = comm13/mag_tr120_u*mag_integ
    tr120_selfnoise = tr120_selfnoise*1e6

    
# -----------------------------------------------    
# write
# -----------------------------------------------
if write and not readhdf5:
    print('Write ')
    ixv1.write('./fs_ixv1.hdf5',format='hdf5',overwrite=True,path='hoge')
    exv.write('./fs_exv.hdf5',format='hdf5',overwrite=True,path='hoge')
    diff12.write('./fs_diff12.hdf5',format='hdf5',overwrite=True,path='hoge')
    diff13.write('./fs_diff13.hdf5',format='hdf5',overwrite=True,path='hoge')
    comm12.write('./fs_comm12.hdf5',format='hdf5',overwrite=True,path='hoge')
    comm13.write('./fs_comm13.hdf5',format='hdf5',overwrite=True,path='hoge')
    tr120_selfnoise.write('./fs_selfnoise.hdf5',format='hdf5',overwrite=True,path='hoge')
    strain.write('./fs_gif.hdf5',format='hdf5',overwrite=True,path='hoge')


    
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
    ax.plot(diff12, color='r',label=r'(IXV1 - IXV2)/$\sqrt{2}$')
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
    ax.plot(diff12, color='r',label=r'(IXV1 - IXV2)/$\sqrt{2}$')    
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
    ax.plot(comm12, color='k',label=r'(IXV1 + IXV2)/$\sqrt{2}$')
    ax.plot(diff12, color='r',label=r'(IXV1 - IXV2)/$\sqrt{2}$')
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
if comparison_seis_gif and readgif:
    from gwpy.plot import Plot
    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(1e-3, 100), yscale='log', ylim=(1e-6,1e1))
    ax.plot(diff13*np.sqrt(2), color='k',label=r'2 Seismometer diffs')
    ax.plot(gif, color='g',label=r'Strainmeter',zorder=0,linewidth=3)
    ax.plot(np.logspace(-4,2,1e4),2e-12*1e6*3e3*np.ones(10000),'g--')
    ax.set_xlabel('Frequency [Hz]',fontsize=20)
    ax.set_ylabel(r'Displacement [um/$\sqrt{\mathrm{Hz}}$]',fontsize=20)
    ax.set_title('X-arm Baseline Motion',fontsize=20)
    ax.legend(fontsize=15,numpoints=2,handlelength=1,loc='lower left')
    ax.text(110, 1e-6, 'START : {0}'.format(start), rotation=90,ha='left',va='bottom')
    ax.text(150, 1e-6, 'BW : {0:3.2e}, Window : {1}, AVE : {2:3d}'.format(df,window,ave), rotation=90,ha='left',va='bottom')
    plot.savefig('img_comparison_seis_gif.png')
    print('img_comparison_seis_gif.png')    
