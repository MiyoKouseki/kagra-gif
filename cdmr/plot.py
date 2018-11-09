#
#! coding:utf-8
from __future__ import print_function
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['agg.path.chunksize'] = 1000000
#print(mpl.rcParams['agg.path.chunksize'])
import numpy as np
from matplotlib.ticker import ScalarFormatter
from scipy.signal import butter, lfilter
from scipy import signal, interpolate
from control import matlab
from trillium import selfnoise,V2Vel
from tips import *

c_pwave = 5500.0 # m/s

try:
    import nds2
    import gwpy    
    from miyopy.timeseries import TimeSeries as ts
    from gwpy.timeseries import TimeSeries
except:
    pass
        

def plot_asd(ax,datalist,fname='asd',labels=None,
             ave=None,
             tlen=None,
             disp=True,model=None,adcnoise=True,
             unit=None,selfnoiseplot=True,trillium=None,
             linestyle=['r-','b-','g-'],**kwargs):
    
    ax.set_xlim([1e-3, 1e2])
    ax.set_ylim([1e-12, 1e-5])    
    if unit=='strain':
        ax.set_ylabel('ASD [1/sqrtHz]')           
    elif unit == 'm':
        ax.set_ylabel('ASD [m/sqrtHz]')   
    else:
        raise ValueError('Unit is not defined. unit; {}'.format(unit))

    if tlen==None:
        raise ValueError('tlen is not defined. tlen {}'.format(tlen))
    
    plotOK = [True,True,False]
    integ = [True,True,False]

    for i,data in enumerate(datalist):
        f,Asd = asd(np.array(data),fs=len(data)/tlen,integ=integ[i],ave=ave,**kwargs)
        print(i)
        if i < 2:
            #f,Asd = V2Vel(f, Asd, trillium=trillium)
            ax.loglog(f, Asd, linestyle[i], label=labels[i], linewidth=2)            
        else: # for gifx
            if model=='comm/diff':
                pass
            else:
                ax.loglog(f, Asd, linestyle[i], label=labels[i], linewidth=2)
        if (True in np.isnan(Asd)):
            print('Data has nan value!')    
                
    #print(trillium)
    if adcnoise==False:
        #adc = datalist[2]
        #f,Asd = asd(np.array(adc),fs=len(adc)/tlen,integ=False,**kwargs)
        #Asd = np.ones(len(Asd))*np.average(Asd)
        Asd = np.ones(len(f))*1e-2
        Asd = Asd/(2.0*np.pi*f)
        f,Asd = V2Vel(f, Asd, trillium=trillium)
        ax.loglog(f, Asd, 'b:',label='adc',linewidth=2,alpha=0.5)
    if selfnoiseplot==False:
        f_self,Psd_self = selfnoise(trillium=trillium,psd='PSD',acc='acc')
        Asd_self = np.sqrt(Psd_self) #
        #Asd_self = np.sqrt(Psd_self)*np.sqrt(2.0) # in case in diff,comm
        Asd_self = Asd_self/(2.0*np.pi*f_self)/(2.0*np.pi*f_self)
        ax.loglog(f_self, Asd_self, 'g-',label='self',linewidth=2)
        
    cfmin,cfmax = cf(alpha=0.05,k=ave*2)    
    ax.errorbar(1.0, 1e-6, yerr=[[(1-cfmin)*1e-6],[(cfmax-1)*1e-6]], fmt='ko',markersize=2,capsize=3,label='{0:3.0f}%, DoF={1}'.format((1-0.05)*100,ave*2))        
    ax.set_xlabel('Frequency [Hz]')
    ax.legend(loc='upper right',fontsize=8)
    ax.tick_params(axis='both',direction='in',which='both')
    ax.grid(which='major',linestyle='-', linewidth=1)
    ax.grid(which='minor',linestyle=':', linewidth=1)
    return ax

def plot_cdmr(ax,datalist,fname='cdmr',tlen=None,labels=None,
              disp=True,model='comm/diff',trillium=None,L=3000.0,**kwargs):
    '''
    
    '''    
    # plot cdmr 
    if len(datalist)==3: # [comm, diff, gifx] case
        integ = [True,True,False] 
        f,Asd_diff = asd(datalist[0],fs=len(datalist[0])/tlen,integ=integ[0],**kwargs)
        f,Asd_comm = asd(datalist[1],fs=len(datalist[1])/tlen,integ=integ[1],**kwargs)
        f_,Asd_gifx = asd(datalist[2],fs=len(datalist[2])/tlen,integ=integ[2],**kwargs)
        ax.loglog(f, Asd_comm/Asd_diff, label=labels[0],color='k',linewidth=2)
        f, Asd_comm = V2Vel(f, Asd_comm, trillium=trillium)
        ax.loglog(f_, interp(Asd_comm,f,f_)/Asd_gifx, label=labels[1],
                  color='r',linewidth=2,linestyle='-')
    elif len(datalist)==2: # [comm, diff] case
        integ = [True,True]
        f,Asd_diff = asd(datalist[0],fs=len(datalist[0])/tlen,integ=integ[0],**kwargs)
        f,Asd_comm = asd(datalist[1],fs=len(datalist[1])/tlen,integ=integ[1],**kwargs)
        ax.loglog(f, Asd_comm/Asd_diff, label=labels[0],color='k',linewidth=2)
    else:
        raise ValueError('Invalid datalist. len(datalist)={}'.format(len(datalist)))
    
    # plane wave model
    #f = np.linspace(f[0],f[-1],1e6)
    ax.loglog(f, np.ones(len(f)),
              label='No Correlation Model',color='b',
              linewidth=2,linestyle='--'
              )
    if model=='comm/gifx': # for Comm/GIFx Model
        ax.loglog(f, (2.0*c_pwave)/(2.0*np.pi*f*L)*np.cos(2.0*np.pi*f*(L/2.0/c_pwave)),
                label='Plane Wave Model (v=5500 m/s)',
                color='g',linewidth=2,linestyle='--'
                )
    elif model=='comm/diff': # for Comm/Diff Model
        ax.loglog(f, 1.0/np.tan(2.0*np.pi*f*(L/2.0/c_pwave)),
                label='Plane Wave Model (v=5500 m/s)',
                color='g',linewidth=2,linestyle='--'
                )
    else:
        raise ValueError('Invalid model name {}'.format(model))
    
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('CDMR')
    ax.set_xlim([1e-2,1e2])
    ax.legend(fontsize=8)
    ax.grid(which='major',linestyle='-', linewidth=1)
    ax.grid(which='minor',linestyle=':', linewidth=1)        
    ax.tick_params(axis='both',direction='in',which='both')
    ax.set_ylim([5e-1,5e2])
    return ax


def plot_coh(ax,data,fname='cdmr',tlen=None,ave=32,labels=None,disp=True,**kwargs):
    if len(data)==3:
        data1, data2, gif = data
    else:
        data1, data2 = data
        
    if disp:
        integ=True
    else:
        integ=False
    #print(ave)
    dof = ave*2
    alpha = 0.05
    integ=False # kesu!
    #
    f,coh,deg = get_coh(data1,data2,fs=len(data1)/tlen,integ=integ,tlen=tlen,**kwargs)
    
    ax.semilogx(f, coh, label=labels[0],color='k',linewidth=2)
    #cl = np.arange(len(f))*
    cl = 1.0-alpha**(1./(float(dof)/2.0-1.0))
    ax.semilogx(f, cl*np.ones(len(f)),
                label='95% ',color='k',
                linewidth=1,linestyle='--')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Magnitude-Squared \n Coherence')
    ax.set_xlim([1e-2,1e2])
    ax.legend(fontsize=8)
    ax.grid(which='major',linestyle='-', linewidth=1)
    ax.grid(which='minor',linestyle=':', linewidth=1)        
    ax.tick_params(axis='both',direction='in',which='both')
    #ax.set_yticks(np.arange(10)[::1])
    ax.set_ylim([0,1])
    return ax

def plot_coh_deg(ax,data,tlen=None,fname='cdmr',labels=None,disp=True,**kwargs):
    if len(data)==3:
        data1, data2, gif = data
    else:
        data1, data2 = data
    if disp:
        integ=True
    else:
        integ=False
    
    f,coh,deg = get_coh(data1,data2,fs=len(data1)/tlen,tlen=tlen,integ=integ,**kwargs)
    ax.semilogx(f, deg, label=labels[0],color='k',linewidth=2)
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Phase [deg]')
    ax.set_xlim([1e-2,1e2])
    ax.legend(fontsize=8,loc='upper right')
    ax.grid(which='major',linestyle='-', linewidth=1)
    ax.grid(which='minor',linestyle=':', linewidth=1)        
    ax.tick_params(axis='both',direction='in',which='both')
    ax.set_yticks(np.arange(-180,181,90))
    ax.set_ylim([-180,180])
    return ax


def plot21_cdmr(data,fname='cdmr',start=None,tlen=None,
                title='No title',labels1=None,labels2=None,**kwargs):
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, dpi=640)
    ax1 = plot_asd(ax1,data,labels=labels1,ave=32,tlen=tlen,disp=True,unit='m',**kwargs)
    ax2 = plot_cdmr(ax2,data,labels=labels2,ave=32,tlen=tlen,disp=True,**kwargs)
    plt.subplots_adjust(hspace=0.1,top=0.92)
    xticklabels = ax1.get_xticklabels()
    plt.setp(xticklabels, visible=False)
    ax_pos = ax1.get_position()
    fig.text(ax_pos.x1*1.01, ax_pos.y0,'GPS:{0}\nHanning,ovlp=50%'.format(start),rotation=90,verticalalignment='bottom')    
    fig.suptitle(title,fontsize=12)
    ax1.yaxis.set_label_coords(-0.1,0.5)
    ax2.yaxis.set_label_coords(-0.1,0.5)    
    plt.savefig('{0}.png'.format(fname))
    plt.close()
    print('plot {}.png'.format(fname))
    

def plot(data,fname='NoTile',title='No title',
         labels1=None,labels2=None,
         tlen=None,**kwargs):
    
    fig, ax1 = plt.subplots(1, 1, sharex=True, dpi=640)
    start = kwargs.get('start',None)
    ax1 = plot_asd(ax1,data,labels=labels1,ave=32,disp=True,tlen=tlen,**kwargs)
    plt.subplots_adjust(hspace=0.1,top=0.92)
    ax_pos = ax1.get_position()
    fig.text(ax_pos.x1*1.01, ax_pos.y0,'GPS:{0}\nHanning,ovlp=50%'.format(start),rotation=90,verticalalignment='bottom')
    ax_pos = ax1.get_position()
    fig.suptitle(title,fontsize=12)
    ax1.yaxis.set_label_coords(-0.1,0.5)
    ax1.set_xlabel('Frequency [Hz]')
    #ax2.yaxis.set_label_coords(-0.1,0.5)    
    plt.savefig('{0}.png'.format(fname))
    plt.close()
    print('plot {}.png'.format(fname))    


def plot_timeseries(data,fname='No Title',
                    title='No title',labels1=None,
                    tlen=None,start=None,labels2=None,**kwargs):
    
    fig, ax1 = plt.subplots(1, 1, sharex=True, dpi=640)
    for i in range(len(data))[:1]:
        time = np.arange(len(data[i]))/(float(len(data[i]))/tlen)
        ax1.plot(time,data[i],label=labels1[i])
    plt.subplots_adjust(hspace=0.1,top=0.92)
    plt.legend()
    #xticklabels = ax1.get_xticklabels()
    #plt.setp(xticklabels, visible=False)
    ax_pos = ax1.get_position()
    fig.text(ax_pos.x1*1.01, ax_pos.y0,'GPS:{0}\nHanning,ovlp=50%'.format(start),rotation=90,verticalalignment='bottom')    
    ax_pos = ax1.get_position()
    fig.suptitle(title,fontsize=12)
    ax1.yaxis.set_label_coords(-0.1,0.5)
    ax1.set_xlabel('Time [sec]')
    #ax2.yaxis.set_label_coords(-0.1,0.5)    
    plt.savefig('{0}.png'.format(fname))
    plt.close()


def plot41_blrms_timeseries(data,fname='No Title',
                            title='No title',labels1=None,
                            tlen=None,start=None,**kwargs):
    '''
    Parameter
    ---------
    data : 1d-array
        プロットしたい時系列データ。
    tlen : int
        時系列の長さ。これがないと時系列データのサンプリング周波数が分からない。
    '''
    
    fs = float(len(data))/tlen
    time = np.arange(len(data))/fs
    #time = time
    #data = data
    
    y0,y1,y2,y3 = get_bandpass(data,fs=fs,plot=False)

    fig, (ax1,ax2,ax3,ax4) = plt.subplots(4, 1, sharex=True, dpi=640)   
    ax1.plot(time[::1],y0[::1],label='no filt')
    ax1.set_ylim([-1e-6,1e-6])
    ax1.legend(loc='upper right')
    ax1.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax1.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
    ax2.plot(time[::1],y1[::1],label='0.03-0.1Hz')
    ax2.set_ylim([-1e-6,1e-6])
    ax2.legend(loc='upper right')
    ax2.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax2.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))    
    ax3.plot(time[::1],y2[::1],label='0.1-0.3Hz')
    ax3.set_ylim([-1e-6,1e-6])
    ax3.legend(loc='upper right')
    ax3.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax3.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))    
    ax4.plot(time[::1],y3[::1],label='0.3-3Hz')
    ax4.set_ylim([-1e-6,1e-6])
    ax4.legend(loc='upper right')
    ax4.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax4.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
    plt.subplots_adjust(hspace=0.26,top=0.95)
    fig.text(.05, .5, 'Velocity [m/s]', ha='center', va='center', rotation='vertical')
    xticklabels = ax1.get_xticklabels()
    plt.setp(xticklabels, visible=False)
    ax_pos = ax4.get_position()
    fig.text(ax_pos.x1*1.01,
             ax_pos.y0,
             'GPS:{0}\nHanning,ovlp=50%'.format(start),
             rotation=90,verticalalignment='bottom')    
    ax_pos = ax4.get_position()
    fig.suptitle(title,fontsize=12)
    ax4.yaxis.set_label_coords(-0.1,0.5)
    ax4.set_xlabel('Time [sec]')
    #ax2.yaxis.set_label_coords(-0.1,0.5)    
    plt.savefig('{0}.png'.format(fname))
    plt.close()
    print('plot as ./{}.png'.format(fname))
    
    
def plot21_coherence(data,fname='seismometer',title='No title',tlen=None,labels1=None,labels2=None,start=None,**kwargs):
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, dpi=340)
    ax1 = plot_coh(ax1,data,labels=labels1,ave=32,tlen=tlen,disp=False,**kwargs)
    ax2 = plot_coh_deg(ax2,data,labels=labels2,ave=32,tlen=tlen,disp=False,**kwargs)
    plt.subplots_adjust(hspace=0.1,top=0.92)
    xticklabels = ax1.get_xticklabels()
    plt.setp(xticklabels, visible=False)
    ax_pos = ax1.get_position()
    fig.text(ax_pos.x1*1.01, ax_pos.y0,'GPS:{0}\nHanning,ovlp=50%'.format(start),rotation=90,verticalalignment='bottom')    
    fig.suptitle(title,fontsize=12)
    ax1.yaxis.set_label_coords(-0.09,0.5)
    ax2.yaxis.set_label_coords(-0.1,0.5)    
    plt.savefig('{0}.png'.format(fname))
    plt.close()
    
def plot_31(data,fname='seismometer',title='No title',labels1=None,labels2=None,**kwargs):   
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, dpi=340)
    fs = len(data[0])/tlen
    time = np.arange(len(data[0]))/fs
    ax1.plot(time,data[0],label=labels1[0])
    ax2.plot(time,data[0],label=labels1[0])
    #ax1 = plot_ts(ax1,data,labels=labels1,ave=32,disp=True,**kwargs)
    plt.subplots_adjust(hspace=0.1,top=0.92)
    xticklabels = ax1.get_xticklabels()
    plt.setp(xticklabels, visible=False)
    ax_pos = ax1.get_position()
    fig.suptitle(title,fontsize=12)
    ax1.yaxis.set_label_coords(-0.09,0.5)
    ax2.yaxis.set_label_coords(-0.1,0.5)    
    plt.savefig('{0}.png'.format(fname))
    plt.close()


def save(data,fnames,ave=32,**kwargs):
    if False:
        i = 0
        np.savetxt(fnames[i]+'.dat',data[0],delimiter=',')
    if True:
        diff,comm,gif = data[0],data[1],data[2]
        integ=True
        f,Ad = asd(diff,fs=len(diff)/tlen,integ=integ,ave=ave,**kwargs)
        f,Ac = asd(comm,fs=len(comm)/tlen,integ=integ,ave=ave,**kwargs)
        f_,Agif = asd(gif,fs=len(gif)/tlen,integ=False,ave=ave,**kwargs)
        i=0
        header_tmp = '''Filename : {0}
Date : 2018/07/20
Author : K.Miyo

Discription
-----------
Xend   \t: displacement of the seismometer on the Xend 
       \t  2nd floar(EXV) with Xarm direction
Center \t: displacement of the seismometer on the Center 
       \t  2nd floar(IXV) with Xarm direction
GIF    \t: gifx of the Xarm 1500 m distance measured by 
       \t  GIF gifxmeter
diff_seis \t:= (Xend-Center)/sqrt(2)
comm_seis \t:= (Xend+Center)/sqrt(2)
diff_gif  \t:= GIF*3000/sqrt(2)

Data Information
----------------
Data Name         \t: {0}
Start [GPS Time]  \t: {1}
Time Lenght [sec] \t: {2}
BW [Hz]           \t: {3:3.4e}
Window            \t: Hanning
Average           \t: {4}
Overlap           \t: 50% 
Dof               \t: {5}


Frequency[Hz],ASD [um/sqrtHz]'''
        header = header_tmp.format('asd_'+fnames[0]+'.dat',start,tlen,f_[1]-f_[0],ave,ave*2)    
        np.savetxt('asd_'+fnames[0]+'.dat',np.c_[f_,interp(Ad,f,f_)],delimiter=',',fmt='%1.7e',newline='\n',comments='#',header=header)
        header = header_tmp.format('asd_'+fnames[1]+'.dat',start,tlen,f_[1]-f_[0],ave,ave*2)    
        np.savetxt('asd_'+fnames[1]+'.dat',np.c_[f_,interp(Ad,f,f_)],delimiter=',',fmt='%1.7e',newline='\n',comments='#',header=header)
        header = header_tmp.format('asd_'+fnames[2]+'.dat',start,tlen,f_[1]-f_[0],ave,ave*2)    
        np.savetxt('asd_'+fnames[2]+'.dat',np.c_[f_,Agif],delimiter=',',fmt='%1.7e',newline='\n',comments='#',header=header)
        pass
        exit()










