

# main.py

## seismodel

**スクリプト**

* **fetchnds.py** : ndsから最近の地面振動を取得するスクリプト

**Data1**　2019 Mar 19 00:00:00 JSTから3時間分の時系列から計算

* **data1_ixv\_x\_low.hdf5** : ixvのX軸を5％のパーセンタイル
* **data1_ixv\_x\_median.hdf5** : ixvのX軸を50％のパーセンタイル
* **data1_ixv\_x\_high.hdf5** : ixvのX軸を95％のパーセンタイル


## vismodel
**概要**

* このディレクトリには、IPの制御のノイズバジェットの計算に必要なデータが置いてある。
* IPの伝達関数はLuciaのフィッティングから引用している。
* IPのセンサーノイズは奥富さんのデータから引用している。

**中身**

* **SuspensionControlModel**
   * VISのサスペンション制御のためのMatlabモデル。
* **etmx** : etmxのIPのアクチュエータからLVDTへの伝達関数
	* **etmx/tfmodel.txt** : 実測データ
	* **etmx/get_TF.m** : 実測データをフィッティングするLuciaのMatlabコード
	* **etmx/get_TF.py** : Luciaのコードにある周波数、Q値をZPKへ変換するスクリプト
* **itmx** : itmxのIPのアクチュエータからLVDTへの伝達関数
	* **itmx/tfmodel.txt** : 実測データ
	* **itmx/get_TF.m** : LuciaのMatlabコード
	* **itmx/get_TF.py** : None
* **noise** : 奥富さんが測定したETMXのセンサーノイズ 
	* **noise/readme.txt** : 奥富さんのREADME
	* **noise/LVDTnoiseETMX_disp.dat** : ETMXのLVDTのノイズ。H1,H2,H3。
	* **noise/GEOnoiseproto_vel.dat** : Geophoneのノイズ。
* **lvdt.py** : ETMXのLVDTのノイズを計算する
* **geophone.py** : ETMXのGeophoneのノイズを計算する
* **filt** : Servoフィルター
* **utils** : Utils
* **ip.py** : etmx,itmxのIPの伝達関数
	* Luciaが実測したアクチュエータからLVDTへの伝達関数をフィッティングしたもの。
	* 変位からLVDTのセンサーへの伝達関数は10Hz以下は同じ形で、それ以上は付近でサチるらしい。（奥富さん談）
	* なので10Hz以下はアクチュエータからと地面からのステージへの伝達関数は同じにした。

## results
