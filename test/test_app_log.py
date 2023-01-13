import pytest 

from logging import DEBUG, ERROR, INFO, WARNING

from bin.common.app_log import (
    entry_log, exec_log
)

def test_entry_log(caplog):
    
    # ログレベルの設定
    caplog.set_level(DEBUG)

    # ログの出力
    entry_log('entry_log')(lambda :0)()

    # ログ出力のテスト
    assert ("entry_log", INFO, f'***** entry_log > 開始 *****') in caplog.record_tuples
    assert ("entry_log", INFO, f'***** entry_log > 終了 *****') in caplog.record_tuples

def test_exec_log(caplog):

    # ログレベルの設定
    caplog.set_level(DEBUG)

    # ログの出力
    exec_log('exec_log')(lambda :0)()
    
    # ログ出力のテスト
    assert ("exec_log", INFO, f'***** exec_log - 開始 *****') in caplog.record_tuples
    assert ("exec_log", INFO, f'***** exec_log - 終了 *****') in caplog.record_tuples
    