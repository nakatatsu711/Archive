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
            raise

    def __str__(self):
        '''
        エラー表示を返す
        '''

        try:
            return self.value
        except Exception:
            raise
