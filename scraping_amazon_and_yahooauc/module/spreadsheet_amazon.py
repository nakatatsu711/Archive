'''スプレッドシート'''
import gspread  # スプレッドシート操作
from oauth2client.service_account import ServiceAccountCredentials  # 各種APIへアクセス
'''標準ライブラリ'''
import traceback  # スタックトレースを取得


class SpreadSheet:
    '''
    スプレッドシート読み書き
    '''

    def __init__(self, logger_object, spreadsheet_key, json):
        '''
        初期化
        '''

        try:
            # ロガー
            self.logger_object = logger_object
            # スプレッドシートキー
            self.spreadsheet_key = spreadsheet_key
            # スプレッドシート初期設定
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']  # スコープ
            self.credentials = ServiceAccountCredentials.from_json_keyfile_name(json, scope)  # ダウンロードしたjsonファイル名をクレデンシャル変数に設定
            self.sheet_name_read = 'アカウント'
            self.sheet_name_write = 'アウトプット'
            self.row_num_before = 2
            # OAuth2の資格情報を使用してGoogleAPIにログイン（読み込み）
            gc = gspread.authorize(self.credentials)
            wb = gc.open_by_key(self.spreadsheet_key)
            self.ws = wb.worksheet(self.sheet_name_read)
            # OAuth2の資格情報を使用してGoogleAPIにログイン（書き込み）
            gc = gspread.authorize(self.credentials)
            wb = gc.open_by_key(self.spreadsheet_key)
            self.ws = wb.worksheet(self.sheet_name_write)
        except Exception:
            raise

    def read_sheet(self):
        '''
        スプレッドシート読み込み
        '''

        try:
            # OAuth2の資格情報を使用してGoogleAPIにログイン（読み込み）
            gc = gspread.authorize(self.credentials)
            wb = gc.open_by_key(self.spreadsheet_key)
            self.ws = wb.worksheet(self.sheet_name_read)
            # 「Eメール」を読み込む
            row_3s = self.ws.row_values(3)
            if not row_3s:
                raise MyError('「Amazonメール」が読み込めませんでした')
            # 「パスワード」を読み込む
            row_4s = self.ws.row_values(4)
            if not row_4s:
                raise MyError('「パスワード」が読み込めませんでした')
            if len(row_3s) != len(row_4s):
                raise MyError('「Amazonメール」と「パスワード」の数が異なっています')
            self.account_list = []
            for row_3, row_4 in zip(row_3s, row_4s):
                account_dict = {}
                if (row_3 == 'Amazonメール') and (row_4 == 'パスワード'):
                    continue
                account_dict['Eメール'] = row_3
                account_dict['パスワード'] = row_4
                self.account_list.append(account_dict)
            if not self.account_list:
                raise MyError('「Amazonメール」、「パスワード」が指定されていません')
        except Exception:
            raise

    def delete_sheet(self):
        '''
        スプレッドシート内容削除
        '''

        try:
            # OAuth2の資格情報を使用してGoogleAPIにログイン（書き込み）
            gc = gspread.authorize(self.credentials)
            wb = gc.open_by_key(self.spreadsheet_key)
            self.ws = wb.worksheet(self.sheet_name_write)
            # 書き込まれている内容を削除
            col_6s = self.ws.col_values(6)
            if len(col_6s) != 1:
                row_num = len(col_6s)
                cell_list = self.ws.range('F2' + ':K' + str(row_num))
                for cell in cell_list:
                    cell.value = ''
                self.ws.update_cells(cell_list)
        except Exception:
            raise

    def write_sheet(self, info_list, account, now_url):
        '''
        スプレッドシート書き込み
        '''

        try:
            if info_list:
                # 行番号（後）を計算
                row_num_after = self.row_num_before + len(info_list) - 1
                # OAuth2の資格情報を使用してGoogleAPIにログイン（書き込み）
                gc = gspread.authorize(self.credentials)
                wb = gc.open_by_key(self.spreadsheet_key)
                self.ws = wb.worksheet(self.sheet_name_write)
                # F列からK列まで書き込み
                cell_list = self.ws.range('F' + str(self.row_num_before) + ':K' + str(row_num_after))
                item_list = []
                for info in info_list:
                    item_list.append(info['商品名'])
                    item_list.append(info['商品URL'])
                    item_list.append(info['ASIN'])
                    item_list.append(info['購入価格'])
                    item_list.append(info['注文番号'])
                    item_list.append(info['仕入れ'])
                for cell, item in zip(cell_list, item_list):
                    cell.value = item
                self.ws.update_cells(cell_list)
                # 行番号（前）を計算
                self.row_num_before = self.row_num_before + len(info_list)
        except gspread.exceptions.APIError as e:
            if '"code": 429' in str(e):
                time.sleep(100)
            error = 'スプレッドシート書き込みエラー'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, account, now_url)
        except Exception:
            error = 'スプレッドシート書き込みエラー'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, account, now_url)
