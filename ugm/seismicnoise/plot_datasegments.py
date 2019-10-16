import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import traceback


import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--start',type=int,default=1211817600)
parser.add_argument('--end',type=int,default=1245372032)
parser.add_argument('--nproc',type=int,default=8)
parser.add_argument('--percentile', action='store_false')
parser.add_argument('--alldata', action='store_false')
args = parser.parse_args()
nproc = args.nproc
run_percentile = args.percentile
alldata = args.alldata
if args.start!=1211817600 or args.end!=1245372032:
    alldata = True 
    

from dataquality.dataquality import DataQuality
with DataQuality('./dataquality/dqflag.db') as db:
    total      = db.ask('select startgps,endgps from EXV_SEIS')
    available  = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=0')
    lackoffile = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=2')
    lackofdata = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=4')
    glitch     = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=8')
    use        = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=0 ' +
                        'and startgps>={0} and endgps<={1}'.format(args.start,args.end))

bad = len(total)-len(available)-len(lackoffile)-len(lackofdata)-len(glitch)

if True:
    data = [len(available),len(glitch),len(lackoffile)+len(lackofdata)]
    label = ['Stationary Data','Glitch Data','Lack of Data']
    fig,ax=plt.subplots(1,1,figsize=(6,3),subplot_kw=dict(aspect="equal"))
    wedges, texts, autotexts = ax.pie(data,startangle=90,counterclock=False,wedgeprops={'linewidth': 1, 'edgecolor':"black"},autopct="%1.1f%%",textprops=dict(color="w"))
    ax.legend(wedges, label,
              title="Data Condition",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=8, weight="bold")
    plt.tight_layout()
    plt.savefig('segmentpi.png')
    plt.close()
    
if bad!=0:
    raise ValueError('SegmentList Error: Missmatch the number of segments.')    

# Plot segmentlist
if True:
    fname = './segmentlist.png'
    start, end = total[0][0],total[-1][1]
    from gwpy.segments import DataQualityFlag
    available = DataQualityFlag(name='Available',active=available,
                                   known=[(start,end)])
    lackoffile = DataQualityFlag(name='No Frame Files',active=lackoffile,
                                    known=[(start,end)])
    lackofdata = DataQualityFlag(name='Lack of Data',active=lackofdata,
                                    known=[(start,end)])
    lack = lackofdata | lackoffile
    glitch = DataQualityFlag(name='Glitch',active=glitch,known=[(start,end)])
    total = DataQualityFlag(name='Total',active=total,known=[(start,end)])
    args = available,glitch,lack,total
    start = args[0].known[0].start
    end = args[0].known[0].end
    plot = args[0].plot(figsize=(8,5),epoch=start,xlim=(start,end))
    ax = plot.gca()
    for data in args[1:]:
        ax.plot(data,label=data.name)
    ax.set_xlim(start,end)
    plt.savefig(fname)

