#
#! coding:utf-8

from miyopy.io.reader import kagra
t0 = 1208339257-2**10
tlen = 2**12
data = kagra.loaddata_nds(t0,tlen,chlst='4.chlst')
