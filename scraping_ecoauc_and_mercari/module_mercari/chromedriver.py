'''モジュール'''
from module_mercari.myerror import MyError
'''Selenium'''
from selenium import webdriver  # ブラウザを自動操作
from selenium.webdriver.chrome.options import Options  # オプションを指定
from selenium.webdriver.support.ui import WebDriverWait  # 待機用
from selenium.webdriver.support import expected_conditions as EC  # 待機条件
from selenium.webdriver.common.by import By  # 属性条件
from selenium.common.exceptions import TimeoutException  # タイムアウトエラー
'''標準ライブラリ'''
import os  # ディレクトリ確認、作成
import re  # 正規表現
import time  # 待ち時間を指定
import traceback  # スタックトレースを取得
from urllib.parse import urljoin  # 絶対URL取得


class ChromeDriver:
    '''
    ChromeDriverの操作
    '''

    def __init__(self, mercari_url, logger_object):
        '''
        初期化
        '''

        try:
            # URL
            self.absolute_url = mercari_url
            # ロガー
            self.logger_object = logger_object
            # ChromeDriverパス
            if os.name == 'nt':
                executable_path = os.getcwd() + '/chromedriver_exe/chromedriver.exe'
            elif os.name == 'posix':
                executable_path = os.getcwd() + '/chromedriver_exe/chromedriver'
            else:
                raise MyError('不明なOSです')
            executable_path = executable_path.replace('/', os.sep)
            # ユーザーエージェントパス
            ua_path = os.getcwd() + '/setting_file/user_agent.txt'
            ua_path = ua_path.replace('/', os.sep)
            # 除外ワードパス
            ng_path = os.getcwd() + '/setting_file/ng_word.txt'
            ng_path = ng_path.replace('/', os.sep)
            # ユーザーエージェント
            with open(ua_path, encoding=self.logger_object.encoding) as rf:
                ua = rf.readline().rstrip()
                headers = '--user-agent=' + ua
            # 除外ワード読み込み
            with open(ng_path, encoding=self.logger_object.encoding) as rf:
                self.ng_list = [ng.rstrip() for ng in rf.readlines() if ng.rstrip()]
            # GoogleChrome初期設定
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--window-size=1200,1291')
            options.add_argument('--log-level=3')
            options.add_argument(headers)
            self.driver = webdriver.Chrome(options=options, executable_path=executable_path)
            self.driver.set_page_load_timeout(60)
        except Exception:
            raise

    def initialize(self, row):
        '''
        初期化
        '''

        try:
            self.row_price = row
            self.row_url = {}
            self.row_price['キーワード'] = '-'
            self.row_price['リンク'] = '-'
            self.row_price['最低価格'] = '-'
            self.row_price['最高価格'] = '-'
            self.row_price['個数'] = '-'
            # URL作成
            name_tmp1 = re.sub(r'　', ' ', row['商品名'])
            name_tmp2 = re.sub(r' +', ' ', name_tmp1)
            keyword_list = name_tmp2.split(' ')
            keyword_tmp = ''
            for keyword in keyword_list:
                if keyword in self.ng_list:
                    continue
                if not keyword_tmp:
                    keyword_tmp = keyword
                else:
                    keyword_tmp += '+' + keyword
            if not keyword_tmp:
                raise MyError('「商品名」を取得できませんでした')
            self.now_url = 'https://www.mercari.com/jp/search/?sort_order=&keyword=' + keyword_tmp + '&category_root=&brand_name=&brand_id=&size_group=&price_min=&price_max=&status_trading_sold_out=1'
            self.row_price['キーワード'] = keyword_tmp.replace('+', ' ')
            self.row_price['リンク'] = self.now_url
            # リスト初期化
            self.price_list = []
            self.url_list = []
        except MyError as e:
            self.logger_object.write_log('初期化エラー', str(e), '', row['商品名'])
            raise
        except Exception:
            self.logger_object.write_log('初期化エラー', traceback.format_exc().strip(), '', row['商品名'])
            raise

    def access(self):
        '''
        各ページにアクセス
        '''

        try:
            self.driver.get(self.now_url)
        except Exception:
            self.logger_object.write_log('アクセスエラー', traceback.format_exc().strip(), self.now_url, self.row_price['商品名'])
            raise

    def check(self):
        '''
        商品があるかどうかチェック
        '''

        try:
            try:
                check = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search-result-description')))
            except TimeoutException:
                return
            raise MyError()
        except MyError:
            raise
        except Exception:
            self.logger_object.write_log('商品チェックエラー', traceback.format_exc().strip(), self.now_url, self.row_price['商品名'])
            raise

    def get_item(self):
        '''
        商品情報を取得
        '''

        try:
            items = WebDriverWait(self.driver, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'section.items-box')))
            for item in items:
                # アイテム初期化
                self.price = '-'
                self.url = '-'
                # スクロール
                self.driver.execute_script('arguments[0].scrollIntoView(true);', item)
                # 価格
                self.sub_get_item_get_price(item)
                # 商品写真URL
                self.sub_get_item_get_url(item)
                # リストに追加
                self.price_list.append(self.price)
                self.url_list.append(self.url)
                # 件数確認
                if len(self.price_list) >= self.logger_object.limit:
                    break
        except Exception:
            self.logger_object.write_log('商品情報取得エラー', traceback.format_exc().strip(), self.now_url, self.row_price['商品名'])

    def sub_get_item_get_price(self, item):
        '''
        価格を取得
        '''

        try:
            price = WebDriverWait(item, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.items-box-body > .items-box-num > .items-box-price')))
            if price.text is None:
                raise MyError('価格要素が存在しません')
            if not price.text.strip():
                raise MyError('価格要素が空です')
            self.price = price.text.strip()
        except MyError as e:
            self.logger_object.write_log('商品情報取得エラー（一部）', str(e), self.now_url, self.row_price['商品名'])
        except Exception:
            self.logger_object.write_log('商品情報取得エラー（一部）', traceback.format_exc().strip(), self.now_url, self.row_price['商品名'])

    def sub_get_item_get_url(self, item):
        '''
        商品写真URLを取得
        '''

        try:
            url = WebDriverWait(item, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'figure.items-box-photo > img')))
            if url.get_attribute('src') is None:
                raise MyError('商品写真URL要素が存在しません')
            if not url.get_attribute('src').strip():
                raise MyError('商品写真URL要素が空です')
            self.url = url.get_attribute('src').strip()
        except MyError as e:
            self.logger_object.write_log('商品情報取得エラー（一部）', str(e), self.now_url, self.row_price['商品名'])
        except Exception:
            self.logger_object.write_log('商品情報取得エラー（一部）', traceback.format_exc().strip(), self.now_url, self.row_price['商品名'])

    def trans_next(self, flag):
        '''
        次ページに遷移
        '''

        try:
            now_url = self.now_url
            # 件数確認
            if len(self.price_list) >= self.logger_object.limit:
                flag = True
                return flag
            try:
                next_urls = WebDriverWait(self.driver, 3).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'ul.pager > li.pager-next > ul > li.pager-cell > a')))
            except TimeoutException:
                flag = True
                return flag
            if len(next_urls) != 2:
                raise MyError('次ページURL要素を取得できませんでした')
            next_url = next_urls[0]
            if next_url.get_attribute('href') is None:
                raise MyError('次ページURL要素が存在しません')
            if not next_url.get_attribute('href').strip():
                raise MyError('次ページURL要素が空です')
            self.now_url = urljoin(self.absolute_url, next_url.get_attribute('href').strip())
            next_url.click()
            return flag
        except MyError as e:
            self.logger_object.write_log('次ページ遷移エラー', str(e), now_url, self.row_price['商品名'])
            flag = True
            return flag
        except Exception:
            self.logger_object.write_log('次ページ遷移エラー', traceback.format_exc().strip(), now_url, self.row_price['商品名'])
            flag = True
            return flag

    def calculate_low_and_high(self):
        '''
        「最低価格」、「最高価格」を計算
        '''

        try:
            if not self.price_list:
                raise MyError('「最低価格」、「最高価格」を計算することができません')
            # 価格を数字に変換
            item_list = []
            for item in self.price_list:
                item_tmp = item.replace('¥', '').replace(',', '')
                if not item_tmp.isdecimal():
                    continue
                item_list.append(int(item_tmp))
            # 「最低価格」
            self.row_price['最低価格'] = min(item_list)
            # 「最高価格」
            self.row_price['最高価格'] = max(item_list)
        except MyError as e:
            self.logger_object.write_log('各種計算エラー', str(e), '', self.row_price['商品名'])
        except Exception:
            self.logger_object.write_log('各種計算エラー', traceback.format_exc().strip(), '', self.row_price['商品名'])

    def calculate_num(self):
        '''
        「個数」を計算
        '''

        try:
            if (not self.price_list) or (not self.url_list):
                raise MyError('リストが存在しないので、「個数」を計算することができません')
            if len(self.price_list) != len(self.url_list):
                raise MyError('リストの数が異なっているので、「個数」を計算することができません')
            # 「個数」
            if len(self.price_list) >= self.logger_object.limit:
                self.row_price['個数'] = str(self.logger_object.limit) + '以上'
            else:
                self.row_price['個数'] = str(len(self.price_list))
            # 上段
            for i, item in enumerate(self.price_list, 1):
                self.row_price['価格、商品写真URL、商品写真' + str(i)] = item
            # 中断
            for i, item in enumerate(self.url_list, 1):
                self.row_url['価格、商品写真URL、商品写真' + str(i)] = item
        except MyError as e:
            self.logger_object.write_log('各種計算エラー', str(e), '', self.row_price['商品名'])
        except Exception:
            self.logger_object.write_log('各種計算エラー', traceback.format_exc().strip(), '', self.row_price['商品名'])

    def quit_driver(self):
        '''
        ドライバーを閉じる
        '''

        try:
            self.driver.quit()
        except Exception:
            raise
