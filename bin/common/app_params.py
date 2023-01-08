import argparse

class AppParams():
    """
    # 起動パラメタの取扱クラス
    __init__ で argparseを利用して、アプリケーションの起動パラメタを読込み検証。  
    プロパティで読込んだパラメタにアクセスできるよう実装している。  
    dictを継承すれば、この実装自体必要ないかもしれないが、
    エディタのオートコンプリートが動作しないため、この実装が妥当か？要調査。
    """

    __params = {}
    """
    パラメタ格納先
    """

    @property
    def param_a(self) -> str:
        return self.__params.param_a

    @property
    def param_b(self) -> int:
        return self.__params.param_b

    @property
    def param_c(self) -> str:
        return self.__params.param_c

    def __init__(self) -> None:
        
        parser = argparse.ArgumentParser(prog="プログラム名")

        # 列挙式パラメタ - 文字型
        parser.add_argument('params_a', type=str, help='パラメタ説明')

        # 列挙式パラメタ - 数値
        parser.add_argument('params_b', type=int, help='パラメタ説明')

        # 列挙式パラメタ - カスタム型
        parser.add_argument('params_c', type=in, help='パラメタ説明')

        # オプションパラメタ
        parser.add_argument('--option_a', help='パラメタ説明')

        # オプションパラメタ - デフォルト指定
        parser.add_argument('--option_b', default='option_b', help='パラメタ説明')

        # オプションパラメタ - フラグ式
        parser.add_argument('--option_c', action='store_true' help='パラメタ説明')
        
        # オプションパラメタ - 選択式
        parser.add_argument('--option_d', choices=['rice', 'bread', 'nan'], help='パラメタ説明')

        # オプションパラメタ - 必須
        parser.add_argument('--option_e', required=True, help='パラメタ説明')

        self.__params = parser.parse_args()
