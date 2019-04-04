'''Read timeseries from gwffile
'''

__author__ = "Chihiro Kozakai"
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

# Searce channel name
# FrChannels /data/full/12091/K-K1_C-1209168000-32.gwf | grep SEIS_WE_BLRMS
#
# BLRMS_HI : 100-300 Hz
# BLRMS_LOW : 0.01-1 Hz
# BLRMS_MID : 1-100 Hz

# readout from gwf file
# measurement period 2018/12/29~2019/01/03, 1230044418~1230476418
#start = tconvert('Mar 31 2018 00:00:00 JST')
start = tconvert('Apr 7 2018 00:00:00 JST')
#start = tconvert('Apr 14 2018 00:00:00 JST')
#start = tconvert('Apr 28 2018 00:00:00 JST')
#start = tconvert('Apr 30 2018 00:00:00 JST')
#end   = tconvert('May 1 2018 00:00:00 JST')
#end   = tconvert('May 9 2018 00:00:00 JST')
#end   = tconvert('May 23 2018 00:00:00 JST')
end   = tconvert('May 30 2018 00:00:00 JST')
end   = tconvert('Jun 9 2018 00:00:00 JST')
#end = tconvert('May 8 2018 00:00:00 JST')
#
# TimeSeries 1 span: [1207699260.0 ... 1208905200.0)
# TimeSeries 2 span: [1208908800.0 ... 1208912400.0)

#end = '1230130818' # 12/29 24:00
#end = '1230217218' # 12/30 24:00
#end = '1230303618' # 12/31 24:00
#end = '1230390018' # 1/1 24:00
# 1/2 24:00
#end = '1230476418' 


# make file list

sources = []

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

# make channel list
channels=[
    #'K1:PEM-EX1_SEIS_WE_SENSINF_OUT_DQ',
    'K1:PEM-EX1_SEIS_WE_BLRMS_LOW_OUT_DQ',
]

if not os.path.exists('results'):
    cmd = 'mkdir results'
    subprocess.call(cmd.split())

for channel in channels:
    print(channel)
    chnames = []
    latexchnames = []
    #suffix = ['max','min','mean','rms']
    suffix = ['rms']
    
    unit = ''
    if channel.find('TEMPERATURE') != -1:
        unit = r'Temperature [\textcelsius]' 
    elif channel.find('HUMIDITY') != -1:
        unit = 'Humidity [\%]'
    elif channel.find('ACC') != -1:
        unit = r'Acceleration [$m/s^2$]'
    elif channel.find('MIC') != -1:
        unit = 'Sound [Pa]'

    for x in suffix:
        chnames.append(channel + '.' + x)
        latexchnames.append(channel.replace('_','\_') + '.' + x)

    # Time series
    data = TimeSeriesDict.read(sources,chnames,format='gwf.lalframe',nproc=14,start=int(start),pad=0.0)
    data = data.resample(1./60./10.) # 10 min trend
    print data['K1:PEM-EX1_SEIS_WE_BLRMS_LOW_OUT_DQ.rms'].dt
    data['K1:PEM-EX1_SEIS_WE_BLRMS_LOW_OUT_DQ.rms'].write('bKAGRA_rms_ground_velocity_hor.gwf',format='gwf.lalframe')
    #data.resample(10.)
    #source and chname are necessary.
    #format='gwf.lalframe': input file format
    #nproc=2              : # of CPUs
    #start=1231133850     : start time can be selected.
    #end=1231133860       : end time can be selected.
    #resample=10.         : change the sampling rate. [Hz]
    #data.override_unit(unit)
    
    plot = data.plot(label='name')
    ax = plot.axes
    #ax[0].legend(latexchnames,bbox_to_anchor = (1,0),borderaxespad=1)
    ax[0].legend(latexchnames)
    ax[0].set_ylabel(unit)
    ax[0].set_ylim(0,3e-6)
    plot.savefig('./results/' + channel + '_timeseries.png')
    plot.close()
