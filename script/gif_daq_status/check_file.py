#
#! coding: utf-8

import miyopy.io.reader as reader
#import miyopy.io

def main():
    hoge = {
        '0417_17h00m':[1207000000,2**13],
        '0413_19h00m':[1207652418-3600,2**14], # lack in 04-13-19:52 AD02 file
        }
    t0,tlen = hoge['0413_19h00m']
    chname = 'X1500_TR240velNS'
    fnames = reader.gif.findFiles(t0,tlen,chname)
    print len(fnames)*60, tlen
    t_lack = reader.gif.check_filesize(fnames,chname)
    data = reader.gif.fromfiles(fnames,chname)
    data = reader.gif.check_nan(data,fnames,chname)

if __name__ == '__main__':
    main()

    
