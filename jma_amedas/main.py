import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy.time import Time

def main_May():    
    df_toyama1 = pd.read_csv("toyama0502.txt", header=0, delimiter='\t')
    df_toyama2 = pd.read_csv("toyama0503.txt", header=0, delimiter='\t')
    df_toyama = pd.concat([df_toyama1,df_toyama2])
    df_toyama =  df_toyama.loc[:,'pressure']
    df_toyama.reset_index(drop=True,inplace=True)
    #
    df_takayama1 = pd.read_csv("takayama0502.txt", header=0, delimiter='\t')
    df_takayama2 = pd.read_csv("takayama0503.txt", header=0, delimiter='\t')
    df_takayama = pd.concat([df_takayama1,df_takayama2])
    df_takayama =  df_takayama.loc[:,'pressure']
    df_takayama.reset_index(drop=True,inplace=True)
    #
    plt.figure()
    ax = df_toyama.plot()
    #ax = df_takayama.plot()
    plt.savefig("hoge.png")
    plt.close()


    

def main_Long():    
    df_toyama = pd.read_csv("toyama0101-0520.txt", header=0, delimiter=',')
    df_inotani = pd.read_csv("inotani0101-0520.txt", header=0, delimiter=',')
    df_kamioka = pd.read_csv("kamioka0101-0520.txt", header=0, delimiter=',')
    df_takayama = pd.read_csv("takayama0101-0520.txt", header=0, delimiter=',')
    df_kanazawa = pd.read_csv("kanazawa0101-0520.txt", header=0, delimiter=',')
    df_nigata = pd.read_csv("nigata0101-0520.txt", header=0, delimiter=',')
    df_shizuoka = pd.read_csv("shizuoka0101-0520.txt", header=0, delimiter=',')    
    df_toyama_water =  df_toyama.loc[:,'water']
    df_toyama_hPa =  df_toyama.loc[:,'hPa']
    df_takayama_water =  df_takayama.loc[:,'water']
    df_takayama_hPa =  df_takayama.loc[:,'hPa']
    df_kanazawa_water =  df_kanazawa.loc[:,'water']
    df_kanazawa_hPa =  df_kanazawa.loc[:,'hPa']
    df_nigata_water =  df_nigata.loc[:,'water']
    df_nigata_hPa =  df_nigata.loc[:,'hPa']        
    df_shizuoka_water =  df_shizuoka.loc[:,'water']
    df_shizuoka_hPa =  df_shizuoka.loc[:,'hPa']        
    df_inotani_water =  df_inotani.loc[:,'water']
    df_kamioka_water =  df_kamioka.loc[:,'water']
    #
    figure,(ax1,ax2) = plt.subplots(2,1,figsize=(9,5),dpi=500)
    box1 = ax1.get_position()
    ax1.set_position([box1.x0, box1.y0, box1.width * 0.75, box1.height])
    box2 = ax2.get_position()
    ax2.set_position([box2.x0, box2.y0, box2.width * 0.75, box2.height])
    df_toyama_water.plot(ax=ax2,alpha=0.1)
    df_takayama_water.plot(ax=ax2,alpha=0.1)
    #df_kanazawa_water.plot(ax=ax2)
    #df_nigata_water.plot(ax=ax2)
    df_shizuoka_water.plot(ax=ax2,alpha=0.1)
    df_inotani_water.plot(ax=ax2)
    df_kamioka_water.plot(ax=ax2)    
    #ax2.legend(['Toyama','Takayama','Kanazawa','Nigata','Shizuoka',"Inotani",'Kamioka'])
    ax2.legend(['Toyama','Takayama','Shizuoka',"Inotani",'Kamioka'],
               loc='upper left',
               bbox_to_anchor=(1.01,1), 
               borderaxespad=0.0)
    ax2.set_ylim([0,10])
    ax2.set_ylabel('Rainfall [mm]',fontsize=15)
    df_toyama_hPa.plot(ax=ax1)
    df_takayama_hPa.plot(ax=ax1)
    #df_kanazawa_hPa.plot(ax=ax1)
    #df_nigata_hPa.plot(ax=ax1)
    df_shizuoka_hPa.plot(ax=ax1)
    #ax1.legend(['Toyama(9m)','Takayama(560m)','Kanazawa(6m)','Nigata(4m)','Shizuoka(14m)'])
    lgd = ax1.legend(['Toyama(9m)','Takayama(560m)','Shizuoka(14m)'],
               loc='upper left',
               bbox_to_anchor=(1.01,1), 
               borderaxespad=0.0)
    #ax1.set_ylim([980,1040])
    ax1.set_ylabel('Pressure [hPa]',fontsize=15)
    plt.setp([a.get_xticklabels() for a in [ax1,ax2][:-1]], visible=False)
    gps2JST = lambda gps:Time(gps+3600*9, format='gps').utc.datetime
    from_ = 1-1 # from 4/20
    xticks = np.arange(0+from_*24,3360,24*10) # for 0101-0520
    #xticks = np.arange(0+from_*24,1200,24*4) # for 0101-0520
    xticklabels = gps2JST(1198767618+from_*24*3600+(xticks-xticks[0])*3600)  # from JST 01-01-00:00
    #xticklabels = gps2JST(1206543618+from_*24*3600+(xticks-xticks[0])*3600)  # from JST 04-01-00:00
    datetime2str = lambda x:x.strftime('%m/%d')
    xticklabels = map(datetime2str,xticklabels)
    figure.subplots_adjust(hspace=0.05)    
    ax2.set_xticks(xticks)    
    ax2.set_xticklabels(xticklabels,rotation=0,fontsize=10)
    ax1.set_xlim([xticks[0],xticks[-1]])
    ax2.set_xlim([xticks[0],xticks[-1]])
    plt.xlabel('date',fontsize=15)
    #plt.tight_layout()
    fname = 'JMA_Rainfall_Pressure'
    spt = plt.suptitle(fname,fontsize=20)
    plt.savefig(fname+'.png', bbox_extra_artists=(lgd,spt), bbox_inches='tight')
    plt.close()
    

def main_histogram_4year():
    thre_hPa = 1005
    df_toyama = pd.read_csv("toyama140520-180520.txt", header=0, delimiter=',')   
    df_toyama_hPa =  df_toyama.loc[:,'hPa']
    fname='timeseries'
    figure,(ax1,ax2) = plt.subplots(1,2,figsize=(9,3),dpi=500)
    figure.subplots_adjust(wspace=0.05)                
    plt.setp([a.get_yticklabels() for a in [ax1,ax2][-1:]], visible=False)    
    box1 = ax1.get_position()
    ax1.set_position([box1.x0, box1.y0, box1.width * 1.4, box1.height])
    box2 = ax2.get_position()
    ax2.set_position([box1.x0+box1.width*1.5,
                      box2.y0,
                      box2.width * 0.3,
                      box2.height])
    gps2JST = lambda gps:Time(gps+3600*9, format='gps').utc.datetime
    xticks = np.arange(0,df_toyama_hPa.size+24*30*6,24*30*6) #
    xticklabels = gps2JST(1084546816+(xticks-xticks[0])*3600) # JST 2018-05-20-00:00
    datetime2str = lambda x:x.strftime('%Y\n%m/%d')
    xticklabels = map(datetime2str,xticklabels)
    df_toyama_hPa.plot(ax=ax1,color='k',alpha=0.8,linewidth=0.7)
    ax1.hlines(thre_hPa,0, df_toyama_hPa.size*1.4, "black", linestyles=':',linewidth=2) 
    ax1.set_ylim(980,1040)
    ax1.set_xticks(xticks)    
    ax1.set_xticklabels(xticklabels,rotation=0,fontsize=10)
    ax1.set_xlim([xticks[0],xticks[-1]])
    ax1.set_ylabel('Pressure [hPa]',fontsize=15)
    ax1.set_xlabel('Date',fontsize=15)
    ax1.legend(['Toyama'],loc='upper right')
    #plt.savefig(fname+'.png', bbox_inches='tight')
    #plt.close()    
    #
    #
    #ax2 = plt.axes([0.55, 0.55, 0.3, 0.3])
    n,bins,_ = ax2.hist(df_toyama_hPa,
                        bins=50,color='k',
                        histtype='step',normed=False,
                        orientation="horizontal")    
    nmax = n.max()
    index = np.where(bins>thre_hPa)[0]
    n[index-1] = 0.0
    print bins
    print n
    ax2.step(n,bins[:-1],color='red',where='pre')
    count = (df_toyama_hPa < thre_hPa).sum()
    #print (n[index-1]).sum()
    rate = float(count)/df_toyama_hPa.size
    print rate
    ax2.text(nmax*0.45,thre_hPa-10,'{0:2.0f}%'.format(rate*100))
    ax2.hlines(thre_hPa, 0,nmax*1.4 , "black", linestyles=':',linewidth=2)
    ax2.set_xlim(0,nmax*1.4)
    ax2.set_ylim(980,1040)
    fname = 'histogram'
    #ax2.set_ylabel('Pressure [hPa]')
    ax2.set_xlabel('Count',fontsize=15)
    ax2.xaxis.set_label_coords(0.5,-0.2)        
    ax1.set_xlabel('Date',fontsize=15)
    ax1.xaxis.set_label_coords(0.5,-0.2)    
    plt.savefig(fname+'.png', bbox_inches='tight')
    plt.close()

def main_histogram():
    thre_hPa = 1005
    df_toyama = pd.read_csv("toyama0422-0506.txt", header=0, delimiter=',')
    #df_toyama = pd.read_csv("toyama0428-0506.txt", header=0, delimiter=',')
    df_toyama_hPa = df_toyama.loc[:,'hPa']
    fname='timeseries'
    figure,(ax1,ax2) = plt.subplots(1,2,figsize=(9,3),dpi=500)
    figure.subplots_adjust(wspace=0.05)                
    plt.setp([a.get_yticklabels() for a in [ax1,ax2][-1:]], visible=False)    
    box1 = ax1.get_position()
    ax1.set_position([box1.x0, box1.y0, box1.width * 1.4, box1.height])
    box2 = ax2.get_position()
    ax2.set_position([box1.x0+box1.width*1.5,
                      box2.y0,
                      box2.width * 0.3,
                      box2.height])
    gps2JST = lambda gps:Time(gps+3600*9, format='gps').utc.datetime
    xticks = np.arange(0,df_toyama_hPa.size+48,24*2) #
    print xticks,'---'
    print df_toyama.size
    xticklabels = gps2JST(1208876418+(xticks-xticks[0])*3600) # JST 2018-04-28-00:00
    xticklabels = gps2JST(1208358018+(xticks-xticks[0])*3600) # JST 2018-04-22-00:00    
    datetime2str = lambda x:x.strftime('%Y\n%m/%d')
    xticklabels = map(datetime2str,xticklabels)
    print xticklabels    
    df_toyama_hPa.plot(ax=ax1,color='k',alpha=0.8,linewidth=0.7)
    ax1.hlines(thre_hPa,0, df_toyama_hPa.size*1.4, "black", linestyles=':',linewidth=2) 
    ax1.set_ylim(980,1040)
    ax1.set_xticks(xticks)    
    ax1.set_xticklabels(xticklabels,rotation=0,fontsize=10)
    ax1.set_xlim([xticks[0],xticks[-1]])
    ax1.set_ylabel('Pressure [hPa]',fontsize=15)
    ax1.set_xlabel('Date',fontsize=15)
    ax1.legend(['Toyama'],loc='upper right')
    #plt.savefig(fname+'.png', bbox_inches='tight')
    #plt.close()    
    #
    #
    #ax2 = plt.axes([0.55, 0.55, 0.3, 0.3])
    n,bins,_ = ax2.hist(df_toyama_hPa,
                        bins=50,color='k',
                        histtype='step',normed=False,
                        orientation="horizontal")    
    nmax = n.max()
    index = np.where(bins>thre_hPa)[0]
    n[index-1] = 0.0
    print bins
    print n
    ax2.step(n,bins[:-1],color='red',where='pre')
    count = (df_toyama_hPa < thre_hPa).sum()
    #print (n[index-1]).sum()
    rate = float(count)/df_toyama_hPa.size
    print rate
    ax2.text(nmax*0.45,thre_hPa-10,'{0:2.0f}%'.format(rate*100))
    ax2.hlines(thre_hPa, 0,nmax*1.4 , "black", linestyles=':',linewidth=2)
    ax2.set_xlim(0,nmax*1.4)
    ax2.set_ylim(980,1040)
    fname = 'histogram'
    #ax2.set_ylabel('Pressure [hPa]')
    ax2.set_xlabel('Count',fontsize=15)
    ax2.xaxis.set_label_coords(0.5,-0.2)        
    ax1.set_xlabel('Date',fontsize=15)
    ax1.xaxis.set_label_coords(0.5,-0.2)    
    plt.savefig(fname+'.png', bbox_inches='tight')
    plt.close()

    
if __name__ == '__main__':
    #main_May()
    #main_Long()
    main_histogram_4year()
    #main_histogram()
    
