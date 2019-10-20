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
fmt_total = 'select startgps,endgps from {2} WHERE ' +\
  '(startgps>={0} and endgps<={1})'
fmt_lack = 'select startgps,endgps from {2} WHERE (flag=2 or flag=4) and' +\
  '(startgps>={0} and endgps<={1})'
fmt_lack_day   = 'select startgps,endgps from {2} WHERE (flag=2 or flag=4) and ' +\
  '(startgps>={0} and endgps<={1}) and ' +\
  '(((startgps-18)%86400)>=0) and (((startgps-18)%86400)<43200)'
fmt_lack_night = 'select startgps,endgps from {2} WHERE (flag=2 or flag=4) and ' +\
  '(startgps>={0} and endgps<={1}) and ' +\
  '(((startgps-18)%86400)>=43200) and (((startgps-18)%86400)<86400)'  
fmt_gauss = 'select startgps,endgps from {2} WHERE flag=0 and ' +\
  '(startgps>={0} and endgps<={1})'
fmt_gauss_day   = 'select startgps,endgps from {2} WHERE flag=0 and ' +\
  '(startgps>={0} and endgps<={1}) and ' +\
  '(((startgps-18)%86400)>=0) and (((startgps-18)%86400)<43200)'
fmt_gauss_night = 'select startgps,endgps from {2} WHERE flag=0 and ' +\
  '(startgps>={0} and endgps<={1}) and ' +\
  '(((startgps-18)%86400)>=43200) and (((startgps-18)%86400)<86400)'
fmt_nonegauss = 'select startgps,endgps from {2} WHERE flag=8 and ' +\
  '(startgps>={0} and endgps<={1})'
fmt_nonegauss_day   = 'select startgps,endgps from {2} WHERE flag=8 and ' +\
  '(startgps>={0} and endgps<={1}) and ' +\
  '(((startgps-18)%86400)>=0) and (((startgps-18)%86400)<43200)'
fmt_nonegauss_night = 'select startgps,endgps from {2} WHERE flag=8 and ' +\
  '(startgps>={0} and endgps<={1}) and ' +\
  '(((startgps-18)%86400)>=43200) and (((startgps-18)%86400)<86400)'
  
with DataQuality('./dataquality/dqflag.db') as db:
    total = db.ask(fmt_total.format(args.start,args.end,'EXV_SEIS'))
    lack = db.ask(fmt_lack.format(args.start,args.end,'EXV_SEIS'))
    lack_day = db.ask(fmt_lack_day.format(args.start,args.end,'EXV_SEIS'))
    lack_night = db.ask(fmt_lack_night.format(args.start,args.end,'EXV_SEIS'))    
    gauss = db.ask(fmt_gauss.format(args.start,args.end,'EXV_SEIS'))
    gauss_day   = db.ask(fmt_gauss_day.format(args.start,args.end,'EXV_SEIS'))
    gauss_night = db.ask(fmt_gauss_night.format(args.start,args.end,'EXV_SEIS'))
    nonegauss = db.ask(fmt_nonegauss.format(args.start,args.end,'EXV_SEIS'))
    nonegauss_day   = db.ask(fmt_nonegauss_day.format(args.start,args.end,'EXV_SEIS'))
    nonegauss_night = db.ask(fmt_nonegauss_night.format(args.start,args.end,'EXV_SEIS'))            
plot_pi = True
if plot_pi:
    data = [len(gauss),len(nonegauss),len(lack)]
    #data = [len(gauss_day),len(nonegauss_day),len(lack_day)]
    #data = [len(gauss_night),len(nonegauss_night),len(lack_night)]
    label = ['Gaussian','Non-Gaussian','Lack of Data']
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
    gauss,lack,nonegauss = gauss,lack,nonegauss
    #gauss,lack,nonegauss = gauss_day,lack_day,nonegauss_day    
    #gauss,lack,nonegauss = gauss_night,lack_night,nonegauss_night
    start, end = total[0][0],total[-1][1]
    from gwpy.segments import DataQualityFlag
    gauss = DataQualityFlag(name='Gaussian ({0})'.format(len(gauss)),
                             active=gauss,
                             known=[(start,end)])
    lack = DataQualityFlag(name='Lack of Data ({0})'.format(len(lack)),
                           active=lack,
                           known=[(start,end)])
    nonegauss = DataQualityFlag(name='Non-Gaussian ({0})'.format(len(nonegauss)),
                                 active=nonegauss,known=[(start,end)])
    total = DataQualityFlag(name='Total ({0})'.format(len(total)),
                            active=total,known=[(start,end)])
    args = gauss,nonegauss,lack,total
    start = args[0].known[0].start
    end = args[0].known[0].end
    plot = args[0].plot(figsize=(14,5),epoch=start,xlim=(start,end))
    ax = plot.gca()
    for data in args[1:]:
        ax.plot(data,label=data.name)
    ax.set_xlim(start,end)
    plt.savefig(fname)

