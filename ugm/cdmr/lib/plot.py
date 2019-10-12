import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import traceback

from gwpy.segments import DataQualityFlag

import logger
log = logger.Logger(__name__)


def plot_averaged_asd(specgrams,fname):
    '''
    '''
    fig ,ax = plt.subplots(1,1,figsize=(7,7))
    median = specgrams.percentile(50)
    low = specgrams.percentile(5)
    high = specgrams.percentile(95)
    ax.plot_mmm(median, low, high, color='black')    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_ylim(5e-3,50)
    ax.set_ylabel('Velocity [um/sec/rtHz]')
    ax.set_xlabel('Frequency [Hz]')
    plt.savefig(fname)
    log.debug('Plot {0}'.format(fname))
    plt.close()


def plot_segmentlist(*args,**kwargs):
    '''
    '''        
    start = args[0].known[0].start
    end = args[0].known[0].end
    plot = args[0].plot(figsize=(25,5),epoch=start,xlim=(start,end))
    ax = plot.gca()
    for data in args[1:]:
        ax.plot(data,label=data.name)
    fname = kwargs.pop('fname')
    ax.set_xlim(start,end)
    log.debug(fname)
    plt.savefig(fname)


def plot_asd(asdlist,fname_img,**kwargs):
    '''
    '''
    fig ,ax = plt.subplots(1,1)
    nproc = kwargs.pop('nproc',2)
    for asd in asdlist:
        ax.loglog(asd,label=asd.name.replace('_','\_'))
    ax.legend(loc='lower left')
    ax.set_ylim(5e-3,50)
    ax.set_ylabel('Velocity [um/sec/rtHz]')
    ax.set_xlabel('Frequency [Hz]')
    plt.savefig(fname_img)
    plt.close()


def plot_timeseries(data,start,end,bad_status,fname_img):
    '''
    '''
    fig = plt.figure(figsize=(15, 10))
    plt.suptitle('Seismometer at 2nd floor in X-end (EXV) {0}'.format(bad_status),fontsize=30)
    grid = plt.GridSpec(3, 6, hspace=0.4, wspace=0.5)
    
    if not data:
        return False

    for i,d in enumerate(data.values()):
        main_ax = fig.add_subplot(grid[i, :-1])
        main_ax.plot(d,label=d.name.replace('_','\_'))
        main_ax.set_ylabel('Velocity [um/sec]')
        main_ax.set_xscale('minutes')
        main_ax.legend()
        main_ax.plot([start,end],[d.mean().value,d.mean().value],'k')
        std5 = d.std().value*6
        std10 = d.std().value*10
        mean = d.mean().value
        main_ax.plot([start,end],[mean+std5,mean+std5],'k')
        main_ax.plot([start,end],[mean-std5,mean-std5],'k')
        x_hist = fig.add_subplot(grid[i,-1],sharey=main_ax)
        try:
            x_hist.hist(d.value,bins=50,orientation=u'horizontal',histtype='step')
        except ValueError as e:
            # Error in "5415/7457 ./data/TS_1234833538_1234837634.png 20"
            #log.debug(traceback.format_exc())            
            x_hist.axhspan(mean-std10, mean+std10, alpha=0.5, color='Yellow')
        try:
            main_ax.set_ylim(mean-std10,mean+std10)
            x_hist.set_ylim(mean-std10,mean+std10)
        except:
            pass
        if bad_status:
            main_ax.axvspan(start, end, alpha=0.5, color='red')
    plt.savefig(fname_img)
    plt.close()
