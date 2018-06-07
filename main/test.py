# Import module
import nds2

# Open connection and print some information about the server
conn = nds2.connection('10.68.10.121',8088)
print "Connection:", conn
print "Host:", conn.get_host()
print "Port:", conn.get_port()
print "Protocol:", conn.get_protocol()

# Get list of available channels and print some information about them
channels = conn.find_channels('K1:PEM-EY*')
print "Number matching of channels:", len(channels)
print "First channel:", channels[0]
print "First channel name:", channels[0].name
exit()
# Fetch some data
data = conn.fetch(1038296031, 1038296035,
    ['L1:PEM-EY_SEISX_OUT_DQ', 'L1:PEM-EY_SEISY_OUT_DQ', 'L1:PEM-EY_SEISZ_OUT_DQ'])
print "A buffer:", data[0]
print "Its data:", data[0].data
print "Its channel:", data[0].channel

print "Now block by block..."
for bufs in conn.iterate(1038296031, 1038296035, 1, ['L1:PEM-EY_SEISX_OUT_DQ', 'L1:PEM-EY_SEISY_OUT_DQ', 'L1:PEM-EY_SEISZ_OUT_DQ']):
    print bufs
