# Noise
## データ1
### 期間

* start : Dec 6 12:00:00 JST
* tlen : 2**16 (18hours)
* fftlen : 2**9 (512seconds)

### チャンネル
1. IXV
2. IXV_TEST
3. EXV

### setup
30dbのフラットなアンプをいれた。

**ブロック図を描く**

**ノイズバジェットを描く**

* Whiteningの雑音をJGWDocから引用
* ADCの雑音を引用
 

## 結果と考察
### Amplitude Spectrum Density
* 30dbのアンプを入れたので、



<img src='./Asd.png' width=500>














### Coherence
<img src='./Coherence.png' width=500>

### Coherent Signal
<img src='./CoherentSignal.png' width=500>

### Non-coherent Signal
<img src='./NoncoherentSignal.png' width=500>

### Spectrogram
<img src='./Spectrogram_ixv_gnd_tr120q_x.png' width=500>

<img src='./Spectrogram_ixv_gnd_tr120qtest_x.png' width=500>

<img src='./Spectrogram_exv_gnd_tr120q_x.png' width=500>


### 次やること
取ってきたデータが定常じゃないので、定常な時を探してプロットする。
