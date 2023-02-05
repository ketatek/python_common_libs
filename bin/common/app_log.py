#!/usr/bin/env python

#-----------------------------------------
# ログ出力関連のクラス や デコレーターを実装
# 
# * issue:
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

    __default_logger = None

    __logger = None

    @classmethod
    def get_default(cls):
        """デフォルトロガーを取得。
        ロガーは遅延生成。実態はクラス変数で保持。
        デフォルトロガーは、以下の設定で運用。

        * ログレベル > Debug
        * ハンドラ > 標準出力
        * 出力書式 > %(asctime)s > %(name)s [%(levelname)s] %(module)s > %(message)s

        Returns:
            logger: デフォルトのロガー
        """

        # デフォルトロガーがすでにあれば、それを返す。
        if cls.__default_logger is None:
            return cls.__default_logger

        # デフォルトロガーの生成
        cls.__default_logger = getLogger(__name__)
        logger = cls.__default_logger

        # デバッグレベルに設定
        logger.setLevel(DEBUG)

        # ログの出力書式
        formatter = Formatter(  
            fmt='%(asctime)s > %(name)s [%(levelname)s] %(module)s > %(message)s'
        )

        # 標準出力を対象にログ出力するようハンドラを設定
        handler = StreamHandler(sys.stdout)
        handler.setLevel(DEBUG)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger
    
    @classmethod
    def create_from_file(cls, path: str):
        """ロギング設定ファイル(json)をベースにした、ロガーを生成。

        Args:
            path (str): ロギング設定ファイルのパス

        Returns:
            logger:設定ファイルベースのロガー 
        """

        with open(path, 'rt') as f:
            config = json.load(f)
            logging.config.dictConfig(config)
        
        logger = getLogger()

        return logger

    @classmethod
    def getLogger(cls):
        """アプリケーション設定ファイル読込前なら、デフォルトのロガーを返す。
        
        アプリケーション設定ファイル読込後は、
        設定ファイルのロギング設定ファイルのパス(log_setting_path)があれば、
        そのパスに保存されている、設定ファイルをもとに、ロガーを生成。

        設定ファイルのロギング設定ファイルのパス(log_setting_path)がなければ、
        デフォルトのロガーを返す。
        
        また、一度ロガーが生成されたら、
        以降はクラス内に保持された、ロガーを返す。

        Returns:
           logger: 生成されたロガー
        """
        
        # 設定ファイル未読込済みなら、設定ファイルの記載の
        # ロギング設定ファイルを読込
        # if AppSettings.log_setting_path is None:
        #     return __class__.get_default()

        # ロガーがすでに生成されたされていたら、それを返す。
        if __class__.__logger is not None:
            return __class__.__logger

        # 設定ファイルベースのロガーを生成
        __class__.__logger = __class__.create_from_file()
        if __class__.__logger is None:
            # ロガーが生成されなければ、デフォルトのロガーを設定。
            __class__.__logger = __class__.get_default()

        return __class__.__logger

def entry_log(prog_name:str):
    """バッチエントリーポイントでの実行ログ
    
    * ログ出力イメージ  
        * prog_name=xxxデータ作成  
        %(asctime)s > %(name)s [%(levelname)s] %(module)s > ***** xxxデータ作成 > 開始 *****  
        %(asctime)s > %(name)s [%(levelname)s] %(module)s > ***** xxxデータ作成 > 終了 *****

    Args:
        prog_name (str): コードの論理名。
    """
    def _entry_log(func):

        @functools.wraps(func)
        def _wrapper(*args, **keywords):
            
            logger = AppLogger.getLogger()

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
        %(asctime)s > %(name)s [%(levelname)s] %(module)s > xxxデータ作成 - 開始
        %(asctime)s > %(name)s [%(levelname)s] %(module)s > xxxデータ作成 - 終了

    Args:
        func_name (str): コードの論理名。
    """

    def _exec_log(func):

        @functools.wraps(func)
        def _wrapper(*args, **keywords):
            
            logger = AppLogger.getLogger()

            try:
                logger.info(f'> {func_name} - 開始')

                result = func(*args, **keywords)

            finally:

                logger.info(f'> {func_name} - 終了')
                
            return result

        return _wrapper

    return _exec_log

