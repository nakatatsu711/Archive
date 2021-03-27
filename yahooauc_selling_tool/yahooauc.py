'''Selenium'''
from selenium import webdriver  # ブラウザを自動操作
from selenium.webdriver.common.keys import Keys  # キーを送信
from selenium.webdriver.chrome.options import Options  # オプションを指定
from selenium.webdriver.support.ui import Select  # selectタグを操作
'''requests'''
import requests  # 画像取得
'''標準ライブラリ'''
import csv  # CSVファイル読み込み
import datetime  # 日付
import glob  # ファイル検索
import os  # ディレクトリ確認、作成
import re  # 正規表現
import shutil  # ディレクトリ削除
import time  # 待ち時間を指定
import traceback  # スタックトレースを取得


class ChromeDriver:
    '''
    chromedriverの操作
    '''

    def __init__(self, headers, executable_path, txt_name, encoding):
        '''
        初期化
        '''

        try:
            # GoogleChrome
            options = Options()
            options.add_argument('--headless')  # ヘッドレスモード
            options.add_argument('--incognito')  # シークレットモード
            options.add_argument('--window-size=1200,1291')  # 画面サイズを指定
            options.add_argument(headers)
            self.driver = webdriver.Chrome(options=options, executable_path=executable_path)
            self.driver.set_page_load_timeout(30)
            # テキストファイル読み込み
            with open(txt_name, encoding=encoding) as rf:
                setting_list = [s.rstrip() for s in rf.readlines()]
                if len(setting_list) == 3:
                    m1 = re.search(r'INTERVAL = (\d+)$', setting_list[0])
                    m2 = re.search(r'ID = (.+)$', setting_list[1])
                    m3 = re.search(r'PASSWORD = (.+)$', setting_list[2])
                    if m1 and m2 and m3:
                        self.interval = m1.group(1)
                        self.id = m2.group(1)
                        self.password = m3.group(1)
                    else:
                        raise MyError('設定が無効な値です')
                else:
                    raise MyError('設定が正しくありません')
        except Exception:
            print("'''")
            print('chromedriver初期化、設定エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def access_top(self, url):
        '''
        トップページにアクセス
        '''

        try:
            self.driver.get(url)
            time.sleep(2)
        except Exception:
            print("'''")
            print('トップページアクセスエラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def close_modal(self):
        '''
        モーダルを閉じる
        '''

        try:
            modals = self.driver.find_elements_by_css_selector('#js-prMdl > #pfmmdl > a#js-close')
            if modals:
                modals[0].click()
                time.sleep(1)
            else:
                pass
        except Exception:
            print("'''")
            print('モーダルクローズエラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def login(self):
        '''
        ログイン
        '''

        try:
            login = self.driver.find_element_by_css_selector('#masthead .yjmthloginarea > p > strong > a')
            login.click()
            time.sleep(2)
            id_element = self.driver.find_element_by_id('username')
            id_element.send_keys(self.id)
            time.sleep(1)
            id_element.send_keys(Keys.RETURN)
            time.sleep(2)
            password_element = self.driver.find_element_by_id('passwd')
            password_element.send_keys(self.password)
            time.sleep(1)
            password_element.send_keys(Keys.RETURN)
            time.sleep(2)
        except Exception:
            print("'''")
            print('ログインエラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def access_sell(self, sell_url):
        '''
        出品ページにアクセス
        '''

        try:
            self.driver.get(sell_url)
            time.sleep(2)
        except Exception:
            print("'''")
            print('出品ページアクセスエラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def close_modal2(self):
        '''
        モーダルを閉じる
        '''

        try:
            modals = self.driver.find_elements_by_css_selector('.CrossListingModal.js-modal-wrap.is-show #js-ListingModalClose')
            if modals:
                modals[0].click()
                time.sleep(1)
            else:
                pass
        except Exception:
            print("'''")
            print('モーダルクローズエラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def sell_image(self, download_dir, row_num):
        '''
        「画像」を出品
        '''

        try:
            image_upload = self.driver.find_element_by_id('selectFileMultiple')
            images = sorted(glob.glob(download_dir + str(row_num) + '-*.jpg'))
            for image in images:
                image_upload.send_keys(image)
                time.sleep(2)
        except Exception:
            print("'''")
            print('「画像」出品エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def sell_name(self, row):
        '''
        「商品名」を出品
        '''

        try:
            if row['タイトル']:
                name = self.driver.find_element_by_id('fleaTitleForm')
                name.send_keys(row['タイトル'])
            else:
                raise MyError('【タイトル】が入力されていません')
        except MyError as e:
            print("'''")
            print('「商品名」出品エラー')
            print(e)
            print("'''")
            raise
        except Exception:
            print("'''")
            print('「商品名」出品エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def sell_category(self, category_list):
        '''
        「カテゴリ」を出品
        '''

        try:
            category = self.driver.find_element_by_id('acMdCateChange')
            category.click()
            time.sleep(2)
            # "リストから選択する"をクリック
            lists = self.driver.find_elements_by_css_selector('#CategorySelect > ul.Tab.cf > li.Tab__item.js-tab-item > a')
            if lists:
                for list in lists:
                    if list.text is not None:
                        if list.text.strip() == 'リストから選択する':
                            list.click()
                            time.sleep(1)
                            break
                        else:
                            continue
                    else:
                        continue
                else:
                    raise MyError('"リストから選択する"の要素が見つかりませんでした')
            else:
                raise MyError('"リストから選択する"の要素取得に失敗しました')
            # category_listからカテゴリを選択する
            for category_parts_num, category_parts in enumerate(category_list):
                category_selects = self.driver.find_elements_by_css_selector('#ptsSlctList' + str(category_parts_num) + ' ul > li > a')
                if category_selects:
                    for category_select in category_selects:
                        if category_select.text is not None:
                            if category_select.text.strip():
                                if category_select.text.strip() == category_parts:
                                    category_select.click()
                                    time.sleep(1)
                                    break
                                else:
                                    continue
                            else:
                                continue
                        else:
                            continue
                    else:
                        raise MyError('カテゴリパーツの要素が見つかりませんでした')
                else:
                    raise MyError('カテゴリパーツの要素取得に失敗しました')
            # "このカテゴリに出品"をクリック
            category_update = self.driver.find_element_by_id('updateCategory')
            category_update.click()
            time.sleep(2)
        except MyError as e:
            print("'''")
            print('「カテゴリ」出品エラー')
            print(e)
            print("'''")
            raise
        except Exception:
            print("'''")
            print('「カテゴリ」出品エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def sell_status(self, row):
        '''
        「商品の状態」を出品
        '''

        try:
            if row['商品の状態']:
                status = self.driver.find_element_by_name('istatus')
                status_select = Select(status)
                if (row['商品の状態'] == '新品') or (row['商品の状態'] == '未使用'):
                    status_select.select_by_value('new')
                elif row['商品の状態'] == '未使用に近い':
                    status_select.select_by_value('used10')
                elif row['商品の状態'] == '目立った傷や汚れなし':
                    status_select.select_by_value('used20')
                elif row['商品の状態'] == 'やや傷や汚れあり':
                    status_select.select_by_value('used40')
                elif row['商品の状態'] == '傷や汚れあり':
                    status_select.select_by_value('used60')
                elif row['商品の状態'] == '全体的に状態が悪い':
                    status_select.select_by_value('used80')
                else:
                    raise MyError('【商品の状態】が無効な値です')
            else:
                raise MyError('【商品の状態】が入力されていません')
        except MyError as e:
            print("'''")
            print('「商品の状態」出品エラー')
            print(e)
            print("'''")
            raise
        except Exception:
            print("'''")
            print('「商品の状態」出品エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def sell_description(self, row):
        '''
        「説明」を出品
        '''

        try:
            if row['説明']:
                description_html = self.driver.find_element_by_id('aucHTMLtag')
                description_html.click()
                time.sleep(1)
                description_textarea = self.driver.find_element_by_name('Description_plain_work')
                description_textarea.send_keys(row['説明'])
            else:
                raise MyError('【説明】が入力されていません')
        except MyError as e:
            print("'''")
            print('「説明」出品エラー')
            print(e)
            print("'''")
            raise
        except Exception:
            print("'''")
            print('「説明」出品エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def sell_quantity(self, row):
        '''
        「個数」を出品
        '''

        try:
            if row['個数']:
                quantity = self.driver.find_element_by_name('Quantity')
                quantity_select = Select(quantity)
                if row['個数'] == '1':
                    quantity_select.select_by_value('1')
                elif row['個数'] == '2':
                    quantity_select.select_by_value('2')
                elif row['個数'] == '3':
                    quantity_select.select_by_value('3')
                elif row['個数'] == '4':
                    quantity_select.select_by_value('4')
                elif row['個数'] == '5':
                    quantity_select.select_by_value('5')
                elif row['個数'] == '6':
                    quantity_select.select_by_value('6')
                elif row['個数'] == '7':
                    quantity_select.select_by_value('7')
                elif row['個数'] == '8':
                    quantity_select.select_by_value('8')
                elif row['個数'] == '9':
                    quantity_select.select_by_value('9')
                else:
                    raise MyError('【個数】が無効な値です')
            else:
                raise MyError('【個数】が入力されていません')
        except MyError as e:
            print("'''")
            print('「個数」出品エラー')
            print(e)
            print("'''")
            raise
        except Exception:
            print("'''")
            print('「個数」出品エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def sell_location(self, row):
        '''
        「発送元の地域」を出品
        '''

        try:
            if row['商品発送元の都道府県']:
                location = self.driver.find_element_by_name('loc_cd')
                location_select = Select(location)
                if row['商品発送元の都道府県'] == '北海道':
                    location_select.select_by_value('1')
                elif row['商品発送元の都道府県'] == '青森県':
                    location_select.select_by_value('2')
                elif row['商品発送元の都道府県'] == '岩手県':
                    location_select.select_by_value('3')
                elif row['商品発送元の都道府県'] == '宮城県':
                    location_select.select_by_value('4')
                elif row['商品発送元の都道府県'] == '秋田県':
                    location_select.select_by_value('5')
                elif row['商品発送元の都道府県'] == '山形県':
                    location_select.select_by_value('6')
                elif row['商品発送元の都道府県'] == '福島県':
                    location_select.select_by_value('7')
                elif row['商品発送元の都道府県'] == '茨城県':
                    location_select.select_by_value('8')
                elif row['商品発送元の都道府県'] == '栃木県':
                    location_select.select_by_value('9')
                elif row['商品発送元の都道府県'] == '群馬県':
                    location_select.select_by_value('10')
                elif row['商品発送元の都道府県'] == '埼玉県':
                    location_select.select_by_value('11')
                elif row['商品発送元の都道府県'] == '千葉県':
                    location_select.select_by_value('12')
                elif row['商品発送元の都道府県'] == '東京都':
                    location_select.select_by_value('13')
                elif row['商品発送元の都道府県'] == '神奈川県':
                    location_select.select_by_value('14')
                elif row['商品発送元の都道府県'] == '山梨県':
                    location_select.select_by_value('15')
                elif row['商品発送元の都道府県'] == '長野県':
                    location_select.select_by_value('16')
                elif row['商品発送元の都道府県'] == '新潟県':
                    location_select.select_by_value('17')
                elif row['商品発送元の都道府県'] == '富山県':
                    location_select.select_by_value('18')
                elif row['商品発送元の都道府県'] == '石川県':
                    location_select.select_by_value('19')
                elif row['商品発送元の都道府県'] == '福井県':
                    location_select.select_by_value('20')
                elif row['商品発送元の都道府県'] == '岐阜県':
                    location_select.select_by_value('21')
                elif row['商品発送元の都道府県'] == '静岡県':
                    location_select.select_by_value('22')
                elif row['商品発送元の都道府県'] == '愛知県':
                    location_select.select_by_value('23')
                elif row['商品発送元の都道府県'] == '三重県':
                    location_select.select_by_value('24')
                elif row['商品発送元の都道府県'] == '滋賀県':
                    location_select.select_by_value('25')
                elif row['商品発送元の都道府県'] == '京都府':
                    location_select.select_by_value('26')
                elif row['商品発送元の都道府県'] == '大阪府':
                    location_select.select_by_value('27')
                elif row['商品発送元の都道府県'] == '兵庫県':
                    location_select.select_by_value('28')
                elif row['商品発送元の都道府県'] == '奈良県':
                    location_select.select_by_value('29')
                elif row['商品発送元の都道府県'] == '和歌山県':
                    location_select.select_by_value('30')
                elif row['商品発送元の都道府県'] == '鳥取県':
                    location_select.select_by_value('31')
                elif row['商品発送元の都道府県'] == '島根県':
                    location_select.select_by_value('32')
                elif row['商品発送元の都道府県'] == '岡山県':
                    location_select.select_by_value('33')
                elif row['商品発送元の都道府県'] == '広島県':
                    location_select.select_by_value('34')
                elif row['商品発送元の都道府県'] == '山口県':
                    location_select.select_by_value('35')
                elif row['商品発送元の都道府県'] == '徳島県':
                    location_select.select_by_value('36')
                elif row['商品発送元の都道府県'] == '香川県':
                    location_select.select_by_value('37')
                elif row['商品発送元の都道府県'] == '愛媛県':
                    location_select.select_by_value('38')
                elif row['商品発送元の都道府県'] == '高知県':
                    location_select.select_by_value('39')
                elif row['商品発送元の都道府県'] == '福岡県':
                    location_select.select_by_value('40')
                elif row['商品発送元の都道府県'] == '佐賀県':
                    location_select.select_by_value('41')
                elif row['商品発送元の都道府県'] == '長崎県':
                    location_select.select_by_value('42')
                elif row['商品発送元の都道府県'] == '熊本県':
                    location_select.select_by_value('43')
                elif row['商品発送元の都道府県'] == '大分県':
                    location_select.select_by_value('44')
                elif row['商品発送元の都道府県'] == '宮崎県':
                    location_select.select_by_value('45')
                elif row['商品発送元の都道府県'] == '鹿児島県':
                    location_select.select_by_value('46')
                elif row['商品発送元の都道府県'] == '沖縄県':
                    location_select.select_by_value('47')
                elif row['商品発送元の都道府県'] == '海外':
                    location_select.select_by_value('48')
                else:
                    raise MyError('【商品発送元の都道府県】が無効な値です')
            else:
                raise MyError('【商品発送元の都道府県】が入力されていません')
        except MyError as e:
            print("'''")
            print('「発送元の地域」出品エラー')
            print(e)
            print("'''")
            raise
        except Exception:
            print("'''")
            print('「発送元の地域」出品エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def sell_shippingwho(self, row):
        '''
        「送料負担」を出品
        '''

        try:
            if row['送料負担'] == '落札者':
                shippingwho = self.driver.find_element_by_id('auc_shipping_who')
                shippingwho_select = Select(shippingwho)
                shippingwho_select.select_by_value('buyer')
            else:
                raise MyError('【送料負担】が無効な値か入力されていません')
        except MyError as e:
            print("'''")
            print('「送料負担」出品エラー')
            print(e)
            print("'''")
            raise
        except Exception:
            print("'''")
            print('「送料負担」出品エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def sell_deliverymethod(self, row):
        '''
        「配送方法」を出品
        '''

        try:
            if row['配送方法1'] and row['配送方法1全国一律価格']:
                deliverymethod_checkboxs = self.driver.find_elements_by_css_selector('#auc_shipname_block1 > label.CheckExpand__label.CheckExpand__label--postageBox.cf')
                if deliverymethod_checkboxs:
                    deliverymethod_checkbox_ischecks = self.driver.find_elements_by_css_selector('#auc_shipname_block1 > label.CheckExpand__label.CheckExpand__label--postageBox.cf')
                    if deliverymethod_checkbox_ischecks:
                        pass
                    else:
                        deliverymethod_checkboxs[0].click()
                        time.sleep(1)
                else:
                    deliverymethod_add = self.driver.find_element_by_id('auc_add_shipform')
                    deliverymethod_add.click()
                    time.sleep(1)
                    deliverymethod_checkbox = self.driver.find_element_by_css_selector('#auc_shipname_block1 > label.CheckExpand__label.CheckExpand__label--postageBox.cf')
                    deliverymethod_checkbox.click()
                    time.sleep(1)
                deliverymethod = self.driver.find_element_by_id('auc_shipname_standard1')
                deliverymethod_select = Select(deliverymethod)
                deliverymethod_select.select_by_value('other')
                deliverymethod_input = self.driver.find_element_by_id('auc_shipname_text1')
                deliverymethod_input.clear()
                deliverymethod_input.send_keys(row['配送方法1'])
                deliverymethod_price = self.driver.find_element_by_id('auc_shipname_uniform_fee_data1')
                deliverymethod_price.clear()
                deliverymethod_price.send_keys(row['配送方法1全国一律価格'])
            else:
                raise MyError('【配送方法1】が入力されていません')
        except MyError as e:
            print("'''")
            print('「配送方法」出品エラー')
            print(e)
            print("'''")
            raise
        except Exception:
            print("'''")
            print('「配送方法」出品エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def sell_shipschedule(self, row):
        '''
        「支払いから発送までの日数」を出品
        '''

        try:
            if row['発送までの日数']:
                shipschedule = self.driver.find_element_by_name('shipschedule')
                shipschedule_select = Select(shipschedule)
                if row['発送までの日数'] == '1〜2日':
                    shipschedule_select.select_by_value('1')
                elif row['発送までの日数'] == '2〜3日':
                    shipschedule_select.select_by_value('7')
                elif row['発送までの日数'] == '3〜7日':
                    shipschedule_select.select_by_value('2')
                elif row['発送までの日数'] == '7〜13日':
                    shipschedule_select.select_by_value('5')
                elif row['発送までの日数'] == '14日以降':
                    shipschedule_select.select_by_value('6')
                else:
                    raise MyError('【発送までの日数】が無効な値です')
            else:
                raise MyError('【発送までの日数】が入力されていません')
        except MyError as e:
            print("'''")
            print('「支払いから発送までの日数」出品エラー')
            print(e)
            print("'''")
            raise
        except Exception:
            print("'''")
            print('「支払いから発送までの日数」出品エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def sell_startprice(self, row):
        '''
        「開始価格」を出品
        '''

        try:
            if row['開始価格'] and row['即決価格']:
                # 開始価格
                startprice = self.driver.find_element_by_id('auc_StartPrice_auction')
                startprice.send_keys(row['開始価格'])
                # 即決価格
                endprice_trigger = self.driver.find_element_by_css_selector('#price_auction .Overhead.js-toggleExpand .Overhead__title.Overhead__title--fontNormal.js-toggleExpand-trigger')
                endprice_trigger.click()
                time.sleep(1)
                endprice = self.driver.find_element_by_id('auc_BidOrBuyPrice_auction')
                endprice.send_keys(row['即決価格'])
            else:
                raise MyError('【開始価格】もしくは【即決価格】が入力されていません')
        except MyError as e:
            print("'''")
            print('「開始価格」出品エラー')
            print(e)
            print("'''")
            raise
        except Exception:
            print("'''")
            print('「開始価格」出品エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def sell_closingymdtime(self, row):
        '''
        「終了する日時」を出品
        '''

        try:
            if row['終了時間']:
                # 終了する日にち
                closingymd_value = datetime.date.today() + datetime.timedelta(days=2)
                closingymd = self.driver.find_element_by_id('ClosingYMD')
                closingymd_select = Select(closingymd)
                closingymd_select.select_by_value(str(closingymd_value))
                # 終了する時間
                if row['終了時間'].isdecimal():
                    closingtime = self.driver.find_element_by_id('ClosingTime')
                    closingtime_select = Select(closingtime)
                    closingtime_select.select_by_value(row['終了時間'])
                else:
                    raise MyError('【終了時間】が無効な値です')
            else:
                raise MyError('【終了時間】が入力されていません')
        except MyError as e:
            print("'''")
            print('「終了する日時」出品エラー')
            print(e)
            print("'''")
            raise
        except Exception:
            print("'''")
            print('「終了する日時」出品エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def sell_option(self):
        '''
        「オプション」を出品
        '''

        try:
            # "自動再出品"を設定
            resubmit = self.driver.find_element_by_id('numResubmit')
            resubmit_select = Select(resubmit)
            resubmit_select.select_by_value('3')  # 3回
            markdown = self.driver.find_element_by_id('markdown_ratio')
            markdown_select = Select(markdown)
            markdown_select.select_by_value('0')  # 自動で値下げしない
            # "入札者認証制限を設定する"をチェック
            creditlimit_ischecks = self.driver.find_elements_by_css_selector('#option_Area .CheckBox.js-checkbox-wrap > label.CheckBox__label.js-checkbox-label.is-check')
            if len(creditlimit_ischecks) == 4:
                pass
            elif len(creditlimit_ischecks) == 3:
                creditlimits = self.driver.find_elements_by_css_selector('#option_Area .CheckBox.js-checkbox-wrap > label.CheckBox__label.js-checkbox-label')
                if creditlimits:
                    for creditlimit in creditlimits[::-1]:
                        if creditlimit.text is not None:
                            if creditlimit.text.strip() == '入札者認証制限を設定する':
                                creditlimit.click()
                                break
                            else:
                                continue
                        else:
                            continue
                    else:
                        raise MyError('"入札者認証制限を設定する"の要素が見つかりませんでした')
                else:
                    raise MyError('"入札者認証制限を設定する"の要素取得に失敗しました')
            else:
                raise MyError('"入札者認証制限を設定する"の要素取得に失敗しました')
        except MyError as e:
            print("'''")
            print('「オプション」出品エラー')
            print(e)
            print("'''")
            raise
        except Exception:
            print("'''")
            print('「オプション」出品エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def confirm(self):
        '''
        "確認する"をクリック
        '''

        try:
            confirm = self.driver.find_element_by_css_selector('.Button.Button--proceed')
            confirm.click()
            time.sleep(2)
        except Exception:
            print("'''")
            print('"確認する"ボタンクリックエラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def confirm_error(self):
        '''
        出品エラーを確認
        '''

        try:
            errors = self.driver.find_elements_by_css_selector('.decErrorBox.u-marginB10 > .decErrorBox__title')
            if errors:
                raise MyError('入力内容に誤りがあります')
            else:
                pass
        except MyError as e:
            print("'''")
            print('出品確認エラー')
            print(e)
            print("'''")
            raise
        except Exception:
            print("'''")
            print('出品確認エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def submit(self):
        '''
        "ガイドラインと上記規約に同意して出品する"をクリック
        '''

        try:
            submit = self.driver.find_element_by_id('auc_preview_submit_up')
            submit.click()
            time.sleep(2)
        except Exception:
            print("'''")
            print('"ガイドラインと上記規約に同意して出品する"ボタンクリックエラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def take_interval(self):
        '''
        インターバル管理
        '''

        try:
            time.sleep(int(self.interval))
        except MyError as e:
            print("'''")
            print('インターバルエラー')
            print(e)
            print("'''")
        except Exception:
            print("'''")
            print('インターバルエラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def quit_driver(self):
        '''
        ドライバーを閉じる
        '''

        try:
            self.driver.quit()
        except Exception:
            print("'''")
            print('chromedriver終了エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise


class ReadCSV:
    '''
    CSVファイル読み込み
    '''

    def __init__(self, csv_name, encoding):
        '''
        初期化
        '''

        try:
            self.rf = open(csv_name, encoding=encoding)
            self.reader = csv.DictReader(self.rf)
        except MyError as e:
            print("'''")
            print('CSVファイル読み込み初期化エラー')
            print(e)
            print("'''")
            self.close_csv()
            raise
        except Exception:
            print("'''")
            print('CSVファイル読み込み初期化エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def make_dir(self):
        '''
        画像を保存するフォルダを作成
        '''

        try:
            if os.path.isdir('./yahooauc_images/'):
                shutil.rmtree('./yahooauc_images/')
                os.mkdir('./yahooauc_images/')
            else:
                os.mkdir('./yahooauc_images/')
        except Exception:
            print("'''")
            print('画像フォルダ作成エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def save_image(self, row, row_num):
        '''
        画像を保存
        '''

        try:
            img_num = 1
            while img_num <= 10:
                img_key = '画像' + str(img_num)
                if row[img_key]:
                    data = self.save_image_sub(row, img_key)
                    with open('./yahooauc_images/' + str(row_num) + '-' + str(img_num) + '.jpg', 'wb') as wf:
                        wf.write(data.content)
                else:
                    pass
                img_num += 1
        except Exception:
            print("'''")
            print('画像保存エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def save_image_sub(self, row, img_key):
        '''
        画像を保存（requests）
        '''

        try:
            data = requests.get(row[img_key], timeout=30)
            time.sleep(1)
            return data
        except requests.exceptions.SSLError:  # SSL認証エラー
            try:
                data = requests.get(row[img_key], verify=False, timeout=30)
                time.sleep(1)
                return data
            except Exception:
                raise
        except requests.exceptions.ConnectionError:  # 通信エラー
            try:
                time.sleep(10)
                data = requests.get(row[img_key], timeout=30)
                time.sleep(1)
                return data
            except Exception:
                raise
        except Exception:
            raise

    def close_csv(self):
        '''
        CSVファイルを閉じる
        '''

        try:
            self.rf.close()
        except Exception:
            print("'''")
            print('CSVファイル終了エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def del_dir(self):
        '''
        画像を保存するフォルダを削除
        '''

        try:
            if os.path.isdir('./yahooauc_images/'):
                shutil.rmtree('./yahooauc_images/')
            else:
                pass
        except Exception:
            print("'''")
            print('画像フォルダ削除エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise


class ReadCategoryCSV:
    '''
    カテゴリCSVファイル読み込み
    '''

    def __init__(self, category_csv_name, encoding):
        '''
        初期化
        '''

        try:
            self.rf_category = open(category_csv_name, encoding=encoding)
            self.reader_category = csv.DictReader(self.rf_category)
        except Exception:
            print("'''")
            print('カテゴリCSVファイル読み込み初期化エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def get_category(self, row):
        '''
        カテゴリを取得
        '''

        try:
            if row['カテゴリ']:
                for row_category in self.reader_category:
                    if row['カテゴリ'] == row_category['カテゴリID'].strip():
                        category_list = [category_parts.strip() for category_parts in row_category['カテゴリ'].split('>')]
                        if category_list:
                            del category_list[0]
                        else:
                            raise MyError('【カテゴリ】が入力されていません')
                        return category_list
                    else:
                        continue
                else:
                    raise MyError('【カテゴリ】が無効な値です')
            else:
                raise MyError('【カテゴリ】が入力されていません')
        except MyError as e:
            print("'''")
            print('カテゴリ取得エラー')
            print(e)
            print("'''")
            self.close_csv()
            raise
        except Exception:
            print("'''")
            print('カテゴリ取得エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            self.close_csv()
            raise

    def close_csv(self):
        '''
        カテゴリCSVファイルを閉じる
        '''

        try:
            self.rf_category.close()
        except Exception:
            print("'''")
            print('カテゴリCSVファイル終了エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise


class MyError(Exception):
    '''
    カスタム例外クラス
    '''

    def __init__(self, value):
        '''
        初期化
        '''

        try:
            self.value = value
        except Exception:
            print("'''")
            print('カスタム例外クラス初期化エラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise

    def __str__(self):
        '''
        エラー表示を返す
        '''

        try:
            return self.value
        except Exception:
            print("'''")
            print('カスタム例外クラスリターンエラー')
            text = traceback.format_exc()
            print(text.strip())
            print("'''")
            raise
