import os
from gwpy.segments import SegmentList

fmt_gwf     = '{prefix}/{gps5}/{start}_{end}.gwf'
fmt_png_asd = '{prefix}/{gps5}/{start}_{end}_ASD.png'
fmt_png_ts  = '{prefix}/{gps5}/{start}_{end}_TS.png'
fmt_hdf5_sg = '{prefix}/{gps5}/{start}_{end}_{axis}.hdf5'
fmt_hdf5_percentile = './data2/{prefix}/{axis}_{percentile}{suffix}.hdf5'
fmt_hdf5_asd = '{prefix}/{gps5}/{start}_{end}_{axis}.hdf5'
fmt_hdf5_diffasd = '{prefix}/{gps5}/DIFF_{start}_{end}_{axis}.hdf5'
fmt_specgram = './data/{prefix}/{gps5}/{start}_{end}_{axis}.hdf5'

def fname_gwf(start,end,prefix):
    gps5 = str(start)[:5]
    return fmt_gwf.format(prefix=prefix,gps5=gps5,start=start,end=end)

def fname_png_ts(start,end,prefix):
    gps5 = str(start)[:5]
    return fmt_png_ts.format(prefix=prefix,gps5=gps5,start=start,end=end)

def fname_png_asd(start,end,prefix):
    gps5 = str(start)[:5]
    return fmt_png_asd.format(prefix=prefix,gps5=gps5,start=start,end=end)

def fname_hdf5_sg(start,end,prefix,axis):
    gps5 = str(start)[:5]
    return fmt_hdf5_sg.format(axis=axis,prefix=prefix,gps5=gps5,start=start,end=end)

def fname_hdf5_percentile(axis,percentile,prefix='./data',suffix=''):
    return fmt_hdf5_percentile.format(prefix=prefix,axis=axis,
                                      percentile=percentile,suffix=suffix)

def fname_hdf5_asd(start,end,prefix,axis):
    gps5 = str(start)[:5]
    return fmt_hdf5_asd.format(prefix=prefix,gps5=gps5,start=start,end=end,axis=axis)

def fname_specgram(start,end,prefix,axis):
    gps5 = str(start)[:5]
    return fmt_specgram.format(prefix=prefix,gps5=gps5,start=start,end=end,axis=axis)


def fname_hdf5_diffasd(start,end,prefix,axis):
    gps5 = str(start)[:5]
    return fmt_hdf5_diffasd.format(prefix=prefix,gps5=gps5,start=start,end=end,axis=axis)


def existance(args,ftype='gwf',prefix='./data',**kwargs):
    if isinstance(args,SegmentList):
        if ftype=="gwf":
            segmentlist = args
            fnames = [fname_gwf(start,end,prefix) for start,end in segmentlist]
        elif ftype=="png_ts":
            segmentlist = args
            fnames = [fname_png_ts(start,end,prefix) for start,end in segmentlist]
        else:
            raise ValueError('!!')
        exists = [os.path.exists(fname) for fname in fnames]
        return exists
    elif isinstance(args,str):
        fname = args
        return os.path.exists(fname)
