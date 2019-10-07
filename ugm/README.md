# Under Ground Motion

* **seismicnoise**
	* 使える地震計データを調べるためのディレクトリ。
	* 使えるデータはdqflag.dbにある。
	* klog: [9386](http://klog.icrr.u-tokyo.ac.jp/osl/?r=9386)
* **seismicarlert** 
	* コントロールルームで表示しているSeismicAlertをつくるためのディレクトリ。
	* このSeismicAlertは、SeismicNoise ディレクトリで計算したパーセンタイルをもとに、今の地面振動がどれぐらいうるさいのか、黄色（50-90）赤（90以上）緑（50以下）で知らせてくれる。
	* klog: [9700](http://klog.icrr.u-tokyo.ac.jp/osl/?r=9700)
* **dam**
	* 新猪谷ダムの放水が、2Hz付近で地面を揺らすことを調べるためのディレクトリ。
	* klog: [9586](http://klog.icrr.u-tokyo.ac.jp/osl/?r=9586), [9667](http://klog.icrr.u-tokyo.ac.jp/osl/?r=9667)
* **cdmr**
	* CDMRの計算に使ったディレクトリ。まだdqflag.dbが無い頃に使っていたので、かなり煩雑。
	* ここは早く整理して書き直す必要がある。
* **seismometer_noise**
	* 地震計のノイズを解析するためのディレクトリ。
* **seismic_response** 
	* 離れた2点の地面応答
	* klog: 
	* Issue: [#129](https://github.com/MiyoKouseki/kagra-gif/issues/129)
* phase_velocity
	* なにをやっていたか忘れた。位相速度の計算が、いろんな時期で同じ値になるか確かめようとしたんだと思う。消すにはもったいないので、残しておく。でもそのうちきれいにまとめ直さないと。。