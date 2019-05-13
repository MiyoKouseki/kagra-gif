#
#
import numpy as np
from control import matlab
from gwpy.timeseries import TimeSeriesDict
from gwpy.frequencyseries import FrequencySeries
from gwpy.time import tconvert

def asd(data,fftlength=512):
    sg = data.spectrogram2(fftlength=fftlength, overlap=fftlength/2, window='hanning', nproc=nproc) ** (1/2.)
    median = sg.percentile(50)
    low = sg.percentile(5)
    high = sg.percentile(95)
    return median,low,high

# setting
nproc = 2
fftlength = 256

# TimeSeriese data
chnames = [
    'K1:PEM-IXV_GND_TR120Q_X_OUT_DQ',
    'K1:PEM-IXV_GND_TR120QTEST_X_OUT_DQ',
    'K1:PEM-EXV_GND_TR120Q_X_OUT_DQ',
]
start = 'Dec 10 2018 00:00:00 UTC'
end = 'Dec 10 2018 02:00:00 UTC'

data = TimeSeriesDict.read('Dec10_3hours.gwf',chnames,start,end,format='gwf.lalframe',nproc=nproc)
ixv1 = data['K1:PEM-IXV_GND_TR120Q_X_OUT_DQ']
ixv2 = data['K1:PEM-IXV_GND_TR120QTEST_X_OUT_DQ']
exv = data['K1:PEM-EXV_GND_TR120Q_X_OUT_DQ']
diff12 = (ixv1-ixv2)/np.sqrt(2)
diff13 = (ixv1-exv)/np.sqrt(2)
comm12 = (ixv1+ixv2)/np.sqrt(2)
comm13 = (ixv1+exv)/np.sqrt(2)


# treatment
readhdf5 = True
comparison_ixv1_diff12=True
comparison_diff12_diff13=True
comparison_comm13_diff13=True
comparison_comm12_diff12=True
plot_coherence=True
tplot = False
write = True


# coherence
import matplotlib.pyplot as plt
if plot_coherence:
    coh12 = ixv1.coherence(ixv2, fftlength, fftlength/2)
    coh13 = ixv1.coherence(exv, fftlength, fftlength/2)
    deg12 = ixv1.csd(ixv2, fftlength, fftlength/2).angle().rad2deg()
    deg13 = ixv1.csd(exv, fftlength, fftlength/2).angle().rad2deg()    
    fig, [ax1,ax2] = plt.subplots(2,1,figsize=[12, 6],sharex=True)
    ax1.plot(coh13,label='coh13',color='r')
    ax1.plot(coh12,label='coh12',color='k')    
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
    ax1.legend(fontsize=15)
    ax1.set_title('Coherence')    
    plt.savefig('img_coherence.png')
    
    
# Calibrated ASD
if readhdf5:
    print('Read from hdf5')
    ixv1 = FrequencySeries.read('./fs_ixv1.hdf5',format='hdf5')
    diff12 = FrequencySeries.read('./fs_diff12.hdf5',format='hdf5')
    diff13 = FrequencySeries.read('./fs_diff13.hdf5',format='hdf5')
    comm12 = FrequencySeries.read('./fs_comm12.hdf5',format='hdf5')
    comm13 = FrequencySeries.read('./fs_comm13.hdf5',format='hdf5')
    tr120_selfnoise = FrequencySeries.read('./fs_selfnoise.hdf5',format='hdf5')
    selfnoise_2seis = FrequencySeries.read('./fs_selfnoise2.hdf5',format='hdf5')
else:
    _,ixv1,_ = asd(ixv1,fftlength=fftlength)
    _,diff12,_ = asd(diff12,fftlength=fftlength)
    _,diff13,_ = asd(diff13,fftlength=fftlength)
    _,comm12,_ = asd(comm12,fftlength=fftlength)
    _,comm13,_ = asd(comm13,fftlength=fftlength)
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

# spectrum plot
if comparison_ixv1_diff12:
    from gwpy.plot import Plot
    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(1e-3, 100),
                yscale='log', ylim=(1e-7,1e2))                
    ax.plot(ixv1, color='k',label='ixv1')
    ax.plot(diff12, color='r',label=r'(ixv1 - ixv2)/$\sqrt{2}$')
    ax.plot(tr120_selfnoise, color='k',label='Selfnoise',linestyle='--',zorder=0)
    ax.set_xlabel('Frequency [Hz]',fontsize=15)
    ax.set_ylabel(r'Displacement [m/$\sqrt{\mathrm{Hz}}$]',fontsize=15)    
    ax.set_title('Comparison of various ground motion',fontsize=20)
    ax.text(110, 1e-7, 'START : {0}'.format(start), rotation=90,ha='left',va='bottom')
    ax.legend(fontsize=12)
    plot.savefig('img_comparison_ixv1_diff12.png')

# spectrum plot
if comparison_diff12_diff13:
    from gwpy.plot import Plot
    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(1e-3, 100),yscale='log', ylim=(1e-7,1e2))
    ax.plot(diff13, color='k',label=r'(ixv1 - exv)/$\sqrt{2}$')
    ax.plot(diff12, color='r',label=r'(ixv1 - ixv2)/$\sqrt{2}$')    
    ax.plot(tr120_selfnoise, color='k',label='selfnoise',linestyle='--')    
    ax.set_xlabel('Frequency [Hz]',fontsize=15)
    ax.set_ylabel(r'Displacement [m/$\sqrt{\mathrm{Hz}}$]',fontsize=15)    
    ax.set_title('Comparison of various ground motion',fontsize=20)
    ax.text(110, 1e-7, 'START : {0}'.format(start), rotation=90,ha='left',va='bottom')
    ax.legend(fontsize=12)    
    plot.savefig('img_comparison_diff12_diff13.png')

# spectrum plot
if comparison_comm13_diff13:
    from gwpy.plot import Plot
    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(1e-3, 100),yscale='log', ylim=(1e-7,1e2))
    ax.plot(comm13, color='k',label=r'(ixv1 + exv)/$\sqrt{2}$')
    ax.plot(diff13, color='r',label=r'(ixv1 - exv)/$\sqrt{2}$')
    ax.plot(tr120_selfnoise, color='k',label='selfnoise',linestyle='--')    
    ax.set_xlabel('Frequency [Hz]',fontsize=15)
    ax.set_ylabel(r'Displacement [m/$\sqrt{\mathrm{Hz}}$]',fontsize=15)    
    ax.set_title('Comparison of various ground motion',fontsize=20)
    ax.text(110, 1e-7, 'START : {0}'.format(start), rotation=90,ha='left',va='bottom')
    ax.legend(fontsize=12)        
    plot.savefig('img_comparison_comm13_diff13.png')

# com12, diff12
if comparison_comm12_diff12:
    from gwpy.plot import Plot
    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(1e-3, 100), yscale='log', ylim=(1e-7,1e2))
    ax.plot(comm12, color='k',label=r'(ixv1 + ixv2)/$\sqrt{2}$')
    ax.plot(diff12, color='r',label=r'(ixv1 - ixv2)/$\sqrt{2}$')
    ax.plot(tr120_selfnoise, color='k',label='selfnoise',linestyle='--')
    ax.set_xlabel('Frequency [Hz]',fontsize=15)
    ax.set_ylabel(r'Displacement [m/$\sqrt{\mathrm{Hz}}$]',fontsize=15)    
    ax.set_title('Comparison of various ground motion',fontsize=20)    
    ax.legend(fontsize=12)
    ax.text(110, 1e-7, 'START : {0}'.format(start), rotation=90,ha='left',va='bottom')
    plot.savefig('img_comparison_comm12_diff12.png')
    

# timeseries plot
if tplot:
    plot = data.plot()
    plot.savefig('result_timeseries.png')
    plot.close()    

# write
if write and not readhdf5:
    print('Write ')
    ixv1.write('./fs_ixv1.hdf5',format='hdf5',overwrite=True,path='hoge')
    diff12.write('./fs_diff12.hdf5',format='hdf5',overwrite=True,path='hoge')
    diff13.write('./fs_diff13.hdf5',format='hdf5',overwrite=True,path='hoge')
    comm12.write('./fs_comm12.hdf5',format='hdf5',overwrite=True,path='hoge')
    comm13.write('./fs_comm13.hdf5',format='hdf5',overwrite=True,path='hoge')
    tr120_selfnoise.write('./fs_selfnoise.hdf5',format='hdf5',overwrite=True,path='hoge')
       
