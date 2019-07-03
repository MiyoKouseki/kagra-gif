import os
from gwpy.segments import SegmentList

fmt_gwf     = '{prefix}/{start}_{end}.gwf'
fmt_png_asd = '{prefix}/{start}_{end}_ASD.png'
fmt_png_ts  = '{prefix}/{start}_{end}_TS.png'
fmt_hdf5_sg = '{prefix}/{start}_{end}_{axis}.hdf5'


def fname_gwf(start,end,prefix):
    return fmt_gwf.format(prefix=prefix,start=start,end=end)

def fname_png_ts(start,end,prefix):
    return fmt_png_ts.format(prefix=prefix,start=start,end=end)

def fname_png_asd(start,end,prefix):
    return fmt_png_asd.format(prefix=prefix,start=start,end=end)

def fname_hdf5_sg(start,end,prefix,axis):
    return fmt_hdf5_sg.format(axis=axis,prefix=prefix,start=start,end=end)


def existance(args,ftype='gwf',prefix='./data',**kwargs):
    if isinstance(args,SegmentList):
        if ftype=="gwf":
            segmentlist = args
            fnames = [fname_gwf(start,end,prefix) for start,end in segmentlist]
        else:
            raise ValueError('!!')
        exists = [os.path.exists(fname) for fname in fnames]
        return exists
    elif isinstance(args,str):
        fname = args
        return os.path.exists(fname)
