'''モジュール'''
from module.myerror import MyError
from module.logger import Logger
from module import spreadsheet_yahooauc
from module import chromedriver_yahooauc
'''tqdm'''
from tqdm import tqdm  # 進捗
'''標準ライブラリ'''
import traceback  # スタックトレースを取得


'''各種設定情報'''
ENCODING = 'utf-8'
'''スプレッドシート情報'''
# jsonファイル名
JSON = 'JSONファイル名'
# スプレッドシートキー
SPREADSHEET_KEY = 'スプレッドシートキー'
'''各種URL'''
YAHOOAUC_URL = 'https://auctions.yahoo.co.jp/closeduser/jp/show/mystatus?select=closed&hasWinner=1'


def main():
    '''
    ヤフオクから情報を収集して、スプレッドシートに書き込む
    '''

    try:
        # 情報取得処理
        logger = Logger(ENCODING)
        logger.write_today()
        spreadsheet = spreadsheet_yahooauc.SpreadSheet(logger, SPREADSHEET_KEY, JSON)
        spreadsheet.read_sheet()
        spreadsheet.delete_sheet()
        chromedriver = chromedriver_yahooauc.ChromeDriver(logger, YAHOOAUC_URL)
        pbar = tqdm(spreadsheet.account_list)
        for account in pbar:
            try:
                pbar.set_description('Yahooauc')
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
        print('ヤフオクエラー')
        print(e)
    except Exception:
        print('ヤフオクエラー')
        print(traceback.format_exc().strip())


if __name__ == '__main__':
    main()
