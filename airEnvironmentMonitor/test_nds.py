
import nds2
conn = nds2.connection('10.68.10.121',8088)

chnames = ['K1:PEM-IXV_GND_TR120Q_X_OUT_DQ',
           'K1:PEM-IXV_GND_TR120QTEST_X_OUT_DQ',
           'K1:PEM-IYC_WEATHER_TEMP_OUT_DQ',
           'K1:FEC-99_STATE_WORD_FE',           
               ]
buffers = conn.fetch(1227485200, 1227485203,chnames)
for data in buffers:
    print '-----'
    print data.name,data.signal_units
    print data.data
