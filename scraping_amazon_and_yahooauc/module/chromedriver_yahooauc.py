'''MyErrorクラス'''
from module.myerror import MyError
'''Selenium'''
from selenium import webdriver  # ブラウザを自動操作
from selenium.webdriver.common.keys import Keys  # キーを送信
from selenium.webdriver.chrome.options import Options  # オプションを指定
from selenium.webdriver.support.ui import WebDriverWait  # 待機用
from selenium.webdriver.support import expected_conditions as EC  # 待機条件
from selenium.webdriver.common.by import By  # 属性条件
from selenium.common.exceptions import NoSuchElementException  # エラー
'''標準ライブラリ'''
from decimal import Decimal  # 値を丸める
from decimal import ROUND_HALF_UP  # 四捨五入
import os  # ディレクトリ確認、作成
import re  # 正規表現
import time  # 待ち時間を指定
import traceback  # スタックトレースを取得
from urllib.parse import urljoin  # 絶対URL取得


class ChromeDriver:
    '''
    ChromeDriverの操作
    '''

    def __init__(self, logger_object, yahooauc_url):
        '''
        初期化
        '''

        try:
            # ロガー
            self.logger_object = logger_object
            # URL
            self.absolute_url = yahooauc_url
            self.now_url = yahooauc_url
            # ChromeDriverパス、ユーザーエージェントパス
            if os.name == 'nt':
                executable_path = os.getcwd() + '\\chromedriver.exe'
                ua_path = os.getcwd() + '\\user_agent.txt'
            elif os.name == 'posix':
                executable_path = os.getcwd() + '/chromedriver'
                ua_path = os.getcwd() + '/user_agent.txt'
            else:
                raise MyError('不明なOSです')
            # ユーザーエージェント
            with open(ua_path, encoding=self.logger_object.encoding) as rf:
                ua = rf.readline().rstrip()
                self.headers = '--user-agent=' + ua
            # GoogleChrome初期設定
            options = Options()
            options.add_argument('--headless')  # ヘッドレスモード
            options.add_argument('--incognito')  # シークレットモード
            options.add_argument('--window-size=1200,1291')
            options.add_argument('--log-level=3')
            options.add_argument(self.headers)
            self.driver = webdriver.Chrome(options=options, executable_path=executable_path)
            self.driver.set_page_load_timeout(60)
        except Exception:
            raise

    def access(self, account):
        '''
        各ページにアクセス
        '''

        try:
            self.driver.get(self.now_url)
        except Exception:
            error = 'アクセスエラー'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, account['ヤフオクID'], '')
            raise

    def login(self, account):
        '''
        ログイン
        '''

        try:
            # アカウント
            self.id = account['ヤフオクID']
            self.password = account['パスワード']
            # ヤフオクID
            id = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.ID, 'username')))
            id.send_keys(self.id)
            time.sleep(1)
            id.send_keys(Keys.RETURN)
            # パスワード
            password = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.ID, 'passwd')))
            password.send_keys(self.password)
            time.sleep(1)
            password.send_keys(Keys.RETURN)
        except Exception:
            error = 'ログインエラー'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, account['ヤフオクID'], '')
            raise

    def get_item(self):
        '''
        商品情報を取得
        '''

        try:
            # リスト初期化
            self.info_list = []
            items = WebDriverWait(self.driver, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '#acWrContents > div > table > tbody > tr > td > table > tbody > tr:nth-child(3) > td > table:nth-child(6) > tbody > tr')))
            for count, item in enumerate(items):
                if count == 0:
                    continue
                # 辞書初期化
                self.info_dict = {}
                self.info_dict['落札日'] = '-'
                self.info_dict['オークションID'] = '-'
                self.info_dict['落札額'] = '-'
                self.info_dict['落札手数料'] = '-'
                # 「落札日」
                self.sub_get_item_get_day(item)
                # 「オークションID」
                self.sub_get_item_get_id(item)
                # 「落札額」
                self.sub_get_item_get_price(item)
                # 「落札手数料」
                self.sub_get_item_get_charge(item)
                # リストに追加
                self.info_list.append(self.info_dict)
        except Exception:
            error = '商品情報取得エラー'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, self.id, self.now_url)

    def sub_get_item_get_day(self, item):
        '''
        「落札日」を取得
        '''

        try:
            days = WebDriverWait(item, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'td')))
            if len(days) != 11:
                raise MyError('「落札日」要素を取得できませんでした')
            day = days[4]
            if day.text is None:
                raise MyError('「落札日」要素が存在しません')
            if not day.text.strip():
                raise MyError('「落札日」要素が空です')
            self.info_dict['落札日'] = day.text.strip()
        except MyError as e:
            error = '商品情報取得エラー（一部）'
            text = str(e)
            self.logger_object.write_log(error, text, self.id, self.now_url)
        except Exception:
            error = '商品情報取得エラー（一部）'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, self.id, self.now_url)

    def sub_get_item_get_id(self, item):
        '''
        「オークションID」を取得
        '''

        try:
            ids = WebDriverWait(item, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'td')))
            if len(ids) != 11:
                raise MyError('「オークションID」要素を取得できませんでした')
            id = ids[1]
            if id.text is None:
                raise MyError('「オークションID」要素が存在しません')
            if not id.text.strip():
                raise MyError('「オークションID」要素が空です')
            self.info_dict['オークションID'] = id.text.strip()
            id = ids[2]
        except MyError as e:
            error = '商品情報取得エラー（一部）'
            text = str(e)
            self.logger_object.write_log(error, text, self.id, self.now_url)
        except Exception:
            error = '商品情報取得エラー（一部）'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, self.id, self.now_url)

    def sub_get_item_get_price(self, item):
        '''
        「落札額」を取得
        '''

        try:
            prices = WebDriverWait(item, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'td')))
            if len(prices) != 11:
                raise MyError('「落札額」要素を取得できませんでした')
            price = prices[3]
            if price.text is None:
                raise MyError('「落札額」要素が存在しません')
            if not price.text.strip():
                raise MyError('「落札額」要素が空です')
            self.info_dict['落札額'] = price.text.strip()
        except MyError as e:
            error = '商品情報取得エラー（一部）'
            text = str(e)
            self.logger_object.write_log(error, text, self.id, self.now_url)
        except Exception:
            error = '商品情報取得エラー（一部）'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, self.id, self.now_url)

    def sub_get_item_get_charge(self, item):
        '''
        「落札手数料」を取得
        '''

        try:
            if self.info_dict['落札額'] != '情報取得失敗':
                charge = str(int(self.info_dict['落札額'].replace('円', '').replace(',', '').strip()) * 0.088)
                self.info_dict['落札手数料'] = int(Decimal(charge).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
        except MyError as e:
            error = '商品情報取得エラー（一部）'
            text = str(e)
            self.logger_object.write_log(error, text, self.id, self.now_url)
        except Exception:
            error = '商品情報取得エラー（一部）'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, self.id, self.now_url)

    def trans_next(self, flag):
        '''
        次ページに遷移
        '''

        try:
            now_url = self.now_url
            try:
                next_url = self.driver.find_element_by_link_text('次の50件')
            except NoSuchElementException:
                flag = True
                return flag
            if next_url.get_attribute('href') is None:
                raise MyError('次ページURL要素が存在しません')
            if not next_url.get_attribute('href').strip():
                raise MyError('次ページURL要素が空です')
            self.now_url = urljoin(self.absolute_url, next_url.get_attribute('href').strip())
            self.driver.get(self.now_url)
            return flag
        except MyError as e:
            error = '次ページ遷移エラー'
            text = str(e)
            self.logger_object.write_log(error, text, self.id, now_url)
            flag = True
            return flag
        except Exception:
            error = '次ページ遷移エラー'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, self.id, now_url)
            flag = True
            return flag

    def interval(self):
        '''
        インターバルを取る
        '''

        try:
            time.sleep(2)
        except Exception:
            error = 'インターバルエラー'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, self.id, self.now_url)

    def quit_driver(self):
        '''
        ドライバーを閉じる
        '''

        try:
            self.driver.quit()
        except Exception:
            raise
