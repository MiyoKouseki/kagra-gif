#
#! coding:utf-8
from plotTimeseries import plotBandPassTimeseries

def main(start,chname):
    if start%(3600*24)==54018: # 00h00m00sの条件        
        plotBandPassTimeseries(start,start+24*3600,
                               chname,
                               imgdir='./daily/{0}/'.format(start))
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
    
