
from ..bin.common.app_log import (
    entry_log, exec_log
)

def test_entry_log():
    assert entry_log('test')


@exec_log('exec_log')
def test_entry_log():
    pass
