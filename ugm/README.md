# Under Ground Motion

* seismicnoise
	* 長期間の地面振動データから使えるデータを調べるためのディレクトリ。
	* 使えるデータはdqflag.dbにある。
	* klog: [9386](http://klog.icrr.u-tokyo.ac.jp/osl/?r=9386)
* seismicarlert 
	* コントロールルームで表示しているSeismicAlertをつくるための場所
	* このSeismicAlertは、SeismicNoise ディレクトリで計算したパーセンタイルをもとに、今の地面振動がどれぐらいうるさいのか、黄色（50-90）赤（90以上）緑（50以下）で知らせてくれる。
	* klog: [9700](http://klog.icrr.u-tokyo.ac.jp/osl/?r=9700)
* dam
	* 新猪谷ダムの放水が、2Hz付近で地面を揺らすことを調べた場所。
	* klog: [9586](http://klog.icrr.u-tokyo.ac.jp/osl/?r=9586), [9667](http://klog.icrr.u-tokyo.ac.jp/osl/?r=9667)
	* 
* cdmr
	* CDMRの計算に使ったディレクトリ。まだdqflag.dbが無い頃に使っていたので、かなり煩雑。
	* ここは早く整理して書き直す必要がある。
* phase_velocity
	* なにをやっていたか忘れた。位相速度の計算が、いろんな時期で同じ値になるか確かめようとしたんだと思う。消すにはもったいないので、残しておく。でもそのうちきれいにまとめ直さないと。。
	