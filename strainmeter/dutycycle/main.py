from gwpy.timeseries import TimeSeries
from astropy import units as u
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------

def get(source,chname,**kwargs):   
    data = TimeSeries.read(source,name=chname,**kwargs)
    data.name = chname
    return data

def get_contrast(data,**kwargs):
    pk2pk = kwargs.pop('pk2pk',True)
    chname = data.name
    shape = data.shape[0]
    hoge = data.reshape(int(shape/300),300)
    _max = hoge.max(axis=1)
    _min = hoge.min(axis=1)
    if pk2pk:
        _contrast = _max-_min
        _contrast.name = data.name+'_PK2PK'
    else:
        _contrast = (_max**2-_min**2)/(_max**2+_min**2)
        _contrast.name = data.name+'_CONTRAST'        
    _contrast.dt=60*u.s    
    return _contrast

def get_statevector(absp,c_p,c_s):
    shape = absp.shape[0]
    hoge = absp.reshape(int(shape/300),300)
    absp_min = hoge.min(axis=1)    
    is_locked = absp_min > 0.200*u.V
    is_locked.dt=60*u.s        
    is_good_contrast_p = c_p > 0.01*u.V
    is_good_contrast_s = c_s > 0.01*u.V
    is_ok = is_locked * is_good_contrast_p * is_good_contrast_s
    return is_ok

def plot(data,**kwargs):
    ylim = kwargs.pop('ylim',(0.0,0.3))
    color = kwargs.pop('color','k')
    is_ok = kwargs.pop('sv',None)
    title = kwargs.pop('title',None)
    hlines = kwargs.pop('hlines',None)
    #plot = data.plot()
    prefix = '{0}-{1}-'.format(str(from_gps(start)).split(' ')[0],
                              str(from_gps(end)).split(' ')[0])
    fname = data.name.lower()
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
        plot.add_segments_bar(obs,label='Observing')    
    plot.savefig('tmp_{0}.png'.format(fname))
    yyyy = prefix.split('-')[0]
    mm = prefix.split('-')[1]
    print('./img/{0}/{1}/{2}.png'.format(yyyy,mm,fname))    
    plot.savefig('./img/{0}/{1}/{2}.png'.format(yyyy,mm,fname))        
    plot.close()


if __name__ == '__main__':
    from miyopy.gif.datatype import GifData
    from gwpy.time import tconvert, from_gps
    import argparse
    #
    parser = argparse.ArgumentParser(
        prog='argparseTest.py', 
        usage='Demonstration of argparser',
        description='description',
        epilog='end',
        add_help=True,
        )
    parser.add_argument('-v', '--verbose', help='select mode')
    parser.add_argument('start', help='start')
    parser.add_argument('end', help='end')
    args = parser.parse_args()
    print(args.start)    
    start = tconvert(args.start)
    end = tconvert(args.end)
    
    # load    
    #start = tconvert('Jun-01-2017-00:00')
    #end   = tconvert('Jul-01-2017-00:00')
    prefix = '/Users/miyo/Git/kagra-gif/strainmeter/dutycycle'
    kwargs={'start':start,'end':end,'verbose':True,'nproc':1,    
            'format':'gif','pad':0.0}
    from miyopy.gif.datatype import GifData
    source = GifData.findfiles(start,end,'PD_ABSORP_PXI01_5',prefix=prefix)[0]
    absp = get(source,'PD_ABSORP_PXI01_5',**kwargs)
    source = [s.replace('.AD03','.AD00') for s in source]
    source = GifData.findfiles(start,end,'PD_PPOL_PXI01_5',prefix=prefix)[0]
    ppol = get(source,'PD_PPOL_PXI01_5',**kwargs)
    source = [s.replace('.AD00','.AD01') for s in source]
    source = GifData.findfiles(start,end,'PD_SPOL_PXI01_5',prefix=prefix)[0]
    spol = get(source,'PD_SPOL_PXI01_5',**kwargs)
    # get contrast
    c_p = get_contrast(ppol)
    c_s = get_contrast(spol)
    
    # get statevector
    is_ok = get_statevector(absp,c_p,c_s)
    
    # DutyCycle
    dc = (float(is_ok.sum())/float(is_ok.shape[0]))

    # Plot
    title = 'Duty cycle : {0:3.2f} %'.format(dc*100)
    plotkwargs = {'title':title,'start':start,'end':end,'sv':is_ok}
    plot(absp,color='k',ylim=(0,1),hlines=[0.2],**plotkwargs)
    plot(ppol,color='b',**plotkwargs)
    plot(spol,color='r',**plotkwargs)
    plot(c_p,color='b',hlines=[0.01],ylim=(0,0.1),**plotkwargs)
    plot(c_s,color='r',hlines=[0.01],ylim=(0,0.1),**plotkwargs)
    
    if False:
        ppol = ppol.value[:300]
        spol = spol.value[:300]
        pmax,pmin = ppol.max(),ppol.min()
        smax,smin = spol.max(),spol.min()
        plt.clf()
        fig, ax = plt.subplots(1,1,figsize=(7,7))
        ax.plot(ppol,spol,'ko',markersize=2)
        ax.set_ylim(0,0.3)
        ax.set_xlim(0,0.3)
        ax.set_ylabel('spol [V]')
        ax.set_xlabel('ppol [V]')
        fname = str(from_gps(start))+'_UTC'
        fname = fname.replace(' ','_')
        plt.title(fname)
        #plt.savefig('tmp_lisa_{0}.png'.format(fname))
        plt.savefig('tmp_lisa.png')
        plt.close()
