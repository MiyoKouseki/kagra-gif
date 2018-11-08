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
    print hoge

    from gwpy.timeseries import TimeSeries
    channel = 'K1:PEM-EXV_SEIS_NS_SENSINF_DQ_IN1_DQ'
    start = gps -5*60
    end = gps -5*60
    gwf_cache = 'K-K1_C.Oct1-Oct21.cache'
    with open(gwf_cache, 'r') as fobj:
        cache = Cache.fromfile(fobj)
    data = TimeSeries.read(cache,chname,start,end,verbose=True,nproc=8,pad=np.nan)

