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

import matplotlib.pyplot as plt


def check(start,end,plot=False,nproc=2,cl=0.05,tlen=4096,sample_rate=16,place='EXV',axis='X'):
    ''' Return the data status of a seismometer at specified time.

    Check the data status with three steps; 

    Parameters
    ----------
    start : `int`
        start GPS time.
    end : `int`
        end GPS time.
    place : `str`, optional
        place of the seismometer. default is 'EXV'
    axis : `str`
        axis of the seismometer. default is 'X'
    nproc : `int`
        number of CPU process.
    cl : `float`
        confidential level. default is 0.05.
    tlen : `int`
        time of the length of data. default is 4096 sec.
    sample_rate : `int`
        sample rate of data. default is 16.
    plot : `Bool`
        If you want to plot a timeseries, True. default is True.

    Returns
    -------
    status : `str`
        status of data
    '''
    # Check DAQ trouble    
    try:
        chname = get_seis_chname(start,end,place=place,axis=axis)[0]
        fnamelist = existedfilelist(start,end)
        data = TimeSeries.read(fnamelist,chname,nproc=nproc)
        data = data.resample(sample_rate)
        data = data.crop(start,end)
        data = data.detrend('linear')
    except ValueError as e:
        if 'Cannot append discontiguous TimeSeries' in e.args[0]:
            return 'NoData_LackofData'
        elif 'Failed to read' in e.args[0]:
            return 'NoData_NoChannel'
        elif 'array must not contain infs or NaNs' in e.args[0]:
            return 'Nodata_AnyNan'
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

    # Check Outlier
    if data.shape[0] != tlen*sample_rate:
        return 'NoData_FewData'
    if data.std().value == 0.0:
        return 'NoData_AllZero'
    if any(data.value==0.0):
        return 'NoData_AnyZero'
    if any(np.diff(data.value) == 0.0):
        return 'WrongData_AnyConstant'

    # Check Gaussianity
    w,p_value = stats.shapiro(data.resample(1).value)
    if plot:
        std = data.std().value
        mean = data.mean().value
        _max = data.max().value
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
        mu, sigma = norm.fit(data.value)
        y = np.linspace(ymin, ymax, 100)
        p = norm.pdf(y, mu, sigma)
        ax1.plot(p,y,'k', linewidth=2)
        n, bins, patches = ax1.hist(data.value, 50, normed=1, facecolor='black',
                                    orientation="horizontal",
                                    alpha=0.50)
        ax1.set_ylim(ymin,ymax)
        ax1.set_xlim(0,0.07)
        ax1.set_xticklabels(np.arange(0.0,0.15,0.02), rotation=-90)
        ax1.set_xlabel('Probability Density')
        if p_value<cl:
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
        plt.savefig('./data/img/{0}_{1}.png'.format(start,end))
        plt.close()

    if p_value < cl:
        return 'Normal_Reject'
    else :
        return 'Normal'

    return None
