from gwpy.timeseries import TimeSeries
from astropy import units as u
import matplotlib.pyplot as plt
import numpy as np
# ----------------------------------------------------------------------

def get(source,chname,**kwargs):
    data = TimeSeries.read(source,name=chname,**kwargs)
    #data.name = chname
    return data

def get_contrast(data,**kwargs):
    pk2pk = kwargs.pop('pk2pk',False)
    chname = data.name
    shape = data.shape[0]
    hoge = data.reshape(int(shape/300),300)
    _max = hoge.max(axis=1)
    _min = hoge.min(axis=1)
    if pk2pk:
        _contrast = _max-_min
        _contrast.name = data.name+'_PK2PK'
    else:
        _contrast = (_max-_min)/(_max+_min)
        _contrast.name = data.name+'_CONTRAST'        
    _contrast.dt=60*u.s    
    return _contrast

def get_statevector(absp,c_p,c_s):
    shape = absp.shape[0]
    hoge = absp.reshape(int(shape/300),300)
    absp_min = hoge.min(axis=1)    
    is_locked = absp_min > 0.200*u.V
    is_locked.dt=60*u.s
    try:
        is_good_p = c_p > 0.01*u.V
        is_good_s = c_s > 0.01*u.V
    except:
        is_good_p = c_p > 0.02
        is_good_s = c_s > 0.02
    is_ok = is_locked * is_good_p * is_good_s
    is_good = is_good_p * is_good_s
    return is_ok, is_locked, is_good, is_good_p, is_good_s

def plot(data,**kwargs):
    ylim = kwargs.pop('ylim',(0.0,0.3))
    color = kwargs.pop('color','k')
    is_ok,is_locked,is_good,is_good_p,is_good_s = kwargs.pop('sv',[])
    title = kwargs.pop('title',None)
    hlines = kwargs.pop('hlines',None)
    version = kwargs.pop('version',None)
    tmp = kwargs.pop('tmp',True)
    prefix = '{0}-{1}-'.format(str(from_gps(start)).split(' ')[0],
                               str(from_gps(end)).split(' ')[0])
    fname = version+'_'+data.name.lower()
    plot = data.plot(ylim=ylim,epoch=start,figsize=(25,5),
                     color=color,label=data.name)
    ax = plot.gca()
    ax.set_title(title)
    #ax.set_xscale('days')
    #plot.refresh()
    ax.legend(loc='upper right')
    
    if hlines:
        for hline in hlines:
            ax.hlines(hline,start,end,linestyle='--',color=color)
    if is_ok:
        obs = is_ok.to_dqflag(round=True)
        absp = is_locked.to_dqflag(round=True)
        ppol = is_good_p.to_dqflag(round=True)
        spol = is_good_s.to_dqflag(round=True)
        plot.add_segments_bar(obs,label='Observing')
        plot.add_segments_bar(absp,label='absorp')
        plot.add_segments_bar(ppol,label='p-pol')
        plot.add_segments_bar(spol,label='s-pol')    

    if not 'tmp' in version:
        yyyy = prefix.split('-')[0]
        mm = prefix.split('-')[1]
        print('./img/{0}/{1}/{2}.png'.format(yyyy,mm,fname))    
        plot.savefig('./img/{0}/{1}/{2}.png'.format(yyyy,mm,fname))
    else:
        plot.savefig('tmp_{0}.png'.format(fname))    
    plot.close()


if __name__ == '__main__':
    from miyopy.gif.datatype import GifData
    from gwpy.time import tconvert, from_gps
    import argparse
    import timeit
    #
    # ----------------------------------------------------------------------    
    parser = argparse.ArgumentParser(
        prog='main.py', 
        #usage='%(prog)s May-01-2020-00:00JST May-01-2020-01:00JST Label',
        usage='%(prog)s [options]',
        description='Calculate duty cycle during specific period')
    parser.add_argument('-v', '--verbose',action='store_true',
                        help='Show verbose message')
    parser.add_argument('--prefix',type=str,
                        default='/Volumes/HDPF-UT/DATA',
                        help='Set prefix. default is /Volumes/HDPF-UT/DATA')
    parser.add_argument('--pk2pk',action='store_true',
                        help='Use pk-pk. default is not use. use contrast.')    
    parser.add_argument('start',
                        help='Start datetime like "May-01-2020-00:00JST"')
    parser.add_argument('end',
                        help='End datetime like "May-01-2020-01:00JST"')
    parser.add_argument('label',
                        help='Label')
    args = parser.parse_args()
    start = tconvert(args.start)
    end = tconvert(args.end)
    label = args.label
    verbose = args.verbose
    prefix = args.prefix
    pk2pk = args.pk2pk
    if verbose:
        print(args.start)        
    print(start,end,label,verbose,prefix,pk2pk)
    #
    # ----------------------------------------------------------------------    
    kwargs={'start':start,'end':end,'verbose':verbose,'nproc':1,    
            'format':'gif','pad':0.0}
    from miyopy.gif.datatype import GifData
    loop = 5
    print(timeit.timeit('GifData.findfiles(start,end,"PD_ABSORP_PXI01_5",'+\
                        'prefix=prefix)[0]', globals=globals(),number=loop)/loop)
    print(GifData.findfiles(start,end,'PD_ABSORP_PXI01_5',prefix=prefix)[0])


    
    exit()
    source = GifData.findfiles(start,end,'PD_ABSORP_PXI01_5',prefix=prefix)[0]
    absp = get(source,'PD_ABSORP_PXI01_5',**kwargs)
    source = [s.replace('.AD03','.AD00') for s in source]
    ppol = get(source,'PD_PPOL_PXI01_5',**kwargs)
    source = [s.replace('.AD00','.AD01') for s in source]
    spol = get(source,'PD_SPOL_PXI01_5',**kwargs)
    source = GifData.findfiles(start,end,'CALC_STRAIN',
                               prefix=prefix)[0]    
    strain = get(source,'CALC_STRAIN',**kwargs)
    strain = strain.resample(1)
    exit()
    # get contrast
    c_p = get_contrast(ppol,pk2pk=pk2pk)
    c_s = get_contrast(spol,pk2pk=pk2pk)
    
    # get statevector
    sv = get_statevector(absp,c_p,c_s) 
    
    # DutyCycle
    is_ok, is_locked, is_good, _, _ = sv
    dc = (float(is_ok.sum())/float(is_ok.shape[0]))
    dc_locked = (float(is_locked.sum())/float(is_locked.shape[0]))
    dc_good_contrast = (float(is_good.sum())/float(is_good.shape[0]))

    # Plot
    title = 'Duty cycle : {0:3.2f} %, {1:3.2f} %, {2:3.2f} %'.\
    format(dc*100,dc_locked*100,dc_good_contrast*100)
    plotkwargs = {'title':title,'start':start,'tmp':tmp,
                  'end':end,'sv':sv,'version':version}
    _min,_max = np.nanmin(strain),np.nanmax(strain)
    _mean = np.nanmean(strain)
    _std = np.nanstd(strain)    
    plot(strain,color='k',ylim=(_mean-2*_std,_mean+2*_std),**plotkwargs)
    plot(absp,color='g',ylim=(0,1),hlines=[0.2],**plotkwargs)
    plot(ppol,color='b',**plotkwargs)
    plot(spol,color='r',**plotkwargs)
    if pk2pk:
        plot(c_p,color='b',hlines=[0.01],ylim=(0,0.05),**plotkwargs)
        plot(c_s,color='r',hlines=[0.01],ylim=(0,0.05),**plotkwargs)
    else:
        plot(c_p,color='b',hlines=[0.02],ylim=(0,0.2),**plotkwargs)
        plot(c_s,color='r',hlines=[0.02],ylim=(0,0.2),**plotkwargs)
    
    
    if False:
        ppol = ppol.value[:300]
        spol = spol.value[:300]
        pmax,pmin = ppol.max(),ppol.min()
        smax,smin = spol.max(),spol.min()
        plt.clf()
        fig, ax = plt.subplots(1,1,figsize=(7,7))
        ax.plot(ppol,spol,'ko',markersize=2)
        #ax.set_ylim(0,0.3)
        #ax.set_xlim(0,0.3)
        ax.set_ylabel('spol [V]')
        ax.set_xlabel('ppol [V]')
        fname = str(from_gps(start))+'_UTC'
        fname = fname.replace(' ','_')
        plt.title(fname)
        #plt.savefig('tmp_lisa_{0}.png'.format(fname))
        plt.savefig('tmp_lisa.png')
        plt.close()
