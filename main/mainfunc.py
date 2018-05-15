#
#! coding:utf-8

def main_plotSEismometerSepctrogram(*args):
    theta = 0
    ave = 16
    ex1 = Seismometer(t0,tlen,'EX1',theta=theta)    
    ey1 = Seismometer(t0,tlen,'EY1',theta=theta)
    cen = Seismometer(t0,tlen,'IY0',theta=theta)
    # Yend-Xend
    if True:
        from spectrogram import spectrogram
        sec = 1
        wlen = 128
        clip = [0,1]
        print title
        # Xend
        spectrogram(ex1.x.timeseries,ex1.x._fs,outfile='{0}/Spectrogram_{1}_{2}_{3}.png'.format(title,t0,tlen,ex1.x._name),wlen=wlen,log=True,clip=clip,per_lap=0.9)
        spectrogram(ex1.y.timeseries,ex1.y._fs,outfile='{0}/Spectrogram_{1}_{2}_{3}.png'.format(title,t0,tlen,ex1.y._name),wlen=wlen,log=True,clip=clip,per_lap=0.9)
        spectrogram(ex1.z.timeseries,ex1.z._fs,outfile='{0}/Spectrogram_{1}_{2}_{3}.png'.format(title,t0,tlen,ex1.z._name),wlen=wlen,log=True,clip=clip,per_lap=0.9)        
        # Yend
        spectrogram(ey1.y.timeseries,ey1.y._fs,outfile='{0}/Spectrogram_{1}_{2}_{3}.png'.format(title,t0,tlen,ey1.y._name),wlen=wlen,log=True,clip=clip,per_lap=0.9)
        spectrogram(ey1.x.timeseries,ey1.x._fs,outfile='{0}/Spectrogram_{1}_{2}_{3}.png'.format(title,t0,tlen,ey1.x._name),wlen=wlen,log=True,clip=clip,per_lap=0.9)
        spectrogram(ey1.z.timeseries,ey1.z._fs,outfile='{0}/Spectrogram_{1}_{2}_{3}.png'.format(title,t0,tlen,ey1.z._name),wlen=wlen,log=True,clip=clip,per_lap=0.9)        
        # Cent
        spectrogram(cen.y.timeseries,cen.y._fs,outfile='{0}/Spectrogram_{1}_{2}_{3}.png'.format(title,t0,tlen,cen.y._name),wlen=wlen,log=True,clip=clip,per_lap=0.9)
        spectrogram(cen.x.timeseries,cen.x._fs,outfile='{0}/Spectrogram_{1}_{2}_{3}.png'.format(title,t0,tlen,cen.x._name),wlen=wlen,log=True,clip=clip,per_lap=0.9)
        spectrogram(cen.z.timeseries,cen.z._fs,outfile='{0}/Spectrogram_{1}_{2}_{3}.png'.format(title,t0,tlen,cen.z._name),wlen=wlen,log=True,clip=clip,per_lap=0.9)
