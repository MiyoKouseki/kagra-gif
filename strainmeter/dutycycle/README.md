# Duty Cycle
## 作業場所

作業場所はここ。

```
\$(dutycycle) = kagra-gif/strainmeter/dutycycle
```

作業場所にあるファイルなどは以下の通り。

| 場所 | 説明 |
|:--|:--|
|./PXI_DATA2 | KAGRA-CMのTopディレクトリにあるPXI_DATA2をrsync | 
|./README.md | このREADME。 |
|./main.py | メインファイル |

## DutyCycleを計算する
### 方法
レーザーのロック状態とフリンジコントラストの下限を設定して判定[1]。


[1]新谷さんの2020/05/01のメールより


### 作業ログ
5Hzのデータの場所

* /PXI_DATA2/PXI1_data/5Hz/2020/05/04/00/2005040059.AD0{0,1,2,3}
* 4byte, 5Hz , 60 second のデータ。1200byte。

データのダウンロード

```
rsync -av --include="*/" --include="*.AD0*" --exclude="*" -e ssh GIF@172.16.32.201:/PXI_DATA2/PXI1_data/5Hz/2020 /Volumes/HDPF-UT/DATA/PXI_DATA2/PXI1_data/5Hz/                  
```

```
rsync -av --include="*/" --include="*.STRAIN" --exclude="*" -e ssh GIF@172.16.32.201:/data1/PHASE/50000Hz/2020 /Volumes/HDPF-UT/DATA/data1/PHASE/50000Hz/
```

```
rsync -av --include="*/" --include="*.AD02" --exclude="*" -e ssh GIF@172.16.32.201:/NAS/cRIO01_data/2020 /Volumes/HDPF-UT/DATA/NAS/cRIO01_data/
```

#### バグ
マルチプロセスにして一ヶ月程度以上のデータを選ぶと、```raise Full``` エラーが出て止まる。```~/Git/gwpy/gwpy/utils/mp.py``` の149行で起きているらしい。```nproc=1```にしてシングルプロセスにするとエラーは起きない。

#### Feature Plan

