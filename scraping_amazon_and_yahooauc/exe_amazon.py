'''モジュール'''
from module.myerror import MyError
from module.logger import Logger
from module import spreadsheet_amazon
from module import chromedriver_amazon
'''tqdm'''
from tqdm import tqdm  # 進捗
'''標準ライブラリ'''
import traceback  # スタックトレースを取得


'''各種設定情報'''
ENCODING = 'utf-8'
'''スプレッドシート情報'''
# jsonファイル名
JSON = 'JSONファイル名'
# スプレッドシートID
SPREADSHEET_ID = 'スプレッドシートキー'
'''各種URL'''
AMAZON_URL = 'https://www.amazon.co.jp/gp/css/order-history?ref_=nav_orders_first'


def main():
    '''
    Amazonから情報を収集して、スプレッドシートに書き込む
    '''

    # 情報取得処理
    try:
        logger = Logger(ENCODING)
        logger.write_today()
        spreadsheet = spreadsheet_amazon.SpreadSheet(logger, SPREADSHEET_ID, JSON)
        spreadsheet.read_sheet()
        spreadsheet.delete_sheet()
        chromedriver = chromedriver_amazon.ChromeDriver(logger, AMAZON_URL)
        pbar = tqdm(spreadsheet.account_list)
        for account in pbar:
            try:
                pbar.set_description('Amazon')
                chromedriver.access(account)
                chromedriver.login(account)
                while True:
                    # 商品情報取得
                    chromedriver.get_item()
                    # スプレッドシート書き込み
                    spreadsheet.write_sheet(chromedriver.info_list, account, chromedriver.now_url)
                    # 次ページ遷移
                    flag = chromedriver.trans_next(flag=False)
                    if flag:
                        break
                    # インターバル
                    chromedriver.interval()
            except Exception:
                pass
        chromedriver.quit_driver()
    except MyError as e:
        print('Amazonエラー')
        print(e)
    except Exception:
        print('Amazonエラー')
        print(traceback.format_exc().strip())


if __name__ == '__main__':
    main()
