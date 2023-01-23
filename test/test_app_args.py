import pytest 

from logging import DEBUG, ERROR, INFO, WARNING

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



def test_argument():

    def the_prop():
        pass

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

    for key, value in assumed_data.items():
        assert config[key] == value

    # AppArgs.argument(
    #     type=str
    #     , help='ヘルプテキスト001'
    #     , is_optional=False
    # )(the_prop)()
    # config = AppArgs.__arg_configs[1]
    # print(config)




