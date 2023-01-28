#!/usr/bin/env python

#-----------------------------------------
# ログ出力関連のクラス や デコレーターを実装
# 
# * issue:
#   * ログの書式を別途定義できるようにする。
#   * 今のところエントリーポイントと、サブモジュールは、  
#   ログ出力フローに違いがないので、書式の問題を切り離せるなら、  
#   単一のデコレーターにまとめたい。  
#   * グローバルスコープを汚さない、ロガー関連の機能の提供方法を調査。
#   * 
#-------------------------------------------

import functools
import sys
import json
import __main__
from logging import (
    getLogger
    , Formatter
    , StreamHandler
    , DEBUG
)
import logging

class AppLogger():


    def create_default(self):

        logger = getLogger(__name__)
        logger.setLevel(DEBUG)

        formatter = Formatter(  
            fmt='%(asctime)s > %(name)s [%(levelname)s] %(module)s > %(message)s'
        )

        handler = StreamHandler(sys.stderr)
        handler.setLevel(DEBUG)
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)

        return logger

    def create_from_file(path: str):

        with open(path, 'rt') as f:
            config = json.load(f)
            logging.config.dictConfig(config)
        
        logger = getLogger()

        return logger

    def getLogger():
        pass
        # TBD

    def __init__(self) -> None:
        pass



def entry_log(prog_name:str):
    """バッチエントリーポイントでの実行ログ
    
    * ログ出力イメージ  
        * prog_name=xxxデータ作成  
        2022-01-01 00:00:00.000 ***** xxxデータ作成 > 開始 *****  
        2022-01-01 00:00:00.000 ***** xxxデータ作成 > 終了 *****

    Args:
        prog_name (str): コードの論理名。
    """
    def _entry_log(func):

        @functools.wraps(func)
        def _wrapper(*args, **keywords):
            
            logger = logging.getLogger(prog_name)

            try:
                logger.info(f'***** {prog_name} > 開始 *****')

                result = func(*args, **keywords)

            finally:

                logger.info(f'***** {prog_name} > 終了 *****')
                
            return result

        return _wrapper

    return _entry_log

def exec_log(func_name: str):
    """メソッド/関数での実行ログ
    
    * ログ出力イメージ  
        * func_name=xxx処理  
        2022-01-01 00:00:00.000 > xxx処理 - 開始  
        2022-01-01 00:00:00.000 > xxx処理 - 終了

    Args:
        func_name (str): コードの論理名。
    """

    def _exec_log(func):

        @functools.wraps(func)
        def _wrapper(*args, **keywords):
            
            logger = logging.getLogger(func_name)

            try:
                logger.info(f'***** {func_name} - 開始 *****')

                result = func(*args, **keywords)

            finally:

                logger.info(f'***** {func_name} - 終了 *****')
                
            return result

        return _wrapper

    return _exec_log

