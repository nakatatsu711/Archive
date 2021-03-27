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
import os  # ディレクトリ確認、作成
import re  # 正規表現
import time  # 待ち時間を指定
import traceback  # スタックトレースを取得
from urllib.parse import urljoin  # 絶対URL取得


class ChromeDriver:
    '''
    ChromeDriverの操作
    '''

    def __init__(self, logger_object, amazon_url):
        '''
        初期化
        '''

        try:
            # ロガー
            self.logger_object = logger_object
            # URL
            self.absolute_url = amazon_url
            self.now_url = amazon_url
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
            self.logger_object.write_log(error, text, account['Eメール'], '')
            raise

    def login(self, account):
        '''
        ログイン
        '''

        try:
            # アカウント
            self.email = account['Eメール']
            self.password = account['パスワード']
            # Eメール
            email = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.ID, 'ap_email')))
            email.send_keys(self.email)
            time.sleep(1)
            email.send_keys(Keys.RETURN)
            # パスワード
            password = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.ID, 'ap_password')))
            password.send_keys(self.password)
            time.sleep(1)
            password.send_keys(Keys.RETURN)
            # 最小化
            self.driver.minimize_window()
        except Exception:
            error = 'ログインエラー'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, account['Eメール'], '')
            raise

    def get_item(self):
        '''
        商品情報を取得
        '''

        try:
            # リスト初期化
            self.info_list = []
            items = WebDriverWait(self.driver, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '#ordersContainer > .a-box-group.a-spacing-base.order')))
            for item in items:
                # 辞書初期化
                self.info_dict = {}
                self.info_dict['購入価格'] = '-'
                self.info_dict['注文番号'] = '-'
                self.info_dict['商品名'] = '-'
                self.info_dict['商品URL'] = '-'
                self.info_dict['ASIN'] = '-'
                self.info_dict['仕入れ'] = '-'
                # 「購入価格」
                self.sub_get_item_get_price(item)
                # 「注文番号」
                self.sub_get_item_get_num(item)
                # 「商品名」
                self.sub_get_item_get_name(item)
                # 「商品URL」、「ASIN」
                self.sub_get_item_get_url_and_asin(item)
                # 「仕入れ」
                self.sub_get_item_get_purchase(item)
                # リストに追加
                self.info_list.append(self.info_dict)
        except Exception:
            error = '商品情報取得エラー'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, self.email, self.now_url)

    def sub_get_item_get_price(self, item):
        '''
        「購入価格」を取得
        '''

        try:
            price = WebDriverWait(item, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.a-column.a-span2 span.a-color-secondary.value')))
            if price.text is None:
                raise MyError('「購入価格」要素が存在しません')
            if not price.text.strip():
                raise MyError('「購入価格」要素が空です')
            self.info_dict['購入価格'] = price.text.strip()
        except MyError as e:
            error = '商品情報取得エラー（一部）'
            text = str(e)
            self.logger_object.write_log(error, text, self.email, self.now_url)
        except Exception:
            error = '商品情報取得エラー（一部）'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, self.email, self.now_url)

    def sub_get_item_get_num(self, item):
        '''
        「注文番号」を取得
        '''

        try:
            num = WebDriverWait(item, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.a-fixed-right-grid-col.actions.a-col-right span.a-color-secondary.value')))
            if num.text is None:
                raise MyError('「注文番号」要素が存在しません')
            if not num.text.strip():
                raise MyError('「注文番号」要素が空です')
            self.info_dict['注文番号'] = num.text.strip()
        except MyError as e:
            error = '商品情報取得エラー（一部）'
            text = str(e)
            self.logger_object.write_log(error, text, self.email, self.now_url)
        except Exception:
            error = '商品情報取得エラー（一部）'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, self.email, self.now_url)

    def sub_get_item_get_name(self, item):
        '''
        「商品名」を取得
        '''

        try:
            name = WebDriverWait(item, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.a-fixed-left-grid-inner > .a-fixed-left-grid-col.a-col-right a.a-link-normal')))
            if name.text is None:
                raise MyError('「商品名」要素が存在しません')
            if not name.text.strip():
                raise MyError('「商品名」要素が空です')
            self.info_dict['商品名'] = name.text.strip()
        except MyError as e:
            error = '商品情報取得エラー（一部）'
            text = str(e)
            self.logger_object.write_log(error, text, self.email, self.now_url)
        except Exception:
            error = '商品情報取得エラー（一部）'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, self.email, self.now_url)

    def sub_get_item_get_url_and_asin(self, item):
        '''
        「商品URL」、「ASIN」を取得
        '''

        try:
            url = WebDriverWait(item, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.a-fixed-left-grid-inner > .a-fixed-left-grid-col.a-col-right a.a-link-normal')))
            if url.get_attribute('href') is None:
                raise MyError('「商品URL」要素が存在しません')
            if not url.get_attribute('href').strip():
                raise MyError('「商品URL」要素が空です')
            self.info_dict['商品URL'] = urljoin(self.absolute_url, url.get_attribute('href').strip())
            m = re.search(r'/gp/product/([^/]+)/', url.get_attribute('href').strip())
            if not m:
                raise MyError('「ASIN」を抽出できませんでした')
            self.info_dict['ASIN'] = m.group(1)
        except MyError as e:
            error = '商品情報取得エラー（一部）'
            text = str(e)
            self.logger_object.write_log(error, text, self.email, self.now_url)
        except Exception:
            error = '商品情報取得エラー（一部）'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, self.email, self.now_url)

    def sub_get_item_get_purchase(self, item):
        '''
        「仕入れ」を取得
        '''

        try:
            purchase = WebDriverWait(item, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.a-fixed-left-grid-inner > .a-fixed-left-grid-col.a-col-right span.a-size-small.a-color-secondary')))
            if purchase.text is None:
                raise MyError('「仕入れ」要素が存在しません')
            if not purchase.text.replace('販売:', '').strip():
                raise MyError('「仕入れ」要素が空です')
            self.info_dict['仕入れ'] = purchase.text.replace('販売:', '').strip()
        except MyError as e:
            error = '商品情報取得エラー（一部）'
            text = str(e)
            self.logger_object.write_log(error, text, self.email, self.now_url)
        except Exception:
            error = '商品情報取得エラー（一部）'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, self.email, self.now_url)

    def trans_next(self, flag):
        '''
        次ページに遷移
        '''

        try:
            now_url = self.now_url
            try:
                next_url = self.driver.find_element_by_css_selector('ul.a-pagination > li.a-last > a')
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
            self.logger_object.write_log(error, text, self.email, now_url)
            flag = True
            return flag
        except Exception:
            error = '次ページ遷移エラー'
            text = traceback.format_exc().strip()
            self.logger_object.write_log(error, text, self.email, now_url)
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
            self.logger_object.write_log(error, text, self.email, self.now_url)

    def quit_driver(self):
        '''
        ドライバーを閉じる
        '''

        try:
            self.driver.quit()
        except Exception:
            raise
