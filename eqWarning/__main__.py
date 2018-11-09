from event import (get_catalog, get_eventids, get_eventtimes,
                   get_eventdepths, get_eventmags,
                   calc_distance_from_eq, get_arrivals, get_eventgps,
                   )
from main import make_eventcsv
from plot import (main_plot_eqmap, plot_arrivals, plot_eqmap)
from arrival import get_first_arrival_times

import numpy as np
#import pandas as pd


def main():
    kwargs = {}
    kwargs['minmagnitude'] = 7.5
    #kwargs['minlatitude'] = 0
    #kwargs['maxlatitude'] = 45
    #kwargs['minlongitude'] = 120
    #kwargs['maxlongitude'] = 180
    #kwargs['maxmagnitude'] = 8    
    start_str = '2018-09-01'
    end_str = '2018-11-01'
    
    from event import get_catalog
    catalog = get_catalog(start_str,end_str,**kwargs)
    
    plot_eqmap(catalog,lat_0=36.43,lon_0=137.31,radius=8000e3,title='None')
    df = make_eventcsv(catalog,to_csv=True,phase_list=['P'],**kwargs)
    #print df
    #plot_arrivals(eventid=10944928)


def hoge(gps):
    if np.isnan(gps):
        return None
    from gwpy.time import tconvert
    #print tconvert(gps)
    from gwpy.timeseries import TimeSeries
    from glue.lal import Cache
    channel = 'K1:PEM-EXV_SEIS_Z_SENSINF_OUT_DQ'
    start = gps #- 5*60
    end = gps + 30*60
    gwf_cache = 'full_Sep01-Nov01.cache'
    with open(gwf_cache, 'r') as fobj:
        cache = Cache.fromfile(fobj)
    #print cache
    data = TimeSeries.read(cache,channel,start=start,end=end,verbose=True,nproc=2,pad=np.nan,format='gwf.lalframe')    
    plot = data.plot(
        title = 'hoge'
        #ylabel='Strain amplitude',
    )
    plot.savefig('{0}.png'.format(gps))
    plot.close()

def main_hoge():
    df = pd.read_csv('Sep01-Nov01_M6_pwave.csv')
    #hoge = df.loc[:,['EventTime[UTC]','PwaveFirstArrivalGPS','EventMagnitude']]
    pwave_gps = df['PwaveFirstArrivalGPS']
    for gps in pwave_gps.__iter__():
        print gps
        hoge(gps)    
    
if __name__=='__main__':
    main()   
