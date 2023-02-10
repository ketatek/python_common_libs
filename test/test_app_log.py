import pytest 
import re

import logging
from _pytest.logging import LogCaptureFixture
from logging import DEBUG, ERROR, INFO, WARNING, FATAL

from bin.common.app_log import (
    entry_log, exec_log, AppLogger
)

def test_get_default(caplog):
    """
    デフォルトロガーによるログインの検証コード

    issue:
        _pytest.logging のコードを確認したが、結果としてroot loggerが、
        キャプチャの対象となっているため、子ロガーの検証はできない模様。
        LogCaptureFixture での検証をあきらめるか、
        実装方法を再検討するか検討する。

        [ _pytest.logging ]
        https://docs.pytest.org/en/7.1.x/_modules/_pytest/logging.html#LogCaptureFixture

    Args:
        caplog (_type_): _description_
    """
    
    caplog.set_level(DEBUG, "app_log")

    logger = AppLogger.get_default()
    
    # ログ出力
    logger.debug('debaug メッセージ')
    logger.info('info メッセージ')
    logger.warning('warning メッセージ')
    logger.error('error メッセージ')
    logger.fatal('fatal メッセージ')

    pattern_fmt = '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} > app_log \[%s\] %s > %s メッセージ'
    for item in caplog.record_tuples:
        name, level, message = item

        assert 'app_log' == name

        if level == DEBUG:
            result = re.match((pattern_fmt % ('DEBUG', 'debug')), message)
            assert re.match((pattern_fmt % ('DEBUG', 'debug')), message)

        if level == INFO:
            assert re.match((pattern_fmt % ('INFO', 'info')), message)

        if level == WARNING:
            assert re.match((pattern_fmt % ('WARNING', 'warning')), message)

        if level == ERROR:
            assert re.match((pattern_fmt % ('ERROR', 'error')), message)

        if level == FATAL:
            assert re.match((pattern_fmt % ('FATAL', 'debug')), message)

def test_create_from_file(caplog: LogCaptureFixture):
    """
    loggin.jsonの設定をもとに、生成するロガーの
    出力内容の検証。

    issue:
        3種類のハンドラで出力された内容をチェックしたい。
        -> 子ロガーの検証ができないので、実装/検証方法を含め検討する。 

    Args:
        caplog (_type_): _description_
    """
    # ログレベルの設定
    caplog.set_level(DEBUG)
    # logger = logging.getLogger(__name__)
    logger = AppLogger.create_from_file("./config/logging.json")

    # ログ出力
    logger.debug('debaug メッセージ')
    logger.info('info メッセージ')
    logger.warning('warning メッセージ')
    logger.error('error メッセージ')
    logger.fatal('fatal メッセージ')

    # issue: キャプチャされないので、原因を調査。
    # dictConfigを利用していることが原因の模様。調査を進める。

    print(caplog.record_tuples)
    # pattern_fmt = '\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} > app_log \[%s\] %s > %s メッセージ'
    # for item in caplog.record_tuples:
    #     name, level, message = item

    #     assert 'app_log' == name

    #     if level == DEBUG:
    #         assert re.match((pattern_fmt % ('DEBUG', 'debug')), message)

    #     if level == INFO:
    #         assert re.match((pattern_fmt % ('INFO', 'info')), message)

    #     if level == WARNING:
    #         assert re.match((pattern_fmt % ('WARNING', 'warning')), message)

    #     if level == ERROR:
    #         assert re.match((pattern_fmt % ('ERROR', 'error')), message)

    #     if level == FATAL:
    #         assert re.match((pattern_fmt % ('FATAL', 'debug')), message)

def test_get_logger():
    pass

def test_entry_log(caplog):
    """common.app_log.entry_log デコレーターのテスト

    Args:
        caplog (LogCaptureFixture): ログキャプチャデータのfixture
    """    
    
    # ログレベルの設定
    caplog.set_level(DEBUG)

    # ログの出力実行
    entry_log('entry_log')(lambda :0)()

    # ログ出力のテスト
    assert ("entry_log", INFO, f'***** entry_log > 開始 *****') in caplog.record_tuples
    assert ("entry_log", INFO, f'***** entry_log > 終了 *****') in caplog.record_tuples

def test_exec_log(caplog):
    """common.app_log.exec_log デコレーターのテスト

    Args:
        caplog (LogCaptureFixture): ログキャプチャデータのfixture
    """

    # ログレベルの設定
    caplog.set_level(DEBUG)

    # ログの出力
    exec_log('exec_log')(lambda :0)()
    
    # ログ出力のテスト
    assert ("exec_log", INFO, f'***** exec_log - 開始 *****') in caplog.record_tuples
    assert ("exec_log", INFO, f'***** exec_log - 終了 *****') in caplog.record_tuples
    