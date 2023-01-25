import pytest 

from unittest.mock import patch
from bin.common.app_args import (
    AppArgs
)

def test_get_arg_name():

    # 列挙引数名
    test_01 = AppArgs.get_arg_name("test_argument", is_option=False)
    assert test_01 == "test_argument"

    # オプション引数名
    test_02 = AppArgs.get_arg_name("test_argument", is_option=True)
    assert test_02 == "--test_argument"

def test_argument_01():

    def the_prop():
        pass

    AppArgs._AppArgs__arg_configs.clear()
    arg_config = {
        'type': str
        , 'help': 'ヘルプテキスト001'
        , 'is_optional': True
    }
    AppArgs.argument(**arg_config)(the_prop)()
    config = AppArgs._AppArgs__arg_configs[0]

    # 想定される結果データ
    assumed_data = arg_config.copy()
    assumed_data['name'] = '--the_prop' 
    del assumed_data['is_optional']

    # 登録されたデータの検証
    for key, value in assumed_data.items():
        assert config[key] == value

def test_argument_02():

    def the_prop():
        pass

    AppArgs._AppArgs__arg_configs.clear()
    arg_config = {
        'type': str
        , 'help': 'ヘルプテキスト001'
        , 'is_optional': False
    }
    AppArgs.argument(**arg_config)(the_prop)()
    config = AppArgs._AppArgs__arg_configs[0]
    
    # 想定される結果データ
    assumed_data = arg_config.copy()
    assumed_data['name'] = 'the_prop' 
    del assumed_data['is_optional']

    # 登録されたデータの検証
    for key, value in assumed_data.items():
        assert config[key] == value


def test__init__():

    def the_prop():
        pass

    AppArgs._AppArgs__arg_configs.clear()
    arg_config = {
        'type': str
        , 'help': 'ヘルプテキスト001'
        , 'is_optional': False
    }
    AppArgs.argument(**arg_config)(the_prop)()

    with patch( "sys.argv", [ "program", "test" ] ):
        test_target = AppArgs()
        assert test_target.args.the_prop == 'test'

    # issue:
    # 引数の異常ケースの検証方法が見当たらない。
    # 検証方法がわかったら検証コードを追加する。
