#
#! coding:utf-8
from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert
import numpy as np
'''
神岡のNDSをつかって、複数チャンネルのトレンドデータをプロットするスクリプト
'''

start = tconvert('May 01 2019 00:00:00 JST')
end   = tconvert('May 07 2019 00:00:00 JST')


chname = [
    #'K1:PEM-SEIS_IXV_GND_X_OUT_DQ.mean,m-trend',
    #'K1:PEM-SEIS_EXV_GND_X_OUT_DQ.mean,m-trend',
    'K1:PEM-WEATHER_IXV_FIELD_PRES_OUT16.mean,m-trend',
    'K1:GIF-X_STRAIN_OUT16.mean,m-trend',
    #'K1:GIF-X_ZABS_OUT16.mean,m-trend',
    ]
    
data = TimeSeriesDict.fetch(chname,start,end,
                            host='10.68.10.122',port=8088,
                            verbose=True,pad=np.nan)
fftlen = 2**16

for data in data.values():
    name = data.name
    plot = data.plot(label=name.replace('_',' '),epoch=data.t0)    
    ax = plot.gca()
    if 'PRES' in name:
        ax.set_ylim(8000,10000)
    ax.legend()
    plot.savefig('{0}.png'.format(name))
    plot.close()
exit()
# strain = data['K1:GIF-X_STRAIN_OUT16.mean,m-trend']
# sg = strain.spectrogram2(fftlength=fftlen, overlap=fftlen/2, window='hanning') ** (1/2.)
# median = sg.percentile(50)
# low = sg.percentile(5)
# high = sg.percentile(95)

# from gwpy.plot import Plot
# plot = Plot()
# ax = plot.gca(xscale='log', xlim=(1e-6, 10), xlabel='Frequency [Hz]',
#               yscale='log', ylim=(1e-14, 1e-5),
#               ylabel=r'Strain noise [1/$\sqrt{\mathrm{Hz}}$]')
# ax.plot_mmm(median, low, high, color='gwpy:ligo-hanford')
# ax.set_title('LIGO-Hanford strain noise variation around GW170817',
#              fontsize=16)
# plot.savefig('img_asd.png')    



coh = data['K1:GIF-X_STRAIN_OUT16.mean,m-trend'].coherence(data['K1:PEM-WEATHER_IXV_FIELD_PRES_OUT16.mean,m-trend'], fftlen, fftlen/2)

plot = coh.plot(figsize=[12, 6], label=None)
ax = plot.gca()
ax.set_yscale('linear')
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Coherence')
ax.set_title('Coherence between SRCL and CARM for L1')
ax.grid(True, 'both', 'both')
plot.savefig('img_coh.png')
