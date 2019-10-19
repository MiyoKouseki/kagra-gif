import scipy.stats as stats
from scipy.stats import norm
import traceback
import os
import numpy as np

from gwpy.time import tconvert
from gwpy.timeseries import TimeSeries,TimeSeriesDict
from gwpy.spectrogram import Spectrogram

import Kozapy.utils.filelist as existedfilelist
from matplotlib import gridspec

import lib.logger
log = lib.logger.Logger(__name__)
from lib.channel import get_seis_chname
from lib.iofunc import fname_hdf5_longasd,fname_gwf,fname_hdf5_asd

import matplotlib.pyplot as plt


def check(start,end,plot=False,nproc=2):
    #if os.path.exists('./tmp/{0}_{1}.png'.format(start,end)):
    #    return 'Pass'
    try:
        chname = get_seis_chname(start,end,axis='X')
        fnamelist = existedfilelist(start,end)
        data = TimeSeries.read(fnamelist,chname,nproc=nproc)
        data = data.resample(16)
        data = data.crop(start,end)
        data = data.detrend('linear')
    except ValueError as e:
        if 'Cannot append discontiguous TimeSeries' in e.args[0]:
            return 'NoData_LackofData'
        elif 'Failed to read' in e.args[0]:
            return 'NoData_FailedtoRead'
        else:
            log.debug(traceback.format_exc())
            raise ValueError('!!!')
    except IndexError as e:
        if 'cannot read TimeSeries from empty source list' in e.args[0]:
            return 'NoData_Empty'
        else:
            log.debug(traceback.format_exc())
            raise ValueError('!!!')
    except RuntimeError as e:
        if 'Failed to read' in e.args[0]:
            return 'NoData_FailedtoRead'
        elif 'Not a frame file (Invalid FrHeader)' in e.args[0]:
            return 'NoData_FailedtoRead'
        else:
            log.debug(traceback.format_exc())
            raise ValueError('!!!')
    except TypeError  as e:
        if 'NoneType' in e.args[0]:
            return 'NoData_NoChannel'
        else:
            log.debug(traceback.format_exc())
            raise ValueError('!!!')
    except:
        log.debug(traceback.format_exc())
        raise ValueError('!!!')

    if data.shape[0] != 4096:
        return 'NoData_FewData'
    if data.std().value == 0.0:
        return 'NoData_AllZero'
    if any(data.value==0.0):
        return 'NoData_AnyZero'
    if any(np.diff(data.value) == 0.0):
        return 'WrongData_AnyConstant'
    std = data.std().value
    mean = data.mean().value
    _max = data.max().value
    if plot:
        fig = plt.figure(figsize=(19,8))
        gs = gridspec.GridSpec(1, 3, width_ratios=[3,1,3],wspace=0.15) 
        ax0 = plt.subplot(gs[0])
        ax1 = plt.subplot(gs[1:2])
        ax2 = plt.subplot(gs[2:])
        ax0.set_ylabel('Counts')
        ax0.plot(data,'k')
        ax0.hlines(mean,start,end,'k')
        ax0.set_xscale('auto-gps')
        ax0.set_xlim(start,end)
        ymin,ymax = mean-std*6,mean+std*6
        _ymin,_ymax = mean-std*5,mean+std*5
        ax0.set_ylim(ymin,ymax)
        #ax0.hlines(_ymin,start,end,color='k',linestyle='--')
        #ax0.hlines(_ymax,start,end,color='k',linestyle='--')
        mu, sigma = norm.fit(data.value)
        y = np.linspace(ymin, ymax, 100)
        p = norm.pdf(y, mu, sigma)
        ax1.plot(p,y,'k', linewidth=2)
        n, bins, patches = ax1.hist(data.value, 50, normed=1, facecolor='black',
                                    orientation="horizontal",
                                    alpha=0.50)
        ax1.set_ylim(ymin,ymax)
        ax1.set_xlim(0,0.14)
        #ax1.set_xticks(np.arange(0.0,0.15,0.02))
        ax1.set_xticklabels(np.arange(0.0,0.15,0.02), rotation=-90)
        #ax1.hlines(_ymin,0,0.14,color='k',linestyle='--')
        #ax1.hlines(_ymax,0,0.14,color='k',linestyle='--')        
        ax1.set_xlabel('Probability Density')
        w,p_value = stats.shapiro(data.resample(1).value)
        if p_value<0.05:
            ax1.patch.set_facecolor('red')
            ax1.patch.set_alpha(0.3) 
        ax1.text(0.005,ymin,
                 'mu     '+': {0:03.1f}\n'.format(mu) + \
                 'sigma  '+': {0:03.1f}\n'.format(sigma)+\
                 'w      '+': {0:01.2f}\n'.format(w)+\
                 'p-value'+': {0:01.2f}'.format(p_value),
                 verticalalignment='bottom',
                 fontsize=17,
                 bbox=dict(facecolor='black', alpha=0.1))
        stats.probplot(data.value,dist='norm',plot=ax2)
        ax2.set_ylim(ymin,ymax)
        plt.savefig('./tmp/{0}_{1}.png'.format(start,end))
        plt.close()

    # if np.abs(_max-mean)/std > 10:
    #     return 'Glitch_10sigma'
    # elif  np.abs(_max-mean)/std > 5:
    #     return 'Glitch_5sigma'
    if p_value < 0.05:
        return 'Normal_Reject'
    else :
        return 'Normal'

    return 'Stationaly'
