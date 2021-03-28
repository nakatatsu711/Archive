import sys
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


URL = 'https://www.lancers.jp/user/login?ref=header_menu'
URL_TITLE = 'ランサーズ'
# 設定値
mail_address = 'メールアドレス'
password = 'パスワード'
chromedriver_path = 'ChromeDriverのパス'


def input_keyword():
    '''
    メインの処理
    ランサーズのログインページからログインし、指定キーワードを取得し、テキストファイルに保存
    '''

    # ChromeのWebDriverオブジェクトを作成し、ランサーズのトップページを開く
    driver = webdriver.Chrome(chromedriver_path)
    driver.get(URL)
    assert URL_TITLE in driver.title

    # ログインページからログイン
    input_element = driver.find_element_by_name('data[User][email]')
    input_element.send_keys(mail_address)
    input_element = driver.find_element_by_name('data[User][password]')
    input_element.send_keys(password)
    time.sleep(2)
    input_element.send_keys(Keys.RETURN)

    # '仕事を探す'をクリック
    driver.find_elements_by_css_selector('.header-menu__left__item--work > a')[0].click()

    # コマンドラインから入力した仕事検索キーワードで検索
    work = sys.argv[1]
    input_element = driver.find_element_by_id('Keyword')
    input_element.send_keys(work)
    time.sleep(2)
    input_element.send_keys(Keys.RETURN)

    # 1番目にヒットしたページに遷移
    time.sleep(2)
    driver.find_elements_by_css_selector('.c-media__content > .c-media__content__right > a')[0].click()
    assert work in driver.title

    # '作業を開始する'をクリック
    time.sleep(2)
    driver.find_element_by_link_text('作業を開始する').click()

    # 同意ページがある場合、'同意して作業を開始する'をクリック
    try:
        only_first = driver.find_element_by_id('form_end')
        time.sleep(2)
        only_first.click()
    except NoSuchElementException:
        pass

    # 'この作業を開始する'をクリック
    time.sleep(2)
    driver.find_elements_by_css_selector('div.mar_t20 > input')[0].click()

    # 指定キーワードを収集し、リストにする
    objects = driver.find_elements_by_css_selector('.taskFormWrap > p > span')
    keywords = []
    for keyword in objects:
        keywords.append(keyword.text[10:])

    # テキストファイルに書き出す
    with open('yahoo2_data.txt', 'w') as f:
        f.write('\n'.join(keywords))

    # ブラウザを閉じる
    driver.quit()


if __name__ == '__main__':
    input_keyword()
