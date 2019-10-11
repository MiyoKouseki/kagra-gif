
# Sensor Correction Trial
## Measurement Scripts
template.py : template file to measure 

## Control Status
* **Name** : 測定のID
* **Start** : 測定開始時刻
* **End** : 測定終了時刻
* **tlen** : 測定時間
* **IP2IP** : IPのLVDTをつかったFB制御
* **BF2BF** : BFのLVDTをつかったFB制御
* **TM2IM** : TM_OpLevからIMへのFB制御
* **IP_SC** : IPのSC制御
* **Diffs** : EXとIXで異なる制御

|Name| Start<br>(JST)| End<br>(JST) | tlen | IP2IP | BF2BF | TM2IM | IP_SC| Diffs |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|
|SC1_0 | Sep 06 00:30| Sep 06 01:30| 60 | L,T,Y | Y | P,Y | SEIS | **EX**:(P07,08,12,14,15) <br>**EX**:(TM2MN\_P) <br>**IX**:(P02,03,04,05,13),  | 
|SC1_1 | Sep 06 01:41| Sep 06 02:41| 60 | L,T,Y | Y | P,Y | NO | **EX**:(P07,08,12,14,15) <br>**EX**:(TM2MN\_P) <br>**IX**:(P02,03,04,05,13),  | 
|SC1_2 | Sep 06 02:52| Sep 06 03:02| 10 | L,T,Y | Y | P,Y | GIF | **EX**:(P07,08,12,14,15) <br>**EX**:(TM2MN\_P) <br>**IX**:(P02,03,04,05,13),  |
|SC1_3 | Sep 06 03:10| Sep 06 03:20| 10 | L,T,Y | Y | P,Y | GIF(-1) | **EX**:(P07,08,12,14,15) <br>**EX**:(TM2MN\_P) <br>**IX**:(P02,03,04,05,13),  |  
|SC1_4 | Sep 06 03:22| Sep 06 04:00| 38 | L,T,Y | Y | P,Y | GIF (satu) | **EX**:(P07,08,12,14,15) <br>**EX**:(TM2MN\_P) <br>**IX**:(P02,03,04,05,13),  | 
|SC1_5 | Sep 06 03:42| Sep 06 04:42| 60 | L,T,Y | Y | P,Y | GIF | **EX**:(P07,08,12,14,15) <br>**EX**:(TM2MN\_P) <br>**IX**:(P02,03,04,05,13),  |  
|---|---|---|---|---|---|---|---|---|
|SC2_0 | Sep 17 05:26| Sep 17 05:36| 10 | L(0.5),T,Y | Y | P,Y | GIF | **EX**:(P07,08,14,15) <br>**IX**:(P02,03,04,05),  | 
|SC2_1 | Sep 17 05:39| Sep 17 05:49| 10 | L(0.5),T,Y | Y | P,Y | NO | **EX**:(P07,08,14,15) <br>**IX**:(P02,03,04,05),  | 
|---|---|---|---|---|---|---|---|---|
|SC3_0 | Sep 23 20:43| Sep 23 20:53| 10 | L,T,Y | Y | P,Y(IX(10)) | GIF(1.4) | **EX**:(P07,08,12,14,15) <br>**EX**:(TM2MN\_P) <br>**IX**:(P02,03,04,05),  |
|SC3_1 | Sep 23 21:09| Sep 23 21:19| 10 | L,T,Y | Y | P,Y(IX(10)) | GIF | **EX**:(P07,08,12,14,15) <br>**EX**:(TM2MN\_P) <br>**IX**:(P02,03,04,05),  |
|SC3_2 | Sep 23 21:22| Sep 23 21:32| 10 | L,T,Y | Y | P,Y(IX(10)) | GIF(1.2) | **EX**:(P07,08,12,14,15) <br>**EX**:(TM2MN\_P) <br>**IX**:(P02,03,04,05),  | 
|SC3_3 | Sep 23 21:34| Sep 23 21:44| 10 | L,T,Y | Y | P,Y(IX(10)) | GIF(0.8) | **EX**:(P07,08,12,14,15) <br>**EX**:(TM2MN\_P) <br>**IX**:(P02,03,04,05),  | 
|SC3_4 | Sep 23 21:46| Sep 23 21:56| 10 | L,T,Y | Y | P,Y(IX(10)) | GIF(1.1) | **EX**:(P07,08,12,14,15) <br>**EX**:(TM2MN\_P) <br>**IX**:(P02,03,04,05),  | 
|SC3_5 | Sep 23 22:35| Sep 23 22:45| 10 | L(0.5),T,Y | Y | P,Y(IX(10)) | GIF | **EX**:(P07,08,12,14,15) <br>**EX**:(TM2MN\_P) <br>**IX**:(P02,03,04,05),  | 
|SC3_6 | Sep 23 22:46| Sep 23 22:56| 10 | L,T,Y | Y | P,Y(IX(10)) | GIF | **EX**:(P07,08,12,14,15) <br>**EX**:(TM2MN\_P) <br>**IX**:(P02,03,04,05),  |  
|SC3_7 | Sep 23 23:25| Sep 23 23:35| 10 | L,T,Y | Y | P,Y(IX(10)) | GIF | **EX**:(P07,08,12,14,15) <br>**EX**:(TM2MN\_P) <br>**IX**:(P02,03,04,05),  | 
|SC3_8 | Sep 23 20:57| Sep 23 21:07| 10 | L,T,Y | Y | P,Y(IX(10)) | NO | **EX**:(P07,08,12,14,15) <br>**EX**:(TM2MN\_P) <br>**IX**:(P02,03,04,05),  | 
|---|---|---|---|---|---|---|---|---|
|SC4_0 | Sep 24 21:55| Sep 24 22:05| 10 | L | Y | P,Y | GIF | **EX**:(P07,08,12,14,15) <br>**IX**:(P02,03,04,05) |  
|SC4_1 | Sep 24 23:20| Sep 25 00:10| 30 | L | Y | P,Y | GIF | **EX**:(P07,08,12,14,15) <br>**IX**:(P02,03,04,05) |
|SC4_2 | Sep 25 00:11| Sep 25 00:38| 27 | L | Y | P,Y | GIF | **EX**:(P07,08,12,14,15) <br>**EX**:(TM2MN_P) <br>**IX**:(P02,03,04,05),  |
|SC4_3 | Sep 25 00:53| Sep 25 01:03| 10 | L | Y | P,Y | GIF | **EX**:(P07,08,12,14,15) <br>**EX**:(TM2MN_P) <br>**IX**:(P02,03,04,05),  | 
|SC4_4 | Sep 25 01:15| Sep 25 01:40| 25 | L | Y | P,Y | GIF | No diff | 
|SC4_5 | Sep 24 22:08| Sep 24 22:18| 10 | L | Y | P,Y | No | **EX**:(P07,08,12,14,15) <br>**IX**:(P02,03,04,05) | 
|SC4_6 | Sep 24 22:42| Sep 24 22:52| 10 | L | Y | P,Y | No | **EX**:(P07,08,12,14,15) <br>**IX**:(P02,03,04,05) |
|---|---|---|---|---|---|---|---|---|
|SC_ |  |  | - | - | - | - | - | - |


## Comment
* **SC1**
	* SC1では、GIFの符号がアームの信号に対して合っているか確かめた
	* SC1_0,1 で地震計SCの有りなしでどう変わるか調べた。
	* SC1_2,3 でGIFの符号を調べた。SC_1_4でGIFのLimitterで信号がサチった。
* **SC2**
	* SC1ではゲインを上げすぎていたせいか150mHzでコヒーレンスを持っていなかった。なのでSC2では、ゲインを半分にしてどう変わるか調べてみた
* **SC3**
	* SCのゲインを変えてみた。
	* SC3_5 ではGIFからのGlitchが混入
* **SC4**
	* 他の自由度からのカップリングがあることがわかったので、YawとPay以外はすべて切った。
	* FBのループが無くなったので、 150 mHz のピークの問題は 200 mHz に移動。
	* SC4_1 : EX_MN_P12 に 210 mHz の Notchを入れた
	* SC4_2 : EX_BF_YAW に 210 mHz の Notchを入れた
	* SC4_3 : P12を改良


## 制御状態の調べ方
上の表を作るための手順をのべる。

制御の状態はフィルターバンクのSWSTATの値と、信号を分配するマトリックスの値で知ることができる。制御信号はこれだけではわからないが、どういうフィルターがONになっていて、どういう信号が分岐されて制御信号として使われているか知ることができる。

上の表をつくるための手順は以下のとおり。

 1. miyopy/script/filtstatus/main.py を使って、指定時刻でのEXとIXのフィルターの値を調べる。
 2. 各段の制御の状態は、**以下**のBashのコマンドをつかって情報を抜き取る。


**フィルターバンク用**
```bash
cd /Users/miyo/Dropbox/Git/miyopy/script/filtstatus/results
for j in {0..9} ; do for i in {0..9} ; do echo sc${j}_${i}; less sc${j}_${i}.txt | awk -F'[,]' '{print $1,$2,$5}'| grep -e DAMP -e SENSCORR | grep -v 0.00000e+00 | grep -v GAS |grep -v NO_| grep -v BLADE ;done > ../../../../kagra-gif/alcs/sensor_correction_trial/filtstatus/sc${j}.txt ; done
```
このコマンドは、どの段の Local FeedBack と Sensor Correction が ON になっているかどうかの情報が抜き出せれる。ちなみにこのコマンドはすべての段について DAMP と SC のみを調べているだけで、TEST や BLADE は調べていない。まあTESTとBLADEはDC位置を変えるためにつかうフィルターなので、おそらくなにもない限り一緒だとおもう。

次にマトリックスの状態について。以下のコマンドを使って調べた。

**マトリックス用**
```bash
cd /Users/miyo/Dropbox/Git/miyopy/script/filtstatus/results
for j in {0..9} ; do for i in {0..9} ; do echo sc${j}_${i}; less sc${j}_${i}_matrix.txt | grep IP_SEISALIGN ;done > ../../../../kagra-gif/alcs/sensor_correction_trial/filtstatus/sc${j}_matrix.txt ;done
```
このコマンドは、地震計かGIFか信号を選択してSC信号にするマトリックスのみを抜き出している。

最後に、2つのコマンドを使って抜き出した情報は

> /Users/miyo/Dropbox/Git/kagra-gif/alcs/sensor_correction_trial/filtstatus

にある。このファイルをみて、Measurementの表を埋めた。


MEMO

K1:GRD-LSC_LOCK_STATE_N
20 :ALS_X_LOCK
10 : IR_ARM_LOCK

