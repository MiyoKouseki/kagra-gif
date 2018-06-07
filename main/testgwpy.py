import nds2
import gwpy
from gwpy.timeseries import TimeSeries
#exit()
data = TimeSeries.fetch('K1:PEM-EY1_SEIS_WE_LOW_RMSMON',
                        1212028001, 1212028601,
                        host='10.68.10.121',port=8088)
plot = data.plot()
plot.savefig('hoge.png')
print data
