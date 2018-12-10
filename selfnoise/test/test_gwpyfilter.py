#
#! coding:utf-8


from gwpy.timeseries import TimeSeries
from gwpy.time import tconvert
from gwpy.plot import Plot


timeseriesplot_fname_fmt = 'TimeSeries_{channel}.png'
spectrogramplot_fname_fmt = 'Spectrogram_{channel}.png'
asdplot_fname_fmt = 'ASD_{channel}.png'
dumped_gwf_fmt = './data/{start}_{end}_{chname}.gwf'


def main(start,end,chname):
    data = TimeSeries.read(
        dumped_gwf_fmt.format(start=start,end=end,chname=channel),
        channel, verbose=True ,nproc=8)


    # Filtering
    from gwpy.signal import filter_design
    from gwpy.plot import BodePlot
    import numpy
    bp_high = filter_design.highpass(0.3, data.sample_rate, analog=True,
                                     ftype='butter',
                                     gpass=2,gstop=30#,fstop()
    )
    bp_mid = filter_design.bandpass(0.05, 0.3, data.sample_rate, analog=True,
                                    ftype='butter',
                                    gpass=2, gstop=30#,fstop=(0.01,0.5)
    )
    bp_low = filter_design.lowpass(0.05, data.sample_rate,analog=True, 
                                   ftype='butter',
                                   gpass=2, gstop=30#, fstop=2
    )
    filters = [bp_high,bp_mid,bp_low]

    plot = BodePlot(*filters, analog=True,
                    frequencies=numpy.logspace(-3,1,1e5),
                    dB=False,unwrap=False,
                    title='filter')
    axes = plot.get_axes()
    axes[0].set_yscale('log')
    axes[0].set_ylim(1e-4,2e0)
    axes[-1].set_xlim(1e-2,1e0)
    axes[-1].set_ylim(-180,180)
    plot.savefig('Bodeplot_BandPass.png')
    plot.close()

    data_high = data.filter(bp_high, filtfilt=True)
    data_high = data_high.crop(*data_high.span.contract(1))
    data_mid = data.filter(bp_mid, filtfilt=True)
    data_mid = data_mid.crop(*data_mid.span.contract(1))
    data_low = data.filter(bp_low, filtfilt=True)
    data_low = data_low.crop(*data_low.span.contract(1))

    
    # Plot TimeSeries
    title = channel[3:].replace('_',' ')
    labels = ['No filt', 'High (300mHz-)', 'Mid (50mHz-300mHz)', 'Low (-50mHz)']
    if data.unit == ' ':
        yaxis_label = 'Count'
    else:
        yaxis_label = data.unit

    from gwpy.plot import Plot    
    data_set = [data,data_high, data_mid, data_low]
    plot = Plot(*data_set,
                separate=True, sharex=True, sharey=True,
                color='gwpy:ligo-livingston',
                figsize=[10,10])
    
    axes = plot.get_axes()
    for i,ax in enumerate(axes):
        ax.legend([labels[i]],loc='upper left')

    plot.text(0.04, 0.5, yaxis_label, va='center', rotation='vertical',fontsize=16)
    #plot.text(0.5, 0.93, title, va='center',ha='center',rotation='horizontal',fontsize=16)
    axes[0].set_title(title,fontsize=16)
    axes[-1].set_xscale('Hours', epoch=start)
    plot.savefig(timeseriesplot_fname_fmt.format(channel=channel))
    plot.close()


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
    
    main(start,end,channel)
