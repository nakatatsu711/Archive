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
            if os.name == 'nt':
                self.logger_path = os.getcwd() + '\\logger.txt'
            elif os.name == 'posix':
                self.logger_path = os.getcwd() + '/logger.txt'
            else:
                raise MyError('不明なOSです')
            # 取得日
            self.today = datetime.date.today().strftime('%Y/%m/%d')
            # 取得月
            self.month = datetime.date.today().strftime('%Y/%m')
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

    def write_log(self, error, text, account, url):
        '''
        ログを書き込む
        '''

        try:
            with open(self.logger_path, 'a', encoding=self.encoding, newline='') as wf:
                wf.write('＊')
                wf.write('\n')
                if account:
                    wf.write('アカウント：' + account)
                    wf.write('\n')
                if url:
                    wf.write('URL：' + url)
                    wf.write('\n')
                wf.write('エラー種別：' + error)
                wf.write('\n')
                wf.write('詳細：')
                wf.write('\n')
                wf.write(text)
                wf.write('\n')
        except Exception:
            print('警告（ログ書き込みエラー）')
