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
            self.logger_path = os.getcwd() + '/logger_ecoauc.txt'
            self.logger_path = self.logger_path.replace('/', os.sep)
            # 取得日
            self.today = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')
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

    def write_log(self, error, text, info):
        '''
        ログを書き込む
        '''

        try:
            with open(self.logger_path, 'a', encoding=self.encoding, newline='') as wf:
                wf.write('＊')
                wf.write('\n')
                if info:
                    wf.write('URL：' + info)
                    wf.write('\n')
                wf.write('エラー種別：' + error)
                wf.write('\n')
                wf.write('詳細：')
                wf.write('\n')
                wf.write(text)
                wf.write('\n')
        except Exception:
            print('警告（ログ書き込みエラー）')
