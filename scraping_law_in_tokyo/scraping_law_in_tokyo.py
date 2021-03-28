import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests


base_url = 'http://www.legal-findoffice.com/cat/all/tokyo/'


def main():
    '''
    メインの処理
    法律事務所・検索＆口コミサイトから情報を収集
    「東京都」で絞り込む
    '''

    # Webページを取得し、BeautifulSoupオブジェクトを生成
    r = requests.get(base_url)
    soup = BeautifulSoup(r.content, 'lxml')

    # 各事務所の詳細ページに遷移するためのURLを取得
    laws = []
    page_num = 1
    while True:
        laws = scrape_page(laws, soup)
        next_page = ''
        for page in soup.select('#content > div.list_navi > span > a'):
            if page.text == str(page_num + 1):
                next_page = urljoin(base_url, page.get('href'))
                page_num += 1
                time.sleep(1)
                r = requests.get(next_page)
                soup = BeautifulSoup(r.content, 'lxml')
                break  # 次ページの情報を取得したらfor文をbreak
        if not next_page:
            break  # 最後のページならwhile文をbreak
    print('got', len(laws), 'results')  # 取得事務所数を表示

    # 各事務所の詳細ページに遷移し、詳細情報を取得
    list_num = 0
    for dict in laws:
        laws = get_info(dict['url'], laws, list_num)
        list_num += 1

        # 途中経過を表示
        if list_num % 100 == 0:
            print(list_num, 'completed')

    # 取得した詳細情報をテキストファイルに書き出す
    # 上から「事務所名」、「住所」、「電話番号」、「FAX番号」、「ホームページURL」
    with open('law_in_tokyo.txt', 'w') as f:
        f.write('上から順に「事務所名」，「住所」，「電話番号」，「FAX番号」，「ホームページURL」\n')
        f.write('\n')
        for law in laws:
            f.write(law['name'])
            f.write('\n')
            f.write(law['address'])
            f.write('\n')
            f.write(law['tel'])
            f.write('\n')
            f.write(law['fax'])
            f.write('\n')
            f.write(law['url'])
            f.write('\n\n')

    # 終了報告
    print('success')


def scrape_page(laws, soup):
    '''
    各事務所の詳細ページに遷移するためのURLを取得
    '''

    a_objects_1 = soup.select('#content > div.list_recommend > h3 > a')  # パターン1
    if a_objects_1:
        laws = get_laws_list(a_objects_1, laws)

    a_objects_2 = soup.select('#content > div.list_owner > div.info_img > h3 > a')  # パターン2
    if a_objects_2:
        laws = get_laws_list(a_objects_2, laws)

    a_objects_3 = soup.select('#content > div.list_user > h3 > a')  # パターン3
    if a_objects_3:
        laws = get_laws_list(a_objects_3, laws)

    a_objects_4 = soup.select('#content > div.list_owner > h3 > a')  # パターン4
    if a_objects_4:
        laws = get_laws_list(a_objects_4, laws)

    # 途中経過を表示
    if len(laws) % 100 == 0:
        print(len(laws), 'completed')

    return laws


def get_laws_list(a_objects, laws):
    '''
    事務所名と詳細ページURLを返す
    '''

    # 'name'と'url'をキーとしてdictにまとめ、リストに追加
    join_list = ''  # join_listを定義
    for a in a_objects:
        if 'group' in a.get('href'):  # 詳細ページのa要素が二つに分かれている場合に対応（URLに'group'を含むものを除外）
            join_list = a.text
            continue
        laws.append({'name': join_list + a.text, 'url': urljoin(base_url, a.get('href'))})
        join_list = ''  # リストに追加したらjoin_listを空にする
    return laws


def get_info(url, laws, list_num):
    '''
    詳細ページに遷移し、詳細情報を取得
    '''

    # 詳細ページ情報を取得し、BeautifulSoupオブジェクトを生成
    time.sleep(1)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')

    # 詳細情報を取得
    i = 0
    infos = soup.select('table.detail td.cell')
    for info in infos:
        if i not in [0, 2, 3, 7]:  # 「住所」、「電話番号」、「FAX番号」、「ホームページURL」以外の情報は取得しない
            i += 1
            continue

        # 「住所」の場合
        if i == 0:
            laws = empty_process('address', info, laws, list_num)

        # 「電話番号」の場合
        elif i == 2:
            laws = empty_process('tel', info, laws, list_num)

        # 「FAX番号」の場合
        elif i == 3:
            laws = empty_process('fax', info, laws, list_num)

        # 「ホームページURL」の場合
        elif i == 7:
            laws = empty_process('url', info, laws, list_num)

        i += 1

    return laws


def empty_process(key, info, laws, list_num):
    '''
    記載されていない場合の処理
    '''

    # 記載されていない場合は、「不明」と入力する
    if not info.text.strip():
        laws[list_num][key] = '不明'
    else:
        laws[list_num][key] = info.text.strip()
    return laws


if __name__ == '__main__':
    main()
