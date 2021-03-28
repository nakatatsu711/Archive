'''モジュール'''
from module_mercari.myerror import MyError
'''標準ライブラリ'''
import csv  # CSVファイル出力のため
import glob  # CSVファイル検索
import os  # ディレクトリ確認、作成
import traceback  # スタックトレースを取得


class CsvFile:
    '''
    CSVファイル書き込み
    '''

    def __init__(self, logger_object):
        '''
        初期化
        '''

        try:
            # ロガー
            self.logger_object = logger_object
            # CSVパス
            read_csvs = glob.glob(os.getcwd() + '/SET_ECOAUC_CSV/*.csv')
            if len(read_csvs) != 1:
                raise MyError('SET_ECOAUC_CSVフォルダにCSVファイルをセットしてください')
            self.read_path = read_csvs[0]
            self.read_path = self.read_path.replace('/', os.sep)
            self.read_path_logger = self.read_path.replace(os.getcwd(), '').replace('SET_ECOAUC_CSV', '').replace('/', '').replace('\\', '')
            self.write_path = os.getcwd() + '/DOWNLOAD_MERCARI_CSV/mercari_' + self.logger_object.today + '.csv'
            self.write_path = self.write_path.replace('/', os.sep)
            # ヘッダー
            self.keys = [
                '商品名',
                'ランク',
                '開始価格',
                '出品順位',
                '商品写真URL',
                'キーワード',
                'リンク',
                '最低価格',
                '最高価格',
                '個数'
            ]
            # ヘッダーに追加
            for i in range(1, self.logger_object.limit + 1):
                self.keys.append('価格、商品写真URL、商品写真' + str(i))
        except Exception:
            raise

    def read_csv(self):
        '''
        ecoaucファイルを読み込む
        '''

        try:
            self.info_list = []
            with open(self.read_path, encoding=self.logger_object.encoding, newline='') as rf:
                reader = csv.DictReader(rf)
                for row in reader:
                    self.info_list.append(row)
        except Exception:
            raise

    def write_header(self):
        '''
        CSVファイルにヘッダーを書き込む
        '''

        try:
            with open(self.write_path, 'w', encoding=self.logger_object.encoding, newline='') as wf:
                writer = csv.DictWriter(wf, self.keys)
                writer.writeheader()
        except Exception:
            raise

    def write_csv(self, row_price, row_url):
        '''
        CSVファイルに書き込む
        '''

        try:
            # 上段
            with open(self.write_path, 'a', encoding=self.logger_object.encoding, newline='') as wf:
                writer = csv.DictWriter(wf, self.keys)
                writer.writerow(row_price)
            # 中断
            with open(self.write_path, 'a', encoding=self.logger_object.encoding, newline='') as wf:
                writer = csv.DictWriter(wf, self.keys)
                writer.writerow(row_url)
            # 下段
            with open(self.write_path, 'a', encoding=self.logger_object.encoding, newline='') as wf:
                writer = csv.DictWriter(wf, self.keys)
                writer.writerow({})
        except Exception:
            self.logger_object.write_log('CSVファイル書き込みエラー', traceback.format_exc().strip(), '', row_price['商品名'])
