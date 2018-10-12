#
#! coding:utf-8

from miyopy.io import read
from miyopy.io.read import save_to_dump,DumpFileException
from miyopy.plot import plotBandPassTimeseries


def main(start,chname):
    if start%(3600*24)==54018: # 00h00m00sの条件
        end = start + 3600*24
        try:
            value = read(start,end,chname,fmt='dump')
        except DumpFileException as e:
            data = read(start,end,[chname],fmt='nds')
            value = data[0].data            
            save_to_dump(value,start,end,chname)
        plotBandPassTimeseries(value,start,end,chname,imgdir='./daily/{0}/'.format(start))
    else:
        raise ValueError('start time dose not match "00h00m00s". start:{}' \
                         .format(start))

    
if __name__ == '__main__':
    import sys 
    argvs = sys.argv
    argc = len(argvs)
    if argc == 3:
        _,start,chname = argvs
    else:
        raise ValueError('Usage: # python {start} {chname}')
    
    main(int(start),chname)
    
