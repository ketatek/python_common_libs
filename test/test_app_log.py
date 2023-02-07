import pytest 
import re

from logging import DEBUG, ERROR, INFO, WARNING, FATAL, CRITICAL

from bin.common.app_log import (
    entry_log, exec_log, AppLogger
)

def test_get_default(caplog):
    
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
            assert re.match((pattern_fmt % ('DEBUG', 'debug')), message)

        if level == INFO:
            assert re.match((pattern_fmt % ('INFO', 'info')), message)

        if level == WARNING:
            assert re.match((pattern_fmt % ('WARNING', 'warning')), message)

        if level == ERROR:
            assert re.match((pattern_fmt % ('ERROR', 'error')), message)

        if level == FATAL:
            assert re.match((pattern_fmt % ('FATAL', 'debug')), message)

def test_create_from_file():
    pass

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
    