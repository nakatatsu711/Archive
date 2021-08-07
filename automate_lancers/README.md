## 概要
ランサーズからYahoo検索用キーワードを収集し、テキストファイル`yahoo2_data.txt`に書き出します。  
`yahoo2_data.txt`からYahoo検索用キーワードを読み込み、検索結果であるURLをテキストファイル`yahoo2_result.txt`に書き出します。  
`yahoo2_result.txt`からURLを読み込み、ランサーズに書き出します。



## システム環境
以下で動作確認済みです。  
OS：macOS  
Python：3系



## 実行方法
### ライブラリインストール
```
$ pip install selenium
```


### ChromeDriverについて
ブラウザはGoogleChromeを使用します。  
ブラウザを自動操作するためにはChromeDriverが必要です。

以下から自分のGoogleChromeと同じバージョンのドライバーをダウンロードします。  
https://sites.google.com/a/chromium.org/chromedriver/downloads

ChromeDriverをダウンロードしたら解凍して、任意の場所に配置します。  
そして、`chromedriver_path`のところに自分がダウンロードした場所を指定します。  
`input_data_on_lancers.py`、`scraping_yahoo2.py`、`output_data_on_lancers.py`のそれぞれで指定してください。


### ランサーズのログイン情報を指定
`mail_address`、`password`にランサーズのログイン情報を指定します。  
`input_data_on_lancers.py`、`output_data_on_lancers.py`のそれぞれで指定してください。


### 実行
コマンドラインで実行します。  
キーワードには仕事検索キーワードを入力します。
```
$ python automate_lancers.py キーワード
```
