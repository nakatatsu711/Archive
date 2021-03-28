'''モジュール'''
from module_ecoauc.myerror import MyError
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
import time  # 待ち時間を指定
import traceback  # スタックトレースを取得
from urllib.parse import urljoin  # 絶対URL取得


class ChromeDriver:
    '''
    ChromeDriverの操作
    '''

    def __init__(self, login_url, ecoauc_url, logger_object):
        '''
        初期化
        '''

        try:
            # URL
            self.absolute_url = ecoauc_url
            self.now_url = login_url
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
            # ユーザーエージェント
            with open(ua_path, encoding=self.logger_object.encoding) as rf:
                ua = rf.readline().rstrip()
                headers = '--user-agent=' + ua
            # GoogleChrome初期設定
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--window-size=1200,1291')
            options.add_argument('--log-level=3')
            options.add_argument(headers)
            self.driver = webdriver.Chrome(options=options, executable_path=executable_path)
            self.driver.set_page_load_timeout(60)
            # アカウントパス
            account_path = os.getcwd() + '/setting_file/ecoauc_account.txt'
            account_path = account_path.replace('/', os.sep)
            # アカウントを読み込む
            with open(account_path, encoding=self.logger_object.encoding) as rf:
                self.email = rf.readline().rstrip()
                self.password = rf.readline().rstrip()
        except Exception:
            raise

    def access(self):
        '''
        各ページにアクセス
        '''

        try:
            self.driver.get(self.now_url)
        except Exception:
            self.logger_object.write_log('アクセスエラー', traceback.format_exc().strip(), self.now_url)
            raise

    def login(self):
        '''
        ログイン
        '''

        try:
            # Eメール
            email = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.NAME, 'email_address')))
            email.send_keys(self.email)
            email.send_keys(Keys.RETURN)
            # パスワード
            password = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.NAME, 'password')))
            password.send_keys(self.password)
            time.sleep(1)
            # ログイン
            password.send_keys(Keys.RETURN)
            time.sleep(1)
            # ログインの可否を確認
            if self.driver.current_url == self.now_url:
                raise MyError('ログインに失敗しました')
            self.now_url = self.absolute_url
        except MyError as e:
            self.logger_object.write_log('ログインエラー', str(e), '')
            raise
        except Exception:
            self.logger_object.write_log('ログインエラー', traceback.format_exc().strip(), '')
            raise

    def get_item(self):
        '''
        商品情報を取得
        '''

        try:
            # リスト初期化
            self.info_list = []
            items = WebDriverWait(self.driver, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '#picture > .row > .col-sm-6.col-md-4.col-lg-3')))
            for item in items:
                # 辞書初期化
                self.info_dict = {}
                self.info_dict['商品名'] = '-'
                self.info_dict['ランク'] = '-'
                self.info_dict['開始価格'] = '-'
                self.info_dict['出品順位'] = '-'
                self.info_dict['商品写真URL'] = '-'
                # 「商品名」
                self.sub_get_item_get_name(item)
                # 「ランク」
                self.sub_get_item_get_rank(item)
                # 「開始価格」
                self.sub_get_item_get_price(item)
                # 「出品順位」
                self.sub_get_item_get_ranking(item)
                # 「商品写真URL」
                self.sub_get_item_get_url(item)
                # リストに追加
                self.info_list.append(self.info_dict)
        except Exception:
            self.logger_object.write_log('商品情報取得エラー', traceback.format_exc().strip(), self.now_url)

    def sub_get_item_get_name(self, item):
        '''
        「商品名」を取得
        '''

        try:
            name = WebDriverWait(item, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.card-title-block > b')))
            if name.text is None:
                raise MyError('「商品名」要素が存在しません')
            if not name.text.strip():
                raise MyError('「商品名」要素が空です')
            self.info_dict['商品名'] = name.text.strip()
        except MyError as e:
            self.logger_object.write_log('商品情報取得エラー（一部）', str(e), self.now_url)
        except Exception:
            self.logger_object.write_log('商品情報取得エラー（一部）', traceback.format_exc().strip(), self.now_url)

    def sub_get_item_get_rank(self, item):
        '''
        「ランク」を取得
        '''

        try:
            ranks = WebDriverWait(item, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'ul.canopy.canopy-3.text-default > li')))
            if len(ranks) < 1:
                raise MyError('「ランク」要素を取得できませんでした')
            rank = ranks[0]
            if rank.text is None:
                raise MyError('「ランク」要素が存在しません')
            if not rank.text.replace('ランク', '').strip():
                raise MyError('「ランク」要素が空です')
            self.info_dict['ランク'] = rank.text.replace('ランク', '').strip()
        except MyError as e:
            self.logger_object.write_log('商品情報取得エラー（一部）', str(e), self.now_url)
        except Exception:
            self.logger_object.write_log('商品情報取得エラー（一部）', traceback.format_exc().strip(), self.now_url)

    def sub_get_item_get_price(self, item):
        '''
        「開始価格」を取得
        '''

        try:
            prices = WebDriverWait(item, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'ul.canopy.canopy-3.text-default > li')))
            if len(prices) < 2:
                raise MyError('「開始価格」要素を取得できませんでした')
            price = prices[1]
            if price.text is None:
                raise MyError('「開始価格」要素が存在しません')
            if not price.text.replace('開始価格', '').strip():
                raise MyError('「開始価格」要素が空です')
            self.info_dict['開始価格'] = price.text.replace('開始価格', '').strip()
        except MyError as e:
            self.logger_object.write_log('商品情報取得エラー（一部）', str(e), self.now_url)
        except Exception:
            self.logger_object.write_log('商品情報取得エラー（一部）', traceback.format_exc().strip(), self.now_url)

    def sub_get_item_get_ranking(self, item):
        '''
        「出品順位」を取得
        '''

        try:
            rankings = WebDriverWait(item, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'ul.canopy.canopy-3.text-default > li')))
            if len(rankings) < 3:
                raise MyError('「出品順位」要素を取得できませんでした')
            ranking = rankings[2]
            if ranking.text is None:
                raise MyError('「出品順位」要素が存在しません')
            if not ranking.text.replace('出品順位', '').strip():
                raise MyError('「出品順位」要素が空です')
            self.info_dict['出品順位'] = ranking.text.replace('出品順位', '').strip()
        except MyError as e:
            self.logger_object.write_log('商品情報取得エラー（一部）', str(e), self.now_url)
        except Exception:
            self.logger_object.write_log('商品情報取得エラー（一部）', traceback.format_exc().strip(), self.now_url)

    def sub_get_item_get_url(self, item):
        '''
        「商品写真URL」を取得
        '''

        try:
            url = WebDriverWait(item, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.item-image.item-image-min > img.card-img-top')))
            if url.get_attribute('src') is None:
                raise MyError('「商品写真URL」要素が存在しません')
            if not url.get_attribute('src').strip():
                raise MyError('「商品写真URL」要素が空です')
            self.info_dict['商品写真URL'] = url.get_attribute('src').strip()
        except MyError as e:
            self.logger_object.write_log('商品情報取得エラー（一部）', str(e), self.now_url)
        except Exception:
            self.logger_object.write_log('商品情報取得エラー（一部）', traceback.format_exc().strip(), self.now_url)

    def trans_next(self, flag):
        '''
        次ページに遷移
        '''

        try:
            now_url = self.now_url
            try:
                next_url = self.driver.find_element_by_css_selector('ul.pagination > li.next.disabled')
                flag = True
                return flag
            except NoSuchElementException:
                pass
            next_url = WebDriverWait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.pagination > li.next > a')))
            if next_url.get_attribute('href') is None:
                raise MyError('次ページURL要素が存在しません')
            if not next_url.get_attribute('href').strip():
                raise MyError('次ページURL要素が空です')
            self.now_url = urljoin(self.absolute_url, next_url.get_attribute('href').strip())
            self.driver.get(self.now_url)
            return flag
        except MyError as e:
            self.logger_object.write_log('次ページ遷移エラー', str(e), now_url)
            flag = True
            return flag
        except Exception:
            self.logger_object.write_log('次ページ遷移エラー', traceback.format_exc().strip(), now_url)
            flag = True
            return flag

    def quit_driver(self):
        '''
        ドライバーを閉じる
        '''

        try:
            self.driver.quit()
        except Exception:
            raise
