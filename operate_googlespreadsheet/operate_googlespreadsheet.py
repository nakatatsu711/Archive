import time

from bs4 import BeautifulSoup
import gspread
from selenium import webdriver
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']  # 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
# 設定値
credentials = ServiceAccountCredentials.from_json_keyfile_name('JSONファイル名', scope)  # ダウンロードしたJSONファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
SPREADSHEET_KEY = 'スプレッドシートキー'  # 共有設定したスプレッドシートキーを格納
chromedriver_path = 'ChromeDriverのパス'


def info_get():
    '''
    Googleスプレッドシート読み書き
    モノレートサイトから「商品名」、「ASIN」、「商品型番」を取得
    '''

    # OAuth2の資格情報を使用してGoogleAPIにログイン
    gc = gspread.authorize(credentials)

    # 共有設定したスプレッドシートのシート1を開く
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

    # 制限
    # ①ユーザーごとに100秒あたり100件のリクエスト
    # ②1回のプログラムで設定できる最大値は1,000件まで
    # ③1秒あたり10件まで

    # スプレッドシートからURLを読み出す
    row = 2
    column = 1
    monorate_urls = []
    while True:
        url = worksheet.cell(row, column).value
        if not url:  # 最後の行までURLを取得したらWhile文をbreak
            break
        monorate_urls.append(url)
        row += 1
        time.sleep(2)  # 2秒待つ

    # ChromeのWebDriverオブジェクトを作成
    driver = webdriver.Chrome(chromedriver_path)

    # 「商品名」、「ASIN」、「商品型番」のdictをリストに追加
    items = []
    for url in monorate_urls:
        time.sleep(1)
        driver.get(url)
        driver.execute_script('window.scrollTo(0, 0);')  # ページ上部へ移動
        soup = BeautifulSoup(driver.page_source, 'lxml')
        dict = {}
        dict['name'] = soup.select('.item_detail > div > h3 > a')[0].text  # 「商品名」を追加
        dict['asin'] = soup.find(id='_asin').text  # 「ASIN」を追加
        clips = soup.select('.item_detail > div > span > .clip_bd')
        if len(clips) == 2:
            dict['model'] = '不明'  # 規格番号が記載されていない場合、'不明'と入力
        else:
            dict['model'] = clips[2].text  # 「商品型番」を追加

        items.append(dict)

    # 「商品名」をスプレッドシートに書き出す
    row = 2
    column = 2
    for item in items:
        worksheet.update_cell(row, column, item['name'])
        row += 1
        time.sleep(2)  # 2秒待つ

    # 「ASIN」をスプレッドシートに書き出す
    row = 2
    column = 3
    for item in items:
        worksheet.update_cell(row, column, item['asin'])
        row += 1
        time.sleep(2)  # 2秒待つ

    # 「商品型番」をスプレッドシートに書き出す
    row = 2
    column = 4
    for item in items:
        worksheet.update_cell(row, column, item['model'])
        row += 1
        time.sleep(2)  # 2秒待つ

    # ブラウザを閉じる
    driver.quit()


if __name__ == '__main__':
    info_get()
