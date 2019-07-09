'''Read timeseries from gwffile
'''

__author__ = "K. Miyo"
import matplotlib
matplotlib.use('Agg')

import numpy as np
import os
import subprocess
import glob
import gwpy
from gwpy.timeseries import TimeSeries
from gwpy.timeseries import TimeSeriesDict
from matplotlib import pylab as pl
from gwpy.detector import Channel
from gwpy.time import tconvert
'''
M6.7, Iburi,  Sep  6 2018 03:07:59.3
M5.2, Nagano, May 25 2018 21:13:42.2

'''

start = tconvert('Aug 19 2018 00:19:40 UTC') # Fiji M8.2
end = tconvert('Aug 19 2018 01:19:40 UTC')


#start = tconvert('Sep 6 2018 03:07:59.3 JST') # 1220238498
#start = tconvert('Sep 6 2018 03:10:13 JST') 
#end   = tconvert('Sep 6 2018 03:10:14 JST') 
#end   = tconvert('Sep 6 2018 03:37:59.3 JST') 
#
#
#start = tconvert('May 25 2018 21:13:42.2 JST')
#end   = tconvert('May 25 2018 21:23:42.2 JST')

# make file list
sources = []

mtrend = False
if mtrend:
    for i in range(int(str(start)[0:5]),int(str(end)[0:5])+1):
        dir = '/data/trend/minute/' + str(i) + '/*'
        source = glob.glob(dir)
        sources.extend(source)
    sources.sort()
    removelist = []
    for x in sources:
        if int(x[32:42])<(int(start)-3599):
            removelist.append(x)
        if int(x[32:42])>int(end):
            removelist.append(x)

    for y in removelist:
        sources.remove(y)

full = True
if full:
    for i in range(int(str(start)[0:5]),int(str(end)[0:5])+1):
        dir = '/data/full/' + str(i) + '/*'
        source = glob.glob(dir)
        sources.extend(source)
    sources.sort()
    removelist = []
    for x in sources:
        if int(x[24:34])<(int(start)-31):
            removelist.append(x)
        if int(x[24:34])>int(end):
            removelist.append(x)

    for y in removelist:
        sources.remove(y)

# make channel list
channels=[
    'K1:PEM-EXV_SEIS_WE_SENSINF_OUT_DQ', # Sep
    #'K1:PEM-EX1_SEIS_WE_SENSINF_OUT_DQ', # May
    #'K1:PEM-EX1_SEIS_WE_BLRMS_LOW_OUT_DQ', 
    #'K1:GRD-LSC_MICH_STATE_N',    
]

if not os.path.exists('results'):
    cmd = 'mkdir results'
    subprocess.call(cmd.split())

for channel in channels:
    print(channel)
    chnames = []
    latexchnames = []
    suffix = ['max','min']
    
    unit = ''
    if channel.find('TEMPERATURE') != -1:
        unit = r'Temperature [\textcelsius]' 
    elif channel.find('HUMIDITY') != -1:
        unit = 'Humidity [\%]'
    elif channel.find('ACC') != -1:
        unit = r'Acceleration [$m/s^2$]'
    elif channel.find('MIC') != -1:
        unit = 'Sound [Pa]'

    if mtrend:
        for x in suffix:
            chnames.append(channel + '.' + x)
            latexchnames.append(channel.replace('_','\_') + '.' + x)

    # Time series
    if mtrend:
        data = TimeSeriesDict.read(sources,chnames,format='gwf.lalframe',
                                   nproc=2,start=int(start),pad=0.0)
        #data = data.crop(send)
        t0 = data['K1:PEM-EXV_SEIS_WE_SENSINF_OUT_DQ.max'].t0
    if full:
        data = TimeSeries.read(sources,channel,format='gwf.lalframe',
                               nproc=2,start=int(start),pad=0.0)
        t0 = data.t0
        _max = data.max()
        _min = data.min()
        fs = 1./data.dt
        #data.write('bKAGRA_mich_state.gwf',format='gwf.lalframe')
        #exit()

    if True:
        print _max,_min
        print fs
        #data = data.crop(t0,t0+2048*data.dt*4)
        plot = data.plot(label='name',epoch=t0,linestyle='None',marker='o',
                         linewidth=1,markersize=1)
        ax = plot.axes
        #ax[0].legend(latexchnames,bbox_to_anchor = (1,0),borderaxespad=1)
        ax[0].legend(latexchnames)
        ax[0].set_ylabel(unit)
        ax[0].set_ylim(-1e-3,1e-3)
        plot.savefig('./results/' + channel + '_timeseries.png')
        plot.close()

    if False:
        specgram = data.spectrogram(2,fftlength=1,overlap=.5)**(1./2.)
        plot = specgram.plot(norm='log', vmin=1e-9, vmax=1e-3,epoch=t0)
        ax = plot.gca()
        ax.set_yscale('log')
        ax.colorbar(label=r'Ground Velocity [m/sec/$\sqrt{\mathrm{Hz}}$]')
        ax.set_ylim(1, 1024)
        plot.savefig('./results/' + channel + '_specgram.png')
