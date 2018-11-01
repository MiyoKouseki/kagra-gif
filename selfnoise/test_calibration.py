#
#! coding:utf-8
import numpy
import matplotlib as mpl
mpl.use('Agg')

from gwpy.timeseries import TimeSeries
from gwpy.time import tconvert
from gwpy.signal import filter_design
from gwpy.plot import Plot,BodePlot

from miyopy.utils import trillium

c2V = 10.0/2**15
deGain = 10**(-30.0/20.0)

__dumped_gwf_fmt = './data/{start}_{tlen}_{chname}.gwf'
dumped_gwf_fmt = './data/{start}_{end}_{chname}.gwf'
dumped_gwf_fmt = './data/{start}_{end}_{chname}.gwf'
timeseriesplot_fname_fmt = 'TimeSeries_{channel}.png'
spectrogramplot_fname_fmt = 'Spectrogram_{channel}.png'
asdplot_fname_fmt = 'ASD_{channel}.png'

channels = ['K1:PEM-IXV_SEIS_NS_SENSINF_INMON.mean',
            'K1:PEM-IXV_SEIS_WE_SENSINF_INMON.mean',
            'K1:PEM-IXV_SEIS_Z_SENSINF_INMON.mean',
            'K1:PEM-EXV_SEIS_NS_SENSINF_INMON.mean',
            'K1:PEM-EXV_SEIS_WE_SENSINF_INMON.mean',
            'K1:PEM-EXV_SEIS_Z_SENSINF_INMON.mean',
            'K1:PEM-EYV_SEIS_NS_SENSINF_INMON.mean',
            'K1:PEM-EYV_SEIS_WE_SENSINF_INMON.mean',
            'K1:PEM-EYV_SEIS_Z_SENSINF_INMON.mean',
            'K1:PEM-IXV_SEIS_TEST_NS_SENSINF_INMON.mean',
            'K1:PEM-IXV_SEIS_TEST_WE_SENSINF_INMON.mean',
            'K1:PEM-IXV_SEIS_TEST_Z_SENSINF_INMON.mean']



def main(channel,start,end):
    data = TimeSeries.read(
        dumped_gwf_fmt.format(start=start,end=end,chname=channel),
        channel, verbose=True ,nproc=8)


    # Make Filter
    dnumden_120qa = trillium.tf_120qa(analog=False,
                                      sample_rate=2048/2,
                                      Hz=False,
                                      normalize=True)
    #
    filters = [dnumden_120qa]
    
    # Plot Bodeplot
    plot = BodePlot(*filters,
                    frequencies=numpy.logspace(-3,3,1e5),
                    dB=False,sample_rate=2048/2,
                    unwrap=False,analog=False,
                    title='filter')

    axes = plot.get_axes()
    labels = ['Trillium120QA','TrilliumCompact']
    for i,ax in enumerate(axes):
        ax.legend(labels,loc='lower left')

    #axes[0].set_yscale('log')
    #axes[0].set_ylim(1e-1,2e0)
    #axes[0].set_ylim(-40,2)
    #axes[-1].set_xlim(5e-3,3e0)
    axes[-1].set_ylim(-200,200)
    plot.savefig('Bodeplot_Trillium120QA.png')
    plot.close()

    exit()
    # Filtering
    data_calib = data.filter(zpk_trillium120qa, filtfilt=True,analog=False)

    # crop
    data_calib = data_low.crop(*data_calib.span.contract(1))
        
    # Plot TimeSeries        
    from gwpy.plot import Plot    
    data_set = [data_calib]
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

    # Plot ASD
    fftlen = 2**7
    specgram = data.spectrogram2(fftlength=fftlen, overlap=2, 
                                 window='hanning') ** (1/2.)
    median = specgram.percentile(50)
    low = specgram.percentile(5)
    high = specgram.percentile(95)
    plot = Plot()
    ylabel_fmt = r'{yaxis_label} [{yaxis_label}/\rtHz]'
    ax = plot.gca(xscale='log', xlim=(1e-3, 10), 
                  xlabel='Frequency [Hz]',
                  yscale='log', #ylim=(3e-24, 2e-20),
                  ylabel=ylabel_fmt.format(yaxis_label=yaxis_label))
    ax.plot_mmm(median, low, high, color='gwpy:ligo-livingston')
    ax.set_title(title,fontsize=16)
    plot.savefig(asdplot_fname_fmt.format(channel=channel))
    plot.close()

    # Plot Spectrogram
    specgram = data.spectrogram(fftlen*2, fftlength=fftlen, overlap=.5) ** (1/2.)
    plot = specgram.imshow(norm='log')
    ax = plot.gca()
    ax.set_yscale('log')
    ax.set_ylim(1e-3, 10)
    ax.set_title(title,fontsize=16)
    ax.colorbar(label=ylabel_fmt.format(yaxis_label=yaxis_label))
    plot.savefig(spectrogramplot_fname_fmt.format(channel=channel))


if __name__ == "__main__":
    tlen = 2**16
    #start = 1222354818 # UTC 2018-09-30T15:00:00
    if False:
        start, end = 'Sep30 15:00:00', 'Oct20 15:00:00'
    if True:
        start,end = 'Sep30 15:00:00', 'Oct01 09:12:16'

    start = tconvert(start)
    end = tconvert(end)
    channel = 'K1:PEM-IXV_SEIS_NS_SENSINF_INMON'    
    
    main(channel,start,end)
    
    
