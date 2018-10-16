#
#! coding-utf8

from miyopy.io.reader import gif




if __name__=='__main__':
    start = 1223251218
    end = 60
    chname = 'X2000_BARO'
    fs = 8
    gif.read(start,end,chname,fs)
    
