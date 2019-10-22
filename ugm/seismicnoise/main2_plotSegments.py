import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

    
def plotpi(gauss,nonegauss,lack,seis):
    data = [len(gauss),len(nonegauss),len(lack)]
    label = ['Gaussian','Non-Gaussian','Lack of Data']
    fig,ax=plt.subplots(1,1,figsize=(7,3))
    wedges,texts,autotexts = ax.pie(
        data,startangle=90,counterclock=False,
        wedgeprops={'linewidth':1, 'edgecolor':"black"},
        autopct="%1.1f%%",textprops=dict(color="w"),colors=['g','y','red'])
    ax.legend(wedges, label,title="Conditions of the \nData Segments",
              loc="center left",bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=12, weight="bold")
    plt.title(seis)
    fname = './results/segmentpi_{0}.png'.format(seis)
    print(fname)    
    plt.savefig(fname)
    plt.close()

    
def plotlist(total,gauss,nonegauss,lack,seis):
    fname = './results/segmentlist_{0}.png'.format(seis)
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
    print(fname)
    plt.title(seis)
    plt.savefig(fname)

    

from dataquality.dataquality import DataQuality
fmt_total = 'select startgps,endgps from {2} WHERE ' +\
            '(startgps>={0} and endgps<={1})'
fmt_lack = 'select startgps,endgps from {2} WHERE (flag=2 or flag=4) and' +\
           '(startgps>={0} and endgps<={1})'
fmt_gauss = 'select startgps,endgps from {2} WHERE flag=0 and ' +\
            '(startgps>={0} and endgps<={1})'
fmt_nonegauss = 'select startgps,endgps from {2} WHERE flag=8 and ' +\
                '(startgps>={0} and endgps<={1})'

start,end = 1211817600, 1245372032                
seislist = ['EXV_SEIS','IXV_SEIS','IXVTEST_SEIS','MCE_SEIS','MCF_SEIS','BS_SEIS']
for seis in seislist:
    with DataQuality('./dataquality/dqflag.db') as db:
        total = db.ask(fmt_total.format(start,end,seis))
        gauss = db.ask(fmt_gauss.format(start,end,seis))
        nonegauss = db.ask(fmt_nonegauss.format(start,end,seis))
        lack = db.ask(fmt_lack.format(start,end,seis))    
        plotpi(gauss,nonegauss,lack,seis)
        plotlist(total,gauss,nonegauss,lack,seis)        
