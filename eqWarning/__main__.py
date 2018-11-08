#import numpy as np
from event import (get_catalog, get_eventids, get_eventtimes,
                   get_eventdepths, get_eventmags,
                   calc_distance_from_eq, get_arrivals, get_eventgps,
                   )
from main import make_eventcsv
from plot import (main_plot_eqmap, plot_arrivals, plot_eqmap)
from arrival import get_first_arrival_times

import numpy as np
import pandas as pd
   
  
def main():
    kwargs = {}
    kwargs['minmagnitude'] = 5
    #kwargs['minlatitude'] = 0
    #kwargs['maxlatitude'] = 45
    #kwargs['minlongitude'] = 120
    #kwargs['maxlongitude'] = 180
    #kwargs['maxmagnitude'] = 8    
    start_str = '2018-09-01'
    end_str = '2018-11-01'
    #main_plot_eqmap(start_str,end_str,**kwargs)
    #df = make_eventcsv(start_str,end_str,to_csv=True,phase_list=['P'],**kwargs)
    #print df
    #plot_arrivals(eventid=10944928)


    
if __name__=='__main__':
    #main()
    df = pd.read_csv('Sep01-Nov01_M6_pwave.csv')
    hoge = df.loc[:,['EventTime[UTC]','PwaveFirstArrivalGPS']]
    pwave_gps = df['PwaveFirstArrivalGPS']
    gps = pwave_gps[0]
    from gwpy.time import tconvert
    print tconvert(gps)
    #print hoge
    #import matplotlib
    #matplotlib.use('Agg')
    from gwpy.timeseries import TimeSeries
    from glue.lal import Cache
    channel = 'K1:PEM-EXV_SEIS_NS_SENSINF_IN1_DQ'
    start = gps -5*60
    end = gps -5*60
    gwf_cache = 'full_Sep01-Nov01.cache'
    with open(gwf_cache, 'r') as fobj:
        cache = Cache.fromfile(fobj)
    print cache
    #data = TimeSeries.read(cache,channel,start=start,end=end,verbose=True,nproc=8,pad=np.nan)
    data = TimeSeries.read('/data/full/12202/K-K1_C-1220294944-32.gwf',channel,verbose=True,nproc=8,pad=np.nan)
    
    plot = data.plot(
        title = 'hoge'
        #ylabel='Strain amplitude',
    )
    plot.savefig('huge.png')
    plot.close()
