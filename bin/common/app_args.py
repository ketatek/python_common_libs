import functools
from typing import Callable, TypeVar, Union
from argparse import FileType, ArgumentParser, HelpFormatter

_T = TypeVar("_T")

class AppArgs():

    # argument 設定リスト
    __arg_configs = []

    @classmethod
    def get_arg_name(cls, name: str, is_option: bool) -> str:
        """argument 名を取得

        Args:
            name (str): ベースとなる argument 名
            is_option (bool): True を指定した場合、prefixに '--' を追加

        Returns:
            str: argument 名
        """
        return name if not is_option else f'--{name}'
    
    @classmethod
    def argument(
        cls,
        type: Union[Callable[[str], _T] , FileType] = ...,
        help: str = ...,
        is_optional: bool=False,
    ):
        """プログラムのargumentを定義するデコレーター。
        argumentをマッピングするクラスの、プロパティに付加して使用する。

        argumentの登録は、ArgumentParser.add_argumentに委譲するため、
        このデコレーターの引数は、ArgumentParser.add_argumentのものをサポートする。
        現在は、type/helpのみ。今後追加する予定。
        
        argment name は、デコレーターの付加先のプロパティ名から設定される。
        example: 
            class ArgMapCls():
                @AppArgs.argument(type=str, help="sample", is_optional=True)
                @property
                def sample_arg() -> str:
                    pass
            --
            オプション引数名 -> --sample_arg

        Args:
            type (Union[Callable[[str], _T] , FileType], optional): 
                ArgumentParser.add_argument の type に対応。 Defaults to ....
            help (str, optional):
                ArgumentParser.add_argument の help に対応。。 Defaults to ....
            is_optional (bool, optional):
                True指定の場合、オプション引数として登録される。
                argument name のprefixに、'--'が付与される。
                [example]test_arg -> --test_arg
                Defaults to False.
        """

        def _argument(func):

            cls.__arg_configs.append(
                {
                    "name":cls.get_arg_name(func.__name__, is_optional), 
                    "type":type, 
                    "help":help
                }
            )

            @functools.wraps(func)
            def _wrapper(*args, **keywords):                
                result = func(*args, **keywords)
                return result

            return _wrapper

        return _argument

    def __init__(self) -> None:
        """
        インスタンスの初期化
        """
        for arg_item in type(self).__arg_configs:
            
            # パラメタの追加
            self._parser.add_argument(
                arg_item["name"], 
                type=arg_item["type"], 
                help=arg_item["help"],
            )

        # argument のパース実行
        self.__args = self._parse()

    @property
    def _parser(self) -> ArgumentParser:
        """
        ArgumentParser を返す。
        ArgumentParserは、本プロパティを利用することで、遅延生成する。
        
        Returns:
            ArgumentParser: arugumentのパース結果用の ArgumentParser
        """
        if not hasattr(self, "_AppArgs__argParser"):
           self.__argParser = self._setup_perser()

        return self.__argParser

    @property
    def args(self) -> dict:
        """
        argument の パース結果

        Returns:
            argparse.Namespace: arugumentのパース結果。
        """
        return self.__args 

    def _setup_perser(self) -> ArgumentParser:
        """
        ArgumentParserを生成して返す。
        ヘルパメッセージなどの カスタマイズが必要な場合は、
        本メソッドをオーバーライドして、カスタマイズする。

        Returns:
            ArgumentParser: 生成した ArgumentParser
        """
        return ArgumentParser()  

    def _parse(self) -> dict:
        """
        ArgumentParser.parse_args の 結果を返す。

        Returns:
            argparse.Namespace: arugumentのパース結果。
        """
        return self._parser.parse_args()
