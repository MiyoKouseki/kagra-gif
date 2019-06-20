

# ----------------------------------------
# Parse Arguments
# ----------------------------------------
import argparse
parser = argparse.ArgumentParser(description='Find Channels in NDS')
parser.add_argument('channel', help='channel name')
parser.add_argument('-trend', default='minutes',
                    help='choose in ["minutes","seconds"]',)
parser.add_argument('-types', default='mean',
                    help='choose in ["mean","max","min","rms"]')
args = parser.parse_args()
chname = args.channel
trend = args.trend
types = args.types

# ----------------------------------------
# Fetch data from NDS
# ----------------------------------------
import nds2
conn = nds2.connection('10.68.10.121', 8088)
fmt = '{c}.{type},{trend}-trend'.format(c=chname,type=types,trend=trend[0])
found = conn.find_channels(fmt)
for ch in found:
    print ch.name

