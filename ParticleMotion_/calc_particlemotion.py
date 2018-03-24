#
#! coding:utf-8
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import matplotlib
import numpy as np
from  check_fw import is_record_in_fw0
import sys
sys.path.append("./miyopy/miyopy")
#from  miyopy.miyopy.mpio import fetch_data, dump, load
from  mpio import fetch_data, dump, load

#exit()
# init 
chlst_fname = '1.chlst'
#start = 1205201472 # 03/16 11
start = 1205810784 # 03/23 12
start = 1204969376 # 03/13 10:00:00 (UTC)
#duration = 4096 # sec
duration = 23040 # sec
#duration = 55872
pickle_fname = './{0}_{1}_{2}.pickle'.format(start,duration,chlst_fname.split('.chlst')[0])
# get chlst
with open(chlst_fname,'r') as f:
    chlst = f.read().splitlines()    
    chdic = {str(ch):i for i,ch in enumerate(chlst)}
# get data
start,duration = is_record_in_fw0(start,duration)
#data = fetch_data(start,start+duration,chlst)
#dump(pickle_fname,data)
data = load(pickle_fname)

def plot_3seisNS_30secTimeseries():
    start,end = 30,60
    time = np.arange((end-start)*16)/16.0
    func = lambda x,s_sec,e_sec : x[s_sec*16:e_sec*16]
    #
    # plot
    fig, ax1 = plt.subplots(figsize=(10,3))
    box = ax1.get_position()
    ax1.set_position([box.x0, box.y0*1.5, box.width * 0.7, box.height*0.9])
    index = chdic['K1:PEM-EX1_SEIS_NS_SENSINF_OUT16']
    seis = data[index]
    print len(seis)
    seis = func(seis,start,end)
    ax1.plot(time,seis,label=chlst[index],color='b')
    ax1.ticklabel_format(style="sci",  axis="y",scilimits=(0,0))
    index = chdic['K1:PEM-EY1_SEIS_NS_SENSINF_OUT16']
    seis = data[index]
    seis = func(seis,start,end)
    ax1.plot(time,seis,label=chlst[index],color='r')
    index = chdic['K1:PEM-IY0_SEIS_NS_SENSINF_OUT16']
    seis = data[index]
    seis = func(seis,start,end)
    ax1.plot(time,seis,label=chlst[index],color='g')
    ax1.legend(bbox_to_anchor=(1.1,1), loc='upper left', borderaxespad=0, fontsize=8)
    #
    ax2 = ax1.twinx()
    box = ax2.get_position()
    ax2.set_position([box.x0, box.y0*1.5, box.width * 0.7, box.height*0.9])
    index = chdic['K1:PEM-EX1_SEIS_NS_SENSINF_SWSTAT']
    seis = data[index]
    seis = func(seis,start,end)
    ax2.semilogy(time,seis,label=chlst[index],color='b',basey=2,linestyle=':')
    index = chdic['K1:PEM-EY1_SEIS_NS_SENSINF_SWSTAT']
    seis = data[index]
    seis = func(seis,start,end)
    ax2.semilogy(time,seis,label=chlst[index],color='r',basey=2,linestyle=':')
    index = chdic['K1:PEM-IY0_SEIS_NS_SENSINF_SWSTAT']
    seis = data[index]
    seis = func(seis,start,end)
    ax2.semilogy(time,seis,label=chlst[index],color='g',basey=2,linestyle=':')
    ax2.legend(bbox_to_anchor=(1.1, 0), loc='lower left', borderaxespad=0, fontsize=8)
    ax1.set_xlabel('Time [sec]')
    ax1.set_ylabel('Velocity [m/sec]')
    ax2.set_ylabel('Count')
    plt.savefig('hoge.png')
    plt.close()


def plot_particleMotion():
    start,end = 0,10
    time = np.arange((end-start)*16)/16.0
    func = lambda x,s_sec,e_sec : x[s_sec*16:e_sec*16]
    index = chdic['K1:PEM-EY1_SEIS_NS_SENSINF_OUT16']
    seis1 = data[index]
    seis1 = func(seis1,start,end)
    index = chdic['K1:PEM-EY1_SEIS_WE_SENSINF_OUT16']
    seis2 = data[index]
    seis2 = func(seis2,start,end)
    plt.plot(seis1,seis2)
    plt.savefig('huge.png')
    plt.close()

def anime():
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    fig = plt.figure()
    rand = [np.random.randn() for i in range(100)]
    start,end = 0,30
    time = np.arange((end-start)*16)/16.0
    func = lambda x,s_sec,e_sec : x[s_sec*16:e_sec*16]
    index = chdic['K1:PEM-EX1_SEIS_NS_SENSINF_OUT16']
    seis1x = data[index]
    seis1x = func(seis1x,start,end)
    index = chdic['K1:PEM-EX1_SEIS_WE_SENSINF_OUT16']
    seis2x = data[index]
    seis2x = func(seis2x,start,end)

    def plot(i):
        plt.cla()                      # 現在描写されているグラフを消去
        #plt.xlim(-1e-6,1e-6)
        #plt.ylim(-1e-6,1e-6)
        plt.plot(seis1x[i],seis2x[i])            # グラフを生成
    ani = animation.FuncAnimation(fig, plot, interval=100)
    ani.save("output.gif", writer="imagemagick")


def main():    
    import matplotlib.animation as anm
    import matplotlib.pyplot as plt
    import numpy as np
    
    fig = plt.figure(figsize = (10, 6))
    w, h = fig.get_figwidth(), fig.get_figheight()
    ax = fig.add_axes((0.5 - 0.5 * 0.8 * h / w, 0.1, 0.8 * h / w, 0.8))
    aspect = (ax.get_xlim()[1] - ax.get_xlim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0])                     
    ax.set_aspect(aspect)
    x = np.arange(0, 10, 0.1)

    start,end = 0,30
    time = np.arange((end-start)*16)/16.0
    func = lambda x,s_sec,e_sec : x[s_sec*16:e_sec*16]
    index = chdic['K1:PEM-EY1_SEIS_NS_SENSINF_OUT16']
    seis1y = data[index]
    seis1y = func(seis1y,start,end)
    index = chdic['K1:PEM-EY1_SEIS_WE_SENSINF_OUT16']
    seis2y = data[index]
    seis2y = func(seis2y,start,end)    
    
    
    def update(i, fig_title, A):
        if i != 0:
            plt.cla()
        plt.xlim(-1e-6,1e-6)
        plt.ylim(-1e-6,1e-6)
        plt.plot(seis1y[i], seis2y[i], "ro",markersize=5)
        plt.title(fig_title + 'i=' + str(i))
        
    ani = anm.FuncAnimation(fig, update, fargs = ('Initial Animation! ', 2.0),
                            interval = 10, frames = len(seis1y))    
    ani.save("Sample.gif", writer = 'imagemagick')
    
if __name__ == '__main__':
    main()
    exit()
    #plot_3seisNS_30secTimeseries()
    #plot_particleMotion()
    anime()
    exit()
    import math
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    #
    start,end = 0,30
    time = np.arange((end-start)*16)/16.0
    func = lambda x,s_sec,e_sec : x[s_sec*16:e_sec*16]
    index = chdic['K1:PEM-EX1_SEIS_NS_SENSINF_OUT16']
    seis1x = data[index]
    seis1x = func(seis1x,start,end)
    index = chdic['K1:PEM-EX1_SEIS_WE_SENSINF_OUT16']
    seis2x = data[index]
    seis2x = func(seis2x,start,end)    
    #
    start,end = 0,30
    time = np.arange((end-start)*16)/16.0
    func = lambda x,s_sec,e_sec : x[s_sec*16:e_sec*16]
    index = chdic['K1:PEM-EY1_SEIS_NS_SENSINF_OUT16']
    seis1y = data[index]
    seis1y = func(seis1y,start,end)
    index = chdic['K1:PEM-EY1_SEIS_WE_SENSINF_OUT16']
    seis2y = data[index]
    seis2y = func(seis2y,start,end)    
    #
    start,end = 0,30
    time = np.arange((end-start)*16)/16.0
    func = lambda x,s_sec,e_sec : x[s_sec*16:e_sec*16]
    index = chdic['K1:PEM-IY0_SEIS_NS_SENSINF_OUT16']
    seis1c = data[index]
    seis1c = func(seis1c,start,end)
    index = chdic['K1:PEM-IY0_SEIS_WE_SENSINF_OUT16']
    seis2c = data[index]
    seis2c = func(seis2c,start,end)    
    #
