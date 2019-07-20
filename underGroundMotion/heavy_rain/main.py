import matplotlib.pyplot as plt
from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert

import re

def coherence_specgram(me,you,stride,fftlen,overlap):
    specgram = me.coherence_spectrogram(you,stride,fftlen,overlap)
    ans = re.search(r"K1.*SEIS_(?P<name>[A-Z]+)_GND_(?P<axis>[A-Z]+)", str(me.name))
    if ans:
        me_name = ans.group('name')
        me_axis = ans.group('axis')
    ans = re.search(r"K1.*SEIS_(?P<name>[A-Z]+)_GND_(?P<axis>[A-Z]+)", str(you.name))
    if ans:
        you_name = ans.group('name')
        you_axis = ans.group('axis')
    fname = './results/COH_{0}_{1}_{2}.png'.format(me_name,you_name,me_axis)
    title = '{0} vs {1} with each {2} Axes'.format(me_name,you_name,me_axis)
    plot = specgram.imshow( vmin=0, vmax=1, title=title)
    ax = plot.gca()
    ax.set_yscale('log')
    ax.set_ylim(1e-2, 8)
    ax.colorbar(label=r'Coherence')
    plot.savefig(fname)
    plot.close()
    print fname

def specgram(data,stride,fftlen,overlap):
    specgram = data.spectrogram(stride,fftlen,overlap)
    ans = re.search(r"K1.*SEIS_(?P<name>[A-Z]+)_GND_(?P<axis>[A-Z]+)", str(data.name))
    if ans:
        me_name = ans.group('name')
        me_axis = ans.group('axis')
        title = '{1} Axis of the {0} Seiscmometer'.format(me_name,me_axis)
    plot = specgram.imshow(norm='log', vmin=1e-5, vmax=1e1, title=title)
    ax = plot.gca()
    ax.set_yscale('log')
    ax.set_ylim(1e-2, 8)
    ax.colorbar(label=r'Velocity [um/sec/$\sqrt{\mathrm{Hz}}$]')
    fname = './results/SG_{0}_{1}.png'.format(me_name,me_axis)
    plot.savefig(fname)
    plot.close()
    print fname



    
start = tconvert('Jul 18 2019 12:00:00 JST')
#start = tconvert('Jul 20 2019 13:00:00 JST')
end   = tconvert('Jul 20 2019 15:00:00 JST')
channels = ['K1:PEM-SEIS_EYV_GND_X_OUT16',
            'K1:PEM-SEIS_EYV_GND_Y_OUT16',
            'K1:PEM-SEIS_EYV_GND_Z_OUT16',
            'K1:PEM-SEIS_EXV_GND_X_OUT16',
            'K1:PEM-SEIS_EXV_GND_Y_OUT16',
            'K1:PEM-SEIS_EXV_GND_Z_OUT16',            
            'K1:PEM-SEIS_IXV_GND_X_OUT16',
            'K1:PEM-SEIS_IXV_GND_Y_OUT16',
            'K1:PEM-SEIS_IXV_GND_Z_OUT16'
           ]
    
data = TimeSeriesDict.fetch(channels,start,end,host='10.68.10.122',port=8088,
                            verbose=True,pad=0.0)
eyv_x = data.values()[0]
eyv_y = data.values()[1]
eyv_z = data.values()[2]
exv_x = data.values()[3]
exv_y = data.values()[4]
exv_z = data.values()[5]
ixv_x = data.values()[6]
ixv_y = data.values()[7]
ixv_z = data.values()[8]

# eyv
specgram(eyv_x,2**8,2**6,2**5)
specgram(eyv_y,2**8,2**6,2**5)
specgram(eyv_z,2**8,2**6,2**5)

# coherence
# X axis
coherence_specgram(eyv_x,exv_x,2**8,2**6,2**5)
coherence_specgram(eyv_x,ixv_x,2**8,2**6,2**5)
# Y axis
coherence_specgram(eyv_y,exv_y,2**8,2**6,2**5)
coherence_specgram(eyv_y,ixv_y,2**8,2**6,2**5)
# Z axis
coherence_specgram(eyv_z,exv_z,2**8,2**6,2**5)
coherence_specgram(eyv_z,ixv_z,2**8,2**6,2**5)

