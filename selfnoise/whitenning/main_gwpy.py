
from gwpy.timeseries import TimeSeries

chname = 'K1:PEM-IXV_SEIS_NS_SENSINF_IN1_DQ'
start = 'Nov 12 3:0:0'
end = 'Nov 12 4:0:0'
data = TimeSeries.fetch(chname, start, end, host='10.68.10.121', port=8088)
data.write('ixv_ns.gwf',format='gwf.lalframe')
