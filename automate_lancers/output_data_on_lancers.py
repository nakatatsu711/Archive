import sys
import times

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


URL = 'https://www.lancers.jp/user/login?ref=header_menu'
URL_TITLE = 'ランサーズ'
# 設定値
mail_address = 'メールアドレス'
password = 'パスワード'
chromedriver_path = 'ChromeDriverのパス'


def output_keyword():
    '''
    メインの処理
    ランサーズのログインページからログインし、テキストファイルから検索結果を出力
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

    # 結果入力用テキストボックスのオブジェクトを指定
    objects = driver.find_elements_by_css_selector('input.taskForm')

    # 検索結果をリストにする
    with open('yahoo2_result.txt') as f:
        keywords = [s.rstrip() for s in f.readlines()]

    # テキストボックスの数と検索結果の数を比較
    assert len(objects) == len(keywords)

    # 検索結果を入力
    i = 0
    for keyword in keywords:
        input_element = objects[i]
        input_element.send_keys(keyword)
        i += 1

    # '内容を確認する'をクリック
    time.sleep(2)
    driver.find_element_by_id('form_end').click()

    # '作業を完了する'をクリック
    time.sleep(2)
    driver.find_element_by_id('form_end').click()

    # 'マイページ'に戻る
    driver.find_elements_by_css_selector('.header-menu__left__item--mypage > a')[0].click()

    # ブラウザを閉じる
    driver.quit()


if __name__ == '__main__':
    output_keyword()
