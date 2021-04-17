'''yahooaucモジュール'''
import yahooauc  # 各クラスをインポート
'''標準ライブラリ'''
import sys  # プログラム終了


'''各種設定情報'''
HEADERS = '--user-agent=ユーザーエージェント'  # http://www.ugtop.com/spill.shtmlで調べる
ENCODING = 'utf-8'
EXECUTABLE_PATH = 'ChromeDriverのパス'
'''各種URL'''
YAHOOAUC_URL = 'https://auctions.yahoo.co.jp/'
YAHOOAUC_SELL_URL = 'https://auctions.yahoo.co.jp/sell/jp/show/submit?category=0'
'''CSVファイル名'''
CSV_NAME = 'sample.csv'
CATEGORY_CSV_NAME = 'category.csv'
'''テキストファイル名'''
TXT_NAME = 'setting.txt'
'''ダウンロードディレクトリ名'''
DOWNLOAD_DIR = './yahooauc_images/'


def main():
    '''
    ヤフオクに出品
    '''

    try:
        print('開始')
        # 前処理
        csvfile = yahooauc.ReadCSV(CSV_NAME, ENCODING)
        chromedriver = yahooauc.ChromeDriver(HEADERS, EXECUTABLE_PATH, TXT_NAME, ENCODING)
        csvfile.make_dir()
        chromedriver.access_top(YAHOOAUC_URL)
        chromedriver.close_modal()
        chromedriver.login()
        chromedriver.close_modal()
        # 出品処理
        for row_num, row in enumerate(csvfile.reader, 2):
            try:
                # 出品ページにアクセス
                chromedriver.access_sell(YAHOOAUC_SELL_URL)
                chromedriver.close_modal2()
                # 画像保存処理
                csvfile.save_image(row, row_num)
                # 「画像」出品処理
                chromedriver.sell_image(DOWNLOAD_DIR, row_num)
                # 「商品名」出品処理
                chromedriver.sell_name(row)
                # カテゴリ情報取得処理
                categorycsvfile = yahooauc.ReadCategoryCSV(CATEGORY_CSV_NAME, ENCODING)
                category_list = categorycsvfile.get_category(row)
                categorycsvfile.close_csv()
                chromedriver.sell_category(category_list)
                # 「商品の状態」出品処理
                chromedriver.sell_status(row)
                # 「説明」出品処理
                chromedriver.sell_description(row)
                # 「個数」出品処理
                chromedriver.sell_quantity(row)
                # 「発送元の地域」出品処理
                chromedriver.sell_location(row)
                # 「送料負担」出品処理
                chromedriver.sell_shippingwho(row)
                # 「配送方法」出品処理
                chromedriver.sell_deliverymethod(row)
                # 「支払いから発送までの日数」出品処理
                chromedriver.sell_shipschedule(row)
                # 「開始価格」出品処理
                chromedriver.sell_startprice(row)
                # 「終了する日時」出品処理
                chromedriver.sell_closingymdtime(row)
                # 「オプション」出品処理
                chromedriver.sell_option()
                # "確認する"をクリック
                chromedriver.confirm()
                # 出品エラー確認
                chromedriver.confirm_error()
                # "ガイドラインと上記規約に同意して出品する"をクリック
                chromedriver.submit()
                print('行番号' + str(row_num) + '：成功')
                # インターバル管理
                chromedriver.take_interval()
            except Exception:
                print('行番号' + str(row_num) + '：失敗')
                continue
        # 終了処理
        csvfile.close_csv()
        csvfile.del_dir()
        chromedriver.quit_driver()
        print('終了')
    except Exception:
        try:
            print('終了します')
            csvfile.close_csv()
            csvfile.del_dir()
            chromedriver.quit_driver()
            sys.exit()
        except Exception:
            sys.exit()


if __name__ == '__main__':
    main()
