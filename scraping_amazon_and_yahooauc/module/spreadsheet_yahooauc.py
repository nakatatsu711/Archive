'''スプレッドシート'''
import gspread  # スプレッドシート操作
from oauth2client.service_account import ServiceAccountCredentials  # 各種APIへアクセス
'''標準ライブラリ'''
import traceback  # スタックトレースを取得


class SpreadSheet:
    '''
    スプレッドシート読み書き
    '''

    def __init__(self, logger_object, spreadsheet_id, json):
        '''
        初期化
        '''

        try:
            # ロガー
            self.logger_object = logger_object
            # スプレッドシートID
            self.spreadsheet_id = spreadsheet_id
            # スプレッドシート初期設定
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']  # スコープ
            self.credentials = ServiceAccountCredentials.from_json_keyfile_name(json, scope)  # ダウンロードしたjsonファイル名をクレデンシャル変数に設定
            self.sheet_name_read = 'アカウント'
            self.sheet_name_write = 'アウトプット'
            self.row_num_before = 2
            # OAuth2の資格情報を使用してGoogleAPIにログイン（書き込み）
            gc = gspread.authorize(self.credentials)
            wb = gc.open_by_key(self.spreadsheet_id)
            self.ws = wb.worksheet(self.sheet_name_write)
            # OAuth2の資格情報を使用してGoogleAPIにログイン（読み込み）
            gc = gspread.authorize(self.credentials)
            wb = gc.open_by_key(self.spreadsheet_id)
            self.ws = wb.worksheet(self.sheet_name_read)
        except Exception:
            raise

    def read_sheet(self):
        '''
        スプレッドシート読み込み
        '''

        try:
            # 「ヤフオクID」を読み込む
            row_1s = self.ws.row_values(1)
            if not row_1s:
                raise MyError('「ヤフオクID」が読み込めませんでした')
            # 「パスワード」を読み込む
            row_2s = self.ws.row_values(2)
            if not row_2s:
                raise MyError('「パスワード」が読み込めませんでした')
            if len(row_1s) != len(row_2s):
                raise MyError('「ヤフオクID」と「パスワード」の数が異なっています')
            self.account_list = []
            for row_1, row_2 in zip(row_1s, row_2s):
                account_dict = {}
                if (row_1 == 'ヤフオクID') and (row_2 == 'パスワード'):
                    continue
                account_dict['ヤフオクID'] = row_1
                account_dict['パスワード'] = row_2
                self.account_list.append(account_dict)
            if not self.account_list:
                raise MyError('「ヤフオクID」、「パスワード」が指定されていません')
        except Exception:
            raise

    def delete_sheet(self):
        '''
        スプレッドシート内容削除
        '''

        try:
            # OAuth2の資格情報を使用してGoogleAPIにログイン（書き込み）
            gc = gspread.authorize(self.credentials)
            wb = gc.open_by_key(self.spreadsheet_id)
            self.ws = wb.worksheet(self.sheet_name_write)
            # 書き込まれている内容を削除
            col_1s = self.ws.col_values(1)
            if len(col_1s) != 1:
                row_num = len(col_1s)
                cell_list = self.ws.range('A2' + ':D' + str(row_num))
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
                wb = gc.open_by_key(self.spreadsheet_id)
                self.ws = wb.worksheet(self.sheet_name_write)
                # A列からD列まで書き込み
                cell_list = self.ws.range('A' + str(self.row_num_before) + ':D' + str(row_num_after))
                item_list = []
                for info in info_list:
                    item_list.append(info['オークションID'])
                    item_list.append(info['落札日'])
                    item_list.append(info['落札額'])
                    item_list.append(info['落札手数料'])
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
