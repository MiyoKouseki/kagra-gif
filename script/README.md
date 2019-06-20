# monitor
 
## このディレクトリについて
 * モニターするためのスクリプト等をここにまとめて、すぐに使えるようにしておく。
 * 

## Usage
### Plotting TimeSeries
```
gwpy-plot timeseries --chan K1:PEM-EXV_GND_TR120Q_X_OUT_DQ.mean,m-trend --start "Jan 14 2019 00:00:00" --duration 259200  -n k1nds0 --pad -1 --
ymin -2 --ymax 2
```
<img src='./gwpy_timeseries.png' width=600> 

### main_gif.py

### plot_trend.py
python plot_trend.py -channel K1:GIF-X_PPOL_IN1_DQ.mean,m-trend K1:GIF-X_SPOL_IN1_DQ.mean,m-trend K1:GIF-X_ZABS_IN1_DQ.mean,m-trend K1:GIF-X_STRAIN_IN1_DQ.mean,m-trend -trend=minutes -types=mean "Mar 01 2019 00:00:00 JST" "Jun 20 2019 00:00:00 JST"               