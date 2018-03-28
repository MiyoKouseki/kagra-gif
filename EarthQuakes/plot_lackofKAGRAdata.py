#
#! coding:utf-8
import matplotlib
matplotlib.use('Agg')
import os

import numpy as np
from check_fw import get_fw0_dataframe
import matplotlib.pyplot as plt
from astropy.time import Time
import pandas as pd

gps2UTC = lambda gps:Time(gps, format='gps').utc.iso

def get_timeseriese(fname = './fw1-latest.txt'):
    '''
    フレームファイルが存在する時刻の情報をつかって、時系列データにし直す関数    
    '''    
    data = get_fw0_dataframe(fname,ascending=True)
    start_end = data.loc[:,['GPS_START','GPS_END']].values[-50:]
    OK_gpstime_lst = map(lambda (st,en):np.arange(st,en),start_end)
    NO_gpstime = np.arange(start_end[0][0],start_end[-1][-1])
    NO_state = np.zeros(len(NO_gpstime))
    for OK_gpstime_lst_ in OK_gpstime_lst:
        mask = np.in1d(NO_gpstime,OK_gpstime_lst_)
        NO_state[mask] = 1
    print 'got timeseries data from '+fname
    return NO_gpstime,NO_state


def plot_fillgraph(time,value):
    plt.plot(time,value)
    plt.fill_between(time,value,where=value>0,alpha=0.5)
    title = 'lack of data on the {0} from {1} to {2}'.format(fw,time[0],time[-1])
    plt.title(title,fontsize=15)
    plt.xlabel('Time',fontsize=15)
    plt.ylabel('Value (0 or 1)',fontsize=15)
    return 

def mpplot_fill(ax,x,y,xlabel='x',ylabel='y',legend='None'):
    ax.plot(x,y,label=legend)
    ax.fill_between(x,y,where=y>0,alpha=0.5)
    ax.set_xlabel(xlabel,fontsize=15)
    ax.set_ylabel(ylabel,fontsize=15)
    ax.set_ylim(0,1)
    xticks = np.arange(x[0],x[-1],60*60*12)
    xticklabels = gps2UTC(xticks)
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels,rotation=10)
    return ax

def subplot21_fill(data,fname):
    fw0_gpstime,fw0_state = data[0]
    fw1_gpstime,fw1_state = data[1]
    #
    fig, ax = plt.subplots(2, 1, figsize=(15, 10))
    fig.suptitle('hoge',fontsize=20)
    ax[0] = mpplot_fill(
        ax[0],
        fw0_gpstime,
        fw0_state,
        xlabel='Time',
        ylabel='Value',
        )
    ax[1] = mpplot_fill(
        ax[1],
        fw1_gpstime,
        fw1_state,
        xlabel='Time',
        ylabel='Value',
        )
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(fname)
    plt.close()    

if __name__=='__main__':
    #
    fw0_time,fw0_state = get_timeseriese('fw0-latest.txt')
    fw1_time,fw1_state = get_timeseriese('fw1-latest.txt')
    #
    end = fw1_time[-1]
    start = end-3600*24*5
    fw0_idx =  np.where((fw0_time>start)*(fw0_time<end)==True)
    fw0_time = fw0_time[fw0_idx]
    fw0_state = fw0_state[fw0_idx]
    fw1_idx =  np.where((fw1_time>start)*(fw1_time<end)==True)
    fw1_time = fw1_time[fw1_idx]
    fw1_state = fw1_state[fw1_idx]
    #
    subplot21_fill(
        data=[[fw0_time,fw0_state],[fw1_time,fw1_state]],
        fname='lackofdata_fw.png'
    )
    
    
