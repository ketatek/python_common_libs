#----------------------------------------------
# * isuue:  
#   * vscodeでのpytest実行にあたり、以下のエラーで実行できていない。  
#     DLL load failed while importing _ssl: 指定されたモジュールが見つかりません。
#       * 現在原因を調査中
#----------------------------------------------
import pytest 

from ..bin.common.app_log import (
    entry_log, exec_log
)

#@entry_log('entry_log')
def test_entry_log():
    assert entry_log('test') == True

@exec_log('exec_log')
def test_entry_log():
    pass
