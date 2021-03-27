'''モジュール'''
import exe_amazon
import exe_yahooauc
'''標準ライブラリ'''
import multiprocessing  # 並列処理


if __name__ == '__main__':
    multiprocessing.freeze_support()
    multiprocessing.set_start_method('spawn')
    # ヤフオク（サブ）
    p_yahooauc = multiprocessing.Process(target=exe_yahooauc.main)
    p_yahooauc.start()
    # Amazon
    exe_amazon.main()
    # 終了処理
    p_yahooauc.join()
    input('情報取得完了（Enterキーで終了）')
