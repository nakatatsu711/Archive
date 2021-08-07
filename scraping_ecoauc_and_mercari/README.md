## 概要
EcoRing the Auctionから取得した商品名をメルカリで検索し、さらにメルカリからも情報を取得します。  
取得した情報はCSVファイルに書き込みます。



## システム環境
以下で動作確認済みです。  
OS：macOS、Windows  
Python：3系



## 実行方法
### ライブラリインストール
```
$ pip install selenium
$ pip install tqdm
```


### ChromeDriverについて
ブラウザはGoogleChromeを使用します。  
ブラウザを自動操作するためにはChromeDriverが必要です。

以下から自分のGoogleChromeと同じバージョンのドライバーをダウンロードします。  
https://sites.google.com/a/chromium.org/chromedriver/downloads

ChromeDriverをダウンロードしたら解凍して、`chromedriver_exe`フォルダに配置します。


### 設定を行う
`ecoauc_account.txt`にEメール、パスワードを指定します。

`item_limit.txt`にメルカリの検索上限数を指定します。

`ng_word.txt`に除外ワードを指定します。  
このファイルで指定したワードは、メルカリで検索されません。

`user_agent.txt`にユーザーエージェントを指定します。


### 実行
まず、EcoRing the Auctionから情報を取得します。
```
$ python exe_ecoauc.py
```

`DOWNLOAD_ECOAUC_CSV`にCSVファイルがダウンロードされますので、そのCSVファイルを`SET_ECOAUC_CSV`に移動します。

次に、メルカリから情報を取得します。
```
$ python exe_mercari.py
```

`DOWNLOAD_MERCARI_CSV`にCSVファイルがダウンロードされます。
このCSVファイルが最終的に欲しい情報をまとめたものです。
