from gwpy.detector import ChannelList
chname = 'K1:PEM-IXV_GND*'
chlst = ChannelList.query_nds2([chname],host='10.68.10.121',port=8088)
print chlst

