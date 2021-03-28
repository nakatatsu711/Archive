'''モジュール'''
from module_ecoauc.myerror import MyError
from module_ecoauc.logger import Logger
from module_ecoauc.csvfile import CsvFile
from module_ecoauc.chromedriver import ChromeDriver
'''標準ライブラリ'''
import os  # ディレクトリ確認、作成
import traceback  # スタックトレースを取得


'''各種設定情報'''
ENCODING = 'utf-8'
'''各種URL'''
LOGIN_URL = 'https://www.ecoauc.com/client/users/sign-in'
ECOAUC_URL = 'https://www.ecoauc.com/client/favorites?limit=100&page=1'
'''各種情報'''
KEYS = [
    '商品名',
    'ランク',
    '開始価格',
    '出品順位',
    '商品写真URL'
]


def main():
    '''
    ecoaucから情報を収集して、CSVファイルに書き込む
    '''

    try:
        # カレントディレクトリ移動
        os.chdir('./ecoauc_and_mercari')
        # インスタンス化、前準備
        logger = Logger(ENCODING)
        logger.write_today()
        csvfile = CsvFile(KEYS, logger)
        csvfile.write_header()
        chromedriver = ChromeDriver(LOGIN_URL, ECOAUC_URL, logger)
        # 情報取得
        chromedriver.access()
        chromedriver.login()
        chromedriver.access()
        while True:
            # 商品情報取得
            chromedriver.get_item()
            # CSVファイル書き込み
            csvfile.write_csv(chromedriver.info_list, chromedriver.now_url)
            # 次ページ遷移
            flag = chromedriver.trans_next(flag=False)
            if flag:
                break
    except MyError as e:
        print(e)
    except Exception:
        print(traceback.format_exc().strip())
    finally:
        try:
            chromedriver.quit_driver()
        except Exception:
            pass
        input('終了（Enterキーを押してください）')


if __name__ == '__main__':
    main()
