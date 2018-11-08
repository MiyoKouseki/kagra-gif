#
#! coding:utf-8

from gwpy.timeseries import TimeSeries
from gwpy.time import tconvert
from gwpy.plot import Plot, BodePlot
from gwpy.signal import filter_design
from scipy import signal

import numpy

dumped_gwf_fmt = './data/{start}_{end}_{chname}.gwf'
timeseriesplot_fname_fmt = 'TimeSeries_{channel}.png'
spectrogramplot_fname_fmt = 'Spectrogram_{channel}.png'
asdplot_fname_fmt = 'ASD_{channel}.png'


def main(channel,start,end):

    data = TimeSeries.read(
        dumped_gwf_fmt.format(start=start,end=end,chname=channel),
        channel, verbose=True ,nproc=8)


    # Filter
    zpk_bp_high = filter_design.highpass(0.3, data.sample_rate, 
                                         ftype='butter',analog=False,
                                         gpass=2,gstop=40,fstop=0.03
    )
    zpk_bp_mid = filter_design.bandpass(0.03, 0.3, data.sample_rate, 
                                        ftype='butter',analog=False,
                                        gpass=2, gstop=40,fstop=(0.003,3)
    )
    zpk_bp_low = filter_design.lowpass(0.03, data.sample_rate, 
                                       ftype='butter',analog=False,
                                       gpass=2, gstop=40, fstop=0.3
    )
    filters = [zpk_bp_high, zpk_bp_mid, zpk_bp_low]

    # Plot Bodeplot
    plot = BodePlot(*filters,
                    frequencies=numpy.logspace(-4,1,1e5),
                    dB=True,sample_rate=data.sample_rate,
                    unwrap=False,analog=False,
                    title='filter')
    axes = plot.get_axes()
    labels = ['High (300mHz-)','Mid (50mHz-300mHz)','Low (-50mHz)']
    for i,ax in enumerate(axes):
        ax.legend(labels,loc='lower left')
        
    #axes[0].set_yscale('log')
    #axes[0].set_ylim(1e-3,2e0)
    axes[0].set_ylim(-40,2)
    axes[-1].set_xlim(5e-3,3e0)
    axes[-1].set_ylim(-200,200)
    plot.savefig('Bodeplot_BandPass.png')
    plot.close()
        
    # Filtering
    data_high = data.filter(zpk_bp_high, filtfilt=True,analog=False)
    data_mid = data.filter(zpk_bp_mid, filtfilt=True,analog=False)
    data_low = data.filter(zpk_bp_low, filtfilt=True,analog=False)

    # 
    data_high = data_high.crop(*data_high.span.contract(1))
    data_mid = data_mid.crop(*data_mid.span.contract(1))
    data_low = data_low.crop(*data_low.span.contract(1))
        
    # Plot TimeSeries        
    from gwpy.plot import Plot    
    data_set = [data,data_high, data_mid, data_low]
    plot = Plot(*data_set,
                separate=True, sharex=True, sharey=True,
                color='gwpy:ligo-livingston',
                figsize=[10,10])

    # Add text, and save figure
    title = channel[3:].replace('_',' ')
    labels = ['No filt', 'High (300mHz-)', 'Mid (50mHz-300mHz)', 'Low (-50mHz)']
    if data.unit == ' ':
        yaxis_label = 'Count'
    else:
        yaxis_label = data.unit
    axes = plot.get_axes()
    for i,ax in enumerate(axes):
        ax.legend([labels[i]],loc='upper left')
    plot.text(0.04, 0.5, yaxis_label, va='center', rotation='vertical',fontsize=18)
    axes[0].set_title(title,fontsize=16)
    axes[-1].set_xscale('Hours', epoch=start)
    plot.savefig(timeseriesplot_fname_fmt.format(channel=channel))
    plot.close()
    
    
if __name__ == "__main__":
    if False:
        start, end = 'Sep30 15:00:00', 'Oct20 15:00:00'
    if True:
        start,end = 'Sep30 15:00:00', 'Oct01 09:12:16'

    start = tconvert(start)
    end = tconvert(end)
    channel = 'K1:PEM-IXV_SEIS_NS_SENSINF_INMON'

    main(channel,start,end)
