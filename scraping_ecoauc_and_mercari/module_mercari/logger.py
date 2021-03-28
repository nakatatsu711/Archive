'''モジュール'''
from module_mercari.myerror import MyError
'''標準ライブラリ'''
import datetime  # 日付
import os  # ディレクトリ確認、作成


class Logger:
    '''
    ロガー
    '''

    def __init__(self, encoding):
        '''
        初期化
        '''

        try:
            # エンコーディング
            self.encoding = encoding
            # ロガーパス
            self.logger_path = os.getcwd() + '/logger_mercari.txt'
            self.logger_path = self.logger_path.replace('/', os.sep)
            # 取得日
            self.today = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
            # リミットパス
            limit_path = os.getcwd() + '/setting_file/item_limit.txt'
            limit_path = limit_path.replace('/', os.sep)
            # 件数の上限を読み込む
            with open(limit_path, encoding=self.encoding) as rf:
                self.limit = rf.readline().rstrip()
            if not self.limit.isdecimal():
                raise MyError('item_limit.txtの値が無効です')
            self.limit = int(self.limit)
        except Exception:
            raise

    def write_today(self):
        '''
        ログに取得日を書き込む
        '''

        try:
            with open(self.logger_path, 'w', encoding=self.encoding, newline='') as wf:
                wf.write('取得日：' + self.today)
                wf.write('\n')
        except Exception:
            raise

    def write_csv_info(self, read_path):
        '''
        セットするCSVファイルを書き込む
        '''

        try:
            with open(self.logger_path, 'a', encoding=self.encoding, newline='') as wf:
                wf.write('＊')
                wf.write('\n')
                wf.write('セットCSV：')
                wf.write('\n')
                wf.write(read_path)
                wf.write('\n')
        except Exception:
            raise

    def write_log(self, error, text, url, keyword):
        '''
        ログを書き込む
        '''

        try:
            with open(self.logger_path, 'a', encoding=self.encoding, newline='') as wf:
                wf.write('＊')
                wf.write('\n')
                if url:
                    wf.write('URL：' + url)
                    wf.write('\n')
                if keyword:
                    wf.write('キーワード：' + keyword)
                    wf.write('\n')
                wf.write('エラー種別：' + error)
                wf.write('\n')
                wf.write('詳細：')
                wf.write('\n')
                wf.write(text)
                wf.write('\n')
        except Exception:
            print('警告（ログ書き込みエラー）')
