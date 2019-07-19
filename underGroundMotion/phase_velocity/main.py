import random
import argparse

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


    CHECK_BIT    = 0b1     # 1
    LACK_OF_FILE = 0b10    # 2
    LACK_OF_DATA = 0b100   # 4
    GLITCH       = 0b1000  # 8
    UNKNOWN      = 0b10000 # 16

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
        # for start,end in use:
        #     log.debug(start)
        #     db.update_flag('IXV_SEIS',start,end,CHECK_BIT,off=True)
        # exit()
        #
        #
        #db.add_table('EYV_SEIS')
        #exit()
        # for start,end,flag in segments:
        #     start = int(start)
        #     end = int(end)
        #     #log.debug('{0} {1} {2}'.format(start,end,flag))
        #     ans = db.get_flag('EYV_SEIS',start,end)
        #     log.debug('##{0}'.format(ans))
        #     if flag=='LACK_OF_FILE':
        #         flag = LACK_OF_FILE
        #     elif flag=='OK':
        #         flag = CHECK_BIT
        #     elif flag=='Unknown':
        #         flag = UNKNOWN
        #     else:
        #         raise ValueError('!')
        #     db.update_flag('EYV_SEIS',start,end,flag)
        #     db.update_flag('EYV_SEIS',start,end,CHECK_BIT,off=True)
        #     ans = db.get_flag('EYV_SEIS',start,end)
        #     log.debug(ans)
        #     #exit()
        # exit()

    log.info('# ----------------------------------------')
    log.info('# Start SeismicNoise                      ')
    log.info('# ----------------------------------------')    

    #random.seed(3434)    
    segments = use
    #segments = random.sample(use,10)
    n = len(segments)
    import traceback
    for i,(start,end) in enumerate(segments,1):
        sources = existedfilelist(start,end)
        channels = get_seis_chname(start,end,place=['IXV'],axis=['X'])
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
                #exit()
        except TypeError as e:
            if 'NoneType' in e[0]:
                status = 'LACK_OF_FILE'
            else:
                log.debug(traceback.format_exc())
                status = 'Unknown'
                #exit()
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
                #exit()                
        except Exception as e:
            log.debug(traceback.format_exc())
            #exit()
            status = 'Unknown'
            
        log.debug('#7 {0:04d}/{4} {1} {2} {3}'.format(i,start,end,status,n))
        # tail ./log/main.log | grep \#1 | awk '{print $3}' > hoge.txt
