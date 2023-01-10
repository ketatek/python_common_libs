import pytest 

from bin.common.app_log import (
    entry_log, exec_log
)

@entry_log('entry_log')
def test_entry_log():
    pass

@exec_log('exec_log')
def test_exec_log():
    pass
