## 概要
GoogleスプレッドシートからURLを読み込みます。  
URL先のサイトへ遷移して情報を取得し、Googleスプレッドシートへ情報を書き込みます。



## システム環境
以下で動作確認済みです。  
`OS`：macOS  
`Python`：3系



## 実行方法
### ライブラリインストール
```
$ pip install selenium
$ pip install beautifulsoup4
$ pip install lxml
$ pip install gspread
$ pip install oauth2client
```


### ChromeDriverについて
ブラウザはGoogleChromeを使用します。  
ブラウザを自動操作するためにはChromeDriverが必要です。

以下から自分のGoogleChromeと同じバージョンのドライバーをダウンロードします。  
[https://sites.google.com/a/chromium.org/chromedriver/downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads)

ChromeDriverをダウンロードしたら解凍して、任意の場所に配置します。  
そして、`chromedriver_path`のところに自分がダウンロードした場所を指定します。  


### スプレッドシートの初期設定
Pythonでスプレッドシートを操作するには初期設定が必要です。

#### プロジェクトを新規作成する
以下にアクセスして、「プロジェクトの選択」、「新しいプロジェクト」と進みます。  
[https://console.cloud.google.com](https://console.cloud.google.com)

「プロジェクト名」を入力し、「作成」をクリックします。

再度、「プロジェクトの選択」から今作成したプロジェクトを選択し、「開く」をクリックします。

#### 必要なAPIを有効にする
左上のハンバーガーメニューから、「APIとサービス」、「ライブラリ」と進みます。  
今回必要なAPIは「Google Drive API」と「Google Sheets API」の2つです。これらを有効にします。

#### 認証情報を設定する
ハンバーガーメニューから、「APIとサービス」、「認証情報」と進みます。  
「認証情報を作成」をクリックし、「サービスアカウント」を選択します。

「サービスアカウント名」を入力し、「作成」をクリックします。  
「ロールを選択」からロールを選択して、「続行」をクリックします。ロールは編集者でいいと思います。

最後に「完了」をクリックします。

今作成したサービスアカウントを選択し、上のタブから「キー」をクリックします。  
「鍵を追加」、「新しい鍵を作成」と進み、「作成」をクリックします。キーのタイプはJSONを選択してください。すると、JSONファイルがダウンロードできます。

このJSONファイルはPythonの実行ファイルと同じ場所に保存しておきます。

#### スプレッドシートの共有設定をする
新しいスプレッドシートを作成します。  
右上の「共有」をクリックし、先ほどダウンロードしたJSONファイルに`client_email`という項目があるので、このメールアドレスを編集者として追加します。

通知をする必要はないので、「通知」のチェックを外して、「共有」をクリックします。


### パラメータを指定
`credentials`にダウンロードしたJSONファイル名を指定します。

`SPREADSHEET_KEY`にはスプレッドシートキーを指定します。  
スプレッドシートキーとは、スプレッドシートのURLを指した名称で、以下の例だと「××××」の部分のことです。  
`https://docs.google.com/spreadsheets/d/××××/edit#gid=0`


### スプレッドシートにURLを指定
スクレイピングしたいページのURLをスプレッドシートに指定しておきます。  
ここでは、モノレート（現在サービスを終了したようです）の商品ページを指定しました。  
A2セルから下に記載してください。


### 実行
コマンドラインで実行します。  
```
$ python operate_googlespreadsheet.py
```
