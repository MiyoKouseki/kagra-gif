from gwpy.timeseries import TimeSeries

import wave

fname = './shininotani_dam.wav'
wfile = wave.open(fname, 'r')
numch = wfile.getnchannels()
samplewidth = wfile.getsampwidth()
samplerate = wfile.getframerate()
numsamples = wfile.getnframes()
print samplewidth
print samplerate
print numsamples
buf = wfile.readframes(numsamples)
wfile.close()
#data = TimeSeries.read('./shininotani_dam.wav')
#print data


#from pydub import AudioSegment
#data = AudioSegment.from_m4a("shininotani_dam.m4a")
