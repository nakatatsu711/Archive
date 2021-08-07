## 概要
法律事務所の情報をスクレイピングするプログラムです。

<br>

~~[法律事務所・検索＆口コミサイト](http://www.legal-findoffice.com/cat/all/tokyo/)（現在閉鎖しているようなのでクリックしないほうがいいです）から東京都にある法律事務所の情報を取得します。  
各法律事務所の詳細情報が記載されたページのURLを取得します。  
詳細情報ページに遷移し、「事務所名」、「住所」、「電話番号」、「FAX番号」、「ホームページURL」の情報を取得します。  
取得した詳細情報はテキストファイルに書き出します。



## システム環境
以下で動作確認済みです。  
OS：macOS  
Python：3系



## 実行方法
### ライブラリインストール
```
$ pip install requests
$ pip install beautifulsoup4
$ pip install lxml
```


### 実行
コマンドラインで実行します。
```
$ python scraping_law_in_tokyo.py
```
