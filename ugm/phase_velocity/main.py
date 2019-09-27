import random
import os
import numpy as np
import argparse
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib import gridspec

from gwpy.timeseries import TimeSeriesDict

from miyopy.dataquality import DataQuality
from miyopy.logger import Logger
from miyopy.channel import get_seis_chname
#from miyopy.timeseries import TimeSeries

import Kozapy.utils.filelist as existedfilelist

log = Logger('main')
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--start',type=int,default=1211817600)
    parser.add_argument('--end',type=int,default=1245372032)
    parser.add_argument('--nproc',type=int,default=2)
    args = parser.parse_args()
    nproc = args.nproc

    # Get segments    
    import numpy as np
    segments = np.loadtxt('hugo.txt',dtype='str')
    with DataQuality('./dqflag.db') as db:
        # use = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=0 ' +
        #              'and startgps>={0} and endgps<={1}'.format(args.start,args.end))
        # use = db.ask('select startgps,endgps from IXV_SEIS WHERE flag=0 ' +
        #              'and startgps>={0} and endgps<={1}'.format(args.start,args.end))
        use = db.ask('select startgps,endgps from EYV_SEIS WHERE flag=0 ' +
                     'and startgps>={0} and endgps<={1}'.format(args.start,args.end))

    log.info('# ----------------------------------------')
    log.info('# Start SeismicNoise                      ')
    log.info('# ----------------------------------------')    

    random.seed(3434)    
    segments = use
    segments = random.sample(use,10)
    n = len(segments)
    import traceback
    for i,(start,end) in enumerate(segments,1):
        sources = existedfilelist(start,end)
        channels = get_seis_chname(start,end,place=['IXV','EXV'],axis=['Z'])
        try:
            data = TimeSeriesDict.read(sources,channels,nproc=nproc)
            data.crop(start,end)
            data.resample(32)
            status = 'OK'
        except ValueError as e:
            if 'Failed to read' in e[0]:
                status = 'LACK_OF_FILE'
            elif 'Cannot append discontiguous TimeSeries' in e[0]:
                status = 'LACK_OF_FILE'
            else:
                log.debug(traceback.format_exc())
                status = 'Unknown'
                exit()
        except TypeError as e:
            if 'NoneType' in e[0]:
                status = 'LACK_OF_FILE'
            else:
                log.debug(traceback.format_exc())
                status = 'Unknown'
                exit()
        except IndexError as e:
            if 'cannot read TimeSeriesDict from empty source list' in e[0]:
                status = 'LACK_OF_FILE'
            elif 'Not a frame file' in e[0]:
                status = 'LACK_OF_FILE'                
            elif 'Missing' in e[0]:
                status = 'LACK_OF_FILE'
            else:
                log.debug(traceback.format_exc())
                status = 'Unknown'
                exit()                
        except Exception as e:
            log.debug(traceback.format_exc())
            exit()
            status = 'Unknown'
            
        #log.debug(data)

        log.debug('#8 {0:04d}/{4} {1} {2} {3}'.format(i,start,end,status,n))

        ixv = data.values()[0]
        exv = data.values()[1]
        t0 = ixv.t0
        #sg = ixv.spectrogram2(fftlength=2**8, overlap=2**7, window='hanning')**(1/2.)
        #asd_ixv = sg.percentile(50)    
        asd_ixv = ixv.asd(fftlength=2**8, overlap=2**7, window='hanning')
        #sg = exv.spectrogram2(fftlength=2**8, overlap=2**7, window='hanning')**(1/2.)
        #asd_exv = sg.percentile(50)
        asd_exv = exv.asd(fftlength=2**8, overlap=2**7, window='hanning') # ct/rtHz
        csd = ixv.csd(exv, fftlength=2**8, overlap=2**7, window='hanning') # ct2/Hz
        _coh = ixv.coherence(exv,fftlength=2**8, overlap=2**7, window='hanning')**0.5
        coh = csd/asd_exv/asd_ixv
        tf = csd/asd_ixv**2

        gain = (asd_exv/asd_ixv).crop(0.1,0.3).mean()

        path = './data2/{0}'.format(str(start)[:5])
        if not os.path.exists(path):
            os.mkdir(path)

        # fname_ts = path + '/{1}_{2}_TS.png'.format(str(start)[:5],start,end) 
        # plot = data.plot(ylim=(-100,100),epoch=t0)
        # plot.savefig(fname_ts)
        # plot.close()
        # log.debug(fname_ts)

        fname_coh = path + '/{1}_{2}_Z.png'.format(str(start)[:5],start,end) 
        fig = plt.figure(figsize=(20,12))
        gs = gridspec.GridSpec(4, 2) 
        #exit()
        ax0 = fig.add_subplot(gs[0,:1])
        ax1 = fig.add_subplot(gs[1,:1])
        ax2 = fig.add_subplot(gs[2,:1])
        ax3 = fig.add_subplot(gs[3,:1])
        ax4 = fig.add_subplot(gs[:2,1:])
        ax5 = fig.add_subplot(gs[2:,1:])
        ax0.loglog(asd_ixv,label='ixv')
        ax0.loglog(asd_exv,label='exv')
        ax0.set_ylabel('Count [1/rtHz]')
        ax0.set_ylim(1e-2,1e2)
        ax0.legend(loc='upper right')
        ax0.set_xlim(1e-2,10)
        ax1.loglog(tf.abs(),'k-',label='exv/ixv')
        ax1.legend(loc='upper right')
        ax1.set_ylabel('Transfer Function [Mag.]')
        ax1.set_ylim(1e-2,1e2)
        ax1.set_xlim(1e-2,10)
        ax2.semilogx(coh.abs(),'k-',label='exv/ixv')
        ax2.set_ylim(0,1)
        ax2.set_ylabel('Coherence')
        ax2.legend(loc='upper right')
        ax2.set_xlim(1e-2,10)
        ax3.semilogx(coh.angle().rad2deg(),'ko',markersize=2,label='exv/ixv')
        ax3.set_ylim(-180,180)
        ax3.set_yticks(range(-180,181,90))
        ax3.set_xlabel('Frequency [Hz]')
        ax3.set_ylabel('Phase [Degree]')
        ax3.set_xlim(1e-2,10)
        ax3.legend(loc='upper right')
        ax4.semilogx(np.real(coh),'k-',label='exv/ixv')
        ax4.set_ylim(-1,1)
        ax4.set_xlim(1e-2,10)
        ax4.set_ylabel('Real')
        ax5.semilogx(np.imag(coh),'k-',label='exv/ixv')
        ax5.set_ylim(-1,1)
        ax5.set_xlim(1e-2,10)
        ax5.set_ylabel('Imaginary')
        ax5.set_xlabel('Frequency [Hz]')
        plt.savefig(fname_coh)
        plt.close()
        log.debug(fname_coh)
        #exit()
        
