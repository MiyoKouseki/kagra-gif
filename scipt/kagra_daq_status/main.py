#
#! coding:utf-8
import matplotlib
matplotlib.use('Agg')
import os
import numpy as np
import miyopy.io
from check_fw import get_fw0_dataframe
import matplotlib.pyplot as plt
from astropy.time import Time
import pandas as pd

gps2JST = lambda gps:Time(gps+3600*9, format='gps').utc.datetime
datetime2str = lambda x:x.strftime('%Y/%m/%d\n%H:%M:%S')

def get_timeseriese(fname = './fw1-latest.txt'):
    '''
    フレームファイルが存在する時刻の情報をつかって、時系列データにし直す関数    
    '''    
    data = get_fw0_dataframe(fname,ascending=True)
    start_end = data.loc[:,['GPS_START','GPS_END']].values[-60:]
    OK_gpstime_lst = map(lambda (st,en):np.arange(st,en),start_end)
    NO_gpstime = np.arange(start_end[0][0],start_end[-1][-1])
    NO_state = np.zeros(len(NO_gpstime))
    for OK_gpstime_lst_ in OK_gpstime_lst:
        mask = np.in1d(NO_gpstime,OK_gpstime_lst_)
        NO_state[mask] = 1
    print 'got timeseries data from '+fname
    return NO_gpstime,NO_state

def mpplot_fill(ax,x,y,xlabel=None,ylabel='y',legend='None'):
    #ax.plot(x,y,label=legend,color='k',linewidth=0.5)
    ax.fill_between(x,y,where=y>0,alpha=0.6,color='k',linewidth=0.5)
    ax.set_ylabel(ylabel,fontsize=20)
    ax.set_ylim(0,1)
    ax.set_yticks([])
    ax.set_xlim(x[0],x[-1])
    if xlabel == None:
        pass
    else:
        ax.set_xlabel(xlabel,fontsize=20)    
        xticks = np.arange(x[0],x[-1]+3600*24,60*60*24)
        print xticks[0]
        xticklabels = gps2JST(xticks)
        print xticklabels[0]        
        xticklabels = map(datetime2str,xticklabels)
        print xticklabels[0]        
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels,rotation=0,fontsize=15)
    return ax

def subplot21_fill(data,fname):
    fw0_gpstime,fw0_state = data[0]
    fw1_gpstime,fw1_state = data[1]
    #
    fig, ax = plt.subplots(2, 1, figsize=(15, 10),sharex=True)
    fig.suptitle('DAQ status',fontsize=20)
    ax[0] = mpplot_fill(ax[0],
                        fw0_gpstime,
                        fw0_state,
                        xlabel=None,
                        ylabel='fw0',
                        )
    ax[1] = mpplot_fill(ax[1],
                        fw1_gpstime,
                        fw1_state,
                        xlabel='Time',
                        ylabel='fw1',
                        )
    fig.subplots_adjust(hspace=0)
    plt.setp([a.get_xticklabels() for a in ax[:1]], visible=False)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(fname)
    plt.close()    

def main():   
    '''メイン関数
    
    
    '''
    fw0_time,fw0_state = get_timeseriese('fw0-latest.txt')
    fw1_time,fw1_state = get_timeseriese('fw1-latest.txt')
    #
    end = fw0_time[-1]
    end = end-end%(3600*24)+18
    start = end-3600*24*7
    fw0_idx =  np.where((fw0_time>=start)*(fw0_time<=end)==True)
    fw0_time = fw0_time[fw0_idx]
    fw0_state = fw0_state[fw0_idx]
    fw1_idx =  np.where((fw1_time>=start)*(fw1_time<=end)==True)
    fw1_time = fw1_time[fw1_idx]
    fw1_state = fw1_state[fw1_idx]
    #
    subplot21_fill(
        data=[[fw0_time,fw0_state],[fw1_time,fw1_state]],
        fname='kagra_daq_status.png'
    )       

if __name__=='__main__':
    main()
