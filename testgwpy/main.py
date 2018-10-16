#
#! coding:utf-8
import sys
sys.path.insert(0,'/Users/miyo/Dropbox/Git/gwpy/')

from gwpy.timeseries import TimeSeries
import gwpy


if __name__=='__main__':
    strain = TimeSeries.read(source='./1810140000.STRAIN',
                             name='CALC_STRAIN',
                             start=1223478018,
                             format='gif')


    # plot timeseries
    plot = strain.plot(title='GIF strain data',
                       ylabel='Strain amplitude',
                       )
    plot.savefig('timeseries.png')
    plot.close()

    
    # plot spectrogram
    stride = 10 # sec
    fftlength = 5 # sec
    spectrogram = strain.spectrogram(stride=stride, fftlength=fftlength) ** (1/2.)
    plot = spectrogram.imshow(norm='log', vmin=5e-12, vmax=1e-10)
    ax = plot.gca()
    ax.set_yscale('log')
    ax.set_ylim(0.01, 200)
    ax.colorbar(
        label=r'GIF strain amplitude [strain/$\sqrt{\mathrm{Hz}}$]')
    plot.savefig('spectrogram.png')
    plot.close()

    
    # plot asd
    fftlength = 5
    overlap = 2
    sg = strain.spectrogram2(fftlength=fftlength,
                             overlap=overlap, window='hanning') ** (1/2.)
    median = sg.percentile(50)
    low = sg.percentile(5)
    high = sg.percentile(95)
    from gwpy.plot import Plot
    plot = Plot()
    ax = plot.gca(xscale='log', xlim=(0.01, 200), xlabel='Frequency [Hz]',
                yscale='log', ylim=(5e-14, 1e-5),
                ylabel=r'Strain noise [1/\rtHz]')
    ax.plot_mmm(median, low, high, color='gwpy:ligo-hanford')
    ax.set_title('GIF strain',
                fontsize=16)
    plot.savefig('asd.png')
    plot.close()
