#
#! coding:utf-8
import numpy as np
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 20000
import matplotlib.pyplot as plt
try:
    from gwpy.timeseries import TimeSeries
    from miyopy.timeseries import TimeSeries as ts
except :
    pass
from scipy.signal import butter,lfilter,freqz
from scipy import signal
from plot import *
from tips import fetch,makedirs,bandpass

    
def plotBandPassTimeseries(start,end,chname,
                           low_high = [[0.01,None],
                                       [0.01,0.05],
                                       [0.05,0.3],
                                       [0.3,1.0]],
                           labels = ['No Filt',
                                     'DC (-0.01 Hz)',
                                     'Low (0.01-0.05 Hz)',
                                     'Mid (0.05-0.3 Hz)',
                                     'High (0.3-1.0 Hz)'],
                           plot_filter=True,
                           plot_timeseries=True,
                           imgdir='./',**kwargs):
    '''時系列データをバンドパスしてプロットする関数   

    Parameter
    ---------
    start : int
        開始GPS時刻
    end : int
        終了GPS時刻
    chname : str
        チャンネル名
    low_high : list of list (2,n)
        バンドパスの周波数リスト。任意の個数に対応。[low,high]で指定する。
        もしローパスにしたいなら[low,None]に、もしハイパスにしたいなら
        [None,high]にして必要ないところをNoneにすればOK。
    labels : list of str (n+1)
        バンドパスのラベル。ただし最初は'No Filt'がはいるのでlow_highリスト
        よりも要素は1多い。
    plot_filter : Bool
        もしTrueなら、フィルタのグラフを描く。デフォルトはTrue。
    plot_timeseries : Bool
        もしTrueなら、Timeseriesのグラフを描く。デフォルトはTrue。
    '''
    
    makedirs(imgdir)
    data = []
    data.append(fetch(chname,start,end).value)
    nlen = len(data[0])    
    tlen = float(end-start)
    fs = nlen/tlen
    time = np.arange(nlen)/fs/60.0/60.0 # hours

    b,a = [],[]
    for low,high in low_high:
        _data,_b,_a = bandpass(data[0], low,high, fs, order=3)    
        data.append(_data)
        b.append(_b)
        a.append(_a)    

    if plot_filter:
        fig, (ax0,ax1) = plt.subplots(2,1,figsize=(10,6),dpi=160)
        for i,[b,a] in enumerate(np.c_[b,a]):
            ax0, ax1 = plot_bode(ax0,ax1,b,a,fs,label=labels[i+1])    
        plot21_bode(ax0,ax1,
                    fname = '{0}bandpass.png'.format(imgdir)
        )
        
    if plot_timeseries:        
        ax_num = len(low_high)+1
        fig, ax = plt.subplots(ax_num,1,figsize=(10,10),dpi=160)
        ylim = (np.max(data[0])-np.min(data[0]))/2.0
        for i in range(ax_num):
            ax[i].set_ylim(-ylim,ylim)
            # !!!! chunksizeではどうしようももなかったので、データを間引いている !!!
            ax[i].plot(time[::8],data[i][::8],label=labels[i],color='k',linewidth=1)
            ax[i].legend()    
            ax[i].grid(which='major',linestyle=':', linewidth=1)
        fname = '{0}TimeSeries_{1}_{2}_{3}.png'.format(imgdir,start,end,chname)
        plotn1_Timeseries(fig,ax,fname=fname,
                          sidetext='GPS: {0}\nChannelName: {1}'.format(start,chname),
                          ylabel='Velocity [count]',
                          xlabel='Time [Hours]',
                          title='Band Passed Timeseries\n{0}'.format(chname),
                          **kwargs)
        
        
if __name__ == '__main__':
    import sys 
    argvs = sys.argv
    argc = len(argvs)
    if argc == 4:
        _,start,end,chname = argvs
        start = int(start)
        end = int(end)
    else:
        raise ValueError('Usage: # python {start} {end} {chname}')


    # Example
    plotBandPassTimeseries(start,end,chname,
                           low_high = [[0.01,None],
                                       [0.01,0.05],
                                       [0.05,0.3],
                                       [0.3,1.0]],
                           labels = ['No Filt',
                                     'DC (-0.01 Hz)',
                                     'Low (0.01-0.05 Hz)',
                                     'Mid (0.05-0.3 Hz)',
                                     'High (0.3-1.0 Hz)'],
                           plot_filter=True,
                           plot_timeseries=True,
                           imgdir='./')
    
