#
#! coding:utf-8
from glue import lal
from gwpy.timeseries import TimeSeries

'''
'''

def dumpdata(cachename,chname,dumpfname):
    '''cacheファイルを元にしてデータを取得してダンプする関数。
    
    cacheファイルはmkcacheを元にして作られる。これは存在すファイル名だけを
    リストアップしたテキストファイル。

    cachename : str
        キャッシュファイル名。
    chanem : str
        チャンネル名。
    '''
    cache = lal.Cache.fromfile(open(cachename))
    data = TimeSeries.read(cache, chname)
    data.write(dumpfname)

    
def fromdumpdata(fname,chname):
    '''ダンプしたGWFファイルからデータを読み込む関数
    
    fname : str
        ダンプしたファイル名。
    chanem : str
        ダンプファイルに存在するチャンネル名。
    '''
    data = TimeSeries.read(fname, chname)
    return data



if __name__ == '__main__':
    dumpdata("../K-K1_C.bKAGRAphase1_a.cache",'K1:PEM-EX1_SEIS_NS_SENSINF_INMON','phase1a_ex1_ns.gwf')
    data = fromdumpdata('./phase1a_ex1_ns.gwf','K1:PEM-EX1_SEIS_NS_SENSINF_INMON')
