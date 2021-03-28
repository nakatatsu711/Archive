'''標準ライブラリ'''
import csv  # CSVファイル出力のため
import os  # ディレクトリ確認、作成
import traceback  # スタックトレースを取得


class CsvFile:
    '''
    CSVファイル書き込み
    '''

    def __init__(self, keys, logger_object):
        '''
        初期化
        '''

        try:
            # ヘッダー
            self.keys = keys
            # ロガー
            self.logger_object = logger_object
            # CSVパス
            self.csv_path = os.getcwd() + '/DOWNLOAD_ECOAUC_CSV/ecoauc_' + self.logger_object.today + '.csv'
            self.csv_path = self.csv_path.replace('/', os.sep)
        except Exception:
            raise

    def write_header(self):
        '''
        CSVファイルにヘッダーを書き込む
        '''

        try:
            with open(self.csv_path, 'w', encoding=self.logger_object.encoding, newline='') as wf:
                writer = csv.DictWriter(wf, self.keys)
                writer.writeheader()
        except Exception:
            raise

    def write_csv(self, info_list, now_url):
        '''
        CSVファイルに書き込む
        '''

        try:
            with open(self.csv_path, 'a', encoding=self.logger_object.encoding, newline='') as wf:
                writer = csv.DictWriter(wf, self.keys)
                for info in info_list:
                    writer.writerow(info)
        except Exception:
            self.logger_object.write_log('CSVファイル書き込みエラー', traceback.format_exc().strip(), now_url)
