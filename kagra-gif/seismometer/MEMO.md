
## チャンネル名の変遷


####　昔のチャンネル
```
'K1:PEM-\(.*\)_SEIS.*_WE_SENSINF_IN1_DQ’ 
```

##### 2018/07/05 : 3箇所に地震計。ただしIXVとEYVはホワイトニングなし。
* 07/05 00:00 UTCに最初のCDMRの計算をした。
* 08/02 00:00 IMCでもCDMRを計算した。

```
# 2018-07-29T23:59:42
$ FrChannels /data/full/12169/K-K1_C-1216944000-32.gwf | grep -e 'K1:PEM-\(.*\)_SEIS.*_WE_SENSINF_IN1_DQ'
K1:PEM-EXV_SEIS_WE_SENSINF_IN1_DQ 2048
K1:PEM-EYV_SEIS_WE_SENSINF_IN1_DQ 2048
K1:PEM-IXV_SEIS_WE_SENSINF_IN1_DQ 2048
K1:PEM-IMC_SEIS_MCE_WE_SENSINF_IN1_DQ 2048
K1:PEM-IMC_SEIS_MCI_WE_SENSINF_IN1_DQ 2048
```

##### 2018/ : Yエンドの地震計をセンターに移動。ホワイトニングなし。
* 09/06 からTESTが加わった。

```
# 2018-09-29T23:59:42
$ FrChannels /data/full/12223/K-K1_C-1222300800-32.gwf | grep -e 'K1:PEM-\(.*\)_SEIS.*_WE_SENSINF_IN1_DQ'
K1:PEM-EXV_SEIS_WE_SENSINF_IN1_DQ 2048
K1:PEM-EYV_SEIS_WE_SENSINF_IN1_DQ 2048
K1:PEM-IXV_SEIS_TEST_WE_SENSINF_IN1_DQ 2048
K1:PEM-IXV_SEIS_WE_SENSINF_IN1_DQ 2048
K1:PEM-IMC_SEIS_MCE_WE_SENSINF_IN1_DQ 2048
K1:PEM-IMC_SEIS_MCI_WE_SENSINF_IN1_DQ 2048
```


##### 2018/11/12 : ホワイトニング入れた。[klog6967]


#### 一時的なチャンネル
##### 2018/11/28 : GND_TR120Qの名前に変更。

12/05 あたりから、合計5台の地震計のチャンネルがDQされている。信号のチェックはまだ。

```
# 2018-12-05T23:59:42
$ FrChannels /data/full/12280/K-K1_C-1228089600-32.gwf | grep -e 'K1:PEM-.*_X_IN1_DQ'
K1:PEM-EXV_GND_TR120Q_X_IN1_DQ 512
K1:PEM-EYV_GND_TR120Q_X_IN1_DQ 512
K1:PEM-IXV_GND_TR120QTEST_X_IN1_DQ 512
K1:PEM-IXV_GND_TR120Q_X_IN1_DQ 512
K1:PEM-IMC_GND_TR120C_MCE_X_IN1_DQ 512
K1:PEM-IMC_GND_TR120C_MCI_X_IN1_DQ 512
```

01/24 Yエンドの地震計を戻した。

#### O3に向けたチャンネル
01/29以降

## チャンネルリスト定義
* chname0
 *	IXV,EXV,EYVに地震計がある。しかしXエンドしか30dbのアンプが入っていない。
 * 09/06 あたりでEYVの地震計をIXV_TESTにするまでの期間。
 * K1:PEM-EXV_SEIS_WE_SENSINF_IN1_DQ
 * K1:PEM-EYV_SEIS_WE_SENSINF_IN1_DQ
 * K1:PEM-IXV_SEIS_WE_SENSINF_IN1_DQ
* chname1
 * EYVを移動してIXV_TESTにした。
 * 11/28 にチャンネル名を変えるまで
 * K1:PEM-EXV_SEIS_WE_SENSINF_IN1_DQ
 * K1:PEM-EYV_SEIS_WE_SENSINF_IN1_DQ
 * K1:PEM-IXV_SEIS_WE_SENSINF_IN1_DQ
 * K1:PEM-IXV_SEIS_TEST_WE_SENSINF_IN1_DQ 
 * 
## 解析に使える安定したデータ一覧
### chname_0
* 

### chname_1
* 09/06 - 11/28

### chname_2
* 

### chname_3 (IXVに2台体制)
* [JST] 12/02 11:00 - 12/03 07:00 (20 hours) > 2^10 * 2^6 = 1mHz 64回平均のデータが取れる。
 * IXV_TESTのRMSがIXVとEXVの2倍程度のときで。（←だから何？？）
 * 