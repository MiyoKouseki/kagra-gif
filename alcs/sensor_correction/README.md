
# Sensor Correction Trial
## Measurements

|Name| Start(JST)| End(JST) | tlen(min) | IP | BF | Pay| Comment|
|---|---|---|---|---|---|---|---|
|SC1_0 | Sep 06 00:30:00 | Sep 06 01:30:00 | 60 | dcdamp(L,T,Y),SEIS_sc | - | - | - | 
|SC1_1 | Sep 06 01:40:00 | Sep 06 02:40:00 | 60 | dcdamp(L,T,Y) | - | - | - | 
|SC1_2 | Sep 06 02:52:00 | Sep 06 03:02:00 | 10 | dcdamp(L,T,Y),GIF_sc | - | - | - | 
|SC1_3 | Sep 06 03:10:00 | Sep 06 03:20:00 | 10 | dcdamp(L,T,Y),GIF_sc | - | - | - | 
|SC1_4 | Sep 06 03:22:00 | Sep 06 04:00:00 | 38 | dcdamp(L,T,Y),GIF_sc | - | - | - | 
|SC1_5 | Sep 06 03:42:00 | Sep 06 04:42:00 | 60 | dcdamp(L,T,Y),GIF_sc | - | - | - | 
|---|---|---|---|---|---|---|---|
|SC2_0 | Sep 17 05:26:00 | Sep 17 05:36:00 | 10 | dcdamp(L,T,Y),GIF_sc | - | - | - |
|SC2_1 | Sep 17 05:39:00 | Sep 17 05:49:00 | 10 | dcdamp(L,T,Y),GIF_sc | - | - | - |
|---|---|---|---|---|---|---|---|
|SC3_0 | Sep 23 20:43:00 | Sep 23 20:53:00 | 10 | dcdamp(L,T,Y),GIF_sc | - | - | - |
|SC3_1 | Sep 23 21:09:00 | Sep 23 21:19:00 | 10 | dcdamp(L,T,Y),GIF_sc | - | - | - |
|SC3_2 | Sep 23 21:22:00 | Sep 23 21:32:00 | 10 | dcdamp(L,T,Y),GIF_sc | - | - | - |
|SC3_3 | Sep 23 21:34:00 | Sep 23 21:44:00 | 10 | dcdamp(L,T,Y),GIF_sc | - | - | - |
|SC3_4 | Sep 23 21:46:00 | Sep 23 21:56:00 | 10 | dcdamp(L,T,Y),GIF_sc | - | - | - |
|SC3_5 | Sep 23 22:35:00 | Sep 23 22:45:00 | 10 | dcdamp(L,T,Y),GIF_sc | - | - | - |
|SC3_6 | Sep 23 22:46:00 | Sep 23 22:56:00 | 10 | dcdamp(L,T,Y),GIF_sc | - | - | - |
|SC3_7 | Sep 23 23:25:00 | Sep 23 23:35:00 | 10 | dcdamp(L,T,Y),GIF_sc | - | - | - |
|SC3_8 | Sep 23 20:57:00 | Sep 23 21:07:00 | 10 | dcdamp(L,T,Y),GIF_sc | - | - | - |
|---|---|---|---|---|---|---|---|
|SC4_0 | Sep 24 21:55:00 | Sep 24 22:05:00 | 10 | - | - | - | - | 
|SC4_1 | Sep 24 23:20:00 | Sep 25 00:10:00 | 30 | - | - | - | - | 
|SC4_2 | Sep 25 00:11:00 | Sep 25 00:38:00 | 26 | - | - | - | - | 
|SC4_3 | Sep 25 00:53:00 | Sep 25 01:03:00 | 10 | - | - | - | - | 
|SC4_4 | Sep 25 01:15:00 | Sep 25 01:40:00 | 25 | - | - | - | - | 
|SC4_5 | Sep 24 22:08:00 | Sep 24 22:18:00 | 10 | - | - | - | - |
|SC4_6 | Sep 24 22:42:00 | Sep 24 22:52:00 | 10 | - | - | - | - |
|---|---|---|---|---|---|---|---|
|SC_ |  |  | - | - | - | - | - | 


## Comment
* **Sensor Correction Matrix (SC Matrix)** : K1:VIS-ETMX\_IP\_SEISALIGHN
* **Sensor Correction Filter Gain (SC Gain)** : K1:VIS-ETMX\_IP\_SENSCORR_L\_GAIN


### SC1
**SC1では、GIFの符号がアームの信号に対して合っているか確かめた。**

* SC1\_0
	* a 
* SC1\_1
	* a
* SC1_2
	* SC matrix\_1\_3 = 1 
	* SC gain = -1
	* Actual SC gain was megative. It was correct sign.
* SC1_3 
	* SC matrix\_1\_3 = -1 
	* SC gain = -1
	* Actual SC gain was positive. It was not correct.
* SC1_4
	* SC matrix\_1\_3 = 1 
	* SC gain = -1
	* Correcti sign, but I founnd that control signal was saturating by limitter on SC Filter.
* SC1_5
	* SC\_gain was same as the SC1\_4, and SC1\_2.
	* Increase the limiter.

 
### SC2
**SC1ではゲインを上げすぎていたせいか150mHzでコヒーレンスを持っていなかった。なのでSC2では、ゲインを半分にしてどう変わるか調べてみた。**

* SC2_0
	* IP のDCDAMPのゲインは1のまま、SC1_2とかと同じ状態。
* SC2_1
	* IP のDCDAMPのゲインは0.5。

### SC3
SCのゲインが合っていないと考え、変えて測定してみた。

* SC3_0
	* SC Gain = 1.4
* SC3_1
	* SC Gain = 1.0
* SC3_2
	* SC Gain = 1.2
* SC3_3
 	* SC Gain = 0.8
* SC3_4
	* SC Gain = 1.1
* SC3_5
 	* SC Gain = 1.0
 	* IP Gain = 0.5
 	* Include a Glitch caused by GIF
* SC3_6
 	* Gain of SC, IP are the same as SC3\_5
* SC3_7
 	* Same as the SC2\_0
 	* SC Gain = 1.0
 	* IP Gain = 1.0
* SC3_8
 	* SC Gain = 1.0
 	* IP Gain = 0.0

### SC4
他の自由度からのカップリングがあることがわかったので、YawとPay以外はすべて切った。FBのループが無くなったので、 150 mHz のピークの問題は 200 mHz に移動。

* SC4_0
 	* 
* SC4_1
 	* ETMX_MN_P12 に 210 mHz の Notchを入れた
* SC4_2
 	* ETMX_BF_YAW に 210 mHz の Notchを入れた
* SC4_3
 	* P12を改良
* SC4_4
 	* ??
* SC4_5
 	* ??
* SC4_6
 	* ?? 

