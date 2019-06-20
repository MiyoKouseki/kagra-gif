#
#! coding:utf-8
from gwpy.timeseries import TimeSeriesDict
from gwpy.time import tconvert
import numpy as np
import traceback
'''
神岡のNDSをつかって、複数チャンネルのトレンドデータをプロットするスクリプト
'''

# ----------------------------------------
# Parse Arguments
# ----------------------------------------
import argparse
parser = argparse.ArgumentParser(description='Plot trend data from nds')
parser.add_argument('-channel', nargs="*", help='channel name')
parser.add_argument('start', help='start time')
parser.add_argument('end', help='end time')
parser.add_argument('-trend', default='minutes',
                    help='choose in ["minutes","seconds"]',)
parser.add_argument('-types', default='mean',
                    help='choose in ["mean","max","min","rms"]')

args = parser.parse_args()
chname = args.channel
trend = args.trend
types = args.types
start = tconvert(args.start)
end = tconvert(args.end)
# ----------------------------------------
# Fetch data from NDS
# ----------------------------------------
kwargs = {'host':'10.68.10.122',
          'port':8088,
          'verbose':True,
          'pad':0.0}
try:
    data = TimeSeriesDict.fetch(chname,start,end,**kwargs)
except ValueError as e:
    print traceback.format_exc()
    raise ValueError('{0} is invaid channel name.\nPlease check a channel name in NDS using a find_channel scipt like "find_channels K1:GIF*"'.format(chname))
except RuntimeError as e:
    print traceback.format_exc()
    raise ValueError('{0} is not in {1} - {2}'.format(chname,start,end))
except:
    print traceback.format_exc()    
    raise ValueError('??????')
labelname = [c.replace('_','\_') for c in chname]
# ----------------------------------------
# Plot
# ----------------------------------------
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec, GridSpecFromSubplotSpec
figure, ax = plt.subplots(4,1,figsize=(30,15),sharex=True)
ylim = [(0,400),
        (0,400),
        (0.99,1.01),
        (-3000,1000)]
for i,value in enumerate(data.values()):    
    ax[i].plot(value,label=labelname[i])
    ax[i].set_ylabel('Count')
    ax[i].legend(fontsize=20,loc='lower left')
    ax[i].set_xscale('days',epoch=value.t0)
    ax[i].set_ylim(ylim[i][0],ylim[i][1])
    #ax[i].set_ylim(0,2)

plt.savefig('img_trend.png')
