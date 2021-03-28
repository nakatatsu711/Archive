import input_data_on_lancers
import scraping_yahoo2
import output_data_on_lancers


def lancers_search():
    '''
    メインの処理
    ランサーズの検索案件を自動化
    '''

    input_data_on_lancers.input_keyword()
    scraping_yahoo2.main()
    output_data_on_lancers.output_keyword()


if __name__ == '__main__':
    lancers_search()
