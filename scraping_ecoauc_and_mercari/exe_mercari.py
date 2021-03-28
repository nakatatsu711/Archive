'''モジュール'''
from module_mercari.myerror import MyError
from module_mercari.logger import Logger
from module_mercari.csvfile import CsvFile
from module_mercari.chromedriver import ChromeDriver
'''tqdm'''
from tqdm import tqdm  # 進捗
'''標準ライブラリ'''
import os  # ディレクトリ確認、作成
import traceback  # スタックトレースを取得


'''各種設定情報'''
ENCODING = 'utf-8'
'''各種URL'''
MERCARI_URL = 'https://www.mercari.com/jp/search/'


def main():
    '''
    メルカリから情報を収集して、CSVファイルに書き込む
    '''

    try:
        # カレントディレクトリ移動
        os.chdir('./ecoauc_and_mercari')
        # インスタンス化、前準備
        logger = Logger(ENCODING)
        logger.write_today()
        csvfile = CsvFile(logger)
        csvfile.read_csv()
        csvfile.write_header()
        logger.write_csv_info(csvfile.read_path_logger)
        chromedriver = ChromeDriver(MERCARI_URL, logger)
        # 情報取得
        for row in tqdm(csvfile.info_list):
            try:
                # 初期化
                chromedriver.initialize(row)
                # アクセス
                chromedriver.access()
                # チェック
                chromedriver.check()
                while True:
                    # 商品情報取得
                    chromedriver.get_item()
                    # 次ページ遷移
                    flag = chromedriver.trans_next(flag=False)
                    if flag:
                        break
                # 各種計算
                chromedriver.calculate_low_and_high()
                chromedriver.calculate_num()
            except Exception:
                pass
            finally:
                # CSVファイル書き込み
                csvfile.write_csv(chromedriver.row_price, chromedriver.row_url)
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
