import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


URL = 'https://www.yahoo.co.jp'
URL_TITLE = 'Yahoo! JAPAN'
# 設定値
chromedriver_path = 'ChromeDriverのパス'


def main():
    '''
    メインの処理
    Yahooの検索エンジンで入力したキーワードを検索し、1番目にヒットしたページのURLを取得
    クリックしてページに遷移し、前ページに戻る
    '''

    with open('yahoo2_data.txt') as f:
        keywords = [s.rstrip() for s in f.readlines()]  # 検索キーワードが入力されたテキストファイルを読み込む

    driver = webdriver.Chrome(chromedriver_path)  # ChromeのWebDriverオブジェクトを作成
    driver.get(URL)  # Yahooのトップページを開く
    time.sleep(2)  # 2秒待機
    assert URL_TITLE in driver.title  # タイトルに'Yahoo! JAPAN'が含まれていることを確認

    urls = []
    for keyword in keywords:
        search(driver, keyword)
        urls.append(get_url(driver, keyword))

    result = []
    for url in urls:
        result.append(' : '.join(url))

    with open('yahoo2_result.txt', 'w') as f:
        f.write('\n'.join(result))  # 検索キーワードとURLをセットにしてテキストファイルに書き出す

    driver.quit()  # ブラウザを閉じる


def search(driver, keyword):
    '''
    検索テキストボックスに検索キーワードを入力し、検索する
    '''

    input_element = driver.find_element_by_name('p')  # 検索テキストボックスの要素をname属性から取得
    input_element.clear()  # 検索テキストボックスに入力されている文字列を消去
    input_element.send_keys(keyword)  # 検索テキストボックスにキーワードを入力
    input_element.send_keys(Keys.RETURN)  # Enterキーを送信
    time.sleep(2)  # 2秒待機
    assert keyword in driver.title  # タイトルにkeywordが含まれていることを確認


def get_url(driver, keyword):
    '''
    1番目にヒットしたページに遷移し、URLを取得
    '''

    number_one = []
    objects = driver.find_elements_by_css_selector('div.Algo > section > div.sw-Card__section > div.sw-Card__headerSpace > div.sw-Card__title > a')  # a要素取得
    object = objects[0]  # 1番目にヒットしたページを指定
    object.click()  # a要素をクリック
    time.sleep(2)  # 2秒待機
    number_one.append(keyword)  # 検索キーワードを追加
    number_one.append(driver.current_url)  # URLを追加
    driver.back()  # 前ページに戻る
    time.sleep(2)  # 2秒待機
    return number_one


if __name__ == '__main__':
    main()
