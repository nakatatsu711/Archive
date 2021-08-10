## 概要
このツールは、CSVファイルから情報を読み込み自動でヤフオクに出品するプログラムです。



## システム環境
以下で動作確認済みです。  
`OS`：macOS  
`Python`：3系



## 実行方法
### ライブラリインストール
```
$ pip install selenium
$ pip install requests
```


### ChromeDriverについて
ブラウザはGoogleChromeを使用します。  
ブラウザを自動操作するためにはChromeDriverが必要です。

以下から自分のGoogleChromeと同じバージョンのドライバーをダウンロードします。  
[https://sites.google.com/a/chromium.org/chromedriver/downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads)

ChromeDriverをダウンロードしたら解凍して、任意の場所に配置します。  
そして、`manage_yahooauc.py`の`EXECUTABLE_PATH`のところに自分がダウンロードした場所を指定します。


### ユーザーエージェントを指定
`manage_yahooauc.py`の`HEADERS`にユーザーエージェントを指定します。


### 出品ファイルを準備する
出品ファイルを準備します。  
GitHubには事前にサンプルをアップロードしてあります。

サンプルのファイル名は`sample.csv`ですが、自由に変更してもらって構いません。  
ファイル名を変更したら、`manage_yahooauc.py`の`CSV_NAME`も変更してください。


### 設定ファイルを変更する
`setting.txt`で変更します。

`INTERVAL`で出品間隔の時間を調整できます。  
`ID`、`PASSWORD`は、Yahoo!JAPANのID、パスワードを指定してください。ログインに使います。


### 実行
コマンドラインで実行します。  
```
$ python manage_yahooauc.py
```
