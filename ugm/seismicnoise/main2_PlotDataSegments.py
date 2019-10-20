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
    normal     = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=0')
    lack       = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=2 or flag=4')
    non_normal = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=8')
    use        = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=0 ' +
                        'and startgps>={0} and endgps<={1}'.format(args.start,args.end))

plot_pi = True
if plot_pi:
    data = [len(normal),len(non_normal),len(lack)]
    label = ['Gaussian','Non-Gaussian','Lack of Data']
    #fig,ax=plt.subplots(1,1,figsize=(7,3),subplot_kw=dict(aspect="equal"))
    fig,ax=plt.subplots(1,1,figsize=(7,3))
    wedges, texts, autotexts = ax.pie(data,startangle=90,counterclock=False,
                                      wedgeprops={'linewidth':1, 'edgecolor':"black"},
                                      autopct="%1.1f%%",textprops=dict(color="w"))
    ax.legend(wedges, label,title="Conditions of the \nData Segments",
              loc="center left",bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=12, weight="bold")
    plt.savefig('./results/segmentpi.png')
    plt.close()
    

plot_segmentlist = True
if plot_segmentlist:
    fname = './results/segmentlist.png'
    start, end = total[0][0],total[-1][1]
    from gwpy.segments import DataQualityFlag
    normal = DataQualityFlag(name='Gaussian ({0})'.format(len(normal)),
                             active=normal,
                             known=[(start,end)])
    lack = DataQualityFlag(name='Lack of Data ({0})'.format(len(lack)),
                           active=lack,
                           known=[(start,end)])
    non_normal = DataQualityFlag(name='Non-Gaussian ({0})'.format(len(non_normal)),
                                 active=non_normal,known=[(start,end)])
    total = DataQualityFlag(name='Total ({0})'.format(len(total)),
                            active=total,known=[(start,end)])
    args = normal,non_normal,lack,total
    start = args[0].known[0].start
    end = args[0].known[0].end
    plot = args[0].plot(figsize=(14,5),epoch=start,xlim=(start,end))
    ax = plot.gca()
    for data in args[1:]:
        ax.plot(data,label=data.name)
    ax.set_xlim(start,end)
    plt.savefig(fname)

